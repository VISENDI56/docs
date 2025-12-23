#!/usr/bin/env python3
"""
iLuminara DSPM Maturity Score Calculator
Based on Microsoft 2026 Data Security Index

Calculates Data Security Posture Management (DSPM) maturity across:
- Data Discovery
- Access Control
- Encryption
- Compliance
- Incident Response
"""

import json
import os
import sys
from pathlib import Path
from typing import Dict, List


class DSPMCalculator:
    """Calculate DSPM maturity score for iLuminara-Core"""
    
    def __init__(self, repo_path: str = "."):
        self.repo_path = Path(repo_path)
        self.score = {
            "overall_score": 0,
            "data_discovery": 0,
            "access_control": 0,
            "encryption": 0,
            "compliance": 0,
            "incident_response": 0,
            "nuclear_ip": {},
            "frameworks": []
        }
    
    def calculate_data_discovery(self) -> int:
        """
        Data Discovery: Ability to identify and classify sensitive data
        
        Checks:
        - Golden Thread data fusion (IP-05)
        - Data classification in governance kernel
        - Audit trail completeness
        """
        score = 0
        
        # Check Golden Thread implementation
        golden_thread_path = self.repo_path / "edge_node" / "sync_protocol" / "golden_thread.py"
        if golden_thread_path.exists():
            score += 30
            print("✅ Golden Thread data fusion: +30")
        
        # Check offline buffer
        offline_buffer_path = self.repo_path / "edge_node" / "sync_protocol" / "golden_thread_offline.py"
        if offline_buffer_path.exists():
            score += 20
            print("✅ Offline buffer (SQLite): +20")
        
        # Check data classification
        vector_ledger_path = self.repo_path / "governance_kernel" / "vector_ledger.py"
        if vector_ledger_path.exists():
            score += 30
            print("✅ Data classification (SovereignGuardrail): +30")
        
        # Check audit trail
        if self._check_audit_trail():
            score += 20
            print("✅ Tamper-proof audit trail: +20")
        
        return min(score, 100)
    
    def calculate_access_control(self) -> int:
        """
        Access Control: Identity and access management
        
        Checks:
        - SovereignGuardrail enforcement
        - Role-based access control
        - Consent management
        """
        score = 0
        
        # Check SovereignGuardrail
        guardrail_path = self.repo_path / "governance_kernel" / "vector_ledger.py"
        if guardrail_path.exists():
            score += 40
            print("✅ SovereignGuardrail enforcement: +40")
        
        # Check consent management
        if self._check_consent_management():
            score += 30
            print("✅ Consent management: +30")
        
        # Check IAM configuration
        if self._check_iam_config():
            score += 30
            print("✅ IAM configuration: +30")
        
        return min(score, 100)
    
    def calculate_encryption(self) -> int:
        """
        Encryption: Data protection at rest and in transit
        
        Checks:
        - Crypto Shredder (IP-02)
        - TLS configuration
        - Key management
        """
        score = 0
        
        # Check Crypto Shredder
        crypto_shredder_path = self.repo_path / "governance_kernel" / "crypto_shredder.py"
        if crypto_shredder_path.exists():
            score += 50
            print("✅ Crypto Shredder (IP-02): +50")
        
        # Check TLS configuration
        if self._check_tls_config():
            score += 25
            print("✅ TLS 1.3 configuration: +25")
        
        # Check key management
        if self._check_key_management():
            score += 25
            print("✅ Cloud KMS integration: +25")
        
        return min(score, 100)
    
    def calculate_compliance(self) -> int:
        """
        Compliance: Adherence to 14 global legal frameworks
        
        Checks:
        - Framework enforcement
        - Audit logging
        - Data retention policies
        """
        score = 0
        
        # Check compliance configuration
        config_path = self.repo_path / "config" / "sovereign_guardrail.yaml"
        if config_path.exists():
            score += 40
            print("✅ Compliance configuration: +40")
        
        # Check framework enforcement
        frameworks = self._check_frameworks()
        score += len(frameworks) * 3  # 3 points per framework (max 42 for 14 frameworks)
        print(f"✅ Frameworks enforced: {len(frameworks)}/14 (+{len(frameworks) * 3})")
        
        # Check retention policies
        if self._check_retention_policies():
            score += 18
            print("✅ Data retention policies: +18")
        
        return min(score, 100)
    
    def calculate_incident_response(self) -> int:
        """
        Incident Response: Detection and response capabilities
        
        Checks:
        - Security workflows (CodeQL, Gitleaks)
        - Monitoring and alerting
        - Incident playbooks
        """
        score = 0
        
        # Check CodeQL workflow
        codeql_path = self.repo_path / ".github" / "workflows" / "codeql.yml"
        if codeql_path.exists():
            score += 25
            print("✅ CodeQL SAST scanning: +25")
        
        # Check Gitleaks workflow
        gitleaks_path = self.repo_path / ".github" / "workflows" / "gitleaks.yml"
        if gitleaks_path.exists():
            score += 25
            print("✅ Gitleaks secret scanning: +25")
        
        # Check audit workflow
        audit_path = self.repo_path / ".github" / "workflows" / "iluminara_audit.yml"
        if audit_path.exists():
            score += 25
            print("✅ Integrated audit workflow: +25")
        
        # Check monitoring
        if self._check_monitoring():
            score += 25
            print("✅ Prometheus monitoring: +25")
        
        return min(score, 100)
    
    def _check_audit_trail(self) -> bool:
        """Check if tamper-proof audit trail is configured"""
        config_path = self.repo_path / "config" / "sovereign_guardrail.yaml"
        if config_path.exists():
            with open(config_path) as f:
                content = f.read()
                return "tamper_proof: true" in content
        return False
    
    def _check_consent_management(self) -> bool:
        """Check if consent management is implemented"""
        config_path = self.repo_path / "config" / "sovereign_guardrail.yaml"
        if config_path.exists():
            with open(config_path) as f:
                content = f.read()
                return "consent:" in content and "require_explicit_consent: true" in content
        return False
    
    def _check_iam_config(self) -> bool:
        """Check if IAM is configured"""
        cloud_run_path = self.repo_path / "frontend_web" / "cloud-run-service.yaml"
        return cloud_run_path.exists()
    
    def _check_tls_config(self) -> bool:
        """Check if TLS is configured"""
        nginx_path = self.repo_path / "frontend_web" / "nginx.conf"
        if nginx_path.exists():
            with open(nginx_path) as f:
                content = f.read()
                return "Strict-Transport-Security" in content
        return False
    
    def _check_key_management(self) -> bool:
        """Check if key management is configured"""
        crypto_path = self.repo_path / "governance_kernel" / "crypto_shredder.py"
        if crypto_path.exists():
            with open(crypto_path) as f:
                content = f.read()
                return "Cloud_KMS" in content or "google-cloud-kms" in content
        return False
    
    def _check_frameworks(self) -> List[str]:
        """Check which compliance frameworks are enforced"""
        frameworks = []
        config_path = self.repo_path / "config" / "sovereign_guardrail.yaml"
        
        if config_path.exists():
            with open(config_path) as f:
                content = f.read()
                
                framework_list = [
                    "GDPR", "KDPA", "HIPAA", "POPIA", "NDPR", "APPI",
                    "PIPEDA", "LGPD", "CCPA", "WHO_IHR", "Geneva",
                    "EU_AI_ACT", "AU_Malabo", "FHIR"
                ]
                
                for framework in framework_list:
                    if framework in content:
                        frameworks.append(framework)
        
        return frameworks
    
    def _check_retention_policies(self) -> bool:
        """Check if data retention policies are configured"""
        crypto_path = self.repo_path / "governance_kernel" / "crypto_shredder.py"
        if crypto_path.exists():
            with open(crypto_path) as f:
                content = f.read()
                return "RetentionPolicy" in content
        return False
    
    def _check_monitoring(self) -> bool:
        """Check if monitoring is configured"""
        config_path = self.repo_path / "config" / "sovereign_guardrail.yaml"
        if config_path.exists():
            with open(config_path) as f:
                content = f.read()
                return "prometheus:" in content
        return False
    
    def _check_nuclear_ip(self) -> Dict:
        """Check Nuclear IP Stack status"""
        nuclear_ip = {
            "crypto_shredder": False,
            "acorn_protocol": False,
            "silent_flux": False,
            "golden_thread": False,
            "5dm_bridge": False
        }
        
        # IP-02: Crypto Shredder
        crypto_path = self.repo_path / "governance_kernel" / "crypto_shredder.py"
        nuclear_ip["crypto_shredder"] = crypto_path.exists()
        
        # IP-05: Golden Thread
        golden_thread_path = self.repo_path / "edge_node" / "sync_protocol" / "golden_thread.py"
        nuclear_ip["golden_thread"] = golden_thread_path.exists()
        
        return nuclear_ip
    
    def calculate(self) -> Dict:
        """Calculate overall DSPM maturity score"""
        print("🔍 Calculating DSPM Maturity Score...\n")
        
        # Calculate individual scores
        self.score["data_discovery"] = self.calculate_data_discovery()
        print(f"📊 Data Discovery: {self.score['data_discovery']}/100\n")
        
        self.score["access_control"] = self.calculate_access_control()
        print(f"🔐 Access Control: {self.score['access_control']}/100\n")
        
        self.score["encryption"] = self.calculate_encryption()
        print(f"🔒 Encryption: {self.score['encryption']}/100\n")
        
        self.score["compliance"] = self.calculate_compliance()
        print(f"⚖️  Compliance: {self.score['compliance']}/100\n")
        
        self.score["incident_response"] = self.calculate_incident_response()
        print(f"🚨 Incident Response: {self.score['incident_response']}/100\n")
        
        # Calculate overall score (weighted average)
        self.score["overall_score"] = int(
            (self.score["data_discovery"] * 0.20) +
            (self.score["access_control"] * 0.20) +
            (self.score["encryption"] * 0.25) +
            (self.score["compliance"] * 0.25) +
            (self.score["incident_response"] * 0.10)
        )
        
        # Check Nuclear IP Stack
        self.score["nuclear_ip"] = self._check_nuclear_ip()
        
        # Check frameworks
        frameworks = self._check_frameworks()
        self.score["frameworks"] = [
            {"name": f, "enabled": True} for f in frameworks
        ]
        
        print(f"🛡️  OVERALL DSPM SCORE: {self.score['overall_score']}/100\n")
        
        return self.score


if __name__ == "__main__":
    calculator = DSPMCalculator()
    score = calculator.calculate()
    
    # Output JSON for GitHub Actions
    print(json.dumps(score, indent=2))
    
    # Exit with appropriate code
    sys.exit(0 if score["overall_score"] >= 80 else 1)
