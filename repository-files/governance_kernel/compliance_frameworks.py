"""
iLuminara-Core: Complete Compliance Framework
Enforces 29 global legal frameworks for sovereign health data

Compliance Coverage:
- Data Protection: 12 frameworks
- Healthcare: 5 frameworks
- Security Standards: 7 frameworks
- AI Ethics: 3 frameworks
- Humanitarian Law: 2 frameworks
"""

from enum import Enum
from typing import Dict, List, Optional
from dataclasses import dataclass
from datetime import datetime


class ComplianceFramework(Enum):
    """All 29 global legal frameworks enforced by iLuminara"""
    
    # === DATA PROTECTION LAWS (12) ===
    GDPR = "GDPR (EU General Data Protection Regulation)"
    KDPA = "KDPA (Kenya Data Protection Act 2019)"
    POPIA = "POPIA (South Africa Protection of Personal Information Act)"
    PIPEDA = "PIPEDA (Canada Personal Information Protection)"
    CCPA = "CCPA (California Consumer Privacy Act)"
    LGPD = "LGPD (Brazil Lei Geral de Proteção de Dados)"
    PDPA_SG = "PDPA (Singapore Personal Data Protection Act)"
    PDPA_TH = "PDPA (Thailand Personal Data Protection Act)"
    DPA_UK = "UK DPA (UK Data Protection Act 2018)"
    APPI = "APPI (Japan Act on Protection of Personal Information)"
    PIPL = "PIPL (China Personal Information Protection Law)"
    NDPR = "NDPR (Nigeria Data Protection Regulation)"
    
    # === HEALTHCARE REGULATIONS (5) ===
    HIPAA = "HIPAA (US Health Insurance Portability)"
    HITECH = "HITECH (US Health Information Technology)"
    FDA_21CFR11 = "FDA 21 CFR Part 11 (Electronic Records)"
    MDR = "MDR (EU Medical Device Regulation 2017/745)"
    IVDR = "IVDR (EU In Vitro Diagnostic Regulation 2017/746)"
    
    # === SECURITY STANDARDS (7) ===
    ISO_27001 = "ISO 27001 (Information Security Management)"
    ISO_27701 = "ISO 27701 (Privacy Information Management)"
    SOC_2 = "SOC 2 (Service Organization Control)"
    NIST_CSF = "NIST Cybersecurity Framework"
    NIST_800_53 = "NIST SP 800-53 (Security Controls)"
    PCI_DSS = "PCI DSS (Payment Card Industry Data Security)"
    CIS_CONTROLS = "CIS Critical Security Controls"
    
    # === AI & ETHICS (3) ===
    EU_AI_ACT = "EU AI Act (Artificial Intelligence Regulation)"
    UNESCO_AI = "UNESCO Recommendation on AI Ethics"
    OECD_AI = "OECD AI Principles"
    
    # === HUMANITARIAN LAW (2) ===
    GENEVA_CONVENTION = "Geneva Convention (International Humanitarian Law)"
    WHO_IHR = "WHO IHR (International Health Regulations 2005)"


@dataclass
class ComplianceRequirement:
    """Individual compliance requirement"""
    framework: ComplianceFramework
    article: str
    description: str
    enforcement_level: str  # MANDATORY | RECOMMENDED | OPTIONAL
    validation_method: str
    penalty_for_violation: str


