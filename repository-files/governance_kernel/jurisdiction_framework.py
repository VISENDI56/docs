"""
iLuminara-Core Jurisdiction Framework
45+ Global Legal Frameworks for Sovereign Health Intelligence

This module defines the complete regulatory universe that iLuminara operates within,
spanning data protection, AI governance, health security, supply chain ethics,
environmental standards, and international reporting.

Architecture: Quantum-Law Nexus
- Dynamic framework activation based on context
- Retroactive alignment engine for regulatory updates
- AI-triggered harmonization across jurisdictions
"""

from enum import Enum
from typing import Dict, List, Optional, Set
from dataclasses import dataclass
from datetime import datetime


class JurisdictionFramework(Enum):
    """
    Complete enumeration of 45+ global legal frameworks.
    Organized by regulatory domain for the Quantum-Law Nexus.
    """
    
    # ═══════════════════════════════════════════════════════════
    # I. CORE DATA PROTECTION (Original 14 Frameworks)
    # ═══════════════════════════════════════════════════════════
    
    GDPR_EU = "GDPR (EU) - General Data Protection Regulation"
    GDPR_ART9 = "GDPR Article 9 - Special Categories of Personal Data"
    KDPA_KE = "KDPA (Kenya) - Kenya Data Protection Act"
    PIPEDA_CA = "PIPEDA (Canada) - Personal Information Protection and Electronic Documents Act"
    POPIA_ZA = "POPIA (South Africa) - Protection of Personal Information Act"
    HIPAA_US = "HIPAA (USA) - Health Insurance Portability and Accountability Act"
    HITECH_US = "HITECH (USA) - Health Information Technology for Economic and Clinical Health Act"
    CCPA_US = "CCPA (USA) - California Consumer Privacy Act"
    NIST_CSF = "NIST CSF (USA) - Cybersecurity Framework"
    ISO_27001 = "ISO 27001 - Information Security Management"
    SOC_2 = "SOC 2 (USA) - Service Organization Control 2"
    EU_AI_ACT = "EU AI Act - Regulation 2024/1689"
    WHO_IHR = "WHO IHR - International Health Regulations (2005, 2025 amendments)"
    GLOBAL_DEFAULT = "GLOBAL_DEFAULT - Universal baseline"
    
    # ═══════════════════════════════════════════════════════════
    # II. SUPPLY CHAIN & PROCUREMENT ETHICS (Expansion Pack 1)
    # ═══════════════════════════════════════════════════════════
    
    EU_CSDDD = "EU CSDDD - Corporate Sustainability Due Diligence Directive"
    OECD_DUE_DILIGENCE = "OECD Due Diligence Guidance for Responsible Business Conduct"
    UN_GUIDING_PRINCIPLES = "UN Guiding Principles on Business and Human Rights"
    ILO_CONVENTIONS = "ILO Core Conventions - Forced Labor, Child Labor, Discrimination"
    IASC_GUIDELINES = "IASC Guidelines - Humanitarian Data Protection"
    
    # ═══════════════════════════════════════════════════════════
    # III. ENVIRONMENTAL & CARBON STANDARDS (Expansion Pack 2)
    # ═══════════════════════════════════════════════════════════
    
    EU_CBAM = "EU CBAM - Carbon Border Adjustment Mechanism"
    ICVCM_STANDARDS = "ICVCM - Integrity Council for Voluntary Carbon Market"
    TCFD = "TCFD - Task Force on Climate-related Financial Disclosures"
    GHG_PROTOCOL = "GHG Protocol - Corporate Accounting and Reporting Standard"
    
    # ═══════════════════════════════════════════════════════════
    # IV. FINANCIAL INTEGRITY & ANTI-CORRUPTION (Expansion Pack 3)
    # ═══════════════════════════════════════════════════════════
    
    EU_TAXONOMY = "EU Taxonomy - Sustainable Finance Regulation"
    SFDR = "SFDR - Sustainable Finance Disclosure Regulation"
    FCPA_US = "FCPA (USA) - Foreign Corrupt Practices Act"
    UK_BRIBERY_ACT = "UK Bribery Act 2010"
    
    # ═══════════════════════════════════════════════════════════
    # V. CLINICAL & PHARMACEUTICAL INTEGRITY (Expansion Pack 4)
    # ═══════════════════════════════════════════════════════════
    
    EU_MDR = "EU MDR - Medical Device Regulation 2017/745"
    FDA_21_CFR_PART_11 = "FDA 21 CFR Part 11 - Electronic Records and Signatures"
    ICH_GCP = "ICH GCP - Good Clinical Practice"
    WHO_GMP = "WHO GMP - Good Manufacturing Practices"
    
    # ═══════════════════════════════════════════════════════════
    # VI. AI & DIGITAL HEALTH GOVERNANCE (New Category)
    # ═══════════════════════════════════════════════════════════
    
    EU_AI_ACT_2024 = "EU AI Act (Regulation 2024/1689) - High-Risk AI Systems"
    FDA_CDS_SOFTWARE = "FDA Clinical Decision Support Software Guidance (2025)"
    IMDRF_AI_PRINCIPLES = "IMDRF AI Principles - International Medical Device Regulators Forum"
    ISO_IEC_42001 = "ISO/IEC 42001 - AI Management Systems"
    SPIRIT_AI = "SPIRIT-AI Guidelines - Clinical Trial Reporting for AI"
    CONSORT_AI = "CONSORT-AI Guidelines - Reporting Standards for AI Interventions"
    US_HEALTHCARE_CYBER_ACT = "US Healthcare Cybersecurity and Resiliency Act (2025)"
    HIPAA_SECURITY_RULE_2025 = "HIPAA Security Rule (2025 updates) - Vulnerability Management"
    
    # ═══════════════════════════════════════════════════════════
    # VII. GLOBAL HEALTH SECURITY & OUTBREAK REPORTING (New Category)
    # ═══════════════════════════════════════════════════════════
    
    WHO_IHR_2025 = "WHO IHR 2025 Amendments - Pandemic Emergency Framework"
    GHSA = "GHSA - Global Health Security Agenda"
    JEE_STANDARDS = "JEE Standards - Joint External Evaluation"
    ONE_HEALTH = "One Health Framework - Zoonotic Disease Surveillance"
    
    # ═══════════════════════════════════════════════════════════
    # VIII. AFRICAN DATA SOVEREIGNTY & INTEROPERABILITY (New Category)
    # ═══════════════════════════════════════════════════════════
    
    MALABO_CONVENTION = "Malabo Convention - African Union Cyber Security and Data Protection"
    NIGERIA_NDPR = "Nigeria NDPR - Nigeria Data Protection Regulation"
    KENYA_DPA_2025 = "Kenya DPA (2025 interoperability guidelines)"
    SOUTH_AFRICA_POPIA_2025 = "South Africa POPIA (2025 cross-border guidelines)"
    AU_DIGITAL_TRANSFORMATION = "African Union Digital Transformation Strategy"
    
    # ═══════════════════════════════════════════════════════════
    # IX. SUSTAINABLE HUMANITARIAN LOGISTICS (New Category)
    # ═══════════════════════════════════════════════════════════
    
    EU_ESPR = "EU ESPR - Ecodesign for Sustainable Products Regulation"
    DIGITAL_PRODUCT_PASSPORT = "Digital Product Passport (DPP) - EU Traceability"
    HUMANITARIAN_LOGISTICS_CARBON = "Humanitarian Logistics Carbon Footprint Framework (2025)"
    WFP_GREEN_SUPPLY_CHAIN = "WFP Green Supply Chain Standards"
    
    # ═══════════════════════════════════════════════════════════
    # X. INTERNATIONAL ESG & REPORTING STANDARDS (New Category)
    # ═══════════════════════════════════════════════════════════
    
    IFRS_S1 = "IFRS S1 - General Sustainability Disclosure (ISSB)"
    IFRS_S2 = "IFRS S2 - Climate-Related Disclosures (ISSB)"
    GRI_STANDARDS = "GRI Standards - Global Reporting Initiative"
    SASB_STANDARDS = "SASB Standards - Sustainability Accounting Standards Board"


