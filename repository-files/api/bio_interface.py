"""
Bio-Interface REST API
Mobile Health Apps integration with Golden Thread protocol

This API enables mobile health applications to submit health data
that automatically integrates with the Golden Thread data fusion engine.

Compliance:
- GDPR Art. 6 (Lawfulness of Processing)
- HIPAA §164.312 (Technical Safeguards)
- Kenya DPA §37 (Transfer Restrictions)
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
from typing import Dict, Optional
import logging
from datetime import datetime
from dataclasses import dataclass, asdict
import hashlib

# Import iLuminara components
import sys
sys.path.append('..')
from governance_kernel.vector_ledger import SovereignGuardrail, SovereigntyViolationError
from edge_node.sync_protocol.golden_thread import GoldenThread

logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app)  # Enable CORS for mobile apps

# Initialize components
guardrail = SovereignGuardrail(enable_tamper_proof_audit=True)
golden_thread = GoldenThread()


@dataclass
class HealthDataSubmission:
    """Health data submission from mobile app"""
    patient_id: str
    location: Dict[str, float]
    symptoms: list
    vital_signs: Optional[Dict[str, float]]
    timestamp: str
    source: str
    consent_token: str
    device_id: str


@dataclass
class SubmissionResponse:
    """Response to health data submission"""
    status: str
    submission_id: str
    verification_score: float
    golden_thread_status: str
    compliance_status: str
    timestamp: str
    message: str


@app.route('/health', methods=['GET'])
def health_check():
    """
    Health check endpoint
    """
    return jsonify({
        'status': 'healthy',
        'service': 'iLuminara Bio-Interface',
        'version': '1.0.0',
        'timestamp': datetime.utcnow().isoformat(),
        'components': {
            'sovereign_guardrail': 'operational',
            'golden_thread': 'operational',
            'audit_trail': 'operational'
        }
    })


@app.route('/api/v1/submit-health-data', methods=['POST'])
def submit_health_data():
    """
    Submit health data from mobile app.
    
    Request body:
    {
        "patient_id": "PAT_12345",
        "location": {"lat": 0.0512, "lng": 40.3129},
        "symptoms": ["fever", "cough", "fatigue"],
        "vital_signs": {"temperature": 38.5, "heart_rate": 95},
        "timestamp": "2025-12-25T10:00:00Z",
        "source": "mobile_app_v2.1",
        "consent_token": "CONSENT_TOKEN_ABC123",
        "device_id": "DEVICE_XYZ789"
    }
    
    Returns:
    {
        "status": "success",
        "submission_id": "SUB_ABC123",
        "verification_score": 0.8,
        "golden_thread_status": "PROBABLE",
        "compliance_status": "COMPLIANT",
        "timestamp": "2025-12-25T10:00:01Z",
        "message": "Health data submitted successfully"
    }
    """
    try:
        # Parse request
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['patient_id', 'location', 'symptoms', 'timestamp', 'consent_token', 'device_id']
        for field in required_fields:
            if field not in data:
                return jsonify({
                    'status': 'error',
                    'error': 'missing_field',
                    'message': f'Required field missing: {field}'
                }), 400
        
        # Create submission object
        submission = HealthDataSubmission(
            patient_id=data['patient_id'],
            location=data['location'],
            symptoms=data['symptoms'],
            vital_signs=data.get('vital_signs'),
            timestamp=data['timestamp'],
            source=data.get('source', 'mobile_app'),
            consent_token=data['consent_token'],
            device_id=data['device_id']
        )
        
        # Step 1: Sovereignty validation
        try:
            guardrail.validate_action(
                action_type='Data_Processing',
                payload={
                    'data_type': 'PHI',
                    'processing_location': 'Edge_Node',
                    'consent_token': submission.consent_token,
                    'consent_scope': 'public_health_surveillance',
                    'patient_id': submission.patient_id
                },
                jurisdiction='KDPA_KE'
            )
            compliance_status = "COMPLIANT"
        except SovereigntyViolationError as e:
            logger.error(f"❌ Sovereignty violation: {e}")
            return jsonify({
                'status': 'error',
                'error': 'sovereignty_violation',
                'message': str(e)
            }), 403
        
        # Step 2: Create CBS signal
        cbs_signal = {
            'location': submission.location,
            'symptom': submission.symptoms[0] if submission.symptoms else 'unknown',
            'timestamp': submission.timestamp,
            'source': f'CBS_MOBILE_{submission.device_id}',
            'vital_signs': submission.vital_signs
        }
        
        # Step 3: Fuse with Golden Thread
        # Note: In production, this would check for matching EMR records
        fused = golden_thread.fuse_data_streams(
            cbs_signal=cbs_signal,
            patient_id=submission.patient_id
        )
        
        # Step 4: Generate submission ID
        submission_id = hashlib.sha256(
            f"{submission.patient_id}{submission.timestamp}".encode()
        ).hexdigest()[:16].upper()
        
        # Step 5: Determine verification status
        if fused.verification_score >= 0.8:
            golden_thread_status = "CONFIRMED"
        elif fused.verification_score >= 0.6:
            golden_thread_status = "PROBABLE"
        elif fused.verification_score >= 0.4:
            golden_thread_status = "POSSIBLE"
        else:
            golden_thread_status = "UNVERIFIED"
        
        # Step 6: Create response
        response = SubmissionResponse(
            status='success',
            submission_id=f"SUB_{submission_id}",
            verification_score=fused.verification_score,
            golden_thread_status=golden_thread_status,
            compliance_status=compliance_status,
            timestamp=datetime.utcnow().isoformat(),
            message='Health data submitted successfully'
        )
        
        logger.info(f"✅ Health data submitted - ID: {response.submission_id}, Score: {fused.verification_score:.2f}")
        
        return jsonify(asdict(response)), 200
    
    except Exception as e:
        logger.error(f"❌ Submission failed: {e}")
        return jsonify({
            'status': 'error',
            'error': 'processing_failed',
            'message': str(e)
        }), 500


@app.route('/api/v1/verify-consent', methods=['POST'])
def verify_consent():
    """
    Verify consent token validity.
    
    Request body:
    {
        "patient_id": "PAT_12345",
        "consent_token": "CONSENT_TOKEN_ABC123",
        "consent_scope": "public_health_surveillance"
    }
    
    Returns:
    {
        "status": "valid",
        "patient_id": "PAT_12345",
        "consent_scope": "public_health_surveillance",
        "expires_at": "2026-12-25T10:00:00Z"
    }
    """
    try:
        data = request.get_json()
        
        # Validate consent
        try:
            guardrail.validate_action(
                action_type='Consent_Validation',
                payload={
                    'consent_token': data['consent_token'],
                    'consent_scope': data['consent_scope'],
                    'patient_id': data['patient_id']
                },
                jurisdiction='KDPA_KE'
            )
            
            return jsonify({
                'status': 'valid',
                'patient_id': data['patient_id'],
                'consent_scope': data['consent_scope'],
                'expires_at': '2026-12-25T10:00:00Z'  # In production, fetch from database
            }), 200
        
        except SovereigntyViolationError as e:
            return jsonify({
                'status': 'invalid',
                'error': 'consent_invalid',
                'message': str(e)
            }), 403
    
    except Exception as e:
        logger.error(f"❌ Consent verification failed: {e}")
        return jsonify({
            'status': 'error',
            'error': 'verification_failed',
            'message': str(e)
        }), 500


@app.route('/api/v1/get-verification-status', methods=['GET'])
def get_verification_status():
    """
    Get verification status for a submission.
    
    Query params:
    - submission_id: Submission ID
    
    Returns:
    {
        "submission_id": "SUB_ABC123",
        "verification_score": 0.8,
        "golden_thread_status": "PROBABLE",
        "emr_match": false,
        "cbs_match": true,
        "idsr_match": false
    }
    """
    submission_id = request.args.get('submission_id')
    
    if not submission_id:
        return jsonify({
            'status': 'error',
            'error': 'missing_parameter',
            'message': 'submission_id required'
        }), 400
    
    # In production, fetch from database
    return jsonify({
        'submission_id': submission_id,
        'verification_score': 0.8,
        'golden_thread_status': 'PROBABLE',
        'emr_match': False,
        'cbs_match': True,
        'idsr_match': False,
        'timestamp': datetime.utcnow().isoformat()
    }), 200


@app.route('/api/v1/get-outbreak-alerts', methods=['GET'])
def get_outbreak_alerts():
    """
    Get active outbreak alerts for a location.
    
    Query params:
    - lat: Latitude
    - lng: Longitude
    - radius_km: Search radius in kilometers
    
    Returns:
    {
        "alerts": [
            {
                "alert_id": "ALERT_001",
                "disease": "cholera",
                "severity": "HIGH",
                "location": {"lat": 0.0512, "lng": 40.3129},
                "radius_km": 5,
                "case_count": 45,
                "timestamp": "2025-12-25T10:00:00Z"
            }
        ]
    }
    """
    lat = request.args.get('lat', type=float)
    lng = request.args.get('lng', type=float)
    radius_km = request.args.get('radius_km', default=10, type=float)
    
    if lat is None or lng is None:
        return jsonify({
            'status': 'error',
            'error': 'missing_parameters',
            'message': 'lat and lng required'
        }), 400
    
    # In production, query from BigQuery/Spanner
    alerts = [
        {
            'alert_id': 'ALERT_001',
            'disease': 'cholera',
            'severity': 'HIGH',
            'location': {'lat': lat, 'lng': lng},
            'radius_km': radius_km,
            'case_count': 45,
            'timestamp': datetime.utcnow().isoformat()
        }
    ]
    
    return jsonify({
        'status': 'success',
        'alerts': alerts,
        'count': len(alerts)
    }), 200


if __name__ == '__main__':
    # Development server
    app.run(host='0.0.0.0', port=8081, debug=True)
