"""
Compliance API Router
REST API endpoints for Governance Kernel v3.0

Endpoints:
- POST /api/compliance/validate - Validate action against regulations
- POST /api/compliance/audit/retroactive - Retroactive compliance audit
- POST /api/compliance/audit/prospective - Prospective compliance audit
- GET /api/compliance/frameworks - Get applicable frameworks
- GET /api/compliance/sectors - List supported sectors
- POST /api/compliance/conflicts/resolve - Resolve regulatory conflicts
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import logging
from typing import Dict, Optional
from datetime import datetime

# Import Governance Kernel v3.0
try:
    from governance_kernel.sovereign_guardrail_v3 import SovereignGuardrailV3, SovereigntyViolationError
    from governance_kernel.sectoral_compliance_engine import Sector
    from governance_kernel.quantum_nexus import ConflictResolutionStrategy
except ImportError:
    logging.error("Failed to import Governance Kernel v3.0 components")
    SovereignGuardrailV3 = None

logger = logging.getLogger(__name__)

# Initialize Flask app
app = Flask(__name__)
CORS(app)

# Initialize Governance Kernel
guardrail = None
if SovereignGuardrailV3:
    try:
        guardrail = SovereignGuardrailV3(
            enable_sectoral_validation=True,
            enable_quantum_resolution=True,
            enable_chrono_audit=True
        )
        logger.info("✅ Governance Kernel v3.0 initialized")
    except Exception as e:
        logger.error(f"❌ Failed to initialize Governance Kernel: {e}")


@app.route('/api/compliance/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        "status": "operational",
        "version": "3.0.0",
        "timestamp": datetime.utcnow().isoformat(),
        "components": {
            "sovereign_guardrail": guardrail is not None,
            "sectoral_engine": guardrail.sectoral_engine is not None if guardrail else False,
            "quantum_nexus": guardrail.quantum_nexus is not None if guardrail else False,
            "chrono_engine": guardrail.chrono_engine is not None if guardrail else False
        }
    }), 200


@app.route('/api/compliance/validate', methods=['POST'])
def validate_action():
    """
    Validate action against all applicable regulations.
    
    Request body:
    {
        "action_type": "Data_Transfer",
        "payload": {
            "data_type": "PHI",
            "destination": "Local_Node",
            "actor": "ml_system",
            "resource": "patient_records"
        },
        "jurisdiction": "KDPA_KE",
        "sector": "health"
    }
    
    Response:
    {
        "compliant": true,
        "timestamp": "2025-12-24T...",
        "frameworks_validated": ["KDPA", "GDPR", "HIPAA"],
        "sectoral_validation": {...},
        "conflicts_detected": 0
    }
    """
    if not guardrail:
        return jsonify({"error": "Governance Kernel not available"}), 503
    
    try:
        data = request.get_json()
        
        # Validate required fields
        required_fields = ["action_type", "payload", "jurisdiction"]
        for field in required_fields:
            if field not in data:
                return jsonify({"error": f"Missing required field: {field}"}), 400
        
        # Validate action
        result = guardrail.validate_action(
            action_type=data["action_type"],
            payload=data["payload"],
            jurisdiction=data["jurisdiction"],
            sector=data.get("sector")
        )
        
        return jsonify(result), 200
    
    except SovereigntyViolationError as e:
        return jsonify({
            "error": "sovereignty_violation",
            "message": str(e),
            "timestamp": datetime.utcnow().isoformat()
        }), 403
    
    except Exception as e:
        logger.error(f"❌ Validation error: {e}")
        return jsonify({
            "error": "validation_failed",
            "message": str(e)
        }), 500


@app.route('/api/compliance/audit/retroactive', methods=['POST'])
def retroactive_audit():
    """
    Perform retroactive compliance audit.
    
    Request body:
    {
        "start_date": "2024-01-01T00:00:00",
        "end_date": "2025-12-31T23:59:59",
        "jurisdiction": "KDPA_KE",
        "sector": "health"
    }
    
    Response:
    {
        "report_id": "abc123",
        "compliance_rate": 0.95,
        "events_analyzed": 1000,
        "violations": [...]
    }
    """
    if not guardrail:
        return jsonify({"error": "Governance Kernel not available"}), 503
    
    try:
        data = request.get_json()
        
        # Validate required fields
        required_fields = ["start_date", "end_date"]
        for field in required_fields:
            if field not in data:
                return jsonify({"error": f"Missing required field: {field}"}), 400
        
        # Perform audit
        report = guardrail.retroactive_compliance_check(
            start_date=data["start_date"],
            end_date=data["end_date"],
            jurisdiction=data.get("jurisdiction"),
            sector=data.get("sector")
        )
        
        return jsonify(report), 200
    
    except Exception as e:
        logger.error(f"❌ Retroactive audit error: {e}")
        return jsonify({
            "error": "audit_failed",
            "message": str(e)
        }), 500


@app.route('/api/compliance/audit/prospective', methods=['POST'])
def prospective_audit():
    """
    Perform prospective compliance audit for upcoming regulation.
    
    Request body:
    {
        "upcoming_regulation": {
            "name": "EU AI Act Amendment 2026",
            "required_fields": ["explainability", "bias_assessment"]
        },
        "effective_date": "2026-01-01T00:00:00",
        "jurisdiction": "GDPR_EU",
        "sector": "health"
    }
    
    Response:
    {
        "report_id": "xyz789",
        "compliance_rate": 0.75,
        "gaps_identified": 25,
        "recommendations": [...]
    }
    """
    if not guardrail:
        return jsonify({"error": "Governance Kernel not available"}), 503
    
    try:
        data = request.get_json()
        
        # Validate required fields
        required_fields = ["upcoming_regulation", "effective_date", "jurisdiction"]
        for field in required_fields:
            if field not in data:
                return jsonify({"error": f"Missing required field: {field}"}), 400
        
        # Perform audit
        report = guardrail.prospective_compliance_check(
            upcoming_regulation=data["upcoming_regulation"],
            effective_date=data["effective_date"],
            jurisdiction=data["jurisdiction"],
            sector=data.get("sector")
        )
        
        return jsonify(report), 200
    
    except Exception as e:
        logger.error(f"❌ Prospective audit error: {e}")
        return jsonify({
            "error": "audit_failed",
            "message": str(e)
        }), 500


@app.route('/api/compliance/frameworks', methods=['GET'])
def get_frameworks():
    """
    Get applicable legal frameworks.
    
    Query parameters:
    - jurisdiction: Jurisdiction code (e.g., KDPA_KE)
    - sector: Sector name (e.g., health)
    - action_type: Action type (optional)
    
    Response:
    {
        "frameworks": ["KDPA", "GDPR", "HIPAA", "HITECH"],
        "count": 4
    }
    """
    if not guardrail:
        return jsonify({"error": "Governance Kernel not available"}), 503
    
    try:
        jurisdiction = request.args.get('jurisdiction')
        sector = request.args.get('sector')
        action_type = request.args.get('action_type')
        
        if not jurisdiction:
            return jsonify({"error": "Missing required parameter: jurisdiction"}), 400
        
        frameworks = guardrail.get_applicable_frameworks(
            jurisdiction=jurisdiction,
            sector=sector,
            action_type=action_type
        )
        
        return jsonify({
            "frameworks": frameworks,
            "count": len(frameworks),
            "jurisdiction": jurisdiction,
            "sector": sector
        }), 200
    
    except Exception as e:
        logger.error(f"❌ Get frameworks error: {e}")
        return jsonify({
            "error": "query_failed",
            "message": str(e)
        }), 500


@app.route('/api/compliance/sectors', methods=['GET'])
def list_sectors():
    """
    List all supported sectors.
    
    Response:
    {
        "sectors": [
            {"name": "health", "frameworks_count": 14},
            {"name": "finance", "frameworks_count": 8},
            ...
        ]
    }
    """
    if not guardrail or not guardrail.sectoral_engine:
        return jsonify({"error": "Sectoral engine not available"}), 503
    
    try:
        sectors = [
            {"name": "health", "frameworks_count": 14, "description": "Healthcare and medical data"},
            {"name": "finance", "frameworks_count": 8, "description": "Financial services and transactions"},
            {"name": "education", "frameworks_count": 3, "description": "Educational institutions and student data"},
            {"name": "energy", "frameworks_count": 2, "description": "Energy infrastructure and utilities"},
            {"name": "transport", "frameworks_count": 3, "description": "Transportation and logistics"},
            {"name": "agriculture", "frameworks_count": 2, "description": "Agriculture and food safety"},
            {"name": "manufacturing", "frameworks_count": 2, "description": "Manufacturing and quality standards"},
            {"name": "telecommunications", "frameworks_count": 3, "description": "Telecommunications and data transmission"}
        ]
        
        return jsonify({
            "sectors": sectors,
            "total_sectors": len(sectors),
            "total_frameworks": sum(s["frameworks_count"] for s in sectors)
        }), 200
    
    except Exception as e:
        logger.error(f"❌ List sectors error: {e}")
        return jsonify({
            "error": "query_failed",
            "message": str(e)
        }), 500


@app.route('/api/compliance/conflicts/resolve', methods=['POST'])
def resolve_conflicts():
    """
    Resolve regulatory conflicts using QuantumNexus.
    
    Request body:
    {
        "frameworks": ["GDPR", "HIPAA", "KDPA"],
        "action": {
            "type": "Data_Transfer",
            "destination": "EU_Cloud"
        },
        "jurisdiction": "KDPA_KE",
        "strategy": "STRICTEST"
    }
    
    Response:
    {
        "conflicts_detected": 2,
        "resolution_strategy": "STRICTEST",
        "recommended_action": "BLOCK",
        "explanation": "..."
    }
    """
    if not guardrail or not guardrail.quantum_nexus:
        return jsonify({"error": "QuantumNexus not available"}), 503
    
    try:
        data = request.get_json()
        
        # Validate required fields
        required_fields = ["frameworks", "action", "jurisdiction"]
        for field in required_fields:
            if field not in data:
                return jsonify({"error": f"Missing required field: {field}"}), 400
        
        # Detect conflicts
        conflicts = guardrail.quantum_nexus.detect_conflicts(
            frameworks=data["frameworks"],
            action=data["action"],
            jurisdiction=data["jurisdiction"]
        )
        
        if not conflicts:
            return jsonify({
                "conflicts_detected": 0,
                "message": "No conflicts detected"
            }), 200
        
        # Resolve conflicts
        strategy_name = data.get("strategy", "STRICTEST")
        strategy = ConflictResolutionStrategy[strategy_name]
        
        resolution = guardrail.quantum_nexus.resolve_conflicts(
            conflicts=conflicts,
            strategy=strategy
        )
        
        return jsonify({
            "conflicts_detected": len(conflicts),
            "conflicts": [c.to_dict() for c in conflicts],
            "resolution": resolution.to_dict()
        }), 200
    
    except Exception as e:
        logger.error(f"❌ Conflict resolution error: {e}")
        return jsonify({
            "error": "resolution_failed",
            "message": str(e)
        }), 500


# Error handlers
@app.errorhandler(404)
def not_found(error):
    return jsonify({"error": "endpoint_not_found"}), 404


@app.errorhandler(500)
def internal_error(error):
    return jsonify({"error": "internal_server_error"}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8081, debug=True)
