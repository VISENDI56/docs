# iLuminara-Core Repository Files

This directory contains all the files you need to copy to your iLuminara-Core repository to implement the **Sovereign Health Fortress** security stack.

## 📁 Directory Structure

```
repository-files/
├── .github/
│   ├── workflows/
│   │   ├── codeql.yml          # CodeQL SAST security scanning
│   │   └── gitleaks.yml        # Gitleaks secret detection
│   └── dependabot.yml          # Daily security updates
├── .gitleaks.toml              # Gitleaks configuration
├── governance_kernel/
│   └── crypto_shredder.py      # IP-02: Data dissolution
├── config/
│   └── sovereign_guardrail.yaml # SovereignGuardrail configuration
├── scripts/
│   └── validate_fortress.sh    # Fortress validation script
├── DEPLOYMENT_GUIDE.md         # Complete deployment guide
└── README.md                   # This file
```

## 🚀 Quick Start

### Step 1: Copy Files to Your Repository

```bash
# Navigate to your iLuminara-Core repository
cd /path/to/iLuminara-Core

# Copy security workflows
mkdir -p .github/workflows
cp /path/to/docs/repository-files/.github/workflows/codeql.yml .github/workflows/
cp /path/to/docs/repository-files/.github/workflows/gitleaks.yml .github/workflows/
cp /path/to/docs/repository-files/.gitleaks.toml .
cp /path/to/docs/repository-files/.github/dependabot.yml .github/

# Copy governance kernel
cp /path/to/docs/repository-files/governance_kernel/crypto_shredder.py governance_kernel/

# Copy configuration
mkdir -p config
cp /path/to/docs/repository-files/config/sovereign_guardrail.yaml config/

# Copy validation script
mkdir -p scripts
cp /path/to/docs/repository-files/scripts/validate_fortress.sh scripts/
chmod +x scripts/validate_fortress.sh
```

### Step 2: Commit and Push

```bash
git add .github/workflows/codeql.yml
git add .github/workflows/gitleaks.yml
git add .gitleaks.toml
git add .github/dependabot.yml
git add governance_kernel/crypto_shredder.py
git add config/sovereign_guardrail.yaml
git add scripts/validate_fortress.sh

git commit -m "feat: integrate Sovereign Health Fortress security stack

- Add CodeQL SAST scanning workflow
- Add Gitleaks secret detection workflow
- Configure Dependabot for daily security updates
- Implement IP-02 Crypto Shredder
- Add SovereignGuardrail configuration
- Add fortress validation script

Compliance: GDPR, HIPAA, KDPA, POPIA, ISO 27001, SOC 2, NIST CSF"

git push origin main
```

### Step 3: Enable GitHub Security Features

```bash
# Authenticate with GitHub CLI
gh auth refresh -s workflow,repo,write:packages,admin:repo_hook

# Enable Dependabot alerts
gh api -X PUT /repos/VISENDI56/iLuminara-Core/vulnerability-alerts

# Enable Dependabot security updates
gh api -X PUT /repos/VISENDI56/iLuminara-Core/automated-security-fixes

# Enable secret scanning
gh api -X PUT /repos/VISENDI56/iLuminara-Core/secret-scanning

# Configure branch protection
gh api -X PUT /repos/VISENDI56/iLuminara-Core/branches/main/protection \
  -f required_status_checks='{"strict":true,"contexts":["CodeQL","Gitleaks"]}' \
  -f enforce_admins=true \
  -f required_pull_request_reviews='{"required_approving_review_count":1}' \
  -f restrictions=null
```

### Step 4: Validate Fortress

```bash
./scripts/validate_fortress.sh
```

Expected output:
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

## 📋 File Descriptions

### Security Workflows

#### `.github/workflows/codeql.yml`
- **Purpose:** Static Application Security Testing (SAST)
- **Frequency:** Weekly + on push/PR
- **Languages:** Python, JavaScript
- **Compliance:** GDPR Art. 32, ISO 27001 A.12.6

#### `.github/workflows/gitleaks.yml`
- **Purpose:** Secret detection and credential scanning
- **Frequency:** Daily at 2 AM UTC
- **Compliance:** NIST SP 800-53 IA-5, HIPAA §164.312(a)(2)(i)

#### `.github/dependabot.yml`
- **Purpose:** Automated dependency updates
- **Frequency:** Daily for security updates
- **Ecosystems:** pip, npm, GitHub Actions, Docker

#### `.gitleaks.toml`
- **Purpose:** Gitleaks configuration
- **Features:** Custom rules for GCP, AWS, private keys, JWT tokens
- **Sovereignty:** Flags AWS keys as sovereignty violations

### Governance Kernel

#### `governance_kernel/crypto_shredder.py`
- **Purpose:** IP-02 implementation - Data dissolution
- **Features:**
  - Ephemeral key encryption (AES-256-GCM)
  - Automatic key shredding after retention period
  - Sovereignty zone enforcement
  - Tamper-proof audit trail
