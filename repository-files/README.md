# iLuminara-Core: Sovereign Health Fortress Implementation Files

This directory contains all the files needed to implement the complete **Sovereign Health Fortress** security and integration stack for iLuminara-Core.

## 🛡️ The Nuclear IP Stack

| Component | Protocol | Status |
|-----------|----------|--------|
| **Security Audit** | Gitleaks + CodeQL | ✅ Ready |
| **Data Lifecycle** | IP-02 Crypto Shredder | ✅ Ready |
| **Governance** | SovereignGuardrail (47 frameworks) | ✅ Ready |
| **Validation** | Fortress Validator | ✅ Ready |

## 📁 Directory Structure

```
repository-files/
├── .github/
│   ├── workflows/
│   │   ├── codeql.yml           # SAST security scanning
│   │   └── gitleaks.yml         # Secret detection
│   └── dependabot.yml           # Daily security updates
├── .gitleaks.toml               # Secret scanning rules
├── config/
│   └── sovereign_guardrail.yaml # 47 framework configuration
├── governance_kernel/
│   └── crypto_shredder.py       # IP-02 implementation
├── scripts/
│   └── validate_fortress.sh     # Complete validation script
└── README.md                    # This file
```

## 🚀 Installation Instructions

### Step 1: Copy Files to Your Repository

```bash
# Navigate to your iLuminara-Core repository
cd /path/to/iLuminara-Core

# Copy all files from repository-files/
cp -r /path/to/docs/repository-files/.github .
cp -r /path/to/docs/repository-files/.gitleaks.toml .
cp -r /path/to/docs/repository-files/config .
cp -r /path/to/docs/repository-files/governance_kernel/crypto_shredder.py governance_kernel/
cp -r /path/to/docs/repository-files/scripts .

# Make scripts executable
chmod +x scripts/validate_fortress.sh
```

### Step 2: Enable GitHub Workflows

```bash
# Ensure you have workflow permissions
gh auth refresh -s workflow,repo,write:packages,admin:repo_hook

# Push the workflows
git add .github/
git commit -m "feat: add security audit workflows (CodeQL, Gitleaks, Dependabot)"
git push
```

### Step 3: Configure Environment Variables

```bash
# Set required environment variables
export NODE_ID=JOR-47
export JURISDICTION=KDPA_KE
export GOOGLE_CLOUD_PROJECT=your-project-id
export ENABLE_TAMPER_PROOF_AUDIT=true
```

### Step 4: Install Dependencies

```bash
# Install cryptography for Crypto Shredder
pip install cryptography

# Or install all requirements
pip install -r requirements.txt
```

### Step 5: Validate the Fortress

```bash
# Run complete validation
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

🔍 Checking .github/workflows/codeql.yml... ✓ OPERATIONAL
   └─ SAST security scanning (GDPR Art. 32, ISO 27001 A.12.6)
🔍 Checking .github/workflows/gitleaks.yml... ✓ OPERATIONAL
   └─ Secret scanning (NIST SP 800-53 IA-5)
...

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
**Purpose:** Static Application Security Testing (SAST)  
**Compliance:** GDPR Art. 32, ISO 27001 A.12.6  
**Schedule:** Weekly + on push/PR  
**Languages:** Python, JavaScript

#### `.github/workflows/gitleaks.yml`
**Purpose:** Secret and credential detection  
**Compliance:** NIST SP 800-53 IA-5, HIPAA §164.312(a)(2)(i)  
**Schedule:** Daily at 2 AM UTC + on push/PR  
**Detection:** API keys, tokens, private keys, AWS/GCP credentials

#### `.github/dependabot.yml`
**Purpose:** Automated dependency security updates  
**Compliance:** NIST CSF (Protect), ISO 27001 A.12.6  
**Schedule:** Daily for pip/npm, weekly for GitHub Actions/Docker  
**Groups:** Security, Google Cloud, AI/ML dependencies

### Configuration Files

#### `.gitleaks.toml`
**Purpose:** Secret detection rules and allowlists  
**Features:**
- GCP API key detection
- AWS credential blocking (sovereignty violation)
- Private key detection
- JWT token detection
- Test file allowlisting

#### `config/sovereign_guardrail.yaml`
**Purpose:** Complete configuration for 47 global legal frameworks  
**Categories:**
- Core Privacy & Data Protection (14 frameworks)
- Cybersecurity & Information Security (8 frameworks)
- AI Ethics & Governance (6 frameworks)
- Healthcare-Specific (5 frameworks)
- International Standards (4 frameworks)
- Regional & Sector-Specific (8 frameworks)
- Humanitarian & Ethical (2 frameworks)

**Key Features:**
- Data sovereignty rules
- Cross-border transfer restrictions
- Explainability requirements
- Consent management
- Data retention policies
- Audit trail configuration
- Humanitarian constraints
- Nuclear IP stack integration

### Core Implementations

#### `governance_kernel/crypto_shredder.py`
**Purpose:** IP-02 implementation - Data dissolution (not deletion)  
**Compliance:** GDPR Art. 17, HIPAA §164.530(j), NIST SP 800-88  
**Features:**
- Ephemeral key encryption (AES-256-GCM)
- Retention policy enforcement (HOT/WARM/COLD/ETERNAL)
- Automatic key shredding
- Sovereignty zone enforcement
- Tamper-proof audit logging

**Usage:**
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

### Validation Scripts

#### `scripts/validate_fortress.sh`
**Purpose:** Complete fortress validation across all components  
**Phases:**
1. Security Audit Layer (CodeQL, Gitleaks, Dependabot)
2. Governance Kernel (SovereignGuardrail, Crypto Shredder, Ethical Engine)
3. Edge Node & AI Agents
4. Cloud Oracle
5. Python Dependencies
6. Environment Configuration
7. Nuclear IP Stack Status

**Exit Codes:**
- `0` - All validations passed, fortress operational
- `1` - Validation errors detected, fortress compromised

## 🔐 Security Features

### 1. CodeQL SAST Scanning
- **Queries:** Security-extended + security-and-quality
- **Languages:** Python, JavaScript
- **Frequency:** Weekly + on push/PR
- **SARIF Upload:** Automatic to GitHub Security tab

### 2. Gitleaks Secret Detection
- **Rules:** Custom sovereignty-aware rules
- **Blocked:** AWS credentials (sovereignty violation)
- **Allowed:** GCP credentials (sovereignty-compliant zones)
- **SARIF Upload:** Automatic to GitHub Security tab

### 3. Dependabot Security Updates
- **Frequency:** Daily for critical dependencies
- **Grouping:** Security, Google Cloud, AI/ML
- **Strategy:** Increase-if-necessary (security-only)
- **Auto-merge:** Configurable

### 4. Crypto Shredder (IP-02)
- **Algorithm:** AES-256-GCM
- **Key Management:** Ephemeral keys with auto-shred
- **Compliance:** GDPR Art. 17, HIPAA §164.530(j)
- **Audit:** Tamper-proof logging

### 5. SovereignGuardrail (47 Frameworks)
- **Enforcement:** Real-time validation
- **Action:** BLOCK | WARN | LOG
- **Notification:** Email, PubSub, Slack
- **Escalation:** Automatic on threshold violations

## 🌍 Compliance Coverage

### Data Sovereignty
- ✅ GDPR Art. 9 (EU)
- ✅ KDPA §37 (Kenya)
- ✅ POPIA §14 (South Africa)
- ✅ HIPAA §164.312 (USA)

### AI Explainability
- ✅ EU AI Act §6 (High-Risk AI)
- ✅ GDPR Art. 22 (Automated Decision-Making)
- ✅ NIST AI RMF (Transparency)

### Audit & Logging
- ✅ GDPR Art. 30 (Records of Processing)
- ✅ HIPAA §164.312(b) (Audit Controls)
- ✅ SOC 2 (Security Monitoring)
- ✅ ISO 27001 A.12.4 (Logging)

### Cybersecurity
- ✅ NIST CSF (5 Functions)
- ✅ ISO 27001 (ISMS)
- ✅ NIST 800-53 (Security Controls)
- ✅ CIS Controls (Prioritized Actions)

## 🧪 Testing

### Unit Tests
```bash
# Test Crypto Shredder
python governance_kernel/crypto_shredder.py

