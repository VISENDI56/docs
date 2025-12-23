"""
Data Security Posture Management (DSPM) Engine
Implements 2026 Data Security Index recommendation: 79% prioritize automated classification

Key Functions:
- Identify data exposure risks (82% priority)
- Detect access patterns (81% priority)
- Automated classification (79% priority)

Compliance:
- GDPR Art. 30 (Records of Processing Activities)
- HIPAA §164.308(a)(1)(ii)(A) (Risk Analysis)
- ISO 27001 A.8.2.1 (Classification of Information)
- NIST SP 800-53 (AC-16 Security Attributes)
"""

import re
import os
import json
import hashlib
from datetime import datetime
from typing import Dict, List, Optional, Tuple
from enum import Enum
from pathlib import Path
import logging

logger = logging.getLogger(__name__)


class DataClassification(Enum):
    """Data classification levels"""
    PUBLIC = "PUBLIC"
    INTERNAL = "INTERNAL"
    CONFIDENTIAL = "CONFIDENTIAL"
    PHI = "PHI"  # Protected Health Information
    PII = "PII"  # Personally Identifiable Information
    RESTRICTED = "RESTRICTED"


class ExposureRisk(Enum):
    """Data exposure risk levels"""
    CRITICAL = "CRITICAL"  # Public exposure of PHI/PII
    HIGH = "HIGH"  # Misconfigured access controls
    MEDIUM = "MEDIUM"  # Overly permissive sharing
    LOW = "LOW"  # Proper controls in place
    NONE = "NONE"  # No risk detected


