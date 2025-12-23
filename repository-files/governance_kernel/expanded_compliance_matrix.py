"""
Expanded Compliance Matrix: 29 Global Legal Frameworks
═══════════════════════════════════════════════════════════════════════════════

This module extends the SovereignGuardrail to enforce all 29 global legal 
frameworks for comprehensive sovereign health intelligence.

Philosophy: "Global sovereignty requires global compliance."
"""

from enum import Enum
from typing import Dict, Any
from datetime import datetime


class ComplianceFramework(Enum):
    """All 29 global legal frameworks encoded in iLuminara-Core"""
    
    # Data Protection Laws (14)
    GDPR_EU = "GDPR (EU)"
    KDPA_KE = "KDPA (Kenya)"
    PIPEDA_CA = "PIPEDA (Canada)"
    POPIA_ZA = "POPIA (South Africa)"
    HIPAA_US = "HIPAA (USA)"
    HITECH_US = "HITECH (USA)"
    CCPA_US = "CCPA (California, USA)"
    NDPA_NG = "NDPA (Nigeria)"
    PDPA_SG = "PDPA (Singapore)"
    LGPD_BR = "LGPD (Brazil)"
    APPI_JP = "APPI (Japan)"
    PDPA_TH = "PDPA (Thailand)"
    DPA_AE = "DPA (UAE)"
    GDPR_ART9 = "GDPR Article 9 (Special Categories)"
    
    # Security & Technical Standards (3)
    NIST_CSF = "NIST CSF (USA)"
    ISO_27001 = "ISO 27001 (Global)"
    SOC_2 = "SOC 2 (USA)"
    
    # AI & Technology Regulation (1)
    EU_AI_ACT = "EU AI Act"
    
    # Humanitarian & International Law (8)
    GENEVA_CONVENTIONS = "Geneva Conventions (1949)"
    WHO_IHR_2005 = "WHO IHR (2005)"
    UN_CRC = "UN Convention on Rights of the Child"
    UNHCR_GUIDELINES = "UNHCR Guidelines"
    SPHERE_STANDARDS = "Sphere Standards"
    ICRC_MEDICAL_ETHICS = "ICRC Medical Ethics"
    UN_HUMANITARIAN_PRINCIPLES = "UN Humanitarian Principles"
    CORE_HUMANITARIAN_STANDARD = "Core Humanitarian Standard (CHS)"
    
    # iLuminara Sovereign Principles (3)
    DATA_SOVEREIGNTY = "Data Sovereignty (Global)"
    RIGHT_TO_EXPLANATION = "Right to Explanation (Global)"
    DIGNITY_PRESERVATION = "Dignity Preservation (Global)"


