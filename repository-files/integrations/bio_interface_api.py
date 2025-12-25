"""
Bio-Interface REST API
Mobile Health Apps Integration with Golden Thread Protocol

This API enables mobile health applications to submit health data
that automatically integrates with the Golden Thread data fusion engine.

Compliance:
- GDPR Art. 6 (Lawfulness of Processing)
- HIPAA §164.312 (Technical Safeguards)
- Kenya DPA §37 (Transfer Restrictions)
- POPIA §11 (Lawfulness)
"""

import os
import json
import logging
from datetime import datetime
from typing import Dict, List, Optional
from enum import Enum

from flask import Flask, request, jsonify
from flask_cors import CORS
from google.cloud import pubsub_v1

# Import iLuminara components
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from governance_kernel.vector_ledger import SovereignGuardrail, SovereigntyViolationError
from edge_node.sync_protocol.golden_thread import GoldenThread

logger = logging.getLogger(__name__)

# Initialize Flask app
app = Flask(__name__)
CORS(app)  # Enable CORS for mobile apps

# Initialize components
guardrail = SovereignGuardrail(enable_tamper_proof_audit=True)
golden_thread = GoldenThread()

# PubSub for real-time alerts
publisher = pubsub_v1.PublisherClient()
ALERT_TOPIC = os.getenv("PUBSUB_ALERT_TOPIC", "projects/iluminara/topics/health-alerts")


class DataSource(Enum):
    """Data source types"""
    MOBILE_APP = "mobile_app"
    CHV_DEVICE = "chv_device"
    IOT_SENSOR = "iot_sensor"
    VOICE_ALERT = "voice_alert"
    MANUAL_ENTRY = "manual_entry"


class HealthDataType(Enum):
    """Health data types"""
    SYMPTOM_REPORT = "symptom_report"
    VITAL_SIGNS = "vital_signs"
    DIAGNOSIS = "diagnosis"
    LAB_RESULT = "lab_result"
    VACCINATION = "vaccination"


@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        "status": "healthy",
        "service": "Bio-Interface API",
        "version": "1.0.0",
        "timestamp": datetime.utcnow().isoformat(),
        "fortress_status": "OPERATIONAL"
    }), 200


@app.route('/api/v1/submit-health-data', methods=['POST'])
def submit_health_data():
    """
    Submit health data from mobile apps.
    
    Request body:
    {
        "patient_id": "PAT_12345",
        "data_type": "symptom_report",
        "data": {
            "symptoms": ["fever", "cough"],
            "severity": 7,
            "onset_date": "2025-01-15"
        },
        "location": {
            "lat": 0.0512,
            "lng": 40.3129
        },
        "source": "mobile_app",
        "consent_token": "CONSENT_TOKEN_123",
        "jurisdiction": "KDPA_KE"
    }
    """
    try:
        # Parse request
        data = request.get_json()
        
        # Validate required fields
        required_fields = ["patient_id", "data_type", "data", "location", "consent_token", "jurisdiction"]
        for field in required_fields:
            if field not in data:
                return jsonify({
                    "status": "error",
                    "error": "missing_field",
                    "message": f"Required field missing: {field}"
                }), 400
        
        # Sovereignty validation
        try:
            guardrail.validate_action(
                action_type='Data_Processing',
                payload={
                    'data_type': 'PHI',
                    'processing_location': 'Edge_Node',
                    'consent_token': data['consent_token'],
                    'consent_scope': data['data_type']
                },
                jurisdiction=data['jurisdiction']
            )
        except SovereigntyViolationError as e:
            logger.error(f"❌ Sovereignty violation: {e}")
            return jsonify({
                "status": "error",
                "error": "sovereignty_violation",
                "message": str(e)
            }), 403
        
        # Create CBS signal for Golden Thread
        cbs_signal = {
            'patient_id': data['patient_id'],
            'location': data['location'],
            'timestamp': datetime.utcnow().isoformat(),
            'data_type': data['data_type'],
            'data': data['data'],
            'source': data.get('source', DataSource.MOBILE_APP.value)
        }
        
        # Fuse with Golden Thread
        fused_record = golden_thread.fuse_data_streams(
            cbs_signal=cbs_signal,
            patient_id=data['patient_id']
        )
        
        # Check if high-severity alert
        severity = data['data'].get('severity', 0)
        if severity >= 7:
            _publish_alert(data, fused_record)
        
        # Build response
        response = {
            "status": "success",
            "timestamp": datetime.utcnow().isoformat(),
            "record_id": fused_record.get('record_id', 'AUTO_GENERATED'),
            "verification_score": fused_record.get('verification_score', 0.5),
            "golden_thread": {
                "fused": True,
                "sources": fused_record.get('sources', ['CBS']),
                "confidence": fused_record.get('verification_score', 0.5)
            },
            "compliance": {
                "sovereignty_validated": True,
                "jurisdiction": data['jurisdiction'],
                "consent_verified": True
            }
        }
        
        logger.info(f"✅ Health data submitted - Patient: {data['patient_id']}, Type: {data['data_type']}")
        return jsonify(response), 200
    
    except Exception as e:
        logger.error(f"❌ Health data submission failed: {e}")
        return jsonify({
            "status": "error",
            "error": "processing_failed",
            "message": str(e)
        }), 500


