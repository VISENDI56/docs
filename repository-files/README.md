# iLuminara-Core Security Stack Implementation Files

This directory contains the complete implementation of the **Sovereign Health Fortress** security architecture and **Nuclear IP Stack** for iLuminara-Core.

## 🛡️ The Fortress

```
┌──────────────────────────────────────────────────────────────┐
│                 SOVEREIGN HEALTH FORTRESS                     │
│                                                               │
│  ┌─────────────────────────────────────────────────────┐    │
│  │  Security Audit Layer                               │    │
│  │  • CodeQL SAST Scanning                             │    │
│  │  • Gitleaks Secret Detection                        │    │
│  │  • Dependabot Daily Updates                         │    │
│  └─────────────────────────────────────────────────────┘    │
│                          ▼                                    │
│  ┌─────────────────────────────────────────────────────┐    │
│  │  Governance Kernel (Nuclear IP Stack)               │    │
│  │  • IP-02: Crypto Shredder                           │    │
│  │  • IP-03: Acorn Protocol                            │    │
│  │  • SovereignGuardrail (14 frameworks)               │    │
│  └─────────────────────────────────────────────────────┘    │
│                          ▼                                    │
│  ┌─────────────────────────────────────────────────────┐    │
│  │  Hardware Attestation                                │    │
│  │  • TPM-based Trust                                   │    │
│  │  • Bill-of-Materials Ledger                          │    │
│  └─────────────────────────────────────────────────────┘    │
└──────────────────────────────────────────────────────────────┘
```

## 📁 Directory Structure

```
repository-files/
├── .github/
│   ├── workflows/
│   │   ├── codeql.yml              # SAST security scanning
│   │   └── gitleaks.yml            # Secret detection
│   └── dependabot.yml              # Daily security updates
│
├── governance_kernel/
│   ├── crypto_shredder.py          # IP-02: Data dissolution
│   └── acorn_protocol.py           # IP-03: Somatic authentication
│
├── config/
│   └── sovereign_guardrail.yaml    # 14 global legal frameworks
│
├── scripts/
│   └── validate_fortress.sh        # Fortress validation script
│
├── .gitleaks.toml                  # Secret scanning rules
├── requirements-security.txt       # Security dependencies
└── README.md                       # This file
```

## 🚀 Quick Start

### 1. Copy Files to Your Repository

```bash
# Navigate to your iLuminara-Core repository
cd /path/to/iLuminara-Core

# Copy all files (preserving directory structure)
cp -r /path/to/repository-files/.github .
cp -r /path/to/repository-files/governance_kernel .
cp -r /path/to/repository-files/config .
cp -r /path/to/repository-files/scripts .
cp /path/to/repository-files/.gitleaks.toml .
cp /path/to/repository-files/requirements-security.txt .
```

### 2. Install Dependencies

```bash
pip install -r requirements-security.txt
```

### 3. Validate the Fortress

```bash
chmod +x scripts/validate_fortress.sh
./scripts/validate_fortress.sh
```

### 4. Enable GitHub Security Features

```bash
# Authenticate with GitHub CLI
gh auth refresh -s workflow,repo,write:packages,admin:repo_hook

# Enable branch protection
gh api repos/:owner/:repo/branches/main/protection \
  -X PUT \
  -f required_status_checks[strict]=true \
  -f required_status_checks[contexts][]=CodeQL \
  -f required_status_checks[contexts][]=Gitleaks \
  -f required_pull_request_reviews[required_approving_review_count]=1 \
  -f enforce_admins=true
```

## ⚡ Nuclear IP Stack

### IP-02: Crypto Shredder

Data is not deleted; it is cryptographically dissolved.

```python
from governance_kernel.crypto_shredder import CryptoShredder, RetentionPolicy

shredder = CryptoShredder(sovereignty_zone=SovereigntyZone.KENYA)

# Encrypt with ephemeral key
encrypted_data, key_id = shredder.encrypt_with_ephemeral_key(
    data=patient_record,
    retention_policy=RetentionPolicy.HOT,
    metadata={"patient_id": "12345", "jurisdiction": "KDPA_KE"}
)

# After retention period, shred the key
shredder.shred_key(key_id)

# Data is now cryptographically irrecoverable
```

**Compliance:**
- GDPR Art. 17 (Right to Erasure)
- HIPAA §164.530(j) (Documentation)
- NIST SP 800-88 (Media Sanitization)

### IP-03: Acorn Protocol

Somatic Triad Authentication: Posture + Location + Stillness

```python
from governance_kernel.acorn_protocol import (
    SomaticTriadAuthentication,
    AuthenticationRisk
)

sta = SomaticTriadAuthentication(posture_tolerance=15.0)

# Enroll user with "Secret Pose"
sta.enroll(
    user_id="coordinator_001",
    posture_keypoints=pose_keypoints,
    gps_coords=(-1.2921, 36.8219),  # Nairobi
    imu_readings=imu_data,
    risk_level=AuthenticationRisk.CRITICAL
)

# Authenticate for high-risk operation
result = sta.authenticate(
    user_id="coordinator_001",
    posture_keypoints=current_pose,
    gps_coords=current_location,
    imu_readings=current_imu,
    operation_risk=AuthenticationRisk.CRITICAL
)

if result.success:
    print(f"✅ Session Token: {result.session_token}")
```

