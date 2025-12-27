# iLuminara-Core: Sovereign Health Fortress Implementation Files

This directory contains all the implementation files for the **Sovereign Health Fortress** security and integration stack.

## 🛡️ The Nuclear IP Stack

| Component | Protocol | Status |
|-----------|----------|--------|
| **Security Audit** | Gitleaks + CodeQL | ✅ Ready |
| **Data Lifecycle** | IP-02 Crypto Shredder | ✅ Ready |
| **Intelligence** | IP-04 Silent Flux | ⚠️ Requires Integration |
| **Connectivity** | IP-06 5DM Bridge | ⚠️ Requires Mobile Network |

## 📁 Directory Structure

```
repository-files/
├── .github/
│   ├── workflows/
│   │   ├── codeql.yml              # SAST security scanning
│   │   └── gitleaks.yml            # Secret detection
│   └── dependabot.yml              # Daily security updates
├── .gitleaks.toml                  # Secret scanning rules
├── config/
│   └── sovereign_guardrail.yaml    # Sovereignty configuration
├── governance_kernel/
│   └── crypto_shredder.py          # IP-02: Data dissolution
├── integrations/
│   ├── vertex_ai_shap.py           # Vertex AI + SHAP explainability
│   └── bio_interface_api.py        # Mobile health apps REST API
└── scripts/
    └── validate_fortress.sh        # Fortress validation script
```

## 🚀 Quick Start

### Step 1: Copy files to your repository

```bash
# Navigate to your iLuminara-Core repository
cd /path/to/iLuminara-Core

# Copy all files
cp -r /path/to/docs/repository-files/* .
```

### Step 2: Make scripts executable

```bash
chmod +x scripts/validate_fortress.sh
```

### Step 3: Install dependencies

```bash
pip install cryptography flask flask-cors shap google-cloud-aiplatform
```

### Step 4: Validate the fortress

```bash
./scripts/validate_fortress.sh
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
- GitHub Actions: Weekly on Monday
- Docker: Weekly on Tuesday

## 🔥 IP-02: Crypto Shredder

**File:** `governance_kernel/crypto_shredder.py`

Data is not deleted; it is cryptographically dissolved.

### Basic Usage

```python
from governance_kernel.crypto_shredder import CryptoShredder, RetentionPolicy, SovereigntyZone

# Initialize
shredder = CryptoShredder(
    sovereignty_zone=SovereigntyZone.KENYA,
    enable_audit=True
)

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

### Retention Policies

| Policy | Duration | Use Case |
|--------|----------|----------|
| `HOT` | 180 days | Active operational data |
| `WARM` | 365 days | Compliance minimum (HIPAA) |
| `COLD` | 1825 days | Legal hold maximum (GDPR Art. 17) |
| `ETERNAL` | Never | Requires explicit justification |

## 🧠 Vertex AI + SHAP Integration

**File:** `integrations/vertex_ai_shap.py`

Every high-risk clinical inference (confidence > 0.7) automatically triggers SHAP analysis.

### Basic Usage

```python
from integrations.vertex_ai_shap import VertexAIExplainer

# Initialize
explainer = VertexAIExplainer(
    project_id="iluminara-health",
    location="us-central1",
    high_risk_threshold=0.7
)

# Make prediction with automatic explanation
result = explainer.predict_with_explanation(
    endpoint_id="projects/123/locations/us-central1/endpoints/456",
    instances=[{"fever": 1.0, "chills": 1.0, "headache": 0.8}],
    feature_names=["fever", "chills", "headache"]
)

# Generate clinical report
report = explainer.generate_explanation_report(
    result=result,
    patient_id="PAT_12345"
)
```

### Compliance

- EU AI Act §6 (High-Risk AI Systems)
- GDPR Art. 22 (Right to Explanation)
- HIPAA §164.312(b) (Audit Controls)

## 📱 Bio-Interface REST API

**File:** `integrations/bio_interface_api.py`

Mobile health apps integration with Golden Thread protocol.

### Start the API

```bash
python integrations/bio_interface_api.py
```

### Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/health` | GET | Health check |
| `/api/v1/cbs/submit` | POST | Submit CBS signal |
| `/api/v1/emr/submit` | POST | Submit EMR record |
| `/api/v1/golden-thread/fuse` | POST | Fuse data streams |
| `/api/v1/verification/status` | GET | Get verification status |
| `/api/v1/consent/validate` | POST | Validate consent |

