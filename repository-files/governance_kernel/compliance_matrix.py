"""
ComplianceMatrix: Unified Regulatory Mapping for 14 Global Data Laws

This module encodes the cross-referencing logic for 14 specific data protection
and health information frameworks, enabling law-as-code enforcement.

The 14 Laws:
1. GDPR (EU General Data Protection Regulation)
2. HIPAA (USA Health Insurance Portability and Accountability Act)
3. Kenya DPA (Kenya Data Protection Act, 2019)
4. POPIA (South Africa Protection of Personal Information Act)
5. NDPR (Nigeria Data Protection Regulation)
6. APPI (Japan Act on Protection of Personal Information)
7. PIPEDA (Canada Personal Information Protection and Electronic Documents Act)
8. LGPD (Brazil Lei Geral de Proteção de Dados)
9. CCPA (California Consumer Privacy Act)
10. WHO IHR (World Health Organization International Health Regulations, 2005)
11. Geneva Conventions (Data Protection in Armed Conflict)
12. EU AI Act (European Union Artificial Intelligence Act)
13. AU Malabo Convention (African Union Convention on Cyber Security)
14. FHIR R4/R5 (Fast Healthcare Interoperability Resources Standards)
"""

from enum import Enum
from typing import Dict, List, Optional, Set
from dataclasses import dataclass
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


class DataLaw(Enum):
    """The 14 global data protection and health information frameworks"""
    GDPR = "GDPR"
    HIPAA = "HIPAA"
    KENYA_DPA = "Kenya_DPA"
    POPIA = "POPIA"
    NDPR = "NDPR"
    APPI = "APPI"
    PIPEDA = "PIPEDA"
    LGPD = "LGPD"
    CCPA = "CCPA"
    WHO_IHR = "WHO_IHR"
    GENEVA_CONVENTIONS = "Geneva_Conventions"
    EU_AI_ACT = "EU_AI_ACT"
    AU_MALABO = "AU_Malabo"
    FHIR_R4_R5 = "FHIR_R4_R5"


class DataHandlingOperation(Enum):
    """Types of data handling operations"""
    COLLECTION = "collection"
    PROCESSING = "processing"
    STORAGE = "storage"
    TRANSFER = "transfer"
    DELETION = "deletion"
    ANONYMIZATION = "anonymization"
    CONSENT_MANAGEMENT = "consent_management"
    ACCESS_CONTROL = "access_control"
    ENCRYPTION = "encryption"
    AUDIT_LOGGING = "audit_logging"
    AI_INFERENCE = "ai_inference"
    CROSS_BORDER_TRANSFER = "cross_border_transfer"


class ComplianceRequirement(Enum):
    """Compliance requirement types"""
    MANDATORY = "mandatory"
    RECOMMENDED = "recommended"
    CONDITIONAL = "conditional"
    PROHIBITED = "prohibited"


@dataclass
class LegalArticle:
    """Represents a specific legal article or section"""
    law: DataLaw
    article: str
    description: str
    requirement: ComplianceRequirement
    penalty_severity: str  # LOW, MEDIUM, HIGH, CRITICAL
    
    def __str__(self):
        return f"{self.law.value} {self.article}: {self.description}"


@dataclass
class ComplianceRule:
    """A compliance rule mapping operations to legal requirements"""
    operation: DataHandlingOperation
    applicable_laws: List[LegalArticle]
    enforcement_logic: str
    humanitarian_override: bool = False
    
    def check_compliance(self, context: Dict) -> bool:
        """Check if operation complies with all applicable laws"""
        # This would contain the actual enforcement logic
        return True


