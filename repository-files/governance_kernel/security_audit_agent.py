"""
GenAI-Driven Security Audit Agent
Implements 2026 Data Security Index recommendation: 82% plan to use GenAI for security

Use Cases:
- Discover sensitive data (44% priority)
- Detect critical risks (43% priority)
- Investigate potential incidents (43% priority)

Compliance:
- SOC 2 (Security Monitoring & Incident Response)
- ISO 27001 A.16.1 (Management of Information Security Incidents)
- NIST CSF (Detect, Respond functions)
"""

import json
import os
from datetime import datetime, timedelta
from typing import Dict, List, Optional
from enum import Enum
from pathlib import Path
import logging

logger = logging.getLogger(__name__)


class IncidentSeverity(Enum):
    """Security incident severity levels"""
    CRITICAL = "CRITICAL"  # Immediate action required
    HIGH = "HIGH"  # Urgent attention needed
    MEDIUM = "MEDIUM"  # Should be addressed soon
    LOW = "LOW"  # Monitor and track
    INFO = "INFO"  # Informational only


class IncidentType(Enum):
    """Types of security incidents"""
    DATA_LEAK = "DATA_LEAK"
    UNAUTHORIZED_ACCESS = "UNAUTHORIZED_ACCESS"
    SOVEREIGNTY_VIOLATION = "SOVEREIGNTY_VIOLATION"
    GENAI_MISUSE = "GENAI_MISUSE"
    ANOMALOUS_BEHAVIOR = "ANOMALOUS_BEHAVIOR"
    POLICY_VIOLATION = "POLICY_VIOLATION"
    VULNERABILITY_DETECTED = "VULNERABILITY_DETECTED"


