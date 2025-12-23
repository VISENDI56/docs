"""
Data Security Posture Management (DSPM) Engine
Aligns with 2026 Data Security Index: 82% prioritize DSPM

Key Functions:
- Identify data exposure risks (82% priority)
- Detect access patterns (81% priority)
- Automated classification (79% priority)

Compliance:
- GDPR Art. 30 (Records of Processing)
- HIPAA §164.308(a)(1)(ii)(A) (Risk Analysis)
- ISO 27001 A.8.1 (Inventory of Assets)
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
    PHI = "Protected Health Information"  # HIPAA
    PII = "Personally Identifiable Information"  # GDPR
    FINANCIAL = "Financial Data"
    OPERATIONAL = "Operational Data"
    PUBLIC = "Public Data"
    UNKNOWN = "Unclassified"


class RiskLevel(Enum):
    """Risk severity levels"""
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"
    NONE = "none"


class DSPMEngine:
    """
    Automated Data Security Posture Management Engine
    
    Discovers, classifies, and monitors sensitive data across environments.
    """
    
    def __init__(
        self,
        scan_paths: List[str] = None,
        enable_ml_classification: bool = False,
        jurisdiction: str = "KDPA_KE"
    ):
        self.scan_paths = scan_paths or ["./"]
        self.enable_ml_classification = enable_ml_classification
        self.jurisdiction = jurisdiction
        
        # Classification patterns (regex-based)
        self.patterns = self._initialize_patterns()
        
        # Scan results
        self.scan_results = {
            "scan_date": None,
            "total_files_scanned": 0,
            "total_data_assets": 0,
            "classified_assets": 0,
            "unclassified_assets": 0,
            "classification_coverage": 0.0,
            "exposure_risks": {
                "critical": 0,
                "high": 0,
                "medium": 0,
                "low": 0
            },
            "data_types": {
                "PHI": 0,
                "PII": 0,
                "Financial": 0,
                "Operational": 0,
                "Public": 0,
                "Unknown": 0
            },
            "access_anomalies": [],
            "misconfigurations": [],
            "findings": []
        }
        
        logger.info(f"🔍 DSPM Engine initialized - Jurisdiction: {jurisdiction}")
    
    def _initialize_patterns(self) -> Dict[DataClassification, List[re.Pattern]]:
        """Initialize regex patterns for data classification"""
        return {
            DataClassification.PHI: [
                re.compile(r'\b(patient|diagnosis|treatment|medication|prescription|medical_record)\b', re.IGNORECASE),
                re.compile(r'\b(symptom|disease|condition|vital_signs|lab_result)\b', re.IGNORECASE),
                re.compile(r'\b(ICD-\d{2}|CPT-\d{5})\b'),  # Medical codes
                re.compile(r'\b(blood_pressure|heart_rate|temperature|oxygen_saturation)\b', re.IGNORECASE),
            ],
            DataClassification.PII: [
                re.compile(r'\b[A-Z][a-z]+ [A-Z][a-z]+\b'),  # Names
                re.compile(r'\b\d{3}-\d{2}-\d{4}\b'),  # SSN
                re.compile(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'),  # Email
                re.compile(r'\b\d{10,15}\b'),  # Phone numbers
                re.compile(r'\b\d{1,5}\s\w+\s(Street|St|Avenue|Ave|Road|Rd|Boulevard|Blvd)\b', re.IGNORECASE),  # Address
                re.compile(r'\b(passport|driver_license|national_id)\b', re.IGNORECASE),
            ],
            DataClassification.FINANCIAL: [
                re.compile(r'\b\d{4}[-\s]?\d{4}[-\s]?\d{4}[-\s]?\d{4}\b'),  # Credit card
                re.compile(r'\b(account_number|routing_number|iban|swift)\b', re.IGNORECASE),
                re.compile(r'\b(payment|transaction|invoice|billing)\b', re.IGNORECASE),
            ],
            DataClassification.OPERATIONAL: [
                re.compile(r'\b(api_key|access_token|secret|password|credential)\b', re.IGNORECASE),
                re.compile(r'\b(config|configuration|settings|environment)\b', re.IGNORECASE),
            ]
        }
    
    def classify_text(self, text: str) -> Tuple[DataClassification, float]:
        """
        Classify text using regex patterns
        
        Returns:
            (classification, confidence_score)
        """
        scores = {classification: 0 for classification in DataClassification}
        
        for classification, patterns in self.patterns.items():
            for pattern in patterns:
                matches = pattern.findall(text)
                scores[classification] += len(matches)
        
        # Determine classification
        max_score = max(scores.values())
        
        if max_score == 0:
            return DataClassification.UNKNOWN, 0.0
        
        classification = max(scores, key=scores.get)
        confidence = min(max_score / 10.0, 1.0)  # Normalize to 0-1
        
        return classification, confidence
    
    def classify_file(self, file_path: Path) -> Dict:
        """
        Classify a single file
        
        Returns:
            Classification result with metadata
        """
        try:
            # Skip binary files
            if file_path.suffix in ['.pyc', '.so', '.dll', '.exe', '.bin']:
                return None
            
            # Read file content
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
            
            # Classify
            classification, confidence = self.classify_text(content)
            
            # Calculate file hash
            file_hash = hashlib.sha256(content.encode()).hexdigest()[:16]
            
            # Assess risk
            risk_level = self._assess_risk(file_path, classification, confidence)
            
            return {
                "file_path": str(file_path),
                "file_name": file_path.name,
                "file_size": file_path.stat().st_size,
                "classification": classification.name,
                "confidence": confidence,
                "risk_level": risk_level.value,
                "file_hash": file_hash,
                "last_modified": datetime.fromtimestamp(file_path.stat().st_mtime).isoformat(),
                "scan_timestamp": datetime.utcnow().isoformat()
            }
        
        except Exception as e:
            logger.error(f"Error classifying {file_path}: {e}")
            return None
    
    def _assess_risk(
        self,
        file_path: Path,
        classification: DataClassification,
        confidence: float
    ) -> RiskLevel:
        """Assess exposure risk based on file location and classification"""
        
        # Critical: PHI/PII in public directories
        if classification in [DataClassification.PHI, DataClassification.PII]:
            if any(x in str(file_path).lower() for x in ['public', 'static', 'www', 'html']):
                return RiskLevel.CRITICAL
            
            # High: PHI/PII without encryption
            if not any(x in str(file_path).lower() for x in ['encrypted', 'secure', 'vault']):
                return RiskLevel.HIGH
        
        # High: Financial data in logs
        if classification == DataClassification.FINANCIAL:
            if 'log' in str(file_path).lower():
                return RiskLevel.HIGH
        
        # Medium: Operational data in version control
        if classification == DataClassification.OPERATIONAL:
            if '.git' in str(file_path):
                return RiskLevel.MEDIUM
        
        # Low: Everything else with classification
        if classification != DataClassification.UNKNOWN:
            return RiskLevel.LOW
        
        return RiskLevel.NONE
    
    def scan_directory(self, directory: Path) -> List[Dict]:
        """Scan a directory recursively"""
        findings = []
        
        for file_path in directory.rglob('*'):
            if file_path.is_file():
                result = self.classify_file(file_path)
                if result:
                    findings.append(result)
                    self.scan_results["total_files_scanned"] += 1
        
        return findings
    
    def run_full_scan(self) -> Dict:
        """
        Run complete DSPM scan across all configured paths
        
        Returns:
            Comprehensive scan results
        """
        logger.info("🔍 Starting DSPM full scan...")
        
        self.scan_results["scan_date"] = datetime.utcnow().isoformat()
        all_findings = []
        
        for scan_path in self.scan_paths:
            path = Path(scan_path)
            if path.exists():
                logger.info(f"Scanning: {scan_path}")
                findings = self.scan_directory(path)
                all_findings.extend(findings)
        
        # Aggregate results
        self.scan_results["total_data_assets"] = len(all_findings)
        self.scan_results["findings"] = all_findings
        
        # Count classifications
        for finding in all_findings:
            classification = finding["classification"]
            risk_level = finding["risk_level"]
            
            # Update data type counts
            if classification in self.scan_results["data_types"]:
                self.scan_results["data_types"][classification] += 1
            
            # Update risk counts
            if risk_level in self.scan_results["exposure_risks"]:
                self.scan_results["exposure_risks"][risk_level] += 1
            
            # Count classified vs unclassified
            if classification != "UNKNOWN":
                self.scan_results["classified_assets"] += 1
            else:
                self.scan_results["unclassified_assets"] += 1
        
        # Calculate coverage
        if self.scan_results["total_data_assets"] > 0:
            self.scan_results["classification_coverage"] = (
                self.scan_results["classified_assets"] / 
                self.scan_results["total_data_assets"] * 100
            )
        
        # Detect misconfigurations
        self._detect_misconfigurations(all_findings)
        
        # Detect access anomalies
        self._detect_access_anomalies(all_findings)
        
        logger.info(f"✅ DSPM scan complete - {len(all_findings)} assets analyzed")
        
        return self.scan_results
    
    def _detect_misconfigurations(self, findings: List[Dict]):
        """Detect security misconfigurations"""
        misconfigurations = []
        
        for finding in findings:
            # PHI/PII in public directories
            if finding["classification"] in ["PHI", "PII"]:
                if any(x in finding["file_path"].lower() for x in ['public', 'static', 'www']):
                    misconfigurations.append({
                        "type": "sensitive_data_in_public_directory",
                        "severity": "critical",
                        "file": finding["file_path"],
                        "classification": finding["classification"],
                        "recommendation": "Move to secure storage with access controls"
                    })
            
            # Credentials in code
            if finding["classification"] == "OPERATIONAL":
                if any(x in finding["file_name"].lower() for x in ['.py', '.js', '.java']):
                    misconfigurations.append({
                        "type": "credentials_in_source_code",
                        "severity": "high",
                        "file": finding["file_path"],
                        "recommendation": "Use environment variables or secret management"
                    })
        
        self.scan_results["misconfigurations"] = misconfigurations
    
    def _detect_access_anomalies(self, findings: List[Dict]):
        """Detect unusual access patterns"""
        anomalies = []
        
        # Group by classification
        phi_files = [f for f in findings if f["classification"] == "PHI"]
        
        # Anomaly: Too many PHI files in one location
        if len(phi_files) > 100:
            anomalies.append({
                "type": "excessive_phi_concentration",
                "severity": "medium",
                "count": len(phi_files),
                "recommendation": "Distribute PHI across secure storage zones"
            })
        
        self.scan_results["access_anomalies"] = anomalies
    
    def export_results(self, output_path: str = "./security_telemetry/dspm_metrics.json"):
        """Export scan results to JSON"""
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
        with open(output_path, 'w') as f:
            json.dump(self.scan_results, f, indent=2)
        
        logger.info(f"📊 DSPM results exported to {output_path}")
    
    def generate_report(self) -> str:
        """Generate human-readable DSPM report"""
        report = []
        report.append("=" * 60)
        report.append("iLuminara DSPM Scan Report")
        report.append("=" * 60)
        report.append(f"Scan Date: {self.scan_results['scan_date']}")
        report.append(f"Jurisdiction: {self.jurisdiction}")
        report.append("")
        
        report.append("SUMMARY")
        report.append("-" * 60)
        report.append(f"Total Files Scanned: {self.scan_results['total_files_scanned']}")
        report.append(f"Total Data Assets: {self.scan_results['total_data_assets']}")
        report.append(f"Classified Assets: {self.scan_results['classified_assets']}")
        report.append(f"Classification Coverage: {self.scan_results['classification_coverage']:.1f}%")
        report.append("")
        
        report.append("DATA CLASSIFICATION")
        report.append("-" * 60)
        for data_type, count in self.scan_results['data_types'].items():
            report.append(f"{data_type}: {count}")
        report.append("")
        
        report.append("EXPOSURE RISKS")
        report.append("-" * 60)
        for risk_level, count in self.scan_results['exposure_risks'].items():
            report.append(f"{risk_level.upper()}: {count}")
        report.append("")
        
        report.append("MISCONFIGURATIONS")
        report.append("-" * 60)
        if self.scan_results['misconfigurations']:
            for misc in self.scan_results['misconfigurations']:
                report.append(f"[{misc['severity'].upper()}] {misc['type']}")
                report.append(f"  File: {misc['file']}")
                report.append(f"  Recommendation: {misc['recommendation']}")
                report.append("")
        else:
            report.append("No misconfigurations detected")
        
        report.append("=" * 60)
        
        return "\n".join(report)


# Example usage
if __name__ == "__main__":
    # Initialize DSPM engine
    dspm = DSPMEngine(
        scan_paths=["./edge_node", "./governance_kernel", "./api_service.py"],
        jurisdiction="KDPA_KE"
    )
    
    # Run full scan
    results = dspm.run_full_scan()
    
    # Export results
    dspm.export_results()
    
    # Generate report
    print(dspm.generate_report())
    
    # Print summary
    print(f"\n✅ DSPM Scan Complete")
    print(f"📊 Classification Coverage: {results['classification_coverage']:.1f}%")
    print(f"🔴 Critical Risks: {results['exposure_risks']['critical']}")
    print(f"🟡 High Risks: {results['exposure_risks']['high']}")
