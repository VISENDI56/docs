# iLuminara-Core Repository Files
## Sovereign Health Fortress Implementation

This directory contains all the files needed to implement the complete iLuminara-Core security and integration stack in your repository.

---

## 📁 Directory Structure

```
repository-files/
├── .github/
│   ├── workflows/
│   │   ├── codeql.yml              # SAST security scanning
│   │   └── gitleaks.yml            # Secret detection
│   └── dependabot.yml              # Daily security updates
├── .gitleaks.toml                  # Gitleaks configuration
├── governance_kernel/
│   └── crypto_shredder.py          # IP-02: Data dissolution
├── cloud_oracle/
│   └── vertex_ai_shap.py           # Vertex AI + SHAP integration
├── edge_node/
│   └── bio_interface_api.py        # Mobile health app API
├── config/
│   └── sovereign_guardrail.yaml    # Compliance configuration
├── scripts/
│   ├── validate_fortress.sh        # Fortress validation
│   └── setup_branch_protection.sh  # GitHub protection setup
├── IMPLEMENTATION_GUIDE.md         # Step-by-step guide
└── README.md                       # This file
```

---

## 🚀 Quick Start

### 1. Copy Files to Your Repository

```bash
# From your iLuminara-Core repository root
cp -r /path/to/repository-files/.github .
cp -r /path/to/repository-files/governance_kernel .
cp -r /path/to/repository-files/cloud_oracle .
cp -r /path/to/repository-files/edge_node .
cp -r /path/to/repository-files/config .
cp -r /path/to/repository-files/scripts .
cp /path/to/repository-files/.gitleaks.toml .
```

### 2. Set Up Branch Protection

```bash
chmod +x scripts/setup_branch_protection.sh
./scripts/setup_branch_protection.sh
```

### 3. Validate Installation

```bash
chmod +x scripts/validate_fortress.sh
./scripts/validate_fortress.sh
```

### 4. Commit and Push

```bash
git add .
git commit -m "feat: integrate Sovereign Health Fortress"
git push origin main
```

---

## 📋 File Descriptions

### Security Audit Layer

#### `.github/workflows/codeql.yml`
**Purpose:** SAST security scanning with CodeQL  
**Runs:** On push, PR, weekly schedule  
**Compliance:** GDPR Art. 32, ISO 27001 A.12.6  
**Languages:** Python, JavaScript  

#### `.github/workflows/gitleaks.yml`
**Purpose:** Secret scanning and detection  
**Runs:** On push, PR, daily at 2 AM UTC  
**Compliance:** NIST SP 800-53 IA-5, HIPAA §164.312(a)(2)(i)  
**Features:** Custom sovereignty rules, SARIF upload  

#### `.github/dependabot.yml`
**Purpose:** Automated dependency updates  
**Schedule:** Daily for pip/npm, weekly for Docker/Actions  
**Groups:** Security, google-cloud, ai-ml  

#### `.gitleaks.toml`
**Purpose:** Gitleaks configuration  
**Features:**
- Detects GCP, AWS, GitHub tokens
- Blocks AWS keys (sovereignty violation)
- Allowlist for test files
- Custom rules for health data

### Governance Kernel

#### `governance_kernel/crypto_shredder.py`
**Purpose:** IP-02 Crypto Shredder implementation  
**Features:**
- Ephemeral key encryption (AES-256-GCM)
- Automatic key shredding after retention
- Sovereignty zone enforcement
- Tamper-proof audit trail

**Compliance:**
- GDPR Art. 17 (Right to Erasure)
- HIPAA §164.530(j) (Documentation)
- NIST SP 800-88 (Media Sanitization)

**Usage:**
```python
from governance_kernel.crypto_shredder import CryptoShredder, RetentionPolicy

shredder = CryptoShredder(sovereignty_zone=SovereigntyZone.KENYA)
encrypted_data, key_id = shredder.encrypt_with_ephemeral_key(
    data=patient_record,
    retention_policy=RetentionPolicy.HOT
)
```

#### `config/sovereign_guardrail.yaml`
**Purpose:** SovereignGuardrail configuration  
**Features:**
- 14 global legal frameworks
- Data sovereignty rules
- Cross-border transfer controls
- Retention policies
- Audit configuration

**Configure:**
```yaml
jurisdiction:
  primary: "KDPA_KE"  # Change to your jurisdiction
```

### Integrations

#### `cloud_oracle/vertex_ai_shap.py`
**Purpose:** Vertex AI + SHAP explainability  
**Features:**
- Right to Explanation (EU AI Act §6)
- SHAP feature importance
- Evidence chain generation
- Automatic compliance validation
- BigQuery audit logging

**Compliance:**
- EU AI Act §6 (High-Risk AI)
- GDPR Art. 22 (Right to Explanation)
- HIPAA §164.524 (Right of Access)

**Usage:**
```python
from cloud_oracle.vertex_ai_shap import VertexAIExplainer

explainer = VertexAIExplainer(
    project_id="iluminara-core",
    model_name="outbreak-forecaster"
)

result = explainer.predict_with_explanation(
    features={"case_count": 45.0, "attack_rate": 0.04},
    patient_id="PAT_12345"
)
```

#### `edge_node/bio_interface_api.py`
**Purpose:** Mobile health app REST API  
**Features:**
- CBS signal submission from CHVs
- EMR record integration
- Golden Thread automatic fusion
- Offline batch submission
- Sovereignty validation
- Crypto Shredder encryption

**Compliance:**
- GDPR Art. 6 (Lawfulness)
- HIPAA §164.312 (Technical Safeguards)
- KDPA §37 (Transfer Restrictions)