- **Compliance:** GDPR Art. 17, HIPAA §164.530(j), NIST SP 800-88

#### `config/sovereign_guardrail.yaml`
- **Purpose:** SovereignGuardrail configuration
- **Features:**
  - 14 global legal frameworks
  - Data residency rules
  - Cross-border transfer controls
  - Retention policies
  - Audit trail configuration
- **Compliance:** GDPR, KDPA, HIPAA, POPIA, EU AI Act, ISO 27001, SOC 2

### Validation

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

## 🔐 Nuclear IP Stack

| IP | Name | Status | File |
|----|------|--------|------|
| **IP-02** | Crypto Shredder | ✅ Implemented | `governance_kernel/crypto_shredder.py` |
| **IP-03** | Acorn Protocol | ⚠️ Requires Hardware | N/A |
| **IP-04** | Silent Flux | ⚠️ Requires Integration | N/A |
| **IP-05** | Golden Thread | ✅ Active | Existing codebase |
| **IP-06** | 5DM Bridge | ⚠️ Requires Mobile Network | N/A |

## 📊 Compliance Matrix

| Framework | Files | Status |
|-----------|-------|--------|
| **GDPR** | All | ✅ Enforced |
| **KDPA** | `sovereign_guardrail.yaml`, `crypto_shredder.py` | ✅ Enforced |
| **HIPAA** | `crypto_shredder.py`, `codeql.yml` | ✅ Enforced |
| **POPIA** | `sovereign_guardrail.yaml` | ✅ Enforced |
| **EU AI Act** | `sovereign_guardrail.yaml` | ✅ Enforced |
| **ISO 27001** | `codeql.yml`, `gitleaks.yml` | ✅ Enforced |
| **SOC 2** | `crypto_shredder.py`, audit trail | ✅ Enforced |
| **NIST CSF** | All security workflows | ✅ Enforced |

## 🛠️ Configuration

### Environment Variables

```bash
# Node identification
export NODE_ID=JOR-47
export JURISDICTION=KDPA_KE

# API configuration
export API_HOST=0.0.0.0
export API_PORT=8080

# GCP configuration
export GOOGLE_CLOUD_PROJECT=your-project-id
export GCP_REGION=us-central1

# Governance configuration
export ENABLE_TAMPER_PROOF_AUDIT=true
export RETENTION_MAX_DAYS=1825
export DATA_SOVEREIGNTY_REQUIRED=true
```

### Customize SovereignGuardrail

Edit `config/sovereign_guardrail.yaml`:

```yaml
jurisdiction:
  primary: "KDPA_KE"  # Change to your jurisdiction
  secondary:
    - "GDPR_EU"
    - "POPIA_ZA"

sovereignty:
  data_residency:
    enabled: true
    allowed_zones:
      - "africa-south1"  # Add your allowed zones
    enforcement_level: "STRICT"  # STRICT | MODERATE | PERMISSIVE
```

## 🧪 Testing

### Test Crypto Shredder

```bash
python governance_kernel/crypto_shredder.py
```

### Test Fortress Validation

```bash
./scripts/validate_fortress.sh
```

### Test Security Workflows

```bash
# Trigger CodeQL manually
gh workflow run codeql.yml

# Trigger Gitleaks manually
gh workflow run gitleaks.yml
```

## 📚 Documentation

- **Full Documentation:** https://docs.iluminara.health
- **Deployment Guide:** `DEPLOYMENT_GUIDE.md`
- **Security Overview:** https://docs.iluminara.health/security/overview
- **Governance Kernel:** https://docs.iluminara.health/governance/overview

## 🆘 Troubleshooting

### CodeQL fails to build

**Solution:** Ensure all Python dependencies are in `requirements.txt`

### Gitleaks reports false positives

**Solution:** Add patterns to `.gitleaks.toml` allowlist:

```toml
[allowlist]
regexes = [
  '''YOUR_PATTERN_HERE''',
]
```

### Crypto Shredder key not found

**Solution:** Check `./keys` directory exists:

```bash
mkdir -p ./keys
chmod 700 ./keys
```

### Branch protection prevents push

**Solution:** Create a pull request instead:

```bash
git checkout -b feature/security-stack
git push origin feature/security-stack
gh pr create --title "feat: integrate security stack" --body "Implements Sovereign Health Fortress"
```

## 🔄 Updates

To update these files in the future:

1. Pull latest changes from docs repository
2. Copy updated files to your repository
3. Review changes with `git diff`
4. Commit and push
5. Re-run validation: `./scripts/validate_fortress.sh`

## 📞 Support

- **GitHub Issues:** https://github.com/VISENDI56/iLuminara-Core/issues
- **Security Issues:** security@iluminara.health
- **Documentation:** https://docs.iluminara.health

---

**The Fortress is ready. Deploy with confidence.**

🛡️ **FORTRESS STATUS: OPERATIONAL**
