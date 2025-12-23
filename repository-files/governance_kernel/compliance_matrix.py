"""
Regional Compliance Localization
Aligns with 2026 Data Security Index regional trends

Regional Tension Modes:
- US: Prioritize DSPM and tool ROI metrics
- EMEA: Increase strictness of GenAI risk controls
- LATAM: Focus on mature DSPM strategy implementation

Compliance:
- GDPR (EMEA)
- HIPAA (US)
- LGPD (LATAM - Brazil)
- KDPA (Africa - Kenya)
- POPIA (Africa - South Africa)
"""

from enum import Enum
from typing import Dict, List, Optional
from dataclasses import dataclass
import logging

logger = logging.getLogger(__name__)


class Region(Enum):
    """Geographic regions with distinct compliance requirements"""
    US = "United States"
    EMEA = "Europe, Middle East, Africa"
    LATAM = "Latin America"
    APAC = "Asia Pacific"
    AFRICA = "Africa"


class TensionMode(Enum):
    """Regional security tension modes from 2026 DSI"""
    STRICT = "strict"  # EMEA - High GenAI controls
    BALANCED = "balanced"  # US - DSPM + ROI focus
    MATURING = "maturing"  # LATAM - DSPM implementation
    EMERGING = "emerging"  # APAC, Africa - Building foundations


@dataclass
class ComplianceFramework:
    """Compliance framework definition"""
    name: str
    region: Region
    articles: List[str]
    enforcement_level: str  # strict, moderate, permissive
    data_residency_required: bool
    cross_border_restrictions: bool
    genai_controls_required: bool
    dspm_priority: int  # 1-10
    audit_retention_days: int


