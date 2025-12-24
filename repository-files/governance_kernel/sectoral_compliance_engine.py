"""
Sectoral Compliance Engine - Governance Kernel v3.0
Maps operational contexts to regulatory bundles and enforces compliance.

The brain of the Regulatory Singularity Stack.
"""

import json
import logging
from typing import Dict, List, Optional, Any, Tuple
from enum import Enum
from datetime import datetime
from pathlib import Path

logger = logging.getLogger(__name__)


class EnforcementAction(Enum):
    """Enforcement actions for compliance violations"""
    BLOCK = "BLOCK"
    REQUIRE_CONFORMITY_ASSESSMENT = "REQUIRE_CONFORMITY_ASSESSMENT"
    REQUIRE_DISCLOSURE = "REQUIRE_DISCLOSURE"
    LOG_ONLY = "LOG_ONLY"
    TRIGGER_IHR_NOTIFICATION = "TRIGGER_IHR_NOTIFICATION"
    ENABLE_WHO_DATA_STREAM = "ENABLE_WHO_DATA_STREAM"
    ENFORCE_MALABO_ADEQUACY = "ENFORCE_MALABO_ADEQUACY"
    ENFORCE_KDPA_SOVEREIGNTY = "ENFORCE_KDPA_SOVEREIGNTY"
    REQUIRE_CLIMATE_DISCLOSURE = "REQUIRE_CLIMATE_DISCLOSURE"
    REQUIRE_DUE_DILIGENCE_REPORT = "REQUIRE_DUE_DILIGENCE_REPORT"
    BLOCK_IMPORT_UNLESS_REBUTTED = "BLOCK_IMPORT_UNLESS_REBUTTED"
    REQUIRE_FATF_SCREENING = "REQUIRE_FATF_SCREENING"
    BLOCK_UNLESS_HUMANITARIAN_EXEMPTION = "BLOCK_UNLESS_HUMANITARIAN_EXEMPTION"
    REQUIRE_MDR_CONFORMITY = "REQUIRE_MDR_CONFORMITY"
    REQUIRE_21_CFR_11_COMPLIANCE = "REQUIRE_21_CFR_11_COMPLIANCE"
    REQUIRE_NIS2_COMPLIANCE = "REQUIRE_NIS2_COMPLIANCE"
    ENFORCE_GDPR = "ENFORCE_GDPR"
    ENFORCE_HIPAA = "ENFORCE_HIPAA"


class ComplianceResult:
    """Result of a compliance check"""
    
    def __init__(
        self,
        compliant: bool,
        sector: str,
        applicable_frameworks: List[Dict],
        enforcement_actions: List[EnforcementAction],
        violations: List[str],
        recommendations: List[str],
        risk_score: float,
        metadata: Optional[Dict] = None
    ):
        self.compliant = compliant
        self.sector = sector
        self.applicable_frameworks = applicable_frameworks
        self.enforcement_actions = enforcement_actions
        self.violations = violations
        self.recommendations = recommendations
        self.risk_score = risk_score
        self.metadata = metadata or {}
        self.timestamp = datetime.utcnow().isoformat()
    
    def to_dict(self) -> Dict:
        return {
            "compliant": self.compliant,
            "sector": self.sector,
            "applicable_frameworks": self.applicable_frameworks,
            "enforcement_actions": [action.value for action in self.enforcement_actions],
            "violations": self.violations,
            "recommendations": self.recommendations,
            "risk_score": self.risk_score,
            "metadata": self.metadata,
            "timestamp": self.timestamp
        }


