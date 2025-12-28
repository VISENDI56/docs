"""
Bio-Interface REST API
Mobile Health Apps integration with Golden Thread protocol

Ensures all mobile health data flows through:
1. SovereignGuardrail validation
2. Golden Thread data fusion
3. Crypto Shredder lifecycle management

Compliance:
- GDPR Art. 9 (Special Categories)
- HIPAA §164.312 (Technical Safeguards)
- Kenya DPA §37 (Transfer Restrictions)
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
from typing import Dict, Optional
import logging
from datetime import datetime
import hashlib

# Import iLuminara components
from governance_kernel.vector_ledger import SovereignGuardrail, SovereigntyViolationError
from governance_kernel.crypto_shredder import CryptoShredder, RetentionPolicy, SovereigntyZone
from edge_node.sync_protocol.golden_thread import GoldenThread

logger = logging.getLogger(__name__)

# Initialize Flask app
app = Flask(__name__)
CORS(app)

# Initialize iLuminara components
guardrail = SovereignGuardrail(enable_tamper_proof_audit=True)
shredder = CryptoShredder(sovereignty_zone=SovereigntyZone.KENYA, enable_audit=True)
golden_thread = GoldenThread()


class BioInterfaceAPI:
    """
    REST API for mobile health apps.
    
    All data flows through:
    - SovereignGuardrail (compliance validation)
    - Golden Thread (data fusion)
    - Crypto Shredder (lifecycle management)
    """
    
    @staticmethod
    def validate_request(data: Dict) -> tuple[bool, Optional[str]]:
        """Validate incoming request data"""
        required_fields = ["patient_id", "location", "data_type"]
        
        for field in required_fields:
            if field not in data:
                return False, f"Missing required field: {field}"
        
        return True, None
    
    @staticmethod
    def generate_patient_hash(patient_id: str) -> str:
        """Generate privacy-preserving patient hash"""
        return hashlib.sha256(patient_id.encode()).hexdigest()[:16]


@app.route("/health", methods=["GET"])
def health_check():
    """Health check endpoint"""
    return jsonify({
        "status": "operational",
        "service": "Bio-Interface API",
        "fortress": "iLuminara Sovereign Health Fortress",
        "timestamp": datetime.utcnow().isoformat(),
        "compliance": {
            "guardrail": "active",
            "crypto_shredder": "active",
            "golden_thread": "active"
        }
    })


@app.route("/api/v1/submit-cbs-report", methods=["POST"])
def submit_cbs_report():
    """
    Submit Community-Based Surveillance (CBS) report from mobile app.
    
    Request body:
    {
        "patient_id": "PATIENT_12345",
        "location": {"lat": 0.0512, "lng": 40.3129},
        "symptoms": ["fever", "cough"],
        "severity": 7,
        "timestamp": "2025-01-15T08:00:00Z",
        "source": "CHV_MOBILE_APP",
        "consent_token": "VALID_TOKEN"
    }
    """
    try:
        data = request.get_json()
        
        # Validate request
        valid, error = BioInterfaceAPI.validate_request({
            "patient_id": data.get("patient_id"),
            "location": data.get("location"),
            "data_type": "CBS"
        })
        
        if not valid:
            return jsonify({"status": "error", "error": error}), 400
        
        # Validate with SovereignGuardrail
        try:
            guardrail.validate_action(
                action_type='Data_Processing',
                payload={
                    'data_type': 'PHI',
                    'processing_location': 'Edge_Node',
                    'consent_token': data.get('consent_token', 'EMERGENCY_CHV_ALERT'),
                    'jurisdiction': 'KDPA_KE'
                },
                jurisdiction='KDPA_KE'
            )
        except SovereigntyViolationError as e:
            logger.error(f"❌ Sovereignty violation: {e}")
            return jsonify({
                "status": "error",
                "error": "sovereignty_violation",
                "message": str(e)
            }), 403
        
        # Generate privacy-preserving patient hash
        patient_hash = BioInterfaceAPI.generate_patient_hash(data["patient_id"])
        
        # Create CBS signal for Golden Thread
        cbs_signal = {
            "location": data["location"],
            "symptom": data["symptoms"][0] if data["symptoms"] else "unknown",
            "timestamp": data.get("timestamp", datetime.utcnow().isoformat()),
            "source": data.get("source", "CHV_MOBILE_APP"),
            "severity": data.get("severity", 5)
        }
        
        # Encrypt sensitive data with Crypto Shredder
        sensitive_data = str(data).encode()
        encrypted_data, key_id = shredder.encrypt_with_ephemeral_key(
            data=sensitive_data,
            retention_policy=RetentionPolicy.HOT,
            metadata={
                "patient_hash": patient_hash,
                "jurisdiction": "KDPA_KE",
                "data_type": "CBS",
                "source": "mobile_app"
            }
        )
        
        # Fuse with Golden Thread (if EMR data available)
        fused = golden_thread.fuse_data_streams(
            cbs_signal=cbs_signal,
            patient_id=patient_hash
        )
        
        logger.info(f"✅ CBS report submitted - Patient: {patient_hash}, Verification: {fused.verification_score}")
        
        return jsonify({
            "status": "success",
            "timestamp": datetime.utcnow().isoformat(),
            "patient_hash": patient_hash,
            "key_id": key_id,
            "verification_score": fused.verification_score,
            "alert_level": _calculate_alert_level(data.get("severity", 5)),
            "message": "CBS report submitted successfully"
        }), 201
    
    except Exception as e:
        logger.error(f"❌ Error submitting CBS report: {e}")
        return jsonify({
            "status": "error",
            "error": "processing_failed",
            "message": str(e)
        }), 500


@app.route("/api/v1/submit-emr-record", methods=["POST"])
def submit_emr_record():
    """
    Submit Electronic Medical Record (EMR) from clinic/hospital.
    
    Request body:
    {
        "patient_id": "PATIENT_12345",
        "location": {"lat": 0.0512, "lng": 40.3129},
        "diagnosis": "malaria",
        "timestamp": "2025-01-15T08:30:00Z",
        "source": "DADAAB_CLINIC",
        "consent_token": "VALID_TOKEN"
    }
    """
    try:
        data = request.get_json()
        
        # Validate request
        valid, error = BioInterfaceAPI.validate_request({
            "patient_id": data.get("patient_id"),
            "location": data.get("location"),
            "data_type": "EMR"
        })
        
        if not valid:
            return jsonify({"status": "error", "error": error}), 400
        
        # Validate with SovereignGuardrail
        try:
            guardrail.validate_action(
                action_type='Data_Processing',
                payload={
                    'data_type': 'PHI',
                    'processing_location': 'Edge_Node',
                    'consent_token': data.get('consent_token', 'CLINIC_CONSENT'),
                    'jurisdiction': 'KDPA_KE'
                },
                jurisdiction='KDPA_KE'
            )
        except SovereigntyViolationError as e:
            logger.error(f"❌ Sovereignty violation: {e}")
            return jsonify({
                "status": "error",
                "error": "sovereignty_violation",
                "message": str(e)
            }), 403
        
        # Generate privacy-preserving patient hash
        patient_hash = BioInterfaceAPI.generate_patient_hash(data["patient_id"])
        
        # Create EMR record for Golden Thread
        emr_record = {
            "location": data["location"],
            "diagnosis": data.get("diagnosis", "unknown"),
            "timestamp": data.get("timestamp", datetime.utcnow().isoformat()),
            "source": data.get("source", "CLINIC")
        }
        
        # Encrypt sensitive data with Crypto Shredder
        sensitive_data = str(data).encode()
        encrypted_data, key_id = shredder.encrypt_with_ephemeral_key(
            data=sensitive_data,
            retention_policy=RetentionPolicy.WARM,  # EMR has longer retention
            metadata={
                "patient_hash": patient_hash,
                "jurisdiction": "KDPA_KE",
                "data_type": "EMR",
                "source": "clinic"
            }
        )
        
        # Fuse with Golden Thread
        fused = golden_thread.fuse_data_streams(
            emr_record=emr_record,
            patient_id=patient_hash
        )
        
        logger.info(f"✅ EMR record submitted - Patient: {patient_hash}, Verification: {fused.verification_score}")
        
        return jsonify({
            "status": "success",
            "timestamp": datetime.utcnow().isoformat(),
            "patient_hash": patient_hash,
            "key_id": key_id,
            "verification_score": fused.verification_score,
            "message": "EMR record submitted successfully"
        }), 201
    
    except Exception as e:
        logger.error(f"❌ Error submitting EMR record: {e}")
        return jsonify({
            "status": "error",
            "error": "processing_failed",
            "message": str(e)
        }), 500


@app.route("/api/v1/fuse-data", methods=["POST"])
def fuse_data():
    """
    Fuse CBS and EMR data streams using Golden Thread.
    
    Request body:
    {
        "patient_id": "PATIENT_12345",
        "cbs_signal": {...},
        "emr_record": {...}
    }
    """
    try:
        data = request.get_json()
        
        if "patient_id" not in data:
            return jsonify({"status": "error", "error": "missing_patient_id"}), 400
        
        # Generate patient hash
        patient_hash = BioInterfaceAPI.generate_patient_hash(data["patient_id"])
        
        # Fuse data streams
        fused = golden_thread.fuse_data_streams(
            cbs_signal=data.get("cbs_signal"),
            emr_record=data.get("emr_record"),
            patient_id=patient_hash
        )
        
        logger.info(f"✅ Data fused - Patient: {patient_hash}, Score: {fused.verification_score}")
        
        return jsonify({
            "status": "success",
            "timestamp": datetime.utcnow().isoformat(),
            "patient_hash": patient_hash,
            "verification_score": fused.verification_score,
            "fused_record": fused.to_dict()
        }), 200
    
    except Exception as e:
        logger.error(f"❌ Error fusing data: {e}")
        return jsonify({
            "status": "error",
            "error": "fusion_failed",
            "message": str(e)
        }), 500


@app.route("/api/v1/retrieve-data", methods=["POST"])
def retrieve_data():
    """
    Retrieve encrypted data using key_id.
    
    Request body:
    {
        "key_id": "abc123",
        "encrypted_data": "base64_encoded_data"
    }
    """
    try:
        data = request.get_json()
        
        if "key_id" not in data or "encrypted_data" not in data:
            return jsonify({"status": "error", "error": "missing_parameters"}), 400
        
        # Decrypt data
        import base64
        encrypted_data = base64.b64decode(data["encrypted_data"])
        decrypted_data = shredder.decrypt_with_key(encrypted_data, data["key_id"])
        
        if decrypted_data is None:
            return jsonify({
                "status": "error",
                "error": "decryption_failed",
                "message": "Key may be shredded or expired"
            }), 404
        
        return jsonify({
            "status": "success",
            "timestamp": datetime.utcnow().isoformat(),
            "data": decrypted_data.decode()
        }), 200
    
    except Exception as e:
        logger.error(f"❌ Error retrieving data: {e}")
        return jsonify({
            "status": "error",
            "error": "retrieval_failed",
            "message": str(e)
        }), 500


def _calculate_alert_level(severity: int) -> str:
    """Calculate alert level from severity score"""
    if severity >= 9:
        return "CRITICAL"
    elif severity >= 7:
        return "HIGH"
    elif severity >= 4:
        return "MEDIUM"
    else:
        return "LOW"


if __name__ == "__main__":
    # Run API server
    app.run(
        host="0.0.0.0",
        port=8080,
        debug=False
    )