class ComplianceMatrix:
    """
    The Unified Regulatory Mapping Engine
    
    Maps data handling operations to the 14 global legal frameworks,
    enabling real-time law-as-code enforcement.
    """
    
    def __init__(self):
        self.rules: Dict[DataHandlingOperation, ComplianceRule] = {}
        self._initialize_matrix()
        logger.info("⚖️ ComplianceMatrix initialized - 14 laws encoded")
    
    def _initialize_matrix(self):
        """Initialize the complete compliance matrix"""
        
        # COLLECTION
        self.rules[DataHandlingOperation.COLLECTION] = ComplianceRule(
            operation=DataHandlingOperation.COLLECTION,
            applicable_laws=[
                LegalArticle(
                    law=DataLaw.GDPR,
                    article="Art. 6",
                    description="Lawfulness of processing - requires legal basis",
                    requirement=ComplianceRequirement.MANDATORY,
                    penalty_severity="CRITICAL"
                ),
                LegalArticle(
                    law=DataLaw.HIPAA,
                    article="§164.502",
                    description="Uses and disclosures of PHI - minimum necessary",
                    requirement=ComplianceRequirement.MANDATORY,
                    penalty_severity="HIGH"
                ),
                LegalArticle(
                    law=DataLaw.KENYA_DPA,
                    article="§25",
                    description="Principles of data processing",
                    requirement=ComplianceRequirement.MANDATORY,
                    penalty_severity="HIGH"
                ),
                LegalArticle(
                    law=DataLaw.POPIA,
                    article="§11",
                    description="Lawfulness of processing",
                    requirement=ComplianceRequirement.MANDATORY,
                    penalty_severity="HIGH"
                ),
                LegalArticle(
                    law=DataLaw.WHO_IHR,
                    article="Art. 6",
                    description="Notification - public health emergency data collection",
                    requirement=ComplianceRequirement.CONDITIONAL,
                    penalty_severity="MEDIUM"
                ),
                LegalArticle(
                    law=DataLaw.FHIR_R4_R5,
                    article="Consent Resource",
                    description="Structured consent for health data collection",
                    requirement=ComplianceRequirement.RECOMMENDED,
                    penalty_severity="LOW"
                ),
            ],
            enforcement_logic="require_explicit_consent AND minimum_necessary_principle",
            humanitarian_override=True
        )
        
        # CROSS-BORDER TRANSFER
        self.rules[DataHandlingOperation.CROSS_BORDER_TRANSFER] = ComplianceRule(
            operation=DataHandlingOperation.CROSS_BORDER_TRANSFER,
            applicable_laws=[
                LegalArticle(
                    law=DataLaw.GDPR,
                    article="Art. 44-50",
                    description="Transfers to third countries - adequacy required",
                    requirement=ComplianceRequirement.MANDATORY,
                    penalty_severity="CRITICAL"
                ),
                LegalArticle(
                    law=DataLaw.KENYA_DPA,
                    article="§48",
                    description="Transfer of personal data outside Kenya",
                    requirement=ComplianceRequirement.MANDATORY,
                    penalty_severity="CRITICAL"
                ),
                LegalArticle(
                    law=DataLaw.POPIA,
                    article="§72",
                    description="Transfer of personal information outside RSA",
                    requirement=ComplianceRequirement.MANDATORY,
                    penalty_severity="CRITICAL"
                ),
                LegalArticle(
                    law=DataLaw.LGPD,
                    article="Art. 33",
                    description="International data transfer",
                    requirement=ComplianceRequirement.MANDATORY,
                    penalty_severity="CRITICAL"
                ),
                LegalArticle(
                    law=DataLaw.APPI,
                    article="Art. 24",
                    description="Restrictions on provision to third parties in foreign countries",
                    requirement=ComplianceRequirement.MANDATORY,
                    penalty_severity="HIGH"
                ),
                LegalArticle(
                    law=DataLaw.AU_MALABO,
                    article="Art. 14",
                    description="Protection of personal data",
                    requirement=ComplianceRequirement.MANDATORY,
                    penalty_severity="HIGH"
                ),
            ],
            enforcement_logic="block_unless_adequacy_decision OR standard_contractual_clauses",
            humanitarian_override=False  # NEVER override sovereignty
        )
        
        # AI INFERENCE
        self.rules[DataHandlingOperation.AI_INFERENCE] = ComplianceRule(
            operation=DataHandlingOperation.AI_INFERENCE,
            applicable_laws=[
                LegalArticle(
                    law=DataLaw.GDPR,
                    article="Art. 22",
                    description="Right not to be subject to automated decision-making",
                    requirement=ComplianceRequirement.MANDATORY,
                    penalty_severity="HIGH"
                ),
                LegalArticle(
                    law=DataLaw.EU_AI_ACT,
                    article="§6",
                    description="Classification of high-risk AI systems",
                    requirement=ComplianceRequirement.MANDATORY,
                    penalty_severity="CRITICAL"
                ),
                LegalArticle(
                    law=DataLaw.EU_AI_ACT,
                    article="§13",
                    description="Transparency and provision of information to users",
                    requirement=ComplianceRequirement.MANDATORY,
                    penalty_severity="HIGH"
                ),
                LegalArticle(
                    law=DataLaw.HIPAA,
                    article="§164.312(a)(2)(i)",
                    description="Unique user identification for AI systems",
                    requirement=ComplianceRequirement.MANDATORY,
                    penalty_severity="HIGH"
                ),
                LegalArticle(
                    law=DataLaw.FHIR_R4_R5,
                    article="Provenance Resource",
                    description="Track AI inference provenance",
                    requirement=ComplianceRequirement.RECOMMENDED,
                    penalty_severity="MEDIUM"
                ),
            ],
            enforcement_logic="require_explainability AND human_oversight AND audit_trail",
            humanitarian_override=True
        )
        
        # DELETION (Right to Erasure)
        self.rules[DataHandlingOperation.DELETION] = ComplianceRule(
            operation=DataHandlingOperation.DELETION,
            applicable_laws=[
                LegalArticle(
                    law=DataLaw.GDPR,
                    article="Art. 17",
                    description="Right to erasure ('right to be forgotten')",
                    requirement=ComplianceRequirement.MANDATORY,
                    penalty_severity="HIGH"
                ),
                LegalArticle(
                    law=DataLaw.CCPA,
                    article="§1798.105",
                    description="Consumer's right to deletion",
                    requirement=ComplianceRequirement.MANDATORY,
                    penalty_severity="HIGH"
                ),
                LegalArticle(
                    law=DataLaw.LGPD,
                    article="Art. 18(VI)",
                    description="Right to deletion of personal data",
                    requirement=ComplianceRequirement.MANDATORY,
                    penalty_severity="HIGH"
                ),
                LegalArticle(
                    law=DataLaw.HIPAA,
                    article="§164.530(j)",
                    description="Retention of documentation (6 years minimum)",
                    requirement=ComplianceRequirement.MANDATORY,
                    penalty_severity="MEDIUM"
                ),
            ],
            enforcement_logic="crypto_shredder_dissolution OR secure_deletion_dod_5220",
            humanitarian_override=False
        )
        
        # CONSENT MANAGEMENT
        self.rules[DataHandlingOperation.CONSENT_MANAGEMENT] = ComplianceRule(
            operation=DataHandlingOperation.CONSENT_MANAGEMENT,
            applicable_laws=[
                LegalArticle(
                    law=DataLaw.GDPR,
                    article="Art. 7",
                    description="Conditions for consent",
                    requirement=ComplianceRequirement.MANDATORY,
                    penalty_severity="HIGH"
                ),
                LegalArticle(
                    law=DataLaw.POPIA,
                    article="§11",
                    description="Consent required for processing",
                    requirement=ComplianceRequirement.MANDATORY,
                    penalty_severity="HIGH"
                ),
                LegalArticle(
                    law=DataLaw.NDPR,
                    article="§2.2",
                    description="Consent and legitimate interest",
                    requirement=ComplianceRequirement.MANDATORY,
                    penalty_severity="HIGH"
                ),
                LegalArticle(
                    law=DataLaw.PIPEDA,
                    article="Principle 3",
                    description="Consent",
                    requirement=ComplianceRequirement.MANDATORY,
                    penalty_severity="MEDIUM"
                ),
                LegalArticle(
                    law=DataLaw.FHIR_R4_R5,
                    article="Consent Resource",
                    description="Structured consent representation",
                    requirement=ComplianceRequirement.RECOMMENDED,
                    penalty_severity="LOW"
                ),
            ],
            enforcement_logic="explicit_consent AND granular_scope AND revocable",
            humanitarian_override=True  # Emergency override per WHO IHR Art. 6
        )
        
        # ENCRYPTION
        self.rules[DataHandlingOperation.ENCRYPTION] = ComplianceRule(
            operation=DataHandlingOperation.ENCRYPTION,
            applicable_laws=[
                LegalArticle(
                    law=DataLaw.GDPR,
                    article="Art. 32",
                    description="Security of processing - encryption required",
                    requirement=ComplianceRequirement.MANDATORY,
                    penalty_severity="HIGH"
                ),
                LegalArticle(
                    law=DataLaw.HIPAA,
                    article="§164.312(a)(2)(iv)",
                    description="Encryption and decryption",
                    requirement=ComplianceRequirement.RECOMMENDED,
                    penalty_severity="MEDIUM"
                ),
                LegalArticle(
                    law=DataLaw.KENYA_DPA,
                    article="§41",
                    description="Security safeguards",
                    requirement=ComplianceRequirement.MANDATORY,
                    penalty_severity="HIGH"
                ),
                LegalArticle(
                    law=DataLaw.AU_MALABO,
                    article="Art. 13",
                    description="Cryptography",
                    requirement=ComplianceRequirement.MANDATORY,
                    penalty_severity="HIGH"
                ),
            ],
            enforcement_logic="aes_256_gcm AND key_rotation AND crypto_shredder",
            humanitarian_override=False
        )
        
        # AUDIT LOGGING
        self.rules[DataHandlingOperation.AUDIT_LOGGING] = ComplianceRule(
            operation=DataHandlingOperation.AUDIT_LOGGING,
            applicable_laws=[
                LegalArticle(
                    law=DataLaw.GDPR,
                    article="Art. 30",
                    description="Records of processing activities",
                    requirement=ComplianceRequirement.MANDATORY,
                    penalty_severity="MEDIUM"
                ),
                LegalArticle(
                    law=DataLaw.HIPAA,
                    article="§164.312(b)",
                    description="Audit controls",
                    requirement=ComplianceRequirement.MANDATORY,
                    penalty_severity="HIGH"
                ),
                LegalArticle(
                    law=DataLaw.EU_AI_ACT,
                    article="§12",
                    description="Record-keeping for high-risk AI",
                    requirement=ComplianceRequirement.MANDATORY,
                    penalty_severity="HIGH"
                ),
                LegalArticle(
                    law=DataLaw.GENEVA_CONVENTIONS,
                    article="Protocol I, Art. 75",
                    description="Fundamental guarantees - accountability",
                    requirement=ComplianceRequirement.MANDATORY,
                    penalty_severity="CRITICAL"
                ),
            ],
            enforcement_logic="tamper_proof_ledger AND cryptographic_signing AND 7_year_retention",
            humanitarian_override=False
        )
        
        # STORAGE
        self.rules[DataHandlingOperation.STORAGE] = ComplianceRule(
            operation=DataHandlingOperation.STORAGE,
            applicable_laws=[
                LegalArticle(
                    law=DataLaw.GDPR,
                    article="Art. 5(1)(e)",
                    description="Storage limitation principle",
                    requirement=ComplianceRequirement.MANDATORY,
                    penalty_severity="MEDIUM"
                ),
                LegalArticle(
                    law=DataLaw.HIPAA,
                    article="§164.530(j)",
                    description="Documentation retention (6 years)",
                    requirement=ComplianceRequirement.MANDATORY,
                    penalty_severity="MEDIUM"
                ),
                LegalArticle(
                    law=DataLaw.FHIR_R4_R5,
                    article="Security Labels",
                    description="Data classification and storage controls",
                    requirement=ComplianceRequirement.RECOMMENDED,
                    penalty_severity="LOW"
                ),
            ],
            enforcement_logic="retention_policy AND hot_warm_cold_storage AND auto_shred",
            humanitarian_override=False
        )
    
    def get_applicable_laws(
        self, 
        operation: DataHandlingOperation
    ) -> List[LegalArticle]:
        """Get all applicable laws for a data handling operation"""
        if operation not in self.rules:
            logger.warning(f"⚠️ No compliance rules for operation: {operation}")
            return []
        
        return self.rules[operation].applicable_laws
    
    def check_compliance(
        self,
        operation: DataHandlingOperation,
        context: Dict,
        jurisdiction: Optional[DataLaw] = None
    ) -> Dict:
        """
        Check compliance for a specific operation
        
        Args:
            operation: The data handling operation
            context: Context including data type, destination, etc.
            jurisdiction: Primary jurisdiction (optional)
        
        Returns:
            Compliance check result with violations and recommendations
        """
        if operation not in self.rules:
            return {
                "compliant": False,
                "error": f"Unknown operation: {operation}",
                "violations": [],
                "recommendations": []
            }
        
        rule = self.rules[operation]
        violations = []
        recommendations = []
        
        # Check each applicable law
        for article in rule.applicable_laws:
            # Filter by jurisdiction if specified
            if jurisdiction and article.law != jurisdiction:
                continue
            
            # Check if requirement is met
            if article.requirement == ComplianceRequirement.MANDATORY:
                # This would contain actual validation logic
                # For now, we'll check basic context requirements
                if not self._validate_article(article, context):
                    violations.append({
                        "law": article.law.value,
                        "article": article.article,
                        "description": article.description,
                        "severity": article.penalty_severity
                    })
            
            elif article.requirement == ComplianceRequirement.RECOMMENDED:
                recommendations.append({
                    "law": article.law.value,
                    "article": article.article,
                    "description": article.description
                })
        
        return {
            "compliant": len(violations) == 0,
            "operation": operation.value,
            "enforcement_logic": rule.enforcement_logic,
            "humanitarian_override_available": rule.humanitarian_override,
            "violations": violations,
            "recommendations": recommendations,
            "timestamp": datetime.utcnow().isoformat()
        }
    
    def _validate_article(self, article: LegalArticle, context: Dict) -> bool:
        """Validate if context meets article requirements"""
        # This would contain the actual validation logic
        # For now, return True for demonstration
        return True
    
    def get_cross_law_conflicts(
        self,
        operation: DataHandlingOperation
    ) -> List[Dict]:
        """
        Identify conflicts between different legal frameworks
        
        Returns:
            List of potential conflicts
        """
        conflicts = []
        
        if operation not in self.rules:
            return conflicts
        
        laws = self.rules[operation].applicable_laws
        
        # Example: HIPAA allows 6-year retention, GDPR requires deletion on request
        if operation == DataHandlingOperation.DELETION:
            conflicts.append({
                "conflict": "Retention vs. Erasure",
                "law_a": "HIPAA §164.530(j) - 6 year minimum retention",
                "law_b": "GDPR Art. 17 - Right to erasure",
                "resolution": "Use Crypto Shredder: Data encrypted, key shredded after 6 years"
            })
        
        return conflicts
    
    def generate_compliance_report(self) -> Dict:
        """Generate a comprehensive compliance report"""
        report = {
            "timestamp": datetime.utcnow().isoformat(),
            "total_laws": len(DataLaw),
            "total_operations": len(DataHandlingOperation),
            "total_rules": len(self.rules),
            "laws": {},
            "operations": {}
        }
        
        # Count articles per law
        for law in DataLaw:
            report["laws"][law.value] = {
                "articles": 0,
                "mandatory": 0,
                "recommended": 0
            }
        
        # Aggregate statistics
        for operation, rule in self.rules.items():
            report["operations"][operation.value] = {
                "applicable_laws": len(rule.applicable_laws),
                "humanitarian_override": rule.humanitarian_override,
                "enforcement_logic": rule.enforcement_logic
            }
            
            for article in rule.applicable_laws:
                report["laws"][article.law.value]["articles"] += 1
                if article.requirement == ComplianceRequirement.MANDATORY:
                    report["laws"][article.law.value]["mandatory"] += 1
                elif article.requirement == ComplianceRequirement.RECOMMENDED:
                    report["laws"][article.law.value]["recommended"] += 1
        
        return report


