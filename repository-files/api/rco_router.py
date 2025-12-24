"""
RCO API Router
Exposes Regenerative Compliance Oracle endpoints with Somatic Auth.

Endpoints:
- GET /rco/predictions - Get predicted amendments
- GET /rco/drift - Get current compliance drift
- GET /rco/patches - Get pending patches
- POST /rco/patches/{patch_id}/approve - Approve patch (requires Somatic Auth)
- POST /rco/signals - Ingest external regulatory signal
"""

from flask import Blueprint, request, jsonify
from governance_kernel.rco_engine import (
    RegenerativeComplianceOracle,
    RegulatorySignal,
    LawAmendmentConfidence
)
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

# Create Blueprint
rco_bp = Blueprint('rco', __name__, url_prefix='/rco')

# Initialize RCO (singleton)
rco = RegenerativeComplianceOracle(
    laws_path="config/sectoral_laws.json",
    enable_auto_patch=False
)


@rco_bp.route('/health', methods=['GET'])
def health_check():
    """RCO health check"""
    return jsonify({
        "status": "operational",
        "service": "Regenerative Compliance Oracle",
        "version": "1.0.0",
        "timestamp": datetime.utcnow().isoformat()
    })


@rco_bp.route('/predictions', methods=['GET'])
def get_predictions():
    """
    Get predicted regulatory amendments.
    
    Query params:
    - framework_id: Optional framework to filter
    """
    framework_id = request.args.get('framework_id')
    
    try:
        if framework_id:
            # Predict for specific framework
            prob, confidence, metadata = rco.oracle.predict_amendment(framework_id)
            
            predictions = [{
                "framework_id": framework_id,
                "amendment_probability": prob,
                "confidence": confidence.value,
                "metadata": metadata
            }]
        else:
            # Predict for all frameworks with signals
            frameworks = ["EU_AI_ACT", "GDPR", "KDPA", "HIPAA", "WHO_IHR"]
            predictions = []
            
            for fw in frameworks:
                prob, confidence, metadata = rco.oracle.predict_amendment(fw)
                
                if prob > 0.10:  # Only show significant predictions
                    predictions.append({
                        "framework_id": fw,
                        "amendment_probability": prob,
                        "confidence": confidence.value,
                        "metadata": metadata
                    })
        
        return jsonify({
            "status": "success",
            "timestamp": datetime.utcnow().isoformat(),
            "predictions": predictions
        })
    
    except Exception as e:
        logger.error(f"❌ Prediction failed: {e}")
        return jsonify({
            "status": "error",
            "error": "prediction_failed",
            "message": str(e)
        }), 500


@rco_bp.route('/drift', methods=['GET'])
def get_drift():
    """
    Get current compliance drift measurements.
    
    Query params:
    - framework_id: Optional framework to filter
    """
    framework_id = request.args.get('framework_id')
    
    try:
        # Get drift history
        drift_history = rco.sensor.drift_history
        
        if framework_id:
            # Filter by framework
            drift_history = [
                d for d in drift_history
                if d.framework_id == framework_id
            ]
        
        # Get latest drift for each framework
        latest_drift = {}
        for drift in drift_history:
            fw = drift.framework_id
            if fw not in latest_drift or drift.timestamp > latest_drift[fw].timestamp:
                latest_drift[fw] = drift
        
        # Format response
        drift_data = [
            {
                "framework_id": drift.framework_id,
                "drift_score": drift.drift_score,
                "drift_level": drift.drift_level.value,
                "contributing_factors": drift.contributing_factors,
                "recommended_action": drift.recommended_action,
                "timestamp": drift.timestamp
            }
            for drift in latest_drift.values()
        ]
        
        return jsonify({
            "status": "success",
            "timestamp": datetime.utcnow().isoformat(),
            "drift_measurements": drift_data
        })
    
    except Exception as e:
        logger.error(f"❌ Drift retrieval failed: {e}")
        return jsonify({
            "status": "error",
            "error": "drift_retrieval_failed",
            "message": str(e)
        }), 500


@rco_bp.route('/patches', methods=['GET'])
def get_patches():
    """
    Get pending law-as-code patches.
    
    Query params:
    - status: 'pending' (default) or 'all'
    """
    status = request.args.get('status', 'pending')
    
    try:
        if status == 'pending':
            patches = rco.get_pending_patches()
        else:
            patches = rco.generator.patch_history
        
        # Format response
        patch_data = [
            {
                "patch_id": patch.patch_id,
                "framework_id": patch.framework_id,
                "patch_type": patch.patch_type,
                "changes": patch.changes,
                "rationale": patch.rationale,
                "confidence": patch.confidence,
                "requires_approval": patch.requires_approval,
                "approved": patch.approved,
                "approved_by": patch.approved_by,
                "approved_at": patch.approved_at,
                "created_at": patch.created_at
            }
            for patch in patches
        ]
        
        return jsonify({
            "status": "success",
            "timestamp": datetime.utcnow().isoformat(),
            "patches": patch_data,
            "count": len(patch_data)
        })
    
    except Exception as e:
        logger.error(f"❌ Patch retrieval failed: {e}")
        return jsonify({
            "status": "error",
            "error": "patch_retrieval_failed",
            "message": str(e)
        }), 500


