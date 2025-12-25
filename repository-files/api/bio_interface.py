"""
Bio-Interface REST API
Mobile Health Apps integration with Golden Thread protocol

Compliance:
- GDPR Art. 9 (Special Categories of Personal Data)
- HIPAA §164.312 (Technical Safeguards)
- KDPA §37 (Transfer Restrictions)
- WHO IHR (2005) Article 6 (Notification)
"""

import os
import json
import logging
from datetime import datetime
from typing import Dict, List, Optional
from enum import Enum

from flask import Flask, request, jsonify
from flask_cors import CORS

from governance_kernel.vector_ledger import SovereignGuardrail, SovereigntyViolationError
from edge_node.sync_protocol.golden_thread import GoldenThread
from edge_node.frenasa_engine.voice_processor import VoiceProcessor

logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app)  # Enable CORS for mobile apps


class DataSource(Enum):
    """Data source types for Golden Thread fusion"""
    CBS = "community_based_surveillance"
    EMR = "electronic_medical_record"
    IDSR = "integrated_disease_surveillance_response"
    MOBILE_APP = "mobile_health_app"
    IOT_SENSOR = "iot_sensor"


class BioInterfaceAPI:
    """
    REST API for Mobile Health Apps.
    
    Ensures all data uses Golden Thread protocol for verification:
    - CBS signals from community health volunteers
    - EMR records from clinics/hospitals
    - IDSR reports for government submission
    
    Verification: Signals are tagged as CONFIRMED only if location 
    and time-delta match within 24 hours.
    """
    
    def __init__(
        self,
        jurisdiction: str = "KDPA_KE",
        enable_sovereignty_check: bool = True
    ):
        self.jurisdiction = jurisdiction
        self.enable_sovereignty_check = enable_sovereignty_check
        
        # Initialize components
        self.guardrail = SovereignGuardrail()
        self.golden_thread = GoldenThread()
        self.voice_processor = VoiceProcessor()
        
        logger.info(f"🔗 Bio-Interface API initialized - Jurisdiction: {jurisdiction}")
    
    def submit_cbs_report(
        self,
        location: Dict[str, float],
        symptoms: List[str],
        severity: int,
        reporter_id: str,
        patient_id: Optional[str] = None,
        metadata: Optional[Dict] = None
    ) -> Dict:
        """
        Submit Community-Based Surveillance (CBS) report.
        
        Args:
            location: {"lat": float, "lng": float}
            symptoms: List of symptoms
            severity: Severity score (0-10)
            reporter_id: CHV/reporter identifier
            patient_id: Optional patient identifier
            metadata: Additional metadata
        
        Returns:
            CBS report with Golden Thread verification
        """
        # Validate sovereignty
        if self.enable_sovereignty_check:
            try:
                self.guardrail.validate_action(
                    action_type='Data_Processing',
                    payload={
                        'data_type': 'PHI',
                        'processing_location': 'Edge_Node',
                        'source': DataSource.CBS.value
                    },
                    jurisdiction=self.jurisdiction
                )
            except SovereigntyViolationError as e:
                logger.error(f"❌ Sovereignty violation: {e}")
                return {
                    "status": "error",
                    "error": "sovereignty_violation",
                    "message": str(e)
                }
        
        # Create CBS signal
        cbs_signal = {
            'location': location,
            'symptoms': symptoms,
            'severity': severity,
            'timestamp': datetime.utcnow().isoformat(),
            'source': DataSource.CBS.value,
            'reporter_id': reporter_id,
            'metadata': metadata or {}
        }
        
        # Attempt Golden Thread fusion
        fused_record = None
        if patient_id:
            try:
                fused_record = self.golden_thread.fuse_data_streams(
                    cbs_signal=cbs_signal,
                    patient_id=patient_id
                )
                
                logger.info(
                    f"✅ CBS report fused - Patient: {patient_id}, "
                    f"Verification: {fused_record.verification_score:.2f}"
                )
            except Exception as e:
                logger.warning(f"⚠️ Golden Thread fusion failed: {e}")
        
        # Response
        response = {
            "status": "success",
            "timestamp": datetime.utcnow().isoformat(),
            "cbs_report": cbs_signal,
            "patient_id": patient_id,
            "fused": fused_record is not None
        }
        
        if fused_record:
            response["verification_score"] = fused_record.verification_score
            response["verification_status"] = fused_record.verification_status
        
        return response
    
    def submit_emr_record(
        self,
        patient_id: str,
        location: Dict[str, float],
        diagnosis: str,
        symptoms: List[str],
        treatment: str,
        facility_id: str,
        metadata: Optional[Dict] = None
    ) -> Dict:
        """
        Submit Electronic Medical Record (EMR).
        
        Args:
            patient_id: Patient identifier
            location: {"lat": float, "lng": float}
            diagnosis: Clinical diagnosis
            symptoms: List of symptoms
            treatment: Treatment provided
            facility_id: Health facility identifier
            metadata: Additional metadata
        
        Returns:
            EMR record with Golden Thread verification
        """
        # Validate sovereignty
        if self.enable_sovereignty_check:
            try:
                self.guardrail.validate_action(
                    action_type='Data_Processing',
                    payload={
                        'data_type': 'PHI',
                        'processing_location': 'Edge_Node',
                        'source': DataSource.EMR.value,
                        'consent_token': metadata.get('consent_token') if metadata else None
                    },
                    jurisdiction=self.jurisdiction
                )
            except SovereigntyViolationError as e:
                logger.error(f"❌ Sovereignty violation: {e}")
                return {
                    "status": "error",
                    "error": "sovereignty_violation",
                    "message": str(e)
                }
        
        # Create EMR record
        emr_record = {
            'patient_id': patient_id,
            'location': location,
            'diagnosis': diagnosis,
            'symptoms': symptoms,
            'treatment': treatment,
            'timestamp': datetime.utcnow().isoformat(),
            'source': DataSource.EMR.value,
            'facility_id': facility_id,
            'metadata': metadata or {}
        }
        
        # Attempt Golden Thread fusion
        fused_record = None
        try:
            fused_record = self.golden_thread.fuse_data_streams(
                emr_record=emr_record,
                patient_id=patient_id
            )
            
            logger.info(
                f"✅ EMR record fused - Patient: {patient_id}, "
                f"Verification: {fused_record.verification_score:.2f}"
            )
        except Exception as e:
            logger.warning(f"⚠️ Golden Thread fusion failed: {e}")
        
        # Response
        response = {
            "status": "success",
            "timestamp": datetime.utcnow().isoformat(),
            "emr_record": emr_record,
            "patient_id": patient_id,
            "fused": fused_record is not None
        }
        
        if fused_record:
            response["verification_score"] = fused_record.verification_score
            response["verification_status"] = fused_record.verification_status
        
        return response
    
    def process_voice_alert(
        self,
        audio_data: bytes,
        location: Dict[str, float],
        reporter_id: str,
        language: str = "swahili"
    ) -> Dict:
        """
        Process voice alert from mobile app.
        
        Args:
            audio_data: Audio file bytes
            location: {"lat": float, "lng": float}
            reporter_id: CHV/reporter identifier
            language: Audio language
        
        Returns:
            Processed voice alert with CBS signal
        """
        # Process voice
        try:
            voice_result = self.voice_processor.process_voice(
                audio_data=audio_data,
                language=language
            )
            
            # Create CBS signal from voice
            cbs_signal = {
                'location': location,
                'symptoms': voice_result.get('symptoms', []),
                'severity': voice_result.get('severity', 5),
                'timestamp': datetime.utcnow().isoformat(),
                'source': DataSource.MOBILE_APP.value,
                'reporter_id': reporter_id,
                'transcription': voice_result.get('transcription'),
                'language': language
            }
            
            # Submit as CBS report
            return self.submit_cbs_report(
                location=location,
                symptoms=cbs_signal['symptoms'],
                severity=cbs_signal['severity'],
                reporter_id=reporter_id,
                metadata={
                    'transcription': cbs_signal['transcription'],
                    'language': language,
                    'source': 'voice_alert'
                }
            )
        
        except Exception as e:
            logger.error(f"❌ Voice processing failed: {e}")
            return {
                "status": "error",
                "error": "voice_processing_failed",
                "message": str(e)
            }
    
    def get_verification_status(
        self,
        patient_id: str
    ) -> Dict:
        """
        Get Golden Thread verification status for a patient.
        
        Args:
            patient_id: Patient identifier
        
        Returns:
            Verification status and fused records
        """
        try:
            # Query Golden Thread
            fused_records = self.golden_thread.get_patient_records(patient_id)
            
            if not fused_records:
                return {
                    "status": "success",
                    "patient_id": patient_id,
                    "records_found": 0,
                    "verification_status": "NO_RECORDS"
                }
            
            # Calculate overall verification
            avg_verification = sum(
                r.verification_score for r in fused_records
            ) / len(fused_records)
            
            return {
                "status": "success",
                "patient_id": patient_id,
                "records_found": len(fused_records),
                "average_verification_score": avg_verification,
                "verification_status": self._get_verification_label(avg_verification),
                "records": [r.to_dict() for r in fused_records]
            }
        
        except Exception as e:
            logger.error(f"❌ Verification query failed: {e}")
            return {
                "status": "error",
                "error": "query_failed",
                "message": str(e)
            }
    
    def _get_verification_label(self, score: float) -> str:
        """Get verification status label"""
        if score >= 1.0:
            return "CONFIRMED"
        elif score >= 0.7:
            return "PROBABLE"
        elif score >= 0.4:
            return "POSSIBLE"
        else:
            return "UNVERIFIED"