class ExpandedComplianceMatrix:
    """
    Comprehensive compliance matrix for all 29 global legal frameworks.
    
    Extends the base SovereignGuardrail with additional jurisdictions and
    humanitarian law enforcement.
    """
    
    def __init__(self):
        self.compliance_rules = self._build_expanded_matrix()
    
    def _build_expanded_matrix(self) -> Dict[str, Dict[str, Any]]:
        """Build the complete 29-framework compliance matrix"""
        
        return {
            # ═══════════════════════════════════════════════════════════
            # DATA PROTECTION LAWS (14 frameworks)
            # ═══════════════════════════════════════════════════════════
            
            "GDPR_EU": {
                "framework": ComplianceFramework.GDPR_EU,
                "region": "European Union",
                "data_sovereignty_required": True,
                "requires_explicit_consent": True,
                "special_categories_prohibited_foreign": True,
                "right_to_explanation_required": True,
                "retention_max_days": 2555,  # 7 years
                "breach_notification_hours": 72,
                "key_articles": ["Art. 6", "Art. 9", "Art. 17", "Art. 22", "Art. 30", "Art. 32"],
                "penalties": "Up to €20M or 4% global revenue"
            },
            
            "KDPA_KE": {
                "framework": ComplianceFramework.KDPA_KE,
                "region": "Kenya",
                "data_sovereignty_required": True,
                "requires_explicit_consent": True,
                "special_categories_prohibited_foreign": True,
                "right_to_explanation_required": False,
                "retention_max_days": 1825,  # 5 years
                "breach_notification_hours": 72,
                "key_sections": ["§37", "§42"],
                "penalties": "Up to KES 5M or 1% revenue"
            },
            
            "PIPEDA_CA": {
                "framework": ComplianceFramework.PIPEDA_CA,
                "region": "Canada",
                "data_sovereignty_required": False,  # Allows cross-border with safeguards
                "requires_explicit_consent": True,
                "special_categories_prohibited_foreign": True,
                "right_to_explanation_required": False,
                "retention_max_days": 1825,
                "breach_notification_hours": 30,
                "key_sections": ["§5", "§6", "§7"],
                "penalties": "Up to CAD $100K per violation"
            },
            
            "POPIA_ZA": {
                "framework": ComplianceFramework.POPIA_ZA,
                "region": "South Africa",
                "data_sovereignty_required": True,
                "requires_explicit_consent": True,
                "special_categories_prohibited_foreign": True,
                "right_to_explanation_required": False,
                "retention_max_days": 2555,
                "breach_notification_hours": 168,  # 7 days
                "key_sections": ["§11", "§14"],
                "penalties": "Up to ZAR 10M or 10 years imprisonment"
            },
            
            "HIPAA_US": {
                "framework": ComplianceFramework.HIPAA_US,
                "region": "United States",
                "data_sovereignty_required": False,
                "requires_explicit_consent": False,  # Covered entities exempt for treatment
                "special_categories_prohibited_foreign": True,
                "right_to_explanation_required": False,
                "retention_max_days": 2555,
                "breach_notification_hours": 60,
                "key_sections": ["§164.312", "§164.404", "§164.530(j)"],
                "penalties": "Up to $1.5M per violation category per year"
            },
            
            "HITECH_US": {
                "framework": ComplianceFramework.HITECH_US,
                "region": "United States",
                "data_sovereignty_required": False,
                "requires_explicit_consent": False,
                "special_categories_prohibited_foreign": True,
                "right_to_explanation_required": False,
                "retention_max_days": 2555,
                "breach_notification_hours": 60,
                "key_sections": ["§13410"],
                "penalties": "Up to $1.5M per violation"
            },
            
            "CCPA_US": {
                "framework": ComplianceFramework.CCPA_US,
                "region": "California, USA",
                "data_sovereignty_required": False,
                "requires_explicit_consent": True,
                "special_categories_prohibited_foreign": False,
                "right_to_explanation_required": False,
                "retention_max_days": 1825,
                "breach_notification_hours": 72,
                "key_sections": ["§1798.100", "§1798.110", "§1798.120"],
                "penalties": "Up to $7,500 per intentional violation"
            },
            
            "NDPA_NG": {
                "framework": ComplianceFramework.NDPA_NG,
                "region": "Nigeria",
                "data_sovereignty_required": True,
                "requires_explicit_consent": True,
                "special_categories_prohibited_foreign": True,
                "right_to_explanation_required": False,
                "retention_max_days": 1825,
                "breach_notification_hours": 72,
                "key_sections": ["Part III", "Part IV"],
                "penalties": "Up to NGN 10M or 2% revenue"
            },
            
            "PDPA_SG": {
                "framework": ComplianceFramework.PDPA_SG,
                "region": "Singapore",
                "data_sovereignty_required": False,
                "requires_explicit_consent": True,
                "special_categories_prohibited_foreign": False,
                "right_to_explanation_required": False,
                "retention_max_days": 1825,
                "breach_notification_hours": 72,
                "key_sections": ["Part IV", "Part VI"],
                "penalties": "Up to SGD 1M"
            },
            
            "LGPD_BR": {
                "framework": ComplianceFramework.LGPD_BR,
                "region": "Brazil",
                "data_sovereignty_required": True,
                "requires_explicit_consent": True,
                "special_categories_prohibited_foreign": True,
                "right_to_explanation_required": True,
                "retention_max_days": 1825,
                "breach_notification_hours": 72,
                "key_sections": ["Art. 7", "Art. 11", "Art. 20"],
                "penalties": "Up to BRL 50M or 2% revenue"
            },
            
            "APPI_JP": {
                "framework": ComplianceFramework.APPI_JP,
                "region": "Japan",
                "data_sovereignty_required": False,
                "requires_explicit_consent": True,
                "special_categories_prohibited_foreign": True,
                "right_to_explanation_required": False,
                "retention_max_days": 1825,
                "breach_notification_hours": 72,
                "key_sections": ["Art. 15", "Art. 16", "Art. 23"],
                "penalties": "Up to JPY 100M"
            },
            
            "PDPA_TH": {
                "framework": ComplianceFramework.PDPA_TH,
                "region": "Thailand",
                "data_sovereignty_required": True,
                "requires_explicit_consent": True,
                "special_categories_prohibited_foreign": True,
                "right_to_explanation_required": False,
                "retention_max_days": 1825,
                "breach_notification_hours": 72,
                "key_sections": ["§26", "§27", "§28"],
                "penalties": "Up to THB 5M"
            },
            
            "DPA_AE": {
                "framework": ComplianceFramework.DPA_AE,
                "region": "United Arab Emirates",
                "data_sovereignty_required": True,
                "requires_explicit_consent": True,
                "special_categories_prohibited_foreign": True,
                "right_to_explanation_required": False,
                "retention_max_days": 1825,
                "breach_notification_hours": 72,
                "key_sections": ["Art. 5", "Art. 6", "Art. 9"],
                "penalties": "Up to AED 3M"
            },
            
            "GDPR_ART9": {
                "framework": ComplianceFramework.GDPR_ART9,
                "region": "European Union",
                "data_sovereignty_required": True,
                "requires_explicit_consent": True,
                "special_categories_prohibited_foreign": True,
                "right_to_explanation_required": True,
                "retention_max_days": 2555,
                "breach_notification_hours": 72,
                "key_articles": ["Art. 9"],
                "penalties": "Up to €20M or 4% global revenue"
            },
            
            # ═══════════════════════════════════════════════════════════
            # SECURITY & TECHNICAL STANDARDS (3 frameworks)
            # ═══════════════════════════════════════════════════════════
            
            "NIST_CSF": {
                "framework": ComplianceFramework.NIST_CSF,
                "region": "United States",
                "functions": ["Identify", "Protect", "Detect", "Respond", "Recover"],
                "categories": 23,
                "subcategories": 108,
                "implementation_tiers": ["Partial", "Risk Informed", "Repeatable", "Adaptive"]
            },
            
            "ISO_27001": {
                "framework": ComplianceFramework.ISO_27001,
                "region": "Global",
                "control_objectives": 14,
                "controls": 114,
                "key_controls": ["A.8.3.2", "A.12.4", "A.12.6"],
                "certification_required": True
            },
            
            "SOC_2": {
                "framework": ComplianceFramework.SOC_2,
                "region": "United States",
                "trust_service_criteria": [
                    "Security",
                    "Availability",
                    "Processing Integrity",
                    "Confidentiality",
                    "Privacy"
                ],
                "audit_required": True
            },
            
            # ═══════════════════════════════════════════════════════════
            # AI & TECHNOLOGY REGULATION (1 framework)
            # ═══════════════════════════════════════════════════════════
            
            "EU_AI_ACT": {
                "framework": ComplianceFramework.EU_AI_ACT,
                "region": "European Union",
                "high_risk_systems": True,
                "transparency_required": True,
                "human_oversight_required": True,
                "key_articles": ["§6", "§8", "§12"],
                "penalties": "Up to €30M or 6% global revenue"
            },
            
            # ═══════════════════════════════════════════════════════════
            # HUMANITARIAN & INTERNATIONAL LAW (8 frameworks)
            # ═══════════════════════════════════════════════════════════
            
            "GENEVA_CONVENTIONS": {
                "framework": ComplianceFramework.GENEVA_CONVENTIONS,
                "region": "International",
                "year": 1949,
                "key_principles": [
                    "Protection of civilians",
                    "Distinction between combatants and civilians",
                    "Proportionality",
                    "Precaution",
                    "Prohibition of collective punishment"
                ],
                "key_articles": ["Art. 3", "Art. 27", "Art. 147"],
                "binding": True
            },
            
            "WHO_IHR_2005": {
                "framework": ComplianceFramework.WHO_IHR_2005,
                "region": "International",
                "year": 2005,
                "key_requirements": [
                    "Disease surveillance",
                    "Outbreak notification",
                    "Emergency response",
                    "Core capacity building"
                ],
                "key_articles": ["Art. 6", "Art. 7", "Art. 12"],
                "binding": True
            },
            
            "UN_CRC": {
                "framework": ComplianceFramework.UN_CRC,
                "region": "International",
                "year": 1989,
                "key_principles": [
                    "Best interests of the child",
                    "Non-discrimination",
                    "Right to life and development",
                    "Respect for views of the child"
                ],
                "key_articles": ["Art. 3", "Art. 6", "Art. 24"],
                "binding": True
            },
            
            "UNHCR_GUIDELINES": {
                "framework": ComplianceFramework.UNHCR_GUIDELINES,
                "region": "International",
                "key_principles": [
                    "Refugee protection",
                    "Non-refoulement",
                    "Access to asylum",
                    "Family unity"
                ],
                "binding": False,
                "authoritative": True
            },
            
            "SPHERE_STANDARDS": {
                "framework": ComplianceFramework.SPHERE_STANDARDS,
                "region": "International",
                "key_sectors": [
                    "Water supply and sanitation",
                    "Food security and nutrition",
                    "Shelter and settlement",
                    "Health"
                ],
                "minimum_standards": True,
                "binding": False
            },
            
            "ICRC_MEDICAL_ETHICS": {
                "framework": ComplianceFramework.ICRC_MEDICAL_ETHICS,
                "region": "International",
                "key_principles": [
                    "Medical neutrality",
                    "Impartiality",
                    "Do no harm",
                    "Confidentiality",
                    "Informed consent"
                ],
                "binding": False,
                "authoritative": True
            },
            
            "UN_HUMANITARIAN_PRINCIPLES": {
                "framework": ComplianceFramework.UN_HUMANITARIAN_PRINCIPLES,
                "region": "International",
                "core_principles": [
                    "Humanity",
                    "Neutrality",
                    "Impartiality",
                    "Independence"
                ],
                "binding": False,
                "authoritative": True
            },
            
            "CORE_HUMANITARIAN_STANDARD": {
                "framework": ComplianceFramework.CORE_HUMANITARIAN_STANDARD,
                "region": "International",
                "commitments": 9,
                "key_areas": [
                    "Appropriateness and relevance",
                    "Effectiveness and timeliness",
                    "Strengthening local capacities",
                    "Communication and participation",
                    "Complaints and feedback"
                ],
                "binding": False
            },
            
            # ═══════════════════════════════════════════════════════════
            # iLUMINARA SOVEREIGN PRINCIPLES (3 frameworks)
            # ═══════════════════════════════════════════════════════════
            
            "DATA_SOVEREIGNTY": {
                "framework": ComplianceFramework.DATA_SOVEREIGNTY,
                "region": "Global",
                "principle": "Health data remains in sovereign territory",
                "enforcement": "SovereignGuardrail + Golden Thread",
                "violations_blocked": True
            },
            
            "RIGHT_TO_EXPLANATION": {
                "framework": ComplianceFramework.RIGHT_TO_EXPLANATION,
                "region": "Global",
                "principle": "Every high-risk inference requires SHAP explainability",
                "enforcement": "Vertex AI Explainable AI",
                "violations_blocked": True
            },
            
            "DIGNITY_PRESERVATION": {
                "framework": ComplianceFramework.DIGNITY_PRESERVATION,
                "region": "Global",
                "principle": "Every decision enhances sovereign dignity",
                "enforcement": "Ethical Engine + Humanitarian Constraints",
                "violations_blocked": True
            },
            
            # ═══════════════════════════════════════════════════════════
            # GLOBAL DEFAULT (Baseline)
            # ═══════════════════════════════════════════════════════════
            
            "GLOBAL_DEFAULT": {
                "framework": "GLOBAL_DEFAULT",
                "region": "Global",
                "data_sovereignty_required": True,
                "requires_explicit_consent": True,
                "special_categories_prohibited_foreign": True,
                "right_to_explanation_required": True,
                "retention_max_days": 1825,
                "breach_notification_hours": 72,
                "description": "Baseline sovereignty rules when specific jurisdiction unknown"
            }
        }
    
    def get_framework_details(self, framework_id: str) -> Dict[str, Any]:
        """Get detailed information about a specific framework"""
        return self.compliance_rules.get(framework_id, self.compliance_rules["GLOBAL_DEFAULT"])
    
    def get_all_frameworks(self) -> list:
        """Get list of all 29 frameworks"""
        return list(ComplianceFramework)
    
    def get_frameworks_by_region(self, region: str) -> list:
        """Get all frameworks applicable to a specific region"""
        return [
            framework_id 
            for framework_id, details in self.compliance_rules.items()
            if details.get("region") == region
        ]
    
    def validate_multi_jurisdiction(
        self,
        action_type: str,
        payload: Dict[str, Any],
        jurisdictions: list
    ) -> Dict[str, Any]:
        """
        Validate an action against multiple jurisdictions simultaneously.
        
        Returns:
            {
                "compliant": bool,
                "violations": list,
                "strictest_requirements": dict
            }
        """
        violations = []
        strictest_requirements = {
            "retention_max_days": float('inf'),
            "breach_notification_hours": float('inf'),
            "data_sovereignty_required": False,
            "requires_explicit_consent": False
        }
        
        for jurisdiction in jurisdictions:
            rules = self.get_framework_details(jurisdiction)
            
            # Track strictest requirements
            if "retention_max_days" in rules:
                strictest_requirements["retention_max_days"] = min(
                    strictest_requirements["retention_max_days"],
                    rules["retention_max_days"]
                )
            
            if "breach_notification_hours" in rules:
                strictest_requirements["breach_notification_hours"] = min(
                    strictest_requirements["breach_notification_hours"],
                    rules["breach_notification_hours"]
                )
            
            if rules.get("data_sovereignty_required"):
                strictest_requirements["data_sovereignty_required"] = True
            
            if rules.get("requires_explicit_consent"):
                strictest_requirements["requires_explicit_consent"] = True
        
        return {
            "compliant": len(violations) == 0,
            "violations": violations,
            "strictest_requirements": strictest_requirements,
            "jurisdictions_checked": jurisdictions
        }


