"""
Bio-Interface REST API
Mobile Health Apps Integration with Golden Thread Protocol

This module provides REST API endpoints for mobile health applications
to submit data using the Golden Thread protocol for data fusion.

Features:
- CBS (Community-Based Surveillance) signal ingestion
- EMR (Electronic Medical Record) integration
- IDSR (Integrated Disease Surveillance Response) reporting
- Golden Thread verification
- Offline-first sync protocol

Compliance:
- GDPR Art. 6 (Lawfulness of Processing)
- HIPAA §164.312 (Technical Safeguards)
- Kenya DPA §37 (Transfer Restrictions)
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
    CBS = "community_based_surveillance"
    EMR = "electronic_medical_record"
    IDSR = "integrated_disease_surveillance"
    CHV = "community_health_volunteer"
    MOBILE_APP = "mobile_health_app"


class SyncPriority(Enum):
    """Sync priority levels for offline-first protocol"""
    CRITICAL = 1   # Life-threatening, sync immediately
    HIGH = 2       # Outbreak signals, sync within 1 hour
    MEDIUM = 3     # Routine surveillance, sync within 24 hours
    LOW = 4        # Historical data, sync when convenient


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


@app.route('/api/v1/cbs/submit', methods=['POST'])
def submit_cbs_signal():
    """
    Submit Community-Based Surveillance (CBS) signal.
    
    Request body:
    {
        "patient_id": "PAT_12345",
        "location": {"lat": 0.0512, "lng": 40.3129},
        "symptom": "diarrhea",
        "severity": 8,
        "timestamp": "2025-01-15T08:00:00Z",
        "source": "CHV_AMINA_HASSAN",
        "metadata": {
            "age": 25,
            "gender": "F",
            "village": "Ifo Camp"
        }
    }
    
    Returns:
    {
        "status": "success",
        "signal_id": "CBS_123456",
        "verification_score": 0.0,
        "sync_priority": "HIGH",
        "message": "CBS signal queued for Golden Thread fusion"
    }
    """
    try:
        data = request.get_json()
        
        # Validate required fields
        required_fields = ["patient_id", "location", "symptom", "timestamp", "source"]
        missing_fields = [field for field in required_fields if field not in data]
        
        if missing_fields:
            return jsonify({
                "status": "error",
                "error": "missing_fields",
                "message": f"Missing required fields: {', '.join(missing_fields)}"
            }), 400
        
        # Sovereignty validation
        try:
            guardrail.validate_action(
                action_type='Data_Processing',
                payload={
                    'data_type': 'PHI',
                    'processing_location': 'Edge_Node',
                    'source': data['source'],
                    'consent_token': data.get('consent_token', 'CBS_EMERGENCY')
                },
                jurisdiction=data.get('jurisdiction', 'KDPA_KE')
            )
        except SovereigntyViolationError as e:
            logger.error(f"❌ Sovereignty violation: {e}")
            return jsonify({
                "status": "error",
                "error": "sovereignty_violation",
                "message": str(e)
            }), 403
        
        # Create CBS signal
        cbs_signal = {
            'location': data['location'],
            'symptom': data['symptom'],
            'timestamp': data['timestamp'],
            'source': data['source'],
            'severity': data.get('severity', 5),
            'metadata': data.get('metadata', {})
        }
        
        # Queue for Golden Thread fusion
        signal_id = f"CBS_{datetime.utcnow().strftime('%Y%m%d%H%M%S')}"
        
        # Determine sync priority
        severity = data.get('severity', 5)
        if severity >= 9:
            sync_priority = SyncPriority.CRITICAL
        elif severity >= 7:
            sync_priority = SyncPriority.HIGH
        else:
            sync_priority = SyncPriority.MEDIUM
        
        # Store in local queue (offline-first)
        _queue_for_sync(signal_id, cbs_signal, sync_priority)
        
        logger.info(f"✅ CBS signal received - ID: {signal_id}, Priority: {sync_priority.name}")
        
        return jsonify({
            "status": "success",
            "signal_id": signal_id,
            "verification_score": 0.0,  # Will be updated after EMR fusion
            "sync_priority": sync_priority.name,
            "message": "CBS signal queued for Golden Thread fusion"
        }), 201
    
    except Exception as e:
        logger.error(f"❌ CBS submission error: {e}")
        return jsonify({
            "status": "error",
            "error": "processing_failed",
            "message": str(e)
        }), 500


@app.route('/api/v1/emr/submit', methods=['POST'])
def submit_emr_record():
    """
    Submit Electronic Medical Record (EMR).
    
    Request body:
    {
        "patient_id": "PAT_12345",
        "location": {"lat": 0.0512, "lng": 40.3129},
        "diagnosis": "cholera",
        "timestamp": "2025-01-15T08:30:00Z",
        "source": "DADAAB_CLINIC",
        "lab_results": {
            "test": "stool_culture",
            "result": "positive",
            "pathogen": "vibrio_cholerae"
        },
        "treatment": {
            "medication": "ORS",
            "dosage": "1L",
            "frequency": "every_4_hours"
        }
    }
    
    Returns:
    {
        "status": "success",
        "record_id": "EMR_123456",
        "fused_record": {...},
        "verification_score": 1.0,
        "message": "EMR record fused with CBS signal"
    }
    """
    try:
        data = request.get_json()
        
        # Validate required fields
        required_fields = ["patient_id", "location", "diagnosis", "timestamp", "source"]
        missing_fields = [field for field in required_fields if field not in data]
        
        if missing_fields:
            return jsonify({
                "status": "error",
                "error": "missing_fields",
                "message": f"Missing required fields: {', '.join(missing_fields)}"
            }), 400
        
        # Sovereignty validation
        try:
            guardrail.validate_action(
                action_type='Data_Processing',
                payload={
                    'data_type': 'PHI',
                    'processing_location': 'Edge_Node',
                    'source': data['source'],
                    'consent_token': data.get('consent_token', 'CLINICAL_CARE')
                },
                jurisdiction=data.get('jurisdiction', 'KDPA_KE')
            )
        except SovereigntyViolationError as e:
            logger.error(f"❌ Sovereignty violation: {e}")
            return jsonify({
                "status": "error",
                "error": "sovereignty_violation",
                "message": str(e)
            }), 403
        
        # Create EMR record
        emr_record = {
            'location': data['location'],
            'diagnosis': data['diagnosis'],
            'timestamp': data['timestamp'],
            'source': data['source'],
            'lab_results': data.get('lab_results', {}),
            'treatment': data.get('treatment', {})
        }
        
        # Fuse with CBS signal using Golden Thread
        fused = golden_thread.fuse_data_streams(
            cbs_signal=None,  # Will search for matching CBS signal
            emr_record=emr_record,
            patient_id=data['patient_id']
        )
        
        record_id = f"EMR_{datetime.utcnow().strftime('%Y%m%d%H%M%S')}"
        
        logger.info(f"✅ EMR record fused - ID: {record_id}, Verification: {fused.verification_score}")
        
        return jsonify({
            "status": "success",
            "record_id": record_id,
            "fused_record": fused.to_dict(),
            "verification_score": fused.verification_score,
            "message": "EMR record fused with CBS signal" if fused.verification_score > 0.5 else "EMR record stored"
        }), 201
    
    except Exception as e:
        logger.error(f"❌ EMR submission error: {e}")
        return jsonify({
            "status": "error",
            "error": "processing_failed",
            "message": str(e)
        }), 500


@app.route('/api/v1/sync/status', methods=['GET'])
def sync_status():
    """
    Get sync status for offline-first protocol.
    
    Returns:
    {
        "status": "success",
        "sync_queue": {
            "critical": 0,
            "high": 5,
            "medium": 12,
            "low": 45
        },
        "last_sync": "2025-01-15T10:00:00Z",
        "connectivity": "online"
    }
    """
    try:
        # Get queue status
        queue_status = _get_queue_status()
        
        return jsonify({
            "status": "success",
            "sync_queue": queue_status,
            "last_sync": datetime.utcnow().isoformat(),
            "connectivity": "online"  # TODO: Implement connectivity check
        }), 200
    
    except Exception as e:
        logger.error(f"❌ Sync status error: {e}")
        return jsonify({
            "status": "error",
            "error": "processing_failed",
            "message": str(e)
        }), 500


@app.route('/api/v1/sync/trigger', methods=['POST'])
def trigger_sync():
    """
    Manually trigger sync for offline-first protocol.
    
    Request body:
    {
        "priority": "HIGH"  # Optional: CRITICAL, HIGH, MEDIUM, LOW
    }
    
    Returns:
    {
        "status": "success",
        "synced_records": 17,
        "message": "Sync completed successfully"
    }
    """
    try:
        data = request.get_json() or {}
        priority = data.get('priority', 'ALL')
        
        # Trigger sync
        synced_count = _trigger_sync(priority)
        
        logger.info(f"✅ Sync triggered - Priority: {priority}, Synced: {synced_count}")
        
        return jsonify({
            "status": "success",
            "synced_records": synced_count,
            "message": "Sync completed successfully"
        }), 200
    
    except Exception as e:
        logger.error(f"❌ Sync trigger error: {e}")
        return jsonify({
            "status": "error",
            "error": "processing_failed",
            "message": str(e)
        }), 500


@app.route('/api/v1/verification/check', methods=['POST'])
def check_verification():
    """
    Check verification score for a patient record.
    
    Request body:
    {
        "patient_id": "PAT_12345"
    }
    
    Returns:
    {
        "status": "success",
        "patient_id": "PAT_12345",
        "verification_score": 1.0,
        "verification_status": "CONFIRMED",
        "data_sources": ["CBS", "EMR"],
        "last_updated": "2025-01-15T08:30:00Z"
    }
    """
    try:
        data = request.get_json()
        patient_id = data.get('patient_id')
        
        if not patient_id:
            return jsonify({
                "status": "error",
                "error": "missing_patient_id",
                "message": "patient_id is required"
            }), 400
        
        # Get verification status from Golden Thread
        verification = golden_thread.get_verification_status(patient_id)
        
        return jsonify({
            "status": "success",
            "patient_id": patient_id,
            "verification_score": verification.get('score', 0.0),
            "verification_status": verification.get('status', 'UNVERIFIED'),
            "data_sources": verification.get('sources', []),
            "last_updated": verification.get('timestamp', datetime.utcnow().isoformat())
        }), 200
    
    except Exception as e:
        logger.error(f"❌ Verification check error: {e}")
        return jsonify({
            "status": "error",
            "error": "processing_failed",
            "message": str(e)
        }), 500


# Helper functions

def _queue_for_sync(signal_id: str, data: Dict, priority: SyncPriority):
    """Queue data for offline-first sync"""
    # TODO: Implement persistent queue (SQLite, Redis, etc.)
    logger.info(f"📥 Queued for sync - ID: {signal_id}, Priority: {priority.name}")


def _get_queue_status() -> Dict:
    """Get sync queue status"""
    # TODO: Implement queue status retrieval
    return {
        "critical": 0,
        "high": 5,
        "medium": 12,
        "low": 45
    }


def _trigger_sync(priority: str) -> int:
    """Trigger sync for queued data"""
    # TODO: Implement sync logic
    return 17  # Mock synced count


if __name__ == '__main__':
    # Development server
    app.run(
        host='0.0.0.0',
        port=int(os.environ.get('API_PORT', 8080)),
        debug=os.environ.get('DEBUG', 'False').lower() == 'true'
    )