class SecurityAuditAgent:
    """
    Autonomous GenAI-driven security audit agent
    
    Leverages iLuminara Intelligence Engine to:
    1. Investigate potential security incidents
    2. Recommend controls
    3. Automatically block/flag risky patterns
    4. Maintain human oversight in final decisions
    """
    
    def __init__(
        self,
        auto_block_critical: bool = True,
        require_human_approval: bool = True,
        intelligence_engine_endpoint: Optional[str] = None
    ):
        self.auto_block_critical = auto_block_critical
        self.require_human_approval = require_human_approval
        self.intelligence_engine_endpoint = intelligence_engine_endpoint or "http://localhost:8080"
        
        # Investigation history
        self.investigations = []
        
        # Recommended controls
        self.recommended_controls = []
        
        # Blocked patterns
        self.blocked_patterns = []
        
        logger.info("🤖 Security Audit Agent initialized")
    
    def investigate_incident(
        self,
        incident_data: Dict,
        incident_type: IncidentType,
        auto_remediate: bool = False
    ) -> Dict:
        """
        Investigate a potential security incident using GenAI analysis
        
        Args:
            incident_data: Raw incident data
            incident_type: Type of incident
            auto_remediate: Whether to automatically apply remediation
        
        Returns:
            Investigation results with recommendations
        """
        
        logger.info(f"🔍 Investigating {incident_type.value} incident...")
        
        # Step 1: Analyze incident using GenAI
        analysis = self._analyze_with_genai(incident_data, incident_type)
        
        # Step 2: Determine severity
        severity = self._calculate_severity(analysis, incident_type)
        
        # Step 3: Generate recommendations
        recommendations = self._generate_recommendations(analysis, severity, incident_type)
        
        # Step 4: Auto-remediation (if enabled and critical)
        remediation_applied = False
        if auto_remediate and severity == IncidentSeverity.CRITICAL and self.auto_block_critical:
            remediation_applied = self._apply_remediation(recommendations)
        
        # Step 5: Create investigation record
        investigation = {
            "investigation_id": self._generate_investigation_id(),
            "timestamp": datetime.utcnow().isoformat(),
            "incident_type": incident_type.value,
            "severity": severity.value,
            "incident_data": incident_data,
            "analysis": analysis,
            "recommendations": recommendations,
            "remediation_applied": remediation_applied,
            "requires_human_review": self.require_human_approval or severity in [IncidentSeverity.CRITICAL, IncidentSeverity.HIGH],
            "status": "OPEN"
        }
        
        # Save investigation
        self.investigations.append(investigation)
        self._save_investigation(investigation)
        
        logger.info(f"✅ Investigation complete - Severity: {severity.value}, Remediation: {remediation_applied}")
        
        return investigation
    
    def discover_sensitive_data(self, scan_paths: Optional[List[str]] = None) -> Dict:
        """
        Discover sensitive data across the environment (44% priority in 2026 DSI)
        
        Uses DSPM engine + GenAI analysis
        
        Returns:
            Discovery results
        """
        
        logger.info("🔍 Starting sensitive data discovery...")
        
        # Import DSPM engine
        try:
            from governance_kernel.dspm_engine import DSPMEngine
            
            dspm = DSPMEngine(scan_paths=scan_paths)
            scan_results = dspm.run_full_scan()
            
            # Analyze results with GenAI
            analysis = self._analyze_dspm_results(scan_results)
            
            # Generate recommendations
            recommendations = self._generate_dspm_recommendations(analysis)
            
            return {
                "discovery_date": datetime.utcnow().isoformat(),
                "scan_results": scan_results,
                "genai_analysis": analysis,
                "recommendations": recommendations
            }
        
        except ImportError:
            logger.error("DSPM Engine not available")
            return {"error": "DSPM Engine not available"}
    
    def detect_critical_risks(self) -> List[Dict]:
        """
        Detect critical security risks (43% priority in 2026 DSI)
        
        Returns:
            List of detected risks
        """
        
        logger.info("🔍 Detecting critical risks...")
        
        risks = []
        
        # Risk 1: Check for sovereignty violations
        sovereignty_risks = self._check_sovereignty_violations()
        risks.extend(sovereignty_risks)
        
        # Risk 2: Check for GenAI misuse
        genai_risks = self._check_genai_misuse()
        risks.extend(genai_risks)
        
        # Risk 3: Check for anomalous access patterns
        access_risks = self._check_anomalous_access()
        risks.extend(access_risks)
        
        # Risk 4: Check for unpatched vulnerabilities
        vuln_risks = self._check_vulnerabilities()
        risks.extend(vuln_risks)
        
        # Prioritize by severity
        risks.sort(key=lambda r: self._severity_to_int(r['severity']), reverse=True)
        
        logger.info(f"✅ Detected {len(risks)} critical risks")
        
        return risks
    
    def recommend_controls(self, risk_assessment: Dict) -> List[Dict]:
        """
        Recommend security controls based on risk assessment
        
        Returns:
            List of recommended controls
        """
        
        controls = []
        
        # Analyze risk assessment
        for risk in risk_assessment.get('risks', []):
            control = self._recommend_control_for_risk(risk)
            if control:
                controls.append(control)
        
        # Save recommendations
        self.recommended_controls.extend(controls)
        
        return controls
    
    def auto_block_risky_pattern(
        self,
        pattern: str,
        pattern_type: str,
        severity: IncidentSeverity,
        reason: str
    ) -> bool:
        """
        Automatically block a risky pattern
        
        Args:
            pattern: Pattern to block (regex or string)
            pattern_type: Type of pattern (e.g., "prompt", "access", "data")
            severity: Severity level
            reason: Reason for blocking
        
        Returns:
            True if blocked successfully
        """
        
        # Require human approval for non-critical blocks
        if severity != IncidentSeverity.CRITICAL and self.require_human_approval:
            logger.info(f"⏸️  Pattern requires human approval: {pattern}")
            return False
        
        blocked_pattern = {
            "pattern": pattern,
            "pattern_type": pattern_type,
            "severity": severity.value,
            "reason": reason,
            "blocked_at": datetime.utcnow().isoformat(),
            "auto_blocked": True
        }
        
        self.blocked_patterns.append(blocked_pattern)
        self._save_blocked_pattern(blocked_pattern)
        
        logger.warning(f"🚫 Pattern blocked: {pattern} - {reason}")
        
        return True
    
    def _analyze_with_genai(self, incident_data: Dict, incident_type: IncidentType) -> Dict:
        """
        Analyze incident using GenAI (simulated - would use actual LLM in production)
        
        Returns:
            GenAI analysis
        """
        
        # In production, this would call the iLuminara Intelligence Engine
        # For now, return rule-based analysis
        
        analysis = {
            "incident_type": incident_type.value,
            "timestamp": datetime.utcnow().isoformat(),
            "findings": [],
            "confidence": 0.0
        }
        
        if incident_type == IncidentType.DATA_LEAK:
            analysis["findings"].append("Sensitive data detected in unauthorized location")
            analysis["confidence"] = 0.95
        
        elif incident_type == IncidentType.SOVEREIGNTY_VIOLATION:
            analysis["findings"].append("Cross-border data transfer without authorization")
            analysis["confidence"] = 0.98
        
        elif incident_type == IncidentType.GENAI_MISUSE:
            analysis["findings"].append("Unauthorized GenAI tool usage detected")
            analysis["confidence"] = 0.87
        
        elif incident_type == IncidentType.ANOMALOUS_BEHAVIOR:
            analysis["findings"].append("User behavior deviates from baseline")
            analysis["confidence"] = 0.72
        
        return analysis
    
    def _calculate_severity(self, analysis: Dict, incident_type: IncidentType) -> IncidentSeverity:
        """Calculate incident severity"""
        
        confidence = analysis.get("confidence", 0.0)
        
        # Critical incidents
        if incident_type in [IncidentType.DATA_LEAK, IncidentType.SOVEREIGNTY_VIOLATION]:
            if confidence > 0.9:
                return IncidentSeverity.CRITICAL
            elif confidence > 0.7:
                return IncidentSeverity.HIGH
        
        # High severity incidents
        if incident_type in [IncidentType.UNAUTHORIZED_ACCESS, IncidentType.GENAI_MISUSE]:
            if confidence > 0.8:
                return IncidentSeverity.HIGH
            elif confidence > 0.6:
                return IncidentSeverity.MEDIUM
        
        # Default to medium
        return IncidentSeverity.MEDIUM
    
    def _generate_recommendations(
        self,
        analysis: Dict,
        severity: IncidentSeverity,
        incident_type: IncidentType
    ) -> List[Dict]:
        """Generate remediation recommendations"""
        
        recommendations = []
        
        if incident_type == IncidentType.DATA_LEAK:
            recommendations.append({
                "action": "IMMEDIATE_CONTAINMENT",
                "description": "Isolate affected systems and revoke access",
                "priority": "CRITICAL"
            })
            recommendations.append({
                "action": "CRYPTO_SHRED",
                "description": "Shred encryption keys for leaked data",
                "priority": "HIGH"
            })
        
        elif incident_type == IncidentType.SOVEREIGNTY_VIOLATION:
            recommendations.append({
                "action": "BLOCK_TRANSFER",
                "description": "Block cross-border data transfer",
                "priority": "CRITICAL"
            })
            recommendations.append({
                "action": "AUDIT_REVIEW",
                "description": "Review all recent cross-border transfers",
                "priority": "HIGH"
            })
        
        elif incident_type == IncidentType.GENAI_MISUSE:
            recommendations.append({
                "action": "BLOCK_USER",
                "description": "Temporarily suspend user's GenAI access",
                "priority": "HIGH"
            })
            recommendations.append({
                "action": "SECURITY_TRAINING",
                "description": "Require security training before re-enabling access",
                "priority": "MEDIUM"
            })
        
        return recommendations
    
    def _apply_remediation(self, recommendations: List[Dict]) -> bool:
        """Apply automatic remediation"""
        
        applied = False
        
        for rec in recommendations:
            if rec["priority"] == "CRITICAL":
                logger.warning(f"🔧 Applying remediation: {rec['action']}")
                # In production, this would actually execute the remediation
                applied = True
        
        return applied
    
    def _check_sovereignty_violations(self) -> List[Dict]:
        """Check for sovereignty violations"""
        
        risks = []
        
        # Load sovereignty violation logs
        audit_file = Path("./keys/audit.jsonl")
        
        if audit_file.exists():
            with open(audit_file, 'r') as f:
                for line in f:
                    try:
                        entry = json.loads(line)
                        if "VIOLATION" in entry.get("action", ""):
                            risks.append({
                                "risk_type": "SOVEREIGNTY_VIOLATION",
                                "severity": IncidentSeverity.CRITICAL.value,
                                "description": entry.get("action"),
                                "timestamp": entry.get("timestamp")
                            })
                    except json.JSONDecodeError:
                        continue
        
        return risks[-10:]  # Last 10 violations
    
    def _check_genai_misuse(self) -> List[Dict]:
        """Check for GenAI misuse"""
        
        risks = []
        
        # Load GenAI violation logs
        violation_file = Path("./security_telemetry/genai_violations.jsonl")
        
        if violation_file.exists():
            with open(violation_file, 'r') as f:
                for line in f:
                    try:
                        entry = json.loads(line)
                        risks.append({
                            "risk_type": "GENAI_MISUSE",
                            "severity": IncidentSeverity.HIGH.value,
                            "description": entry.get("violation_type"),
                            "timestamp": entry.get("timestamp")
                        })
                    except json.JSONDecodeError:
                        continue
        
        return risks[-10:]
    
    def _check_anomalous_access(self) -> List[Dict]:
        """Check for anomalous access patterns"""
        
        # Would integrate with DSPM engine in production
        return []
    
    def _check_vulnerabilities(self) -> List[Dict]:
        """Check for unpatched vulnerabilities"""
        
        # Would integrate with CodeQL/Dependabot results
        return []
    
    def _recommend_control_for_risk(self, risk: Dict) -> Optional[Dict]:
        """Recommend control for a specific risk"""
        
        risk_type = risk.get("risk_type")
        
        if risk_type == "SOVEREIGNTY_VIOLATION":
            return {
                "control_id": "SOV-001",
                "control_name": "Enhanced Data Residency Enforcement",
                "description": "Implement stricter data residency controls",
                "implementation": "Update SovereignGuardrail configuration"
            }
        
        elif risk_type == "GENAI_MISUSE":
            return {
                "control_id": "GENAI-001",
                "control_name": "GenAI Usage Policy Enforcement",
                "description": "Enforce mandatory training and approval workflow",
                "implementation": "Enable GenAI guardrail with approval gates"
            }
        
        return None
    
    def _severity_to_int(self, severity: str) -> int:
        """Convert severity to integer for sorting"""
        severity_map = {
            "CRITICAL": 4,
            "HIGH": 3,
            "MEDIUM": 2,
            "LOW": 1,
            "INFO": 0
        }
        return severity_map.get(severity, 0)
    
    def _generate_investigation_id(self) -> str:
        """Generate unique investigation ID"""
        import hashlib
        timestamp = datetime.utcnow().isoformat()
        return f"INV-{hashlib.sha256(timestamp.encode()).hexdigest()[:12].upper()}"
    
    def _save_investigation(self, investigation: Dict):
        """Save investigation to disk"""
        output_dir = Path("./security_telemetry/investigations")
        output_dir.mkdir(parents=True, exist_ok=True)
        
        output_file = output_dir / f"{investigation['investigation_id']}.json"
        
        with open(output_file, 'w') as f:
            json.dump(investigation, f, indent=2)
    
    def _save_blocked_pattern(self, pattern: Dict):
        """Save blocked pattern to disk"""
        output_file = Path("./security_telemetry/blocked_patterns.jsonl")
        
        with open(output_file, 'a') as f:
            f.write(json.dumps(pattern) + '\n')
    
    def _analyze_dspm_results(self, scan_results: Dict) -> Dict:
        """Analyze DSPM scan results with GenAI"""
        
        summary = scan_results.get("summary", {})
        
        analysis = {
            "total_findings": summary.get("total_findings", 0),
            "critical_files": len(summary.get("critical_files", [])),
            "risk_assessment": "HIGH" if summary.get("total_findings", 0) > 10 else "MEDIUM",
            "recommendations": []
        }
        
        # Generate recommendations based on findings
        if analysis["total_findings"] > 0:
            analysis["recommendations"].append("Implement data classification policies")
            analysis["recommendations"].append("Enable automatic data redaction")
        
        return analysis
    
    def _generate_dspm_recommendations(self, analysis: Dict) -> List[Dict]:
        """Generate recommendations from DSPM analysis"""
        
        recommendations = []
        
        if analysis.get("risk_assessment") == "HIGH":
            recommendations.append({
                "priority": "CRITICAL",
                "action": "IMMEDIATE_REVIEW",
                "description": "Review all critical files for data exposure"
            })
        
        for rec in analysis.get("recommendations", []):
            recommendations.append({
                "priority": "HIGH",
                "action": "IMPLEMENT_CONTROL",
                "description": rec
            })
        
        return recommendations


# Example usage
if __name__ == "__main__":
    import os
    os.makedirs("./security_telemetry", exist_ok=True)
    
    logging.basicConfig(level=logging.INFO)
    
    # Initialize security audit agent
    agent = SecurityAuditAgent(
        auto_block_critical=True,
        require_human_approval=True
    )
    
    # Test 1: Investigate data leak
    incident = agent.investigate_incident(
        incident_data={
            "file": "api_service.py",
            "line": 145,
            "data_type": "PHI",
            "exposure": "public_endpoint"
        },
        incident_type=IncidentType.DATA_LEAK,
        auto_remediate=True
    )
    
    print(f"\n🔍 Investigation: {incident['investigation_id']}")
    print(f"   Severity: {incident['severity']}")
    print(f"   Remediation Applied: {incident['remediation_applied']}")
    
    # Test 2: Detect critical risks
    risks = agent.detect_critical_risks()
    print(f"\n⚠️  Critical Risks Detected: {len(risks)}")
    
    # Test 3: Discover sensitive data
    discovery = agent.discover_sensitive_data()
    print(f"\n🔍 Sensitive Data Discovery:")
    print(f"   Total Findings: {discovery.get('genai_analysis', {}).get('total_findings', 0)}")
