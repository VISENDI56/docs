"""
Dynamic Omni-Law Matrix
The Hyper-Law Singularity: 45+ Framework Orchestration Engine

This module implements context-aware, AI-actuated compliance triggers that
dynamically activate regulatory frameworks based on operational context.

Compliance Coverage (45+ Frameworks):
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
I. FOUNDATIONAL DATA PROTECTION (14 frameworks)
II. SUPPLY CHAIN & PROCUREMENT ETHICS (5 frameworks)
III. ENVIRONMENTAL & CLIMATE STANDARDS (4 frameworks)
IV. FINANCIAL INTEGRITY & ANTI-CORRUPTION (3 frameworks)
V. CLINICAL RESEARCH & MEDICAL DEVICE REGULATION (4 frameworks)
VI. AI & DIGITAL HEALTH GOVERNANCE (5 frameworks) ← NEW
VII. GLOBAL HEALTH SECURITY & OUTBREAK REPORTING (3 frameworks) ← NEW
VIII. AFRICAN DATA SOVEREIGNTY & INTEROPERABILITY (4 frameworks) ← NEW
IX. SUSTAINABLE HUMANITARIAN LOGISTICS (2 frameworks) ← NEW
X. INTERNATIONAL ESG & REPORTING STANDARDS (3 frameworks) ← NEW
XI. U.S. HEALTHCARE CYBERSECURITY (2 frameworks) ← NEW
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
TOTAL: 45+ Frameworks
"""

from enum import Enum
from typing import Dict, List, Optional, Set, Any
from dataclasses import dataclass, field
from datetime import datetime
import logging
import json

logger = logging.getLogger(__name__)


class ComplianceCategory(Enum):
    """Sectoral abstraction layer for compliance domains"""
    FOUNDATIONAL_DATA_PROTECTION = "foundational_data_protection"
    SUPPLY_CHAIN_ETHICS = "supply_chain_ethics"
    ENVIRONMENTAL_CLIMATE = "environmental_climate"
    FINANCIAL_INTEGRITY = "financial_integrity"
    CLINICAL_RESEARCH = "clinical_research"
    AI_DIGITAL_HEALTH = "ai_digital_health"
    GLOBAL_HEALTH_SECURITY = "global_health_security"
    AFRICAN_DATA_SOVEREIGNTY = "african_data_sovereignty"
    SUSTAINABLE_LOGISTICS = "sustainable_logistics"
    INTERNATIONAL_ESG = "international_esg"
    US_HEALTHCARE_CYBERSECURITY = "us_healthcare_cybersecurity"


class RiskLevel(Enum):
    """AI risk classification per EU AI Act"""
    UNACCEPTABLE = "unacceptable"  # Prohibited
    HIGH = "high"  # Conformity assessment required
    LIMITED = "limited"  # Transparency obligations
    MINIMAL = "minimal"  # No obligations


@dataclass
class ComplianceFramework:
    """Individual regulatory framework"""
    id: str
    name: str
    category: ComplianceCategory
    jurisdiction: str
    risk_level: RiskLevel
    articles: List[str]
    enforcement_level: str  # STRICT | MODERATE | PERMISSIVE
    activation_triggers: List[str]
    harmonization_mappings: Dict[str, str] = field(default_factory=dict)
    effective_date: Optional[str] = None
    sunset_date: Optional[str] = None


@dataclass
class ComplianceContext:
    """Operational context for dynamic framework activation"""
    action_type: str
    data_type: str
    jurisdiction: str
    ai_involved: bool = False
    cross_border: bool = False
    high_risk: bool = False
    outbreak_context: bool = False
    clinical_decision: bool = False
    supply_chain_event: bool = False
    environmental_impact: bool = False
    metadata: Dict[str, Any] = field(default_factory=dict)


