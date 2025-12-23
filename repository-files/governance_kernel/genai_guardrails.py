"""
GenAI SovereignGuardrail Reinforcement
Aligns with 2026 Data Security Index: 32% of incidents involve GenAI

Key Controls:
- Leak Filter: Intercepts prompts to prevent PHI/PII uploads
- Anomaly Detection: Identifies unauthorized GenAI tool usage
- Response Filtering: Sanitizes AI outputs for sensitive data
- Usage Monitoring: Tracks GenAI interactions for compliance

Compliance:
- GDPR Art. 9 (Special Categories of Data)
- HIPAA §164.312(e)(1) (Transmission Security)
- EU AI Act §8 (Transparency)
"""

import re
import json
import hashlib
from datetime import datetime
from typing import Dict, List, Optional, Tuple
from enum import Enum
import logging

logger = logging.getLogger(__name__)


class GenAIRiskLevel(Enum):
    """GenAI risk severity levels"""
    CRITICAL = "critical"  # PHI/PII upload attempt
    HIGH = "high"  # Unauthorized LLM access
    MEDIUM = "medium"  # Suspicious prompt patterns
    LOW = "low"  # Minor policy violations
    NONE = "none"  # Clean


class GenAIAction(Enum):
    """Actions to take on GenAI violations"""
    BLOCK = "block"  # Block the request entirely
    SANITIZE = "sanitize"  # Remove sensitive data and allow
    FLAG = "flag"  # Allow but log for review
    ALLOW = "allow"  # No action needed


