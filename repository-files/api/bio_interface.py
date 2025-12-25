"""
Bio-Interface REST API
Mobile Health Apps Integration with Golden Thread Protocol

This module provides REST API endpoints for mobile health applications
to integrate with iLuminara-Core using the Golden Thread data fusion protocol.

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
from google.cloud import pubsub_v1

# Import iLuminara components
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from governance_kernel.vector_ledger import SovereignGuardrail, SovereigntyViolationError
from edge_node.sync_protocol.golden_thread import GoldenThread
from edge_node.frenasa_engine.voice_processor import VoiceProcessor

logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app)  # Enable CORS for mobile apps


class DataSource(Enum):
    """Data source types"""
    MOBILE_APP = "mobile_app"
    CHV_DEVICE = "chv_device"
    IOT_SENSOR = "iot_sensor"
    VOICE_ALERT = "voice_alert"
    MANUAL_ENTRY = "manual_entry"


class BioInterface:
    """
    Bio-Interface for mobile health applications.
    
    Provides REST API endpoints that enforce:
    - Golden Thread data fusion
    - Sovereignty constraints
    - Real-time verification
    """
    
    def __init__(
        self,
        project_id: str,
        jurisdiction: str = "KDPA_KE",
        enable_pubsub: bool = True
    ):
        self.project_id = project_id
        self.jurisdiction = jurisdiction
        self.enable_pubsub = enable_pubsub
        
        # Initialize components
        self.guardrail = SovereignGuardrail()
        self.golden_thread = GoldenThread()
        self.voice_processor = VoiceProcessor()
        
        # Initialize PubSub for real-time alerts
        if enable_pubsub:
            self.publisher = pubsub_v1.PublisherClient()
            self.topic_path = self.publisher.topic_path(
                project_id,
                "iluminara-health-alerts"
            )
        
        logger.info(f"🔗 Bio-Interface initialized - Jurisdiction: {jurisdiction}")
    
    def submit_cbs_report(
        self,
        location: Dict[str, float],
        symptoms: List[str],
        severity: int,
        reporter_id: str,
        source: DataSource = DataSource.MOBILE_APP,
        metadata: Optional[Dict] = None
    ) -> Dict:
        """
        Submit Community-Based Surveillance (CBS) report.
        
        Args:
            location: {"lat": float, "lng": float}
            symptoms: List of symptoms
            severity: Severity score (0-10)
            reporter_id: CHV or user ID
            source: Data source type
            metadata: Additional metadata
        
        Returns:
            Response with verification status
        """
        try:
            # Validate sovereignty constraints
            self.guardrail.validate_action(
                action_type='Data_Collection',
                payload={
                    'data_type': 'PHI',
                    'source': source.value,
                    'processing_location': 'Edge_Node',
                    'consent_token': metadata.get('consent_token') if metadata else None
                },
                jurisdiction=self.jurisdiction
            )
            
            # Create CBS signal
            cbs_signal = {
                'location': location,
                'symptoms': symptoms,
                'severity': severity,
                'timestamp': datetime.utcnow().isoformat(),
                'reporter_id': reporter_id,
                'source': source.value,
                'metadata': metadata or {}
            }
            
            # Attempt Golden Thread fusion
            # (will verify against EMR if available)
            fused_record = self.golden_thread.fuse_data_streams(
                cbs_signal=cbs_signal,
                patient_id=metadata.get('patient_id') if metadata else None
            )
            
            # Publish alert if high severity
            if severity >= 7 and self.enable_pubsub:
                self._publish_alert(cbs_signal, fused_record)
            
            return {
                "status": "success",
                "message": "CBS report submitted successfully",
                "record_id": fused_record.get('record_id'),
                "verification_score": fused_record.get('verification_score'),
                "verification_status": self._get_verification_status(
                    fused_record.get('verification_score', 0)
                ),
                "timestamp": datetime.utcnow().isoformat(),
                "compliance": {
                    "jurisdiction": self.jurisdiction,
                    "frameworks": ["GDPR Art. 9", "KDPA §37", "WHO IHR Art. 6"]
                }
            }
        
        except SovereigntyViolationError as e:
            logger.error(f"❌ Sovereignty violation: {e}")
            return {
                "status": "error",
                "error": "sovereignty_violation",
                "message": str(e)
            }, 403
        
        except Exception as e:
            logger.error(f"❌ CBS submission failed: {e}")
            return {
                "status": "error",
                "error": "submission_failed",
                "message": str(e)
            }, 500
    
    def submit_emr_record(
        self,
        patient_id: str,
        location: Dict[str, float],
        diagnosis: str,
        symptoms: List[str],
        facility_id: str,
        metadata: Optional[Dict] = None
    ) -> Dict:
        """
        Submit Electronic Medical Record (EMR) from health facility.
        
        Args:
            patient_id: Patient identifier
            location: {"lat": float, "lng": float}
            diagnosis: Clinical diagnosis
            symptoms: List of symptoms
            facility_id: Health facility ID
            metadata: Additional metadata
        
        Returns:
            Response with verification status
        """
        try:
            # Validate sovereignty constraints
            self.guardrail.validate_action(
                action_type='Data_Processing',
                payload={
                    'data_type': 'PHI',
                    'processing_location': 'Edge_Node',
                    'consent_token': metadata.get('consent_token') if metadata else None
                },
                jurisdiction=self.jurisdiction
            )
            
            # Create EMR record
            emr_record = {
                'patient_id': patient_id,
                'location': location,
                'diagnosis': diagnosis,
                'symptoms': symptoms,
                'timestamp': datetime.utcnow().isoformat(),
                'facility_id': facility_id,
                'source': 'EMR',
                'metadata': metadata or {}
            }
            
            # Fuse with CBS signals via Golden Thread
            fused_record = self.golden_thread.fuse_data_streams(
                emr_record=emr_record,
                patient_id=patient_id
            )
            
            return {
                "status": "success",
                "message": "EMR record submitted successfully",
                "record_id": fused_record.get('record_id'),
                "verification_score": fused_record.get('verification_score'),
                "verification_status": self._get_verification_status(
                    fused_record.get('verification_score', 0)
                ),
                "timestamp": datetime.utcnow().isoformat(),
                "compliance": {
                    "jurisdiction": self.jurisdiction,
                    "frameworks": ["HIPAA §164.312", "GDPR Art. 9", "KDPA §37"]
                }
            }
        
        except SovereigntyViolationError as e:
            logger.error(f"❌ Sovereignty violation: {e}")
            return {
                "status": "error",
                "error": "sovereignty_violation",
                "message": str(e)
            }, 403
        
        except Exception as e:
            logger.error(f"❌ EMR submission failed: {e}")
            return {
                "status": "error",
                "error": "submission_failed",
                "message": str(e)
            }, 500
    
    def submit_voice_alert(
        self,
        audio_data: bytes,
        location: Dict[str, float],
        reporter_id: str,
        language: str = "swahili",
        metadata: Optional[Dict] = None
    ) -> Dict:
        """
        Submit voice alert from CHV.
        
        Args:
            audio_data: Audio file bytes
            location: {"lat": float, "lng": float}
            reporter_id: CHV ID
            language: Audio language
            metadata: Additional metadata
        
        Returns:
            Response with transcription and verification
        """
        try:
            # Process voice alert
            voice_result = self.voice_processor.process_voice(
                audio_data=audio_data,
                language=language,
                location=location
            )
            
            # Create CBS signal from voice
            cbs_signal = {
                'location': location,
                'symptoms': voice_result.get('symptoms', []),
                'severity': voice_result.get('severity', 5),
                'timestamp': datetime.utcnow().isoformat(),
                'reporter_id': reporter_id,
                'source': DataSource.VOICE_ALERT.value,
                'transcription': voice_result.get('transcription'),
                'metadata': metadata or {}
            }
            
            # Fuse via Golden Thread
            fused_record = self.golden_thread.fuse_data_streams(
                cbs_signal=cbs_signal,
                patient_id=metadata.get('patient_id') if metadata else None
            )
            
            # Publish alert if critical
            if voice_result.get('alert_level') == 'CRITICAL' and self.enable_pubsub:
                self._publish_alert(cbs_signal, fused_record)
            
            return {
                "status": "success",
                "message": "Voice alert processed successfully",
                "transcription": voice_result.get('transcription'),
                "symptoms": voice_result.get('symptoms'),
                "severity": voice_result.get('severity'),
                "alert_level": voice_result.get('alert_level'),
                "record_id": fused_record.get('record_id'),
                "verification_score": fused_record.get('verification_score'),
                "timestamp": datetime.utcnow().isoformat()
            }
        
        except Exception as e:
            logger.error(f"❌ Voice alert processing failed: {e}")
            return {
                "status": "error",
                "error": "processing_failed",
                "message": str(e)
            }, 500
    
    def get_verification_status(self, record_id: str) -> Dict:
        """
        Get verification status of a submitted record.
        
        Args:
            record_id: Record identifier
        
        Returns:
            Verification status
        """
        try:
            # Query Golden Thread for record
            record = self.golden_thread.get_record(record_id)
            
            if not record:
                return {
                    "status": "error",
                    "error": "record_not_found",
                    "message": f"Record {record_id} not found"
                }, 404
            
            return {
                "status": "success",
                "record_id": record_id,
                "verification_score": record.get('verification_score'),
                "verification_status": self._get_verification_status(
                    record.get('verification_score', 0)
                ),
                "sources": record.get('sources', []),
                "timestamp": record.get('timestamp'),
                "last_updated": record.get('last_updated')
            }
        
        except Exception as e:
            logger.error(f"❌ Verification query failed: {e}")
            return {
                "status": "error",
                "error": "query_failed",
                "message": str(e)
            }, 500
    
    def _get_verification_status(self, score: float) -> str:
        """Convert verification score to status"""
        if score >= 1.0:
            return "CONFIRMED"
        elif score >= 0.7:
            return "PROBABLE"
        elif score >= 0.4:
            return "POSSIBLE"
        else:
            return "UNVERIFIED"
    
    def _publish_alert(self, cbs_signal: Dict, fused_record: Dict):
        """Publish alert to PubSub"""
        try:
            alert = {
                "alert_type": "health_event",
                "severity": cbs_signal.get('severity'),
                "location": cbs_signal.get('location'),
                "symptoms": cbs_signal.get('symptoms'),
                "verification_score": fused_record.get('verification_score'),
                "timestamp": datetime.utcnow().isoformat()
            }
            
            message_data = json.dumps(alert).encode('utf-8')
            future = self.publisher.publish(self.topic_path, message_data)
            future.result()
            
            logger.info(f"🚨 Alert published - Severity: {cbs_signal.get('severity')}")
        
        except Exception as e:
            logger.error(f"❌ Alert publishing failed: {e}")


# Initialize Bio-Interface
bio_interface = BioInterface(
    project_id=os.getenv('GOOGLE_CLOUD_PROJECT', 'iluminara-health'),
    jurisdiction=os.getenv('JURISDICTION', 'KDPA_KE')
)


# REST API Endpoints

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        "status": "healthy",
        "service": "Bio-Interface API",
        "version": "1.0.0",
        "timestamp": datetime.utcnow().isoformat()
    })


@app.route('/api/v1/cbs/submit', methods=['POST'])
def submit_cbs():
    """Submit CBS report"""
    data = request.get_json()
    
    result = bio_interface.submit_cbs_report(
        location=data.get('location'),
        symptoms=data.get('symptoms'),
        severity=data.get('severity'),
        reporter_id=data.get('reporter_id'),
        source=DataSource(data.get('source', 'mobile_app')),
        metadata=data.get('metadata')
    )
    
    if isinstance(result, tuple):
        return jsonify(result[0]), result[1]
    return jsonify(result)


@app.route('/api/v1/emr/submit', methods=['POST'])
def submit_emr():
    """Submit EMR record"""
    data = request.get_json()
    
    result = bio_interface.submit_emr_record(
        patient_id=data.get('patient_id'),
        location=data.get('location'),
        diagnosis=data.get('diagnosis'),
        symptoms=data.get('symptoms'),
        facility_id=data.get('facility_id'),
        metadata=data.get('metadata')
    )
    
    if isinstance(result, tuple):
        return jsonify(result[0]), result[1]
    return jsonify(result)


@app.route('/api/v1/voice/submit', methods=['POST'])
def submit_voice():
    """Submit voice alert"""
    audio_data = request.data
    location = request.args.get('location')
    reporter_id = request.args.get('reporter_id')
    language = request.args.get('language', 'swahili')
    
    if not audio_data:
        return jsonify({
            "status": "error",
            "error": "no_audio_data",
            "message": "No audio data provided"
        }), 400
    
    result = bio_interface.submit_voice_alert(
        audio_data=audio_data,
        location=json.loads(location) if location else {},
        reporter_id=reporter_id,
        language=language
    )
    
    if isinstance(result, tuple):
        return jsonify(result[0]), result[1]
    return jsonify(result)


@app.route('/api/v1/verification/<record_id>', methods=['GET'])
def get_verification(record_id):
    """Get verification status"""
    result = bio_interface.get_verification_status(record_id)
    
    if isinstance(result, tuple):
        return jsonify(result[0]), result[1]
    return jsonify(result)


if __name__ == '__main__':
    port = int(os.getenv('PORT', 8080))
    app.run(host='0.0.0.0', port=port, debug=False)
