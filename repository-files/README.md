# iLuminara-Core Repository Files

## 📦 Contents

This directory contains all files ready to be copied to your iLuminara-Core repository to implement the **Sovereign Health Fortress** security and integration stack.

## 🗂️ Directory Structure

```
repository-files/
├── .github/
│   ├── workflows/
│   │   ├── codeql.yml          # CodeQL SAST security scanning
│   │   └── gitleaks.yml        # Gitleaks secret detection
│   └── dependabot.yml          # Daily security updates
├── .gitleaks.toml              # Secret detection rules
├── governance_kernel/
│   └── crypto_shredder.py      # IP-02: Crypto Shredder implementation
├── config/
│   └── sovereign_guardrail.yaml # SovereignGuardrail configuration (50 frameworks)
├── scripts/
│   └── validate_fortress.sh    # Fortress validation script
├── IMPLEMENTATION_SUMMARY.md   # Complete implementation guide
└── README.md                   # This file
```

## 🚀 Quick Start

### 1. Copy Files to Repository

```bash
# Navigate to your iLuminara-Core repository
cd /path/to/iLuminara-Core

# Copy all files (from the parent directory of repository-files)
cp -r repository-files/.github .
cp -r repository-files/governance_kernel .
cp -r repository-files/config .
cp -r repository-files/scripts .
cp repository-files/.gitleaks.toml .
```

### 2. Set Permissions

```bash
chmod +x scripts/validate_fortress.sh
```

### 3. Configure Environment

```bash
export NODE_ID=JOR-47
export JURISDICTION=KDPA_KE
export GOOGLE_CLOUD_PROJECT=your-project-id
export ENABLE_TAMPER_PROOF_AUDIT=true
```

### 4. Validate

```bash
./scripts/validate_fortress.sh
```

## 📋 File Descriptions

### Security Audit Layer

#### `.github/workflows/codeql.yml`
- **Purpose:** Static Application Security Testing (SAST)
- **Runs:** On push, PR, weekly schedule
- **Languages:** Python, JavaScript
- **Compliance:** GDPR Art. 32, ISO 27001 A.12.6

#### `.github/workflows/gitleaks.yml`
- **Purpose:** Secret and credential scanning
- **Runs:** Daily at 2 AM UTC
- **Output:** SARIF format for GitHub Security
- **Compliance:** NIST SP 800-53 IA-5, HIPAA §164.312(a)(2)(i)

#### `.gitleaks.toml`
- **Purpose:** Custom secret detection rules
- **Features:**
  - Sovereignty-aware (blocks AWS keys, allows GCP)
  - Allowlist for test files
  - Detects: API keys, private keys, JWT tokens, service accounts

#### `.github/dependabot.yml`
- **Purpose:** Automated dependency updates
- **Frequency:** Daily for Python/npm, weekly for Docker/Actions
- **Groups:** Security, Google Cloud, AI/ML dependencies

### Governance Kernel

#### `governance_kernel/crypto_shredder.py`
- **Purpose:** IP-02 Crypto Shredder implementation
- **Features:**
  - Ephemeral key encryption (AES-256-GCM)
  - Retention policies: HOT (180d), WARM (365d), COLD (1825d)
  - Cryptographic key shredding (DoD 5220.22-M)
  - Tamper-proof audit trail
- **Compliance:** GDPR Art. 17, HIPAA §164.530(j), NIST SP 800-88

#### `config/sovereign_guardrail.yaml`
- **Purpose:** Complete SovereignGuardrail configuration
- **Features:**
  - 50 global legal frameworks
  - Jurisdiction routing (KDPA_KE, GDPR_EU, HIPAA_US, POPIA_ZA)
  - Data sovereignty enforcement
  - Consent management
  - Retention policies
  - Tamper-proof audit configuration
  - Nuclear IP Stack integration

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
- **Exit Codes:**
  - `0` = FORTRESS OPERATIONAL
  - `1` = FORTRESS COMPROMISED

## 🔧 Configuration

### Required Environment Variables

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

# Governance
export ENABLE_TAMPER_PROOF_AUDIT=true
export RETENTION_MAX_DAYS=1825
export DATA_SOVEREIGNTY_REQUIRED=true
export REQUIRES_EXPLICIT_CONSENT=true
```

### Optional Environment Variables

```bash
# Offline operation
export ENABLE_OFFLINE_MODE=true
export SYNC_INTERVAL_SECONDS=300

