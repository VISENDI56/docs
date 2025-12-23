"""
Bio-Interface REST API for Mobile Health Apps
Golden Thread Protocol Integration

Enables mobile health apps to submit CBS (Community-Based Surveillance) signals
that are automatically fused with EMR and IDSR data streams.

Compliance:
- GDPR Art. 6 (Lawfulness of Processing)
- KDPA §37 (Transfer Restrictions)
- HIPAA §164.312 (Technical Safeguards)
- WHO IHR Article 6 (Notification)
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
from typing import Dict, Optional
from datetime import datetime
from dataclasses import dataclass, asdict
import logging
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
class HealthSignal:
    """Community-based surveillance signal from mobile app"""
    signal_id: str
    timestamp: str
    location: Dict[str, float]  # {lat, lng}
    symptoms: list
    severity: int  # 0-10
    patient_age: Optional[int]
    patient_gender: Optional[str]
    reporter_id: str  # CHV or patient ID
    reporter_type: str  # "CHV", "PATIENT", "FAMILY"
    consent_token: str
    device_id: str
    app_version: str


@dataclass
class VerificationResponse:
    """Response with Golden Thread verification"""
    signal_id: str
    status: str  # "CONFIRMED", "PROBABLE", "POSSIBLE", "UNVERIFIED"
    verification_score: float
    fused_record_id: Optional[str]
    recommendations: list
    alert_level: str  # "LOW", "MEDIUM", "HIGH", "CRITICAL"
    compliance_status: Dict[str, str]


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


@app.route('/api/v1/submit-signal', methods=['POST'])
def submit_health_signal():
    """
    Submit community-based surveillance signal from mobile app.
    
    Request body:
    {
        "location": {"lat": 0.0512, "lng": 40.3129},
        "symptoms": ["fever", "cough", "fatigue"],
        "severity": 7,
        "patient_age": 35,
        "patient_gender": "F",
        "reporter_id": "CHV_AMINA_HASSAN",
        "reporter_type": "CHV",
        "consent_token": "CONSENT_TOKEN_123",
        "device_id": "DEVICE_ABC123",
        "app_version": "2.1.0"
    }
    
    Returns:
    {
        "signal_id": "SIG_123",
        "status": "CONFIRMED",
        "verification_score": 1.0,
        "recommendations": [...],
        "alert_level": "HIGH"
    }
    """
    try:
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['location', 'symptoms', 'reporter_id', 'consent_token']
        for field in required_fields:
            if field not in data:
                return jsonify({
                    "error": "missing_field",
                    "message": f"Required field missing: {field}"
                }), 400
        
        # Generate signal ID
        signal_id = _generate_signal_id(data)
        
        # Create health signal
        signal = HealthSignal(
            signal_id=signal_id,
            timestamp=datetime.utcnow().isoformat(),
            location=data['location'],
            symptoms=data['symptoms'],
            severity=data.get('severity', 5),
            patient_age=data.get('patient_age'),
            patient_gender=data.get('patient_gender'),
            reporter_id=data['reporter_id'],
            reporter_type=data.get('reporter_type', 'PATIENT'),
            consent_token=data['consent_token'],
            device_id=data.get('device_id', 'UNKNOWN'),
            app_version=data.get('app_version', '1.0.0')
        )
        
        # Sovereignty validation
        try:
            guardrail.validate_action(
                action_type='Data_Processing',
                payload={
                    'data_type': 'PHI',
                    'processing_location': 'Edge_Node',
                    'consent_token': signal.consent_token,
                    'consent_scope': 'public_health_surveillance'
                },
                jurisdiction='KDPA_KE'
            )
        except SovereigntyViolationError as e:
            logger.error(f"❌ Sovereignty violation: {e}")
            return jsonify({
                "error": "sovereignty_violation",
                "message": str(e)
            }), 403
        
        # Submit to Golden Thread for data fusion
        fused_result = golden_thread.fuse_data_streams(
            cbs_signal={
                'signal_id': signal.signal_id,
                'location': signal.location,
                'symptom': signal.symptoms[0] if signal.symptoms else 'unknown',
                'timestamp': signal.timestamp,
                'severity': signal.severity,
                'source': f"{signal.reporter_type}_{signal.reporter_id}"
            },
            patient_id=f"AUTO_{signal.signal_id}"
        )
        
        # Determine alert level
        alert_level = _calculate_alert_level(signal.severity, fused_result.verification_score)
        
        # Generate recommendations
        recommendations = _generate_recommendations(signal, alert_level)
        
        # Build response
        response = VerificationResponse(
            signal_id=signal.signal_id,
            status=_get_verification_status(fused_result.verification_score),
            verification_score=fused_result.verification_score,
            fused_record_id=fused_result.record_id if hasattr(fused_result, 'record_id') else None,
            recommendations=recommendations,
            alert_level=alert_level,
            compliance_status={
                "sovereignty": "COMPLIANT",
                "consent": "VALIDATED",
                "frameworks": "GDPR, KDPA, WHO IHR"
            }
        )
        
        logger.info(
            f"✅ Health signal submitted: {signal_id} "
            f"(verification: {fused_result.verification_score:.2f}, "
            f"alert: {alert_level})"
        )
        
        return jsonify(asdict(response)), 200
    
    except Exception as e:
        logger.error(f"❌ Error processing health signal: {e}")
        return jsonify({
            "error": "processing_failed",
            "message": str(e)
        }), 500


@app.route('/api/v1/query-status', methods=['GET'])
def query_signal_status():
    """
    Query status of previously submitted signal.
    
    Query params:
    - signal_id: Signal identifier
    
    Returns signal status and verification updates.
    """
    signal_id = request.args.get('signal_id')
    
    if not signal_id:
        return jsonify({
            "error": "missing_parameter",
            "message": "signal_id required"
        }), 400
    
    # TODO: Query from database
    # For now, return mock status
    return jsonify({
        "signal_id": signal_id,
        "status": "CONFIRMED",
        "verification_score": 0.95,
        "last_updated": datetime.utcnow().isoformat(),
        "fused_with_emr": True,
        "alert_triggered": True
    })


@app.route('/api/v1/outbreak-alerts', methods=['GET'])
def get_outbreak_alerts():
    """
    Get active outbreak alerts for a location.
    
    Query params:
    - lat: Latitude
    - lng: Longitude
    - radius_km: Search radius (default: 50km)
    
    Returns active alerts within radius.
    """
    try:
        lat = float(request.args.get('lat', 0))
        lng = float(request.args.get('lng', 0))
        radius_km = float(request.args.get('radius_km', 50))
        
        # TODO: Query from BigQuery/Spanner
        # For now, return mock alerts
        alerts = [
            {
                "alert_id": "ALERT_001",
                "disease": "cholera",
                "location": {"lat": lat, "lng": lng},
                "severity": "HIGH",
                "case_count": 45,
                "trend": "INCREASING",
                "recommendations": [
                    "Boil water before drinking",
                    "Seek medical attention for diarrhea",
                    "Report symptoms to health authorities"
                ],
                "issued_at": datetime.utcnow().isoformat()
            }
        ]
        
        return jsonify({
            "alerts": alerts,
            "count": len(alerts),
            "search_location": {"lat": lat, "lng": lng},
            "radius_km": radius_km
        })
    
    except ValueError:
        return jsonify({
            "error": "invalid_parameters",
            "message": "lat, lng, and radius_km must be numbers"
        }), 400


@app.route('/api/v1/consent/validate', methods=['POST'])
def validate_consent():
    """
    Validate consent token for data processing.
    
    Request body:
    {
        "consent_token": "TOKEN_123",
        "scope": "public_health_surveillance"
    }
    
    Returns consent validation status.
    """
    data = request.get_json()
    
    consent_token = data.get('consent_token')
    scope = data.get('scope', 'public_health_surveillance')
    
    if not consent_token:
        return jsonify({
            "error": "missing_consent_token",
            "message": "consent_token required"
        }), 400
    
    # Validate with SovereignGuardrail
    try:
        guardrail.validate_action(
            action_type='Consent_Validation',
            payload={
                'consent_token': consent_token,
                'consent_scope': scope
            },
            jurisdiction='KDPA_KE'
        )
        
        return jsonify({
            "valid": True,
            "scope": scope,
            "frameworks": "GDPR Art. 6, KDPA §42, POPIA §11",
            "validated_at": datetime.utcnow().isoformat()
        })
    
    except SovereigntyViolationError as e:
        return jsonify({
            "valid": False,
            "error": str(e)
        }), 403


def _generate_signal_id(data: Dict) -> str:
    """Generate unique signal ID"""
    content = f"{data['reporter_id']}_{data['location']}_{datetime.utcnow().isoformat()}"
    hash_digest = hashlib.sha256(content.encode()).hexdigest()
    return f"SIG_{hash_digest[:12].upper()}"


def _calculate_alert_level(severity: int, verification_score: float) -> str:
    """Calculate alert level based on severity and verification"""
    if severity >= 9 and verification_score >= 0.8:
        return "CRITICAL"
    elif severity >= 7 and verification_score >= 0.6:
        return "HIGH"
    elif severity >= 4:
        return "MEDIUM"
    else:
        return "LOW"


def _get_verification_status(score: float) -> str:
    """Map verification score to status"""
    if score >= 0.9:
        return "CONFIRMED"
    elif score >= 0.7:
        return "PROBABLE"
    elif score >= 0.4:
        return "POSSIBLE"
    else:
        return "UNVERIFIED"


def _generate_recommendations(signal: HealthSignal, alert_level: str) -> list:
    """Generate health recommendations based on signal"""
    recommendations = []
    
    # Symptom-specific recommendations
    if "diarrhea" in signal.symptoms or "vomiting" in signal.symptoms:
        recommendations.append("Start oral rehydration solution (ORS) immediately")
        recommendations.append("Seek medical attention if symptoms worsen")
        if alert_level in ["HIGH", "CRITICAL"]:
            recommendations.append("URGENT: Suspected cholera - isolate patient")
    
    if "fever" in signal.symptoms:
        recommendations.append("Monitor temperature regularly")
        recommendations.append("Take antimalarial medication if in endemic area")
    
    if "cough" in signal.symptoms or "breathing_difficulty" in signal.symptoms:
        recommendations.append("Wear mask to prevent transmission")
        recommendations.append("Seek immediate medical attention for breathing difficulty")
    
    # Alert-level recommendations
    if alert_level == "CRITICAL":
        recommendations.append("🚨 CRITICAL: Contact emergency services immediately")
        recommendations.append("Notify district health officer")
    elif alert_level == "HIGH":
        recommendations.append("⚠️ HIGH PRIORITY: Visit health facility within 24 hours")
    
    return recommendations


if __name__ == '__main__':
    # Run API server
    app.run(
        host='0.0.0.0',
        port=8080,
        debug=False
    )
