# iLuminara-Core Repository Files

This directory contains all the files that should be copied to your `VISENDI56/iLuminara-Core` repository to complete the **Sovereign Health Fortress** implementation.

## 🛡️ What's Included

### Security Audit Layer
- `.github/workflows/codeql.yml` - CodeQL SAST security scanning
- `.github/workflows/gitleaks.yml` - Gitleaks secret detection
- `.gitleaks.toml` - Gitleaks configuration with sovereignty rules
- `.github/dependabot.yml` - Daily security updates

### Governance Kernel (Nuclear IP Stack)
- `governance_kernel/crypto_shredder.py` - **IP-02:** Cryptographic data dissolution
- `config/sovereign_guardrail.yaml` - SovereignGuardrail configuration

### Cloud Oracle
- `cloud_oracle/vertex_ai_explainability.py` - Vertex AI + SHAP integration for Right to Explanation

### Bio-Interface
- `bio_interface/mobile_health_api.py` - REST API for mobile health apps with Golden Thread integration

### Scripts
- `scripts/validate_fortress.sh` - Complete fortress validation script

## 📋 Installation Instructions

### Step 1: Copy Files to Repository

```bash
# Clone your repository
git clone https://github.com/VISENDI56/iLuminara-Core.git
cd iLuminara-Core

# Copy all files from this directory
cp -r /path/to/docs/repository-files/* .

# Make scripts executable
chmod +x scripts/validate_fortress.sh
chmod +x launch_all_services.sh
chmod +x deploy_gcp_prototype.sh
```

### Step 2: Install Dependencies

```bash
# Install Python dependencies
pip install -r requirements.txt

# Additional dependencies for Nuclear IP Stack
pip install cryptography shap google-cloud-aiplatform tpm2-pytss
```

### Step 3: Configure Environment

```bash
# Set environment variables
export NODE_ID="JOR-47"
export JURISDICTION="KDPA_KE"
export GOOGLE_CLOUD_PROJECT="your-project-id"
export GCP_REGION="us-central1"

# Enable tamper-proof audit
export ENABLE_TAMPER_PROOF_AUDIT=true
export RETENTION_MAX_DAYS=1825
```

### Step 4: Enable GitHub Security Features

```bash
# Authenticate with GitHub CLI
gh auth refresh -s workflow,repo,write:packages,admin:repo_hook

# Enable branch protection
gh api repos/VISENDI56/iLuminara-Core/branches/main/protection \
  --method PUT \
  --field required_status_checks[strict]=true \
  --field required_status_checks[contexts][]=CodeQL \
  --field required_status_checks[contexts][]=Gitleaks \
  --field enforce_admins=true \
  --field required_pull_request_reviews[required_approving_review_count]=1

# Enable security features
gh api repos/VISENDI56/iLuminara-Core \
  --method PATCH \
  --field security_and_analysis[secret_scanning][status]=enabled \
  --field security_and_analysis[secret_scanning_push_protection][status]=enabled
```

### Step 5: Validate Fortress

```bash
# Run validation script
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

🔍 Checking CodeQL workflow... ✓ OPERATIONAL
   └─ SAST security scanning (GDPR Art. 32, ISO 27001 A.12.6)

🔍 Checking Gitleaks workflow... ✓ OPERATIONAL
   └─ Secret scanning (NIST SP 800-53 IA-5)

...

╔════════════════════════════════════════════════════════════╗
║                    VALIDATION SUMMARY                      ║
╚════════════════════════════════════════════════════════════╝

🛡️  FORTRESS STATUS: OPERATIONAL
✓  All critical components validated
✓  Security audit layer active
✓  Governance kernel operational
✓  Nuclear IP stack initialized

The Sovereign Health Fortress is ready for deployment.
```

## 🚀 Quick Start

### Test Crypto Shredder (IP-02)

```python
from governance_kernel.crypto_shredder import CryptoShredder, RetentionPolicy

shredder = CryptoShredder(sovereignty_zone="KENYA")

# Encrypt data
encrypted_data, key_id = shredder.encrypt_with_ephemeral_key(
    data=b"Patient data",
    retention_policy=RetentionPolicy.HOT
)

# Shred key
shredder.shred_key(key_id)
```

### Test Vertex AI Explainability