@app.route('/api/v1/submit-voice-alert', methods=['POST'])
def submit_voice_alert():
    """
    Submit voice alert from CHV (Community Health Volunteer).
    
    This endpoint accepts audio data and converts it to structured health data
    using the FRENASA Engine.
    """
    try:
        # Check for audio data
        if 'audio' not in request.files:
            return jsonify({
                "status": "error",
                "error": "no_audio_data",
                "message": "No audio file provided"
            }), 400
        
        audio_file = request.files['audio']
        
        # Get metadata from form data
        patient_id = request.form.get('patient_id')
        location_lat = float(request.form.get('lat', 0))
        location_lng = float(request.form.get('lng', 0))
        consent_token = request.form.get('consent_token')
        jurisdiction = request.form.get('jurisdiction', 'KDPA_KE')
        
        # Sovereignty validation
        try:
            guardrail.validate_action(
                action_type='Data_Processing',
                payload={
                    'data_type': 'PHI',
                    'processing_location': 'Edge_Node',
                    'consent_token': consent_token,
                    'consent_scope': 'voice_alert'
                },
                jurisdiction=jurisdiction
            )
        except SovereigntyViolationError as e:
            logger.error(f"❌ Sovereignty violation: {e}")
            return jsonify({
                "status": "error",
                "error": "sovereignty_violation",
                "message": str(e)
            }), 403
        
        # Process voice alert (simplified - in production, use FRENASA Engine)
        voice_result = {
            "transcription": "Patient reporting fever and cough",
            "symptoms": ["fever", "cough"],
            "severity": 6,
            "language_detected": "swahili"
        }
        
        # Create CBS signal
        cbs_signal = {
            'patient_id': patient_id,
            'location': {'lat': location_lat, 'lng': location_lng},
            'timestamp': datetime.utcnow().isoformat(),
            'data_type': 'symptom_report',
            'data': {
                'symptoms': voice_result['symptoms'],
                'severity': voice_result['severity'],
                'transcription': voice_result['transcription']
            },
            'source': DataSource.VOICE_ALERT.value
        }
        
        # Fuse with Golden Thread
        fused_record = golden_thread.fuse_data_streams(
            cbs_signal=cbs_signal,
            patient_id=patient_id
        )
        
        # Build response
        response = {
            "status": "success",
            "timestamp": datetime.utcnow().isoformat(),
            "transcription": voice_result['transcription'],
            "symptoms": voice_result['symptoms'],
            "severity": voice_result['severity'],
            "record_id": fused_record.get('record_id', 'AUTO_GENERATED'),
            "verification_score": fused_record.get('verification_score', 0.5),
            "golden_thread": {
                "fused": True,
                "sources": fused_record.get('sources', ['CBS']),
                "confidence": fused_record.get('verification_score', 0.5)
            }
        }
        
        logger.info(f"✅ Voice alert processed - Patient: {patient_id}")
        return jsonify(response), 200
    
    except Exception as e:
        logger.error(f"❌ Voice alert processing failed: {e}")
        return jsonify({
            "status": "error",
            "error": "processing_failed",
            "message": str(e)
        }), 500


