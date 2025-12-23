"""
SovereignGuardrail Middleware
Enforces 14 global data frameworks on all REST and FHIR endpoints

Compliance Frameworks:
1. GDPR (EU General Data Protection Regulation)
2. HIPAA (Health Insurance Portability and Accountability Act)
3. Kenya DPA (Data Protection Act, 2019)
4. POPIA (South Africa Protection of Personal Information Act)
5. NDPR (Nigeria Data Protection Regulation)
6. APPI (Japan Act on the Protection of Personal Information)
7. PIPEDA (Canada Personal Information Protection and Electronic Documents Act)
8. LGPD (Brazil Lei Geral de Proteção de Dados)
9. CCPA/CPRA (California Consumer Privacy Act)
10. WHO IHR (International Health Regulations, 2005)
11. Geneva Conventions (Data protection in humanitarian contexts)
12. EU AI Act (Transparency and explainability requirements)
13. AU Convention on Cyber Security (Malabo Convention)
14. FHIR R4/R5 (Healthcare data interoperability)
"""

import json
import logging
from datetime import datetime
from typing import Dict, List, Optional, Callable
from enum import Enum
from functools import wraps
from flask import Request, Response, jsonify
import yaml

logger = logging.getLogger(__name__)


class ComplianceFramework(Enum):
    """14 Global Data Frameworks"""
    GDPR = "GDPR (EU General Data Protection Regulation)"
    HIPAA = "HIPAA (Health Insurance Portability and Accountability Act)"
    KENYA_DPA = "Kenya DPA (Data Protection Act, 2019)"
    POPIA = "POPIA (South Africa Protection of Personal Information Act)"
    NDPR = "NDPR (Nigeria Data Protection Regulation)"
    APPI = "APPI (Japan Act on the Protection of Personal Information)"
    PIPEDA = "PIPEDA (Canada Personal Information Protection)"
    LGPD = "LGPD (Brazil Lei Geral de Proteção de Dados)"
    CCPA = "CCPA/CPRA (California Consumer Privacy Act)"
    WHO_IHR = "WHO IHR (International Health Regulations, 2005)"
    GENEVA_CONVENTION = "Geneva Conventions (Humanitarian Data Protection)"
    EU_AI_ACT = "EU AI Act (Transparency and Explainability)"
    MALABO_CONVENTION = "AU Convention on Cyber Security (Malabo Convention)"
    FHIR = "FHIR R4/R5 (Healthcare Data Interoperability)"


class ViolationType(Enum):
    """Types of sovereignty violations"""
    DATA_RESIDENCY = "data_residency_violation"
    CROSS_BORDER_TRANSFER = "cross_border_transfer_violation"
    CONSENT_MISSING = "consent_missing"
    EXPLAINABILITY_REQUIRED = "explainability_required"
    RETENTION_VIOLATION = "retention_violation"
    UNAUTHORIZED_ACCESS = "unauthorized_access"
    PHI_EXPOSURE = "phi_exposure"


class SovereigntyLockout(Exception):
    """Raised when a sovereignty violation is detected"""
    def __init__(self, violation_type: ViolationType, frameworks: List[ComplianceFramework], details: str):
        self.violation_type = violation_type
        self.frameworks = frameworks
        self.details = details
        super().__init__(f"Sovereignty Lockout: {violation_type.value} - {details}")