class SectoralComplianceEngine:
    """
    The brain that maps contexts to laws.
    
    Instead of checking 45 laws individually, the system checks the context
    (e.g., "Predictive Diagnosis in Kenya") and automatically pulls the
    relevant Regulatory Bundle.
    """
    
    def __init__(self, laws_path: Optional[str] = None):
        """
        Initialize the Sectoral Compliance Engine.
        
        Args:
            laws_path: Path to sectoral_laws.json
        """
        if laws_path is None:
            laws_path = Path(__file__).parent / "sectoral_laws.json"
        
        with open(laws_path, 'r') as f:
            self.laws_registry = json.load(f)
        
        self.version = self.laws_registry.get("version", "3.0.0")
        self.sectors = self.laws_registry.get("sectors", {})
        self.conflict_rules = self.laws_registry.get("conflict_resolution_rules", {})
        
        logger.info(f"🧠 Sectoral Compliance Engine v{self.version} initialized")
        logger.info(f"📚 Loaded {len(self.sectors)} sectors with {self._count_frameworks()} frameworks")
    
    def _count_frameworks(self) -> int:
        """Count total frameworks across all sectors"""
        count = 0
        for sector_data in self.sectors.values():
            count += len(sector_data.get("frameworks", []))
        return count
    
    def validate_operation(
        self,
        sector: str,
        context: str,
        payload: Dict[str, Any]
    ) -> ComplianceResult:
        """
        Main entry point for compliance validation.
        
        Args:
            sector: Sector name (e.g., "AI_Trust", "Pandemic_Sentinel")
            context: Operational context (e.g., "diagnosis", "outbreak_detection")
            payload: Operation payload with relevant data
        
        Returns:
            ComplianceResult with enforcement actions
        """
        logger.info(f"🔍 Validating operation - Sector: {sector}, Context: {context}")
        
        # Get sector data
        sector_data = self.sectors.get(sector)
        if not sector_data:
            logger.warning(f"⚠️ Unknown sector: {sector}")
            return ComplianceResult(
                compliant=False,
                sector=sector,
                applicable_frameworks=[],
                enforcement_actions=[EnforcementAction.BLOCK],
                violations=[f"Unknown sector: {sector}"],
                recommendations=["Use a valid sector from the registry"],
                risk_score=1.0
            )
        
        # Find applicable frameworks
        applicable_frameworks = []
        enforcement_actions = []
        violations = []
        recommendations = []
        
        for framework in sector_data.get("frameworks", []):
            if self._check_trigger_condition(framework, context, payload):
                applicable_frameworks.append(framework)
                
                # Check compliance
                is_compliant, framework_violations, framework_recommendations = self._check_framework_compliance(
                    framework, context, payload
                )
                
                if not is_compliant:
                    violations.extend(framework_violations)
                    recommendations.extend(framework_recommendations)
                    
                    # Add enforcement action
                    action_str = framework.get("enforcement_action", "BLOCK")
                    try:
                        action = EnforcementAction[action_str]
                        if action not in enforcement_actions:
                            enforcement_actions.append(action)
                    except KeyError:
                        logger.warning(f"⚠️ Unknown enforcement action: {action_str}")
        
        # Calculate risk score
        risk_score = self._calculate_risk_score(
            applicable_frameworks, violations, payload
        )
        
        # Determine overall compliance
        compliant = len(violations) == 0
        
        result = ComplianceResult(
            compliant=compliant,
            sector=sector,
            applicable_frameworks=[
                {
                    "id": f.get("id"),
                    "name": f.get("name"),
                    "jurisdiction": f.get("jurisdiction")
                }
                for f in applicable_frameworks
            ],
            enforcement_actions=enforcement_actions,
            violations=violations,
            recommendations=recommendations,
            risk_score=risk_score,
            metadata={
                "context": context,
                "frameworks_checked": len(sector_data.get("frameworks", [])),
                "frameworks_applicable": len(applicable_frameworks)
            }
        )
        
        if compliant:
            logger.info(f"✅ Operation compliant - Risk score: {risk_score:.2f}")
        else:
            logger.warning(f"❌ Operation non-compliant - {len(violations)} violations")
        
        return result
    
    def _check_trigger_condition(
        self,
        framework: Dict,
        context: str,
        payload: Dict[str, Any]
    ) -> bool:
        """
        Check if a framework's trigger condition is met.
        
        Args:
            framework: Framework definition
            context: Operational context
            payload: Operation payload
        
        Returns:
            True if framework applies
        """
        trigger = framework.get("trigger_condition")
        if not trigger:
            return False
        
        # Build evaluation context
        eval_context = {
            "context": context,
            **payload
        }
        
        try:
            # Simple expression evaluation
            # In production, use a proper expression parser
            result = self._evaluate_trigger(trigger, eval_context)
            return result
        except Exception as e:
            logger.error(f"❌ Error evaluating trigger: {e}")
            return False
    
    def _evaluate_trigger(self, trigger: str, context: Dict) -> bool:
        """
        Evaluate a trigger condition.
        
        This is a simplified implementation. In production, use a proper
        expression parser like pyparsing or lark.
        """
        # Replace context variables
        for key, value in context.items():
            if isinstance(value, str):
                trigger = trigger.replace(key, f"'{value}'")
            else:
                trigger = trigger.replace(key, str(value))
        
        # Handle IN operator
        if " IN " in trigger:
            parts = trigger.split(" IN ")
            if len(parts) == 2:
                value = parts[0].strip()
                list_str = parts[1].strip()
                # Simple list check
                return value in list_str
        
        # Handle comparison operators
        if "==" in trigger:
            parts = trigger.split("==")
            if len(parts) == 2:
                return parts[0].strip() == parts[1].strip()
        
        if ">" in trigger:
            parts = trigger.split(">")
            if len(parts) == 2:
                try:
                    return float(parts[0].strip()) > float(parts[1].strip())
                except ValueError:
                    return False
        
        if "OR" in trigger:
            parts = trigger.split(" OR ")
            return any(self._evaluate_trigger(part.strip(), context) for part in parts)
        
        if "AND" in trigger:
            parts = trigger.split(" AND ")
            return all(self._evaluate_trigger(part.strip(), context) for part in parts)
        
        # Default: check if variable is truthy
        return context.get(trigger.strip(), False)
    
    def _check_framework_compliance(
        self,
        framework: Dict,
        context: str,
        payload: Dict[str, Any]
    ) -> Tuple[bool, List[str], List[str]]:
        """
        Check compliance with a specific framework.
        
        Returns:
            (is_compliant, violations, recommendations)
        """
        violations = []
        recommendations = []
        
        framework_id = framework.get("id")
        
        # AI Trust sector checks
        if framework_id == "EU_AI_ACT":
            return self._check_eu_ai_act_compliance(framework, context, payload)
        
        # Pandemic Sentinel checks
        elif framework_id == "IHR_2005_2025":
            return self._check_ihr_compliance(framework, context, payload)
        
        # African Sovereignty checks
        elif framework_id in ["AU_MALABO_CONVENTION", "KENYA_DPA", "NIGERIA_NDPR", "SOUTH_AFRICA_POPIA"]:
            return self._check_african_sovereignty_compliance(framework, context, payload)
        
        # Supply Chain checks
        elif framework_id in ["EU_CSDDD", "GERMANY_LKSG", "US_UFLPA", "DODD_FRANK_1502"]:
            return self._check_supply_chain_compliance(framework, context, payload)
        
        # Humanitarian checks
        elif framework_id in ["FATF_REC_8", "OFAC_SANCTIONS"]:
            return self._check_humanitarian_compliance(framework, context, payload)
        
        # Default: assume compliant if no specific checks
        return True, [], []
    
    def _check_eu_ai_act_compliance(
        self,
        framework: Dict,
        context: str,
        payload: Dict[str, Any]
    ) -> Tuple[bool, List[str], List[str]]:
        """Check EU AI Act compliance"""
        violations = []
        recommendations = []
        
        risk_pyramid = framework.get("risk_pyramid", {})
        risk_score = payload.get("risk_score", 0.0)
        
        # Check for prohibited systems
        if context in ["social_scoring", "subliminal_manipulation"]:
            violations.append("EU AI Act: Prohibited AI system detected")
            recommendations.append("This AI system is banned under EU AI Act")
            return False, violations, recommendations
        
        # Check high-risk systems
        if risk_score > 0.7 or context in ["diagnosis", "treatment"]:
            high_risk = risk_pyramid.get("HIGH_RISK", {})
            requirements = high_risk.get("requirements", [])
            
            # Check if conformity assessment is provided
            if not payload.get("conformity_assessment"):
                violations.append("EU AI Act: High-risk AI system requires conformity assessment")
                recommendations.append("Provide: " + ", ".join(requirements))
                return False, violations, recommendations
            
            # Check for explanation (Right to Explanation)
            if not payload.get("explanation"):
                violations.append("EU AI Act: High-risk inference requires explanation")
                recommendations.append("Provide SHAP values or feature importance")
                return False, violations, recommendations
        
        return True, [], []
    
    def _check_ihr_compliance(
        self,
        framework: Dict,
        context: str,
        payload: Dict[str, Any]
    ) -> Tuple[bool, List[str], List[str]]:
        """Check IHR 2005/2025 compliance"""
        violations = []
        recommendations = []
        
        # Check if outbreak detected
        outbreak_detected = payload.get("outbreak_detected", False)
        z_score = payload.get("z_score", 0.0)
        ecf_entropy = payload.get("ecf_entropy", 0.0)
        
        if outbreak_detected or z_score > 3.0 or ecf_entropy > 0.15:
            # Check if notification was sent
            if not payload.get("ihr_notification_sent"):
                violations.append("IHR 2005/2025: Outbreak detected but WHO notification not sent")
                recommendations.append(
                    f"Notify WHO National Focal Point within {framework.get('notification_window_hours', 48)} hours"
                )
                return False, violations, recommendations
        
        return True, [], []
    
    def _check_african_sovereignty_compliance(
        self,
        framework: Dict,
        context: str,
        payload: Dict[str, Any]
    ) -> Tuple[bool, List[str], List[str]]:
        """Check African sovereignty frameworks"""
        violations = []
        recommendations = []
        
        # Check data residency
        destination = payload.get("destination")
        data_type = payload.get("data_type")
        
        if data_type == "PHI" and destination:
            # Check if destination is in adequacy whitelist
            adequacy_whitelist = framework.get("adequacy_whitelist", [])
            
            if destination not in adequacy_whitelist:
                violations.append(
                    f"{framework.get('name')}: Cross-border PHI transfer to non-adequate jurisdiction"
                )
                recommendations.append(
                    f"Transfer only to adequate jurisdictions: {', '.join(adequacy_whitelist)}"
                )
                return False, violations, recommendations
        
        return True, [], []
    
    def _check_supply_chain_compliance(
        self,
        framework: Dict,
        context: str,
        payload: Dict[str, Any]
    ) -> Tuple[bool, List[str], List[str]]:
        """Check supply chain due diligence"""
        violations = []
        recommendations = []
        
        framework_id = framework.get("id")
        
        if framework_id == "US_UFLPA":
            # Check for Xinjiang origin
            origin = payload.get("origin")
            supply_chain_includes_xinjiang = payload.get("supply_chain_includes_xinjiang", False)
            
            if origin == "XINJIANG" or supply_chain_includes_xinjiang:
                # Check for rebuttal evidence
                if not payload.get("forced_labor_rebuttal_evidence"):
                    violations.append("UFLPA: Rebuttable presumption of forced labor not rebutted")
                    recommendations.append("Provide evidence of non-forced labor or change supplier")
                    return False, violations, recommendations
        
        return True, [], []
    
    def _check_humanitarian_compliance(
        self,
        framework: Dict,
        context: str,
        payload: Dict[str, Any]
    ) -> Tuple[bool, List[str], List[str]]:
        """Check humanitarian and sanctions compliance"""
        violations = []
        recommendations = []
        
        framework_id = framework.get("id")
        
        if framework_id == "OFAC_SANCTIONS":
            # Check for sanctioned entities
            involves_sanctioned = payload.get("transaction_involves_sanctioned_entity", False)
            
            if involves_sanctioned:
                # Check for humanitarian exemption
                is_humanitarian = payload.get("humanitarian_exemption", False)
                exemption_type = payload.get("exemption_type")
                
                humanitarian_exemptions = framework.get("humanitarian_exemptions", [])
                
                if not is_humanitarian or exemption_type not in humanitarian_exemptions:
                    violations.append("OFAC: Transaction with sanctioned entity without valid exemption")
                    recommendations.append(
                        f"Apply humanitarian exemption: {', '.join(humanitarian_exemptions)}"
                    )
                    return False, violations, recommendations
        
        return True, [], []
    
    def _calculate_risk_score(
        self,
        applicable_frameworks: List[Dict],
        violations: List[str],
        payload: Dict[str, Any]
    ) -> float:
        """
        Calculate overall risk score.
        
        Returns:
            Risk score between 0.0 (low risk) and 1.0 (high risk)
        """
        # Base risk from payload
        base_risk = payload.get("risk_score", 0.0)
        
        # Add risk for violations
        violation_risk = min(len(violations) * 0.2, 0.8)
        
        # Add risk for number of applicable frameworks
        framework_risk = min(len(applicable_frameworks) * 0.05, 0.3)
        
        # Combine risks
        total_risk = min(base_risk + violation_risk + framework_risk, 1.0)
        
        return total_risk
    
    def get_sector_info(self, sector: str) -> Optional[Dict]:
        """Get information about a sector"""
        return self.sectors.get(sector)
    
    def list_sectors(self) -> List[str]:
        """List all available sectors"""
        return list(self.sectors.keys())
    
    def get_applicable_frameworks(
        self,
        sector: str,
        context: str,
        payload: Dict[str, Any]
    ) -> List[Dict]:
        """Get list of applicable frameworks without full validation"""
        sector_data = self.sectors.get(sector)
        if not sector_data:
            return []
        
        applicable = []
        for framework in sector_data.get("frameworks", []):
            if self._check_trigger_condition(framework, context, payload):
                applicable.append(framework)
        
        return applicable


