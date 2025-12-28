# iLuminara-Core Repository Files

This directory contains all the files you need to copy to your iLuminara-Core repository to implement the complete Sovereign Health Fortress.

## 📁 Directory Structure

```
repository-files/
├── .github/
│   ├── workflows/
│   │   ├── codeql.yml              # CodeQL SAST scanning
│   │   └── gitleaks.yml            # Secret scanning
│   └── dependabot.yml              # Daily security updates
├── .gitleaks.toml                  # Gitleaks configuration
├── config/
│   └── sovereign_guardrail.yaml    # SovereignGuardrail config
├── governance_kernel/
│   └── crypto_shredder.py          # IP-02 implementation
├── scripts/
│   ├── validate_fortress.sh        # Fortress validation
│   └── ingest_repository.py        # Repository ingestion engine
├── FORTRESS_DEPLOYMENT_COMPLETE.md # Deployment summary
└── README.md                       # This file
```

## 🚀 Quick Start

### Step 1: Copy Files to Your Repository

```bash
# Navigate to your iLuminara-Core repository
cd /path/to/iLuminara-Core

# Copy security workflows
mkdir -p .github/workflows
cp /path/to/docs/repository-files/.github/workflows/* .github/workflows/

# Copy Dependabot config
cp /path/to/docs/repository-files/.github/dependabot.yml .github/

# Copy Gitleaks config
cp /path/to/docs/repository-files/.gitleaks.toml .

# Copy governance kernel
cp /path/to/docs/repository-files/governance_kernel/crypto_shredder.py governance_kernel/

# Copy configuration
mkdir -p config
cp /path/to/docs/repository-files/config/sovereign_guardrail.yaml config/

# Copy scripts
cp /path/to/docs/repository-files/scripts/* scripts/
chmod +x scripts/*.sh
```

### Step 2: Commit and Push

```bash
git add .
git commit -m "feat: integrate Sovereign Health Fortress and Nuclear IP security stack

- Add CodeQL SAST scanning workflow
- Add Gitleaks secret scanning workflow
- Add Dependabot daily security updates
- Implement IP-02 Crypto Shredder
- Add SovereignGuardrail configuration
- Add fortress validation script
- Add repository ingestion engine"

git push
```

### Step 3: Enable Branch Protection

```bash
# Authenticate with GitHub CLI
gh auth refresh -s workflow,repo,write:packages,admin:repo_hook

# Enable branch protection
gh api repos/VISENDI56/iLuminara-Core/branches/main/protection \
  --method PUT \
  --field required_status_checks[strict]=true \
  --field required_status_checks[contexts][]=CodeQL \
  --field required_status_checks[contexts][]=Gitleaks \
  --field required_pull_request_reviews[required_approving_review_count]=1
```

### Step 4: Validate Fortress

```bash
./scripts/validate_fortress.sh
```

## 📋 File Descriptions

### Security Workflows

#### `.github/workflows/codeql.yml`
- **Purpose:** Static Application Security Testing (SAST)
- **Frequency:** Weekly + on every push/PR
- **Languages:** Python, JavaScript
- **Compliance:** GDPR Art. 32, ISO 27001 A.12.6

#### `.github/workflows/gitleaks.yml`
- **Purpose:** Secret and credential scanning
- **Frequency:** Daily at 2 AM UTC
- **Compliance:** NIST SP 800-53 IA-5, HIPAA §164.312(a)(2)(i)

#### `.github/dependabot.yml`
- **Purpose:** Automated dependency updates
- **Frequency:** Daily for Python, weekly for Docker/Actions
- **Features:** Security-only updates, grouped by category

### Governance Kernel

#### `governance_kernel/crypto_shredder.py`
- **Purpose:** IP-02 implementation - Data dissolution
- **Features:**
  - Ephemeral key encryption
  - Auto-shred expired keys
  - Retention policies (HOT, WARM, COLD, ETERNAL)
  - Tamper-proof audit trail
- **Compliance:** GDPR Art. 17, HIPAA §164.530(j), NIST SP 800-88

### Configuration

#### `config/sovereign_guardrail.yaml`
- **Purpose:** SovereignGuardrail configuration
- **Features:**
  - 14 global legal frameworks
  - Data sovereignty rules
  - Retention policies
  - Audit configuration
- **Jurisdictions:** KDPA (Kenya), GDPR (EU), POPIA (South Africa), HIPAA (USA)

### Scripts

#### `scripts/validate_fortress.sh`
- **Purpose:** Comprehensive fortress validation
- **Phases:**
  1. Security Audit Layer
  2. Governance Kernel
  3. Edge Node & AI Agents
  4. Cloud Oracle
  5. Python Dependencies
  6. Environment Configuration
  7. Nuclear IP Stack Status

#### `scripts/ingest_repository.py`
- **Purpose:** Generate documentation for 800+ files
- **Features:**
  - Recursive repository scanning
  - MDX documentation generation
  - Navigation structure creation
  - Metadata extraction
  - Compliance tagging

