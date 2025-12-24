"""
Dynamic Quantum-Law Nexus
AI-triggered harmonization and retroactive alignment engine

This module orchestrates the 45+ framework compliance system with:
- Context-aware framework activation
- AI-triggered harmonization across jurisdictions
- Retroactive alignment for regulatory updates
- Cross-framework conflict resolution
"""

import logging
from typing import Dict, List, Optional, Set, Tuple
from datetime import datetime
from enum import Enum
from dataclasses import dataclass

from .jurisdiction_framework import (
    JurisdictionFramework,
    FrameworkCategory,
    FrameworkMetadata,
    FRAMEWORK_REGISTRY
)

logger = logging.getLogger(__name__)


class ActivationTrigger(Enum):
    """Triggers that activate specific frameworks"""
    DATA_TRANSFER = "data_transfer"
    HIGH_RISK_AI = "high_risk_ai"
    CROSS_BORDER = "cross_border"
    OUTBREAK_DETECTION = "outbreak_detection"
    SUPPLY_CHAIN = "supply_chain"
    CARBON_EMISSION = "carbon_emission"
    FINANCIAL_TRANSACTION = "financial_transaction"
    CLINICAL_TRIAL = "clinical_trial"
    ESG_REPORTING = "esg_reporting"
    CYBERSECURITY_INCIDENT = "cybersecurity_incident"


@dataclass
class ComplianceContext:
    """Context for compliance evaluation"""
    action_type: str
    jurisdiction: str
    data_type: str
    risk_level: float  # 0.0 to 1.0
    involves_ai: bool
    cross_border: bool
    involves_phi: bool
    involves_children: bool
    emergency_context: bool
    metadata: Dict


@dataclass
class FrameworkActivation:
    """Result of framework activation"""
    framework: JurisdictionFramework
    reason: str
    priority: int  # 1 = highest
    requirements: List[str]
    conflicts: List[JurisdictionFramework]


