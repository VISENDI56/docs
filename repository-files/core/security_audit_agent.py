"""
GenAI-Driven Security Audit Agent
Aligns with 2026 Data Security Index: 82% plan to use GenAI in security programs

Key Capabilities:
- Discover sensitive data (44% top use case)
- Detect critical risks (43% top use case)
- Investigate potential incidents (43% top use case)
- Recommend controls with human oversight

Compliance:
- EU AI Act §8 (Transparency & Human Oversight)
- ISO 27001 A.12.4 (Logging and Monitoring)
- SOC 2 (Incident Response)
"""

import json
import os
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
from enum import Enum
import logging

logger = logging.getLogger(__name__)


class IncidentSeverity(Enum):
    """Incident severity levels"""
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"
    INFO = "info"


class IncidentStatus(Enum):
    """Incident investigation status"""
    DETECTED = "detected"
    INVESTIGATING = "investigating"
    ANALYZED = "analyzed"
    RESOLVED = "resolved"
    FALSE_POSITIVE = "false_positive"


class SecurityAuditAgent:
    """
    Autonomous GenAI-powered security audit agent
    
    Uses iLuminara Intelligence Engine to investigate data security incidents
    in real-time with human oversight in the final decision loop.
    """
    
    def __init__(
        self,
        jurisdiction: str = "KDPA_KE",
        enable_auto_response: bool = False,
        require_human_approval: bool = True
    ):
        self.jurisdiction = jurisdiction
        self.enable_auto_response = enable_auto_response
        self.require_human_approval = require_human_approval
        
        # Incident tracking
        self.incidents = []
        self.investigation_log = []
        
        # Risk patterns
        self.risk_patterns = self._initialize_risk_patterns()
        
        logger.info(f"🤖 Security Audit Agent initialized - Jurisdiction: {jurisdiction}")
        logger.info(f"   Auto-response: {enable_auto_response}")
        logger.info(f"   Human approval required: {require_human_approval}")
    
    def _initialize_risk_patterns(self) -> Dict:
        """Initialize known risk patterns"""
        return {
            "data_exfiltration": {
                "indicators": [
                    "large_data_transfer",
                    "unusual_access_time",
                    "unauthorized_endpoint",
                    "rapid_sequential_access"
                ],
                "severity": IncidentSeverity.CRITICAL,
                "recommended_actions": [
                    "Block user access immediately",
                    "Isolate affected systems",
                    "Notify security team",
                    "Initiate forensic investigation"
                ]
            },
            "unauthorized_access": {
                "indicators": [
                    "failed_authentication_attempts",
                    "access_from_unusual_location",
                    "privilege_escalation_attempt",
                    "access_outside_business_hours"
                ],
                "severity": IncidentSeverity.HIGH,
                "recommended_actions": [
                    "Lock user account",
                    "Require MFA re-authentication",
                    "Review access logs",
                    "Notify user and security team"
                ]
            },
            "data_misconfiguration": {
                "indicators": [
                    "public_exposure_of_phi",
                    "weak_encryption",
                    "missing_access_controls",
                    "retention_policy_violation"
                ],
                "severity": IncidentSeverity.HIGH,
                "recommended_actions": [
                    "Restrict access immediately",
                    "Enable encryption",
                    "Apply access controls",
                    "Audit affected data"
                ]
            },
            "genai_data_leak": {
                "indicators": [
                    "phi_in_prompt",
                    "unauthorized_llm_endpoint",
                    "sensitive_data_in_response",
                    "excessive_genai_usage"
                ],
                "severity": IncidentSeverity.CRITICAL,
                "recommended_actions": [
                    "Block GenAI access",
                    "Sanitize prompts",
                    "Review user training",
                    "Implement leak prevention controls"
                ]
            },
            "compliance_violation": {
                "indicators": [
                    "cross_border_transfer_without_consent",
                    "retention_period_exceeded",
                    "missing_audit_trail",
                    "unauthorized_data_processing"
                ],
                "severity": IncidentSeverity.HIGH,
                "recommended_actions": [
                    "Halt violating operation",
                    "Notify Data Protection Officer",
                    "Document incident",
                    "Implement corrective controls"
                ]
            }
        }
    
    def detect_incident(
        self,
        event_type: str,
        event_data: Dict,
        source: str
    ) -> Optional[Dict]:
        """
        Detect potential security incident from event data
        
        Returns:
            Incident object if detected, None otherwise
        """
        # Match event to risk patterns
        matched_pattern = None
        matched_indicators = []
        
        for pattern_name, pattern_data in self.risk_patterns.items():
            for indicator in pattern_data["indicators"]:
                if indicator in event_data.get("indicators", []):
                    matched_indicators.append(indicator)
                    matched_pattern = pattern_name
        
        if not matched_pattern:
            return None
        
        # Create incident
        incident = {
            "incident_id": self._generate_incident_id(),
            "timestamp": datetime.utcnow().isoformat(),
            "event_type": event_type,
            "pattern": matched_pattern,
            "severity": self.risk_patterns[matched_pattern]["severity"].value,
            "status": IncidentStatus.DETECTED.value,
            "indicators": matched_indicators,
            "event_data": event_data,
            "source": source,
            "investigation": None,
            "recommended_actions": self.risk_patterns[matched_pattern]["recommended_actions"],
            "actions_taken": [],
            "human_approval_required": self.require_human_approval,
            "human_approved": False
        }
        
        self.incidents.append(incident)
        
        logger.warning(f"🚨 Incident detected: {incident['incident_id']} - {matched_pattern}")
        
        return incident
    
    def investigate_incident(self, incident_id: str) -> Dict:
        """
        Use GenAI to investigate an incident
        
        Returns:
            Investigation report with analysis and recommendations
        """
        # Find incident
        incident = next((i for i in self.incidents if i["incident_id"] == incident_id), None)
        
        if not incident:
            logger.error(f"Incident not found: {incident_id}")
            return {"error": "Incident not found"}
        
        # Update status
        incident["status"] = IncidentStatus.INVESTIGATING.value
        
        logger.info(f"🔍 Investigating incident: {incident_id}")
        
        # Analyze incident using GenAI reasoning
        investigation = self._analyze_incident(incident)
        
        # Update incident with investigation results
        incident["investigation"] = investigation
        incident["status"] = IncidentStatus.ANALYZED.value
        
        # Log investigation
        self.investigation_log.append({
            "incident_id": incident_id,
            "timestamp": datetime.utcnow().isoformat(),
            "investigation": investigation
        })
        
        logger.info(f"✅ Investigation complete: {incident_id}")
        
        return investigation
    
    def _analyze_incident(self, incident: Dict) -> Dict:
        """
        Analyze incident using GenAI reasoning
        
        This simulates GenAI analysis. In production, this would call
        the iLuminara Intelligence Engine (Vertex AI) for deep analysis.
        """
        pattern = incident["pattern"]
        indicators = incident["indicators"]
        event_data = incident["event_data"]
        
        # Simulate GenAI analysis
        analysis = {
            "timestamp": datetime.utcnow().isoformat(),
            "pattern_matched": pattern,
            "confidence_score": 0.85,
            "risk_assessment": {
                "severity": incident["severity"],
                "impact": self._assess_impact(incident),
                "likelihood": self._assess_likelihood(incident),
                "risk_score": 0.0  # Will be calculated
            },
            "root_cause_analysis": self._perform_root_cause_analysis(incident),
            "affected_assets": self._identify_affected_assets(incident),
            "recommended_controls": self._recommend_controls(incident),
            "evidence_chain": indicators,
            "compliance_implications": self._assess_compliance_impact(incident),
            "human_review_required": True  # Always require human review
        }
        
        # Calculate risk score
        impact_score = {"critical": 10, "high": 7, "medium": 5, "low": 3}[analysis["risk_assessment"]["impact"]]
        likelihood_score = analysis["risk_assessment"]["likelihood"]
        analysis["risk_assessment"]["risk_score"] = impact_score * likelihood_score / 10
        
        return analysis
    
    def _assess_impact(self, incident: Dict) -> str:
        """Assess potential impact of incident"""
        severity = incident["severity"]
        pattern = incident["pattern"]
        
        if pattern in ["data_exfiltration", "genai_data_leak"]:
            return "critical"
        elif pattern in ["unauthorized_access", "data_misconfiguration"]:
            return "high"
        else:
            return "medium"
    
    def _assess_likelihood(self, incident: Dict) -> float:
        """Assess likelihood of incident (0-1)"""
        indicators = incident["indicators"]
        
        # More indicators = higher likelihood
        return min(len(indicators) / 5.0, 1.0)
    
    def _perform_root_cause_analysis(self, incident: Dict) -> Dict:
        """Perform root cause analysis"""
        pattern = incident["pattern"]
        
        root_causes = {
            "data_exfiltration": {
                "primary": "Insufficient access controls",
                "secondary": ["Lack of data loss prevention", "Missing anomaly detection"],
                "contributing_factors": ["User training gap", "Policy enforcement weakness"]
            },
            "unauthorized_access": {
                "primary": "Weak authentication",
                "secondary": ["Missing MFA", "Inadequate monitoring"],
                "contributing_factors": ["Password policy weakness", "Lack of user awareness"]
            },
            "data_misconfiguration": {
                "primary": "Configuration error",
                "secondary": ["Lack of automated checks", "Missing security review"],
                "contributing_factors": ["Human error", "Insufficient testing"]
            },
            "genai_data_leak": {
                "primary": "Insufficient GenAI controls",
                "secondary": ["Lack of prompt filtering", "Missing user training"],
                "contributing_factors": ["Policy gap", "Technology limitation"]
            },
            "compliance_violation": {
                "primary": "Policy non-compliance",
                "secondary": ["Lack of enforcement", "Missing controls"],
                "contributing_factors": ["User awareness gap", "Process weakness"]
            }
        }
        
        return root_causes.get(pattern, {"primary": "Unknown", "secondary": [], "contributing_factors": []})
    
    def _identify_affected_assets(self, incident: Dict) -> List[str]:
        """Identify assets affected by incident"""
        event_data = incident["event_data"]
        
        affected = []
        
        if "file_path" in event_data:
            affected.append(f"File: {event_data['file_path']}")
        
        if "user_id" in event_data:
            affected.append(f"User: {event_data['user_id']}")
        
        if "endpoint" in event_data:
            affected.append(f"Endpoint: {event_data['endpoint']}")
        
        if "data_classification" in event_data:
            affected.append(f"Data Type: {event_data['data_classification']}")
        
        return affected
    
    def _recommend_controls(self, incident: Dict) -> List[Dict]:
        """Recommend security controls to prevent recurrence"""
        pattern = incident["pattern"]
        
        controls = {
            "data_exfiltration": [
                {"control": "Data Loss Prevention (DLP)", "priority": "critical", "implementation": "Deploy DLP solution with real-time monitoring"},
                {"control": "Network Segmentation", "priority": "high", "implementation": "Isolate sensitive data networks"},
                {"control": "User Behavior Analytics", "priority": "high", "implementation": "Implement UBA for anomaly detection"}
            ],
            "unauthorized_access": [
                {"control": "Multi-Factor Authentication", "priority": "critical", "implementation": "Enforce MFA for all users"},
                {"control": "Privileged Access Management", "priority": "high", "implementation": "Implement PAM solution"},
                {"control": "Access Review", "priority": "medium", "implementation": "Quarterly access rights review"}
            ],
            "data_misconfiguration": [
                {"control": "Configuration Management", "priority": "high", "implementation": "Automated configuration scanning"},
                {"control": "Security Baseline", "priority": "high", "implementation": "Enforce security baseline policies"},
                {"control": "Change Management", "priority": "medium", "implementation": "Require security review for changes"}
            ],
            "genai_data_leak": [
                {"control": "GenAI Guardrails", "priority": "critical", "implementation": "Deploy prompt filtering and response sanitization"},
                {"control": "User Training", "priority": "high", "implementation": "GenAI security awareness training"},
                {"control": "Endpoint Control", "priority": "high", "implementation": "Whitelist approved GenAI endpoints"}
            ],
            "compliance_violation": [
                {"control": "Policy Enforcement", "priority": "critical", "implementation": "Automated policy compliance checks"},
                {"control": "Audit Trail", "priority": "high", "implementation": "Tamper-proof audit logging"},
                {"control": "Compliance Monitoring", "priority": "high", "implementation": "Real-time compliance dashboard"}
            ]
        }
        
        return controls.get(pattern, [])
    
    def _assess_compliance_impact(self, incident: Dict) -> Dict:
        """Assess compliance implications"""
        pattern = incident["pattern"]
        severity = incident["severity"]
        
        frameworks_impacted = []
        
        if pattern in ["data_exfiltration", "genai_data_leak"]:
            frameworks_impacted = ["GDPR Art. 9", "HIPAA §164.312", "KDPA §37"]
        elif pattern == "unauthorized_access":
            frameworks_impacted = ["GDPR Art. 32", "HIPAA §164.308", "ISO 27001 A.9"]
        elif pattern == "data_misconfiguration":
            frameworks_impacted = ["GDPR Art. 32", "ISO 27001 A.12", "SOC 2"]
        elif pattern == "compliance_violation":
            frameworks_impacted = ["GDPR", "HIPAA", "KDPA", "POPIA"]
        
        notification_required = severity in ["critical", "high"]
        
        return {
            "frameworks_impacted": frameworks_impacted,
            "notification_required": notification_required,
            "notification_deadline": (datetime.utcnow() + timedelta(hours=72)).isoformat() if notification_required else None,
            "regulatory_risk": "high" if notification_required else "medium"
        }
    
    def recommend_response(self, incident_id: str) -> Dict:
        """
        Recommend response actions for an incident
        
        Returns:
            Response plan with actions and approval status
        """
        incident = next((i for i in self.incidents if i["incident_id"] == incident_id), None)
        
        if not incident or not incident.get("investigation"):
            return {"error": "Incident not investigated"}
        
        investigation = incident["investigation"]
        
        response_plan = {
            "incident_id": incident_id,
            "timestamp": datetime.utcnow().isoformat(),
            "immediate_actions": self._get_immediate_actions(incident),
            "short_term_actions": investigation["recommended_controls"],
            "long_term_actions": self._get_long_term_actions(incident),
            "estimated_effort": self._estimate_effort(incident),
            "requires_human_approval": self.require_human_approval,
            "auto_response_enabled": self.enable_auto_response
        }
        
        return response_plan
    
    def _get_immediate_actions(self, incident: Dict) -> List[Dict]:
        """Get immediate response actions"""
        pattern = incident["pattern"]
        
        immediate = {
            "data_exfiltration": [
                {"action": "Block user access", "automated": True, "priority": "critical"},
                {"action": "Isolate affected systems", "automated": False, "priority": "critical"},
                {"action": "Notify security team", "automated": True, "priority": "critical"}
            ],
            "unauthorized_access": [
                {"action": "Lock user account", "automated": True, "priority": "high"},
                {"action": "Require MFA re-authentication", "automated": True, "priority": "high"}
            ],
            "data_misconfiguration": [
                {"action": "Restrict access", "automated": True, "priority": "high"},
                {"action": "Enable encryption", "automated": False, "priority": "high"}
            ],
            "genai_data_leak": [
                {"action": "Block GenAI access", "automated": True, "priority": "critical"},
                {"action": "Sanitize prompts", "automated": True, "priority": "critical"}
            ],
            "compliance_violation": [
                {"action": "Halt violating operation", "automated": True, "priority": "high"},
                {"action": "Notify DPO", "automated": True, "priority": "high"}
            ]
        }
        
        return immediate.get(pattern, [])
    
    def _get_long_term_actions(self, incident: Dict) -> List[Dict]:
        """Get long-term remediation actions"""
        return [
            {"action": "Review and update security policies", "timeline": "30 days"},
            {"action": "Conduct security awareness training", "timeline": "60 days"},
            {"action": "Implement recommended controls", "timeline": "90 days"},
            {"action": "Perform security audit", "timeline": "90 days"}
        ]
    
    def _estimate_effort(self, incident: Dict) -> Dict:
        """Estimate effort required for remediation"""
        severity = incident["severity"]
        
        effort_map = {
            "critical": {"hours": 40, "cost": "high", "resources": "multiple_teams"},
            "high": {"hours": 20, "cost": "medium", "resources": "security_team"},
            "medium": {"hours": 8, "cost": "low", "resources": "security_team"},
            "low": {"hours": 2, "cost": "minimal", "resources": "single_engineer"}
        }
        
        return effort_map.get(severity, effort_map["medium"])
    
    def _generate_incident_id(self) -> str:
        """Generate unique incident ID"""
        timestamp = datetime.utcnow().strftime("%Y%m%d%H%M%S")
        return f"INC-{timestamp}-{len(self.incidents) + 1:04d}"
    
    def export_incidents(self, output_path: str = "./security_telemetry/incidents.json"):
        """Export incidents to JSON"""
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
        with open(output_path, 'w') as f:
            json.dump(self.incidents, f, indent=2)
        
        logger.info(f"📊 Incidents exported to {output_path}")