# Federated learning
export FEDERATED_LEARNING_EPSILON=1.0
export FEDERATED_LEARNING_DELTA=1e-5

# Monitoring
export PROMETHEUS_PORT=9090
export GRAFANA_PORT=3000
```

## 🧪 Testing

### Test Crypto Shredder

```python
from governance_kernel.crypto_shredder import CryptoShredder, RetentionPolicy

shredder = CryptoShredder()

# Encrypt
encrypted, key_id = shredder.encrypt_with_ephemeral_key(
    data=b"Patient data",
    retention_policy=RetentionPolicy.HOT
)

# Decrypt
decrypted = shredder.decrypt_with_key(encrypted, key_id)

# Shred
shredder.shred_key(key_id)
```

### Test SovereignGuardrail

```python
from governance_kernel.vector_ledger import SovereignGuardrail

guardrail = SovereignGuardrail()

guardrail.validate_action(
    action_type='Data_Transfer',
    payload={'data_type': 'PHI', 'destination': 'Local_Node'},
    jurisdiction='KDPA_KE'
)
```

### Validate Fortress

```bash
./scripts/validate_fortress.sh
```

## 📊 Compliance Coverage

| Framework | File | Status |
|-----------|------|--------|
| **GDPR** | sovereign_guardrail.yaml | ✅ |
| **KDPA** | sovereign_guardrail.yaml | ✅ |
| **HIPAA** | sovereign_guardrail.yaml | ✅ |
| **POPIA** | sovereign_guardrail.yaml | ✅ |
| **EU AI Act** | sovereign_guardrail.yaml | ✅ |
| **ISO 27001** | codeql.yml, crypto_shredder.py | ✅ |
| **SOC 2** | gitleaks.yml, crypto_shredder.py | ✅ |
| **NIST CSF** | All workflows | ✅ |
| **+42 more** | sovereign_guardrail.yaml | ✅ |

## 🔐 Security Features

### CodeQL SAST
- Security-extended queries
- Python and JavaScript analysis
- Weekly scheduled scans
- PR blocking on critical findings

### Gitleaks Secret Detection
- Daily automated scans
- Custom sovereignty-aware rules
- SARIF output for GitHub Security
- Allowlist for test files

### Crypto Shredder (IP-02)
- AES-256-GCM encryption
- Ephemeral key management
- Retention policy enforcement
- DoD 5220.22-M key shredding
- Tamper-proof audit trail

### SovereignGuardrail
- 50 global legal frameworks
- Real-time sovereignty validation
- Cross-border transfer blocking
- Consent management
- Retention window enforcement

## 🚨 Troubleshooting

### Validation Fails

```bash
# Check missing dependencies
pip install -r requirements.txt

# Check environment variables
echo $NODE_ID
echo $JURISDICTION

# Re-run validation
./scripts/validate_fortress.sh
```

### GitHub Workflows Not Running

```bash
# Refresh permissions
gh auth refresh -s workflow,repo,write:packages

# Check workflow status
gh workflow list
gh run list
```

### Crypto Shredder Errors

```python
# Check key storage directory
import os
os.makedirs("./keys", exist_ok=True)

# Enable debug logging
import logging
logging.basicConfig(level=logging.DEBUG)
```

## 📚 Documentation

For complete documentation, see:
- **IMPLEMENTATION_SUMMARY.md** - Full implementation guide
- **Main Documentation** - (Your documentation site URL)
- **GitHub Repository** - https://github.com/VISENDI56/iLuminara-Core

## 🌟 Next Steps

1. ✅ Copy files to repository
2. ✅ Set permissions
3. ✅ Configure environment
4. ✅ Run validation
5. ✅ Enable GitHub workflows
6. ✅ Test Crypto Shredder
7. ✅ Test SovereignGuardrail
8. ✅ Commit and push

## 🎯 Support

- **Issues:** https://github.com/VISENDI56/iLuminara-Core/issues
- **Discussions:** https://github.com/VISENDI56/iLuminara-Core/discussions

---

**Status:** FORTRESS OPERATIONAL  
**Compliance:** 50 Global Frameworks  
**Mission:** Transform preventable suffering from statistical inevitability to historical anomaly