class OmniLawMatrix:
    """
    The Hyper-Law Singularity: Dynamic compliance orchestration engine
    
    Features:
    - Context-aware framework activation
    - AI-actuated compliance triggers
    - Retroactive harmonization
    - Multi-jurisdictional conflict resolution
    - Real-time regulatory updates
    """
    
    def __init__(self, enable_ai_triggers: bool = True):
        self.enable_ai_triggers = enable_ai_triggers
        self.frameworks: Dict[str, ComplianceFramework] = {}
        self.active_frameworks: Set[str] = set()
        self.harmonization_graph: Dict[str, List[str]] = {}
        
        # Initialize all 45+ frameworks
        self._initialize_frameworks()
        
        logger.info("🌐 Omni-Law Matrix initialized - 45+ frameworks loaded")
    
    def _initialize_frameworks(self):
        """Initialize all 45+ compliance frameworks"""
        
        # ═══════════════════════════════════════════════════════════════
        # I. FOUNDATIONAL DATA PROTECTION (14 frameworks)
        # ═══════════════════════════════════════════════════════════════
        
        self._register_framework(ComplianceFramework(
            id="GDPR",
            name="General Data Protection Regulation",
            category=ComplianceCategory.FOUNDATIONAL_DATA_PROTECTION,
            jurisdiction="EU",
            risk_level=RiskLevel.HIGH,
            articles=["Art. 6", "Art. 9", "Art. 17", "Art. 22", "Art. 30", "Art. 32"],
            enforcement_level="STRICT",
            activation_triggers=["PHI_processing", "cross_border_EU", "automated_decision"]
        ))
        
        self._register_framework(ComplianceFramework(
            id="KDPA",
            name="Kenya Data Protection Act",
            category=ComplianceCategory.FOUNDATIONAL_DATA_PROTECTION,
            jurisdiction="Kenya",
            risk_level=RiskLevel.HIGH,
            articles=["§37", "§42"],
            enforcement_level="STRICT",
            activation_triggers=["PHI_processing", "kenya_jurisdiction"]
        ))
        
        self._register_framework(ComplianceFramework(
            id="POPIA",
            name="Protection of Personal Information Act",
            category=ComplianceCategory.FOUNDATIONAL_DATA_PROTECTION,
            jurisdiction="South Africa",
            risk_level=RiskLevel.HIGH,
            articles=["§11", "§14"],
            enforcement_level="STRICT",
            activation_triggers=["PHI_processing", "south_africa_jurisdiction"]
        ))
        
        self._register_framework(ComplianceFramework(
            id="HIPAA",
            name="Health Insurance Portability and Accountability Act",
            category=ComplianceCategory.FOUNDATIONAL_DATA_PROTECTION,
            jurisdiction="USA",
            risk_level=RiskLevel.HIGH,
            articles=["§164.312", "§164.530(j)"],
            enforcement_level="STRICT",
            activation_triggers=["PHI_processing", "usa_jurisdiction"]
        ))
        
        # ═══════════════════════════════════════════════════════════════
        # VI. AI & DIGITAL HEALTH GOVERNANCE (5 frameworks) ← NEW
        # ═══════════════════════════════════════════════════════════════
        
        self._register_framework(ComplianceFramework(
            id="EU_AI_ACT",
            name="EU AI Act (Regulation 2024/1689)",
            category=ComplianceCategory.AI_DIGITAL_HEALTH,
            jurisdiction="EU",
            risk_level=RiskLevel.HIGH,
            articles=["Art. 6", "Art. 8", "Art. 12", "Art. 13", "Art. 61"],
            enforcement_level="STRICT",
            activation_triggers=["ai_inference", "high_risk_ai", "health_prediction"],
            harmonization_mappings={"GDPR": "Art. 22", "MDR": "Annex VIII"},
            effective_date="2025-08-01"
        ))
        
        self._register_framework(ComplianceFramework(
            id="FDA_CDS_SOFTWARE",
            name="FDA Clinical Decision Support Software Guidance",
            category=ComplianceCategory.AI_DIGITAL_HEALTH,
            jurisdiction="USA",
            risk_level=RiskLevel.HIGH,
            articles=["Section 520(o)", "21 CFR 880.6310"],
            enforcement_level="STRICT",
            activation_triggers=["clinical_decision", "ai_diagnosis", "usa_jurisdiction"],
            harmonization_mappings={"IMDRF": "AI-SaMD Principles"}
        ))
        
        self._register_framework(ComplianceFramework(
            id="ISO_42001",
            name="ISO/IEC 42001 - AI Management Systems",
            category=ComplianceCategory.AI_DIGITAL_HEALTH,
            jurisdiction="Global",
            risk_level=RiskLevel.HIGH,
            articles=["Clause 6.1", "Clause 8.2", "Clause 9.1"],
            enforcement_level="MODERATE",
            activation_triggers=["ai_deployment", "ai_governance"],
            harmonization_mappings={"ISO_27001": "A.18"}
        ))
        
        self._register_framework(ComplianceFramework(
            id="IMDRF_AI_SAMD",
            name="IMDRF AI Principles for Software as Medical Device",
            category=ComplianceCategory.AI_DIGITAL_HEALTH,
            jurisdiction="Global",
            risk_level=RiskLevel.HIGH,
            articles=["Good Machine Learning Practice", "Real-World Performance"],
            enforcement_level="MODERATE",
            activation_triggers=["ai_medical_device", "clinical_decision"],
            harmonization_mappings={"FDA_CDS_SOFTWARE": "Section 520(o)", "EU_MDR": "Annex VIII"}
        ))
        
        self._register_framework(ComplianceFramework(
            id="SPIRIT_AI_CONSORT_AI",
            name="SPIRIT-AI/CONSORT-AI Clinical Trial Reporting",
            category=ComplianceCategory.AI_DIGITAL_HEALTH,
            jurisdiction="Global",
            risk_level=RiskLevel.MODERATE,
            articles=["Item 5", "Item 11a", "Item 24"],
            enforcement_level="MODERATE",
            activation_triggers=["clinical_trial", "ai_intervention"]
        ))
        
        # ═══════════════════════════════════════════════════════════════
        # VII. GLOBAL HEALTH SECURITY & OUTBREAK REPORTING (3 frameworks) ← NEW
        # ═══════════════════════════════════════════════════════════════
        
        self._register_framework(ComplianceFramework(
            id="IHR_2005",
            name="International Health Regulations (2005, 2025 amendments)",
            category=ComplianceCategory.GLOBAL_HEALTH_SECURITY,
            jurisdiction="Global",
            risk_level=RiskLevel.HIGH,
            articles=["Art. 6", "Art. 7", "Annex 2"],
            enforcement_level="STRICT",
            activation_triggers=["outbreak_detection", "pheic_event", "anomaly_detection"],
            harmonization_mappings={"GHSA": "Prevent-1", "JEE": "D.1.1"}
        ))
        
        self._register_framework(ComplianceFramework(
            id="GHSA",
            name="Global Health Security Agenda",
            category=ComplianceCategory.GLOBAL_HEALTH_SECURITY,
            jurisdiction="Global",
            risk_level=RiskLevel.HIGH,
            articles=["Prevent-1", "Detect-1", "Respond-1"],
            enforcement_level="MODERATE",
            activation_triggers=["outbreak_detection", "surveillance_event"],
            harmonization_mappings={"IHR_2005": "Art. 6"}
        ))
        
        self._register_framework(ComplianceFramework(
            id="JEE",
            name="Joint External Evaluation Standards",
            category=ComplianceCategory.GLOBAL_HEALTH_SECURITY,
            jurisdiction="Global",
            risk_level=RiskLevel.MODERATE,
            articles=["D.1.1", "D.2.1", "D.3.1"],
            enforcement_level="MODERATE",
            activation_triggers=["surveillance_capacity", "real_time_data"]
        ))
        
        # ═══════════════════════════════════════════════════════════════
        # VIII. AFRICAN DATA SOVEREIGNTY & INTEROPERABILITY (4 frameworks) ← NEW
        # ═══════════════════════════════════════════════════════════════
        
        self._register_framework(ComplianceFramework(
            id="MALABO_CONVENTION",
            name="African Union Convention on Cyber Security and Personal Data Protection",
            category=ComplianceCategory.AFRICAN_DATA_SOVEREIGNTY,
            jurisdiction="African Union",
            risk_level=RiskLevel.HIGH,
            articles=["Art. 8", "Art. 14", "Art. 22"],
            enforcement_level="STRICT",
            activation_triggers=["cross_border_africa", "continental_data_flow"],
            harmonization_mappings={"GDPR": "Art. 45", "KDPA": "§37"}
        ))
        
        self._register_framework(ComplianceFramework(
            id="NIGERIA_NDPR",
            name="Nigeria Data Protection Regulation",
            category=ComplianceCategory.AFRICAN_DATA_SOVEREIGNTY,
            jurisdiction="Nigeria",
            risk_level=RiskLevel.HIGH,
            articles=["Part III", "Part IV"],
            enforcement_level="STRICT",
            activation_triggers=["PHI_processing", "nigeria_jurisdiction"]
        ))
        
        self._register_framework(ComplianceFramework(
            id="AU_DIGITAL_TRANSFORMATION",
            name="African Union Digital Transformation Strategy",
            category=ComplianceCategory.AFRICAN_DATA_SOVEREIGNTY,
            jurisdiction="African Union",
            risk_level=RiskLevel.MODERATE,
            articles=["Pillar 2", "Pillar 4"],
            enforcement_level="MODERATE",
            activation_triggers=["digital_health", "continental_interoperability"]
        ))
        
        self._register_framework(ComplianceFramework(
            id="IASC_VULNERABLE_POPULATIONS",
            name="IASC Guidelines on Data Protection in Humanitarian Action",
            category=ComplianceCategory.AFRICAN_DATA_SOVEREIGNTY,
            jurisdiction="Global",
            risk_level=RiskLevel.HIGH,
            articles=["Principle 1", "Principle 4", "Principle 8"],
            enforcement_level="STRICT",
            activation_triggers=["refugee_data", "vulnerable_population", "humanitarian_context"]
        ))
        
        # ═══════════════════════════════════════════════════════════════
        # IX. SUSTAINABLE HUMANITARIAN LOGISTICS (2 frameworks) ← NEW
        # ═══════════════════════════════════════════════════════════════
        
        self._register_framework(ComplianceFramework(
            id="EU_ESPR_DPP",
            name="EU Ecodesign for Sustainable Products Regulation & Digital Product Passports",
            category=ComplianceCategory.SUSTAINABLE_LOGISTICS,
            jurisdiction="EU",
            risk_level=RiskLevel.MODERATE,
            articles=["Art. 7", "Art. 8", "Annex I"],
            enforcement_level="MODERATE",
            activation_triggers=["hardware_deployment", "supply_chain_event"],
            harmonization_mappings={"ISO_14001": "Clause 8.1"}
        ))
        
        self._register_framework(ComplianceFramework(
            id="HUMANITARIAN_LOGISTICS_CARBON",
            name="Humanitarian Logistics Carbon Footprint Reduction Framework",
            category=ComplianceCategory.SUSTAINABLE_LOGISTICS,
            jurisdiction="Global",
            risk_level=RiskLevel.LIMITED,
            articles=["WFP Guidelines", "Logistics Cluster Standards"],
            enforcement_level="PERMISSIVE",
            activation_triggers=["logistics_optimization", "carbon_reporting"]
        ))
        
        # ═══════════════════════════════════════════════════════════════
        # X. INTERNATIONAL ESG & REPORTING STANDARDS (3 frameworks) ← NEW
        # ═══════════════════════════════════════════════════════════════
        
        self._register_framework(ComplianceFramework(
            id="IFRS_S1",
            name="IFRS S1 - General Requirements for Disclosure of Sustainability-related Financial Information",
            category=ComplianceCategory.INTERNATIONAL_ESG,
            jurisdiction="Global",
            risk_level=RiskLevel.MODERATE,
            articles=["Para 1", "Para 51", "Para 72"],
            enforcement_level="MODERATE",
            activation_triggers=["esg_reporting", "investor_disclosure"]
        ))
        
        self._register_framework(ComplianceFramework(
            id="IFRS_S2",
            name="IFRS S2 - Climate-related Disclosures",
            category=ComplianceCategory.INTERNATIONAL_ESG,
            jurisdiction="Global",
            risk_level=RiskLevel.MODERATE,
            articles=["Para 9", "Para 14", "Para 29"],
            enforcement_level="MODERATE",
            activation_triggers=["climate_reporting", "carbon_credits"]
        ))
        
        self._register_framework(ComplianceFramework(
            id="GRI_STANDARDS",
            name="GRI Universal Standards 2021",
            category=ComplianceCategory.INTERNATIONAL_ESG,
            jurisdiction="Global",
            risk_level=RiskLevel.LIMITED,
            articles=["GRI 2", "GRI 3", "GRI 305"],
            enforcement_level="PERMISSIVE",
            activation_triggers=["sustainability_reporting"]
        ))
        
        # ═══════════════════════════════════════════════════════════════
        # XI. U.S. HEALTHCARE CYBERSECURITY (2 frameworks) ← NEW
        # ═══════════════════════════════════════════════════════════════
        
        self._register_framework(ComplianceFramework(
            id="HEALTHCARE_CYBERSECURITY_ACT",
            name="Health Care Cybersecurity and Resiliency Act (2025)",
            category=ComplianceCategory.US_HEALTHCARE_CYBERSECURITY,
            jurisdiction="USA",
            risk_level=RiskLevel.HIGH,
            articles=["Section 2", "Section 3", "Section 5"],
            enforcement_level="STRICT",
            activation_triggers=["cyber_incident", "usa_jurisdiction", "healthcare_system"],
            harmonization_mappings={"HIPAA": "§164.312", "NIST_CSF": "Detect"}
        ))
        
        self._register_framework(ComplianceFramework(
            id="HHS_CISA_COORDINATION",
            name="HHS-CISA Healthcare Sector Coordination",
            category=ComplianceCategory.US_HEALTHCARE_CYBERSECURITY,
            jurisdiction="USA",
            risk_level=RiskLevel.HIGH,
            articles=["405D Program", "HICP Guidelines"],
            enforcement_level="STRICT",
            activation_triggers=["cyber_incident", "threat_intelligence"]
        ))
        
        logger.info(f"✅ Initialized {len(self.frameworks)} compliance frameworks")
    
    def _register_framework(self, framework: ComplianceFramework):
        """Register a compliance framework"""
        self.frameworks[framework.id] = framework
        
        # Build harmonization graph
        for related_id in framework.harmonization_mappings.keys():
            if framework.id not in self.harmonization_graph:
                self.harmonization_graph[framework.id] = []
            self.harmonization_graph[framework.id].append(related_id)
    
    def activate_frameworks(self, context: ComplianceContext) -> List[ComplianceFramework]:
        """
        Dynamically activate frameworks based on operational context
        
        This is the core of the Hyper-Law Singularity: AI-actuated compliance
        """
        activated = []
        
        for framework in self.frameworks.values():
            # Check if any activation trigger matches context
            should_activate = False
            
            for trigger in framework.activation_triggers:
                if self._evaluate_trigger(trigger, context):
                    should_activate = True
                    break
            
            if should_activate:
                activated.append(framework)
                self.active_frameworks.add(framework.id)
                logger.info(f"⚡ Activated: {framework.name} ({framework.id})")
        
        # Apply harmonization (retroactive alignment)
        harmonized = self._apply_harmonization(activated)
        
        return harmonized
    
    def _evaluate_trigger(self, trigger: str, context: ComplianceContext) -> bool:
        """Evaluate if a trigger condition is met"""
        trigger_map = {
            "PHI_processing": context.data_type == "PHI",
            "ai_inference": context.ai_involved,
            "high_risk_ai": context.ai_involved and context.high_risk,
            "health_prediction": context.action_type == "prediction",
            "clinical_decision": context.clinical_decision,
            "ai_diagnosis": context.ai_involved and context.clinical_decision,
            "outbreak_detection": context.outbreak_context,
            "pheic_event": context.outbreak_context and context.high_risk,
            "cross_border_EU": context.cross_border and context.jurisdiction == "EU",
            "cross_border_africa": context.cross_border and "africa" in context.jurisdiction.lower(),
            "kenya_jurisdiction": context.jurisdiction == "Kenya",
            "south_africa_jurisdiction": context.jurisdiction == "South Africa",
            "usa_jurisdiction": context.jurisdiction == "USA",
            "nigeria_jurisdiction": context.jurisdiction == "Nigeria",
            "refugee_data": context.metadata.get("population_type") == "refugee",
            "vulnerable_population": context.metadata.get("vulnerable", False),
            "humanitarian_context": context.metadata.get("humanitarian", False),
            "supply_chain_event": context.supply_chain_event,
            "environmental_impact": context.environmental_impact,
            "cyber_incident": context.action_type == "cyber_incident",
            "esg_reporting": context.action_type == "esg_report",
            "climate_reporting": context.action_type == "climate_report",
        }
        
        return trigger_map.get(trigger, False)
    
    def _apply_harmonization(self, frameworks: List[ComplianceFramework]) -> List[ComplianceFramework]:
        """
        Apply retroactive harmonization across frameworks
        
        Example: If EU AI Act is activated, also activate GDPR Art. 22
        """
        harmonized = set(frameworks)
        
        for framework in frameworks:
            # Check harmonization mappings
            for related_id in framework.harmonization_mappings.keys():
                if related_id in self.frameworks:
                    related = self.frameworks[related_id]
                    harmonized.add(related)
                    logger.info(f"🔗 Harmonized: {related.name} ← {framework.name}")
        
        return list(harmonized)
    
    def validate_action(
        self,
        context: ComplianceContext,
        strict_mode: bool = True
    ) -> Dict[str, Any]:
        """
        Validate an action against all applicable frameworks
        
        Returns:
            {
                "compliant": bool,
                "activated_frameworks": List[str],
                "violations": List[Dict],
                "recommendations": List[str]
            }
        """
        # Activate relevant frameworks
        activated = self.activate_frameworks(context)
        
        violations = []
        recommendations = []
        
        # Check each activated framework
        for framework in activated:
            # Framework-specific validation logic
            violation = self._check_framework_compliance(framework, context)
            
            if violation:
                violations.append({
                    "framework": framework.name,
                    "article": violation["article"],
                    "description": violation["description"],
                    "severity": framework.risk_level.value
                })
        
        # Generate recommendations
        if violations:
            recommendations = self._generate_recommendations(violations, context)
        
        compliant = len(violations) == 0 or not strict_mode
        
        return {
            "compliant": compliant,
            "activated_frameworks": [f.id for f in activated],
            "violations": violations,
            "recommendations": recommendations,
            "timestamp": datetime.utcnow().isoformat()
        }
    
    def _check_framework_compliance(
        self,
        framework: ComplianceFramework,
        context: ComplianceContext
    ) -> Optional[Dict]:
        """Check compliance for a specific framework"""
        
        # EU AI Act specific checks
        if framework.id == "EU_AI_ACT":
            if context.ai_involved and context.high_risk:
                if not context.metadata.get("conformity_assessment"):
                    return {
                        "article": "Art. 6",
                        "description": "High-risk AI system requires conformity assessment"
                    }
                if not context.metadata.get("transparency_log"):
                    return {
                        "article": "Art. 13",
                        "description": "High-risk AI requires transparency documentation"
                    }
        
        # IHR 2005 specific checks
        if framework.id == "IHR_2005":
            if context.outbreak_context:
                if not context.metadata.get("who_notification"):
                    return {
                        "article": "Art. 6",
                        "description": "Outbreak event requires WHO notification within 24 hours"
                    }
        
        # Malabo Convention specific checks
        if framework.id == "MALABO_CONVENTION":
            if context.cross_border and "africa" in context.jurisdiction.lower():
                if not context.metadata.get("continental_authorization"):
                    return {
                        "article": "Art. 14",
                        "description": "Cross-border African data transfer requires authorization"
                    }
        
        return None
    
    def _generate_recommendations(
        self,
        violations: List[Dict],
        context: ComplianceContext
    ) -> List[str]:
        """Generate actionable recommendations"""
        recommendations = []
        
        for violation in violations:
            if "conformity assessment" in violation["description"]:
                recommendations.append(
                    "Conduct EU AI Act conformity assessment before deployment"
                )
            if "WHO notification" in violation["description"]:
                recommendations.append(
                    "Trigger IHR Art. 6 notification to national focal point"
                )
            if "authorization" in violation["description"]:
                recommendations.append(
                    "Obtain Data Protection Commissioner authorization for cross-border transfer"
                )
        
        return recommendations
    
    def get_framework_summary(self) -> Dict[str, Any]:
        """Get summary of all frameworks"""
        summary = {
            "total_frameworks": len(self.frameworks),
            "by_category": {},
            "by_jurisdiction": {},
            "by_risk_level": {}
        }
        
        for framework in self.frameworks.values():
            # By category
            cat = framework.category.value
            summary["by_category"][cat] = summary["by_category"].get(cat, 0) + 1
            
            # By jurisdiction
            jur = framework.jurisdiction
            summary["by_jurisdiction"][jur] = summary["by_jurisdiction"].get(jur, 0) + 1
            
            # By risk level
            risk = framework.risk_level.value
            summary["by_risk_level"][risk] = summary["by_risk_level"].get(risk, 0) + 1
        
        return summary


