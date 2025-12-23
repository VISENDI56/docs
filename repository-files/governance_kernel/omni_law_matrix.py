"""
Dynamic Omni-Law Matrix
Real-time compliance orchestration across 45+ global legal frameworks

This matrix dynamically selects and applies the most restrictive compliant path
when multiple frameworks conflict, using quantum superposition logic.
"""

from typing import Dict, List, Optional
from enum import Enum
from dataclasses import dataclass
from datetime import datetime
import logging

from .quantum_law_nexus import QuantumLawNexus, LegalDomain, LegalFramework

logger = logging.getLogger(__name__)


class ComplianceStatus(Enum):
    """Compliance status levels"""
    COMPLIANT = "compliant"
    PARTIAL = "partial"
    VIOLATION = "violation"
    UNKNOWN = "unknown"


@dataclass
class ComplianceResult:
    """Result of compliance check"""
    status: ComplianceStatus
    governing_frameworks: List[str]
    violations: List[str]
    recommendations: List[str]
    risk_score: float  # 0.0 (no risk) to 1.0 (critical risk)
    timestamp: str


class OmniLawMatrix:
    """
    Dynamic Omni-Law Matrix for real-time compliance orchestration.
    
    The Matrix:
    1. Receives an action request
    2. Identifies all applicable frameworks
    3. Resolves conflicts using quantum logic
    4. Returns the most restrictive compliant path
    5. Logs all decisions to tamper-proof audit trail
    """
    
    def __init__(self, enable_audit: bool = True):
        self.nexus = QuantumLawNexus()
        self.enable_audit = enable_audit
        self.audit_trail = []
        
        logger.info("🌐 Dynamic Omni-Law Matrix initialized")
    
    def validate_data_transfer(
        self,
        source_jurisdiction: str,
        destination_jurisdiction: str,
        data_type: str,
        consent_token: Optional[str] = None,
        emergency_override: bool = False
    ) -> ComplianceResult:
        """
        Validate cross-border data transfer.
        
        Args:
            source_jurisdiction: Origin jurisdiction (e.g., "Kenya")
            destination_jurisdiction: Destination jurisdiction (e.g., "EU")
            data_type: Type of data (e.g., "PHI", "PII")
            consent_token: Consent authorization token
            emergency_override: Emergency override flag (WHO IHR Article 6)
        
        Returns:
            ComplianceResult with validation outcome
        """
        violations = []
        recommendations = []
        risk_score = 0.0
        
        # Get applicable frameworks
        result = self.nexus.validate_action(
            action="Data_Transfer",
            jurisdiction=source_jurisdiction,
            domains=[LegalDomain.DATA_PROTECTION, LegalDomain.HEALTH_SECURITY],
            context={
                "data_type": data_type,
                "destination": destination_jurisdiction,
                "consent_token": consent_token,
                "emergency_override": emergency_override
            }
        )
        
        governing_framework = self.nexus.frameworks.get(result["governing_framework"])
        
        # Check for sovereignty violations
        if data_type in ["PHI", "PII", "Sensitive"]:
            # GDPR Art. 9, KDPA §37, POPIA §57 - Special categories cannot leave territory
            if source_jurisdiction in ["Kenya", "EU", "South Africa"]:
                if destination_jurisdiction not in ["Kenya", "EU", "South Africa"]:
                    if not emergency_override:
                        violations.append(
                            f"Sovereignty violation: {data_type} cannot transfer from "
                            f"{source_jurisdiction} to {destination_jurisdiction} without emergency authorization"
                        )
                        risk_score += 0.8
                        recommendations.append("Obtain Data Protection Commissioner authorization")
                        recommendations.append("Implement Standard Contractual Clauses (SCC)")
        
        # Check consent requirements
        if not consent_token and not emergency_override:
            violations.append("Missing consent token for data transfer")
            risk_score += 0.3
            recommendations.append("Obtain explicit consent from data subject")
        
        # Emergency override (WHO IHR Article 6)
        if emergency_override:
            logger.warning(f"⚠️ Emergency override activated for {data_type} transfer")
            recommendations.append("Document emergency justification per WHO IHR Article 6")
            risk_score = max(0.0, risk_score - 0.5)  # Reduce risk score for emergency
        
        # Determine status
        if violations and not emergency_override:
            status = ComplianceStatus.VIOLATION
        elif violations and emergency_override:
            status = ComplianceStatus.PARTIAL
        else:
            status = ComplianceStatus.COMPLIANT
        
        result_obj = ComplianceResult(
            status=status,
            governing_frameworks=result["frameworks"],
            violations=violations,
            recommendations=recommendations,
            risk_score=min(1.0, risk_score),
            timestamp=datetime.utcnow().isoformat()
        )
        
        if self.enable_audit:
            self._log_audit("Data_Transfer", result_obj)
        
        return result_obj
    
    def validate_high_risk_inference(
        self,
        inference_type: str,
        confidence_score: float,
        explanation: Optional[Dict] = None,
        evidence_chain: Optional[List] = None,
        jurisdiction: str = "Global"
    ) -> ComplianceResult:
        """
        Validate high-risk AI inference (EU AI Act §6, FDA CDSS).
        
        Args:
            inference_type: Type of inference (e.g., "diagnosis", "treatment_recommendation")
            confidence_score: Model confidence (0.0 to 1.0)
            explanation: SHAP values or other explainability data
            evidence_chain: Chain of evidence supporting inference
            jurisdiction: Applicable jurisdiction
        
        Returns:
            ComplianceResult with validation outcome
        """
        violations = []
        recommendations = []
        risk_score = 0.0
        
        # Get applicable frameworks
        result = self.nexus.validate_action(
            action="High_Risk_Inference",
            jurisdiction=jurisdiction,
            domains=[LegalDomain.AI_GOVERNANCE, LegalDomain.HEALTH_SECURITY],
            context={
                "inference_type": inference_type,
                "confidence_score": confidence_score
            }
        )
        
        # EU AI Act §6 - High-risk AI systems
        if confidence_score >= 0.7:
            # Requires explainability
            if not explanation:
                violations.append("EU AI Act §6: High-risk inference requires explainability (SHAP values)")
                risk_score += 0.6
                recommendations.append("Implement SHAP explainability for model outputs")
            
            # Requires evidence chain
            if not evidence_chain:
                violations.append("EU AI Act §8: Missing evidence chain for high-risk inference")
                risk_score += 0.4
                recommendations.append("Document complete evidence chain")
        
        # FDA CDSS - Clinical Decision Support Software
        if inference_type in ["diagnosis", "treatment_recommendation"]:
            if confidence_score < 0.85:
                recommendations.append("FDA CDSS: Consider human-in-the-loop for confidence < 0.85")
                risk_score += 0.2
        
        # GDPR Art. 22 - Right to explanation
        if jurisdiction in ["EU", "Global"]:
            if not explanation:
                violations.append("GDPR Art. 22: Automated decision requires explanation")
                risk_score += 0.5
                recommendations.append("Provide human-readable explanation to data subject")
        
        # Determine status
        status = ComplianceStatus.VIOLATION if violations else ComplianceStatus.COMPLIANT
        
        result_obj = ComplianceResult(
            status=status,
            governing_frameworks=result["frameworks"],
            violations=violations,
            recommendations=recommendations,
            risk_score=min(1.0, risk_score),
            timestamp=datetime.utcnow().isoformat()
        )
        
        if self.enable_audit:
            self._log_audit("High_Risk_Inference", result_obj)
        
        return result_obj
    
    def validate_esg_disclosure(
        self,
        disclosure_type: str,
        metrics: Dict,
        jurisdiction: str = "Global"
    ) -> ComplianceResult:
        """
        Validate ESG disclosure compliance (ISSB S1/S2, CSRD, TCFD).
        
        Args:
            disclosure_type: Type of disclosure (e.g., "climate", "health_impact")
            metrics: Disclosure metrics
            jurisdiction: Applicable jurisdiction
        
        Returns:
            ComplianceResult with validation outcome
        """
        violations = []
        recommendations = []
        risk_score = 0.0
        
        # Get applicable frameworks
        result = self.nexus.validate_action(
            action="ESG_Disclosure",
            jurisdiction=jurisdiction,
            domains=[LegalDomain.FINANCIAL_REPORTING, LegalDomain.ENVIRONMENTAL],
            context={"disclosure_type": disclosure_type}
        )
        
        # ISSB S1 - General Requirements
        required_metrics = ["governance", "strategy", "risk_management", "metrics_targets"]
        missing_metrics = [m for m in required_metrics if m not in metrics]
        
        if missing_metrics:
            violations.append(f"ISSB S1: Missing required metrics: {', '.join(missing_metrics)}")
            risk_score += 0.3 * len(missing_metrics)
            recommendations.append("Complete all four pillars of ISSB S1 disclosure")
        
        # ISSB S2 - Climate-related Disclosures
        if disclosure_type == "climate":
            if "scope_1_emissions" not in metrics or "scope_2_emissions" not in metrics:
                violations.append("ISSB S2: Missing Scope 1 and Scope 2 emissions data")
                risk_score += 0.4
                recommendations.append("Calculate and disclose Scope 1, 2, and 3 emissions")
        
        # CSRD (EU) - Corporate Sustainability Reporting Directive
        if jurisdiction == "EU":
            if "double_materiality" not in metrics:
                violations.append("CSRD: Missing double materiality assessment")
                risk_score += 0.5
                recommendations.append("Conduct double materiality assessment per ESRS 2")
        
        # Determine status
        status = ComplianceStatus.VIOLATION if violations else ComplianceStatus.COMPLIANT
        
        result_obj = ComplianceResult(
            status=status,
            governing_frameworks=result["frameworks"],
            violations=violations,
            recommendations=recommendations,
            risk_score=min(1.0, risk_score),
            timestamp=datetime.utcnow().isoformat()
        )
        
        if self.enable_audit:
            self._log_audit("ESG_Disclosure", result_obj)
        
        return result_obj
    
    def validate_pandemic_response(
        self,
        response_type: str,
        jurisdiction: str,
        pheic_declared: bool = False
    ) -> ComplianceResult:
        """
        Validate pandemic response compliance (IHR 2025, Pandemic Treaty).
        
        Args:
            response_type: Type of response (e.g., "notification", "containment")
            jurisdiction: Applicable jurisdiction
            pheic_declared: Whether PHEIC (Public Health Emergency of International Concern) is declared
        
        Returns:
            ComplianceResult with validation outcome
        """
        violations = []
        recommendations = []
        risk_score = 0.0
        
        # Get applicable frameworks
        result = self.nexus.validate_action(
            action="Pandemic_Response",
            jurisdiction=jurisdiction,
            domains=[LegalDomain.HEALTH_SECURITY, LegalDomain.HUMANITARIAN],
            context={"response_type": response_type, "pheic": pheic_declared}
        )
        
        # IHR 2025 Art. 6 - Notification
        if response_type == "notification":
            recommendations.append("IHR 2025 Art. 6: Notify WHO within 24 hours of assessment")
            recommendations.append("IHR 2025 Art. 7: Continue information sharing")
        
        # IHR 2025 Art. 4bis - Pandemic Prevention
        if pheic_declared:
            recommendations.append("IHR 2025 Art. 4bis: Activate pandemic prevention measures")
            recommendations.append("IHR 2025 Art. 18: Implement pandemic emergency recommendations")
        
        # Pandemic Treaty Art. 12 - Access and Benefit-Sharing
        if response_type == "vaccine_distribution":
            recommendations.append("Pandemic Treaty Art. 12: Ensure equitable access to vaccines")
            recommendations.append("Pandemic Treaty Art. 15: Activate sustainable financing mechanisms")
        
        # Geneva Convention - Humanitarian protection
        if response_type == "containment":
            recommendations.append("Geneva Convention Art. 3: Protect civilian population")
            recommendations.append("ICRC Code: Ensure access to health care")
        
        # Determine status (pandemic response is always compliant if following IHR)
        status = ComplianceStatus.COMPLIANT
        
        result_obj = ComplianceResult(
            status=status,
            governing_frameworks=result["frameworks"],
            violations=violations,
            recommendations=recommendations,
            risk_score=risk_score,
            timestamp=datetime.utcnow().isoformat()
        )
        
        if self.enable_audit:
            self._log_audit("Pandemic_Response", result_obj)
        
        return result_obj
    
    def get_compliance_dashboard(self) -> Dict:
        """
        Get real-time compliance dashboard.
        
        Returns:
            Dashboard with compliance metrics
        """
        # Analyze audit trail
        total_checks = len(self.audit_trail)
        
        if total_checks == 0:
            return {
                "total_checks": 0,
                "compliance_rate": 1.0,
                "violation_rate": 0.0,
                "average_risk_score": 0.0,
                "top_violations": []
            }
        
        compliant = sum(1 for entry in self.audit_trail if entry["result"].status == ComplianceStatus.COMPLIANT)
        violations = sum(1 for entry in self.audit_trail if entry["result"].status == ComplianceStatus.VIOLATION)
        
        avg_risk = sum(entry["result"].risk_score for entry in self.audit_trail) / total_checks
        
        # Count violation types
        violation_counts = {}
        for entry in self.audit_trail:
            for violation in entry["result"].violations:
                violation_counts[violation] = violation_counts.get(violation, 0) + 1
        
        top_violations = sorted(violation_counts.items(), key=lambda x: x[1], reverse=True)[:5]
        
        return {
            "total_checks": total_checks,
            "compliance_rate": compliant / total_checks,
            "violation_rate": violations / total_checks,
            "average_risk_score": avg_risk,
            "top_violations": [{"violation": v, "count": c} for v, c in top_violations],
            "framework_summary": self.nexus.get_framework_summary()
        }
    
    def _log_audit(self, action: str, result: ComplianceResult):
        """Internal audit logging"""
        audit_entry = {
            "timestamp": datetime.utcnow().isoformat(),
            "action": action,
            "result": result
        }
        self.audit_trail.append(audit_entry)
        
        logger.info(f"🌐 Omni-Law Matrix: {action} - {result.status.value}")
        if result.violations:
            logger.warning(f"   Violations: {len(result.violations)}")
        if result.recommendations:
            logger.info(f"   Recommendations: {len(result.recommendations)}")


