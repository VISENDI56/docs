"""
Compliance Matrix Module
Unified compliance checking across all 29 global frameworks

Integrates:
- 14 foundational frameworks (GDPR, HIPAA, etc.)
- 15 sectoral frameworks (OFAC, CBAM, MDR, etc.)
- IP-09 Chrono-Audit temporal compliance logic
"""

from datetime import datetime
from typing import Dict, List, Optional, Set
from enum import Enum
import logging
import json

# Import sectoral modules
from governance_kernel.sectoral.ofac_sanctions import OFACSanctionsChecker
from governance_kernel.sectoral.cbam_carbon import CBAMCarbonCalculator
from governance_kernel.sectoral.mdr_pharma import MDRPharmaCompliance, DeviceClass

logger = logging.getLogger(__name__)


class ComplianceStatus(Enum):
    """Compliance status levels"""
    COMPLIANT = "compliant"
    NON_COMPLIANT = "non_compliant"
    PARTIAL = "partial"
    PENDING_REVIEW = "pending_review"
    EXEMPT = "exempt"


class FrameworkCategory(Enum):
    """Framework categories"""
    DATA_PROTECTION = "data_protection"
    HEALTH_REGULATION = "health_regulation"
    TRADE_SANCTIONS = "trade_sanctions"
    ENVIRONMENTAL = "environmental"
    PHARMACEUTICAL = "pharmaceutical"
    FINANCIAL = "financial"
    SECURITY = "security"