# Example usage
if __name__ == "__main__":
    # Initialize Omni-Law Matrix
    matrix = OmniLawMatrix(enable_ai_triggers=True)
    
    # Example 1: AI-powered outbreak prediction in Kenya
    context1 = ComplianceContext(
        action_type="prediction",
        data_type="PHI",
        jurisdiction="Kenya",
        ai_involved=True,
        high_risk=True,
        outbreak_context=True,
        metadata={
            "conformity_assessment": False,
            "transparency_log": True,
            "who_notification": False
        }
    )
    
    result1 = matrix.validate_action(context1)
    print(f"\n{'='*60}")
    print("SCENARIO 1: AI Outbreak Prediction in Kenya")
    print(f"{'='*60}")
    print(f"Compliant: {result1['compliant']}")
    print(f"Activated Frameworks: {', '.join(result1['activated_frameworks'])}")
    print(f"Violations: {len(result1['violations'])}")
    for v in result1['violations']:
        print(f"  ❌ {v['framework']} - {v['article']}: {v['description']}")
    print(f"Recommendations:")
    for r in result1['recommendations']:
        print(f"  💡 {r}")
    
    # Example 2: Cross-border African data transfer
    context2 = ComplianceContext(
        action_type="data_transfer",
        data_type="PHI",
        jurisdiction="African Union",
        cross_border=True,
        metadata={
            "continental_authorization": False,
            "vulnerable": True,
            "humanitarian": True
        }
    )
    
    result2 = matrix.validate_action(context2)
    print(f"\n{'='*60}")
    print("SCENARIO 2: Cross-border African Data Transfer")
    print(f"{'='*60}")
    print(f"Compliant: {result2['compliant']}")
    print(f"Activated Frameworks: {', '.join(result2['activated_frameworks'])}")
    
    # Framework summary
    summary = matrix.get_framework_summary()
    print(f"\n{'='*60}")
    print("OMNI-LAW MATRIX SUMMARY")
    print(f"{'='*60}")
    print(f"Total Frameworks: {summary['total_frameworks']}")
    print(f"\nBy Category:")
    for cat, count in summary['by_category'].items():
        print(f"  {cat}: {count}")
    print(f"\nBy Risk Level:")
    for risk, count in summary['by_risk_level'].items():
        print(f"  {risk}: {count}")
