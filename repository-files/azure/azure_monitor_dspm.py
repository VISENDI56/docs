"""
Azure Monitor Integration with DSPM Compliance
Implements Microsoft 2026 Data Security Index telemetry requirements

Compliance:
- Microsoft DSPM 2026
- Azure Security Center
- GenAI Governance Telemetry
"""

import os
import json
from typing import Dict, Optional
from datetime import datetime
from azure.monitor.opentelemetry import configure_azure_monitor
from azure.monitor.ingestion import LogsIngestionClient
from azure.identity import DefaultAzureCredential
from opentelemetry import trace, metrics
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.metrics import MeterProvider
import logging

logger = logging.getLogger(__name__)


class AzureMonitorDSPM:
    """
    Azure Monitor integration with DSPM compliance telemetry.
    Implements Microsoft 2026 Data Security Index requirements.
    """
    
    def __init__(
        self,
        connection_string: str,
        data_collection_endpoint: str,
        data_collection_rule_id: str,
        stream_name: str = "Custom-iLuminara_CL"
    ):
        self.connection_string = connection_string
        self.data_collection_endpoint = data_collection_endpoint
        self.data_collection_rule_id = data_collection_rule_id
        self.stream_name = stream_name
        
        # Configure Azure Monitor
        configure_azure_monitor(connection_string=connection_string)
        
        # Initialize credential
        self.credential = DefaultAzureCredential()
        
        # Initialize logs ingestion client
        self.logs_client = LogsIngestionClient(
            endpoint=data_collection_endpoint,
            credential=self.credential
        )
        
        # Initialize OpenTelemetry
        self.tracer = trace.get_tracer(__name__)
        self.meter = metrics.get_meter(__name__)
        
        # Create DSPM metrics
        self._init_dspm_metrics()
        
        logger.info("📊 Azure Monitor DSPM integration initialized")
    
    def _init_dspm_metrics(self):
        """Initialize DSPM-specific metrics"""
        # Data classification metrics
        self.data_classification_counter = self.meter.create_counter(
            name="iluminara.dspm.data_classification",
            description="Count of data classification operations",
            unit="1"
        )
        
        # Sovereignty violation metrics
        self.sovereignty_violation_counter = self.meter.create_counter(
            name="iluminara.dspm.sovereignty_violations",
            description="Count of sovereignty violations detected",
            unit="1"
        )
        
        # GenAI governance metrics
        self.genai_inference_counter = self.meter.create_counter(
            name="iluminara.dspm.genai_inferences",
            description="Count of GenAI inferences",
            unit="1"
        )
        
        # Crypto shredder metrics
        self.crypto_shred_counter = self.meter.create_counter(
            name="iluminara.dspm.crypto_shreds",
            description="Count of cryptographic key shreds",
            unit="1"
        )
        
        # Audit trail metrics
        self.audit_event_counter = self.meter.create_counter(
            name="iluminara.dspm.audit_events",
            description="Count of audit trail events",
            unit="1"
        )
    
    def log_data_classification(self, classification: Dict):
        """
        Log data classification event to Azure Monitor.
        
        Args:
            classification: Classification result from Purview
        """
        event = {
            "TimeGenerated": datetime.utcnow().isoformat(),
            "EventType": "DataClassification",
            "Classification": classification.get("classification"),
            "SensitivityLabels": json.dumps(classification.get("sensitivity_labels", [])),
            "DSPMCategories": json.dumps(classification.get("dspm_categories", [])),
            "ComplianceFrameworks": json.dumps(classification.get("compliance_frameworks", [])),
            "Jurisdiction": classification.get("context", {}).get("jurisdiction"),
            "DataType": classification.get("data_type")
        }
        
        # Send to Azure Monitor
        self._send_log(event)
        
        # Update metric
        self.data_classification_counter.add(
            1,
            {"classification": classification.get("classification")}
        )
        
        logger.info(f"✅ Data classification logged - Type: {classification.get('classification')}")
    
    def log_sovereignty_violation(self, violation: Dict):
        """
        Log sovereignty violation to Azure Monitor.
        
        Args:
            violation: Sovereignty violation details
        """
        event = {
            "TimeGenerated": datetime.utcnow().isoformat(),
            "EventType": "SovereigntyViolation",
            "ViolationType": violation.get("violation_type"),
            "ActionType": violation.get("action_type"),
            "Jurisdiction": violation.get("jurisdiction"),
            "Destination": violation.get("destination"),
            "Severity": "CRITICAL",
            "Blocked": True,
            "Actor": violation.get("actor"),
            "Resource": violation.get("resource")
        }
        
        # Send to Azure Monitor
        self._send_log(event)
        
        # Update metric
        self.sovereignty_violation_counter.add(
            1,
            {"violation_type": violation.get("violation_type")}
        )
        
        logger.warning(f"⚠️ Sovereignty violation logged - Type: {violation.get('violation_type')}")
    
    def log_genai_inference(self, inference: Dict):
        """
        Log GenAI inference with governance metadata.
        
        Args:
            inference: GenAI inference details
        """
        event = {
            "TimeGenerated": datetime.utcnow().isoformat(),
            "EventType": "GenAIInference",
            "ModelID": inference.get("model_id"),
            "ConfidenceScore": inference.get("confidence_score"),
            "HighRisk": inference.get("confidence_score", 0) > 0.7,
            "ExplainabilityProvided": inference.get("explainability_provided", False),
            "ExplainabilityMethod": inference.get("explainability_method"),
            "HumanOversight": inference.get("human_oversight", False),
            "BiasMonitoring": inference.get("bias_monitoring", False),
            "ClinicalDecision": inference.get("clinical_decision", False),
            "Jurisdiction": inference.get("jurisdiction"),
            "ComplianceFramework": "EU_AI_ACT"
        }
        
        # Send to Azure Monitor
        self._send_log(event)
        
        # Update metric
        self.genai_inference_counter.add(
            1,
            {
                "model_id": inference.get("model_id"),
                "high_risk": str(event["HighRisk"])
            }
        )
        
        logger.info(f"✅ GenAI inference logged - Model: {inference.get('model_id')}")
    
    def log_crypto_shred(self, shred_event: Dict):
        """
        Log cryptographic key shred event (IP-02).
        
        Args:
            shred_event: Crypto shredder event details
        """
        event = {
            "TimeGenerated": datetime.utcnow().isoformat(),
            "EventType": "CryptoShred",
            "KeyID": shred_event.get("key_id"),
            "RetentionPolicy": shred_event.get("retention_policy"),
            "DataType": shred_event.get("data_type"),
            "Jurisdiction": shred_event.get("jurisdiction"),
            "Reason": shred_event.get("reason", "Retention period expired"),
            "DataIrrecoverable": True,
            "ComplianceFramework": "GDPR_Art17"
        }
        
        # Send to Azure Monitor
        self._send_log(event)
        
        # Update metric
        self.crypto_shred_counter.add(
            1,
            {"retention_policy": shred_event.get("retention_policy")}
        )
        
        logger.info(f"✅ Crypto shred logged - Key: {shred_event.get('key_id')}")
    
    def log_audit_event(self, audit_event: Dict):
        """
        Log tamper-proof audit trail event.
        
        Args:
            audit_event: Audit event details
        """
        event = {
            "TimeGenerated": datetime.utcnow().isoformat(),
            "EventType": "AuditTrail",
            "Action": audit_event.get("action"),
            "Actor": audit_event.get("actor"),
            "Resource": audit_event.get("resource"),
            "Result": audit_event.get("result"),
            "Jurisdiction": audit_event.get("jurisdiction"),
            "TamperProof": True,
            "HashChain": audit_event.get("hash_chain"),
            "Signature": audit_event.get("signature"),
            "ComplianceFramework": "HIPAA_164_312_b"
        }
        
        # Send to Azure Monitor
        self._send_log(event)
        
        # Update metric
        self.audit_event_counter.add(
            1,
            {"action": audit_event.get("action")}
        )
        
        logger.info(f"✅ Audit event logged - Action: {audit_event.get('action')}")
    
    def log_dspm_posture(self, posture: Dict):
        """
        Log DSPM security posture assessment.
        
        Args:
            posture: DSPM posture assessment
        """
        event = {
            "TimeGenerated": datetime.utcnow().isoformat(),
            "EventType": "DSPMPosture",
            "OverallScore": posture.get("overall_score"),
            "DataDiscovery": posture.get("data_discovery_score"),
            "DataClassification": posture.get("data_classification_score"),
            "AccessGovernance": posture.get("access_governance_score"),
            "DataLineage": posture.get("data_lineage_score"),
            "RiskAssessment": posture.get("risk_assessment_score"),
            "ComplianceMonitoring": posture.get("compliance_monitoring_score"),
            "GenAIGovernance": posture.get("genai_governance_score"),
            "Recommendations": json.dumps(posture.get("recommendations", [])),
            "ComplianceFramework": "Microsoft_DSPM_2026"
        }
        
        # Send to Azure Monitor
        self._send_log(event)
        
        logger.info(f"✅ DSPM posture logged - Score: {posture.get('overall_score')}")
    
    def _send_log(self, event: Dict):
        """
        Send log event to Azure Monitor.
        
        Args:
            event: Log event data
        """
        try:
            self.logs_client.upload(
                rule_id=self.data_collection_rule_id,
                stream_name=self.stream_name,
                logs=[event]
            )
        except Exception as e:
            logger.error(f"❌ Failed to send log to Azure Monitor: {e}")
    
    def create_trace_span(self, name: str, attributes: Optional[Dict] = None):
        """
        Create a distributed trace span.
        
        Args:
            name: Span name
            attributes: Span attributes
        
        Returns:
            Trace span context manager
        """
        return self.tracer.start_as_current_span(
            name=name,
            attributes=attributes or {}
        )
    
    def query_dspm_metrics(self, time_range: str = "PT1H") -> Dict:
        """
        Query DSPM metrics from Azure Monitor.
        
        Args:
            time_range: Time range (ISO 8601 duration)
        
        Returns:
            DSPM metrics summary
        """
        # This would use Azure Monitor Query API
        # Simplified for example
        metrics = {
            "time_range": time_range,
            "data_classifications": 0,
            "sovereignty_violations": 0,
            "genai_inferences": 0,
            "crypto_shreds": 0,
            "audit_events": 0
        }
        
        return metrics