# Example usage
if __name__ == "__main__":
    engine = SectoralComplianceEngine()
    
    # Example 1: AI diagnosis in EU
    result = engine.validate_operation(
        sector="AI_Trust",
        context="diagnosis",
        payload={
            "region": "EU",
            "risk_score": 0.85,
            "explanation": "SHAP values: [0.7, 0.2, 0.1]",
            "conformity_assessment": True
        }
    )
    
    print(f"\n{'='*60}")
    print("Example 1: AI Diagnosis in EU")
    print(f"{'='*60}")
    print(f"Compliant: {result.compliant}")
    print(f"Risk Score: {result.risk_score:.2f}")
    print(f"Applicable Frameworks: {len(result.applicable_frameworks)}")
    for fw in result.applicable_frameworks:
        print(f"  - {fw['name']}")
    
    # Example 2: Outbreak detection in Kenya
    result = engine.validate_operation(
        sector="Pandemic_Sentinel",
        context="outbreak_detection",
        payload={
            "outbreak_detected": True,
            "z_score": 4.5,
            "ecf_entropy": 0.18,
            "ihr_notification_sent": False
        }
    )
    
    print(f"\n{'='*60}")
    print("Example 2: Outbreak Detection in Kenya")
    print(f"{'='*60}")
    print(f"Compliant: {result.compliant}")
    print(f"Violations: {len(result.violations)}")
    for violation in result.violations:
        print(f"  - {violation}")
    print(f"Recommendations: {len(result.recommendations)}")
    for rec in result.recommendations:
        print(f"  - {rec}")