```python
from cloud_oracle.vertex_ai_explainability import OutbreakForecaster

forecaster = OutbreakForecaster(project_id="your-project")

result = forecaster.forecast_outbreak(
    location="Dadaab",
    disease="cholera",
    historical_cases=[5, 8, 12, 15, 18],
    environmental_factors={"temperature": 32.0, "rainfall": 15.0},
    forecast_horizon_days=14
)

print(f"Prediction: {result.prediction:.1f} cases")
print(f"Confidence: {result.confidence_score:.1%}")
print(f"Rationale: {result.decision_rationale}")
```

### Test Bio-Interface API

```bash
# Start API server
python bio_interface/mobile_health_api.py

# Submit health signal
curl -X POST http://localhost:8080/api/v1/submit-signal \
  -H "Content-Type: application/json" \
  -d '{
    "location": {"lat": 0.0512, "lng": 40.3129},
    "symptoms": ["fever", "cough"],
    "severity": 7,
    "reporter_id": "CHV_AMINA",
    "consent_token": "VALID_TOKEN"
  }'
```

## 📊 Nuclear IP Stack Status

| Innovation | File | Status |
|------------|------|--------|
| **IP-02: Crypto Shredder** | `governance_kernel/crypto_shredder.py` | ✅ Production-ready |
| **IP-03: Acorn Protocol** | Documentation only | ⚠️ Requires hardware |
| **IP-04: Silent Flux** | Documentation only | ⚠️ Requires integration |
| **IP-05: Golden Thread** | `edge_node/sync_protocol/golden_thread.py` | ✅ Production-ready |
| **IP-06: 5DM Bridge** | Documentation only | ⚠️ Requires platform access |

## 🔒 Security Workflows

### CodeQL (SAST)
- **Trigger:** Push to main/develop, PRs, weekly schedule
- **Languages:** Python, JavaScript
- **Queries:** Security-extended + quality
- **Compliance:** GDPR Art. 32, ISO 27001 A.12.6

### Gitleaks (Secret Scanning)
- **Trigger:** Push to main/develop, PRs, daily schedule
- **Detection:** API keys, tokens, credentials
- **Compliance:** NIST SP 800-53 IA-5, HIPAA §164.312(a)(2)(i)

### Dependabot (Dependency Updates)
- **Schedule:** Daily for security updates
- **Ecosystems:** pip, npm, GitHub Actions, Docker
- **Grouping:** Security, Google Cloud, AI/ML

## 🌍 Compliance Matrix

| Framework | Files | Status |
|-----------|-------|--------|
| **GDPR** | `crypto_shredder.py`, `sovereign_guardrail.yaml` | ✅ Enforced |
| **KDPA** | `sovereign_guardrail.yaml` | ✅ Enforced |
| **HIPAA** | `crypto_shredder.py`, `mobile_health_api.py` | ✅ Enforced |
| **EU AI Act** | `vertex_ai_explainability.py` | ✅ Enforced |
| **ISO 27001** | `codeql.yml`, `gitleaks.yml` | ✅ Enforced |
| **SOC 2** | `sovereign_guardrail.yaml` (audit trail) | ✅ Enforced |

## 📚 Documentation

Complete documentation is available at your docs site:

- **Getting Started:** `/quickstart`
- **Architecture:** `/architecture/overview`
- **Governance Kernel:** `/governance/overview`
- **Nuclear IP Stack:** `/nuclear-ip/overview`
- **Security:** `/security/overview`
- **API Reference:** `/api-reference/overview`
- **Deployment:** `/deployment/overview`

## 🆘 Troubleshooting

### Validation fails

```bash
# Check Python version (requires 3.8+)
python3 --version

# Install missing dependencies
pip install -r requirements.txt

# Check environment variables
echo $NODE_ID
echo $JURISDICTION
```

### CodeQL workflow fails

```bash
# Check workflow syntax
gh workflow view codeql.yml

# Re-run workflow
gh workflow run codeql.yml
```

### Gitleaks detects false positives

Edit `.gitleaks.toml` to add allowlist:

```toml
[allowlist]
paths = [
  '''.*_test\\.py''',
  '''.*\\.example''',
]
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Run validation: `./scripts/validate_fortress.sh`
5. Submit a pull request

All PRs must pass:
- CodeQL security scan
- Gitleaks secret scan
- Fortress validation

## 📄 License

See LICENSE file in the main repository.

## 🔗 Links

- **Repository:** https://github.com/VISENDI56/iLuminara-Core
- **Documentation:** Your docs site
- **Issues:** https://github.com/VISENDI56/iLuminara-Core/issues

---

**The Sovereign Health Fortress is now operational. Transform preventable suffering from statistical inevitability to historical anomaly.**