**Usage:**
```bash
export NODE_ID=BIO-INTERFACE-01
export JURISDICTION=KDPA_KE
python edge_node/bio_interface_api.py
```

### Scripts

#### `scripts/validate_fortress.sh`
**Purpose:** Complete fortress validation  
**Validates:**
1. Security Audit Layer
2. Governance Kernel
3. Edge Node & AI Agents
4. Cloud Oracle
5. Python Dependencies
6. Environment Configuration
7. Nuclear IP Stack Status

**Usage:**
```bash
chmod +x scripts/validate_fortress.sh
./scripts/validate_fortress.sh
```

#### `scripts/setup_branch_protection.sh`
**Purpose:** GitHub branch protection setup  
**Configures:**
- Require PR reviews (1 approval)
- Require status checks (CodeQL, Gitleaks)
- Enforce for administrators
- Block force pushes and deletions
- Enable secret scanning push protection

**Usage:**
```bash
chmod +x scripts/setup_branch_protection.sh
./scripts/setup_branch_protection.sh
```

---

## 🔐 Security Features

### The 10/10 Security Stack

| Component | File | Status |
|-----------|------|--------|
| **CodeQL SAST** | `.github/workflows/codeql.yml` | ✅ Active |
| **Gitleaks Secrets** | `.github/workflows/gitleaks.yml` | ✅ Active |
| **Dependabot** | `.github/dependabot.yml` | ✅ Active |
| **Crypto Shredder** | `governance_kernel/crypto_shredder.py` | ✅ Active |
| **SovereignGuardrail** | `config/sovereign_guardrail.yaml` | ✅ Active |
| **Vertex AI + SHAP** | `cloud_oracle/vertex_ai_shap.py` | ✅ Active |
| **Bio-Interface** | `edge_node/bio_interface_api.py` | ✅ Active |
| **Branch Protection** | `scripts/setup_branch_protection.sh` | ✅ Active |

---

## 📊 Compliance Coverage

### 14 Global Legal Frameworks

✅ GDPR (EU)  
✅ KDPA (Kenya)  
✅ HIPAA (USA)  
✅ HITECH (USA)  
✅ PIPEDA (Canada)  
✅ POPIA (South Africa)  
✅ CCPA (California)  
✅ NIST CSF (USA)  
✅ ISO 27001 (Global)  
✅ SOC 2 (USA)  
✅ EU AI Act (EU)  
✅ GDPR Art. 9 (EU)  
✅ WHO IHR (Global)  
✅ Geneva Convention (Global)  

---

## 🧪 Testing

### Test Individual Components

```bash
# Test Crypto Shredder
python governance_kernel/crypto_shredder.py

# Test Vertex AI + SHAP
python cloud_oracle/vertex_ai_shap.py

# Test Bio-Interface API
python edge_node/bio_interface_api.py
```

### Test API Endpoints

```bash
# Start Bio-Interface API
python edge_node/bio_interface_api.py &

# Health check
curl http://localhost:8081/health

# Submit CBS signal
curl -X POST http://localhost:8081/api/v1/submit-cbs \
  -H "Content-Type: application/json" \
  -d '{
    "chv_id": "CHV_TEST",
    "location": {"lat": 0.05, "lng": 40.31},
    "symptom": "fever",
    "timestamp": "2025-12-25T10:00:00Z"
  }'
```

---

## 🚨 Troubleshooting

### CodeQL Workflow Fails

**Issue:** CodeQL analysis fails  
**Solution:**
```bash
# Check workflow logs
gh run list --workflow=codeql.yml

# Re-run failed workflow
gh run rerun RUN_ID
```

### Gitleaks Detects False Positive

**Issue:** Gitleaks flags test data  
**Solution:** Add to `.gitleaks.toml` allowlist:
```toml
[allowlist]
paths = [
  '''.*_test\\.py''',
  '''.*\\.example'''
]
```

### Branch Protection Blocks Push

**Issue:** Cannot push to main  
**Solution:** Create PR instead:
```bash
git checkout -b feature/my-changes
git push origin feature/my-changes
gh pr create
```

### Crypto Shredder Import Error

**Issue:** `ModuleNotFoundError: No module named 'cryptography'`  
**Solution:**
```bash
pip install cryptography
```

---

## 📚 Documentation

- **Implementation Guide:** `IMPLEMENTATION_GUIDE.md`
- **Online Docs:** https://docs.iluminara.health
- **API Reference:** https://docs.iluminara.health/api-reference
- **Security Stack:** https://docs.iluminara.health/security

---

## 🤝 Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'feat: add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open Pull Request

**Note:** All PRs must pass CodeQL and Gitleaks checks.

---

## 📄 License

This project is part of iLuminara-Core and follows the same license.

---

## 🆘 Support

- **GitHub Issues:** https://github.com/VISENDI56/iLuminara-Core/issues
- **Documentation:** https://docs.iluminara.health
- **Email:** support@iluminara.health

---

## ✅ Verification Checklist

Before deploying to production:

- [ ] All files copied to repository
- [ ] Branch protection enabled
- [ ] CodeQL workflow running
- [ ] Gitleaks workflow running
- [ ] Dependabot enabled
- [ ] Crypto Shredder tested
- [ ] SovereignGuardrail configured
- [ ] Vertex AI + SHAP deployed
- [ ] Bio-Interface API running
- [ ] Fortress validator passing
- [ ] Documentation updated

---

**The Fortress is ready. Deploy with confidence.**
