"""
Step 36: GCP Cloud Operations Integration
Sovereignty Health Monitoring & 24/7 Alerting

Compliance:
- ISO 27001 A.12.4 (Logging and Monitoring)
- SOC 2 (Security Monitoring)
- NIST CSF (Detect Function)
"""

import logging
from typing import Dict, List, Optional
from datetime import datetime, timedelta
from enum import Enum
from google.cloud import monitoring_v3
from google.cloud import logging as cloud_logging
from google.cloud.monitoring_dashboard import v1 as dashboard_v1
import json

logger = logging.getLogger(__name__)


class SovereigntyHealthStatus(Enum):
    """Sovereignty health status levels"""
    OPTIMAL = "optimal"  # No violations, all systems operational
    DEGRADED = "degraded"  # Minor issues, non-critical violations
    CRITICAL = "critical"  # Active sovereignty violations
    EMERGENCY = "emergency"  # Multiple critical violations


class CloudOperationsMonitor:
    """
    Integrates GCP Cloud Monitoring and Logging for 24/7 Sovereignty Health tracking.
    
    Monitors:
    - SovereigntyViolationError events
    - Cross-border data transfer attempts
    - High-risk AI inference compliance
    - Crypto Shredder key lifecycle
    - Audit trail integrity
    """
    
    def __init__(
        self,
        project_id: str,
        notification_channels: Optional[List[str]] = None
    ):
        self.project_id = project_id
        self.notification_channels = notification_channels or []
        
        # Initialize GCP clients
        self.metrics_client = monitoring_v3.MetricServiceClient()
        self.alert_client = monitoring_v3.AlertPolicyServiceClient()
        self.dashboard_client = dashboard_v1.DashboardsServiceClient()
        self.logging_client = cloud_logging.Client(project=project_id)
        
        # Project path
        self.project_name = f"projects/{project_id}"
        
        logger.info(f"🔍 Cloud Operations Monitor initialized - Project: {project_id}")
    
    def create_sovereignty_health_dashboard(self) -> str:
        """
        Create comprehensive Sovereignty Health dashboard.
        
        Returns:
            Dashboard ID
        """
        dashboard = {
            "display_name": "iLuminara Sovereignty Health",
            "mosaic_layout": {
                "columns": 12,
                "tiles": [
                    # Sovereignty Violations
                    {
                        "width": 6,
                        "height": 4,
                        "widget": {
                            "title": "Sovereignty Violations (24h)",
                            "xy_chart": {
                                "data_sets": [{
                                    "time_series_query": {
                                        "time_series_filter": {
                                            "filter": 'metric.type="custom.googleapis.com/sovereignty/violations"',
                                            "aggregation": {
                                                "alignment_period": "3600s",
                                                "per_series_aligner": "ALIGN_RATE"
                                            }
                                        }
                                    },
                                    "plot_type": "LINE"
                                }],
                                "y_axis": {"label": "Violations/hour", "scale": "LINEAR"}
                            }
                        }
                    },
                    
                    # Cross-Border Transfers
                    {
                        "x_pos": 6,
                        "width": 6,
                        "height": 4,
                        "widget": {
                            "title": "Cross-Border Transfer Attempts",
                            "xy_chart": {
                                "data_sets": [{
                                    "time_series_query": {
                                        "time_series_filter": {
                                            "filter": 'metric.type="custom.googleapis.com/sovereignty/cross_border_transfers"',
                                            "aggregation": {
                                                "alignment_period": "3600s",
                                                "per_series_aligner": "ALIGN_SUM"
                                            }
                                        }
                                    },
                                    "plot_type": "STACKED_BAR"
                                }],
                                "y_axis": {"label": "Attempts", "scale": "LINEAR"}
                            }
                        }
                    },
                    
                    # High-Risk AI Inferences
                    {
                        "y_pos": 4,
                        "width": 6,
                        "height": 4,
                        "widget": {
                            "title": "High-Risk AI Inferences (EU AI Act §6)",
                            "xy_chart": {
                                "data_sets": [{
                                    "time_series_query": {
                                        "time_series_filter": {
                                            "filter": 'metric.type="custom.googleapis.com/ai/high_risk_inferences"',
                                            "aggregation": {
                                                "alignment_period": "3600s",
                                                "per_series_aligner": "ALIGN_RATE"
                                            }
                                        }
                                    },
                                    "plot_type": "LINE"
                                }]
                            }
                        }
                    },
                    
                    # Crypto Shredder Activity
                    {
                        "x_pos": 6,
                        "y_pos": 4,
                        "width": 6,
                        "height": 4,
                        "widget": {
                            "title": "Crypto Shredder (IP-02) - Keys Shredded",
                            "xy_chart": {
                                "data_sets": [{
                                    "time_series_query": {
                                        "time_series_filter": {
                                            "filter": 'metric.type="custom.googleapis.com/crypto_shredder/keys_shredded"',
                                            "aggregation": {
                                                "alignment_period": "86400s",
                                                "per_series_aligner": "ALIGN_SUM"
                                            }
                                        }
                                    },
                                    "plot_type": "STACKED_AREA"
                                }]
                            }
                        }
                    },
                    
                    # Audit Trail Integrity
                    {
                        "y_pos": 8,
                        "width": 12,
                        "height": 4,
                        "widget": {
                            "title": "Audit Trail Integrity Score",
                            "scorecard": {
                                "time_series_query": {
                                    "time_series_filter": {
                                        "filter": 'metric.type="custom.googleapis.com/audit/integrity_score"',
                                        "aggregation": {
                                            "alignment_period": "3600s",
                                            "per_series_aligner": "ALIGN_MEAN"
                                        }
                                    }
                                },
                                "gauge_view": {
                                    "lower_bound": 0.0,
                                    "upper_bound": 1.0
                                }
                            }
                        }
                    },
                    
                    # Sovereignty Health Status
                    {
                        "y_pos": 12,
                        "width": 12,
                        "height": 2,
                        "widget": {
                            "title": "Overall Sovereignty Health Status",
                            "text": {
                                "content": "Real-time sovereignty compliance across 14 global legal frameworks",
                                "format": "MARKDOWN"
                            }
                        }
                    }
                ]
            }
        }
        
        request = dashboard_v1.CreateDashboardRequest(
            parent=self.project_name,
            dashboard=dashboard
        )
        
        response = self.dashboard_client.create_dashboard(request=request)
        logger.info(f"✅ Sovereignty Health Dashboard created: {response.name}")
        
        return response.name
    
    def create_sovereignty_violation_alert(self) -> str:
        """
        Create high-priority alert for SovereigntyViolationError events.
        
        Returns:
            Alert policy ID
        """
        alert_policy = {
            "display_name": "🚨 CRITICAL: Sovereignty Violation Detected",
            "documentation": {
                "content": """
# Sovereignty Violation Alert

A SovereigntyViolationError has been triggered by the Governance Kernel.

## Immediate Actions:
1. Review the violation details in Cloud Logging
2. Identify the source system/user
3. Verify the legal framework violated (GDPR, KDPA, HIPAA, etc.)
4. Escalate to Data Protection Officer if cross-border transfer attempted
5. Document incident in compliance audit trail

## Legal Frameworks:
- GDPR Art. 9 (Special Categories)
- Kenya DPA §37 (Transfer Restrictions)
- HIPAA §164.312 (Safeguards)
- POPIA §14 (Cross-border Transfers)

## Contact:
- DPO: dpo@iluminara.health
- Compliance: compliance@iluminara.health
                """,
                "mime_type": "text/markdown"
            },
            "conditions": [{
                "display_name": "Sovereignty Violation Rate > 0",
                "condition_threshold": {
                    "filter": 'metric.type="custom.googleapis.com/sovereignty/violations"',
                    "comparison": "COMPARISON_GT",
                    "threshold_value": 0,
                    "duration": {"seconds": 60},
                    "aggregations": [{
                        "alignment_period": {"seconds": 60},
                        "per_series_aligner": "ALIGN_RATE"
                    }]
                }
            }],
            "notification_channels": self.notification_channels,
            "alert_strategy": {
                "auto_close": {"seconds": 3600}  # Auto-close after 1 hour
            },
            "severity": "CRITICAL"
        }
        
        request = monitoring_v3.CreateAlertPolicyRequest(
            name=self.project_name,
            alert_policy=alert_policy
        )
        
        response = self.alert_client.create_alert_policy(request=request)
        logger.info(f"✅ Sovereignty Violation Alert created: {response.name}")
        
        return response.name
    
    def create_cross_border_transfer_alert(self) -> str:
        """
        Create alert for unauthorized cross-border data transfer attempts.
        
        Returns:
            Alert policy ID
        """
        alert_policy = {
            "display_name": "⚠️ HIGH: Unauthorized Cross-Border Transfer Attempt",
            "documentation": {
                "content": """
# Cross-Border Transfer Alert

An attempt to transfer PHI/PII across sovereign borders has been detected and blocked.

## Compliance Frameworks:
- GDPR Art. 44-50 (Transfers to Third Countries)
- Kenya DPA §48 (Transfer of Personal Data)
- POPIA §72 (Transfer of Personal Information)

## Investigation Required:
1. Identify source and destination zones
2. Verify if Standard Contractual Clauses (SCC) exist
3. Check adequacy decision status
4. Review consent tokens
5. Escalate if intentional bypass attempt
                """,
                "mime_type": "text/markdown"
            },
            "conditions": [{
                "display_name": "Cross-Border Transfer Attempts > 5/hour",
                "condition_threshold": {
                    "filter": 'metric.type="custom.googleapis.com/sovereignty/cross_border_transfers"',
                    "comparison": "COMPARISON_GT",
                    "threshold_value": 5,
                    "duration": {"seconds": 3600},
                    "aggregations": [{
                        "alignment_period": {"seconds": 3600},
                        "per_series_aligner": "ALIGN_SUM"
                    }]
                }
            }],
            "notification_channels": self.notification_channels,
            "severity": "WARNING"
        }
        
        request = monitoring_v3.CreateAlertPolicyRequest(
            name=self.project_name,
            alert_policy=alert_policy
        )
        
        response = self.alert_client.create_alert_policy(request=request)
        logger.info(f"✅ Cross-Border Transfer Alert created: {response.name}")
        
        return response.name
    
    def log_sovereignty_event(
        self,
        event_type: str,
        severity: str,
        details: Dict,
        jurisdiction: str
    ):
        """
        Log sovereignty event to Cloud Logging.
        
        Args:
            event_type: Type of event (violation, transfer, inference, etc.)
            severity: Log severity (DEBUG, INFO, WARNING, ERROR, CRITICAL)
            details: Event details
            jurisdiction: Legal jurisdiction (GDPR_EU, KDPA_KE, etc.)
        """
        logger_name = "sovereignty-events"
        cloud_logger = self.logging_client.logger(logger_name)
        
        log_entry = {
            "timestamp": datetime.utcnow().isoformat(),
            "event_type": event_type,
            "jurisdiction": jurisdiction,
            "details": details,
            "fortress_component": "governance_kernel"
        }
        
        cloud_logger.log_struct(
            log_entry,
            severity=severity,
            labels={
                "component": "sovereignty_monitor",
                "jurisdiction": jurisdiction
            }
        )
    
    def write_custom_metric(
        self,
        metric_type: str,
        value: float,
        labels: Optional[Dict[str, str]] = None
    ):
        """
        Write custom metric to Cloud Monitoring.
        
        Args:
            metric_type: Metric type (e.g., "sovereignty/violations")
            value: Metric value
            labels: Optional metric labels
        """
        series = monitoring_v3.TimeSeries()
        series.metric.type = f"custom.googleapis.com/{metric_type}"
        
        if labels:
            for key, val in labels.items():
                series.metric.labels[key] = val
        
        series.resource.type = "global"
        
        now = datetime.utcnow()
        interval = monitoring_v3.TimeInterval(
            {"end_time": {"seconds": int(now.timestamp())}}
        )
        point = monitoring_v3.Point(
            {"interval": interval, "value": {"double_value": value}}
        )
        series.points = [point]
        
        self.metrics_client.create_time_series(
            name=self.project_name,
            time_series=[series]
        )
    
    def get_sovereignty_health_status(self) -> Dict:
        """
        Calculate overall sovereignty health status.
        
        Returns:
            Health status report
        """
        # Query recent violations
        now = datetime.utcnow()
        start_time = now - timedelta(hours=24)
        
        # This is a simplified version - in production, query actual metrics
        violations_24h = 0  # Query from Cloud Monitoring
        cross_border_attempts = 0
        audit_integrity = 1.0
        
        # Determine status
        if violations_24h == 0 and cross_border_attempts == 0:
            status = SovereigntyHealthStatus.OPTIMAL
        elif violations_24h < 5:
            status = SovereigntyHealthStatus.DEGRADED
        elif violations_24h < 20:
            status = SovereigntyHealthStatus.CRITICAL
        else:
            status = SovereigntyHealthStatus.EMERGENCY
        
        return {
            "status": status.value,
            "timestamp": now.isoformat(),
            "metrics": {
                "violations_24h": violations_24h,
                "cross_border_attempts_24h": cross_border_attempts,
                "audit_integrity_score": audit_integrity
            },
            "compliance_frameworks": [
                "GDPR", "KDPA", "HIPAA", "POPIA", "PIPEDA",
                "CCPA", "EU_AI_ACT", "ISO_27001", "SOC_2",
                "NIST_CSF", "HITECH", "LGPD", "NDPR", "APPI"
            ]
        }


# Example usage
if __name__ == "__main__":
    monitor = CloudOperationsMonitor(
        project_id="iluminara-core",
        notification_channels=["projects/iluminara-core/notificationChannels/123"]
    )
    
    # Create dashboard
    dashboard_id = monitor.create_sovereignty_health_dashboard()
    print(f"✅ Dashboard: {dashboard_id}")
    
    # Create alerts
    violation_alert = monitor.create_sovereignty_violation_alert()
    transfer_alert = monitor.create_cross_border_transfer_alert()
    
    # Log event
    monitor.log_sovereignty_event(
        event_type="sovereignty_violation",
        severity="ERROR",
        details={
            "action": "Data_Transfer",
            "source": "kenya",
            "destination": "aws_us",
            "blocked": True
        },
        jurisdiction="KDPA_KE"
    )
    
    # Write metric
    monitor.write_custom_metric(
        metric_type="sovereignty/violations",
        value=1.0,
        labels={"jurisdiction": "KDPA_KE", "severity": "high"}
    )
    
    # Get health status
    health = monitor.get_sovereignty_health_status()
    print(f"🛡️ Sovereignty Health: {health['status']}")