# Singleton instance
_compliance_matrix = None

def get_compliance_matrix() -> ComplianceMatrix:
    """Get the global ComplianceMatrix instance"""
    global _compliance_matrix
    if _compliance_matrix is None:
        _compliance_matrix = ComplianceMatrix()
    return _compliance_matrix


# Example usage
if __name__ == "__main__":
    matrix = get_compliance_matrix()
    
    # Check cross-border transfer compliance
    result = matrix.check_compliance(
        operation=DataHandlingOperation.CROSS_BORDER_TRANSFER,
        context={
            "data_type": "PHI",
            "source_country": "Kenya",
            "destination_country": "USA",
            "adequacy_decision": False
        },
        jurisdiction=DataLaw.KENYA_DPA
    )
    
    print("🔍 Compliance Check: Cross-Border Transfer")
    print(f"Compliant: {result['compliant']}")
    print(f"Violations: {len(result['violations'])}")
    
    for violation in result['violations']:
        print(f"  ❌ {violation['law']} {violation['article']}")
        print(f"     {violation['description']}")
        print(f"     Severity: {violation['severity']}")
    
    # Generate compliance report
    report = matrix.generate_compliance_report()
    print(f"\n📊 Compliance Report")
    print(f"Total Laws: {report['total_laws']}")
    print(f"Total Operations: {report['total_operations']}")
    print(f"Total Rules: {report['total_rules']}")
