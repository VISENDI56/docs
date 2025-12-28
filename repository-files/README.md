# iLuminara-Core: Sovereign Health Fortress Implementation Files

This directory contains all the files needed to implement the complete **Sovereign Health Fortress** security and integration stack for iLuminara-Core.

## 🛡️ The Fortress Stack

| Component | File | Purpose |
|-----------|------|---------|
| **Security Audit** | `.github/workflows/codeql.yml` | SAST security scanning |
| **Secret Detection** | `.github/workflows/gitleaks.yml` | Secret scanning |
| **Secret Config** | `.gitleaks.toml` | Gitleaks rules |
| **Dependency Updates** | `.github/dependabot.yml` | Daily security updates |
| **Crypto Shredder (IP-02)** | `governance_kernel/crypto_shredder.py` | Data dissolution |
| **SovereignGuardrail Config** | `config/sovereign_guardrail.yaml` | Compliance configuration |
| **Fortress Validator** | `scripts/validate_fortress.sh` | Complete stack validation |
| **Vertex AI + SHAP** | `integrations/vertex_ai_shap.py` | Explainable AI |
| **Bio-Interface API** | `integrations/bio_interface_api.py` | Mobile health integration |

## 📋 Installation Instructions

### Step 1: Copy Files to Your Repository

```bash
# Navigate to your iLuminara-Core repository
cd /path/to/iLuminara-Core

# Copy all files from this directory
cp -r repository-files/.github .
cp -r repository-files/governance_kernel .
cp -r repository-files/config .
cp -r repository-files/scripts .
cp -r repository-files/integrations .
cp repository-files/.gitleaks.toml .
```

### Step 2: Set Permissions

```bash
# Make scripts executable
chmod +x scripts/validate_fortress.sh
chmod +x launch_all_services.sh
chmod +x deploy_gcp_prototype.sh
```

### Step 3: Install Dependencies

```bash
# Install Python dependencies
pip install cryptography flask flask-cors google-cloud-aiplatform shap

# Or add to requirements.txt
cat >> requirements.txt << EOF
cryptography>=41.0.0
flask>=3.0.0
flask-cors>=4.0.0
google-cloud-aiplatform>=1.38.0
shap>=0.43.0
EOF

pip install -r requirements.txt
```

### Step 4: Configure Environment

```bash
# Set environment variables
export NODE_ID=JOR-47
export JURISDICTION=KDPA_KE
export GOOGLE_CLOUD_PROJECT=your-project-id
export GCP_REGION=us-central1
export ENABLE_TAMPER_PROOF_AUDIT=true
```

### Step 5: Validate Installation

```bash
# Run fortress validation
./scripts/validate_fortress.sh
```

Expected output:
```
🛡️  FORTRESS STATUS: OPERATIONAL
✓  All critical components validated
✓  Security audit layer active
✓  Governance kernel operational
✓  Nuclear IP stack initialized

The Sovereign Health Fortress is ready for deployment.
```

## 🔐 Security Workflows

### CodeQL (SAST Scanning)

**File:** `.github/workflows/codeql.yml`

**Triggers:**
- Push to `main` or `develop`
- Pull requests to `main`
- Weekly schedule (Sunday midnight UTC)

**Compliance:**
- GDPR Art. 32 (Security of Processing)
- ISO 27001 A.12.6 (Technical Vulnerability Management)

### Gitleaks (Secret Scanning)

**File:** `.github/workflows/gitleaks.yml`

**Triggers:**
- Push to `main` or `develop`
- Pull requests to `main`
- Daily schedule (2 AM UTC)

**Compliance:**
- NIST SP 800-53 (IA-5 Authenticator Management)
- HIPAA §164.312(a)(2)(i) (Unique User Identification)

### Dependabot (Security Updates)

**File:** `.github/dependabot.yml`

**Schedule:**
- Python dependencies: Daily at 2 AM UTC
- GitHub Actions: Weekly (Monday)
- Docker: Weekly (Tuesday)
- npm: Daily at 2 AM UTC

## ⚡ Nuclear IP Stack

### IP-02: Crypto Shredder

**File:** `governance_kernel/crypto_shredder.py`

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

**Compliance:**
- GDPR Art. 17 (Right to Erasure)
- HIPAA §164.530(j) (Documentation)
- NIST SP 800-88 (Media Sanitization)

### IP-05: Golden Thread

Already implemented in `edge_node/sync_protocol/golden_thread.py`

**Integration:** Automatically used by Bio-Interface API

## 🔧 Configuration

### SovereignGuardrail Configuration

**File:** `config/sovereign_guardrail.yaml`

**Key settings:**
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
    enforcement_level: "STRICT"