# Example usage
if __name__ == "__main__":
    # Initialize security audit agent
    agent = SecurityAuditAgent(
        jurisdiction="KDPA_KE",
        enable_auto_response=False,
        require_human_approval=True
    )
    
    # Simulate incident detection
    incident = agent.detect_incident(
        event_type="genai_interaction",
        event_data={
            "indicators": ["phi_in_prompt", "unauthorized_llm_endpoint"],
            "user_id": "dr_john_doe",
            "endpoint": "https://api.openai.com",
            "prompt_hash": "abc123",
            "data_classification": "PHI"
        },
        source="GenAI Guardrail"
    )
    
    if incident:
        print(f"🚨 Incident Detected: {incident['incident_id']}")
        print(f"   Pattern: {incident['pattern']}")
        print(f"   Severity: {incident['severity']}")
        print()
        
        # Investigate
        investigation = agent.investigate_incident(incident['incident_id'])
        print(f"🔍 Investigation Complete:")
        print(f"   Confidence: {investigation['confidence_score']:.0%}")
        print(f"   Risk Score: {investigation['risk_assessment']['risk_score']:.1f}/10")
        print(f"   Root Cause: {investigation['root_cause_analysis']['primary']}")
        print()
        
        # Recommend response
        response = agent.recommend_response(incident['incident_id'])
        print(f"💡 Response Plan:")
        print(f"   Immediate Actions: {len(response['immediate_actions'])}")
        print(f"   Estimated Effort: {response['estimated_effort']['hours']} hours")
        print(f"   Human Approval Required: {response['requires_human_approval']}")
        print()
        
        # Export
        agent.export_incidents()