**Compliance:**
- NIST SP 800-63B (Biometric Authentication)
- ISO/IEC 30107 (Presentation Attack Detection)
- GDPR Art. 9 (Biometric Data Processing)

## 🔒 Security Workflows

### CodeQL (SAST)

Runs on:
- Every push to `main` and `develop`
- Every pull request
- Weekly schedule (Sunday midnight UTC)

**Coverage:**
- Python security vulnerabilities
- JavaScript security issues
- Security-extended queries

### Gitleaks (Secret Scanning)

Runs on:
- Every push to `main` and `develop`
- Every pull request
- Daily schedule (2 AM UTC)

**Detects:**
- API keys (GCP, AWS, GitHub)
- Private keys
- JWT tokens
- Service account credentials

### Dependabot (Dependency Updates)

Runs daily at 2 AM UTC for:
- Python dependencies (pip)
- GitHub Actions
- Docker images
- npm packages

## 🌍 SovereignGuardrail Configuration

The Fortress enforces 14 global legal frameworks:

| Framework | Region | Status |
|-----------|--------|--------|
| GDPR | 🇪🇺 EU | ✅ Enforced |
| KDPA | 🇰🇪 Kenya | ✅ Enforced |
| HIPAA | 🇺🇸 USA | ✅ Enforced |
| POPIA | 🇿🇦 South Africa | ✅ Enforced |
| PIPEDA | 🇨🇦 Canada | ✅ Enforced |
| EU AI Act | 🇪🇺 EU | ✅ Enforced |
| ISO 27001 | 🌐 Global | ✅ Enforced |
| SOC 2 | 🇺🇸 USA | ✅ Enforced |

Configure in `config/sovereign_guardrail.yaml`:

```yaml
jurisdiction:
  primary: "KDPA_KE"
  secondary:
    - "GDPR_EU"
    - "POPIA_ZA"
    - "HIPAA_US"

sovereignty:
  data_residency:
    enabled: true
    allowed_zones:
      - "africa-south1"
      - "europe-west1"
    enforcement_level: "STRICT"
```

## 🧪 Testing

### Run Crypto Shredder Demo

```bash
python governance_kernel/crypto_shredder.py
```

### Run Acorn Protocol Demo

```bash
python governance_kernel/acorn_protocol.py
```

### Validate Fortress

```bash
./scripts/validate_fortress.sh
```

Expected output:
```
╔════════════════════════════════════════════════════════════╗
║     iLuminara-Core Sovereign Health Fortress Validator     ║
╚════════════════════════════════════════════════════════════╝

═══════════════════════════════════════════════════════════
PHASE 1: Security Audit Layer
═══════════════════════════════════════════════════════════

📄 Checking .github/workflows/codeql.yml... ✓ EXISTS
   └─ SAST security scanning (GDPR Art. 32, ISO 27001 A.12.6)
📄 Checking .github/workflows/gitleaks.yml... ✓ EXISTS
   └─ Secret scanning (NIST SP 800-53 IA-5)
...

🛡️  FORTRESS STATUS: OPERATIONAL
✓  All critical components validated
✓  Security audit layer active
✓  Governance kernel operational
✓  Nuclear IP stack initialized

The Sovereign Health Fortress is ready for deployment.
```

## 📊 Monitoring

### Prometheus Metrics

The security stack exposes metrics at `:9090/metrics`:

```
sovereignty_violations_total
cross_border_transfers_total
high_risk_inferences_total
keys_shredded_total
authentication_attempts_total
authentication_failures_total
```

### Grafana Dashboards

Import dashboards for:
- Sovereignty Compliance
- Audit Trail
- Data Retention
- Authentication Analytics

## 🔐 Compliance Attestation

The Fortress provides continuous compliance attestation:

| Framework | Attestation Method | Frequency |
|-----------|-------------------|-----------|
| GDPR | SovereignGuardrail + Audit Trail | Real-time |
| HIPAA | Crypto Shredder + Retention Policies | Daily |
| ISO 27001 | CodeQL + Gitleaks | Weekly |
| SOC 2 | Tamper-proof Audit | Continuous |
| NIST CSF | Security Workflows | Daily |

## 🚨 Incident Response

1. **Detection**: Security workflows trigger alerts
2. **Containment**: SovereignGuardrail blocks violating actions
3. **Investigation**: Tamper-proof audit trail provides forensics
4. **Remediation**: Crypto Shredder dissolves compromised data
5. **Recovery**: Golden Thread reconstructs verified timeline

## 📚 Documentation

Full documentation available at: [docs.iluminara.health](https://docs.iluminara.health)

- [Security Overview](/security/overview)
- [Crypto Shredder (IP-02)](/security/crypto-shredder)
- [Acorn Protocol (IP-03)](/security/acorn-protocol)
- [Governance Kernel](/governance/overview)
- [Deployment Guide](/deployment/overview)

## 🤝 Contributing

When contributing security-related code:

1. All PRs must pass CodeQL and Gitleaks scans
2. Security changes require 2 approvals
3. Update `config/sovereign_guardrail.yaml` for new jurisdictions
4. Add tests for new security features
5. Update documentation

## 📄 License

This security stack is part of iLuminara-Core and follows the same license.

## 🆘 Support

For security issues:
- **Email**: security@iluminara.health
- **GitHub**: Open a security advisory
- **Slack**: #security channel

---

**The Fortress is not built. It is continuously attested.**

🛡️ iLuminara-Core Sovereign Health Fortress