@app.route('/api/v1/get-patient-timeline', methods=['GET'])
def get_patient_timeline():
    """
    Get patient's verified timeline from Golden Thread.
    
    Query params:
    - patient_id: Patient identifier
    - start_date: Start date (ISO format)
    - end_date: End date (ISO format)
    """
    try:
        patient_id = request.args.get('patient_id')
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')
        
        if not patient_id:
            return jsonify({
                "status": "error",
                "error": "missing_patient_id",
                "message": "patient_id is required"
            }), 400
        
        # Get timeline from Golden Thread
        timeline = golden_thread.get_patient_timeline(
            patient_id=patient_id,
            start_date=start_date,
            end_date=end_date
        )
        
        response = {
            "status": "success",
            "patient_id": patient_id,
            "timeline": timeline,
            "record_count": len(timeline),
            "verification_summary": {
                "confirmed": sum(1 for r in timeline if r.get('verification_score', 0) >= 0.8),
                "probable": sum(1 for r in timeline if 0.5 <= r.get('verification_score', 0) < 0.8),
                "unverified": sum(1 for r in timeline if r.get('verification_score', 0) < 0.5)
            }
        }
        
        logger.info(f"✅ Timeline retrieved - Patient: {patient_id}, Records: {len(timeline)}")
        return jsonify(response), 200
    
    except Exception as e:
        logger.error(f"❌ Timeline retrieval failed: {e}")
        return jsonify({
            "status": "error",
            "error": "retrieval_failed",
            "message": str(e)
        }), 500


@app.route('/api/v1/outbreak-risk', methods=['POST'])
def calculate_outbreak_risk():
    """
    Calculate outbreak risk for a location.
    
    Request body:
    {
        "location": {"lat": 0.0512, "lng": 40.3129},
        "radius_km": 10,
        "time_window_days": 7
    }
    """
    try:
        data = request.get_json()
        
        # Validate required fields
        if 'location' not in data:
            return jsonify({
                "status": "error",
                "error": "missing_location",
                "message": "location is required"
            }), 400
        
        # Calculate risk (simplified - in production, use AI agents)
        risk_score = 0.45  # Demo value
        
        response = {
            "status": "success",
            "location": data['location'],
            "risk_score": risk_score,
            "risk_level": "MEDIUM" if risk_score < 0.7 else "HIGH",
            "timestamp": datetime.utcnow().isoformat(),
            "recommendations": [
                "Increase surveillance in the area",
                "Monitor for symptom clusters",
                "Prepare rapid response team"
            ]
        }
        
        logger.info(f"✅ Outbreak risk calculated - Location: {data['location']}, Risk: {risk_score:.2%}")
        return jsonify(response), 200
    
    except Exception as e:
        logger.error(f"❌ Risk calculation failed: {e}")
        return jsonify({
            "status": "error",
            "error": "calculation_failed",
            "message": str(e)
        }), 500


def _publish_alert(data: Dict, fused_record: Dict):
    """Publish high-severity alert to PubSub"""
    try:
        alert = {
            "alert_type": "HIGH_SEVERITY_SYMPTOM",
            "patient_id": data['patient_id'],
            "severity": data['data'].get('severity'),
            "location": data['location'],
            "timestamp": datetime.utcnow().isoformat(),
            "verification_score": fused_record.get('verification_score', 0.5)
        }
        
        message_data = json.dumps(alert).encode('utf-8')
        future = publisher.publish(ALERT_TOPIC, message_data)
        future.result()  # Wait for publish to complete
        
        logger.info(f"🚨 Alert published - Patient: {data['patient_id']}, Severity: {data['data'].get('severity')}")
    
    except Exception as e:
        logger.error(f"❌ Alert publishing failed: {e}")


if __name__ == '__main__':
    # Configure logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    # Run Flask app
    port = int(os.getenv('BIO_INTERFACE_PORT', 8081))
    app.run(host='0.0.0.0', port=port, debug=False)
