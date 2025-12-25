# iLuminara-Core Repository Files

This directory contains all the files that need to be copied to your iLuminara-Core repository to implement the **Sovereign Health Fortress**.

## 📁 Directory Structure

```
repository-files/
├── .github/
│   ├── workflows/
│   │   ├── codeql.yml          # CodeQL SAST scanning
│   │   └── gitleaks.yml        # Gitleaks secret detection
│   └── dependabot.yml          # Daily security updates
├── governance_kernel/
│   └── crypto_shredder.py      # IP-02: Data dissolution
├── config/
│   └── sovereign_guardrail.yaml # 14 global legal frameworks
├── scripts/
│   └── validate_fortress.sh    # Fortress validation
└── .gitleaks.toml              # Secret detection rules
```

## 🚀 Installation

### Step 1: Copy Files to Repository

```bash
# Navigate to your iLuminara-Core repository
cd /path/to/iLuminara-Core

# Copy all files from this directory
cp -r /path/to/docs/repository-files/.github ./
cp -r /path/to/docs/repository-files/governance_kernel ./
cp -r /path/to/docs/repository-files/config ./
cp -r /path/to/docs/repository-files/scripts ./
cp /path/to/docs/repository-files/.gitleaks.toml ./
```

### Step 2: Install Dependencies

```bash
pip install cryptography flask streamlit pandas google-cloud-bigquery google-cloud-spanner
```

### Step 3: Configure Environment

```bash
export NODE_ID=JOR-47
export JURISDICTION=KDPA_KE
export GOOGLE_CLOUD_PROJECT=your-project-id
export ENABLE_TAMPER_PROOF_AUDIT=true
```

### Step 4: Validate Installation

```bash
chmod +x scripts/validate_fortress.sh
./scripts/validate_fortress.sh
```

## 📋 File Descriptions

### Security Workflows

#### `.github/workflows/codeql.yml`
- **Purpose:** Static Application Security Testing (SAST)
- **Frequency:** Weekly (Sunday midnight UTC)
- **Languages:** Python, JavaScript
- **Compliance:** GDPR Art. 32, ISO 27001 A.12.6

#### `.github/workflows/gitleaks.yml`
- **Purpose:** Secret detection and scanning
- **Frequency:** Daily (2 AM UTC)
- **Compliance:** NIST SP 800-53 IA-5, HIPAA §164.312(a)(2)(i)

#### `.github/dependabot.yml`
- **Purpose:** Automated security updates
- **Frequency:** Daily (2 AM UTC)
- **Ecosystems:** pip, npm, docker, github-actions

#### `.gitleaks.toml`
- **Purpose:** Secret detection rules
- **Features:** Custom rules for GCP, AWS (blocked), private keys, tokens

### Nuclear IP Stack

#### `governance_kernel/crypto_shredder.py`
- **Protocol:** IP-02 (Crypto Shredder)
- **Purpose:** Data is not deleted; it is cryptographically dissolved
- **Features:**
  - Ephemeral key encryption (AES-256-GCM)
  - Retention policies (HOT, WARM, COLD, ETERNAL)
  - Auto-shred expired keys
  - Sovereignty zone enforcement
  - Tamper-proof audit logging
- **Compliance:** GDPR Art. 17, HIPAA §164.530(j), NIST SP 800-88

### Configuration

#### `config/sovereign_guardrail.yaml`
- **Purpose:** Configure 14 global legal frameworks
- **Features:**
  - Jurisdiction configuration
  - Data residency enforcement
  - Cross-border transfer controls
  - Consent management
  - Retention policies
  - Audit trail configuration
  - Humanitarian constraints

### Scripts

#### `scripts/validate_fortress.sh`
- **Purpose:** Validate complete Fortress deployment
- **Phases:**
  1. Security Audit Layer
  2. Governance Kernel
  3. Edge Node & AI Agents
  4. Cloud Oracle
  5. Python Dependencies
  6. Environment Configuration
  7. Nuclear IP Stack Status

## 🔐 Security Configuration

### Enable GitHub Workflows

```bash
# Refresh GitHub permissions
gh auth refresh -s workflow,repo,write:packages,admin:repo_hook

# Commit and push
git add .
git commit -m "feat: integrate SovereignGuardrail and Nuclear IP security stack"
git push

# Enable branch protection
gh api repos/VISENDI56/iLuminara-Core/branches/main/protection \
  -X PUT \
  -f required_status_checks[strict]=true \
  -f required_status_checks[contexts][]=CodeQL \
  -f required_status_checks[contexts][]=Gitleaks
```

### Configure Secrets

Add these secrets to your GitHub repository:

```bash
# GitHub token for Gitleaks
gh secret set GITHUB_TOKEN

# Gitleaks license (optional)
gh secret set GITLEAKS_LICENSE

# GCP credentials (if using cloud)
gh secret set GCP_SA_KEY
```

## 🧪 Testing

### Test Crypto Shredder

```bash
python governance_kernel/crypto_shredder.py
```

Expected output:
```
✅ Encrypted - Key ID: abc123
✅ Decrypted: Patient ID: 12345, Diagnosis: Malaria, Location: Dadaab
🔥 Key shredded - Data irrecoverable: abc123
❌ Decryption after shred: None
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

## 📊 Compliance Matrix

| Framework | File | Status |
|-----------|------|--------|
| GDPR Art. 32 | `.github/workflows/codeql.yml` | ✅ |
| NIST SP 800-53 | `.github/workflows/gitleaks.yml` | ✅ |
| GDPR Art. 17 | `governance_kernel/crypto_shredder.py` | ✅ |
| HIPAA §164.312 | `config/sovereign_guardrail.yaml` | ✅ |
| ISO 27001 A.12.6 | `.github/dependabot.yml` | ✅ |

## 🚨 Troubleshooting

### CodeQL Workflow Fails

**Issue:** CodeQL analysis fails with "No code to analyze"

**Solution:**
```bash
# Ensure Python files exist in repository
ls -la *.py
ls -la **/*.py

# Check workflow configuration
cat .github/workflows/codeql.yml
```

### Gitleaks Detects False Positives

**Issue:** Gitleaks flags test files or documentation

**Solution:**
```toml
# Add to .gitleaks.toml
[allowlist]
paths = [
  '''.*_test\\.py''',
  '''.*\\.md''',
]
```

### Crypto Shredder Import Error

**Issue:** `ModuleNotFoundError: No module named 'cryptography'`

**Solution:**
```bash
pip install cryptography
```

### Fortress Validation Fails

**Issue:** Missing dependencies or environment variables

**Solution:**
```bash
# Install dependencies
pip install -r requirements.txt

# Set environment variables
export NODE_ID=JOR-47
export JURISDICTION=KDPA_KE

# Re-run validation
./scripts/validate_fortress.sh
```

## 📚 Documentation

Full documentation available at: https://docs.iluminara.health

- **Security Stack:** /security/overview
- **Governance Kernel:** /governance/overview
- **Crypto Shredder:** /security/crypto-shredder
- **Compliance Matrix:** /governance/compliance

## 🤝 Support

- **Compliance:** compliance@iluminara.health
- **Security:** security@iluminara.health
- **Technical:** support@iluminara.health
- **GitHub:** https://github.com/VISENDI56/iLuminara-Core

## 📝 License

Proprietary - Nuclear IP Stack protected

---

**The Fortress is not built. It is continuously attested.**
