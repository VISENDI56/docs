"""
Sectoral Compliance Module for iLuminara Governance Kernel
Implements 15 additional global frameworks across 5 sectors

Sectors:
1. Supply Chain & Manufacturing (Ethical Operations Stack)
2. ESG & Carbon Credits (Green Sovereign Stack)
3. Humanitarian Finance & Non-Profit (Clean Money Stack)
4. Healthcare & Pharma (Clinical Grade Stack)
5. Cybersecurity & Critical Infrastructure (Digital Fortress Stack)

Total Frameworks: 29 (14 base + 15 sectoral)
"""

import json
import os
import hashlib
from datetime import datetime
from typing import Dict, List, Optional, Tuple
from enum import Enum
import logging
from fuzzywuzzy import fuzz
import requests

logger = logging.getLogger(__name__)


class SectoralContext(Enum):
    """Sectoral contexts for compliance checking"""
    SUPPLY_CHAIN = "supply_chain"
    PROCUREMENT = "procurement"
    ESG_CARBON = "esg_carbon"
    HUMANITARIAN_FINANCE = "humanitarian_finance"
    HEALTHCARE_PHARMA = "healthcare_pharma"
    CYBERSECURITY = "cybersecurity"
    CLINICAL_TRIALS = "clinical_trials"
    CARBON_TRADING = "carbon_trading"


class ComplianceViolation(Exception):
    """Raised when sectoral compliance check fails"""
    pass


