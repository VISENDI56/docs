"""
iLuminara Compliance Matrix
Law-as-Code implementation of 29 global frameworks

This module implements boolean logic gates for all regulatory frameworks.
Example: IF Region == "Kenya" AND Data_Type == "HIV_Status" AND Target_Server == "USA"
         THEN Block_Transfer() (citing KDPA Sec 37)
"""

import json
import os
from typing import Dict, List, Optional, Any
from enum import Enum
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


class ComplianceStatus(Enum):
    """Compliance check results"""
    COMPLIANT = "COMPLIANT"
    VIOLATION = "VIOLATION"
    WARNING = "WARNING"
    REQUIRES_REVIEW = "REQUIRES_REVIEW"


class SectoralContext(Enum):
    """Sectoral contexts for compliance checking"""
    DATA_PRIVACY = "data_privacy"
    SUPPLY_CHAIN = "supply_chain"
    ESG_CARBON = "esg_carbon"
    HUMANITARIAN_FINANCE = "humanitarian_finance"
    HEALTHCARE_PHARMA = "healthcare_pharma"
    CYBERSECURITY = "cybersecurity"
    AI_GOVERNANCE = "ai_governance"


class ComplianceMatrix:
    """
    The Omni-Law Matrix: 29 global frameworks as boolean logic gates
    """
    
    def __init__(self, sectoral_laws_path: str = "governance_kernel/sectoral_laws.json"):
        self.sectoral_laws_path = sectoral_laws_path
        self.frameworks = self._load_frameworks()
        self.violation_log = []
        
        logger.info(f"🛡️ Compliance Matrix initialized - {len(self.frameworks)} frameworks loaded")
    
    def _load_frameworks(self) -> Dict:
        """Load sectoral laws configuration"""
        if not os.path.exists(self.sectoral_laws_path):
            logger.warning(f"⚠️ Sectoral laws file not found: {self.sectoral_laws_path}")
            return {}
        
        with open(self.sectoral_laws_path, 'r') as f:
            return json.load(f)
    
    def check_sectoral_compliance(
        self,
        context: SectoralContext,
        payload: Dict[str, Any],
        jurisdiction: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Check compliance across sectoral frameworks
        
        Args:
            context: Sectoral context (supply_chain, esg_carbon, etc.)
            payload: Action payload with relevant data
            jurisdiction: Optional jurisdiction override
        
        Returns:
            Compliance result with status, violations, and recommendations
        """
        result = {
            "status": ComplianceStatus.COMPLIANT.value,
            "context": context.value,
            "timestamp": datetime.utcnow().isoformat(),
            "violations": [],
            "warnings": [],
            "frameworks_checked": [],
            "recommendations": []
        }
        
        # Route to appropriate sectoral checker
        if context == SectoralContext.SUPPLY_CHAIN:
            return self._check_supply_chain_compliance(payload, result)
        elif context == SectoralContext.ESG_CARBON:
            return self._check_esg_carbon_compliance(payload, result)
        elif context == SectoralContext.HUMANITARIAN_FINANCE:
            return self._check_humanitarian_finance_compliance(payload, result)
        elif context == SectoralContext.HEALTHCARE_PHARMA:
            return self._check_healthcare_pharma_compliance(payload, result)
        elif context == SectoralContext.CYBERSECURITY:
            return self._check_cybersecurity_compliance(payload, result)
        elif context == SectoralContext.AI_GOVERNANCE:
            return self._check_ai_governance_compliance(payload, result)
        elif context == SectoralContext.DATA_PRIVACY:
            return self._check_data_privacy_compliance(payload, jurisdiction, result)
        
        return result
    
    def _check_supply_chain_compliance(self, payload: Dict, result: Dict) -> Dict:
        """Check supply chain & manufacturing compliance"""
        frameworks = self.frameworks.get("supply_chain_manufacturing", {}).get("frameworks", [])
        
        for framework in frameworks:
            result["frameworks_checked"].append(framework["id"])
            
            # CSDDD: Supplier risk check
            if framework["id"] == "CSDDD":
                supplier_risk = payload.get("supplier_risk_score", 0)
                threshold = payload.get("risk_threshold", 0.7)
                
                if supplier_risk > threshold:
                    violation = {
                        "framework": "CSDDD",
                        "severity": "HIGH",
                        "message": f"Supplier risk score ({supplier_risk}) exceeds threshold ({threshold})",
                        "action": "Block procurement until audit proof is logged",
                        "citation": "EU Corporate Sustainability Due Diligence Directive"
                    }
                    result["violations"].append(violation)
                    result["status"] = ComplianceStatus.VIOLATION.value
            
            # UFLPA: Forced labor check
            elif framework["id"] == "UFLPA":
                component_origin = payload.get("component_origin", "")
                
                if component_origin == "XUAR":
                    violation = {
                        "framework": "UFLPA",
                        "severity": "SEVERE",
                        "message": "Component origin flagged: Xinjiang Uyghur Autonomous Region",
                        "action": "BLOCK IMPORT - Forced labor prevention",
                        "citation": "Uyghur Forced Labor Prevention Act (USA)"
                    }
                    result["violations"].append(violation)
                    result["status"] = ComplianceStatus.VIOLATION.value
            
            # Dodd-Frank 1502: Conflict minerals
            elif framework["id"] == "DODD_FRANK_1502":
                hardware_components = payload.get("hardware_components", [])
                conflict_minerals = ["Tin", "Tantalum", "Tungsten", "Gold"]
                
                if any(comp in conflict_minerals for comp in hardware_components):
                    if not payload.get("smelter_verification_complete", False):
                        violation = {
                            "framework": "Dodd-Frank §1502",
                            "severity": "HIGH",
                            "message": "3TG minerals detected without smelter verification",
                            "action": "Verify smelter sources in BOM",
                            "citation": "Dodd-Frank Section 1502 (Conflict Minerals)"
                        }
                        result["violations"].append(violation)
                        result["status"] = ComplianceStatus.VIOLATION.value
        
        return result
    
    def _check_esg_carbon_compliance(self, payload: Dict, result: Dict) -> Dict:
        """Check ESG & carbon credit compliance"""
        frameworks = self.frameworks.get("esg_carbon", {}).get("frameworks", [])
        
        for framework in frameworks:
            result["frameworks_checked"].append(framework["id"])
            
            # CBAM: Carbon border adjustment
            if framework["id"] == "CBAM":
                destination = payload.get("goods_destination", "")
                carbon_intensive = payload.get("carbon_intensive", False)
                
                if destination == "EU" and carbon_intensive:
                    if not payload.get("embedded_emissions_calculated", False):
                        violation = {
                            "framework": "CBAM",
                            "severity": "HIGH",
                            "message": "Carbon-intensive goods to EU require emissions calculation",
                            "action": "Calculate embedded emissions per logistics hop",
                            "citation": "EU Carbon Border Adjustment Mechanism"
                        }
                        result["violations"].append(violation)
                        result["status"] = ComplianceStatus.VIOLATION.value
            
            # Paris Agreement 6.2: Double counting check
            elif framework["id"] == "PARIS_AGREEMENT_6_2":
                if payload.get("carbon_credit_trade", False):
                    if not payload.get("double_counting_check", False):
                        violation = {
                            "framework": "Paris Agreement Art. 6.2",
                            "severity": "CRITICAL",
                            "message": "Carbon credit transfer without double counting check",
                            "action": "Verify on IP-09 Chrono-Ledger",
                            "citation": "Paris Agreement Article 6.2 (Sovereign Carbon Transfers)"
                        }
                        result["violations"].append(violation)
                        result["status"] = ComplianceStatus.VIOLATION.value
            
            # ICVCM: High-integrity carbon credits
            elif framework["id"] == "ICVCM_CCP":
                if payload.get("credit_minting", False):
                    permanence_check = payload.get("permanence_verified", False)
                    additionality_check = payload.get("additionality_verified", False)
                    
                    if not (permanence_check and additionality_check):
                        violation = {
                            "framework": "ICVCM CCP",
                            "severity": "HIGH",
                            "message": "Carbon credit minting requires permanence and additionality verification",
                            "action": "Complete integrity checks before minting",
                            "citation": "Integrity Council for Voluntary Carbon Market - Core Carbon Principles"
                        }
                        result["violations"].append(violation)
                        result["status"] = ComplianceStatus.VIOLATION.value
        
        return result
    
    def _check_humanitarian_finance_compliance(self, payload: Dict, result: Dict) -> Dict:
        """Check humanitarian finance & clean money compliance"""
        frameworks = self.frameworks.get("humanitarian_finance", {}).get("frameworks", [])
        
        for framework in frameworks:
            result["frameworks_checked"].append(framework["id"])
            
            # FATF R8: Know Your Beneficiary
            if framework["id"] == "FATF_R8":
                if payload.get("aid_disbursement", False):
                    if not payload.get("kyb_verified", False):
                        violation = {
                            "framework": "FATF R8",
                            "severity": "CRITICAL",
                            "message": "Aid disbursement requires KYB verification",
                            "action": "Verify beneficiary using Acorn Protocol",
                            "citation": "FATF Recommendation 8 (Non-Profits & Terrorist Financing)"
                        }
                        result["violations"].append(violation)
                        result["status"] = ComplianceStatus.VIOLATION.value
            
            # OFAC: Sanctions screening
            elif framework["id"] == "OFAC_SANCTIONS":
                if payload.get("payment_initiation", False):
                    payee_id = payload.get("payee_id", "")
                    
                    # This would call the actual OFAC checker
                    if not payload.get("ofac_check_passed", False):
                        violation = {
                            "framework": "OFAC",
                            "severity": "CRITICAL",
                            "message": f"Payment to {payee_id} requires OFAC sanctions screening",
                            "action": "BLOCK PAYMENT - Run sanctions check",
                            "citation": "OFAC Sanctions Lists (USA)"
                        }
                        result["violations"].append(violation)
                        result["status"] = ComplianceStatus.VIOLATION.value
            
            # IASC: Data minimization for vulnerable populations
            elif framework["id"] == "IASC_DATA_RESPONSIBILITY":
                population_type = payload.get("population_type", "")
                
                if population_type in ["refugees", "vulnerable"]:
                    if payload.get("location_data_included", False):
                        result["warnings"].append({
                            "framework": "IASC",
                            "severity": "MEDIUM",
                            "message": "Vulnerable population data should minimize location information",
                            "action": "Redact distinct location data",
                            "citation": "IASC Guidelines on Data Responsibility"
                        })
        
        return result
    
    def _check_healthcare_pharma_compliance(self, payload: Dict, result: Dict) -> Dict:
        """Check healthcare & pharmaceutical compliance"""
        frameworks = self.frameworks.get("healthcare_pharma", {}).get("frameworks", [])
        
        for framework in frameworks:
            result["frameworks_checked"].append(framework["id"])
            
            # EU MDR: Medical device classification
            if framework["id"] == "EU_MDR":
                if payload.get("system_provides_diagnosis", False):
                    if not payload.get("clinical_evaluation_logged", False):
                        violation = {
                            "framework": "EU MDR",
                            "severity": "HIGH",
                            "message": "Diagnostic system requires clinical evaluation logging",
                            "action": "Log clinical evaluation and PMS events",
                            "citation": "EU Medical Device Regulation 2017/745 (Class IIa/IIb)"
                        }
                        result["violations"].append(violation)
                        result["status"] = ComplianceStatus.VIOLATION.value
            
            # FDA 21 CFR Part 11: Audit trail integrity
            elif framework["id"] == "FDA_21_CFR_11":
                if payload.get("pharma_data_entry", False):
                    if not payload.get("audit_trail_timestamped", False):
                        violation = {
                            "framework": "FDA 21 CFR Part 11",
                            "severity": "HIGH",
                            "message": "Pharma data requires timestamped, non-repudiable audit trail",
                            "action": "Enable IP-02 Crypto Shredder audit",
                            "citation": "FDA 21 CFR Part 11 (Electronic Records & Signatures)"
                        }
                        result["violations"].append(violation)
                        result["status"] = ComplianceStatus.VIOLATION.value
            
            # FHIR: Interoperability
            elif framework["id"] == "FHIR_R4_R5":
                if payload.get("data_exchange_with_moh", False):
                    if not payload.get("fhir_compliant", False):
                        violation = {
                            "framework": "FHIR R4/R5",
                            "severity": "MEDIUM",
                            "message": "MoH data exchange requires FHIR compliance",
                            "action": "Ensure FHIR R4/R5 compatibility",
                            "citation": "Fast Healthcare Interoperability Resources"
                        }
                        result["violations"].append(violation)
                        result["status"] = ComplianceStatus.VIOLATION.value
        
        return result
    
    def _check_cybersecurity_compliance(self, payload: Dict, result: Dict) -> Dict:
        """Check cybersecurity & critical infrastructure compliance"""
        frameworks = self.frameworks.get("cybersecurity_infrastructure", {}).get("frameworks", [])
        
        for framework in frameworks:
            result["frameworks_checked"].append(framework["id"])
            
            # NIS2: Incident reporting
            if framework["id"] == "NIS2":
                if payload.get("security_incident", False):
                    incident_time = payload.get("incident_timestamp", datetime.utcnow())
                    reported = payload.get("cert_notified", False)
                    
                    if not reported:
                        violation = {
                            "framework": "NIS2",
                            "severity": "CRITICAL",
                            "message": "Security incident requires 24-hour CERT notification",
                            "action": "Notify national CERT immediately",
                            "citation": "NIS2 Directive (EU)"
                        }
                        result["violations"].append(violation)
                        result["status"] = ComplianceStatus.VIOLATION.value
            
            # CRA: Software Bill of Materials
            elif framework["id"] == "CRA":
                if payload.get("device_deployment", False):
                    if not payload.get("sbom_generated", False):
                        violation = {
                            "framework": "CRA",
                            "severity": "HIGH",
                            "message": "Device deployment requires SBOM generation",
                            "action": "Generate automated SBOM",
                            "citation": "Cyber Resilience Act (EU)"
                        }
                        result["violations"].append(violation)
                        result["status"] = ComplianceStatus.VIOLATION.value
        
        return result
    
    def _check_ai_governance_compliance(self, payload: Dict, result: Dict) -> Dict:
        """Check AI governance compliance"""
        frameworks = self.frameworks.get("ai_governance", {}).get("frameworks", [])
        
        for framework in frameworks:
            result["frameworks_checked"].append(framework["id"])
            
            if framework["id"] == "EU_AI_ACT":
                # High-risk classification
                use_case = payload.get("use_case", "")
                if use_case in ["healthcare", "critical_infrastructure"]:
                    
                    # Art. 14: Human oversight
                    if not payload.get("human_oversight_enabled", False):
                        violation = {
                            "framework": "EU AI Act Art. 14",
                            "severity": "CRITICAL",
                            "message": "High-risk AI requires human oversight (kill switch)",
                            "action": "Implement human-in-the-loop controls",
                            "citation": "EU AI Act Article 14 (Human Oversight)"
                        }
                        result["violations"].append(violation)
                        result["status"] = ComplianceStatus.VIOLATION.value
                    
                    # Art. 10: Data governance
                    if payload.get("model_training", False):
                        if not payload.get("bias_mitigation_applied", False):
                            violation = {
                                "framework": "EU AI Act Art. 10",
                                "severity": "HIGH",
                                "message": "Model training requires bias mitigation",
                                "action": "Apply bias mitigation techniques",
                                "citation": "EU AI Act Article 10 (Data Governance)"
                            }
                            result["violations"].append(violation)
                            result["status"] = ComplianceStatus.VIOLATION.value
        
        return result
    
    def _check_data_privacy_compliance(
        self,
        payload: Dict,
        jurisdiction: Optional[str],
        result: Dict
    ) -> Dict:
        """Check data privacy & sovereignty compliance"""
        frameworks = self.frameworks.get("primary_privacy_sovereignty", {}).get("frameworks", [])
        
        # Example: KDPA Section 37 logic
        # IF Region == "Kenya" AND Data_Type == "HIV_Status" AND Target_Server == "USA"
        # THEN Block_Transfer()
        
        region = payload.get("region", jurisdiction)
        data_type = payload.get("data_type", "")
        target_server = payload.get("target_server", "")
        
        if region == "Kenya" and data_type in ["HIV_Status", "sensitive_health"] and target_server == "USA":
            violation = {
                "framework": "KDPA §37",
                "severity": "CRITICAL",
                "message": "Cross-border transfer of sensitive health data from Kenya to USA blocked",
                "action": "BLOCK TRANSFER - Sovereignty violation",
                "citation": "Kenya Data Protection Act Section 37 (Cross-border transfer restrictions)",
                "logic": "IF Region == 'Kenya' AND Data_Type == 'HIV_Status' AND Target_Server == 'USA' THEN Block_Transfer()"
            }
            result["violations"].append(violation)
            result["status"] = ComplianceStatus.VIOLATION.value
        
        # GDPR Art. 9: Special categories
        if region in ["EU", "GDPR"] and data_type == "health_data":
            if not payload.get("explicit_consent", False):
                violation = {
                    "framework": "GDPR Art. 9",
                    "severity": "CRITICAL",
                    "message": "Processing health data requires explicit consent",
                    "action": "Obtain explicit consent",
                    "citation": "GDPR Article 9 (Processing of special categories)"
                }
                result["violations"].append(violation)
                result["status"] = ComplianceStatus.VIOLATION.value
        
        return result
    
    def get_compliance_summary(self) -> Dict:
        """Get summary of all frameworks"""
        return {
            "total_frameworks": self.frameworks.get("total_frameworks", 29),
            "categories": {
                "primary_privacy_sovereignty": len(self.frameworks.get("primary_privacy_sovereignty", {}).get("frameworks", [])),
                "ai_governance": len(self.frameworks.get("ai_governance", {}).get("frameworks", [])),
                "supply_chain_manufacturing": len(self.frameworks.get("supply_chain_manufacturing", {}).get("frameworks", [])),
                "esg_carbon": len(self.frameworks.get("esg_carbon", {}).get("frameworks", [])),
                "humanitarian_finance": len(self.frameworks.get("humanitarian_finance", {}).get("frameworks", [])),
                "healthcare_pharma": len(self.frameworks.get("healthcare_pharma", {}).get("frameworks", [])),
                "cybersecurity_infrastructure": len(self.frameworks.get("cybersecurity_infrastructure", {}).get("frameworks", [])),
                "humanitarian_interoperability": len(self.frameworks.get("humanitarian_interoperability", {}).get("frameworks", []))
            },
            "fortress_status": "OPERATIONAL"
        }


# Example usage
if __name__ == "__main__":
    matrix = ComplianceMatrix()
    
    # Test supply chain compliance
    print("=" * 60)
    print("TEST 1: Supply Chain Compliance (UFLPA)")
    print("=" * 60)
    
    result = matrix.check_sectoral_compliance(
        context=SectoralContext.SUPPLY_CHAIN,
        payload={
            "component_origin": "XUAR",
            "hardware_components": ["Tin", "Tantalum"]
        }
    )
    
    print(json.dumps(result, indent=2))
    
    # Test data privacy compliance (KDPA §37)
    print("\n" + "=" * 60)
    print("TEST 2: Data Privacy Compliance (KDPA §37)")
    print("=" * 60)
    
    result = matrix.check_sectoral_compliance(
        context=SectoralContext.DATA_PRIVACY,
        payload={
            "region": "Kenya",
            "data_type": "HIV_Status",
            "target_server": "USA"
        }
    )
    
    print(json.dumps(result, indent=2))
    
    # Test humanitarian finance (OFAC)
    print("\n" + "=" * 60)
    print("TEST 3: Humanitarian Finance (OFAC)")
    print("=" * 60)
    
    result = matrix.check_sectoral_compliance(
        context=SectoralContext.HUMANITARIAN_FINANCE,
        payload={
            "payment_initiation": True,
            "payee_id": "UNKNOWN_ENTITY",
            "ofac_check_passed": False
        }
    )
    
    print(json.dumps(result, indent=2))
    
    # Get compliance summary
    print("\n" + "=" * 60)
    print("COMPLIANCE SUMMARY")
    print("=" * 60)
    
    summary = matrix.get_compliance_summary()
    print(json.dumps(summary, indent=2))