audit:
  enabled: true
  tamper_proof: true
  retention_days: 2555  # 7 years (HIPAA)
```

## 🤖 Integrations

### Vertex AI + SHAP

**File:** `integrations/vertex_ai_shap.py`

**Purpose:** Provides explainable AI for high-risk clinical decisions

**Usage:**
```python
from integrations.vertex_ai_shap import OutbreakRiskPredictor

predictor = OutbreakRiskPredictor(
    project_id="iluminara-core",
    model_endpoint="projects/123/locations/us-central1/endpoints/456"
)

result = predictor.predict_outbreak_risk(
    case_count=150,
    population=100000,
    attack_rate=0.0015,
    r_effective=2.5,
    days_since_first_case=14,
    location="Dadaab Refugee Camp"
)

# Check compliance
if result["compliance_validation"]["compliant"]:
    print("✅ Compliant with EU AI Act §6 and GDPR Art. 22")
```

**Compliance:**
- EU AI Act §6 (High-Risk AI)
- GDPR Art. 22 (Right to Explanation)

### Bio-Interface REST API

**File:** `integrations/bio_interface_api.py`

**Purpose:** Mobile health apps integration with Golden Thread protocol

**Start server:**
```bash
python integrations/bio_interface_api.py
```

**Test endpoint:**
```bash
curl -X POST http://localhost:8080/api/v1/submit-cbs-report \
  -H "Content-Type: application/json" \
  -d '{
    "patient_id": "PATIENT_12345",
    "location": {"lat": 0.0512, "lng": 40.3129},
    "symptoms": ["fever", "cough"],
    "severity": 7,
    "source": "CHV_MOBILE_APP",
    "consent_token": "VALID_TOKEN"
  }'
```

**Compliance:**
- GDPR Art. 9 (Special Categories)
- HIPAA §164.312 (Technical Safeguards)
- Kenya DPA §37 (Transfer Restrictions)

## 🚀 Deployment

### Local Development

```bash
# Validate fortress
./scripts/validate_fortress.sh

# Launch all services
./launch_all_services.sh
```

### Google Cloud Platform

```bash
# Deploy to GCP
./deploy_gcp_prototype.sh
```

### Docker

```bash
# Build and run
docker-compose up -d
```

## ✅ Validation Checklist

Run this checklist after installation:

- [ ] CodeQL workflow exists (`.github/workflows/codeql.yml`)
- [ ] Gitleaks workflow exists (`.github/workflows/gitleaks.yml`)
- [ ] Gitleaks config exists (`.gitleaks.toml`)
- [ ] Dependabot config exists (`.github/dependabot.yml`)
- [ ] Crypto Shredder implemented (`governance_kernel/crypto_shredder.py`)
- [ ] SovereignGuardrail config exists (`config/sovereign_guardrail.yaml`)
- [ ] Validation script executable (`scripts/validate_fortress.sh`)
- [ ] Vertex AI + SHAP integration (`integrations/vertex_ai_shap.py`)
- [ ] Bio-Interface API (`integrations/bio_interface_api.py`)
- [ ] Environment variables configured
- [ ] Dependencies installed
- [ ] Fortress validation passes

## 📊 Monitoring

### Prometheus Metrics

The fortress exposes these metrics:

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

## 🆘 Troubleshooting

### Validation Fails

```bash
# Check missing files
ls -la .github/workflows/
ls -la governance_kernel/
ls -la config/
ls -la scripts/
ls -la integrations/

# Check permissions
ls -l scripts/validate_fortress.sh

# Re-run validation with verbose output
bash -x scripts/validate_fortress.sh
```

### Import Errors

```bash
# Verify Python path
export PYTHONPATH="${PYTHONPATH}:$(pwd)"

# Reinstall dependencies
pip install -r requirements.txt --force-reinstall
```

### Sovereignty Violations

Check logs:
```bash
tail -f logs/audit.log
tail -f governance_kernel/keys/audit.jsonl
```

## 📚 Documentation

Full documentation available at: https://docs.iluminara.health

- [Security Stack](/security/overview)
- [Governance Kernel](/governance/overview)
- [Vertex AI + SHAP](/integrations/vertex-ai-shap)
- [Bio-Interface API](/integrations/bio-interface)

## 🤝 Support

For issues or questions:
- GitHub Issues: https://github.com/VISENDI56/iLuminara-Core/issues
- Documentation: https://docs.iluminara.health

## 📄 License

See LICENSE file in the main repository.

---

**The Fortress is now built. Your Agent AI has transitioned iLuminara from a repository to a Sovereign Architecture.**

🛡️ **FORTRESS STATUS: OPERATIONAL**
