"""
Regional Compliance Localization
Implements 2026 Data Security Index regional findings

Regional Tension Modes:
- US: Prioritize DSPM and tool ROI metrics
- EMEA: Increase strictness of GenAI risk controls
- LATAM: Focus on mature DSPM strategy implementation

Compliance:
- Regional data protection laws (GDPR, CCPA, LGPD, etc.)
- Regional AI governance frameworks
- Regional security standards
"""

import json
from datetime import datetime
from typing import Dict, List, Optional
from enum import Enum
from pathlib import Path
import logging

logger = logging.getLogger(__name__)


class Region(Enum):
    """Geographic regions with distinct compliance requirements"""
    US = "US"  # United States
    EMEA = "EMEA"  # Europe, Middle East, Africa
    LATAM = "LATAM"  # Latin America
    APAC = "APAC"  # Asia-Pacific
    GLOBAL = "GLOBAL"  # Global default


class TensionMode(Enum):
    """Regional security tension modes based on 2026 DSI"""
    STRICT = "STRICT"  # Maximum enforcement
    BALANCED = "BALANCED"  # Standard enforcement
    PERMISSIVE = "PERMISSIVE"  # Minimum enforcement


class RegionalComplianceMatrix:
    """
    Regional compliance matrix with localized enforcement rules
    
    Based on 2026 Data Security Index regional trends:
    - US: DSPM maturity + ROI focus
    - EMEA: GenAI risk controls + GDPR strictness
    - LATAM: DSPM strategy implementation
    """
    
    def __init__(self, primary_region: Region = Region.EMEA):
        self.primary_region = primary_region
        self.regional_configs = self._load_regional_configs()
        
        logger.info(f"🌍 Regional Compliance Matrix initialized - Region: {primary_region.value}")
    
    def _load_regional_configs(self) -> Dict:
        """Load regional compliance configurations"""
        
        return {
            Region.US: {
                "tension_mode": TensionMode.BALANCED,
                "frameworks": ["HIPAA", "HITECH", "CCPA", "NIST_CSF", "SOC_2"],
                "priorities": {
                    "dspm_maturity": 0.9,  # High priority
                    "tool_roi": 0.85,  # High priority
                    "genai_controls": 0.6,  # Medium priority
                    "data_sovereignty": 0.5  # Lower priority (cloud-first)
                },
                "dspm_focus": {
                    "automated_classification": True,
                    "exposure_risk_detection": True,
                    "access_pattern_monitoring": True,
                    "roi_metrics": True  # US-specific
                },
                "genai_controls": {
                    "leak_filter": True,
                    "anomaly_detection": True,
                    "external_llm_blocking": False,  # More permissive
                    "prompt_injection_detection": True
                },
                "audit_requirements": {
                    "retention_days": 2555,  # 7 years (HIPAA)
                    "tamper_proof": True,
                    "real_time_monitoring": True
                },
                "notes": "Focus on DSPM maturity and demonstrating ROI. Cloud-first approach."
            },
            
            Region.EMEA: {
                "tension_mode": TensionMode.STRICT,
                "frameworks": ["GDPR", "EU_AI_ACT", "KDPA", "POPIA", "ISO_27001"],
                "priorities": {
                    "dspm_maturity": 0.8,
                    "tool_roi": 0.6,
                    "genai_controls": 0.95,  # Highest priority
                    "data_sovereignty": 0.98  # Critical priority
                },
                "dspm_focus": {
                    "automated_classification": True,
                    "exposure_risk_detection": True,
                    "access_pattern_monitoring": True,
                    "gdpr_compliance": True  # EMEA-specific
                },
                "genai_controls": {
                    "leak_filter": True,
                    "anomaly_detection": True,
                    "external_llm_blocking": True,  # Strict blocking
                    "prompt_injection_detection": True,
                    "eu_ai_act_compliance": True  # EMEA-specific
                },
                "audit_requirements": {
                    "retention_days": 1825,  # 5 years (GDPR)
                    "tamper_proof": True,
                    "real_time_monitoring": True,
                    "gdpr_article_30": True  # Records of processing
                },
                "notes": "Strictest GenAI controls. Data sovereignty is non-negotiable."
            },
            
            Region.LATAM: {
                "tension_mode": TensionMode.BALANCED,
                "frameworks": ["LGPD", "ISO_27001"],
                "priorities": {
                    "dspm_maturity": 0.95,  # Highest priority (strategy implementation)
                    "tool_roi": 0.7,
                    "genai_controls": 0.65,
                    "data_sovereignty": 0.75
                },
                "dspm_focus": {
                    "automated_classification": True,
                    "exposure_risk_detection": True,
                    "access_pattern_monitoring": True,
                    "strategy_implementation": True,  # LATAM-specific
                    "maturity_assessment": True  # LATAM-specific
                },
                "genai_controls": {
                    "leak_filter": True,
                    "anomaly_detection": True,
                    "external_llm_blocking": False,
                    "prompt_injection_detection": True
                },
                "audit_requirements": {
                    "retention_days": 1825,  # 5 years (LGPD)
                    "tamper_proof": True,
                    "real_time_monitoring": False  # More flexible
                },
                "notes": "Focus on mature DSPM strategy implementation. Building security programs."
            },
            
            Region.APAC: {
                "tension_mode": TensionMode.BALANCED,
                "frameworks": ["ISO_27001", "SOC_2"],
                "priorities": {
                    "dspm_maturity": 0.75,
                    "tool_roi": 0.8,
                    "genai_controls": 0.7,
                    "data_sovereignty": 0.85  # High priority (varied regulations)
                },
                "dspm_focus": {
                    "automated_classification": True,
                    "exposure_risk_detection": True,
                    "access_pattern_monitoring": True
                },
                "genai_controls": {
                    "leak_filter": True,
                    "anomaly_detection": True,
                    "external_llm_blocking": False,
                    "prompt_injection_detection": True
                },
                "audit_requirements": {
                    "retention_days": 1825,
                    "tamper_proof": True,
                    "real_time_monitoring": True
                },
                "notes": "Varied regulations across countries. Focus on flexibility."
            },
            
            Region.GLOBAL: {
                "tension_mode": TensionMode.STRICT,
                "frameworks": ["ISO_27001", "SOC_2", "NIST_CSF"],
                "priorities": {
                    "dspm_maturity": 0.8,
                    "tool_roi": 0.7,
                    "genai_controls": 0.8,
                    "data_sovereignty": 0.9
                },
                "dspm_focus": {
                    "automated_classification": True,
                    "exposure_risk_detection": True,
                    "access_pattern_monitoring": True
                },
                "genai_controls": {
                    "leak_filter": True,
                    "anomaly_detection": True,
                    "external_llm_blocking": True,
                    "prompt_injection_detection": True
                },
                "audit_requirements": {
                    "retention_days": 2555,  # Maximum retention
                    "tamper_proof": True,
                    "real_time_monitoring": True
                },
                "notes": "Strictest global baseline. Complies with all major frameworks."
            }
        }
    
    def get_regional_config(self, region: Optional[Region] = None) -> Dict:
        """Get configuration for a specific region"""
        
        region = region or self.primary_region
        return self.regional_configs.get(region, self.regional_configs[Region.GLOBAL])
    
    def apply_regional_enforcement(
        self,
        action: str,
        payload: Dict,
        region: Optional[Region] = None
    ) -> Dict:
        """
        Apply regional enforcement rules to an action
        
        Args:
            action: Action type (e.g., "genai_prompt", "data_transfer")
            payload: Action payload
            region: Target region
        
        Returns:
            Enforcement result
        """
        
        region = region or self.primary_region
        config = self.get_regional_config(region)
        
        result = {
            "region": region.value,
            "action": action,
            "tension_mode": config["tension_mode"].value,
            "approved": True,
            "enforcement_rules_applied": [],
            "warnings": []
        }
        
        # Apply region-specific enforcement
        if action == "genai_prompt":
            result = self._enforce_genai_rules(payload, config, result)
        
        elif action == "data_transfer":
            result = self._enforce_data_transfer_rules(payload, config, result)
        
        elif action == "dspm_scan":
            result = self._enforce_dspm_rules(payload, config, result)
        
        return result
    
    def _enforce_genai_rules(self, payload: Dict, config: Dict, result: Dict) -> Dict:
        """Enforce GenAI-specific rules"""
        
        genai_controls = config["genai_controls"]
        
        # EMEA: Strict external LLM blocking
        if config["tension_mode"] == TensionMode.STRICT:
            if genai_controls.get("external_llm_blocking") and payload.get("provider") != "internal":
                result["approved"] = False
                result["enforcement_rules_applied"].append("EMEA: External LLM blocked (GDPR Art. 9)")
        
        # US: More permissive but track ROI
        elif config["tension_mode"] == TensionMode.BALANCED and result["region"] == "US":
            if payload.get("provider") != "internal":
                result["warnings"].append("US: External LLM usage tracked for ROI analysis")
                result["enforcement_rules_applied"].append("US: ROI tracking enabled")
        
        return result
    
    def _enforce_data_transfer_rules(self, payload: Dict, config: Dict, result: Dict) -> Dict:
        """Enforce data transfer rules"""
        
        sovereignty_priority = config["priorities"]["data_sovereignty"]
        
        # High sovereignty priority (EMEA, APAC)
        if sovereignty_priority > 0.9:
            if payload.get("destination_region") != result["region"]:
                result["approved"] = False
                result["enforcement_rules_applied"].append(
                    f"{result['region']}: Cross-border transfer blocked (sovereignty priority: {sovereignty_priority})"
                )
        
        # Medium sovereignty priority (US, LATAM)
        elif sovereignty_priority > 0.5:
            if payload.get("destination_region") != result["region"]:
                result["warnings"].append(
                    f"{result['region']}: Cross-border transfer requires authorization"
                )
                result["enforcement_rules_applied"].append(
                    f"{result['region']}: Authorization check required"
                )
        
        return result
    
    def _enforce_dspm_rules(self, payload: Dict, config: Dict, result: Dict) -> Dict:
        """Enforce DSPM-specific rules"""
        
        dspm_focus = config["dspm_focus"]
        
        # LATAM: Focus on strategy implementation
        if result["region"] == "LATAM":
            if not dspm_focus.get("strategy_implementation"):
                result["warnings"].append("LATAM: DSPM strategy implementation required")
            result["enforcement_rules_applied"].append("LATAM: Maturity assessment enabled")
        
        # US: Focus on ROI metrics
        elif result["region"] == "US":
            if dspm_focus.get("roi_metrics"):
                result["enforcement_rules_applied"].append("US: ROI metrics collection enabled")
        
        # EMEA: Focus on GDPR compliance
        elif result["region"] == "EMEA":
            if dspm_focus.get("gdpr_compliance"):
                result["enforcement_rules_applied"].append("EMEA: GDPR Art. 30 compliance check")
        
        return result
    
    def generate_regional_compliance_report(self) -> Dict:
        """
        Generate compliance report for all regions
        
        Returns:
            Regional compliance status
        """
        
        report = {
            "report_date": datetime.utcnow().isoformat(),
            "primary_region": self.primary_region.value,
            "regional_status": {}
        }
        
        for region in Region:
            config = self.get_regional_config(region)
            
            report["regional_status"][region.value] = {
                "tension_mode": config["tension_mode"].value,
                "frameworks": config["frameworks"],
                "priorities": config["priorities"],
                "notes": config["notes"]
            }
        
        return report
    
    def recommend_regional_adjustments(self, current_region: Region, target_region: Region) -> List[Dict]:
        """
        Recommend adjustments when moving between regions
        
        Returns:
            List of recommended adjustments
        """
        
        current_config = self.get_regional_config(current_region)
        target_config = self.get_regional_config(target_region)
        
        adjustments = []
        
        # Compare priorities
        for priority, current_value in current_config["priorities"].items():
            target_value = target_config["priorities"][priority]
            
            if abs(target_value - current_value) > 0.2:
                adjustments.append({
                    "priority": priority,
                    "current_value": current_value,
                    "target_value": target_value,
                    "adjustment": "INCREASE" if target_value > current_value else "DECREASE",
                    "impact": "HIGH" if abs(target_value - current_value) > 0.4 else "MEDIUM"
                })
        
        # Compare tension modes
        if current_config["tension_mode"] != target_config["tension_mode"]:
            adjustments.append({
                "priority": "tension_mode",
                "current_value": current_config["tension_mode"].value,
                "target_value": target_config["tension_mode"].value,
                "adjustment": "CHANGE_MODE",
                "impact": "CRITICAL"
            })
        
        return adjustments


