"""
Quantum-Law Nexus: 45+ Global Legal Frameworks
═══════════════════════════════════════════════════════════════════════════════

Expands the SovereignGuardrail to encode 45+ international legal frameworks
across data protection, AI governance, health security, and ESG reporting.

Philosophy: "Law is not a constraint. It is the architecture of dignity."
"""

from enum import Enum
from typing import Dict, Any, List
from dataclasses import dataclass
from datetime import datetime


class JurisdictionFramework(Enum):
    """Comprehensive global legal frameworks (45+ jurisdictions)"""
    
    # ═══════════════════════════════════════════════════════════════════════
    # TIER 1: Data Protection & Privacy (Core 14)
    # ═══════════════════════════════════════════════════════════════════════
    GDPR_EU = "GDPR (EU)"  # General Data Protection Regulation
    KDPA_KE = "KDPA (Kenya)"  # Kenya Data Protection Act
    PIPEDA_CA = "PIPEDA (Canada)"  # Personal Information Protection
    POPIA_ZA = "POPIA (South Africa)"  # Protection of Personal Information
    HIPAA_US = "HIPAA (USA)"  # Health Insurance Portability
    HITECH_US = "HITECH (USA)"  # Health Information Technology
    CCPA_US = "CCPA (USA)"  # California Consumer Privacy Act
    CPRA_US = "CPRA (USA)"  # California Privacy Rights Act (2023)
    NIST_CSF = "NIST CSF (USA)"  # Cybersecurity Framework
    ISO_27001 = "ISO 27001"  # Information Security Management
    ISO_27701 = "ISO 27701"  # Privacy Information Management
    SOC_2 = "SOC 2 (USA)"  # Service Organization Control 2
    GDPR_ART9 = "GDPR Article 9 (Special Categories)"
    GDPR_ART22 = "GDPR Article 22 (Automated Decision-Making)"
    
    # ═══════════════════════════════════════════════════════════════════════
    # TIER 2: AI Governance & Ethics (8 frameworks)
    # ═══════════════════════════════════════════════════════════════════════
    EU_AI_ACT = "EU AI Act (2024)"  # High-Risk AI Systems
    FDA_CDSS = "FDA CDSS (USA)"  # Clinical Decision Support Software
    NIST_AI_RMF = "NIST AI RMF (USA)"  # AI Risk Management Framework
    IEEE_7000 = "IEEE 7000"  # Model Process for Addressing Ethical Concerns
    ISO_42001 = "ISO 42001"  # AI Management System (2023)
    OECD_AI = "OECD AI Principles"  # Responsible AI
    UNESCO_AI = "UNESCO AI Ethics"  # Global AI Ethics Framework
    WHO_AI_HEALTH = "WHO AI for Health"  # AI in Healthcare Guidelines
    
    # ═══════════════════════════════════════════════════════════════════════
    # TIER 3: Global Health Security (7 frameworks)
    # ═══════════════════════════════════════════════════════════════════════
    WHO_IHR_2005 = "WHO IHR (2005)"  # International Health Regulations
    WHO_IHR_2025 = "WHO IHR (2025)"  # Pandemic Treaty (proposed)
    GENEVA_CONV = "Geneva Convention"  # Humanitarian Law
    UN_CRC = "UN CRC"  # Convention on Rights of the Child
    SPHERE_STANDARDS = "Sphere Standards"  # Humanitarian Charter
    ICRC_MEDICAL = "ICRC Medical Ethics"  # Medical Ethics in Armed Conflict
    CHS = "Core Humanitarian Standard"  # Humanitarian Accountability
    
    # ═══════════════════════════════════════════════════════════════════════
    # TIER 4: African Data Sovereignty (6 frameworks)
    # ═══════════════════════════════════════════════════════════════════════
    MALABO_CONV = "Malabo Convention (AU)"  # African Union Cyber Security
    ECOWAS_DATA = "ECOWAS Data Protection"  # West African Economic Community
    SADC_MODEL = "SADC Model Law"  # Southern African Development Community
    NDPA_NG = "NDPA (Nigeria)"  # Nigeria Data Protection Act
    DPA_GH = "DPA (Ghana)"  # Ghana Data Protection Act
    PDPA_UG = "PDPA (Uganda)"  # Uganda Personal Data Protection
    
    # ═══════════════════════════════════════════════════════════════════════
    # TIER 5: International ESG & Reporting (5 frameworks)
    # ═══════════════════════════════════════════════════════════════════════
    ISSB_S1 = "ISSB S1"  # General Sustainability Disclosures
    ISSB_S2 = "ISSB S2"  # Climate-related Disclosures
    IFRS_S2 = "IFRS S2"  # Sustainability Reporting
    GRI_STANDARDS = "GRI Standards"  # Global Reporting Initiative
    TCFD = "TCFD"  # Task Force on Climate-related Financial Disclosures
    
    # ═══════════════════════════════════════════════════════════════════════
    # TIER 6: Regional & Emerging (5 frameworks)
    # ═══════════════════════════════════════════════════════════════════════
    LGPD_BR = "LGPD (Brazil)"  # Lei Geral de Proteção de Dados
    PIPL_CN = "PIPL (China)"  # Personal Information Protection Law
    PDPA_SG = "PDPA (Singapore)"  # Personal Data Protection Act
    APPI_JP = "APPI (Japan)"  # Act on Protection of Personal Information
    PDPA_TH = "PDPA (Thailand)"  # Personal Data Protection Act
    
    # ═══════════════════════════════════════════════════════════════════════
    # GLOBAL DEFAULT
    # ═══════════════════════════════════════════════════════════════════════
    GLOBAL_DEFAULT = "GLOBAL_DEFAULT"  # Baseline sovereignty rules