class SectoralCompliance:
    """
    Sectoral Abstraction Layer for the Governance Kernel
    Implements 15 additional global frameworks
    """
    
    def __init__(self, config_path: str = "governance_kernel/sectoral_laws.json"):
        self.config_path = config_path
        self.frameworks = self._load_frameworks()
        self.sanctions_cache = {}
        self.sanctions_cache_ttl = 86400  # 24 hours
        
        logger.info(f"🌐 Sectoral Compliance initialized - {len(self.frameworks)} frameworks loaded")
    
    def _load_frameworks(self) -> Dict:
        """Load sectoral frameworks from JSON"""
        if not os.path.exists(self.config_path):
            logger.warning(f"⚠️ Sectoral laws config not found: {self.config_path}")
            return {}
        
        with open(self.config_path, 'r') as f:
            return json.load(f)
    
    def check_sectoral_compliance(
        self,
        context: SectoralContext,
        payload: Dict,
        jurisdiction: Optional[str] = None
    ) -> Dict:
        """
        Main entry point for sectoral compliance checking
        
        Args:
            context: Sectoral context (supply_chain, esg_carbon, etc.)
            payload: Action payload with relevant data
            jurisdiction: Optional jurisdiction override
        
        Returns:
            Compliance result with applicable frameworks and violations
        """
        result = {
            "compliant": True,
            "context": context.value,
            "applicable_frameworks": [],
            "violations": [],
            "warnings": [],
            "timestamp": datetime.utcnow().isoformat()
        }
        
        # Find applicable frameworks for this context
        applicable = self._find_applicable_frameworks(context, payload)
        
        for framework in applicable:
            framework_result = self._check_framework(framework, payload, jurisdiction)
            result["applicable_frameworks"].append(framework["id"])
            
            if not framework_result["compliant"]:
                result["compliant"] = False
                result["violations"].extend(framework_result["violations"])
            
            if framework_result.get("warnings"):
                result["warnings"].extend(framework_result["warnings"])
        
        return result
    
    def _find_applicable_frameworks(
        self,
        context: SectoralContext,
        payload: Dict
    ) -> List[Dict]:
        """Find frameworks applicable to this context and payload"""
        applicable = []
        
        for sector_name, sector_data in self.frameworks.get("sectors", {}).items():
            for framework in sector_data.get("frameworks", []):
                trigger_conditions = framework.get("trigger_conditions", {})
                
                # Check if context matches
                if context.value in trigger_conditions.get("context", []):
                    # Additional payload-based filtering
                    if self._matches_trigger_conditions(trigger_conditions, payload):
                        applicable.append(framework)
        
        return applicable
    
    def _matches_trigger_conditions(
        self,
        trigger_conditions: Dict,
        payload: Dict
    ) -> bool:
        """Check if payload matches framework trigger conditions"""
        # Check data types
        if "data_types" in trigger_conditions:
            payload_data_type = payload.get("data_type")
            if payload_data_type and payload_data_type not in trigger_conditions["data_types"]:
                return False
        
        # Check product types
        if "product_types" in trigger_conditions:
            payload_product = payload.get("product_type")
            if payload_product and payload_product not in trigger_conditions["product_types"]:
                return False
        
        # Check destination
        if "destination" in trigger_conditions:
            payload_dest = payload.get("destination")
            if payload_dest and payload_dest not in trigger_conditions["destination"]:
                return False
        
        return True
    
    def _check_framework(
        self,
        framework: Dict,
        payload: Dict,
        jurisdiction: Optional[str]
    ) -> Dict:
        """Check compliance for a specific framework"""
        result = {
            "framework_id": framework["id"],
            "framework_name": framework["name"],
            "compliant": True,
            "violations": [],
            "warnings": []
        }
        
        # Route to specific checker based on framework ID
        framework_id = framework["id"]
        
        if framework_id == "CSDDD":
            return self._check_csddd(framework, payload)
        elif framework_id == "LkSG":
            return self._check_lksg(framework, payload)
        elif framework_id == "UFLPA":
            return self._check_uflpa(framework, payload)
        elif framework_id == "DODD_FRANK_1502":
            return self._check_conflict_minerals(framework, payload)
        elif framework_id == "CBAM":
            return self._check_cbam(framework, payload)
        elif framework_id == "PARIS_ARTICLE_6_2":
            return self._check_paris_article_6(framework, payload)
        elif framework_id == "ICVCM_CCP":
            return self._check_icvcm(framework, payload)
        elif framework_id == "FATF_R8":
            return self._check_fatf_r8(framework, payload)
        elif framework_id in ["OFAC_SANCTIONS", "UN_SANCTIONS"]:
            return self._check_sanctions(framework, payload)
        elif framework_id == "IASC_DATA_RESPONSIBILITY":
            return self._check_iasc(framework, payload)
        elif framework_id == "EU_MDR":
            return self._check_eu_mdr(framework, payload)
        elif framework_id == "FDA_21_CFR_11":
            return self._check_fda_21_cfr_11(framework, payload)
        elif framework_id == "EU_CTR":
            return self._check_eu_ctr(framework, payload)
        elif framework_id == "NIS2":
            return self._check_nis2(framework, payload)
        elif framework_id == "CRA":
            return self._check_cra(framework, payload)
        
        return result
    
    # ========== SUPPLY CHAIN CHECKERS ==========
    
    def _check_csddd(self, framework: Dict, payload: Dict) -> Dict:
        """EU Corporate Sustainability Due Diligence Directive"""
        result = {"framework_id": "CSDDD", "compliant": True, "violations": [], "warnings": []}
        
        supplier_risk_score = payload.get("supplier_risk_score", 0)
        threshold = framework["enforcement_logic"]["threshold"]
        
        if supplier_risk_score > threshold:
            audit_proof = payload.get("audit_proof_logged", False)
            if not audit_proof:
                result["compliant"] = False
                result["violations"].append({
                    "rule": "CSDDD: Supplier risk exceeds threshold without audit proof",
                    "supplier_risk_score": supplier_risk_score,
                    "threshold": threshold,
                    "action_required": "Block procurement until audit proof logged"
                })
        
        return result
    
    def _check_lksg(self, framework: Dict, payload: Dict) -> Dict:
        """German Supply Chain Due Diligence Act"""
        result = {"framework_id": "LkSG", "compliant": True, "violations": [], "warnings": []}
        
        grievance_mechanism_logged = payload.get("grievance_mechanism_logged", False)
        
        if not grievance_mechanism_logged:
            result["compliant"] = False
            result["violations"].append({
                "rule": "LkSG: Grievance mechanism access must be logged for every supply chain node",
                "action_required": "Log grievance mechanism access"
            })
        
        return result
    
    def _check_uflpa(self, framework: Dict, payload: Dict) -> Dict:
        """Uyghur Forced Labor Prevention Act"""
        result = {"framework_id": "UFLPA", "compliant": True, "violations": [], "warnings": []}
        
        component_origin = payload.get("component_origin", "")
        blocked_regions = framework["enforcement_logic"]["blocked_regions"]
        
        if component_origin in blocked_regions:
            result["compliant"] = False
            result["violations"].append({
                "rule": "UFLPA: Component origin from blocked region",
                "component_origin": component_origin,
                "severity": "SEVERE",
                "action_required": "Block import and notify CBP"
            })
        
        return result
    
    def _check_conflict_minerals(self, framework: Dict, payload: Dict) -> Dict:
        """Dodd-Frank Section 1502 (Conflict Minerals)"""
        result = {"framework_id": "DODD_FRANK_1502", "compliant": True, "violations": [], "warnings": []}
        
        bom = payload.get("bill_of_materials", {})
        minerals_3tg = framework["3TG_minerals"]
        
        for mineral, ore in minerals_3tg.items():
            if mineral in bom:
                smelter_verified = bom[mineral].get("smelter_verified", False)
                if not smelter_verified:
                    result["compliant"] = False
                    result["violations"].append({
                        "rule": f"Dodd-Frank 1502: {mineral.upper()} smelter source not verified",
                        "mineral": mineral,
                        "action_required": "Verify smelter source and trace origin"
                    })
        
        return result
    
    # ========== ESG & CARBON CHECKERS ==========
    
    def _check_cbam(self, framework: Dict, payload: Dict) -> Dict:
        """EU Carbon Border Adjustment Mechanism"""
        result = {"framework_id": "CBAM", "compliant": True, "violations": [], "warnings": []}
        
        embedded_emissions = self.calculate_cbam_emissions(payload.get("logistics_data", {}))
        cbam_declaration = payload.get("cbam_declaration_filed", False)
        
        if embedded_emissions > 0 and not cbam_declaration:
            result["compliant"] = False
            result["violations"].append({
                "rule": "CBAM: Embedded emissions require CBAM declaration",
                "embedded_emissions_tco2e": embedded_emissions,
                "action_required": "File CBAM declaration and purchase certificates"
            })
        
        result["embedded_emissions_tco2e"] = embedded_emissions
        return result
    
    def calculate_cbam_emissions(self, logistics_data: Dict) -> float:
        """
        Calculate embedded emissions per logistics hop
        
        Args:
            logistics_data: Dictionary with transport modes and distances
        
        Returns:
            Total embedded emissions in tCO2e
        """
        emission_factors = {
            "air_freight": 0.602,  # kg CO2e per tonne-km
            "sea_freight": 0.016,
            "road_freight": 0.062,
            "rail_freight": 0.022,
            "cold_chain_multiplier": 1.5
        }
        
        total_emissions = 0.0
        
        for hop in logistics_data.get("hops", []):
            mode = hop.get("transport_mode", "road_freight")
            distance_km = hop.get("distance_km", 0)
            weight_tonnes = hop.get("weight_tonnes", 0)
            is_cold_chain = hop.get("cold_chain", False)
            
            emission_factor = emission_factors.get(mode, 0.062)
            hop_emissions = (emission_factor * distance_km * weight_tonnes) / 1000  # Convert to tonnes
            
            if is_cold_chain:
                hop_emissions *= emission_factors["cold_chain_multiplier"]
            
            total_emissions += hop_emissions
        
        return round(total_emissions, 3)
    
    def _check_paris_article_6(self, framework: Dict, payload: Dict) -> Dict:
        """Paris Agreement Article 6.2 (Sovereign Carbon Transfers)"""
        result = {"framework_id": "PARIS_ARTICLE_6_2", "compliant": True, "violations": [], "warnings": []}
        
        double_counting_check = payload.get("double_counting_check", False)
        corresponding_adjustment = payload.get("corresponding_adjustment", False)
        
        if not double_counting_check:
            result["compliant"] = False
            result["violations"].append({
                "rule": "Paris Article 6.2: Double counting check required on IP-09 Chrono-Ledger",
                "action_required": "Verify corresponding adjustment and prevent double counting"
            })
        
        if not corresponding_adjustment:
            result["warnings"].append({
                "rule": "Paris Article 6.2: Corresponding adjustment not logged",
                "recommendation": "Ensure ITMO transfer includes corresponding adjustment"
            })
        
        return result
    
    def _check_icvcm(self, framework: Dict, payload: Dict) -> Dict:
        """ICVCM Core Carbon Principles"""
        result = {"framework_id": "ICVCM_CCP", "compliant": True, "violations": [], "warnings": []}
        
        additionality_verified = payload.get("additionality_verified", False)
        permanence_verified = payload.get("permanence_verified", False)
        
        if not additionality_verified:
            result["compliant"] = False
            result["violations"].append({
                "rule": "ICVCM CCP: Additionality not verified before minting token",
                "action_required": "Verify project is beyond business-as-usual"
            })
        
        if not permanence_verified:
            result["compliant"] = False
            result["violations"].append({
                "rule": "ICVCM CCP: Permanence not verified before minting token",
                "action_required": "Verify long-term carbon storage and reversal risk management"
            })
        
        return result
    
    # ========== HUMANITARIAN FINANCE CHECKERS ==========
    
    def _check_fatf_r8(self, framework: Dict, payload: Dict) -> Dict:
        """FATF Recommendation 8 (Non-Profits & Terrorist Financing)"""
        result = {"framework_id": "FATF_R8", "compliant": True, "violations": [], "warnings": []}
        
        kyb_check = payload.get("kyb_check_completed", False)
        beneficiary_verified = payload.get("beneficiary_verified", False)
        
        if not kyb_check:
            result["compliant"] = False
            result["violations"].append({
                "rule": "FATF R8: Know Your Beneficiary (KYB) check required",
                "action_required": "Use Acorn Protocol to verify aid reached real humans"
            })
        
        if not beneficiary_verified:
            result["warnings"].append({
                "rule": "FATF R8: Beneficiary verification recommended",
                "recommendation": "Use biometric proof to prevent aid diversion"
            })
        
        return result
    
    def _check_sanctions(self, framework: Dict, payload: Dict) -> Dict:
        """OFAC/UN Sanctions Screening"""
        result = {"framework_id": framework["id"], "compliant": True, "violations": [], "warnings": []}
        
        payee_id = payload.get("payee_id", "")
        payee_name = payload.get("payee_name", "")
        
        if not payee_id and not payee_name:
            result["warnings"].append({
                "rule": f"{framework['id']}: No payee information provided",
                "recommendation": "Provide payee_id or payee_name for sanctions screening"
            })
            return result
        
        # Check sanctions (real-time fuzzy matching)
        sanctions_match = self.check_ofac(payee_id, payee_name)
        
        if sanctions_match["is_sanctioned"]:
            result["compliant"] = False
            result["violations"].append({
                "rule": f"{framework['id']}: Payee matches sanctions list",
                "payee_id": payee_id,
                "payee_name": payee_name,
                "match_score": sanctions_match["match_score"],
                "sanctions_list": sanctions_match["list_name"],
                "action_required": "Block transaction and freeze funds"
            })
        
        return result
    
    def check_ofac(self, user_id: str, user_name: str = "") -> Dict:
        """
        Check OFAC sanctions list with fuzzy matching
        
        Args:
            user_id: User identifier
            user_name: User name for fuzzy matching
        
        Returns:
            Sanctions check result
        """
        # Check cache first
        cache_key = hashlib.sha256(f"{user_id}:{user_name}".encode()).hexdigest()
        
        if cache_key in self.sanctions_cache:
            cached = self.sanctions_cache[cache_key]
            if (datetime.utcnow() - cached["timestamp"]).total_seconds() < self.sanctions_cache_ttl:
                return cached["result"]
        
        # In production, this would call real OFAC API
        # For now, simulate with known sanctioned entities
        sanctioned_entities = [
            "SANCTIONED_ENTITY_1",
            "BLOCKED_PERSON",
            "TERRORIST_ORG"
        ]
        
        is_sanctioned = False
        match_score = 0.0
        list_name = ""
        
        # Exact match on ID
        if user_id in sanctioned_entities:
            is_sanctioned = True
            match_score = 1.0
            list_name = "OFAC_SDN"
        
        # Fuzzy match on name
        if user_name:
            for sanctioned in sanctioned_entities:
                score = fuzz.ratio(user_name.upper(), sanctioned.upper()) / 100.0
                if score > 0.85:  # 85% match threshold
                    is_sanctioned = True
                    match_score = score
                    list_name = "OFAC_SDN"
                    break
        
        result = {
            "is_sanctioned": is_sanctioned,
            "match_score": match_score,
            "list_name": list_name,
            "checked_at": datetime.utcnow().isoformat()
        }
        
        # Cache result
        self.sanctions_cache[cache_key] = {
            "result": result,
            "timestamp": datetime.utcnow()
        }
        
        return result
    
    def _check_iasc(self, framework: Dict, payload: Dict) -> Dict:
        """IASC Guidelines on Data Responsibility"""
        result = {"framework_id": "IASC_DATA_RESPONSIBILITY", "compliant": True, "violations": [], "warnings": []}
        
        population_type = payload.get("population_type", "")
        location_data = payload.get("location_data", {})
        
        vulnerable_populations = framework["vulnerable_populations"]
        
        if population_type in vulnerable_populations:
            requirements = vulnerable_populations[population_type]
            
            # Check location data redaction for refugees
            if population_type == "refugees":
                if location_data.get("precise_coordinates") and not location_data.get("redacted"):
                    result["compliant"] = False
                    result["violations"].append({
                        "rule": "IASC: Precise location data for refugees must be redacted",
                        "action_required": "Redact precise coordinates for vulnerable populations"
                    })
        
        return result
    
    # ========== HEALTHCARE & PHARMA CHECKERS ==========
    
    def _check_eu_mdr(self, framework: Dict, payload: Dict) -> Dict:
        """EU Medical Device Regulation"""
        result = {"framework_id": "EU_MDR", "compliant": True, "violations": [], "warnings": []}
        
        provides_diagnosis = payload.get("provides_diagnosis", False)
        clinical_evaluation_logged = payload.get("clinical_evaluation_logged", False)
        pms_enabled = payload.get("post_market_surveillance_enabled", False)
        
        if provides_diagnosis:
            if not clinical_evaluation_logged:
                result["compliant"] = False
                result["violations"].append({
                    "rule": "EU MDR: Clinical evaluation required for diagnostic devices (Class IIa/b)",
                    "action_required": "Log clinical evaluation data"
                })
            
            if not pms_enabled:
                result["warnings"].append({
                    "rule": "EU MDR: Post-Market Surveillance recommended",
                    "recommendation": "Enable PMS event tracking"
                })
        
        return result
    
    def verify_mdr_compliance(self, diagnosis_output: Dict) -> Dict:
        """
        Verify MDR compliance for diagnostic output
        
        Args:
            diagnosis_output: Diagnostic output from FRENASA Engine
        
        Returns:
            MDR compliance verification result
        """
        return self._check_eu_mdr(
            {"id": "EU_MDR"},
            {
                "provides_diagnosis": True,
                "clinical_evaluation_logged": diagnosis_output.get("clinical_evaluation_logged", False),
                "post_market_surveillance_enabled": diagnosis_output.get("pms_enabled", False)
            }
        )
    
    def _check_fda_21_cfr_11(self, framework: Dict, payload: Dict) -> Dict:
        """FDA 21 CFR Part 11 (Electronic Records & Signatures)"""
        result = {"framework_id": "FDA_21_CFR_11", "compliant": True, "violations": [], "warnings": []}
        
        has_timestamp = payload.get("timestamped", False)
        has_digital_signature = payload.get("digital_signature", False)
        has_audit_trail = payload.get("audit_trail", False)
        
        if not has_timestamp:
            result["compliant"] = False
            result["violations"].append({
                "rule": "FDA 21 CFR 11: Electronic records must be timestamped",
                "action_required": "Add timestamp to Golden Thread entry"
            })
        
        if not has_digital_signature:
            result["warnings"].append({
                "rule": "FDA 21 CFR 11: Digital signature recommended",
                "recommendation": "Add non-repudiable digital signature"
            })
        
        if not has_audit_trail:
            result["compliant"] = False
            result["violations"].append({
                "rule": "FDA 21 CFR 11: Audit trail required",
                "action_required": "Enable audit trail for all record modifications"
            })
        
        return result
    
    def _check_eu_ctr(self, framework: Dict, payload: Dict) -> Dict:
        """EU Clinical Trials Regulation"""
        result = {"framework_id": "EU_CTR", "compliant": True, "violations": [], "warnings": []}
        
        sponsor_data_separated = payload.get("sponsor_data_separated", False)
        subject_data_pseudonymized = payload.get("subject_data_pseudonymized", False)
        
        if not sponsor_data_separated:
            result["compliant"] = False
            result["violations"].append({
                "rule": "EU CTR: Sponsor data must be separated from subject clinical data",
                "action_required": "Enforce strict data separation"
            })
        
        if not subject_data_pseudonymized:
            result["compliant"] = False
            result["violations"].append({
                "rule": "EU CTR: Subject data must be pseudonymized",
                "action_required": "Pseudonymize all subject clinical data"
            })
        
        return result
    
    # ========== CYBERSECURITY CHECKERS ==========
    
    def _check_nis2(self, framework: Dict, payload: Dict) -> Dict:
        """NIS2 Directive"""
        result = {"framework_id": "NIS2", "compliant": True, "violations": [], "warnings": []}
        
        is_significant_incident = payload.get("is_significant_incident", False)
        cert_notified = payload.get("cert_notified", False)
        notification_time_hours = payload.get("notification_time_hours", 0)
        
        if is_significant_incident:
            if not cert_notified:
                result["compliant"] = False
                result["violations"].append({
                    "rule": "NIS2: Significant incidents must be reported to national CERT within 24 hours",
                    "action_required": "Notify national CERT immediately"
                })
            elif notification_time_hours > 24:
                result["compliant"] = False
                result["violations"].append({
                    "rule": "NIS2: Early warning notification exceeded 24-hour deadline",
                    "notification_time_hours": notification_time_hours,
                    "action_required": "Improve incident detection and notification speed"
                })
        
        return result
    
    def _check_cra(self, framework: Dict, payload: Dict) -> Dict:
        """Cyber Resilience Act"""
        result = {"framework_id": "CRA", "compliant": True, "violations": [], "warnings": []}
        
        sbom_generated = payload.get("sbom_generated", False)
        vulnerability_monitoring = payload.get("vulnerability_monitoring_enabled", False)
        support_period_years = payload.get("support_period_years", 0)
        
        if not sbom_generated:
            result["compliant"] = False
            result["violations"].append({
                "rule": "CRA: Software Bill of Materials (SBOM) required",
                "action_required": "Generate SBOM in SPDX or CycloneDX format"
            })
        
        if not vulnerability_monitoring:
            result["warnings"].append({
                "rule": "CRA: Vulnerability monitoring recommended",
                "recommendation": "Enable automated vulnerability monitoring for device lifecycle"
            })
        
        if support_period_years < 5:
            result["compliant"] = False
            result["violations"].append({
                "rule": "CRA: Minimum 5-year support period required",
                "current_support_years": support_period_years,
                "action_required": "Extend support period to 5 years minimum"
            })
        
        return result


# Example usage
if __name__ == "__main__":
    sectoral = SectoralCompliance()
    
    # Test supply chain compliance
    supply_chain_result = sectoral.check_sectoral_compliance(
        context=SectoralContext.SUPPLY_CHAIN,
        payload={
            "supplier_risk_score": 0.8,
            "audit_proof_logged": False,
            "component_origin": "China"
        }
    )
    
    print(f"Supply Chain Compliance: {json.dumps(supply_chain_result, indent=2)}")
    
    # Test OFAC sanctions
    sanctions_result = sectoral.check_ofac("USER_123", "John Doe")
    print(f"Sanctions Check: {json.dumps(sanctions_result, indent=2)}")
    
    # Test CBAM emissions
    emissions = sectoral.calculate_cbam_emissions({
        "hops": [
            {"transport_mode": "sea_freight", "distance_km": 5000, "weight_tonnes": 10, "cold_chain": True},
            {"transport_mode": "road_freight", "distance_km": 200, "weight_tonnes": 10, "cold_chain": True}
        ]
    })
    print(f"CBAM Emissions: {emissions} tCO2e")