# Example usage
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    
    # Initialize regional compliance matrix
    matrix = RegionalComplianceMatrix(primary_region=Region.EMEA)
    
    # Test 1: EMEA GenAI enforcement (strict)
    result = matrix.apply_regional_enforcement(
        action="genai_prompt",
        payload={"provider": "openai", "prompt": "Analyze patient data"},
        region=Region.EMEA
    )
    print(f"\n🌍 EMEA GenAI Enforcement:")
    print(f"   Approved: {result['approved']}")
    print(f"   Rules: {result['enforcement_rules_applied']}")
    
    # Test 2: US GenAI enforcement (balanced)
    result = matrix.apply_regional_enforcement(
        action="genai_prompt",
        payload={"provider": "openai", "prompt": "Analyze patient data"},
        region=Region.US
    )
    print(f"\n🌍 US GenAI Enforcement:")
    print(f"   Approved: {result['approved']}")
    print(f"   Warnings: {result['warnings']}")
    
    # Test 3: LATAM DSPM enforcement
    result = matrix.apply_regional_enforcement(
        action="dspm_scan",
        payload={"scan_type": "full"},
        region=Region.LATAM
    )
    print(f"\n🌍 LATAM DSPM Enforcement:")
    print(f"   Rules: {result['enforcement_rules_applied']}")
    
    # Test 4: Regional compliance report
    report = matrix.generate_regional_compliance_report()
    print(f"\n📊 Regional Compliance Report:")
    for region, status in report["regional_status"].items():
        print(f"   {region}: {status['tension_mode']} - {len(status['frameworks'])} frameworks")
    
    # Test 5: Regional adjustments
    adjustments = matrix.recommend_regional_adjustments(Region.US, Region.EMEA)
    print(f"\n🔄 US → EMEA Adjustments:")
    for adj in adjustments:
        print(f"   {adj['priority']}: {adj['adjustment']} (Impact: {adj['impact']})")