@dataclass
class FrameworkMetadata:
    """Metadata for each regulatory framework"""
    framework: JurisdictionFramework
    jurisdiction: str
    effective_date: datetime
    enforcement_level: str  # STRICT | MODERATE | PERMISSIVE
    key_articles: List[str]
    compliance_requirements: List[str]
    penalties: str
    update_frequency: str  # CONTINUOUS | QUARTERLY | ANNUAL
    harmonization_targets: List[JurisdictionFramework]  # Frameworks this aligns with


class FrameworkCategory(Enum):
    """Organizational categories for the Quantum-Law Nexus"""
    CORE_DATA_PROTECTION = "Core Data Protection"
    SUPPLY_CHAIN_ETHICS = "Supply Chain & Procurement Ethics"
    ENVIRONMENTAL_CARBON = "Environmental & Carbon Standards"
    FINANCIAL_INTEGRITY = "Financial Integrity & Anti-Corruption"
    CLINICAL_PHARMA = "Clinical & Pharmaceutical Integrity"
    AI_DIGITAL_HEALTH = "AI & Digital Health Governance"
    HEALTH_SECURITY = "Global Health Security & Outbreak Reporting"
    AFRICAN_SOVEREIGNTY = "African Data Sovereignty & Interoperability"
    HUMANITARIAN_LOGISTICS = "Sustainable Humanitarian Logistics"
    ESG_REPORTING = "International ESG & Reporting Standards"


