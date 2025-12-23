# iLuminara-Core Sovereign Health Fortress - Implementation Files

This directory contains all the files needed to implement the complete **Sovereign Health Fortress** security and integration stack for iLuminara-Core.

## 🛡️ The Nuclear IP Stack

| Component | iLuminara Protocol | Status |
|-----------|-------------------|--------|
| **Security Audit** | Gitleaks + CodeQL | ✅ Ready |
| **Data Lifecycle** | IP-02 Crypto Shredder | ✅ Ready |
| **Intelligence** | IP-04 Silent Flux | ⚠️ Requires Integration |
| **Connectivity** | IP-06 5DM Bridge | ⚠️ Requires Mobile Network |

## 📁 Directory Structure

```
repository-files/
├── .github/
│   ├── workflows/
│   │   ├── codeql.yml           # SAST security scanning
│   │   └── gitleaks.yml         # Secret detection
│   └── dependabot.yml           # Daily security updates
├── .gitleaks.toml               # Secret scanning rules
├── governance_kernel/
│   └── crypto_shredder.py       # IP-02: Data dissolution
├── config/
│   └── sovereign_guardrail.yaml # 14 global legal frameworks
└── scripts/
    └── validate_fortress.sh     # Fortress validation script
```

## 🚀 Quick Deployment

### Step 1: Copy files to your repository

```bash
# Navigate to your iLuminara-Core repository
cd /path/to/iLuminara-Core

# Copy all files from this directory
cp -r /path/to/docs/repository-files/.github .
cp -r /path/to/docs/repository-files/.gitleaks.toml .
cp -r /path/to/docs/repository-files/governance_kernel/crypto_shredder.py governance_kernel/
cp -r /path/to/docs/repository-files/config/sovereign_guardrail.yaml config/
cp -r /path/to/docs/repository-files/scripts/validate_fortress.sh scripts/

# Make scripts executable
chmod +x scripts/validate_fortress.sh
```

### Step 2: Install dependencies

```bash
pip install cryptography flask streamlit pandas google-cloud-bigquery google-cloud-spanner
```

### Step 3: Configure environment

```bash
# Set required environment variables
export NODE_ID=JOR-47
export JURISDICTION=KDPA_KE
export GOOGLE_CLOUD_PROJECT=your-project-id
export GCP_REGION=africa-south1
```

### Step 4: Validate the Fortress

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

### Step 5: Enable GitHub workflows

```bash
# Authenticate with GitHub
gh auth refresh -s workflow,repo,write:packages,admin:repo_hook

# Push changes
git add .
git commit -m "feat: integrate SovereignGuardrail and Nuclear IP security stack"
git push

# Enable branch protection
gh api repos/VISENDI56/iLuminara-Core/branches/main/protection \
  -X PUT \
  -f required_status_checks[strict]=true \
  -f required_status_checks[contexts][]=CodeQL \
  -f required_status_checks[contexts][]=Gitleaks \
  -f enforce_admins=true \
  -f required_pull_request_reviews[required_approving_review_count]=1
```

## 📋 File Descriptions

### Security Workflows

#### `.github/workflows/codeql.yml`
- **Purpose**: SAST security scanning with CodeQL
- **Schedule**: Weekly on Sunday + on every push/PR
- **Compliance**: GDPR Art. 32, ISO 27001 A.12.6
- **Languages**: Python, JavaScript

#### `.github/workflows/gitleaks.yml`
- **Purpose**: Secret detection and credential scanning
- **Schedule**: Daily at 2 AM UTC + on every push/PR
- **Compliance**: NIST SP 800-53 IA-5, HIPAA §164.312(a)(2)(i)
- **Output**: SARIF format for GitHub Security tab

#### `.github/dependabot.yml`
- **Purpose**: Daily automated security updates
- **Ecosystems**: pip, GitHub Actions, Docker, npm
- **Schedule**: Daily at 2 AM UTC
- **Grouping**: Security updates, Google Cloud, AI/ML packages

#### `.gitleaks.toml`
- **Purpose**: Secret detection rules configuration
- **Rules**: GCP keys, AWS keys (blocked), private keys, tokens
- **Allowlist**: Test files, documentation, examples

### Governance Kernel

#### `governance_kernel/crypto_shredder.py`
- **Purpose**: IP-02 implementation - Data dissolution
- **Features**:
  - AES-256-GCM encryption with ephemeral keys
  - Retention policies (HOT, WARM, COLD, ETERNAL)
  - Automatic key shredding after expiration
  - Sovereignty zone enforcement
  - Tamper-proof audit trail
- **Compliance**: GDPR Art. 17, HIPAA §164.530(j), NIST SP 800-88

#### `config/sovereign_guardrail.yaml`
- **Purpose**: Configuration for 14 global legal frameworks
- **Features**:
  - Data sovereignty rules
  - Cross-border transfer restrictions
  - Right to Explanation enforcement
  - Consent management
  - Data retention policies
  - Humanitarian constraints