class DSPMEngine:
    """
    Data Security Posture Management Engine
    
    Discovers, classifies, and monitors sensitive data across the iLuminara stack
    """
    
    def __init__(self, scan_paths: Optional[List[str]] = None):
        self.scan_paths = scan_paths or ["./edge_node", "./governance_kernel", "./api_service.py"]
        self.classification_results = []
        self.exposure_risks = []
        self.access_patterns = []
        
        # Regex patterns for sensitive data detection
        self.patterns = {
            "PHI": [
                # Patient identifiers
                r'\b(?:patient[_\s]?id|medical[_\s]?record[_\s]?number|mrn)\s*[:=]\s*["\']?([A-Z0-9\-]+)["\']?',
                # Diagnosis codes
                r'\b(?:icd[_\s]?10|diagnosis[_\s]?code)\s*[:=]\s*["\']?([A-Z0-9\.]+)["\']?',
                # Medical conditions
                r'\b(?:diagnosis|condition|disease)\s*[:=]\s*["\']?(cholera|malaria|tuberculosis|hiv|aids|covid)["\']?',
                # Vital signs
                r'\b(?:blood[_\s]?pressure|heart[_\s]?rate|temperature|oxygen[_\s]?saturation)\s*[:=]\s*["\']?(\d+)["\']?',
            ],
            "PII": [
                # Names
                r'\b(?:first[_\s]?name|last[_\s]?name|full[_\s]?name)\s*[:=]\s*["\']?([A-Za-z\s]+)["\']?',
                # Email addresses
                r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b',
                # Phone numbers
                r'\b(?:\+?254|0)?[17]\d{8}\b',  # Kenyan phone numbers
                # National IDs
                r'\b(?:national[_\s]?id|id[_\s]?number)\s*[:=]\s*["\']?(\d{7,8})["\']?',
                # GPS coordinates (can identify individuals)
                r'\b(?:lat|latitude)\s*[:=]\s*["\']?([-+]?\d+\.\d+)["\']?',
            ],
            "CREDENTIALS": [
                # API keys
                r'(?:api[_\s]?key|apikey)\s*[:=]\s*["\']?([A-Za-z0-9\-_]{20,})["\']?',
                # Passwords
                r'(?:password|passwd|pwd)\s*[:=]\s*["\']?([^\s"\']+)["\']?',
                # Tokens
                r'(?:token|auth[_\s]?token)\s*[:=]\s*["\']?([A-Za-z0-9\-_\.]+)["\']?',
                # AWS keys (sovereignty violation)
                r'AKIA[0-9A-Z]{16}',
            ]
        }
    
    def scan_file(self, file_path: Path) -> Dict:
        """
        Scan a single file for sensitive data
        
        Returns:
            Classification results with detected patterns
        """
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
        except Exception as e:
            logger.error(f"Failed to read {file_path}: {e}")
            return {}
        
        findings = {
            "file": str(file_path),
            "scan_date": datetime.utcnow().isoformat(),
            "classifications": [],
            "exposure_risk": ExposureRisk.NONE.value,
            "line_numbers": []
        }
        
        # Scan for each classification type
        for classification, patterns in self.patterns.items():
            for pattern in patterns:
                matches = re.finditer(pattern, content, re.IGNORECASE)
                
                for match in matches:
                    # Calculate line number
                    line_num = content[:match.start()].count('\n') + 1
                    
                    # Redact matched value
                    matched_value = match.group(0)
                    redacted_value = self._redact_value(matched_value)
                    
                    findings["classifications"].append({
                        "type": classification,
                        "pattern": pattern[:50] + "...",
                        "line": line_num,
                        "redacted_value": redacted_value,
                        "context": self._get_context(content, match.start(), match.end())
                    })
                    
                    findings["line_numbers"].append(line_num)
        
        # Determine exposure risk
        if findings["classifications"]:
            findings["exposure_risk"] = self._calculate_exposure_risk(file_path, findings["classifications"])
        
        return findings
    
    def scan_directory(self, directory: Path) -> List[Dict]:
        """
        Recursively scan directory for sensitive data
        
        Returns:
            List of classification results
        """
        results = []
        
        # File extensions to scan
        extensions = ['.py', '.js', '.json', '.yaml', '.yml', '.txt', '.md', '.env']
        
        for file_path in directory.rglob('*'):
            if file_path.is_file() and file_path.suffix in extensions:
                # Skip test files and virtual environments
                if any(skip in str(file_path) for skip in ['test', 'venv', 'node_modules', '__pycache__']):
                    continue
                
                findings = self.scan_file(file_path)
                
                if findings and findings.get("classifications"):
                    results.append(findings)
        
        return results
    
    def run_full_scan(self) -> Dict:
        """
        Run full DSPM scan across all configured paths
        
        Returns:
            Comprehensive scan results
        """
        logger.info("🔍 Starting DSPM full scan...")
        
        all_results = []
        
        for scan_path in self.scan_paths:
            path = Path(scan_path)
            
            if path.is_file():
                findings = self.scan_file(path)
                if findings and findings.get("classifications"):
                    all_results.append(findings)
            
            elif path.is_dir():
                results = self.scan_directory(path)
                all_results.extend(results)
        
        # Aggregate statistics
        summary = self._generate_summary(all_results)
        
        # Save results
        self._save_results(all_results, summary)
        
        logger.info(f"✅ DSPM scan complete - {summary['total_files']} files, {summary['total_findings']} findings")
        
        return {
            "scan_date": datetime.utcnow().isoformat(),
            "summary": summary,
            "results": all_results
        }
    
    def detect_access_patterns(self, audit_log_path: str = "./keys/audit.jsonl") -> List[Dict]:
        """
        Detect anomalous access patterns (81% priority in 2026 DSI)
        
        Returns:
            List of detected anomalies
        """
        anomalies = []
        
        if not os.path.exists(audit_log_path):
            return anomalies
        
        access_counts = {}
        
        with open(audit_log_path, 'r') as f:
            for line in f:
                try:
                    entry = json.loads(line)
                    
                    # Track access by actor
                    actor = entry.get("metadata", {}).get("actor", "unknown")
                    action = entry.get("action", "unknown")
                    
                    key = f"{actor}:{action}"
                    access_counts[key] = access_counts.get(key, 0) + 1
                    
                except json.JSONDecodeError:
                    continue
        
        # Detect anomalies (simple threshold-based)
        for key, count in access_counts.items():
            if count > 100:  # More than 100 accesses
                actor, action = key.split(":", 1)
                anomalies.append({
                    "actor": actor,
                    "action": action,
                    "count": count,
                    "severity": "HIGH" if count > 500 else "MEDIUM",
                    "description": f"Unusual access pattern: {count} {action} operations by {actor}"
                })
        
        return anomalies
    
    def identify_exposure_risks(self) -> List[Dict]:
        """
        Identify data exposure risks (82% priority in 2026 DSI)
        
        Returns:
            List of exposure risks
        """
        risks = []
        
        # Check for common misconfigurations
        risk_checks = [
            {
                "check": "public_s3_buckets",
                "description": "S3 buckets with public access",
                "severity": ExposureRisk.CRITICAL,
                "remediation": "Enable S3 Block Public Access"
            },
            {
                "check": "overly_permissive_iam",
                "description": "IAM roles with wildcard permissions",
                "severity": ExposureRisk.HIGH,
                "remediation": "Apply principle of least privilege"
            },
            {
                "check": "unencrypted_data_at_rest",
                "description": "Data stored without encryption",
                "severity": ExposureRisk.HIGH,
                "remediation": "Enable encryption at rest"
            },
            {
                "check": "missing_mfa",
                "description": "Admin accounts without MFA",
                "severity": ExposureRisk.MEDIUM,
                "remediation": "Enforce MFA for all admin accounts"
            }
        ]
        
        # In production, these would be actual checks against cloud infrastructure
        # For now, return template
        for check in risk_checks:
            risks.append({
                "check_id": check["check"],
                "description": check["description"],
                "severity": check["severity"].value,
                "remediation": check["remediation"],
                "detected": False  # Would be True if misconfiguration found
            })
        
        return risks
    
    def _redact_value(self, value: str) -> str:
        """Redact sensitive value for logging"""
        if len(value) <= 4:
            return "***"
        return value[:2] + "*" * (len(value) - 4) + value[-2:]
    
    def _get_context(self, content: str, start: int, end: int, context_chars: int = 50) -> str:
        """Get surrounding context for a match"""
        context_start = max(0, start - context_chars)
        context_end = min(len(content), end + context_chars)
        
        context = content[context_start:context_end]
        
        # Redact the actual match
        match_start = start - context_start
        match_end = end - context_start
        context = context[:match_start] + "***REDACTED***" + context[match_end:]
        
        return context.replace('\n', ' ').strip()
    
    def _calculate_exposure_risk(self, file_path: Path, classifications: List[Dict]) -> str:
        """Calculate exposure risk based on file location and classification"""
        
        # Check if file is in public directory
        if any(public_dir in str(file_path) for public_dir in ['public', 'static', 'assets']):
            return ExposureRisk.CRITICAL.value
        
        # Check for PHI/PII in API endpoints
        if 'api' in str(file_path).lower():
            if any(c['type'] in ['PHI', 'PII'] for c in classifications):
                return ExposureRisk.HIGH.value
        
        # Check for credentials
        if any(c['type'] == 'CREDENTIALS' for c in classifications):
            return ExposureRisk.HIGH.value
        
        # Default to medium for any sensitive data
        if classifications:
            return ExposureRisk.MEDIUM.value
        
        return ExposureRisk.NONE.value
    
    def _generate_summary(self, results: List[Dict]) -> Dict:
        """Generate summary statistics"""
        summary = {
            "total_files": len(results),
            "total_findings": sum(len(r.get("classifications", [])) for r in results),
            "by_classification": {},
            "by_risk": {},
            "critical_files": []
        }
        
        for result in results:
            # Count by classification
            for classification in result.get("classifications", []):
                class_type = classification["type"]
                summary["by_classification"][class_type] = summary["by_classification"].get(class_type, 0) + 1
            
            # Count by risk
            risk = result.get("exposure_risk", ExposureRisk.NONE.value)
            summary["by_risk"][risk] = summary["by_risk"].get(risk, 0) + 1
            
            # Track critical files
            if risk in [ExposureRisk.CRITICAL.value, ExposureRisk.HIGH.value]:
                summary["critical_files"].append(result["file"])
        
        return summary
    
    def _save_results(self, results: List[Dict], summary: Dict):
        """Save scan results to disk"""
        output_dir = Path("./security_telemetry")
        output_dir.mkdir(exist_ok=True)
        
        output_file = output_dir / f"dspm_scan_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}.json"
        
        with open(output_file, 'w') as f:
            json.dump({
                "scan_date": datetime.utcnow().isoformat(),
                "summary": summary,
                "results": results
            }, f, indent=2)
        
        logger.info(f"📊 Results saved to {output_file}")


# Example usage
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    
    # Initialize DSPM engine
    dspm = DSPMEngine(scan_paths=["./edge_node", "./governance_kernel"])
    
    # Run full scan
    scan_results = dspm.run_full_scan()
    
    print(f"\n📊 DSPM Scan Summary:")
    print(f"   Files scanned: {scan_results['summary']['total_files']}")
    print(f"   Findings: {scan_results['summary']['total_findings']}")
    print(f"\n   By Classification:")
    for class_type, count in scan_results['summary']['by_classification'].items():
        print(f"      {class_type}: {count}")
    print(f"\n   By Risk:")
    for risk, count in scan_results['summary']['by_risk'].items():
        print(f"      {risk}: {count}")
    
    # Detect access patterns
    anomalies = dspm.detect_access_patterns()
    print(f"\n🔍 Access Pattern Anomalies: {len(anomalies)}")
    
    # Identify exposure risks
    risks = dspm.identify_exposure_risks()
    print(f"\n⚠️  Exposure Risks: {len([r for r in risks if r['detected']])}")