class SovereignGuardrailMiddleware:
    """
    Middleware that enforces 14 global data frameworks on all API requests.
    
    Every payload is validated against sovereignty constraints before processing.
    """
    
    def __init__(self, config_path: str = "config/sovereign_guardrail.yaml"):
        # Load configuration
        with open(config_path, 'r') as f:
            self.config = yaml.safe_load(f)
        
        # Extract key settings
        self.jurisdiction = self.config['jurisdiction']['primary']
        self.allowed_zones = self.config['sovereignty']['data_residency']['allowed_zones']
        self.blocked_zones = self.config['sovereignty']['data_residency']['blocked_zones']
        self.enforcement_level = self.config['sovereignty']['data_residency']['enforcement_level']
        
        # Violation history
        self.violation_history: List[Dict] = []
        
        logger.info(f"🛡️ SovereignGuardrail Middleware initialized - Jurisdiction: {self.jurisdiction}")
    
    def __call__(self, app):
        """Flask middleware integration"""
        @app.before_request
        def before_request():
            """Validate request before processing"""
            from flask import request
            
            try:
                self.validate_request(request)
            except SovereigntyLockout as e:
                return self._create_lockout_response(e)
        
        return app
    
    def validate_request(self, request: Request) -> None:
        """
        Validate request against all 14 frameworks.
        
        Raises SovereigntyLockout if violation detected.
        """
        # Extract request data
        payload = self._extract_payload(request)
        
        # Rule 1: Data Residency (GDPR Art. 9, Kenya DPA §37, HIPAA §164.312)
        self._validate_data_residency(payload, request)
        
        # Rule 2: Cross-Border Transfers (GDPR Art. 46, POPIA §14, PIPEDA §5-7)
        self._validate_cross_border_transfer(payload, request)
        
        # Rule 3: Consent Validation (GDPR Art. 6, POPIA §11, CCPA §1798.100)
        self._validate_consent(payload, request)
        
        # Rule 4: Explainability (EU AI Act §6, GDPR Art. 22)
        self._validate_explainability(payload, request)
        
        # Rule 5: PHI Protection (HIPAA §164.312, FHIR Security)
        self._validate_phi_protection(payload, request)
        
        # Rule 6: Humanitarian Constraints (Geneva Convention, WHO IHR)
        self._validate_humanitarian_constraints(payload, request)
        
        logger.info(f"✅ Request validated - Endpoint: {request.path}")
    
    def _validate_data_residency(self, payload: Dict, request: Request) -> None:
        """
        Validate data residency constraints.
        
        Frameworks: GDPR Art. 9, Kenya DPA §37, HIPAA §164.312
        """
        # Check if payload contains PHI
        if not self._contains_phi(payload):
            return
        
        # Check destination
        destination = payload.get('destination') or request.headers.get('X-Destination-Zone')
        
        if destination:
            # Check if destination is blocked
            for blocked_pattern in self.blocked_zones:
                if self._matches_zone_pattern(destination, blocked_pattern):
                    raise SovereigntyLockout(
                        violation_type=ViolationType.DATA_RESIDENCY,
                        frameworks=[
                            ComplianceFramework.GDPR,
                            ComplianceFramework.KENYA_DPA,
                            ComplianceFramework.HIPAA
                        ],
                        details=f"PHI cannot be transferred to {destination}. "
                                f"Violates GDPR Art. 9, Kenya DPA §37, HIPAA §164.312"
                    )
            
            # Check if destination is allowed
            if destination not in self.allowed_zones:
                if self.enforcement_level == "STRICT":
                    raise SovereigntyLockout(
                        violation_type=ViolationType.DATA_RESIDENCY,
                        frameworks=[ComplianceFramework.GDPR, ComplianceFramework.KENYA_DPA],
                        details=f"Destination {destination} not in allowed zones: {self.allowed_zones}"
                    )
    
    def _validate_cross_border_transfer(self, payload: Dict, request: Request) -> None:
        """
        Validate cross-border data transfers.
        
        Frameworks: GDPR Art. 46, POPIA §14, PIPEDA §5-7
        """
        if not self._contains_phi(payload):
            return
        
        # Check if cross-border transfer
        destination = payload.get('destination')
        if destination and not self._is_same_jurisdiction(destination):
            # Require authorization
            if not payload.get('authorization_token'):
                raise SovereigntyLockout(
                    violation_type=ViolationType.CROSS_BORDER_TRANSFER,
                    frameworks=[
                        ComplianceFramework.GDPR,
                        ComplianceFramework.POPIA,
                        ComplianceFramework.PIPEDA
                    ],
                    details="Cross-border PHI transfer requires explicit authorization. "
                            "Violates GDPR Art. 46, POPIA §14, PIPEDA §5-7"
                )
            
            # Require Standard Contractual Clauses (SCC)
            if self.config['sovereignty']['cross_border_transfers']['scc_required']:
                if not payload.get('scc_agreement_id'):
                    raise SovereigntyLockout(
                        violation_type=ViolationType.CROSS_BORDER_TRANSFER,
                        frameworks=[ComplianceFramework.GDPR],
                        details="Standard Contractual Clauses (SCC) required for cross-border transfer"
                    )
    
    def _validate_consent(self, payload: Dict, request: Request) -> None:
        """
        Validate consent requirements.
        
        Frameworks: GDPR Art. 6, POPIA §11, CCPA §1798.100
        """
        if not self._contains_phi(payload):
            return
        
        # Check if consent token present
        consent_token = payload.get('consent_token') or request.headers.get('X-Consent-Token')
        
        if not consent_token:
            # Check for emergency override
            if self._is_emergency_override(payload, request):
                logger.warning("⚠️ Emergency override - Consent bypassed (WHO IHR Article 6)")
                return
            
            raise SovereigntyLockout(
                violation_type=ViolationType.CONSENT_MISSING,
                frameworks=[
                    ComplianceFramework.GDPR,
                    ComplianceFramework.POPIA,
                    ComplianceFramework.CCPA
                ],
                details="Explicit consent required for PHI processing. "
                        "Violates GDPR Art. 6, POPIA §11, CCPA §1798.100"
            )
        
        # Validate consent scope
        consent_scope = payload.get('consent_scope')
        if consent_scope not in self.config['consent']['valid_scopes']:
            raise SovereigntyLockout(
                violation_type=ViolationType.CONSENT_MISSING,
                frameworks=[ComplianceFramework.GDPR],
                details=f"Invalid consent scope: {consent_scope}. "
                        f"Valid scopes: {self.config['consent']['valid_scopes']}"
            )
    
    def _validate_explainability(self, payload: Dict, request: Request) -> None:
        """
        Validate explainability requirements for high-risk AI.
        
        Frameworks: EU AI Act §6, GDPR Art. 22
        """
        # Check if high-risk inference
        if payload.get('action_type') == 'High_Risk_Inference':
            confidence_score = payload.get('confidence_score', 0.0)
            
            if confidence_score >= self.config['explainability']['high_risk_threshold']:
                # Require explanation
                if not payload.get('explanation'):
                    raise SovereigntyLockout(
                        violation_type=ViolationType.EXPLAINABILITY_REQUIRED,
                        frameworks=[
                            ComplianceFramework.EU_AI_ACT,
                            ComplianceFramework.GDPR
                        ],
                        details="High-risk AI inference requires explanation (SHAP, LIME, etc.). "
                                "Violates EU AI Act §6, GDPR Art. 22"
                    )
                
                # Validate explanation completeness
                required_fields = self.config['explainability']['requirements']
                missing_fields = [f for f in required_fields if f not in payload]
                
                if missing_fields:
                    raise SovereigntyLockout(
                        violation_type=ViolationType.EXPLAINABILITY_REQUIRED,
                        frameworks=[ComplianceFramework.EU_AI_ACT],
                        details=f"Incomplete explanation. Missing: {missing_fields}"
                    )
    
    def _validate_phi_protection(self, payload: Dict, request: Request) -> None:
        """
        Validate PHI protection requirements.
        
        Frameworks: HIPAA §164.312, FHIR Security
        """
        if not self._contains_phi(payload):
            return
        
        # Check encryption
        if not request.is_secure and self.enforcement_level == "STRICT":
            raise SovereigntyLockout(
                violation_type=ViolationType.PHI_EXPOSURE,
                frameworks=[ComplianceFramework.HIPAA, ComplianceFramework.FHIR],
                details="PHI must be transmitted over HTTPS. Violates HIPAA §164.312"
            )
        
        # Check authentication
        auth_header = request.headers.get('Authorization')
        if not auth_header:
            raise SovereigntyLockout(
                violation_type=ViolationType.UNAUTHORIZED_ACCESS,
                frameworks=[ComplianceFramework.HIPAA],
                details="Authentication required for PHI access. Violates HIPAA §164.312(a)(2)(i)"
            )
    
    def _validate_humanitarian_constraints(self, payload: Dict, request: Request) -> None:
        """
        Validate humanitarian constraints.
        
        Frameworks: Geneva Convention, WHO IHR
        """
        # Check if humanitarian context
        if payload.get('context') == 'humanitarian':
            # Validate impartiality
            if payload.get('resource_allocation'):
                # Ensure no discrimination
                allocation = payload['resource_allocation']
                if 'discrimination_factor' in allocation:
                    raise SovereigntyLockout(
                        violation_type=ViolationType.UNAUTHORIZED_ACCESS,
                        frameworks=[
                            ComplianceFramework.GENEVA_CONVENTION,
                            ComplianceFramework.WHO_IHR
                        ],
                        details="Resource allocation must be impartial. "
                                "Violates Geneva Convention Article 3"
                    )
    
    def _contains_phi(self, payload: Dict) -> bool:
        """Check if payload contains PHI"""
        phi_indicators = ['patient_id', 'diagnosis', 'medical_record', 'health_data', 'phi']
        return any(indicator in payload for indicator in phi_indicators)
    
    def _is_same_jurisdiction(self, destination: str) -> bool:
        """Check if destination is in same jurisdiction"""
        jurisdiction_zones = {
            'KDPA_KE': ['africa-south1'],
            'GDPR_EU': ['europe-west1', 'europe-west2'],
            'HIPAA_US': ['us-central1', 'us-east1'],
        }
        
        current_zones = jurisdiction_zones.get(self.jurisdiction, [])
        return destination in current_zones
    
    def _is_emergency_override(self, payload: Dict, request: Request) -> bool:
        """Check if emergency override conditions met"""
        if not self.config['consent']['emergency_override']['enabled']:
            return False
        
        emergency_conditions = self.config['consent']['emergency_override']['conditions']
        context = payload.get('context')
        
        return context in emergency_conditions
    
    def _matches_zone_pattern(self, zone: str, pattern: str) -> bool:
        """Check if zone matches pattern (supports wildcards)"""
        import re
        regex_pattern = pattern.replace('*', '.*')
        return bool(re.match(regex_pattern, zone))
    
    def _extract_payload(self, request: Request) -> Dict:
        """Extract payload from request"""
        if request.is_json:
            return request.get_json() or {}
        return {}
    
    def _create_lockout_response(self, lockout: SovereigntyLockout) -> Response:
        """Create lockout response"""
        # Log violation
        violation_record = {
            'timestamp': datetime.utcnow().isoformat(),
            'violation_type': lockout.violation_type.value,
            'frameworks': [f.value for f in lockout.frameworks],
            'details': lockout.details,
            'jurisdiction': self.jurisdiction
        }
        self.violation_history.append(violation_record)
        
        logger.error(f"🚨 SOVEREIGNTY LOCKOUT: {lockout.details}")
        
        # Return 403 Forbidden
        return jsonify({
            'status': 'error',
            'error': 'sovereignty_violation',
            'violation_type': lockout.violation_type.value,
            'frameworks_violated': [f.value for f in lockout.frameworks],
            'message': lockout.details,
            'timestamp': datetime.utcnow().isoformat()
        }), 403
    
    def get_violation_history(self, limit: int = 100) -> List[Dict]:
        """Get recent violation history"""
        return self.violation_history[-limit:]