### Example: Submit CBS Signal

```bash
curl -X POST http://localhost:8080/api/v1/cbs/submit \
  -H "Content-Type: application/json" \
  -d '{
    "chv_id": "CHV_AMINA_HASSAN",
    "location": {"lat": 0.0512, "lng": 40.3129},
    "symptom": "fever",
    "severity": 7,
    "timestamp": "2025-12-26T10:00:00Z",
    "consent_token": "VALID_TOKEN",
    "jurisdiction": "KDPA_KE"
  }'
```

## ⚙️ SovereignGuardrail Configuration

**File:** `config/sovereign_guardrail.yaml`

Configure sovereignty constraints for your jurisdiction.

### Key Sections

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
    allowed_zones:
      - "africa-south1"
      - "europe-west1"
    enforcement_level: "STRICT"

audit:
  enabled: true
  tamper_proof: true
  storage:
    backend: "Cloud_Spanner"
    retention_days: 2555  # 7 years (HIPAA)
```

## 🔍 Fortress Validation

**File:** `scripts/validate_fortress.sh`

Validates the complete security stack.

### Run Validation

```bash
./scripts/validate_fortress.sh
```

### Validation Phases

1. **Security Audit Layer** - CodeQL, Gitleaks, Dependabot
2. **Governance Kernel** - SovereignGuardrail, Crypto Shredder
3. **Edge Node & AI Agents** - FRENASA, Golden Thread
4. **Cloud Oracle** - API, Dashboard, Deployment
5. **Python Dependencies** - Critical packages
6. **Environment Configuration** - Required variables
7. **Nuclear IP Stack Status** - IP-02 through IP-06

### Expected Output

```
╔════════════════════════════════════════════════════════════╗
║     iLuminara-Core Sovereign Health Fortress Validator     ║
╚════════════════════════════════════════════════════════════╝

🔍 Checking CodeQL workflow... ✓ OPERATIONAL
🔍 Checking Gitleaks workflow... ✓ OPERATIONAL
🔍 Checking Crypto Shredder... ✓ OPERATIONAL
⚡ IP-02 Crypto Shredder... ✓ ACTIVE
⚡ IP-05 Golden Thread... ✓ ACTIVE

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

## 🚢 Deployment

### Local Development

```bash
# Install dependencies
pip install -r requirements.txt

# Set environment variables
export NODE_ID=JOR-47
export JURISDICTION=KDPA_KE
export GOOGLE_CLOUD_PROJECT=iluminara-health

# Validate fortress
./scripts/validate_fortress.sh

# Start services
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

## 🔒 Security Considerations

<details>
<summary><strong>Data Sovereignty</strong></summary>

Ensure PHI never leaves sovereign territory. Configure jurisdiction-specific rules in `config/sovereign_guardrail.yaml`.
</details>

<details>
<summary><strong>Network Security</strong></summary>

Use VPN or private networking for edge-to-cloud communication. Enable TLS 1.3 for all endpoints.
</details>

<details>
<summary><strong>Access Control</strong></summary>

Implement IAM roles for GCP services. Use service accounts with minimal permissions.
</details>

<details>
<summary><strong>Audit Logging</strong></summary>

Enable tamper-proof audit trail. Configure Cloud KMS for cryptographic signatures.
</details>

## 📚 Documentation

Full documentation available at: https://docs.iluminara.health

- [Architecture Overview](https://docs.iluminara.health/architecture/overview)
- [Governance Kernel](https://docs.iluminara.health/governance/overview)
- [Security Stack](https://docs.iluminara.health/security/overview)
- [Vertex AI + SHAP](https://docs.iluminara.health/integrations/vertex-ai-shap)
- [Bio-Interface API](https://docs.iluminara.health/integrations/bio-interface)

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Run validation: `./scripts/validate_fortress.sh`
4. Submit a pull request

All PRs must pass:
- CodeQL security scanning
- Gitleaks secret detection
- Fortress validation

## 📄 License

See LICENSE file in the main repository.

## 🆘 Support

- GitHub Issues: https://github.com/VISENDI56/iLuminara-Core/issues
- Documentation: https://docs.iluminara.health
- Email: support@iluminara.health

---

**The Fortress is not built. It is continuously attested.**

Transform preventable suffering from statistical inevitability to historical anomaly.