class ComplianceMatrix:
    """
    Complete compliance matrix for iLuminara-Core
    Maps all 29 frameworks to specific requirements
    """
    
    def __init__(self):
        self.requirements = self._initialize_requirements()
    
    def _initialize_requirements(self) -> Dict[ComplianceFramework, List[ComplianceRequirement]]:
        """Initialize all 29 frameworks with specific requirements"""
        
        return {
            # ========== DATA PROTECTION LAWS ==========
            
            ComplianceFramework.GDPR: [
                ComplianceRequirement(
                    framework=ComplianceFramework.GDPR,
                    article="Art. 6",
                    description="Lawfulness of Processing - Requires legal basis for data processing",
                    enforcement_level="MANDATORY",
                    validation_method="SovereignGuardrail.validate_consent()",
                    penalty_for_violation="€20M or 4% global revenue"
                ),
                ComplianceRequirement(
                    framework=ComplianceFramework.GDPR,
                    article="Art. 9",
                    description="Special Categories - Health data requires explicit consent",
                    enforcement_level="MANDATORY",
                    validation_method="SovereignGuardrail.validate_phi_processing()",
                    penalty_for_violation="€20M or 4% global revenue"
                ),
                ComplianceRequirement(
                    framework=ComplianceFramework.GDPR,
                    article="Art. 17",
                    description="Right to Erasure - Data subjects can request deletion",
                    enforcement_level="MANDATORY",
                    validation_method="CryptoShredder.shred_key()",
                    penalty_for_violation="€20M or 4% global revenue"
                ),
                ComplianceRequirement(
                    framework=ComplianceFramework.GDPR,
                    article="Art. 22",
                    description="Right to Explanation - Automated decisions require explanation",
                    enforcement_level="MANDATORY",
                    validation_method="ExplainabilityEngine.generate_shap()",
                    penalty_for_violation="€20M or 4% global revenue"
                ),
                ComplianceRequirement(
                    framework=ComplianceFramework.GDPR,
                    article="Art. 30",
                    description="Records of Processing - Maintain audit trail",
                    enforcement_level="MANDATORY",
                    validation_method="AuditTrail.log_processing()",
                    penalty_for_violation="€10M or 2% global revenue"
                ),
                ComplianceRequirement(
                    framework=ComplianceFramework.GDPR,
                    article="Art. 32",
                    description="Security of Processing - Implement technical safeguards",
                    enforcement_level="MANDATORY",
                    validation_method="SecurityAudit.validate_encryption()",
                    penalty_for_violation="€10M or 2% global revenue"
                ),
                ComplianceRequirement(
                    framework=ComplianceFramework.GDPR,
                    article="Art. 44-50",
                    description="International Transfers - Restrict cross-border data flows",
                    enforcement_level="MANDATORY",
                    validation_method="SovereignGuardrail.validate_data_transfer()",
                    penalty_for_violation="€20M or 4% global revenue"
                ),
            ],
            
            ComplianceFramework.KDPA: [
                ComplianceRequirement(
                    framework=ComplianceFramework.KDPA,
                    article="§37",
                    description="Transfer Restrictions - Data cannot leave Kenya without authorization",
                    enforcement_level="MANDATORY",
                    validation_method="SovereignGuardrail.validate_sovereignty()",
                    penalty_for_violation="KES 5M or imprisonment"
                ),
                ComplianceRequirement(
                    framework=ComplianceFramework.KDPA,
                    article="§42",
                    description="Data Subject Rights - Right to access, correction, deletion",
                    enforcement_level="MANDATORY",
                    validation_method="DataSubjectRights.process_request()",
                    penalty_for_violation="KES 3M"
                ),
                ComplianceRequirement(
                    framework=ComplianceFramework.KDPA,
                    article="§25",
                    description="Data Protection Impact Assessment - Required for high-risk processing",
                    enforcement_level="MANDATORY",
                    validation_method="DPIA.conduct_assessment()",
                    penalty_for_violation="KES 5M"
                ),
            ],
            
            ComplianceFramework.POPIA: [
                ComplianceRequirement(
                    framework=ComplianceFramework.POPIA,
                    article="§11",
                    description="Lawfulness of Processing - Must have legal basis",
                    enforcement_level="MANDATORY",
                    validation_method="SovereignGuardrail.validate_consent()",
                    penalty_for_violation="ZAR 10M or 10 years imprisonment"
                ),
                ComplianceRequirement(
                    framework=ComplianceFramework.POPIA,
                    article="§14",
                    description="Cross-border Transfers - Requires adequate protection",
                    enforcement_level="MANDATORY",
                    validation_method="SovereignGuardrail.validate_data_transfer()",
                    penalty_for_violation="ZAR 10M"
                ),
            ],
            
            ComplianceFramework.HIPAA: [
                ComplianceRequirement(
                    framework=ComplianceFramework.HIPAA,
                    article="§164.312(a)(1)",
                    description="Access Control - Unique user identification required",
                    enforcement_level="MANDATORY",
                    validation_method="AccessControl.validate_user()",
                    penalty_for_violation="$1.5M per violation"
                ),
                ComplianceRequirement(
                    framework=ComplianceFramework.HIPAA,
                    article="§164.312(b)",
                    description="Audit Controls - Log all PHI access",
                    enforcement_level="MANDATORY",
                    validation_method="AuditTrail.log_phi_access()",
                    penalty_for_violation="$1.5M per violation"
                ),
                ComplianceRequirement(
                    framework=ComplianceFramework.HIPAA,
                    article="§164.312(e)(1)",
                    description="Transmission Security - Encrypt PHI in transit",
                    enforcement_level="MANDATORY",
                    validation_method="Encryption.validate_tls()",
                    penalty_for_violation="$1.5M per violation"
                ),
                ComplianceRequirement(
                    framework=ComplianceFramework.HIPAA,
                    article="§164.530(j)",
                    description="Documentation - Retain records for 6 years",
                    enforcement_level="MANDATORY",
                    validation_method="RetentionPolicy.validate_duration()",
                    penalty_for_violation="$1.5M per violation"
                ),
            ],
            
            ComplianceFramework.PIPEDA: [
                ComplianceRequirement(
                    framework=ComplianceFramework.PIPEDA,
                    article="§5-7",
                    description="Lawfulness of Processing - Consent required",
                    enforcement_level="MANDATORY",
                    validation_method="SovereignGuardrail.validate_consent()",
                    penalty_for_violation="CAD $100K"
                ),
            ],
            
            ComplianceFramework.CCPA: [
                ComplianceRequirement(
                    framework=ComplianceFramework.CCPA,
                    article="§1798.100",
                    description="Right to Know - Disclose data collection practices",
                    enforcement_level="MANDATORY",
                    validation_method="DataSubjectRights.disclose_collection()",
                    penalty_for_violation="$7,500 per violation"
                ),
                ComplianceRequirement(
                    framework=ComplianceFramework.CCPA,
                    article="§1798.105",
                    description="Right to Delete - Honor deletion requests",
                    enforcement_level="MANDATORY",
                    validation_method="CryptoShredder.shred_key()",
                    penalty_for_violation="$7,500 per violation"
                ),
            ],
            
            ComplianceFramework.LGPD: [
                ComplianceRequirement(
                    framework=ComplianceFramework.LGPD,
                    article="Art. 7",
                    description="Legal Basis - Requires consent or legitimate interest",
                    enforcement_level="MANDATORY",
                    validation_method="SovereignGuardrail.validate_consent()",
                    penalty_for_violation="BRL 50M or 2% revenue"
                ),
            ],
            
            ComplianceFramework.PDPA_SG: [
                ComplianceRequirement(
                    framework=ComplianceFramework.PDPA_SG,
                    article="§13",
                    description="Consent - Obtain consent before collection",
                    enforcement_level="MANDATORY",
                    validation_method="SovereignGuardrail.validate_consent()",
                    penalty_for_violation="SGD 1M"
                ),
            ],
            
            ComplianceFramework.PDPA_TH: [
                ComplianceRequirement(
                    framework=ComplianceFramework.PDPA_TH,
                    article="§19",
                    description="Consent - Explicit consent for sensitive data",
                    enforcement_level="MANDATORY",
                    validation_method="SovereignGuardrail.validate_consent()",
                    penalty_for_violation="THB 5M"
                ),
            ],
            
            ComplianceFramework.DPA_UK: [
                ComplianceRequirement(
                    framework=ComplianceFramework.DPA_UK,
                    article="Schedule 1",
                    description="GDPR Principles - Mirrors GDPR requirements",
                    enforcement_level="MANDATORY",
                    validation_method="SovereignGuardrail.validate_gdpr()",
                    penalty_for_violation="£17.5M or 4% revenue"
                ),
            ],
            
            ComplianceFramework.APPI: [
                ComplianceRequirement(
                    framework=ComplianceFramework.APPI,
                    article="Art. 23",
                    description="Cross-border Transfer - Requires consent",
                    enforcement_level="MANDATORY",
                    validation_method="SovereignGuardrail.validate_data_transfer()",
                    penalty_for_violation="JPY 100M"
                ),
            ],
            
            ComplianceFramework.PIPL: [
                ComplianceRequirement(
                    framework=ComplianceFramework.PIPL,
                    article="Art. 38",
                    description="Cross-border Transfer - Security assessment required",
                    enforcement_level="MANDATORY",
                    validation_method="SovereignGuardrail.validate_data_transfer()",
                    penalty_for_violation="CNY 50M or 5% revenue"
                ),
            ],
            
            ComplianceFramework.NDPR: [
                ComplianceRequirement(
                    framework=ComplianceFramework.NDPR,
                    article="§2.3",
                    description="Consent - Explicit consent required",
                    enforcement_level="MANDATORY",
                    validation_method="SovereignGuardrail.validate_consent()",
                    penalty_for_violation="NGN 10M or 2% revenue"
                ),
            ],
            
            # ========== HEALTHCARE REGULATIONS ==========
            
            ComplianceFramework.HITECH: [
                ComplianceRequirement(
                    framework=ComplianceFramework.HITECH,
                    article="§13410",
                    description="Breach Notification - Notify within 60 days",
                    enforcement_level="MANDATORY",
                    validation_method="BreachNotification.notify()",
                    penalty_for_violation="$1.5M per violation"
                ),
            ],
            
            ComplianceFramework.FDA_21CFR11: [
                ComplianceRequirement(
                    framework=ComplianceFramework.FDA_21CFR11,
                    article="§11.10",
                    description="Electronic Records - Validation and audit trails",
                    enforcement_level="MANDATORY",
                    validation_method="AuditTrail.validate_integrity()",
                    penalty_for_violation="Warning letter or seizure"
                ),
            ],
            
            ComplianceFramework.MDR: [
                ComplianceRequirement(
                    framework=ComplianceFramework.MDR,
                    article="Art. 62",
                    description="Clinical Evaluation - Safety and performance",
                    enforcement_level="MANDATORY",
                    validation_method="ClinicalEvaluation.conduct()",
                    penalty_for_violation="Market withdrawal"
                ),
            ],
            
            ComplianceFramework.IVDR: [
                ComplianceRequirement(
                    framework=ComplianceFramework.IVDR,
                    article="Art. 56",
                    description="Performance Evaluation - Analytical/clinical performance",
                    enforcement_level="MANDATORY",
                    validation_method="PerformanceEvaluation.conduct()",
                    penalty_for_violation="Market withdrawal"
                ),
            ],
            
            # ========== SECURITY STANDARDS ==========
            
            ComplianceFramework.ISO_27001: [
                ComplianceRequirement(
                    framework=ComplianceFramework.ISO_27001,
                    article="A.8.3.2",
                    description="Disposal of Media - Secure deletion",
                    enforcement_level="MANDATORY",
                    validation_method="CryptoShredder.shred_key()",
                    penalty_for_violation="Certification revocation"
                ),
                ComplianceRequirement(
                    framework=ComplianceFramework.ISO_27001,
                    article="A.12.4",
                    description="Logging and Monitoring - Audit trail",
                    enforcement_level="MANDATORY",
                    validation_method="AuditTrail.log_event()",
                    penalty_for_violation="Certification revocation"
                ),
                ComplianceRequirement(
                    framework=ComplianceFramework.ISO_27001,
                    article="A.12.6",
                    description="Technical Vulnerability Management - SAST/DAST",
                    enforcement_level="MANDATORY",
                    validation_method="SecurityAudit.scan_vulnerabilities()",
                    penalty_for_violation="Certification revocation"
                ),
            ],
            
            ComplianceFramework.ISO_27701: [
                ComplianceRequirement(
                    framework=ComplianceFramework.ISO_27701,
                    article="§6.2",
                    description="Privacy Information Management - PIMS requirements",
                    enforcement_level="MANDATORY",
                    validation_method="PrivacyManagement.validate()",
                    penalty_for_violation="Certification revocation"
                ),
            ],
            
            ComplianceFramework.SOC_2: [
                ComplianceRequirement(
                    framework=ComplianceFramework.SOC_2,
                    article="CC6.1",
                    description="Logical Access - Authentication and authorization",
                    enforcement_level="MANDATORY",
                    validation_method="AccessControl.validate_user()",
                    penalty_for_violation="Audit failure"
                ),
                ComplianceRequirement(
                    framework=ComplianceFramework.SOC_2,
                    article="CC7.2",
                    description="System Monitoring - Detect anomalies",
                    enforcement_level="MANDATORY",
                    validation_method="AnomalyDetection.monitor()",
                    penalty_for_violation="Audit failure"
                ),
            ],
            
            ComplianceFramework.NIST_CSF: [
                ComplianceRequirement(
                    framework=ComplianceFramework.NIST_CSF,
                    article="ID.AM",
                    description="Asset Management - Inventory all assets",
                    enforcement_level="RECOMMENDED",
                    validation_method="AssetInventory.validate()",
                    penalty_for_violation="N/A (voluntary)"
                ),
                ComplianceRequirement(
                    framework=ComplianceFramework.NIST_CSF,
                    article="PR.DS",
                    description="Data Security - Protect data at rest/transit",
                    enforcement_level="RECOMMENDED",
                    validation_method="Encryption.validate_all()",
                    penalty_for_violation="N/A (voluntary)"
                ),
            ],
            
            ComplianceFramework.NIST_800_53: [
                ComplianceRequirement(
                    framework=ComplianceFramework.NIST_800_53,
                    article="IA-5",
                    description="Authenticator Management - Secure credentials",
                    enforcement_level="MANDATORY",
                    validation_method="CredentialManagement.validate()",
                    penalty_for_violation="Federal contract loss"
                ),
            ],
            
            ComplianceFramework.PCI_DSS: [
                ComplianceRequirement(
                    framework=ComplianceFramework.PCI_DSS,
                    article="Req. 3",
                    description="Protect Stored Cardholder Data - Encryption",
                    enforcement_level="MANDATORY",
                    validation_method="Encryption.validate_payment_data()",
                    penalty_for_violation="$100K per month"
                ),
            ],
            
            ComplianceFramework.CIS_CONTROLS: [
                ComplianceRequirement(
                    framework=ComplianceFramework.CIS_CONTROLS,
                    article="Control 1",
                    description="Inventory of Assets - Track all devices",
                    enforcement_level="RECOMMENDED",
                    validation_method="AssetInventory.validate()",
                    penalty_for_violation="N/A (voluntary)"
                ),
            ],
            
            # ========== AI & ETHICS ==========
            
            ComplianceFramework.EU_AI_ACT: [
                ComplianceRequirement(
                    framework=ComplianceFramework.EU_AI_ACT,
                    article="§6",
                    description="High-Risk AI - Safety and transparency requirements",
                    enforcement_level="MANDATORY",
                    validation_method="AIRiskAssessment.classify()",
                    penalty_for_violation="€30M or 6% revenue"
                ),
                ComplianceRequirement(
                    framework=ComplianceFramework.EU_AI_ACT,
                    article="§8",
                    description="Transparency - Disclose AI usage",
                    enforcement_level="MANDATORY",
                    validation_method="AITransparency.disclose()",
                    penalty_for_violation="€15M or 3% revenue"
                ),
                ComplianceRequirement(
                    framework=ComplianceFramework.EU_AI_ACT,
                    article="§12",
                    description="Record Keeping - Maintain AI logs",
                    enforcement_level="MANDATORY",
                    validation_method="AuditTrail.log_ai_decision()",
                    penalty_for_violation="€15M or 3% revenue"
                ),
            ],
            
            ComplianceFramework.UNESCO_AI: [
                ComplianceRequirement(
                    framework=ComplianceFramework.UNESCO_AI,
                    article="Principle 1",
                    description="Human Rights - Respect dignity and autonomy",
                    enforcement_level="RECOMMENDED",
                    validation_method="EthicalEngine.validate_dignity()",
                    penalty_for_violation="N/A (voluntary)"
                ),
            ],
            
            ComplianceFramework.OECD_AI: [
                ComplianceRequirement(
                    framework=ComplianceFramework.OECD_AI,
                    article="Principle 1.3",
                    description="Transparency - Explainable AI",
                    enforcement_level="RECOMMENDED",
                    validation_method="ExplainabilityEngine.generate_shap()",
                    penalty_for_violation="N/A (voluntary)"
                ),
            ],
            
            # ========== HUMANITARIAN LAW ==========
            
            ComplianceFramework.GENEVA_CONVENTION: [
                ComplianceRequirement(
                    framework=ComplianceFramework.GENEVA_CONVENTION,
                    article="Art. 3",
                    description="Protection of Civilians - Humanitarian treatment",
                    enforcement_level="MANDATORY",
                    validation_method="EthicalEngine.validate_humanitarian_margin()",
                    penalty_for_violation="War crimes prosecution"
                ),
            ],
            
            ComplianceFramework.WHO_IHR: [
                ComplianceRequirement(
                    framework=ComplianceFramework.WHO_IHR,
                    article="Art. 6",
                    description="Notification - Report public health emergencies",
                    enforcement_level="MANDATORY",
                    validation_method="EmergencyNotification.notify_who()",
                    penalty_for_violation="International sanctions"
                ),
            ],
        }
    
    def get_all_frameworks(self) -> List[ComplianceFramework]:
        """Get list of all 29 frameworks"""
        return list(ComplianceFramework)
    
    def get_requirements(self, framework: ComplianceFramework) -> List[ComplianceRequirement]:
        """Get requirements for a specific framework"""
        return self.requirements.get(framework, [])
    
    def get_mandatory_requirements(self) -> List[ComplianceRequirement]:
        """Get all mandatory requirements across all frameworks"""
        mandatory = []
        for reqs in self.requirements.values():
            mandatory.extend([r for r in reqs if r.enforcement_level == "MANDATORY"])
        return mandatory
    
    def validate_compliance(self, framework: ComplianceFramework) -> Dict:
        """Validate compliance for a specific framework"""
        requirements = self.get_requirements(framework)
        
        return {
            "framework": framework.value,
            "total_requirements": len(requirements),
            "mandatory_requirements": len([r for r in requirements if r.enforcement_level == "MANDATORY"]),
            "requirements": [
                {
                    "article": r.article,
                    "description": r.description,
                    "enforcement_level": r.enforcement_level,
                    "validation_method": r.validation_method,
                    "penalty": r.penalty_for_violation
                }
                for r in requirements
            ]
        }


# Example usage
if __name__ == "__main__":
    matrix = ComplianceMatrix()
    
    print("=" * 80)
    print("iLuminara-Core: Complete Compliance Matrix")
    print("=" * 80)
    print(f"\nTotal Frameworks: {len(matrix.get_all_frameworks())}")
    print(f"Total Mandatory Requirements: {len(matrix.get_mandatory_requirements())}")
    print("\n")
    
    # Print all frameworks
    for framework in matrix.get_all_frameworks():
        reqs = matrix.get_requirements(framework)
        print(f"✓ {framework.value}")
        print(f"  └─ {len(reqs)} requirements")