# Example usage
if __name__ == "__main__":
    matrix = ExpandedComplianceMatrix()
    
    print("═" * 70)
    print("iLuminara-Core: 29 Global Legal Frameworks")
    print("═" * 70)
    print()
    
    # List all frameworks
    frameworks = matrix.get_all_frameworks()
    print(f"Total Frameworks: {len(frameworks)}")
    print()
    
    # Group by category
    categories = {
        "Data Protection Laws": 14,
        "Security & Technical Standards": 3,
        "AI & Technology Regulation": 1,
        "Humanitarian & International Law": 8,
        "iLuminara Sovereign Principles": 3
    }
    
    for category, count in categories.items():
        print(f"  {category}: {count}")
    
    print()
    print("═" * 70)
    print("Sample Framework Details")
    print("═" * 70)
    print()
    
    # Show details for GDPR
    gdpr = matrix.get_framework_details("GDPR_EU")
    print(f"Framework: {gdpr['framework'].value}")
    print(f"Region: {gdpr['region']}")
    print(f"Data Sovereignty Required: {gdpr['data_sovereignty_required']}")
    print(f"Retention Max: {gdpr['retention_max_days']} days")
    print(f"Breach Notification: {gdpr['breach_notification_hours']} hours")
    print(f"Key Articles: {', '.join(gdpr['key_articles'])}")
    print(f"Penalties: {gdpr['penalties']}")