### Configuration Files

#### `.gitleaks.toml`
- **Purpose:** Gitleaks detection rules
- **Rules:** 45+ secret detection patterns
- **Features:**
  - GCP, AWS, GitHub token detection
  - Private key detection
  - JWT token detection
  - Allowlist for test files

## 🔧 Configuration

### Environment Variables

Set these environment variables before running:

```bash
# Node identification
export NODE_ID=JOR-47
export JURISDICTION=KDPA_KE

# API configuration
export API_HOST=0.0.0.0
export API_PORT=8080

# GCP configuration (if using cloud)
export GOOGLE_CLOUD_PROJECT=your-project-id
export GCP_REGION=us-central1

# Governance configuration
export ENABLE_TAMPER_PROOF_AUDIT=true
export RETENTION_MAX_DAYS=1825
export DATA_SOVEREIGNTY_REQUIRED=true

# AI agents configuration
export ENABLE_OFFLINE_MODE=true
export SYNC_INTERVAL_SECONDS=300
export FEDERATED_LEARNING_EPSILON=1.0
```

### SovereignGuardrail Configuration

Edit `config/sovereign_guardrail.yaml` to customize:

```yaml
jurisdiction:
  primary: "KDPA_KE"  # Change to your primary jurisdiction
  secondary:
    - "GDPR_EU"
    - "POPIA_ZA"

sovereignty:
  data_residency:
    enabled: true
    enforcement_level: "STRICT"  # STRICT | MODERATE | PERMISSIVE
```

## 🧪 Testing

### Test Security Workflows

```bash
# Trigger CodeQL scan
git push

# Check workflow status
gh run list --workflow=codeql.yml

# View results
gh run view
```

### Test Crypto Shredder

```python
from governance_kernel.crypto_shredder import CryptoShredder, RetentionPolicy

shredder = CryptoShredder(sovereignty_zone=SovereigntyZone.KENYA)

# Encrypt data
encrypted_data, key_id = shredder.encrypt_with_ephemeral_key(
    data=b"Test data",
    retention_policy=RetentionPolicy.HOT
)

# Shred key
shredder.shred_key(key_id)

# Verify shredded
status = shredder.get_key_status(key_id)
assert status['shredded'] == True
```

### Test Fortress Validation

```bash
./scripts/validate_fortress.sh
```

Expected output:
```
🛡️  FORTRESS STATUS: OPERATIONAL
✓  All critical components validated
✓  Security audit layer active
✓  Governance kernel operational
✓  Nuclear IP stack initialized
```

## 📊 Monitoring

### GitHub Actions

Monitor security workflows:
- **CodeQL:** https://github.com/VISENDI56/iLuminara-Core/actions/workflows/codeql.yml
- **Gitleaks:** https://github.com/VISENDI56/iLuminara-Core/actions/workflows/gitleaks.yml

### Security Alerts

View security alerts:
```bash
gh api repos/VISENDI56/iLuminara-Core/code-scanning/alerts
```

### Dependabot

View dependency updates:
```bash
gh api repos/VISENDI56/iLuminara-Core/dependabot/alerts
```

## 🆘 Troubleshooting

### CodeQL Workflow Fails

**Problem:** CodeQL workflow fails with permission error

**Solution:**
```bash
gh api repos/VISENDI56/iLuminara-Core/actions/permissions \
  --method PUT \
  --field enabled=true
```

### Gitleaks False Positives

**Problem:** Gitleaks detects test data as secrets

**Solution:** Add to `.gitleaks.toml` allowlist:
```toml
[allowlist]
paths = [
  '''.*_test\\.py''',
  '''.*\\.example'''
]
```

### Crypto Shredder Import Error

**Problem:** Cannot import CryptoShredder

**Solution:**
```bash
pip install cryptography pyyaml
```

### Validation Script Fails

**Problem:** Validation script reports missing files

**Solution:** Ensure all files are copied:
```bash
ls -la .github/workflows/
ls -la governance_kernel/crypto_shredder.py
ls -la config/sovereign_guardrail.yaml
```

## 📚 Documentation

For complete documentation, see:
- **Deployment Guide:** `FORTRESS_DEPLOYMENT_COMPLETE.md`
- **Online Docs:** https://docs.iluminara.health
- **Code Reference:** https://docs.iluminara.health/reference

## 🎯 Next Steps

1. ✅ Copy all files to repository
2. ✅ Commit and push changes
3. ✅ Enable branch protection
4. ✅ Run fortress validation
5. ✅ Review security workflow results
6. Configure GCP project (optional)
7. Deploy to production
8. Train team on new features

## 📞 Support

- **GitHub Issues:** https://github.com/VISENDI56/iLuminara-Core/issues
- **Security:** security@iluminara.health
- **Documentation:** https://docs.iluminara.health

---

**Last Updated:** December 28, 2025  
**Version:** 1.0.0  
**Status:** ✅ Ready for deployment