# Initialize API
bio_api = BioInterfaceAPI(
    jurisdiction=os.getenv("JURISDICTION", "KDPA_KE"),
    enable_sovereignty_check=True
)


# Flask routes
@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        "status": "healthy",
        "service": "Bio-Interface API",
        "version": "1.0.0",
        "jurisdiction": bio_api.jurisdiction
    })


@app.route('/api/v1/cbs/report', methods=['POST'])
def submit_cbs():
    """Submit CBS report"""
    try:
        data = request.get_json()
        
        result = bio_api.submit_cbs_report(
            location=data['location'],
            symptoms=data['symptoms'],
            severity=data['severity'],
            reporter_id=data['reporter_id'],
            patient_id=data.get('patient_id'),
            metadata=data.get('metadata')
        )
        
        return jsonify(result)
    
    except Exception as e:
        logger.error(f"❌ CBS submission failed: {e}")
        return jsonify({
            "status": "error",
            "error": "submission_failed",
            "message": str(e)
        }), 400


@app.route('/api/v1/emr/record', methods=['POST'])
def submit_emr():
    """Submit EMR record"""
    try:
        data = request.get_json()
        
        result = bio_api.submit_emr_record(
            patient_id=data['patient_id'],
            location=data['location'],
            diagnosis=data['diagnosis'],
            symptoms=data['symptoms'],
            treatment=data['treatment'],
            facility_id=data['facility_id'],
            metadata=data.get('metadata')
        )
        
        return jsonify(result)
    
    except Exception as e:
        logger.error(f"❌ EMR submission failed: {e}")
        return jsonify({
            "status": "error",
            "error": "submission_failed",
            "message": str(e)
        }), 400


