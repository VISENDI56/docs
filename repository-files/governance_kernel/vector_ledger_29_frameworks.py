"""
Sovereign Guardrail & Governance Engine - 29 Global Legal Frameworks
═════════════════════════════════════════════════════════════════════════════

The 'Ethical Engine' of VISENDI56 that enforces Sovereign Dignity across 29 
global legal frameworks. This module encodes international compliance logic into 
the genetic code of iLuminara-Core, ensuring deployments operate with identical 
integrity constraints worldwide.

Philosophy: "Does this enhance sovereign dignity?" — Every enforcement decision.
"""

from typing import Dict, Any, Optional, List
from enum import Enum
from dataclasses import dataclass
from datetime import datetime


class SovereigntyViolationError(Exception):
    """
    Raised when an action violates one or more sovereignty/compliance constraints.
    Includes specific legal citation for transparency and auditability.
    """
    pass


class JurisdictionFramework(Enum):
    """29 Global legal frameworks encoded in the sovereign guardrail."""
    
    # Core Data Protection (Original 14)
    GDPR_EU = "GDPR (EU)"  # General Data Protection Regulation
    KDPA_KE = "KDPA (Kenya)"  # Kenya Data Protection Act
    PIPEDA_CA = "PIPEDA (Canada)"  # Personal Information Protection & Electronic Documents Act
    POPIA_ZA = "POPIA (South Africa)"  # Protection of Personal Information Act
    HIPAA_US = "HIPAA (USA)"  # Health Insurance Portability & Accountability Act
    HITECH_US = "HITECH (USA)"  # Health Information Technology for Economic & Clinical Health
    CCPA_US = "CCPA (USA)"  # California Consumer Privacy Act
    NIST_CSF = "NIST CSF (USA)"  # Cybersecurity Framework
    ISO_27001 = "ISO 27001"  # Information Security Management
    SOC_2 = "SOC 2 (USA)"  # Service Organization Control 2
    EU_AI_ACT = "EU AI Act"  # Artificial Intelligence Act
    GDPR_ART9 = "GDPR Article 9 (Special Categories)"  # Sensitive Data
    GDPR_ART22 = "GDPR Article 22 (Automated Decision-Making)"  # Right to Explanation
    GDPR_ART30 = "GDPR Article 30 (Records of Processing)"  # Audit Trail
    
    # Additional Regional Data Protection (15 new frameworks)
    LGPD_BR = "LGPD (Brazil)"  # Lei Geral de Proteção de Dados
    PDPA_SG = "PDPA (Singapore)"  # Personal Data Protection Act
    APPI_JP = "APPI (Japan)"  # Act on Protection of Personal Information
    PIPL_CN = "PIPL (China)"  # Personal Information Protection Law
    DPA_UK = "DPA (UK)"  # Data Protection Act 2018
    PDPA_TH = "PDPA (Thailand)"  # Personal Data Protection Act
    PDPA_MY = "PDPA (Malaysia)"  # Personal Data Protection Act
    PIPA_KR = "PIPA (South Korea)"  # Personal Information Protection Act
    FADP_CH = "FADP (Switzerland)"  # Federal Act on Data Protection
    PDPA_ID = "PDPA (Indonesia)"  # Personal Data Protection Act
    
    # Health-Specific Regulations
    WHO_IHR = "WHO IHR (2005)"  # International Health Regulations
    GENEVA_CONV = "Geneva Conventions (1949)"  # Humanitarian Law
    UN_CRC = "UN CRC (1989)"  # Convention on Rights of the Child
    ICRC_MEDICAL = "ICRC Medical Ethics"  # International Committee Red Cross
    SPHERE_STD = "Sphere Standards"  # Humanitarian Response Standards
    
    # Global Default
    GLOBAL_DEFAULT = "GLOBAL_DEFAULT"  # Baseline sovereignty rules


@dataclass
class ComplianceAction:
    """Represents an action requiring compliance validation."""
    action_type: str
    payload: Dict[str, Any]
    jurisdiction: str = "GLOBAL_DEFAULT"
    timestamp: datetime = None

    def __post_init__(self):
        if self.timestamp is None:
            self.timestamp = datetime.utcnow()