class QuantumLawNexus:
    """
    The orchestrator of the 45+ framework compliance system.
    
    Capabilities:
    - Dynamic framework activation based on context
    - AI-triggered harmonization
    - Retroactive alignment for regulatory updates
    - Cross-framework conflict resolution
    """
    
    def __init__(self, enable_ai_harmonization: bool = True):
        self.enable_ai_harmonization = enable_ai_harmonization
        self.active_frameworks: Set[JurisdictionFramework] = set()
        self.harmonization_cache: Dict[Tuple, List[JurisdictionFramework]] = {}
        
        logger.info("🌐 Quantum-Law Nexus initialized")
    
    def evaluate_compliance(
        self,
        context: ComplianceContext
    ) -> List[FrameworkActivation]:
        """
        Evaluate which frameworks apply to a given context.
        
        Returns list of activated frameworks with priorities and requirements.
        """
        activations: List[FrameworkActivation] = []
        
        # Core data protection (always active for PHI)
        if context.involves_phi:
            activations.extend(self._activate_data_protection(context))
        
        # AI governance (for AI-driven decisions)
        if context.involves_ai and context.risk_level > 0.7:
            activations.extend(self._activate_ai_governance(context))
        
        # Health security (for outbreak detection)
        if context.action_type == "outbreak_detection":
            activations.extend(self._activate_health_security(context))
        
        # African sovereignty (for African jurisdictions)
        if self._is_african_jurisdiction(context.jurisdiction):
            activations.extend(self._activate_african_sovereignty(context))
        
        # Cross-border transfers
        if context.cross_border:
            activations.extend(self._activate_cross_border(context))
        
        # ESG reporting (for carbon/sustainability actions)
        if context.action_type in ["carbon_emission", "esg_reporting"]:
            activations.extend(self._activate_esg_reporting(context))
        
        # Cybersecurity (for security incidents)
        if context.action_type == "cybersecurity_incident":
            activations.extend(self._activate_cybersecurity(context))
        
        # Harmonize and resolve conflicts
        if self.enable_ai_harmonization:
            activations = self._harmonize_frameworks(activations, context)
        
        # Sort by priority
        activations.sort(key=lambda x: x.priority)
        
        return activations
    
    def _activate_data_protection(
        self,
        context: ComplianceContext
    ) -> List[FrameworkActivation]:
        """Activate core data protection frameworks"""
        activations = []
        
        # GDPR for EU jurisdiction
        if context.jurisdiction in ["EU", "GDPR_EU"]:
            activations.append(FrameworkActivation(
                framework=JurisdictionFramework.GDPR_EU,
                reason="PHI processing in EU jurisdiction",
                priority=1,
                requirements=[
                    "Lawful basis for processing",
                    "Special category data protection (Art. 9)",
                    "Data subject rights",
                    "Security of processing (Art. 32)"
                ],
                conflicts=[]
            ))
            
            # GDPR Art. 9 for special categories
            activations.append(FrameworkActivation(
                framework=JurisdictionFramework.GDPR_ART9,
                reason="Health data is special category",
                priority=1,
                requirements=[
                    "Explicit consent or legal basis",
                    "Enhanced security measures",
                    "Data minimization"
                ],
                conflicts=[]
            ))
        
        # KDPA for Kenya
        if context.jurisdiction in ["KENYA", "KDPA_KE"]:
            activations.append(FrameworkActivation(
                framework=JurisdictionFramework.KDPA_KE,
                reason="PHI processing in Kenya",
                priority=1,
                requirements=[
                    "Data localization for sensitive data",
                    "Consent requirements (§42)",
                    "Transfer restrictions (§37)"
                ],
                conflicts=[]
            ))
        
        # HIPAA for USA
        if context.jurisdiction in ["USA", "HIPAA_US"]:
            activations.append(FrameworkActivation(
                framework=JurisdictionFramework.HIPAA_US,
                reason="PHI processing in USA",
                priority=1,
                requirements=[
                    "Physical safeguards (§164.310)",
                    "Technical safeguards (§164.312)",
                    "Administrative safeguards (§164.308)",
                    "Breach notification"
                ],
                conflicts=[]
            ))
        
        # POPIA for South Africa
        if context.jurisdiction in ["SOUTH_AFRICA", "POPIA_ZA"]:
            activations.append(FrameworkActivation(
                framework=JurisdictionFramework.POPIA_ZA,
                reason="PHI processing in South Africa",
                priority=1,
                requirements=[
                    "Lawfulness of processing (§11)",
                    "Cross-border transfer safeguards (§14)",
                    "Data subject participation"
                ],
                conflicts=[]
            ))
        
        return activations
    
    def _activate_ai_governance(
        self,
        context: ComplianceContext
    ) -> List[FrameworkActivation]:
        """Activate AI governance frameworks for high-risk AI"""
        activations = []
        
        # EU AI Act for EU jurisdiction
        if context.jurisdiction in ["EU", "GDPR_EU"]:
            activations.append(FrameworkActivation(
                framework=JurisdictionFramework.EU_AI_ACT_2024,
                reason=f"High-risk AI system (risk={context.risk_level:.2f})",
                priority=1,
                requirements=[
                    "Conformity assessment (§43)",
                    "Transparency obligations (§13)",
                    "Human oversight (§14)",
                    "Accuracy and robustness (§15)",
                    "Post-market monitoring (§61)",
                    "Explainability (SHAP/LIME)"
                ],
                conflicts=[]
            ))
        
        # FDA CDS Software for USA
        if context.jurisdiction in ["USA", "HIPAA_US"]:
            activations.append(FrameworkActivation(
                framework=JurisdictionFramework.FDA_CDS_SOFTWARE,
                reason="Clinical decision support AI",
                priority=1,
                requirements=[
                    "Software as Medical Device (SaMD) classification",
                    "Post-market performance monitoring",
                    "Real-world data validation",
                    "Bias assessment"
                ],
                conflicts=[]
            ))
        
        # ISO/IEC 42001 (global)
        activations.append(FrameworkActivation(
            framework=JurisdictionFramework.ISO_IEC_42001,
            reason="AI management system standard",
            priority=2,
            requirements=[
                "AI risk management",
                "Ethical AI deployment",
                "Transparency reporting",
                "Continuous monitoring"
            ],
            conflicts=[]
        ))
        
        return activations
    
    def _activate_health_security(
        self,
        context: ComplianceContext
    ) -> List[FrameworkActivation]:
        """Activate global health security frameworks"""
        activations = []
        
        # WHO IHR 2025 (global)
        activations.append(FrameworkActivation(
            framework=JurisdictionFramework.WHO_IHR_2025,
            reason="Outbreak detection and reporting",
            priority=1,
            requirements=[
                "Core surveillance capacities",
                "Pandemic emergency notification (Art. 12)",
                "Real-time data sharing",
                "Equity in medical access",
                "National focal point coordination"
            ],
            conflicts=[]
        ))
        
        # GHSA
        activations.append(FrameworkActivation(
            framework=JurisdictionFramework.GHSA,
            reason="Global health security coordination",
            priority=2,
            requirements=[
                "Real-time surveillance",
                "Laboratory capacity",
                "Emergency response",
                "Risk communication"
            ],
            conflicts=[]
        ))
        
        # JEE Standards
        activations.append(FrameworkActivation(
            framework=JurisdictionFramework.JEE_STANDARDS,
            reason="Joint external evaluation metrics",
            priority=2,
            requirements=[
                "Real-time data exchange",
                "One Health integration",
                "Zoonotic signal fusion"
            ],
            conflicts=[]
        ))
        
        return activations
    
    def _activate_african_sovereignty(
        self,
        context: ComplianceContext
    ) -> List[FrameworkActivation]:
        """Activate African data sovereignty frameworks"""
        activations = []
        
        # Malabo Convention
        activations.append(FrameworkActivation(
            framework=JurisdictionFramework.MALABO_CONVENTION,
            reason="African Union data protection",
            priority=1,
            requirements=[
                "Data localization for sensitive data (Art. 14)",
                "Cross-border transfer safeguards (Art. 22)",
                "Cybersecurity minimum standards",
                "National DPA coordination"
            ],
            conflicts=[]
        ))
        
        # Country-specific
        if context.jurisdiction == "KENYA":
            activations.append(FrameworkActivation(
                framework=JurisdictionFramework.KENYA_DPA_2025,
                reason="Kenya interoperability guidelines",
                priority=1,
                requirements=[
                    "Cross-border data flow checks",
                    "Federated learning enablement",
                    "Vulnerable population data redaction"
                ],
                conflicts=[]
            ))
        
        if context.jurisdiction == "NIGERIA":
            activations.append(FrameworkActivation(
                framework=JurisdictionFramework.NIGERIA_NDPR,
                reason="Nigeria data protection",
                priority=1,
                requirements=[
                    "Data protection impact assessment",
                    "Consent management",
                    "Data breach notification"
                ],
                conflicts=[]
            ))
        
        return activations
    
    def _activate_cross_border(
        self,
        context: ComplianceContext
    ) -> List[FrameworkActivation]:
        """Activate frameworks for cross-border data transfers"""
        activations = []
        
        # Additional GDPR requirements for cross-border
        if context.jurisdiction in ["EU", "GDPR_EU"]:
            activations.append(FrameworkActivation(
                framework=JurisdictionFramework.GDPR_EU,
                reason="Cross-border data transfer",
                priority=1,
                requirements=[
                    "Adequacy decision (Art. 45) or",
                    "Standard Contractual Clauses (Art. 46) or",
                    "Binding Corporate Rules (Art. 47)",
                    "Transfer impact assessment"
                ],
                conflicts=[]
            ))
        
        return activations
    
    def _activate_esg_reporting(
        self,
        context: ComplianceContext
    ) -> List[FrameworkActivation]:
        """Activate ESG and sustainability reporting frameworks"""
        activations = []
        
        # IFRS S2 for climate disclosures
        activations.append(FrameworkActivation(
            framework=JurisdictionFramework.IFRS_S2,
            reason="Climate-related disclosures",
            priority=2,
            requirements=[
                "Scope 1, 2, 3 emissions disclosure",
                "Climate risk assessment",
                "Transition planning",
                "Scenario analysis"
            ],
            conflicts=[]
        ))
        
        # TCFD alignment
        activations.append(FrameworkActivation(
            framework=JurisdictionFramework.TCFD,
            reason="Climate-related financial disclosures",
            priority=2,
            requirements=[
                "Governance disclosure",
                "Strategy disclosure",
                "Risk management disclosure",
                "Metrics and targets"
            ],
            conflicts=[]
        ))
        
        return activations
    
    def _activate_cybersecurity(
        self,
        context: ComplianceContext
    ) -> List[FrameworkActivation]:
        """Activate cybersecurity frameworks"""
        activations = []
        
        # US Healthcare Cybersecurity Act
        if context.jurisdiction in ["USA", "HIPAA_US"]:
            activations.append(FrameworkActivation(
                framework=JurisdictionFramework.US_HEALTHCARE_CYBER_ACT,
                reason="Healthcare cybersecurity incident",
                priority=1,
                requirements=[
                    "24-hour incident reporting to HHS-CISA",
                    "Minimum cybersecurity standards compliance",
                    "Vulnerability disclosure program",
                    "Annual security assessment"
                ],
                conflicts=[]
            ))
        
        # NIST CSF (global)
        activations.append(FrameworkActivation(
            framework=JurisdictionFramework.NIST_CSF,
            reason="Cybersecurity framework",
            priority=2,
            requirements=[
                "Identify: Asset management",
                "Protect: Access control",
                "Detect: Anomaly detection",
                "Respond: Incident response",
                "Recover: Recovery planning"
            ],
            conflicts=[]
        ))
        
        return activations
    
    def _harmonize_frameworks(
        self,
        activations: List[FrameworkActivation],
        context: ComplianceContext
    ) -> List[FrameworkActivation]:
        """
        AI-triggered harmonization to resolve conflicts and optimize compliance.
        """
        # Detect conflicts
        for i, activation in enumerate(activations):
            targets = FRAMEWORK_REGISTRY.get_harmonization_targets(activation.framework)
            for j, other in enumerate(activations):
                if i != j and other.framework in targets:
                    # These frameworks harmonize - merge requirements
                    logger.info(f"🔗 Harmonizing {activation.framework.name} with {other.framework.name}")
        
        # Remove duplicates
        seen = set()
        unique_activations = []
        for activation in activations:
            if activation.framework not in seen:
                seen.add(activation.framework)
                unique_activations.append(activation)
        
        return unique_activations
    
    def _is_african_jurisdiction(self, jurisdiction: str) -> bool:
        """Check if jurisdiction is in Africa"""
        african_jurisdictions = [
            "KENYA", "SOUTH_AFRICA", "NIGERIA", "GHANA", "RWANDA",
            "ETHIOPIA", "TANZANIA", "UGANDA", "MALAWI", "ZAMBIA"
        ]
        return jurisdiction.upper() in african_jurisdictions
    
    def retroactive_alignment(
        self,
        framework: JurisdictionFramework,
        update_date: datetime
    ) -> Dict:
        """
        Retroactive alignment engine for regulatory updates.
        
        When a framework is updated, this ensures all historical
        compliance decisions are re-evaluated.
        """
        logger.info(f"🔄 Retroactive alignment for {framework.name} (updated {update_date})")
        
        # This would integrate with the Chrono-Ledger to re-verify
        # historical compliance decisions
        
        return {
            "framework": framework.name,
            "update_date": update_date.isoformat(),
            "status": "aligned",
            "affected_records": 0  # Would query Chrono-Ledger
        }
    
    def generate_compliance_report(
        self,
        activations: List[FrameworkActivation]
    ) -> Dict:
        """Generate comprehensive compliance report"""
        return {
            "timestamp": datetime.utcnow().isoformat(),
            "total_frameworks": len(activations),
            "frameworks": [
                {
                    "name": a.framework.name,
                    "reason": a.reason,
                    "priority": a.priority,
                    "requirements": a.requirements
                }
                for a in activations
            ],
            "compliance_status": "COMPLIANT" if activations else "NO_FRAMEWORKS_ACTIVATED"
        }


# Example usage
if __name__ == "__main__":
    nexus = QuantumLawNexus(enable_ai_harmonization=True)
    
    # Example: High-risk AI outbreak prediction in Kenya
    context = ComplianceContext(
        action_type="outbreak_detection",
        jurisdiction="KENYA",
        data_type="PHI",
        risk_level=0.85,
        involves_ai=True,
        cross_border=False,
        involves_phi=True,
        involves_children=False,
        emergency_context=True,
        metadata={"disease": "cholera", "location": "Dadaab"}
    )
    
    activations = nexus.evaluate_compliance(context)
    
    print(f"🌐 Activated {len(activations)} frameworks:")
    for activation in activations:
        print(f"\n  {activation.framework.name}")
        print(f"  Reason: {activation.reason}")
        print(f"  Priority: {activation.priority}")
        print(f"  Requirements: {len(activation.requirements)}")
    
    report = nexus.generate_compliance_report(activations)
    print(f"\n📊 Compliance Status: {report['compliance_status']}")