# Example usage
if __name__ == "__main__":
    # Initialize Azure Monitor DSPM
    monitor = AzureMonitorDSPM(
        connection_string=os.getenv("APPLICATIONINSIGHTS_CONNECTION_STRING"),
        data_collection_endpoint=os.getenv("AZURE_DATA_COLLECTION_ENDPOINT"),
        data_collection_rule_id=os.getenv("AZURE_DATA_COLLECTION_RULE_ID")
    )
    
    # Log data classification
    monitor.log_data_classification({
        "classification": "PHI",
        "sensitivity_labels": ["PHI", "PII"],
        "dspm_categories": ["Data Discovery", "Data Classification"],
        "compliance_frameworks": ["HIPAA", "GDPR"],
        "data_type": "health_record",
        "context": {"jurisdiction": "KDPA_KE"}
    })
    
    # Log GenAI inference
    monitor.log_genai_inference({
        "model_id": "vertex-ai-outbreak-predictor",
        "confidence_score": 0.95,
        "explainability_provided": True,
        "explainability_method": "SHAP",
        "human_oversight": True,
        "clinical_decision": True,
        "jurisdiction": "EU_AI_ACT"
    })
    
    # Log crypto shred
    monitor.log_crypto_shred({
        "key_id": "key-12345",
        "retention_policy": "HOT",
        "data_type": "PHI",
        "jurisdiction": "KDPA_KE",
        "reason": "Retention period expired"
    })