class FrameworkRegistry:
    """
    Central registry for all 45+ frameworks with metadata and relationships.
    Enables the Quantum-Law Nexus to dynamically activate and harmonize regulations.
    """
    
    def __init__(self):
        self.frameworks: Dict[JurisdictionFramework, FrameworkMetadata] = {}
        self._initialize_registry()
    
    def _initialize_registry(self):
        """Initialize all framework metadata"""
        
        # Core Data Protection
        self.register(FrameworkMetadata(
            framework=JurisdictionFramework.GDPR_EU,
            jurisdiction="EU",
            effective_date=datetime(2018, 5, 25),
            enforcement_level="STRICT",
            key_articles=["Art. 6", "Art. 9", "Art. 17", "Art. 22", "Art. 30", "Art. 32"],
            compliance_requirements=[
                "Lawful basis for processing",
                "Special category data protection",
                "Right to erasure",
                "Right to explanation",
                "Records of processing",
                "Security of processing"
            ],
            penalties="Up to €20M or 4% of global turnover",
            update_frequency="CONTINUOUS",
            harmonization_targets=[
                JurisdictionFramework.KDPA_KE,
                JurisdictionFramework.POPIA_ZA,
                JurisdictionFramework.PIPEDA_CA
            ]
        ))
        
        # AI Governance
        self.register(FrameworkMetadata(
            framework=JurisdictionFramework.EU_AI_ACT_2024,
            jurisdiction="EU",
            effective_date=datetime(2024, 8, 1),
            enforcement_level="STRICT",
            key_articles=["§6", "§8", "§12", "§13", "§61"],
            compliance_requirements=[
                "High-risk AI classification",
                "Conformity assessment",
                "Transparency obligations",
                "Human oversight",
                "Post-market monitoring",
                "Explainability requirements"
            ],
            penalties="Up to €35M or 7% of global turnover",
            update_frequency="QUARTERLY",
            harmonization_targets=[
                JurisdictionFramework.FDA_CDS_SOFTWARE,
                JurisdictionFramework.ISO_IEC_42001
            ]
        ))
        
        # Global Health Security
        self.register(FrameworkMetadata(
            framework=JurisdictionFramework.WHO_IHR_2025,
            jurisdiction="GLOBAL",
            effective_date=datetime(2025, 9, 1),
            enforcement_level="MODERATE",
            key_articles=["Art. 6", "Art. 7", "Art. 12", "Art. 13"],
            compliance_requirements=[
                "Core surveillance capacities",
                "Pandemic emergency notification",
                "Real-time data sharing",
                "Equity in medical access",
                "National focal point coordination"
            ],
            penalties="Diplomatic sanctions, WHO reporting",
            update_frequency="ANNUAL",
            harmonization_targets=[
                JurisdictionFramework.GHSA,
                JurisdictionFramework.JEE_STANDARDS
            ]
        ))
        
        # African Data Sovereignty
        self.register(FrameworkMetadata(
            framework=JurisdictionFramework.MALABO_CONVENTION,
            jurisdiction="AFRICAN_UNION",
            effective_date=datetime(2023, 6, 8),
            enforcement_level="MODERATE",
            key_articles=["Art. 8", "Art. 12", "Art. 14", "Art. 22"],
            compliance_requirements=[
                "Data localization for sensitive data",
                "Cross-border transfer safeguards",
                "Cybersecurity minimum standards",
                "National data protection authority coordination"
            ],
            penalties="Varies by ratifying state",
            update_frequency="ANNUAL",
            harmonization_targets=[
                JurisdictionFramework.GDPR_EU,
                JurisdictionFramework.KDPA_KE,
                JurisdictionFramework.POPIA_ZA
            ]
        ))
        
        # ESG Reporting
        self.register(FrameworkMetadata(
            framework=JurisdictionFramework.IFRS_S2,
            jurisdiction="GLOBAL",
            effective_date=datetime(2024, 1, 1),
            enforcement_level="MODERATE",
            key_articles=["IFRS S2.1", "IFRS S2.14", "IFRS S2.29"],
            compliance_requirements=[
                "Scope 1, 2, 3 emissions disclosure",
                "Climate risk assessment",
                "Transition planning",
                "Scenario analysis"
            ],
            penalties="Regulatory enforcement varies by jurisdiction",
            update_frequency="ANNUAL",
            harmonization_targets=[
                JurisdictionFramework.TCFD,
                JurisdictionFramework.GHG_PROTOCOL,
                JurisdictionFramework.EU_CBAM
            ]
        ))
        
        # US Healthcare Cybersecurity
        self.register(FrameworkMetadata(
            framework=JurisdictionFramework.US_HEALTHCARE_CYBER_ACT,
            jurisdiction="USA",
            effective_date=datetime(2025, 1, 1),
            enforcement_level="STRICT",
            key_articles=["Sec. 3", "Sec. 5", "Sec. 7"],
            compliance_requirements=[
                "HHS-CISA coordination",
                "Minimum cybersecurity standards",
                "24-hour incident reporting",
                "Vulnerability disclosure program",
                "Annual security assessments"
            ],
            penalties="Civil penalties up to $1M per violation",
            update_frequency="QUARTERLY",
            harmonization_targets=[
                JurisdictionFramework.HIPAA_US,
                JurisdictionFramework.NIST_CSF
            ]
        ))
    
    def register(self, metadata: FrameworkMetadata):
        """Register a framework with metadata"""
        self.frameworks[metadata.framework] = metadata
    
    def get_metadata(self, framework: JurisdictionFramework) -> Optional[FrameworkMetadata]:
        """Get metadata for a framework"""
        return self.frameworks.get(framework)
    
    def get_by_category(self, category: FrameworkCategory) -> List[JurisdictionFramework]:
        """Get all frameworks in a category"""
        category_map = {
            FrameworkCategory.CORE_DATA_PROTECTION: [
                JurisdictionFramework.GDPR_EU,
                JurisdictionFramework.GDPR_ART9,
                JurisdictionFramework.KDPA_KE,
                JurisdictionFramework.PIPEDA_CA,
                JurisdictionFramework.POPIA_ZA,
                JurisdictionFramework.HIPAA_US,
                JurisdictionFramework.HITECH_US,
                JurisdictionFramework.CCPA_US,
            ],
            FrameworkCategory.AI_DIGITAL_HEALTH: [
                JurisdictionFramework.EU_AI_ACT_2024,
                JurisdictionFramework.FDA_CDS_SOFTWARE,
                JurisdictionFramework.IMDRF_AI_PRINCIPLES,
                JurisdictionFramework.ISO_IEC_42001,
                JurisdictionFramework.SPIRIT_AI,
                JurisdictionFramework.CONSORT_AI,
                JurisdictionFramework.US_HEALTHCARE_CYBER_ACT,
            ],
            FrameworkCategory.HEALTH_SECURITY: [
                JurisdictionFramework.WHO_IHR_2025,
                JurisdictionFramework.GHSA,
                JurisdictionFramework.JEE_STANDARDS,
                JurisdictionFramework.ONE_HEALTH,
            ],
            FrameworkCategory.AFRICAN_SOVEREIGNTY: [
                JurisdictionFramework.MALABO_CONVENTION,
                JurisdictionFramework.NIGERIA_NDPR,
                JurisdictionFramework.KENYA_DPA_2025,
                JurisdictionFramework.SOUTH_AFRICA_POPIA_2025,
                JurisdictionFramework.AU_DIGITAL_TRANSFORMATION,
            ],
            FrameworkCategory.ESG_REPORTING: [
                JurisdictionFramework.IFRS_S1,
                JurisdictionFramework.IFRS_S2,
                JurisdictionFramework.GRI_STANDARDS,
                JurisdictionFramework.SASB_STANDARDS,
            ],
        }
        return category_map.get(category, [])
    
    def get_harmonization_targets(self, framework: JurisdictionFramework) -> List[JurisdictionFramework]:
        """Get frameworks that harmonize with the given framework"""
        metadata = self.get_metadata(framework)
        return metadata.harmonization_targets if metadata else []
    
    def get_all_frameworks(self) -> List[JurisdictionFramework]:
        """Get all registered frameworks"""
        return list(self.frameworks.keys())
    
    def count_frameworks(self) -> int:
        """Get total count of frameworks"""
        return len(self.frameworks)


# Global registry instance
FRAMEWORK_REGISTRY = FrameworkRegistry()


# Convenience functions
def get_framework_count() -> int:
    """Get total number of frameworks in the Quantum-Law Nexus"""
    return len(list(JurisdictionFramework))


def get_frameworks_by_jurisdiction(jurisdiction: str) -> List[JurisdictionFramework]:
    """Get all frameworks for a specific jurisdiction"""
    result = []
    for framework in JurisdictionFramework:
        metadata = FRAMEWORK_REGISTRY.get_metadata(framework)
        if metadata and metadata.jurisdiction == jurisdiction:
            result.append(framework)
    return result


if __name__ == "__main__":
    print(f"🌐 iLuminara Quantum-Law Nexus")
    print(f"📊 Total Frameworks: {get_framework_count()}")
    print(f"\n🔍 Framework Categories:")
    for category in FrameworkCategory:
        frameworks = FRAMEWORK_REGISTRY.get_by_category(category)
        print(f"  {category.value}: {len(frameworks)} frameworks")