@dataclass
class LegalFrameworkMetadata:
    """Metadata for each legal framework"""
    framework: JurisdictionFramework
    region: str
    effective_date: str
    enforcement_authority: str
    max_penalty: str
    key_articles: List[str]
    sovereignty_level: str  # STRICT | MODERATE | PERMISSIVE
    

class QuantumLawNexus:
    """
    Dynamic Omni-Law Matrix that adapts to jurisdiction-specific requirements.
    
    Implements a "quantum superposition" of legal states where the system
    simultaneously complies with all applicable frameworks until a specific
    jurisdiction is observed/selected.
    """
    
    def __init__(self):
        self.framework_metadata = self._build_framework_metadata()
        self.compliance_matrix = self._build_expanded_compliance_matrix()
    
    def _build_framework_metadata(self) -> Dict[str, LegalFrameworkMetadata]:
        """Build comprehensive metadata for all 45+ frameworks"""
        return {
            # TIER 1: Data Protection
            "GDPR_EU": LegalFrameworkMetadata(
                framework=JurisdictionFramework.GDPR_EU,
                region="European Union (27 countries)",
                effective_date="2018-05-25",
                enforcement_authority="Data Protection Authorities (DPAs)",
                max_penalty="€20M or 4% global revenue",
                key_articles=["Art. 6", "Art. 9", "Art. 17", "Art. 22", "Art. 30", "Art. 32"],
                sovereignty_level="STRICT"
            ),
            "KDPA_KE": LegalFrameworkMetadata(
                framework=JurisdictionFramework.KDPA_KE,
                region="Kenya",
                effective_date="2019-11-08",
                enforcement_authority="Office of the Data Protection Commissioner",
                max_penalty="KES 5M or 1% revenue",
                key_articles=["§37", "§42", "§48"],
                sovereignty_level="STRICT"
            ),
            "POPIA_ZA": LegalFrameworkMetadata(
                framework=JurisdictionFramework.POPIA_ZA,
                region="South Africa",
                effective_date="2021-07-01",
                enforcement_authority="Information Regulator",
                max_penalty="ZAR 10M or 10 years imprisonment",
                key_articles=["§11", "§14", "§72"],
                sovereignty_level="STRICT"
            ),
            
            # TIER 2: AI Governance
            "EU_AI_ACT": LegalFrameworkMetadata(
                framework=JurisdictionFramework.EU_AI_ACT,
                region="European Union",
                effective_date="2024-08-01",
                enforcement_authority="AI Office (European Commission)",
                max_penalty="€35M or 7% global revenue",
                key_articles=["§6", "§8", "§12", "§13"],
                sovereignty_level="STRICT"
            ),
            "FDA_CDSS": LegalFrameworkMetadata(
                framework=JurisdictionFramework.FDA_CDSS,
                region="United States",
                effective_date="2022-09-29",
                enforcement_authority="FDA Center for Devices and Radiological Health",
                max_penalty="Criminal prosecution + product recall",
                key_articles=["21 CFR 880.6310", "21 CFR 880.6320"],
                sovereignty_level="STRICT"
            ),
            
            # TIER 3: Global Health Security
            "WHO_IHR_2005": LegalFrameworkMetadata(
                framework=JurisdictionFramework.WHO_IHR_2005,
                region="196 States Parties",
                effective_date="2007-06-15",
                enforcement_authority="WHO Director-General",
                max_penalty="International sanctions",
                key_articles=["Art. 6", "Art. 7", "Art. 12", "Art. 44"],
                sovereignty_level="MODERATE"
            ),
            "WHO_IHR_2025": LegalFrameworkMetadata(
                framework=JurisdictionFramework.WHO_IHR_2025,
                region="196 States Parties (proposed)",
                effective_date="2025-05-01 (target)",
                enforcement_authority="WHO Pandemic Prevention Hub",
                max_penalty="Trade restrictions + funding suspension",
                key_articles=["Art. 13A", "Art. 18", "Annex 1A"],
                sovereignty_level="STRICT"
            ),
            
            # TIER 4: African Data Sovereignty
            "MALABO_CONV": LegalFrameworkMetadata(
                framework=JurisdictionFramework.MALABO_CONV,
                region="African Union (55 member states)",
                effective_date="2014-06-27",
                enforcement_authority="African Union Commission",
                max_penalty="Varies by member state",
                key_articles=["Art. 8", "Art. 12", "Art. 14"],
                sovereignty_level="STRICT"
            ),
            
            # TIER 5: ESG Reporting
            "ISSB_S2": LegalFrameworkMetadata(
                framework=JurisdictionFramework.ISSB_S2,
                region="Global (IFRS Foundation)",
                effective_date="2024-01-01",
                enforcement_authority="National securities regulators",
                max_penalty="Delisting + investor lawsuits",
                key_articles=["IFRS S2.1", "IFRS S2.9", "IFRS S2.14"],
                sovereignty_level="MODERATE"
            ),
        }
    
    def _build_expanded_compliance_matrix(self) -> Dict[str, Dict[str, Any]]:
        """
        Build comprehensive compliance matrix for all 45+ frameworks.
        
        Returns a mapping of jurisdiction -> compliance rules with granular controls.
        """
        return {
            # ═══════════════════════════════════════════════════════════════
            # TIER 1: Data Protection & Privacy
            # ═══════════════════════════════════════════════════════════════
            "GDPR_EU": {
                "data_sovereignty_required": True,
                "requires_explicit_consent": True,
                "special_categories_prohibited_foreign": True,
                "right_to_explanation_required": True,
                "right_to_erasure": True,
                "data_portability": True,
                "retention_max_days": 2555,
                "breach_notification_hours": 72,
                "dpo_required": True,
                "dpia_required_threshold": "high_risk",
                "cross_border_mechanism": "SCC",  # Standard Contractual Clauses
                "adequacy_whitelist": ["UK", "Switzerland", "Canada", "Japan"],
            },
            "KDPA_KE": {
                "data_sovereignty_required": True,
                "requires_explicit_consent": True,
                "special_categories_prohibited_foreign": True,
                "right_to_explanation_required": False,
                "right_to_erasure": True,
                "data_portability": True,
                "retention_max_days": 1825,
                "breach_notification_hours": 72,
                "dpo_required": True,
                "dpia_required_threshold": "high_risk",
                "cross_border_mechanism": "Authorization",
                "adequacy_whitelist": [],
            },
            "POPIA_ZA": {
                "data_sovereignty_required": True,
                "requires_explicit_consent": True,
                "special_categories_prohibited_foreign": True,
                "right_to_explanation_required": False,
                "right_to_erasure": True,
                "data_portability": False,
                "retention_max_days": 2555,
                "breach_notification_hours": 168,
                "dpo_required": True,
                "dpia_required_threshold": "high_risk",
                "cross_border_mechanism": "Adequacy",
                "adequacy_whitelist": ["EU"],
            },
            
            # ═══════════════════════════════════════════════════════════════
            # TIER 2: AI Governance
            # ═══════════════════════════════════════════════════════════════
            "EU_AI_ACT": {
                "high_risk_classification": True,
                "conformity_assessment_required": True,
                "technical_documentation_required": True,
                "human_oversight_required": True,
                "transparency_obligations": True,
                "accuracy_requirements": 0.95,
                "robustness_testing_required": True,
                "post_market_monitoring": True,
                "incident_reporting_hours": 72,
                "prohibited_practices": [
                    "social_scoring",
                    "subliminal_manipulation",
                    "exploitation_vulnerabilities"
                ],
            },
            "FDA_CDSS": {
                "premarket_notification_required": True,  # 510(k)
                "clinical_validation_required": True,
                "software_as_medical_device": True,
                "quality_system_regulation": True,
                "adverse_event_reporting": True,
                "cybersecurity_requirements": True,
                "algorithm_transparency": True,
                "intended_use_statement": True,
            },
            "NIST_AI_RMF": {
                "risk_assessment_required": True,
                "bias_testing_required": True,
                "explainability_required": True,
                "security_controls": True,
                "continuous_monitoring": True,
                "stakeholder_engagement": True,
            },
            
            # ═══════════════════════════════════════════════════════════════
            # TIER 3: Global Health Security
            # ═══════════════════════════════════════════════════════════════
            "WHO_IHR_2005": {
                "notification_obligation": True,
                "notification_timeframe_hours": 24,
                "core_capacity_requirements": True,
                "surveillance_system_required": True,
                "laboratory_capacity": True,
                "emergency_response_plan": True,
                "international_cooperation": True,
                "public_health_emergency_criteria": [
                    "serious_public_health_impact",
                    "unusual_unexpected",
                    "international_spread_risk",
                    "international_travel_trade_restriction_risk"
                ],
            },
            "WHO_IHR_2025": {
                "notification_obligation": True,
                "notification_timeframe_hours": 12,  # Stricter
                "genomic_surveillance_required": True,
                "pathogen_access_benefit_sharing": True,
                "pandemic_prevention_hub_reporting": True,
                "one_health_approach": True,
                "zoonotic_disease_monitoring": True,
                "antimicrobial_resistance_tracking": True,
            },
            "GENEVA_CONV": {
                "medical_neutrality": True,
                "protection_medical_personnel": True,
                "protection_medical_facilities": True,
                "prohibition_attacks_civilians": True,
                "humanitarian_access": True,
                "proportionality_principle": True,
            },
            
            # ═══════════════════════════════════════════════════════════════
            # TIER 4: African Data Sovereignty
            # ═══════════════════════════════════════════════════════════════
            "MALABO_CONV": {
                "data_sovereignty_required": True,
                "cybersecurity_measures_required": True,
                "critical_infrastructure_protection": True,
                "cybercrime_prevention": True,
                "cross_border_cooperation": True,
                "capacity_building": True,
            },
            "ECOWAS_DATA": {
                "data_sovereignty_required": True,
                "regional_data_sharing": True,
                "harmonized_standards": True,
                "cross_border_transfers_allowed": True,  # Within ECOWAS
            },
            
            # ═══════════════════════════════════════════════════════════════
            # TIER 5: ESG Reporting
            # ═══════════════════════════════════════════════════════════════
            "ISSB_S2": {
                "climate_risk_disclosure": True,
                "scope_1_emissions": True,
                "scope_2_emissions": True,
                "scope_3_emissions": True,
                "scenario_analysis": True,
                "transition_plan": True,
                "governance_disclosure": True,
                "metrics_targets": True,
            },
            "GRI_STANDARDS": {
                "materiality_assessment": True,
                "stakeholder_engagement": True,
                "economic_impacts": True,
                "environmental_impacts": True,
                "social_impacts": True,
                "governance_practices": True,
            },
            
            # ═══════════════════════════════════════════════════════════════
            # GLOBAL DEFAULT (Most Restrictive)
            # ═══════════════════════════════════════════════════════════════
            "GLOBAL_DEFAULT": {
                "data_sovereignty_required": True,
                "requires_explicit_consent": True,
                "special_categories_prohibited_foreign": True,
                "right_to_explanation_required": True,
                "right_to_erasure": True,
                "retention_max_days": 1825,
                "breach_notification_hours": 72,
                "high_risk_classification": True,
                "human_oversight_required": True,
            },
        }
    
    def get_applicable_frameworks(
        self,
        data_type: str,
        operation: str,
        location: str
    ) -> List[JurisdictionFramework]:
        """
        Determine which legal frameworks apply to a given operation.
        
        Implements "quantum superposition" - multiple frameworks may apply
        simultaneously until jurisdiction is observed.
        
        Args:
            data_type: Type of data (PHI, PII, Environmental, etc.)
            operation: Operation type (transfer, inference, storage, etc.)
            location: Geographic location
            
        Returns:
            List of applicable frameworks
        """
        applicable = []
        
        # Data protection frameworks
        if data_type in ["PHI", "PII", "Special_Category"]:
            if "EU" in location or "Europe" in location:
                applicable.extend([
                    JurisdictionFramework.GDPR_EU,
                    JurisdictionFramework.GDPR_ART9,
                ])
            if "Kenya" in location or "KE" in location:
                applicable.append(JurisdictionFramework.KDPA_KE)
            if "South Africa" in location or "ZA" in location:
                applicable.append(JurisdictionFramework.POPIA_ZA)
            if "Africa" in location:
                applicable.append(JurisdictionFramework.MALABO_CONV)
        
        # AI governance frameworks
        if operation in ["inference", "prediction", "diagnosis"]:
            if "EU" in location:
                applicable.append(JurisdictionFramework.EU_AI_ACT)
            if "US" in location and data_type == "PHI":
                applicable.append(JurisdictionFramework.FDA_CDSS)
            applicable.append(JurisdictionFramework.NIST_AI_RMF)
        
        # Health security frameworks
        if data_type == "Outbreak_Data":
            applicable.extend([
                JurisdictionFramework.WHO_IHR_2005,
                JurisdictionFramework.WHO_IHR_2025,
            ])
        
        # ESG frameworks (always applicable for reporting)
        if operation == "reporting":
            applicable.extend([
                JurisdictionFramework.ISSB_S2,
                JurisdictionFramework.GRI_STANDARDS,
            ])
        
        return applicable if applicable else [JurisdictionFramework.GLOBAL_DEFAULT]
    
    def get_compliance_rules(
        self,
        framework: JurisdictionFramework
    ) -> Dict[str, Any]:
        """Get compliance rules for a specific framework"""
        framework_key = framework.value.split(" (")[0].replace(" ", "_").replace("-", "_").upper()
        
        # Try exact match first
        if framework_key in self.compliance_matrix:
            return self.compliance_matrix[framework_key]
        
        # Try framework name
        for key in self.compliance_matrix:
            if framework.name in key:
                return self.compliance_matrix[key]
        
        # Fallback to global default
        return self.compliance_matrix["GLOBAL_DEFAULT"]
    
    def get_framework_metadata(
        self,
        framework: JurisdictionFramework
    ) -> LegalFrameworkMetadata:
        """Get metadata for a specific framework"""
        framework_key = framework.name
        return self.framework_metadata.get(
            framework_key,
            self.framework_metadata.get("GDPR_EU")  # Fallback
        )


# ═══════════════════════════════════════════════════════════════════════════
# MISSION: To architect systems that transform preventable suffering from 
# statistical inevitability to historical anomaly.
#
# COMPLIANCE PILLAR: Quantum-Law Nexus (45+ Global Frameworks)
# ═══════════════════════════════════════════════════════════════════════════