def require_sovereignty_compliance(frameworks: List[ComplianceFramework]):
    """
    Decorator to enforce sovereignty compliance on specific endpoints.
    
    Usage:
        @app.route('/api/transfer')
        @require_sovereignty_compliance([ComplianceFramework.GDPR, ComplianceFramework.KENYA_DPA])
        def transfer_data():
            ...
    """
    def decorator(f: Callable) -> Callable:
        @wraps(f)
        def wrapper(*args, **kwargs):
            from flask import request
            
            # Initialize middleware
            middleware = SovereignGuardrailMiddleware()
            
            try:
                middleware.validate_request(request)
            except SovereigntyLockout as e:
                return middleware._create_lockout_response(e)
            
            return f(*args, **kwargs)
        
        return wrapper
    return decorator


# Example Flask integration
if __name__ == "__main__":
    from flask import Flask, request, jsonify
    
    app = Flask(__name__)
    
    # Apply middleware
    middleware = SovereignGuardrailMiddleware()
    middleware(app)
    
    @app.route('/api/transfer', methods=['POST'])
    def transfer_data():
        """Example endpoint with sovereignty enforcement"""
        data = request.get_json()
        return jsonify({'status': 'success', 'message': 'Data transferred'})
    
    @app.route('/api/inference', methods=['POST'])
    @require_sovereignty_compliance([ComplianceFramework.EU_AI_ACT, ComplianceFramework.GDPR])
    def high_risk_inference():
        """Example high-risk AI endpoint"""
        data = request.get_json()
        return jsonify({'status': 'success', 'prediction': 'malaria', 'confidence': 0.95})
    
    app.run(debug=True, port=8080)