- **Frameworks**: GDPR, KDPA, HIPAA, POPIA, EU AI Act, ISO 27001, SOC 2, NIST CSF

### Validation Scripts

#### `scripts/validate_fortress.sh`
- **Purpose**: Comprehensive Fortress validation
- **Phases**:
  1. Security Audit Layer
  2. Governance Kernel
  3. Edge Node & AI Agents
  4. Cloud Oracle
  5. Python Dependencies
  6. Environment Configuration
  7. Nuclear IP Stack Status
- **Output**: Colored terminal output with detailed status

## 🔐 Security Features

### 1. CodeQL SAST Scanning
- Detects security vulnerabilities in code
- Security-extended queries
- Automatic PR comments with findings
- Integration with GitHub Security tab

### 2. Gitleaks Secret Detection
- Prevents hardcoded credentials
- Custom rules for GCP, AWS, GitHub tokens
- Blocks sovereignty violations (e.g., AWS keys)
- SARIF output for GitHub Security

### 3. Dependabot Security Updates
- Daily automated dependency updates
- Security-only updates for production
- Grouped updates by category
- Automatic PR creation

### 4. Crypto Shredder (IP-02)
- Cryptographic data dissolution
- Ephemeral key management
- Automatic expiration enforcement
- Sovereignty zone isolation

### 5. SovereignGuardrail
- 14 global legal frameworks
- Real-time compliance enforcement
- Tamper-proof audit trail
- Humanitarian constraints

## 📊 Compliance Matrix

| Framework | Component | Status |
|-----------|-----------|--------|
| **GDPR Art. 32** | CodeQL SAST | ✅ Active |
| **NIST SP 800-53** | Gitleaks | ✅ Active |
| **GDPR Art. 17** | Crypto Shredder | ✅ Active |
| **HIPAA §164.530(j)** | Crypto Shredder | ✅ Active |
| **ISO 27001 A.12.6** | CodeQL | ✅ Active |
| **SOC 2** | Dependabot | ✅ Active |
| **EU AI Act §6** | SovereignGuardrail | ✅ Active |

## 🧪 Testing

### Test Crypto Shredder

```python
from governance_kernel.crypto_shredder import CryptoShredder, RetentionPolicy, SovereigntyZone

# Initialize
shredder = CryptoShredder(
    sovereignty_zone=SovereigntyZone.KENYA,
    enable_audit=True
)

# Encrypt
patient_data = b"Patient ID: 12345, Diagnosis: Malaria"
encrypted_data, key_id = shredder.encrypt_with_ephemeral_key(
    data=patient_data,
    retention_policy=RetentionPolicy.HOT,
    metadata={"patient_id": "12345", "jurisdiction": "KDPA_KE"}
)

print(f"✅ Encrypted - Key ID: {key_id}")

# Decrypt (while key exists)
decrypted = shredder.decrypt_with_key(encrypted_data, key_id)
print(f"✅ Decrypted: {decrypted.decode()}")

# Shred key
shredder.shred_key(key_id)

# Try to decrypt after shredding
decrypted = shredder.decrypt_with_key(encrypted_data, key_id)
print(f"❌ After shred: {decrypted}")  # None - data irrecoverable
```

### Test SovereignGuardrail

```python
from governance_kernel.vector_ledger import SovereignGuardrail, SovereigntyViolationError

guardrail = SovereignGuardrail()

# Test data sovereignty
try:
    guardrail.validate_action(
        action_type='Data_Transfer',
        payload={'data_type': 'PHI', 'destination': 'AWS_US'},
        jurisdiction='GDPR_EU'
    )
except SovereigntyViolationError as e:
    print(f"❌ {e}")  # Expected: sovereignty violation
```

## 🚨 Troubleshooting

### CodeQL workflow fails
```bash
# Check workflow logs
gh run list --workflow=codeql.yml

# View specific run
gh run view <run-id>
```

### Gitleaks detects false positive
Add to `.gitleaks.toml` allowlist:
```toml
[allowlist]
regexes = [
  '''your-false-positive-pattern'''
]
```

### Crypto Shredder key not found
```python
# Check key status
status = shredder.get_key_status(key_id)
print(status)

# List all keys
import os
keys = os.listdir('./keys')
print(f"Available keys: {keys}")
```

## 📚 Documentation

Full documentation available at: https://docs.iluminara.health

- [Security Stack Overview](https://docs.iluminara.health/security/overview)
- [Crypto Shredder (IP-02)](https://docs.iluminara.health/security/crypto-shredder)
- [SovereignGuardrail](https://docs.iluminara.health/governance/overview)
- [Vertex AI + SHAP Integration](https://docs.iluminara.health/integration/vertex-ai-shap)
- [Bio-Interface REST API](https://docs.iluminara.health/integration/bio-interface)

## 🤝 Support

For issues or questions:
- GitHub Issues: https://github.com/VISENDI56/iLuminara-Core/issues
- Documentation: https://docs.iluminara.health

## 📄 License

See LICENSE file in the main repository.

---

**The Fortress is not built. It is continuously attested.**