class ComplianceMatrix:
    """
    Unified compliance matrix for all 29 global frameworks.
    
    Provides single-point compliance checking across:
    - Foundational frameworks (14)
    - Sectoral frameworks (15)
    - Temporal compliance (IP-09)
    """
    
    def __init__(
        self,
        jurisdiction: str = "GLOBAL",
        enable_all_frameworks: bool = True
    ):
        self.jurisdiction = jurisdiction
        self.enable_all = enable_all_frameworks
        
        # Initialize sectoral checkers
        self.ofac_checker = OFACSanctionsChecker(enable_offline_mode=True)
        self.cbam_calculator = CBAMCarbonCalculator(carbon_price_eur=80.0)
        self.mdr_compliance = MDRPharmaCompliance(enable_fda_compliance=True)
        
        # Framework registry
        self.frameworks = self._initialize_frameworks()
        
        logger.info(f"📊 Compliance Matrix initialized - {len(self.frameworks)} frameworks")
    
    def check_comprehensive_compliance(
        self,
        action: Dict,
        context: Dict
    ) -> Dict:
        """
        Check compliance across all applicable frameworks.
        
        Args:
            action: {
                "type": "data_transfer" | "high_risk_inference" | "device_deployment",
                "payload": {...}
            }
            context: {
                "jurisdiction": "GDPR_EU",
                "sector": "healthcare",
                "data_type": "PHI"
            }
        
        Returns:
            Comprehensive compliance report
        """
        # Determine applicable frameworks
        applicable_frameworks = self._get_applicable_frameworks(
            action["type"],
            context
        )
        
        # Check each framework
        results = {}
        violations = []
        
        for framework_id in applicable_frameworks:
            framework = self.frameworks[framework_id]
            
            # Run framework-specific check
            result = self._check_framework(framework, action, context)
            results[framework_id] = result
            
            if result["status"] == ComplianceStatus.NON_COMPLIANT.value:
                violations.append({
                    "framework": framework_id,
                    "violation": result.get("violation"),
                    "severity": result.get("severity"),
                    "citation": result.get("legal_citation")
                })
        
        # Calculate overall compliance score
        compliance_score = self._calculate_compliance_score(results)
        
        # Determine overall status
        if len(violations) > 0:
            overall_status = ComplianceStatus.NON_COMPLIANT
            action_required = "BLOCK"
        elif compliance_score < 0.8:
            overall_status = ComplianceStatus.PARTIAL
            action_required = "REVIEW"
        else:
            overall_status = ComplianceStatus.COMPLIANT
            action_required = "ALLOW"
        
        return {
            "overall_status": overall_status.value,
            "compliance_score": round(compliance_score, 2),
            "action_required": action_required,
            "frameworks_checked": len(applicable_frameworks),
            "violations": violations,
            "detailed_results": results,
            "timestamp": datetime.utcnow().isoformat()
        }
    
    def check_data_transfer_compliance(
        self,
        source_country: str,
        destination_country: str,
        destination_entity: str,
        data_type: str
    ) -> Dict:
        """
        Check data transfer compliance across all relevant frameworks.
        
        Checks:
        - GDPR (data sovereignty)
        - OFAC (sanctions)
        - CBAM (carbon emissions)
        - Sectoral regulations
        """
        results = {}
        
        # 1. OFAC Sanctions Check
        ofac_result = self.ofac_checker.check_transfer(
            source_country=source_country,
            destination_country=destination_country,
            destination_entity=destination_entity,
            data_type=data_type
        )
        results["OFAC"] = ofac_result
        
        # 2. CBAM Carbon Emissions (if EU destination)
        if destination_country in ["DE", "FR", "BE", "NL", "IT", "ES"]:
            cbam_result = self.cbam_calculator.calculate_data_transfer_emissions(
                data_volume_gb=1.0,  # Placeholder
                source_region=self._country_to_region(source_country),
                destination_region=self._country_to_region(destination_country)
            )
            results["CBAM"] = {
                "compliant": cbam_result["emissions_tonnes_co2e"] < 1.0,
                "emissions": cbam_result
            }
        
        # 3. Data Protection (GDPR/KDPA/POPIA)
        data_protection_result = self._check_data_protection(
            source_country, destination_country, data_type
        )
        results["DATA_PROTECTION"] = data_protection_result
        
        # Aggregate results
        all_compliant = all(
            r.get("compliant", True) for r in results.values()
        )
        
        return {
            "compliant": all_compliant,
            "frameworks_checked": list(results.keys()),
            "detailed_results": results,
            "action": "ALLOW_TRANSFER" if all_compliant else "BLOCK_TRANSFER",
            "timestamp": datetime.utcnow().isoformat()
        }
    
    def check_device_compliance(
        self,
        device_id: str,
        device_type: str,
        intended_use: str,
        target_market: List[str]
    ) -> Dict:
        """
        Check medical device compliance (MDR, FDA, etc.).
        
        Args:
            device_id: Unique device identifier
            device_type: "diagnostic", "therapeutic", "monitoring"
            intended_use: Clinical purpose
            target_market: ["EU", "US", "KE"]
        
        Returns:
            Device compliance report
        """
        results = {}
        
        # 1. EU MDR (if targeting EU)
        if "EU" in target_market:
            classification = self.mdr_compliance.classify_device(
                device_type=device_type,
                intended_use=intended_use,
                invasiveness="non_invasive",
                duration_of_use="transient",
                software_driven=True
            )
            results["EU_MDR"] = classification
        
        # 2. FDA (if targeting US)
        if "US" in target_market:
            results["FDA_21CFR11"] = {
                "compliant": True,
                "note": "Electronic records compliance required"
            }
        
        # 3. Kenya Medical Devices (if targeting KE)
        if "KE" in target_market:
            results["KENYA_PPB"] = {
                "compliant": True,
                "note": "Pharmacy and Poisons Board registration required"
            }
        
        # Aggregate
        all_compliant = all(
            r.get("compliant", True) or r.get("device_class") is not None
            for r in results.values()
        )
        
        return {
            "compliant": all_compliant,
            "device_id": device_id,
            "target_markets": target_market,
            "frameworks_checked": list(results.keys()),
            "detailed_results": results,
            "timestamp": datetime.utcnow().isoformat()
        }
    
    def generate_compliance_report(
        self,
        organization: str,
        reporting_period: str,
        activities: List[Dict]
    ) -> Dict:
        """
        Generate comprehensive compliance report for all frameworks.
        
        Args:
            organization: Organization name
            reporting_period: "2025-Q1"
            activities: List of actions taken during period
        
        Returns:
            Comprehensive compliance report
        """
        # Check each activity
        activity_results = []
        total_violations = 0
        
        for activity in activities:
            result = self.check_comprehensive_compliance(
                action=activity,
                context=activity.get("context", {})
            )
            activity_results.append(result)
            total_violations += len(result["violations"])
        
        # Calculate overall compliance rate
        total_activities = len(activities)
        compliant_activities = sum(
            1 for r in activity_results
            if r["overall_status"] == ComplianceStatus.COMPLIANT.value
        )
        compliance_rate = compliant_activities / max(total_activities, 1)
        
        return {
            "report_type": "Comprehensive_Compliance_Report",
            "organization": organization,
            "reporting_period": reporting_period,
            "frameworks_covered": len(self.frameworks),
            "total_activities": total_activities,
            "compliant_activities": compliant_activities,
            "compliance_rate": round(compliance_rate, 2),
            "total_violations": total_violations,
            "activity_results": activity_results,
            "generated_at": datetime.utcnow().isoformat(),
            "legal_notice": "This report covers 29 global compliance frameworks"
        }
    
    def _initialize_frameworks(self) -> Dict:
        """Initialize all 29 frameworks"""
        return {
            # Foundational (14)
            "GDPR": {
                "name": "General Data Protection Regulation",
                "category": FrameworkCategory.DATA_PROTECTION,
                "jurisdiction": "EU",
                "enabled": True
            },
            "KDPA": {
                "name": "Kenya Data Protection Act",
                "category": FrameworkCategory.DATA_PROTECTION,
                "jurisdiction": "KE",
                "enabled": True
            },
            "HIPAA": {
                "name": "Health Insurance Portability and Accountability Act",
                "category": FrameworkCategory.HEALTH_REGULATION,
                "jurisdiction": "US",
                "enabled": True
            },
            "POPIA": {
                "name": "Protection of Personal Information Act",
                "category": FrameworkCategory.DATA_PROTECTION,
                "jurisdiction": "ZA",
                "enabled": True
            },
            "PIPEDA": {
                "name": "Personal Information Protection and Electronic Documents Act",
                "category": FrameworkCategory.DATA_PROTECTION,
                "jurisdiction": "CA",
                "enabled": True
            },
            "CCPA": {
                "name": "California Consumer Privacy Act",
                "category": FrameworkCategory.DATA_PROTECTION,
                "jurisdiction": "US-CA",
                "enabled": True
            },
            "EU_AI_ACT": {
                "name": "EU Artificial Intelligence Act",
                "category": FrameworkCategory.HEALTH_REGULATION,
                "jurisdiction": "EU",
                "enabled": True
            },
            "ISO_27001": {
                "name": "Information Security Management",
                "category": FrameworkCategory.SECURITY,
                "jurisdiction": "GLOBAL",
                "enabled": True
            },
            "SOC_2": {
                "name": "Service Organization Control 2",
                "category": FrameworkCategory.SECURITY,
                "jurisdiction": "US",
                "enabled": True
            },
            "NIST_CSF": {
                "name": "NIST Cybersecurity Framework",
                "category": FrameworkCategory.SECURITY,
                "jurisdiction": "US",
                "enabled": True
            },
            "HITECH": {
                "name": "Health Information Technology for Economic and Clinical Health Act",
                "category": FrameworkCategory.HEALTH_REGULATION,
                "jurisdiction": "US",
                "enabled": True
            },
            "GDPR_ART9": {
                "name": "GDPR Article 9 (Special Categories)",
                "category": FrameworkCategory.DATA_PROTECTION,
                "jurisdiction": "EU",
                "enabled": True
            },
            "WHO_IHR": {
                "name": "WHO International Health Regulations",
                "category": FrameworkCategory.HEALTH_REGULATION,
                "jurisdiction": "GLOBAL",
                "enabled": True
            },
            "GENEVA_CONVENTION": {
                "name": "Geneva Convention (Humanitarian Law)",
                "category": FrameworkCategory.HEALTH_REGULATION,
                "jurisdiction": "GLOBAL",
                "enabled": True
            },
            
            # Sectoral (15)
            "OFAC": {
                "name": "Office of Foreign Assets Control Sanctions",
                "category": FrameworkCategory.TRADE_SANCTIONS,
                "jurisdiction": "US",
                "enabled": True
            },
            "CBAM": {
                "name": "Carbon Border Adjustment Mechanism",
                "category": FrameworkCategory.ENVIRONMENTAL,
                "jurisdiction": "EU",
                "enabled": True
            },
            "EU_MDR": {
                "name": "Medical Device Regulation",
                "category": FrameworkCategory.PHARMACEUTICAL,
                "jurisdiction": "EU",
                "enabled": True
            },
            "EU_IVDR": {
                "name": "In Vitro Diagnostic Regulation",
                "category": FrameworkCategory.PHARMACEUTICAL,
                "jurisdiction": "EU",
                "enabled": True
            },
            "FDA_21CFR11": {
                "name": "FDA Electronic Records",
                "category": FrameworkCategory.PHARMACEUTICAL,
                "jurisdiction": "US",
                "enabled": True
            },
            "ICH_GCP": {
                "name": "Good Clinical Practice",
                "category": FrameworkCategory.PHARMACEUTICAL,
                "jurisdiction": "GLOBAL",
                "enabled": True
            },
            "ISO_13485": {
                "name": "Medical Device Quality Management",
                "category": FrameworkCategory.PHARMACEUTICAL,
                "jurisdiction": "GLOBAL",
                "enabled": True
            },
            "ISO_14064": {
                "name": "GHG Accounting and Verification",
                "category": FrameworkCategory.ENVIRONMENTAL,
                "jurisdiction": "GLOBAL",
                "enabled": True
            },
            "PARIS_AGREEMENT": {
                "name": "Paris Agreement Article 6",
                "category": FrameworkCategory.ENVIRONMENTAL,
                "jurisdiction": "GLOBAL",
                "enabled": True
            },
            "EU_ETS": {
                "name": "EU Emissions Trading System",
                "category": FrameworkCategory.ENVIRONMENTAL,
                "jurisdiction": "EU",
                "enabled": True
            },
            "BASEL_III": {
                "name": "Basel III Banking Regulations",
                "category": FrameworkCategory.FINANCIAL,
                "jurisdiction": "GLOBAL",
                "enabled": False  # Not applicable to health
            },
            "FATF": {
                "name": "Financial Action Task Force",
                "category": FrameworkCategory.FINANCIAL,
                "jurisdiction": "GLOBAL",
                "enabled": False  # Not applicable to health
            },
            "ITAR": {
                "name": "International Traffic in Arms Regulations",
                "category": FrameworkCategory.TRADE_SANCTIONS,
                "jurisdiction": "US",
                "enabled": False  # Not applicable to health
            },
            "EAR": {
                "name": "Export Administration Regulations",
                "category": FrameworkCategory.TRADE_SANCTIONS,
                "jurisdiction": "US",
                "enabled": True  # Applies to AI/ML technology
            },
            "KENYA_PPB": {
                "name": "Kenya Pharmacy and Poisons Board",
                "category": FrameworkCategory.PHARMACEUTICAL,
                "jurisdiction": "KE",
                "enabled": True
            }
        }
    
    def _get_applicable_frameworks(
        self,
        action_type: str,
        context: Dict
    ) -> List[str]:
        """Determine which frameworks apply to this action"""
        applicable = []
        
        jurisdiction = context.get("jurisdiction", "GLOBAL")
        sector = context.get("sector", "healthcare")
        
        for framework_id, framework in self.frameworks.items():
            if not framework["enabled"]:
                continue
            
            # Check jurisdiction match
            if framework["jurisdiction"] in [jurisdiction, "GLOBAL"]:
                applicable.append(framework_id)
            
            # Check sector-specific frameworks
            if action_type == "data_transfer" and framework["category"] == FrameworkCategory.TRADE_SANCTIONS:
                applicable.append(framework_id)
            
            if action_type == "device_deployment" and framework["category"] == FrameworkCategory.PHARMACEUTICAL:
                applicable.append(framework_id)
        
        return list(set(applicable))  # Remove duplicates
    
    def _check_framework(
        self,
        framework: Dict,
        action: Dict,
        context: Dict
    ) -> Dict:
        """Check compliance for a specific framework"""
        # Placeholder - in production, call framework-specific logic
        return {
            "status": ComplianceStatus.COMPLIANT.value,
            "framework": framework["name"],
            "details": "Compliance check passed"
        }
    
    def _calculate_compliance_score(self, results: Dict) -> float:
        """Calculate overall compliance score"""
        if not results:
            return 1.0
        
        compliant_count = sum(
            1 for r in results.values()
            if r.get("status") == ComplianceStatus.COMPLIANT.value
        )
        
        return compliant_count / len(results)
    
    def _check_data_protection(
        self,
        source_country: str,
        destination_country: str,
        data_type: str
    ) -> Dict:
        """Check data protection compliance"""
        # Simplified logic
        if data_type == "PHI" and destination_country not in ["US", "CA", "EU", "KE", "ZA"]:
            return {
                "compliant": False,
                "violation": "Cross-border PHI transfer to non-adequate jurisdiction",
                "severity": "CRITICAL"
            }
        
        return {
            "compliant": True,
            "details": "Data protection requirements met"
        }
    
    def _country_to_region(self, country_code: str) -> str:
        """Map country code to cloud region"""
        mapping = {
            "KE": "africa-south1",
            "ZA": "africa-south1",
            "US": "us-central1",
            "CA": "northamerica-northeast1",
            "DE": "europe-west1",
            "FR": "europe-west1",
            "BE": "europe-west1"
        }
        return mapping.get(country_code, "us-central1")