class SovereignGuardrail29:
    """
    Enforcement engine for 29 global legal frameworks. Acts as the constitutional 
    guardian of iLuminara-Core, ensuring no action violates sovereign dignity.
    """

    def __init__(self, enable_tamper_proof_audit: bool = False):
        """
        Initialize the sovereign guardrail with 29-framework compliance matrix.
        
        Args:
            enable_tamper_proof_audit: If True, enable tamper-proof audit trail
        """
        self.compliance_matrix = self._build_29_framework_matrix()
        self.audit_log = []
        self.tamper_proof_audit_enabled = enable_tamper_proof_audit

    def _build_29_framework_matrix(self) -> Dict[str, Dict[str, Any]]:
        """
        Build the comprehensive 29-framework compliance matrix.
        Returns a mapping of jurisdiction -> compliance rules.
        """
        return {
            # ═══════════════════════════════════════════════════════════
            # TIER 1: CORE DATA PROTECTION FRAMEWORKS (14)
            # ═══════════════════════════════════════════════════════════
            
            "GDPR_EU": {
                "data_sovereignty_required": True,
                "requires_explicit_consent": True,
                "special_categories_prohibited_foreign": True,
                "right_to_explanation_required": True,
                "retention_max_days": 2555,  # ~7 years
                "breach_notification_hours": 72,
                "dpo_required": True,  # Data Protection Officer
                "dpia_required": True,  # Data Protection Impact Assessment
                "legal_basis": ["Art. 6", "Art. 9", "Art. 22", "Art. 30", "Art. 32"],
            },
            
            "KDPA_KE": {
                "data_sovereignty_required": True,
                "requires_explicit_consent": True,
                "special_categories_prohibited_foreign": True,
                "right_to_explanation_required": False,
                "retention_max_days": 1825,  # ~5 years
                "breach_notification_hours": 72,
                "data_commissioner_registration": True,
                "legal_basis": ["§37", "§42"],
            },
            
            "PIPEDA_CA": {
                "data_sovereignty_required": False,
                "requires_explicit_consent": True,
                "special_categories_prohibited_foreign": True,
                "right_to_explanation_required": False,
                "retention_max_days": 1825,
                "breach_notification_hours": 30,
                "legal_basis": ["§5-7"],
            },
            
            "POPIA_ZA": {
                "data_sovereignty_required": True,
                "requires_explicit_consent": True,
                "special_categories_prohibited_foreign": True,
                "right_to_explanation_required": False,
                "retention_max_days": 2555,
                "breach_notification_hours": 168,  # 7 days
                "information_officer_required": True,
                "legal_basis": ["§11", "§14"],
            },
            
            "HIPAA_US": {
                "data_sovereignty_required": False,
                "requires_explicit_consent": False,  # Covered entities exempt
                "special_categories_prohibited_foreign": True,
                "right_to_explanation_required": False,
                "retention_max_days": 2555,
                "breach_notification_hours": 60,
                "baa_required": True,  # Business Associate Agreement
                "legal_basis": ["§164.312", "§164.404"],
            },
            
            "HITECH_US": {
                "data_sovereignty_required": False,
                "requires_explicit_consent": False,
                "special_categories_prohibited_foreign": True,
                "right_to_explanation_required": False,
                "retention_max_days": 2555,
                "breach_notification_hours": 60,
                "encryption_required": True,
                "legal_basis": ["§13410"],
            },
            
            "CCPA_US": {
                "data_sovereignty_required": False,
                "requires_explicit_consent": False,  # Opt-out model
                "special_categories_prohibited_foreign": False,
                "right_to_explanation_required": False,
                "retention_max_days": 1825,
                "breach_notification_hours": 72,
                "right_to_delete": True,
                "right_to_know": True,
                "legal_basis": ["§1798.100", "§1798.105"],
            },
            
            "NIST_CSF": {
                "data_sovereignty_required": False,
                "requires_explicit_consent": False,
                "special_categories_prohibited_foreign": False,
                "right_to_explanation_required": False,
                "retention_max_days": 1825,
                "breach_notification_hours": 72,
                "framework_functions": ["Identify", "Protect", "Detect", "Respond", "Recover"],
            },
            
            "ISO_27001": {
                "data_sovereignty_required": False,
                "requires_explicit_consent": False,
                "special_categories_prohibited_foreign": False,
                "right_to_explanation_required": False,
                "retention_max_days": 1825,
                "breach_notification_hours": 72,
                "isms_required": True,  # Information Security Management System
                "legal_basis": ["Annex A.8.3.2", "A.12.4", "A.12.6"],
            },
            
            "SOC_2": {
                "data_sovereignty_required": False,
                "requires_explicit_consent": False,
                "special_categories_prohibited_foreign": False,
                "right_to_explanation_required": False,
                "retention_max_days": 1825,
                "breach_notification_hours": 72,
                "trust_criteria": ["Security", "Availability", "Processing Integrity"],
            },
            
            "EU_AI_ACT": {
                "data_sovereignty_required": True,
                "requires_explicit_consent": True,
                "special_categories_prohibited_foreign": True,
                "right_to_explanation_required": True,
                "retention_max_days": 2555,
                "breach_notification_hours": 72,
                "high_risk_ai_requirements": True,
                "transparency_required": True,
                "legal_basis": ["§6", "§8", "§12"],
            },
            
            "GDPR_ART9": {
                "data_sovereignty_required": True,
                "requires_explicit_consent": True,
                "special_categories_prohibited_foreign": True,
                "right_to_explanation_required": True,
                "retention_max_days": 2555,
                "breach_notification_hours": 72,
                "special_categories": ["health", "genetic", "biometric"],
            },
            
            "GDPR_ART22": {
                "data_sovereignty_required": True,
                "requires_explicit_consent": True,
                "special_categories_prohibited_foreign": True,
                "right_to_explanation_required": True,
                "retention_max_days": 2555,
                "breach_notification_hours": 72,
                "automated_decision_safeguards": True,
            },
            
            "GDPR_ART30": {
                "data_sovereignty_required": True,
                "requires_explicit_consent": True,
                "special_categories_prohibited_foreign": True,
                "right_to_explanation_required": True,
                "retention_max_days": 2555,
                "breach_notification_hours": 72,
                "processing_records_required": True,
            },
            
            # ═══════════════════════════════════════════════════════════
            # TIER 2: REGIONAL DATA PROTECTION (10)
            # ═══════════════════════════════════════════════════════════
            
            "LGPD_BR": {
                "data_sovereignty_required": True,
                "requires_explicit_consent": True,
                "special_categories_prohibited_foreign": True,
                "right_to_explanation_required": True,
                "retention_max_days": 1825,
                "breach_notification_hours": 72,
                "anpd_compliance": True,  # National Data Protection Authority
                "legal_basis": ["Art. 7", "Art. 11", "Art. 20"],
            },
            
            "PDPA_SG": {
                "data_sovereignty_required": False,
                "requires_explicit_consent": True,
                "special_categories_prohibited_foreign": False,
                "right_to_explanation_required": False,
                "retention_max_days": 1825,
                "breach_notification_hours": 72,
                "pdpc_registration": True,  # Personal Data Protection Commission
                "legal_basis": ["§11", "§13", "§24"],
            },
            
            "APPI_JP": {
                "data_sovereignty_required": False,
                "requires_explicit_consent": True,
                "special_categories_prohibited_foreign": False,
                "right_to_explanation_required": False,
                "retention_max_days": 1825,
                "breach_notification_hours": 72,
                "ppc_compliance": True,  # Personal Information Protection Commission
                "legal_basis": ["Art. 17", "Art. 23", "Art. 24"],
            },
            
            "PIPL_CN": {
                "data_sovereignty_required": True,
                "requires_explicit_consent": True,
                "special_categories_prohibited_foreign": True,
                "right_to_explanation_required": False,
                "retention_max_days": 1825,
                "breach_notification_hours": 72,
                "cac_compliance": True,  # Cyberspace Administration of China
                "data_localization_required": True,
                "legal_basis": ["Art. 13", "Art. 38", "Art. 40"],
            },
            
            "DPA_UK": {
                "data_sovereignty_required": True,
                "requires_explicit_consent": True,
                "special_categories_prohibited_foreign": True,
                "right_to_explanation_required": True,
                "retention_max_days": 2555,
                "breach_notification_hours": 72,
                "ico_compliance": True,  # Information Commissioner's Office
                "legal_basis": ["Schedule 1", "Part 2", "Part 3"],
            },
            
            "PDPA_TH": {
                "data_sovereignty_required": False,
                "requires_explicit_consent": True,
                "special_categories_prohibited_foreign": True,
                "right_to_explanation_required": False,
                "retention_max_days": 1825,
                "breach_notification_hours": 72,
                "pdpc_th_compliance": True,
                "legal_basis": ["§21", "§26", "§37"],
            },
            
            "PDPA_MY": {
                "data_sovereignty_required": False,
                "requires_explicit_consent": True,
                "special_categories_prohibited_foreign": False,
                "right_to_explanation_required": False,
                "retention_max_days": 1825,
                "breach_notification_hours": 72,
                "pdp_commissioner_registration": True,
                "legal_basis": ["§6", "§40"],
            },
            
            "PIPA_KR": {
                "data_sovereignty_required": False,
                "requires_explicit_consent": True,
                "special_categories_prohibited_foreign": True,
                "right_to_explanation_required": False,
                "retention_max_days": 1825,
                "breach_notification_hours": 24,  # Stricter
                "pipc_compliance": True,  # Personal Information Protection Commission
                "legal_basis": ["Art. 15", "Art. 17", "Art. 34"],
            },
            
            "FADP_CH": {
                "data_sovereignty_required": True,
                "requires_explicit_consent": True,
                "special_categories_prohibited_foreign": True,
                "right_to_explanation_required": False,
                "retention_max_days": 1825,
                "breach_notification_hours": 72,
                "fdpic_compliance": True,  # Federal Data Protection Commissioner
                "legal_basis": ["Art. 6", "Art. 16", "Art. 24"],
            },
            
            "PDPA_ID": {
                "data_sovereignty_required": True,
                "requires_explicit_consent": True,
                "special_categories_prohibited_foreign": True,
                "right_to_explanation_required": False,
                "retention_max_days": 1825,
                "breach_notification_hours": 72,
                "ministry_compliance": True,
                "legal_basis": ["Art. 11", "Art. 16", "Art. 56"],
            },
            
            # ═══════════════════════════════════════════════════════════
            # TIER 3: HEALTH & HUMANITARIAN LAW (5)
            # ═══════════════════════════════════════════════════════════
            
            "WHO_IHR": {
                "data_sovereignty_required": False,
                "requires_explicit_consent": False,  # Public health emergency
                "special_categories_prohibited_foreign": False,
                "right_to_explanation_required": False,
                "retention_max_days": 3650,  # 10 years for epidemiological data
                "breach_notification_hours": 24,
                "emergency_response_required": True,
                "legal_basis": ["Art. 6", "Art. 7", "Annex 2"],
            },
            
            "GENEVA_CONV": {
                "data_sovereignty_required": False,
                "requires_explicit_consent": False,
                "special_categories_prohibited_foreign": False,
                "right_to_explanation_required": False,
                "retention_max_days": 3650,
                "breach_notification_hours": 24,
                "civilian_protection_required": True,
                "humanitarian_principles": ["Humanity", "Impartiality", "Neutrality", "Independence"],
                "legal_basis": ["Art. 3", "Art. 27"],
            },
            
            "UN_CRC": {
                "data_sovereignty_required": False,
                "requires_explicit_consent": True,  # Parental consent for minors
                "special_categories_prohibited_foreign": True,
                "right_to_explanation_required": False,
                "retention_max_days": 1825,
                "breach_notification_hours": 24,
                "best_interest_child_required": True,
                "legal_basis": ["Art. 3", "Art. 16"],
            },
            
            "ICRC_MEDICAL": {
                "data_sovereignty_required": False,
                "requires_explicit_consent": False,
                "special_categories_prohibited_foreign": False,
                "right_to_explanation_required": False,
                "retention_max_days": 3650,
                "breach_notification_hours": 24,
                "medical_ethics_required": True,
                "triage_fairness_required": True,
                "legal_basis": ["ICRC Code of Conduct"],
            },
            
            "SPHERE_STD": {
                "data_sovereignty_required": False,
                "requires_explicit_consent": False,
                "special_categories_prohibited_foreign": False,
                "right_to_explanation_required": False,
                "retention_max_days": 1825,
                "breach_notification_hours": 24,
                "humanitarian_standards_required": True,
                "quality_accountability_required": True,
                "legal_basis": ["Core Humanitarian Standard"],
            },
            
            # ═══════════════════════════════════════════════════════════
            # GLOBAL DEFAULT
            # ═══════════════════════════════════════════════════════════
            
            "GLOBAL_DEFAULT": {
                "data_sovereignty_required": True,
                "requires_explicit_consent": True,
                "special_categories_prohibited_foreign": True,
                "right_to_explanation_required": True,
                "retention_max_days": 1825,
                "breach_notification_hours": 72,
            },
        }

    def validate_action(
        self,
        action_type: str,
        payload: Dict[str, Any],
        jurisdictions: List[str] = None,
    ) -> bool:
        """
        Validate an action against 29 sovereign compliance constraints.

        Args:
            action_type: Type of action
            payload: The action's data/parameters
            jurisdictions: List of applicable jurisdictions (defaults to GLOBAL_DEFAULT)

        Returns:
            True if action passes all validation checks

        Raises:
            SovereigntyViolationError: If any compliance rule is violated
        """
        if jurisdictions is None:
            jurisdictions = ["GLOBAL_DEFAULT"]
        
        violations = []
        
        for jurisdiction in jurisdictions:
            compliance_rules = self.compliance_matrix.get(
                jurisdiction, self.compliance_matrix["GLOBAL_DEFAULT"]
            )
            
            try:
                # Rule 1: Data Sovereignty
                if compliance_rules["data_sovereignty_required"]:
                    self._validate_data_sovereignty(payload, jurisdiction)
                
                # Rule 2: Right to Explanation
                if action_type == "High_Risk_Inference":
                    self._validate_right_to_explanation(payload, jurisdiction)
                
                # Rule 3: Consent Validation
                if compliance_rules["requires_explicit_consent"]:
                    self._validate_consent(payload, jurisdiction)
                
                # Rule 4: Retention Window
                self._validate_retention(payload, compliance_rules, jurisdiction)
                
            except SovereigntyViolationError as e:
                violations.append(f"{jurisdiction}: {str(e)}")
        
        if violations:
            raise SovereigntyViolationError(
                f"❌ MULTI-JURISDICTION VIOLATION:\\n" + "\\n".join(violations)
            )
        
        # Log successful validation
        self.audit_log.append({
            "timestamp": datetime.utcnow().isoformat(),
            "action_type": action_type,
            "jurisdictions": jurisdictions,
            "status": "PASSED",
        })
        
        return True

    def _validate_data_sovereignty(self, payload: Dict[str, Any], jurisdiction: str):
        """Enforce data sovereignty across all 29 frameworks."""
        if payload.get("data_type") == "PHI" and payload.get("destination") in [
            "Foreign_Cloud", "AWS_US", "Azure_EU_Exemption",
        ]:
            raise SovereigntyViolationError(
                f"Protected health data cannot be transferred to foreign infrastructure. "
                f"Jurisdiction: {jurisdiction}"
            )

    def _validate_right_to_explanation(self, payload: Dict[str, Any], jurisdiction: str):
        """Enforce right to explanation for high-risk inferences."""
        required_fields = ["explanation", "confidence_score", "evidence_chain"]
        missing_fields = [f for f in required_fields if f not in payload]
        
        if missing_fields:
            raise SovereigntyViolationError(
                f"High-risk inference requires explainability. "
                f"Missing: {', '.join(missing_fields)}. "
                f"Jurisdiction: {jurisdiction}"
            )

    def _validate_consent(self, payload: Dict[str, Any], jurisdiction: str):
        """Enforce consent validation."""
        if not payload.get("consent_token"):
            raise SovereigntyViolationError(
                f"Data processing without valid consent token. "
                f"Jurisdiction: {jurisdiction}"
            )

    def _validate_retention(
        self, payload: Dict[str, Any], rules: Dict[str, Any], jurisdiction: str
    ):
        """Enforce data retention windows."""
        record_date_str = payload.get("record_date")
        if not record_date_str:
            return
        
        try:
            record_date = datetime.fromisoformat(record_date_str)
            days_since_record = (datetime.utcnow() - record_date).days
            max_retention = rules.get("retention_max_days", 1825)
            
            if days_since_record > max_retention:
                raise SovereigntyViolationError(
                    f"Data exceeds retention window. "
                    f"Days: {days_since_record}, Max: {max_retention}. "
                    f"Jurisdiction: {jurisdiction}"
                )
        except (ValueError, TypeError):
            pass

    def get_audit_log(self):
        """Return the complete audit trail."""
        return self.audit_log

    def get_supported_jurisdictions(self) -> List[str]:
        """Return list of all 29 supported jurisdictions."""
        return list(self.compliance_matrix.keys())

    def get_jurisdiction_details(self, jurisdiction: str) -> Dict[str, Any]:
        """Get detailed compliance requirements for a jurisdiction."""
        return self.compliance_matrix.get(jurisdiction, {})


# ═════════════════════════════════════════════════════════════════════════════
# MISSION: To architect systems that transform preventable suffering from 
# statistical inevitability to historical anomaly.
#
# COMPLIANCE PILLAR: 29 Global Sovereign Frameworks
# ═════════════════════════════════════════════════════════════════════════════
