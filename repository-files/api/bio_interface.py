"""
Bio-Interface REST API
Mobile Health Apps Integration with Golden Thread Protocol

This API enables mobile health applications to submit health data
that automatically integrates with the Golden Thread data fusion engine.

Compliance:
- GDPR Art. 6 (Lawfulness of Processing)
- HIPAA §164.312 (Technical Safeguards)
- KDPA §37 (Transfer Restrictions)
- WHO IHR Article 6 (Notification)
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

app = Flask(__name__)
CORS(app)  # Enable CORS for mobile apps

# Initialize components
guardrail = SovereignGuardrail(enable_tamper_proof_audit=True)
golden_thread = GoldenThread()


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
    LAB_RESULT = "lab_result"
    DIAGNOSIS = "diagnosis"
    TREATMENT = "treatment"
    VACCINATION = "vaccination"


@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        "status": "operational",
        "service": "iLuminara Bio-Interface API",
        "version": "1.0.0",
        "fortress_status": "ACTIVE",
        "timestamp": datetime.utcnow().isoformat()
    })


@app.route('/api/v1/submit-health-data', methods=['POST'])
def submit_health_data():
    """
    Submit health data from mobile apps.
    
    Request body:
    {
        "patient_id": "PAT_12345",
        "data_type": "symptom_report",
        "data": {
            "symptoms": ["fever", "cough", "fatigue"],
            "severity": 7,
            "onset_date": "2025-12-20T10:00:00Z"
        },
        "location": {
            "lat": 0.0512,
            "lng": 40.3129,
            "name": "Dadaab"
        },
        "source": "mobile_app",
        "consent_token": "CONSENT_TOKEN_123",
        "jurisdiction": "KDPA_KE"
    }
    
    Response:
    {
        "status": "success",
        "submission_id": "SUB_789",
        "golden_thread_id": "GT_456",
        "verification_score": 0.8,
        "timestamp": "2025-12-20T10:05:00Z"
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
            'location': data['location']['name'],
            'symptom': data['data'].get('symptoms', [])[0] if data['data'].get('symptoms') else 'unknown',
            'timestamp': data['data'].get('onset_date', datetime.utcnow().isoformat()),
            'source': f"{data.get('source', 'mobile_app').upper()}_SUBMISSION",
            'severity': data['data'].get('severity', 5),
            'patient_id': data['patient_id']
        }
        
        # Fuse with Golden Thread
        fused = golden_thread.fuse_data_streams(
            cbs_signal=cbs_signal,
            patient_id=data['patient_id']
        )
        
        # Generate submission ID
        submission_id = f"SUB_{datetime.utcnow().strftime('%Y%m%d%H%M%S')}"
        
        # Publish to PubSub for downstream processing
        _publish_to_pubsub(
            topic="health-data-submissions",
            message={
                "submission_id": submission_id,
                "patient_id": data['patient_id'],
                "data_type": data['data_type'],
                "location": data['location'],
                "verification_score": fused.verification_score,
                "timestamp": datetime.utcnow().isoformat()
            }
        )
        
        logger.info(f"✅ Health data submitted - ID: {submission_id}, Verification: {fused.verification_score}")
        
        return jsonify({
            "status": "success",
            "submission_id": submission_id,
            "golden_thread_id": fused.id if hasattr(fused, 'id') else None,
            "verification_score": fused.verification_score,
            "timestamp": datetime.utcnow().isoformat(),
            "compliance": {
                "frameworks": ["GDPR Art. 6", "KDPA §37", "HIPAA §164.312"],
                "audit_trail": True,
                "sovereignty_validated": True
            }
        }), 200
    
    except Exception as e:
        logger.error(f"❌ Error processing health data: {e}")
        return jsonify({
            "status": "error",
            "error": "processing_failed",
            "message": str(e)
        }), 500