@rco_bp.route('/patches/<patch_id>/approve', methods=['POST'])
def approve_patch(patch_id):
    """
    Approve a pending patch (requires Somatic Auth).
    
    Body:
    {
        "approved_by": "user_id",
        "somatic_auth_token": "token",
        "historical_events": [...]
    }
    """
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({
                "status": "error",
                "error": "missing_body",
                "message": "Request body required"
            }), 400
        
        approved_by = data.get('approved_by')
        somatic_auth_token = data.get('somatic_auth_token')
        historical_events = data.get('historical_events', [])
        
        if not approved_by:
            return jsonify({
                "status": "error",
                "error": "missing_approved_by",
                "message": "approved_by field required"
            }), 400
        
        # TODO: Validate Somatic Auth token (IP-03 Acorn Protocol)
        # For now, we'll accept any token
        if not somatic_auth_token:
            return jsonify({
                "status": "error",
                "error": "missing_somatic_auth",
                "message": "Somatic authentication required for patch approval"
            }), 403
        
        # Approve patch
        success, audit_report = rco.approve_patch(
            patch_id=patch_id,
            approved_by=approved_by,
            historical_events=historical_events
        )
        
        if success:
            return jsonify({
                "status": "success",
                "message": "Patch approved and applied",
                "patch_id": patch_id,
                "approved_by": approved_by,
                "audit_report": audit_report,
                "timestamp": datetime.utcnow().isoformat()
            })
        else:
            return jsonify({
                "status": "error",
                "error": "approval_failed",
                "message": "Patch approval failed (see audit_report)",
                "audit_report": audit_report
            }), 400
    
    except Exception as e:
        logger.error(f"❌ Patch approval failed: {e}")
        return jsonify({
            "status": "error",
            "error": "approval_failed",
            "message": str(e)
        }), 500


@rco_bp.route('/signals', methods=['POST'])
def ingest_signal():
    """
    Ingest external regulatory signal.
    
    Body:
    {
        "source": "EU_AI_Act_Draft_Code_Dec2025",
        "content": "Draft Code of Practice released",
        "impact_frameworks": ["EU_AI_ACT", "GDPR"],
        "confidence": 0.87,
        "metadata": {...}
    }
    """
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({
                "status": "error",
                "error": "missing_body",
                "message": "Request body required"
            }), 400
        
        # Validate required fields
        required_fields = ['source', 'content', 'impact_frameworks', 'confidence']
        for field in required_fields:
            if field not in data:
                return jsonify({
                    "status": "error",
                    "error": f"missing_{field}",
                    "message": f"{field} field required"
                }), 400
        
        # Create signal
        signal = RegulatorySignal(
            signal_id=f"SIG_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}",
            source=data['source'],
            timestamp=datetime.utcnow().isoformat(),
            content=data['content'],
            impact_frameworks=data['impact_frameworks'],
            confidence=data['confidence'],
            metadata=data.get('metadata', {})
        )
        
        # Ingest into RCO
        rco.oracle.ingest_signal(signal)
        
        logger.info(f"📡 Signal ingested: {signal.source}")
        
        return jsonify({
            "status": "success",
            "message": "Signal ingested successfully",
            "signal_id": signal.signal_id,
            "timestamp": datetime.utcnow().isoformat()
        })
    
    except Exception as e:
        logger.error(f"❌ Signal ingestion failed: {e}")
        return jsonify({
            "status": "error",
            "error": "ingestion_failed",
            "message": str(e)
        }), 500


@rco_bp.route('/status', methods=['GET'])
def get_status():
    """Get overall RCO status"""
    try:
        # Get pending patches
        pending_patches = rco.get_pending_patches()
        
        # Get latest drift
        drift_history = rco.sensor.drift_history
        latest_drift = {}
        for drift in drift_history:
            fw = drift.framework_id
            if fw not in latest_drift or drift.timestamp > latest_drift[fw].timestamp:
                latest_drift[fw] = drift
        
        # Count critical drift
        critical_drift_count = sum(
            1 for d in latest_drift.values()
            if d.drift_level.value in ["CRITICAL", "CATASTROPHIC"]
        )
        
        # Get signal count
        signal_count = len(rco.oracle.external_signals)
        
        return jsonify({
            "status": "operational",
            "timestamp": datetime.utcnow().isoformat(),
            "metrics": {
                "pending_patches": len(pending_patches),
                "critical_drift_count": critical_drift_count,
                "total_frameworks_monitored": len(latest_drift),
                "external_signals_ingested": signal_count
            },
            "health": "healthy" if critical_drift_count == 0 else "degraded"
        })
    
    except Exception as e:
        logger.error(f"❌ Status retrieval failed: {e}")
        return jsonify({
            "status": "error",
            "error": "status_retrieval_failed",
            "message": str(e)
        }), 500


# Register blueprint in main app
def register_rco_routes(app):
    """Register RCO routes with Flask app"""
    app.register_blueprint(rco_bp)
    logger.info("🌟 RCO API routes registered")


if __name__ == "__main__":
    # Test endpoints
    from flask import Flask
    
    app = Flask(__name__)
    register_rco_routes(app)
    
    print("🌟 RCO API Server starting...")
    print("📡 Endpoints:")
    print("   GET  /rco/health")
    print("   GET  /rco/predictions")
    print("   GET  /rco/drift")
    print("   GET  /rco/patches")
    print("   POST /rco/patches/<patch_id>/approve")
    print("   POST /rco/signals")
    print("   GET  /rco/status")
    
    app.run(host='0.0.0.0', port=8081, debug=True)