class GenAIGuardrail:
    """
    GenAI-specific security guardrails
    
    Prevents sensitive health data from being uploaded to external LLMs
    and detects anomalous GenAI usage patterns.
    """
    
    def __init__(
        self,
        jurisdiction: str = "KDPA_KE",
        enable_leak_filter: bool = True,
        enable_anomaly_detection: bool = True,
        enable_response_filtering: bool = True
    ):
        self.jurisdiction = jurisdiction
        self.enable_leak_filter = enable_leak_filter
        self.enable_anomaly_detection = enable_anomaly_detection
        self.enable_response_filtering = enable_response_filtering
        
        # Sensitive data patterns
        self.sensitive_patterns = self._initialize_sensitive_patterns()
        
        # Blocked LLM endpoints
        self.blocked_endpoints = [
            "api.openai.com",
            "api.anthropic.com",
            "generativelanguage.googleapis.com",
            "api.cohere.ai"
        ]
        
        # Allowed internal endpoints
        self.allowed_endpoints = [
            "localhost",
            "127.0.0.1",
            "iluminara.health",
            "vertex-ai.googleapis.com"  # Sovereign GCP deployment
        ]
        
        # Usage tracking
        self.usage_log = []
        
        logger.info(f"🤖 GenAI Guardrail initialized - Jurisdiction: {jurisdiction}")
    
    def _initialize_sensitive_patterns(self) -> Dict[str, List[re.Pattern]]:
        """Initialize patterns for detecting sensitive data in prompts"""
        return {
            "PHI": [
                re.compile(r'\b(patient|diagnosis|treatment|medication|prescription)\b', re.IGNORECASE),
                re.compile(r'\b(symptom|disease|condition|vital_signs|lab_result)\b', re.IGNORECASE),
                re.compile(r'\b(medical_record|health_record|clinical_note)\b', re.IGNORECASE),
                re.compile(r'\b(blood_pressure|heart_rate|temperature|oxygen)\b', re.IGNORECASE),
            ],
            "PII": [
                re.compile(r'\b[A-Z][a-z]+ [A-Z][a-z]+\b'),  # Names
                re.compile(r'\b\d{3}-\d{2}-\d{4}\b'),  # SSN
                re.compile(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'),  # Email
                re.compile(r'\b\d{10,15}\b'),  # Phone
                re.compile(r'\b(passport|driver_license|national_id):\s*\w+\b', re.IGNORECASE),
            ],
            "LOCATION": [
                re.compile(r'\b\d{1,5}\s\w+\s(Street|St|Avenue|Ave|Road|Rd)\b', re.IGNORECASE),
                re.compile(r'\b(latitude|longitude|GPS|coordinates):\s*[\d\.\-]+\b', re.IGNORECASE),
            ],
            "FINANCIAL": [
                re.compile(r'\b\d{4}[-\s]?\d{4}[-\s]?\d{4}[-\s]?\d{4}\b'),  # Credit card
                re.compile(r'\b(account_number|routing_number|iban):\s*\w+\b', re.IGNORECASE),
            ]
        }
    
    def scan_prompt(self, prompt: str) -> Tuple[GenAIRiskLevel, List[str], str]:
        """
        Scan a prompt for sensitive data
        
        Returns:
            (risk_level, detected_types, sanitized_prompt)
        """
        detected_types = []
        risk_level = GenAIRiskLevel.NONE
        
        for data_type, patterns in self.sensitive_patterns.items():
            for pattern in patterns:
                if pattern.search(prompt):
                    detected_types.append(data_type)
                    
                    # Escalate risk level
                    if data_type in ["PHI", "PII"]:
                        risk_level = GenAIRiskLevel.CRITICAL
                    elif data_type == "FINANCIAL" and risk_level.value != "critical":
                        risk_level = GenAIRiskLevel.HIGH
                    elif risk_level.value == "none":
                        risk_level = GenAIRiskLevel.MEDIUM
        
        # Sanitize prompt
        sanitized_prompt = self._sanitize_prompt(prompt)
        
        return risk_level, list(set(detected_types)), sanitized_prompt
    
    def _sanitize_prompt(self, prompt: str) -> str:
        """Remove sensitive data from prompt"""
        sanitized = prompt
        
        for data_type, patterns in self.sensitive_patterns.items():
            for pattern in patterns:
                sanitized = pattern.sub(f"[REDACTED_{data_type}]", sanitized)
        
        return sanitized
    
    def validate_endpoint(self, endpoint: str) -> Tuple[bool, str]:
        """
        Validate if an LLM endpoint is allowed
        
        Returns:
            (is_allowed, reason)
        """
        # Check if endpoint is explicitly allowed
        for allowed in self.allowed_endpoints:
            if allowed in endpoint.lower():
                return True, "Endpoint is in allowed list"
        
        # Check if endpoint is blocked
        for blocked in self.blocked_endpoints:
            if blocked in endpoint.lower():
                return False, f"Endpoint {blocked} is blocked for PHI/PII protection"
        
        # Unknown endpoint - block by default (zero-trust)
        return False, "Unknown endpoint - blocked by default (zero-trust policy)"
    
    def intercept_request(
        self,
        prompt: str,
        endpoint: str,
        user_id: str,
        metadata: Optional[Dict] = None
    ) -> Dict:
        """
        Intercept and validate a GenAI request
        
        Returns:
            Validation result with action to take
        """
        result = {
            "timestamp": datetime.utcnow().isoformat(),
            "user_id": user_id,
            "endpoint": endpoint,
            "prompt_hash": hashlib.sha256(prompt.encode()).hexdigest()[:16],
            "metadata": metadata or {},
            "risk_level": None,
            "detected_types": [],
            "action": None,
            "reason": None,
            "sanitized_prompt": None
        }
        
        # Step 1: Validate endpoint
        endpoint_allowed, endpoint_reason = self.validate_endpoint(endpoint)
        
        if not endpoint_allowed:
            result["risk_level"] = GenAIRiskLevel.CRITICAL.value
            result["action"] = GenAIAction.BLOCK.value
            result["reason"] = endpoint_reason
            
            self._log_violation(result)
            return result
        
        # Step 2: Scan prompt for sensitive data
        if self.enable_leak_filter:
            risk_level, detected_types, sanitized_prompt = self.scan_prompt(prompt)
            
            result["risk_level"] = risk_level.value
            result["detected_types"] = detected_types
            result["sanitized_prompt"] = sanitized_prompt
            
            # Determine action
            if risk_level == GenAIRiskLevel.CRITICAL:
                result["action"] = GenAIAction.BLOCK.value
                result["reason"] = f"PHI/PII detected in prompt: {', '.join(detected_types)}"
                self._log_violation(result)
            
            elif risk_level == GenAIRiskLevel.HIGH:
                result["action"] = GenAIAction.SANITIZE.value
                result["reason"] = f"Sensitive data detected: {', '.join(detected_types)}"
                self._log_violation(result)
            
            elif risk_level == GenAIRiskLevel.MEDIUM:
                result["action"] = GenAIAction.FLAG.value
                result["reason"] = "Suspicious patterns detected - flagged for review"
            
            else:
                result["action"] = GenAIAction.ALLOW.value
                result["reason"] = "No sensitive data detected"
        
        else:
            result["action"] = GenAIAction.ALLOW.value
            result["reason"] = "Leak filter disabled"
        
        # Step 3: Anomaly detection
        if self.enable_anomaly_detection:
            anomaly_detected = self._detect_anomaly(user_id, endpoint, prompt)
            
            if anomaly_detected:
                result["action"] = GenAIAction.FLAG.value
                result["reason"] += " | Anomalous usage pattern detected"
        
        # Log usage
        self._log_usage(result)
        
        return result
    
    def _detect_anomaly(self, user_id: str, endpoint: str, prompt: str) -> bool:
        """Detect anomalous GenAI usage patterns"""
        
        # Check for rapid-fire requests (potential data exfiltration)
        recent_requests = [
            log for log in self.usage_log[-100:]
            if log["user_id"] == user_id
            and (datetime.utcnow() - datetime.fromisoformat(log["timestamp"])).seconds < 60
        ]
        
        if len(recent_requests) > 10:
            logger.warning(f"⚠️ Anomaly: Rapid requests from {user_id}")
            return True
        
        # Check for unusually long prompts (potential data dump)
        if len(prompt) > 10000:
            logger.warning(f"⚠️ Anomaly: Unusually long prompt from {user_id}")
            return True
        
        return False
    
    def filter_response(self, response: str) -> Tuple[str, bool]:
        """
        Filter AI response for sensitive data leakage
        
        Returns:
            (filtered_response, contains_sensitive_data)
        """
        if not self.enable_response_filtering:
            return response, False
        
        # Scan response
        risk_level, detected_types, sanitized_response = self.scan_prompt(response)
        
        if risk_level in [GenAIRiskLevel.CRITICAL, GenAIRiskLevel.HIGH]:
            logger.warning(f"⚠️ Sensitive data in AI response: {detected_types}")
            return sanitized_response, True
        
        return response, False
    
    def _log_usage(self, result: Dict):
        """Log GenAI usage for monitoring"""
        self.usage_log.append(result)
        
        # Persist to disk
        log_file = "./security_telemetry/genai_usage.jsonl"
        with open(log_file, 'a') as f:
            f.write(json.dumps(result) + '\n')
    
    def _log_violation(self, result: Dict):
        """Log GenAI violations for incident response"""
        violation_file = "./security_telemetry/genai_violations.jsonl"
        with open(violation_file, 'a') as f:
            f.write(json.dumps(result) + '\n')
        
        logger.error(f"🚨 GenAI Violation: {result['reason']}")
    
    def get_usage_stats(self) -> Dict:
        """Get GenAI usage statistics"""
        total_requests = len(self.usage_log)
        
        if total_requests == 0:
            return {
                "total_requests": 0,
                "blocked": 0,
                "sanitized": 0,
                "flagged": 0,
                "allowed": 0
            }
        
        blocked = sum(1 for log in self.usage_log if log["action"] == "block")
        sanitized = sum(1 for log in self.usage_log if log["action"] == "sanitize")
        flagged = sum(1 for log in self.usage_log if log["action"] == "flag")
        allowed = sum(1 for log in self.usage_log if log["action"] == "allow")
        
        return {
            "total_requests": total_requests,
            "blocked": blocked,
            "sanitized": sanitized,
            "flagged": flagged,
            "allowed": allowed,
            "block_rate": blocked / total_requests * 100,
            "risk_score": (blocked * 10 + sanitized * 5 + flagged * 2) / total_requests
        }
    
    def export_metrics(self, output_path: str = "./security_telemetry/genai_risks.json"):
        """Export GenAI risk metrics"""
        stats = self.get_usage_stats()
        
        # Get recent violations
        recent_violations = [
            log for log in self.usage_log[-100:]
            if log["action"] in ["block", "sanitize"]
        ]
        
        # Aggregate risk types
        risk_types = {}
        for log in recent_violations:
            for data_type in log.get("detected_types", []):
                risk_types[data_type] = risk_types.get(data_type, 0) + 1
        
        metrics = {
            "last_check": datetime.utcnow().isoformat(),
            "total_genai_interactions": stats["total_requests"],
            "blocked_prompts": stats["blocked"],
            "flagged_responses": stats["flagged"],
            "data_leak_attempts": stats["blocked"] + stats["sanitized"],
            "risk_score": round(stats.get("risk_score", 0), 1),
            "top_risks": [
                {"type": k, "count": v, "severity": "high" if k in ["PHI", "PII"] else "medium"}
                for k, v in sorted(risk_types.items(), key=lambda x: x[1], reverse=True)[:5]
            ]
        }
        
        with open(output_path, 'w') as f:
            json.dump(metrics, f, indent=2)
        
        logger.info(f"📊 GenAI metrics exported to {output_path}")


# Example usage
if __name__ == "__main__":
    # Initialize GenAI guardrail
    guardrail = GenAIGuardrail(jurisdiction="KDPA_KE")
    
    # Test 1: Attempt to send PHI to external LLM
    result = guardrail.intercept_request(
        prompt="Patient John Doe has been diagnosed with malaria. Blood pressure: 120/80.",
        endpoint="https://api.openai.com/v1/chat/completions",
        user_id="dr_amina_hassan"
    )
    
    print(f"Test 1 - External LLM with PHI:")
    print(f"  Action: {result['action']}")
    print(f"  Reason: {result['reason']}")
    print(f"  Risk Level: {result['risk_level']}")
    print()
    
    # Test 2: Safe request to internal LLM
    result = guardrail.intercept_request(
        prompt="What are the symptoms of malaria?",
        endpoint="https://vertex-ai.googleapis.com/v1/projects/iluminara/models",
        user_id="dr_amina_hassan"
    )
    
    print(f"Test 2 - Internal LLM with safe prompt:")
    print(f"  Action: {result['action']}")
    print(f"  Reason: {result['reason']}")
    print()
    
    # Test 3: Sanitization
    result = guardrail.intercept_request(
        prompt="Analyze this patient data: fever, cough, positive test",
        endpoint="https://vertex-ai.googleapis.com/v1/projects/iluminara/models",
        user_id="dr_amina_hassan"
    )
    
    print(f"Test 3 - Sanitization:")
    print(f"  Action: {result['action']}")
    print(f"  Sanitized: {result.get('sanitized_prompt', 'N/A')}")
    print()
    
    # Export metrics
    guardrail.export_metrics()
    
    # Print stats
    stats = guardrail.get_usage_stats()
    print(f"📊 Usage Stats:")
    print(f"  Total Requests: {stats['total_requests']}")
    print(f"  Blocked: {stats['blocked']}")
    print(f"  Risk Score: {stats.get('risk_score', 0):.1f}/10")