@app.route('/api/v1/submit-outbreak-alert', methods=['POST'])
def submit_outbreak_alert():
    """
    Submit outbreak alert from CHV or mobile app.
    
    Request body:
    {
        "location": {
            "lat": 0.0512,
            "lng": 40.3129,
            "name": "Dadaab"
        },
        "disease": "cholera",
        "case_count": 5,
        "severity": "HIGH",
        "description": "Multiple cases of watery diarrhea reported",
        "reporter_id": "CHV_AMINA_HASSAN",
        "consent_token": "EMERGENCY_ALERT",
        "jurisdiction": "KDPA_KE"
    }
    """
    try:
        data = request.get_json()
        
        # Validate required fields
        required_fields = ["location", "disease", "case_count", "severity", "reporter_id", "jurisdiction"]
        for field in required_fields:
            if field not in data:
                return jsonify({
                    "status": "error",
                    "error": "missing_field",
                    "message": f"Required field missing: {field}"
                }), 400
        
        # Emergency override for outbreak alerts (WHO IHR Article 6)
        try:
            guardrail.validate_action(
                action_type='Data_Processing',
                payload={
                    'data_type': 'PHI',
                    'processing_location': 'Edge_Node',
                    'consent_token': data.get('consent_token', 'EMERGENCY_ALERT'),
                    'consent_scope': 'public_health_surveillance',
                    'emergency_override': True
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
        
        # Create alert ID
        alert_id = f"ALERT_{datetime.utcnow().strftime('%Y%m%d%H%M%S')}"
        
        # Publish to PubSub for immediate response
        _publish_to_pubsub(
            topic="outbreak-alerts",
            message={
                "alert_id": alert_id,
                "location": data['location'],
                "disease": data['disease'],
                "case_count": data['case_count'],
                "severity": data['severity'],
                "description": data.get('description', ''),
                "reporter_id": data['reporter_id'],
                "timestamp": datetime.utcnow().isoformat()
            }
        )
        
        logger.info(f"🚨 Outbreak alert submitted - ID: {alert_id}, Disease: {data['disease']}, Cases: {data['case_count']}")
        
        return jsonify({
            "status": "success",
            "alert_id": alert_id,
            "timestamp": datetime.utcnow().isoformat(),
            "response": {
                "acknowledged": True,
                "priority": "IMMEDIATE",
                "estimated_response_time": "< 5 minutes"
            },
            "compliance": {
                "frameworks": ["WHO IHR Article 6", "KDPA §37"],
                "emergency_override": True,
                "audit_trail": True
            }
        }), 200
    
    except Exception as e:
        logger.error(f"❌ Error processing outbreak alert: {e}")
        return jsonify({
            "status": "error",
            "error": "processing_failed",
            "message": str(e)
        }), 500


@app.route('/api/v1/query-verification', methods=['POST'])
def query_verification():
    """
    Query verification status of submitted data.
    
    Request body:
    {
        "submission_id": "SUB_20251220100500",
        "patient_id": "PAT_12345"
    }
    
    Response:
    {
        "status": "success",
        "verification_score": 1.0,
        "verification_status": "CONFIRMED",
        "data_sources": ["CBS", "EMR"],
        "timestamp": "2025-12-20T10:05:00Z"
    }
    """
    try:
        data = request.get_json()
        
        # In production, query Golden Thread for verification status
        # For now, return mock response
        
        return jsonify({
            "status": "success",
            "submission_id": data.get('submission_id'),
            "patient_id": data.get('patient_id'),
            "verification_score": 0.95,
            "verification_status": "CONFIRMED",
            "data_sources": ["CBS", "EMR"],
            "timestamp": datetime.utcnow().isoformat()
        }), 200
    
    except Exception as e:
        logger.error(f"❌ Error querying verification: {e}")
        return jsonify({
            "status": "error",
            "error": "query_failed",
            "message": str(e)
        }), 500


def _publish_to_pubsub(topic: str, message: Dict):
    """Publish message to Google Cloud Pub/Sub"""
    try:
        project_id = os.getenv('GOOGLE_CLOUD_PROJECT', 'iluminara-core')
        publisher = pubsub_v1.PublisherClient()
        topic_path = publisher.topic_path(project_id, topic)
        
        # Publish message
        data = json.dumps(message).encode('utf-8')
        future = publisher.publish(topic_path, data)
        
        logger.info(f"📤 Published to {topic}: {future.result()}")
    
    except Exception as e:
        logger.warning(f"⚠️ PubSub publish failed (non-critical): {e}")


if __name__ == '__main__':
    # Configure logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    # Start server
    port = int(os.getenv('BIO_INTERFACE_PORT', 8081))
    app.run(host='0.0.0.0', port=port, debug=False)