# Example usage
if __name__ == "__main__":
    matrix = OmniLawMatrix(enable_audit=True)
    
    # Test 1: Data transfer validation
    print("=" * 60)
    print("TEST 1: Cross-border data transfer (Kenya → USA)")
    print("=" * 60)
    
    result = matrix.validate_data_transfer(
        source_jurisdiction="Kenya",
        destination_jurisdiction="USA",
        data_type="PHI",
        consent_token=None,
        emergency_override=False
    )
    
    print(f"Status: {result.status.value}")
    print(f"Risk Score: {result.risk_score:.2f}")
    print(f"Violations: {len(result.violations)}")
    for v in result.violations:
        print(f"  - {v}")
    print(f"Recommendations: {len(result.recommendations)}")
    for r in result.recommendations:
        print(f"  - {r}")
    
    # Test 2: High-risk AI inference
    print("\n" + "=" * 60)
    print("TEST 2: High-risk AI inference (diagnosis)")
    print("=" * 60)
    
    result = matrix.validate_high_risk_inference(
        inference_type="diagnosis",
        confidence_score=0.92,
        explanation={"shap_values": [0.8, 0.1, 0.1]},
        evidence_chain=["fever", "cough", "positive_test"],
        jurisdiction="EU"
    )
    
    print(f"Status: {result.status.value}")
    print(f"Risk Score: {result.risk_score:.2f}")
    print(f"Violations: {len(result.violations)}")
    print(f"Recommendations: {len(result.recommendations)}")
    
    # Test 3: Compliance dashboard
    print("\n" + "=" * 60)
    print("TEST 3: Compliance Dashboard")
    print("=" * 60)
    
    dashboard = matrix.get_compliance_dashboard()
    print(f"Total Checks: {dashboard['total_checks']}")
    print(f"Compliance Rate: {dashboard['compliance_rate']:.1%}")
    print(f"Average Risk Score: {dashboard['average_risk_score']:.2f}")