@app.route('/api/v1/voice/alert', methods=['POST'])
def process_voice():
    """Process voice alert"""
    try:
        # Get audio data
        audio_data = request.data
        
        # Get parameters
        location = json.loads(request.args.get('location', '{}'))
        reporter_id = request.args.get('reporter_id')
        language = request.args.get('language', 'swahili')
        
        result = bio_api.process_voice_alert(
            audio_data=audio_data,
            location=location,
            reporter_id=reporter_id,
            language=language
        )
        
        return jsonify(result)
    
    except Exception as e:
        logger.error(f"❌ Voice processing failed: {e}")
        return jsonify({
            "status": "error",
            "error": "processing_failed",
            "message": str(e)
        }), 400


@app.route('/api/v1/verification/<patient_id>', methods=['GET'])
def get_verification(patient_id):
    """Get verification status"""
    try:
        result = bio_api.get_verification_status(patient_id)
        return jsonify(result)
    
    except Exception as e:
        logger.error(f"❌ Verification query failed: {e}")
        return jsonify({
            "status": "error",
            "error": "query_failed",
            "message": str(e)
        }), 400


if __name__ == "__main__":
    # Run API server
    port = int(os.getenv("API_PORT", 8080))
    app.run(host="0.0.0.0", port=port, debug=False)