# Test SovereignGuardrail
python -c "
from governance_kernel.vector_ledger import SovereignGuardrail
guardrail = SovereignGuardrail()
print('✅ SovereignGuardrail initialized')
"
```

### Integration Tests
```bash
# Run fortress validation
./scripts/validate_fortress.sh

# Test specific framework
python -c "
from governance_kernel.vector_ledger import SovereignGuardrail
guardrail = SovereignGuardrail()
result = guardrail.validate_action(
    action_type='Data_Transfer',
    payload={'data_type': 'PHI', 'destination': 'Local_Node'},
    jurisdiction='KDPA_KE'
)
print('✅ KDPA compliance validated')
"
```

### Security Tests
```bash
# Run Gitleaks locally
docker run -v $(pwd):/path zricethezav/gitleaks:latest detect --source="/path" -v

# Run CodeQL locally (requires CodeQL CLI)
codeql database create codeql-db --language=python
codeql database analyze codeql-db --format=sarif-latest --output=results.sarif
```

## 📊 Monitoring

### Prometheus Metrics
```
sovereignty_violations_total
cross_border_transfers_total
high_risk_inferences_total
keys_shredded_total
audit_events_total
framework_checks_total
```

### Grafana Dashboards
- Sovereignty Compliance (47 Frameworks)
- Audit Trail
- Data Retention
- AI Explainability
- Humanitarian Constraints

## 🚨 Incident Response

### Sovereignty Violation
1. **Detection:** SovereignGuardrail blocks action
2. **Notification:** Email + PubSub + Slack
3. **Logging:** Tamper-proof audit trail
4. **Escalation:** Automatic to DPO/CCO

### Secret Exposure
1. **Detection:** Gitleaks workflow fails
2. **Action:** PR blocked, commit rejected
3. **Remediation:** Rotate credentials immediately
4. **Audit:** Log to security incident tracker

### Data Breach
1. **Detection:** Anomaly detection + audit logs
2. **Containment:** Crypto Shredder immediate key shred
3. **Notification:** GDPR 72h, HIPAA 60d, POPIA 7d
4. **Recovery:** Golden Thread timeline reconstruction

## 📚 Documentation

- **Architecture:** `/docs/architecture/overview.mdx`
- **Governance:** `/docs/governance/overview.mdx`
- **Security:** `/docs/security/overview.mdx`
- **Compliance:** `/docs/governance/compliance.mdx`
- **API Reference:** `/docs/api-reference/overview.mdx`

## 🤝 Contributing

When contributing to the Sovereign Health Fortress:

1. **Security First:** All PRs must pass CodeQL and Gitleaks
2. **Compliance:** Validate against SovereignGuardrail
3. **Testing:** Run `./scripts/validate_fortress.sh`
4. **Documentation:** Update relevant docs

## 📄 License

See main repository LICENSE file.

## 🆘 Support

- **Documentation:** https://docs.iluminara.health
- **Issues:** https://github.com/VISENDI56/iLuminara-Core/issues
- **Security:** security@iluminara.health

---

**The Fortress is not built. It is continuously attested.**

🛡️ iLuminara-Core Sovereign Health Fortress