class ComplianceMatrix:
    """
    Regional compliance localization engine
    
    Adapts iLuminara security posture based on regional requirements
    and 2026 Data Security Index trends.
    """
    
    def __init__(self, primary_region: Region = Region.AFRICA):
        self.primary_region = primary_region
        self.frameworks = self._initialize_frameworks()
        self.tension_mode = self._determine_tension_mode(primary_region)
        
        logger.info(f"🌍 Compliance Matrix initialized - Region: {primary_region.value}")
        logger.info(f"   Tension Mode: {self.tension_mode.value}")
    
    def _initialize_frameworks(self) -> Dict[str, ComplianceFramework]:
        """Initialize regional compliance frameworks"""
        return {
            "GDPR": ComplianceFramework(
                name="General Data Protection Regulation",
                region=Region.EMEA,
                articles=[
                    "Art. 6 (Lawfulness of Processing)",
                    "Art. 9 (Special Categories)",
                    "Art. 17 (Right to Erasure)",
                    "Art. 22 (Right to Explanation)",
                    "Art. 30 (Records of Processing)",
                    "Art. 32 (Security of Processing)",
                    "Art. 45 (Adequacy Decisions)",
                    "Art. 46 (Standard Contractual Clauses)"
                ],
                enforcement_level="strict",
                data_residency_required=True,
                cross_border_restrictions=True,
                genai_controls_required=True,  # 2026 DSI: EMEA strictness
                dspm_priority=9,
                audit_retention_days=2555  # 7 years
            ),
            "HIPAA": ComplianceFramework(
                name="Health Insurance Portability and Accountability Act",
                region=Region.US,
                articles=[
                    "§164.308 (Administrative Safeguards)",
                    "§164.310 (Physical Safeguards)",
                    "§164.312 (Technical Safeguards)",
                    "§164.316 (Policies and Procedures)",
                    "§164.530 (Documentation)"
                ],
                enforcement_level="strict",
                data_residency_required=False,
                cross_border_restrictions=False,
                genai_controls_required=False,  # 2026 DSI: US ROI focus
                dspm_priority=10,  # 2026 DSI: US DSPM priority
                audit_retention_days=2555  # 7 years
            ),
            "KDPA": ComplianceFramework(
                name="Kenya Data Protection Act",
                region=Region.AFRICA,
                articles=[
                    "§25 (Principles of Data Protection)",
                    "§37 (Transfer of Personal Data)",
                    "§42 (Rights of Data Subjects)",
                    "§50 (Data Protection Impact Assessment)"
                ],
                enforcement_level="strict",
                data_residency_required=True,
                cross_border_restrictions=True,
                genai_controls_required=True,
                dspm_priority=8,
                audit_retention_days=1825  # 5 years
            ),
            "POPIA": ComplianceFramework(
                name="Protection of Personal Information Act",
                region=Region.AFRICA,
                articles=[
                    "§11 (Lawfulness of Processing)",
                    "§14 (Security Safeguards)",
                    "§57 (Trans-border Information Flows)"
                ],
                enforcement_level="strict",
                data_residency_required=True,
                cross_border_restrictions=True,
                genai_controls_required=True,
                dspm_priority=8,
                audit_retention_days=1825  # 5 years
            ),
            "LGPD": ComplianceFramework(
                name="Lei Geral de Proteção de Dados",
                region=Region.LATAM,
                articles=[
                    "Art. 6 (Processing Principles)",
                    "Art. 33 (International Data Transfer)",
                    "Art. 46 (Security Measures)"
                ],
                enforcement_level="moderate",
                data_residency_required=False,
                cross_border_restrictions=True,
                genai_controls_required=False,
                dspm_priority=7,  # 2026 DSI: LATAM maturing DSPM
                audit_retention_days=1825  # 5 years
            ),
            "PIPEDA": ComplianceFramework(
                name="Personal Information Protection and Electronic Documents Act",
                region=Region.US,  # Canada grouped with US for simplicity
                articles=[
                    "§5 (Consent)",
                    "§6 (Accountability)",
                    "§7 (Safeguards)"
                ],
                enforcement_level="moderate",
                data_residency_required=False,
                cross_border_restrictions=False,
                genai_controls_required=False,
                dspm_priority=8,
                audit_retention_days=2555  # 7 years
            ),
            "CCPA": ComplianceFramework(
                name="California Consumer Privacy Act",
                region=Region.US,
                articles=[
                    "§1798.100 (Right to Know)",
                    "§1798.105 (Right to Delete)",
                    "§1798.110 (Right to Access)",
                    "§1798.120 (Right to Opt-Out)"
                ],
                enforcement_level="moderate",
                data_residency_required=False,
                cross_border_restrictions=False,
                genai_controls_required=False,
                dspm_priority=9,  # 2026 DSI: US DSPM priority
                audit_retention_days=1825  # 5 years
            )
        }
    
    def _determine_tension_mode(self, region: Region) -> TensionMode:
        """Determine security tension mode based on 2026 DSI regional trends"""
        tension_map = {
            Region.EMEA: TensionMode.STRICT,  # High GenAI controls
            Region.US: TensionMode.BALANCED,  # DSPM + ROI focus
            Region.LATAM: TensionMode.MATURING,  # DSPM implementation
            Region.APAC: TensionMode.EMERGING,  # Building foundations
            Region.AFRICA: TensionMode.STRICT  # Sovereignty-first
        }
        
        return tension_map.get(region, TensionMode.BALANCED)
    
    def get_applicable_frameworks(self, region: Region) -> List[ComplianceFramework]:
        """Get all applicable frameworks for a region"""
        return [fw for fw in self.frameworks.values() if fw.region == region]
    
    def get_regional_config(self, region: Region) -> Dict:
        """
        Get regional security configuration based on 2026 DSI trends
        
        Returns:
            Configuration dict with regional adjustments
        """
        tension_mode = self._determine_tension_mode(region)
        frameworks = self.get_applicable_frameworks(region)
        
        config = {
            "region": region.value,
            "tension_mode": tension_mode.value,
            "frameworks": [fw.name for fw in frameworks],
            "enforcement_level": self._get_enforcement_level(tension_mode),
            "genai_controls": self._get_genai_controls(tension_mode),
            "dspm_config": self._get_dspm_config(tension_mode),
            "audit_config": self._get_audit_config(frameworks),
            "data_residency": self._get_data_residency_config(frameworks),
            "roi_metrics": self._get_roi_metrics(tension_mode)
        }
        
        return config
    
    def _get_enforcement_level(self, tension_mode: TensionMode) -> Dict:
        """Get enforcement level configuration"""
        enforcement_map = {
            TensionMode.STRICT: {
                "level": "strict",
                "auto_block": True,
                "require_approval": True,
                "violation_tolerance": 0
            },
            TensionMode.BALANCED: {
                "level": "moderate",
                "auto_block": False,
                "require_approval": True,
                "violation_tolerance": 2
            },
            TensionMode.MATURING: {
                "level": "moderate",
                "auto_block": False,
                "require_approval": False,
                "violation_tolerance": 5
            },
            TensionMode.EMERGING: {
                "level": "permissive",
                "auto_block": False,
                "require_approval": False,
                "violation_tolerance": 10
            }
        }
        
        return enforcement_map[tension_mode]
    
    def _get_genai_controls(self, tension_mode: TensionMode) -> Dict:
        """Get GenAI control configuration based on 2026 DSI trends"""
        
        if tension_mode == TensionMode.STRICT:
            # EMEA: Increase strictness of GenAI risk controls
            return {
                "enabled": True,
                "leak_filter": {
                    "enabled": True,
                    "sensitivity": "high",
                    "block_threshold": 0.3  # Block if 30% confidence of PHI
                },
                "endpoint_whitelist": {
                    "enabled": True,
                    "allowed_endpoints": ["vertex-ai.googleapis.com", "localhost"]
                },
                "response_filtering": {
                    "enabled": True,
                    "sanitize_responses": True
                },
                "usage_monitoring": {
                    "enabled": True,
                    "alert_threshold": 5  # Alert after 5 blocked prompts
                }
            }
        
        elif tension_mode == TensionMode.BALANCED:
            # US: Balanced approach with ROI focus
            return {
                "enabled": True,
                "leak_filter": {
                    "enabled": True,
                    "sensitivity": "medium",
                    "block_threshold": 0.5
                },
                "endpoint_whitelist": {
                    "enabled": False  # More permissive
                },
                "response_filtering": {
                    "enabled": True,
                    "sanitize_responses": False  # Flag only
                },
                "usage_monitoring": {
                    "enabled": True,
                    "alert_threshold": 10
                }
            }
        
        else:
            # LATAM, APAC, Emerging: Basic controls
            return {
                "enabled": True,
                "leak_filter": {
                    "enabled": True,
                    "sensitivity": "low",
                    "block_threshold": 0.7
                },
                "endpoint_whitelist": {
                    "enabled": False
                },
                "response_filtering": {
                    "enabled": False
                },
                "usage_monitoring": {
                    "enabled": True,
                    "alert_threshold": 20
                }
            }
    
    def _get_dspm_config(self, tension_mode: TensionMode) -> Dict:
        """Get DSPM configuration based on 2026 DSI trends"""
        
        if tension_mode == TensionMode.BALANCED:
            # US: Prioritize DSPM and tool ROI metrics
            return {
                "enabled": True,
                "priority": "high",
                "scan_frequency": "daily",
                "classification_coverage_target": 95.0,
                "auto_classification": True,
                "risk_detection": {
                    "enabled": True,
                    "sensitivity": "high"
                },
                "roi_tracking": {
                    "enabled": True,  # 2026 DSI: US ROI focus
                    "metrics": [
                        "time_to_classify",
                        "risk_reduction",
                        "compliance_cost_savings",
                        "incident_prevention"
                    ]
                }
            }
        
        elif tension_mode == TensionMode.MATURING:
            # LATAM: Focus on mature DSPM strategy implementation
            return {
                "enabled": True,
                "priority": "high",
                "scan_frequency": "weekly",
                "classification_coverage_target": 85.0,
                "auto_classification": True,
                "risk_detection": {
                    "enabled": True,
                    "sensitivity": "medium"
                },
                "roi_tracking": {
                    "enabled": False  # Focus on implementation first
                }
            }
        
        elif tension_mode == TensionMode.STRICT:
            # EMEA, Africa: Comprehensive DSPM
            return {
                "enabled": True,
                "priority": "critical",
                "scan_frequency": "daily",
                "classification_coverage_target": 98.0,
                "auto_classification": True,
                "risk_detection": {
                    "enabled": True,
                    "sensitivity": "high"
                },
                "roi_tracking": {
                    "enabled": True
                }
            }
        
        else:
            # Emerging: Basic DSPM
            return {
                "enabled": True,
                "priority": "medium",
                "scan_frequency": "monthly",
                "classification_coverage_target": 70.0,
                "auto_classification": False,
                "risk_detection": {
                    "enabled": True,
                    "sensitivity": "low"
                },
                "roi_tracking": {
                    "enabled": False
                }
            }
    
    def _get_audit_config(self, frameworks: List[ComplianceFramework]) -> Dict:
        """Get audit configuration based on frameworks"""
        max_retention = max([fw.audit_retention_days for fw in frameworks]) if frameworks else 1825
        
        return {
            "enabled": True,
            "tamper_proof": True,
            "retention_days": max_retention,
            "real_time_monitoring": True,
            "compliance_reporting": True
        }
    
    def _get_data_residency_config(self, frameworks: List[ComplianceFramework]) -> Dict:
        """Get data residency configuration"""
        residency_required = any(fw.data_residency_required for fw in frameworks)
        cross_border_restricted = any(fw.cross_border_restrictions for fw in frameworks)
        
        return {
            "residency_required": residency_required,
            "cross_border_restricted": cross_border_restricted,
            "enforcement": "strict" if residency_required else "moderate"
        }
    
    def _get_roi_metrics(self, tension_mode: TensionMode) -> Dict:
        """Get ROI metrics configuration (2026 DSI: US priority)"""
        
        if tension_mode == TensionMode.BALANCED:
            # US: Prioritize tool ROI metrics
            return {
                "enabled": True,
                "metrics": {
                    "security_tool_consolidation": {
                        "enabled": True,
                        "target": "86%",  # 2026 DSI: 86% prefer integrated platforms
                        "measurement": "percentage_of_unified_tools"
                    },
                    "threat_detection_improvement": {
                        "enabled": True,
                        "target": "64%",  # 2026 DSI: 64% improvement
                        "measurement": "detection_rate_increase"
                    },
                    "management_efficiency": {
                        "enabled": True,
                        "target": "63%",  # 2026 DSI: 63% easier management
                        "measurement": "time_savings"
                    },
                    "cost_per_incident": {
                        "enabled": True,
                        "measurement": "total_cost_reduction"
                    }
                }
            }
        else:
            return {
                "enabled": False
            }
    
    def generate_compliance_report(self, region: Region) -> str:
        """Generate compliance report for a region"""
        config = self.get_regional_config(region)
        
        report = []
        report.append("=" * 70)
        report.append(f"iLuminara Regional Compliance Report - {region.value}")
        report.append("=" * 70)
        report.append(f"Tension Mode: {config['tension_mode']}")
        report.append(f"Applicable Frameworks: {', '.join(config['frameworks'])}")
        report.append("")
        
        report.append("ENFORCEMENT LEVEL")
        report.append("-" * 70)
        for key, value in config['enforcement_level'].items():
            report.append(f"  {key}: {value}")
        report.append("")
        
        report.append("GENAI CONTROLS (2026 DSI Aligned)")
        report.append("-" * 70)
        report.append(f"  Enabled: {config['genai_controls']['enabled']}")
        report.append(f"  Leak Filter: {config['genai_controls']['leak_filter']['enabled']}")
        report.append(f"  Sensitivity: {config['genai_controls']['leak_filter']['sensitivity']}")
        report.append("")
        
        report.append("DSPM CONFIGURATION (2026 DSI Aligned)")
        report.append("-" * 70)
        report.append(f"  Priority: {config['dspm_config']['priority']}")
        report.append(f"  Scan Frequency: {config['dspm_config']['scan_frequency']}")
        report.append(f"  Coverage Target: {config['dspm_config']['classification_coverage_target']}%")
        report.append(f"  ROI Tracking: {config['dspm_config']['roi_tracking']['enabled']}")
        report.append("")
        
        report.append("DATA RESIDENCY")
        report.append("-" * 70)
        report.append(f"  Required: {config['data_residency']['residency_required']}")
        report.append(f"  Cross-border Restricted: {config['data_residency']['cross_border_restricted']}")
        report.append("")
        
        if config['roi_metrics']['enabled']:
            report.append("ROI METRICS (2026 DSI: US Priority)")
            report.append("-" * 70)
            for metric, data in config['roi_metrics']['metrics'].items():
                report.append(f"  {metric}:")
                report.append(f"    Target: {data.get('target', 'N/A')}")
                report.append(f"    Measurement: {data['measurement']}")
            report.append("")
        
        report.append("=" * 70)
        
        return "\n".join(report)


# Example usage
if __name__ == "__main__":
    # Test all regions
    for region in [Region.US, Region.EMEA, Region.LATAM, Region.AFRICA]:
        matrix = ComplianceMatrix(primary_region=region)
        print(matrix.generate_compliance_report(region))
        print("\n")
