# iLuminara-Core Security & Integration Stack

This directory contains the complete **Sovereign Health Fortress** security and integration stack for iLuminara-Core.

## 🛡️ The Fortress

The iLuminara security stack implements:

- **Security Audit Layer** - CodeQL SAST, Gitleaks secret scanning, Dependabot updates
- **Governance Kernel** - SovereignGuardrail, Crypto Shredder (IP-02), Ethical Engine
- **Nuclear IP Stack** - 5 proprietary innovations for sovereign health intelligence
- **Integration Layer** - Vertex AI + SHAP, Bio-Interface REST API

## 📁 Directory Structure

```
repository-files/
├── .github/
│   ├── workflows/
│   │   ├── codeql.yml              # SAST security scanning
│   │   └── gitleaks.yml            # Secret detection
│   └── dependabot.yml              # Daily security updates
├── .gitleaks.toml                  # Secret scanning rules
├── governance_kernel/
│   └── crypto_shredder.py          # IP-02: Data dissolution
├── config/
│   └── sovereign_guardrail.yaml    # Compliance configuration
├── scripts/
│   └── validate_fortress.sh        # Fortress validation
└── README.md                       # This file
```

## 🚀 Quick Start

### Step 1: Copy files to your repository

```bash
# From your iLuminara-Core repository root
cp -r /path/to/docs/repository-files/.github .
cp -r /path/to/docs/repository-files/governance_kernel .
cp -r /path/to/docs/repository-files/config .
cp -r /path/to/docs/repository-files/scripts .
cp /path/to/docs/repository-files/.gitleaks.toml .
```

### Step 2: Make scripts executable

```bash
chmod +x scripts/validate_fortress.sh
```

### Step 3: Validate the fortress

```bash
./scripts/validate_fortress.sh
```

### Step 4: Commit and push

```bash
git add .
git commit -m "feat: integrate Sovereign Health Fortress security stack"
git push
```

### Step 5: Enable branch protection

```bash
# Require PRs and passing status checks
gh api repos/VISENDI56/iLuminara-Core/branches/main/protection \
  --method PUT \
  --field required_status_checks[strict]=true \
  --field required_status_checks[contexts][]=CodeQL \
  --field required_status_checks[contexts][]=Gitleaks \
  --field required_pull_request_reviews[required_approving_review_count]=1 \
  --field enforce_admins=true
```

## 🔐 Security Workflows

### CodeQL (SAST)

**File:** `.github/workflows/codeql.yml`

- **Frequency:** Weekly + on push/PR
- **Languages:** Python, JavaScript
- **Compliance:** GDPR Art. 32, ISO 27001 A.12.6

### Gitleaks (Secret Scanning)

**File:** `.github/workflows/gitleaks.yml`

- **Frequency:** Daily at 2 AM UTC
- **Detection:** API keys, tokens, credentials
- **Compliance:** NIST SP 800-53 IA-5, HIPAA §164.312(a)(2)(i)

### Dependabot (Security Updates)

**File:** `.github/dependabot.yml`

- **Frequency:** Daily at 2 AM UTC
- **Ecosystems:** pip, npm, GitHub Actions, Docker
- **Auto-merge:** Security patches only

## ⚡ Nuclear IP Stack

### IP-02: Crypto Shredder

**File:** `governance_kernel/crypto_shredder.py`

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

Somatic security using posture + location + stillness as cryptographic authentication.

**Status:** Requires hardware attestation (TPM)

### IP-04: Silent Flux

Anxiety-regulated AI output that prevents information overload.

**Status:** Requires integration with operator monitoring

### IP-05: Golden Thread

Quantum entanglement logic to fuse vague signals into verified timelines.

**Status:** Active (see `edge_node/sync_protocol/`)

### IP-06: 5DM Bridge

API-level injection into 14M+ African mobile nodes (94% CAC reduction).

**Status:** Requires mobile network integration

## 🌍 SovereignGuardrail Configuration

**File:** `config/sovereign_guardrail.yaml`

Enforces 14 global legal frameworks:

- GDPR (EU)
- KDPA (Kenya)
- POPIA (South Africa)
- HIPAA (USA)
- PIPEDA (Canada)
- EU AI Act
- ISO 27001
- SOC 2
- NIST CSF
- And 5 more...

**Key features:**
- Data residency enforcement
- Cross-border transfer validation
- Right to explanation (SHAP)
- Consent management
- Retention policies
- Tamper-proof audit trail

## ✅ Validation

Run the fortress validation script:

```bash
./scripts/validate_fortress.sh
```

**Validation phases:**
1. Security Audit Layer (CodeQL, Gitleaks, Dependabot)
2. Governance Kernel (SovereignGuardrail, Crypto Shredder)
3. Edge Node & AI Agents
4. Cloud Oracle
5. Python Dependencies
6. Environment Configuration
7. Nuclear IP Stack Status

**Expected output:**

```
╔════════════════════════════════════════════════════════════╗
║     iLuminara-Core Sovereign Health Fortress Validator     ║
╚════════════════════════════════════════════════════════════╝

🛡️  FORTRESS STATUS: OPERATIONAL
✓  All critical components validated
✓  Security audit layer active
✓  Governance kernel operational
✓  Nuclear IP stack initialized

The Sovereign Health Fortress is ready for deployment.
```

## 📊 Monitoring

### Prometheus Metrics

```
sovereignty_violations_total
cross_border_transfers_total
high_risk_inferences_total
keys_shredded_total
```

### Grafana Dashboards

- **Sovereignty Compliance** - Real-time compliance monitoring
- **Audit Trail** - Tamper-proof audit visualization
- **Data Retention** - Key lifecycle and auto-shred status

## 🔧 Environment Variables

```bash
# Node identification
export NODE_ID=JOR-47
export JURISDICTION=KDPA_KE

# API configuration
export API_HOST=0.0.0.0
export API_PORT=8080

# GCP configuration
export GOOGLE_CLOUD_PROJECT=your-project-id
export GCP_REGION=africa-south1

# Governance
export ENABLE_TAMPER_PROOF_AUDIT=true
export RETENTION_MAX_DAYS=1825
export DATA_SOVEREIGNTY_REQUIRED=true
```

## 📚 Documentation

Complete documentation available at: https://docs.iluminara.health

- [Security Overview](/security/overview)
- [Governance Kernel](/governance/overview)
- [Crypto Shredder](/security/crypto-shredder)
- [API Reference](/api-reference/overview)
- [Deployment Guide](/deployment/overview)

## 🆘 Support

- **GitHub Issues:** https://github.com/VISENDI56/iLuminara-Core/issues
- **Documentation:** https://docs.iluminara.health
- **Email:** support@iluminara.health

## 📄 License

See LICENSE file in repository root.

---

**The Fortress is now built. Your repository has transitioned from code to Sovereign Architecture.**