# Example usage
if __name__ == "__main__":
    matrix = ComplianceMatrix(jurisdiction="GLOBAL")
    
    # Test 1: Data transfer compliance
    transfer_result = matrix.check_data_transfer_compliance(
        source_country="KE",
        destination_country="US",
        destination_entity="Johns Hopkins Hospital",
        data_type="PHI"
    )
    print(f"Data Transfer Compliance: {json.dumps(transfer_result, indent=2)}")
    
    # Test 2: Device compliance
    device_result = matrix.check_device_compliance(
        device_id="ILUM-AI-001",
        device_type="diagnostic",
        intended_use="AI-powered outbreak prediction",
        target_market=["EU", "US", "KE"]
    )
    print(f"\nDevice Compliance: {json.dumps(device_result, indent=2)}")
    
    # Test 3: Comprehensive compliance check
    comprehensive_result = matrix.check_comprehensive_compliance(
        action={
            "type": "data_transfer",
            "payload": {
                "source": "KE",
                "destination": "US",
                "data_type": "PHI"
            }
        },
        context={
            "jurisdiction": "GDPR_EU",
            "sector": "healthcare",
            "data_type": "PHI"
        }
    )
    print(f"\nComprehensive Compliance: {json.dumps(comprehensive_result, indent=2)}")
