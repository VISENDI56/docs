# iLuminara-Core: Sovereign Health Fortress Implementation Files

This directory contains all the implementation files for deploying the complete iLuminara-Core security and integration stack.

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
│   ├── crypto_shredder.py          # IP-02: Data dissolution
│   └── quantum_law_nexus.py        # 45+ global legal frameworks
├── cloud_oracle/
│   └── vertex_ai_shap.py           # Vertex AI + SHAP integration
├── api/
│   └── bio_interface.py            # Bio-Interface REST API
├── config/
│   └── sovereign_guardrail.yaml    # Sovereignty configuration
├── scripts/
│   ├── validate_fortress.sh        # Fortress validation
│   └── setup_branch_protection.sh  # GitHub branch protection
├── requirements.txt                # Python dependencies
└── README.md                       # This file
```

## 🚀 Quick Start

### Step 1: Copy Files to Repository

```bash
# Navigate to your iLuminara-Core repository
cd /path/to/iLuminara-Core

# Copy all files from repository-files/
cp -r /path/to/docs/repository-files/* .

# Make scripts executable
chmod +x scripts/*.sh
```

### Step 2: Install Dependencies

```bash
# Install Python dependencies
pip install -r requirements.txt

# Or use virtual environment (recommended)
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### Step 3: Configure Environment

```bash
# Set required environment variables
export NODE_ID=JOR-47
export JURISDICTION=KDPA_KE
export GOOGLE_CLOUD_PROJECT=your-project-id
export GCP_REGION=us-central1

# Optional: Enable tamper-proof audit
export ENABLE_TAMPER_PROOF_AUDIT=true
```

### Step 4: Validate Installation

```bash
# Run fortress validation
./scripts/validate_fortress.sh
```

### Step 5: Setup GitHub Security

```bash
# Authenticate with GitHub CLI
gh auth refresh -s workflow,repo,write:packages,admin:repo_hook

# Setup branch protection
./scripts/setup_branch_protection.sh
```

## 📦 Component Overview

### Security Audit Layer

**CodeQL Workflow** (`.github/workflows/codeql.yml`)
- SAST security scanning
- Runs on push, PR, and weekly schedule
- Compliance: GDPR Art. 32, ISO 27001 A.12.6

**Gitleaks Workflow** (`.github/workflows/gitleaks.yml`)
- Secret detection and scanning
- Runs daily at 2 AM UTC
- Compliance: NIST SP 800-53 IA-5, HIPAA §164.312

**Dependabot** (`.github/dependabot.yml`)
- Daily security updates for Python, npm, Docker, GitHub Actions
- Automatic vulnerability patching

### Governance Kernel

**Crypto Shredder** (`governance_kernel/crypto_shredder.py`)
- IP-02: Data is dissolved, not deleted
- Ephemeral key encryption with auto-shred
- Compliance: GDPR Art. 17, HIPAA §164.530(j), NIST SP 800-88

**Quantum-Law Nexus** (`governance_kernel/quantum_law_nexus.py`)
- 45+ global legal frameworks
- Dynamic jurisdiction selection
- Quantum superposition of legal states

### Cloud Oracle

**Vertex AI + SHAP** (`cloud_oracle/vertex_ai_shap.py`)
- Right to Explanation for high-risk AI
- SHAP explainability integration
- Compliance: EU AI Act §6, GDPR Art. 22, FDA CDSS

### Bio-Interface

**REST API** (`api/bio_interface.py`)
- Golden Thread protocol integration
- CBS + EMR data fusion
- Verification scoring (CONFIRMED | PROBABLE | POSSIBLE | UNVERIFIED)

### Configuration

**SovereignGuardrail Config** (`config/sovereign_guardrail.yaml`)
- Jurisdiction configuration
- Data sovereignty rules
- Retention policies
- Audit settings

## 🛡️ The Nuclear IP Stack

| Component | Protocol | Status |
|-----------|----------|--------|
| **IP-02** | Crypto Shredder | ✅ Active |
| **IP-03** | Acorn Protocol | ⚠️ Requires Hardware |
| **IP-04** | Silent Flux | ⚠️ Requires Integration |
| **IP-05** | Golden Thread | ✅ Active |
| **IP-06** | 5DM Bridge | ⚠️ Requires Mobile Network |

## 📊 Compliance Coverage

### TIER 1: Data Protection (14 frameworks)
- GDPR, KDPA, POPIA, HIPAA, HITECH, PIPEDA, CCPA, CPRA
- NIST CSF, ISO 27001, ISO 27701, SOC 2, LGPD, NDPA

### TIER 2: AI Governance (8 frameworks)
- EU AI Act, FDA CDSS, NIST AI RMF, IEEE 7000
- ISO 42001, OECD AI, UNESCO AI, WHO AI for Health

### TIER 3: Global Health Security (7 frameworks)
- WHO IHR (2005), WHO IHR (2025), Geneva Convention
- UN CRC, Sphere Standards, ICRC Medical, CHS

### TIER 4: African Data Sovereignty (6 frameworks)
- Malabo Convention, ECOWAS Data, SADC Model
- NDPA (Nigeria), DPA (Ghana), PDPA (Uganda)

### TIER 5: ESG & Reporting (5 frameworks)
- ISSB S1, ISSB S2/IFRS S2, GRI Standards, TCFD, Paris Agreement

### TIER 6: Regional & Emerging (5 frameworks)
- LGPD (Brazil), PIPL (China), PDPA (Singapore)
- APPI (Japan), PDPA (Thailand)

## 🔧 Configuration

### Environment Variables

```bash
# Core Configuration
export NODE_ID=JOR-47
export JURISDICTION=KDPA_KE
export API_HOST=0.0.0.0
export API_PORT=8080

# GCP Configuration
export GOOGLE_CLOUD_PROJECT=your-project-id
export GCP_REGION=us-central1

# Governance Configuration
export ENABLE_TAMPER_PROOF_AUDIT=true
export RETENTION_MAX_DAYS=1825
export AUDIT_LOG_LEVEL=INFO

# Sovereignty Settings
export DATA_SOVEREIGNTY_REQUIRED=true
export REQUIRES_EXPLICIT_CONSENT=true

# AI Agents Configuration
export ENABLE_OFFLINE_MODE=true
export SYNC_INTERVAL_SECONDS=300
export FEDERATED_LEARNING_EPSILON=1.0
```

### Jurisdiction Configuration

Edit `config/sovereign_guardrail.yaml`:

```yaml
jurisdiction:
  primary: "KDPA_KE"  # Your primary jurisdiction
  secondary:
    - "GDPR_EU"
    - "POPIA_ZA"
    - "HIPAA_US"
```

## 🧪 Testing

```bash
# Run all tests
pytest tests/

# Run specific test suite
pytest tests/test_crypto_shredder.py
pytest tests/test_quantum_law_nexus.py
pytest tests/test_vertex_ai_shap.py

# Run with coverage
pytest --cov=governance_kernel --cov=cloud_oracle --cov=api
```

## 📝 Usage Examples

### Crypto Shredder

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
```

### Quantum-Law Nexus

```python
from governance_kernel.quantum_law_nexus import QuantumLawNexus

nexus = QuantumLawNexus()

# Get applicable frameworks
applicable = nexus.get_applicable_frameworks(
    data_type="PHI",
    operation="inference",
    location="Kenya"
)

# Get compliance rules
rules = nexus.get_compliance_rules(JurisdictionFramework.EU_AI_ACT)
```

### Vertex AI + SHAP

```python
from cloud_oracle.vertex_ai_shap import VertexAIExplainer

explainer = VertexAIExplainer(
    project_id="iluminara-core",
    jurisdiction="EU_AI_ACT"
)

# Generate explanation
result = explainer.explain_prediction(
    model_endpoint="projects/123/locations/us-central1/endpoints/456",
    input_data={"fever": 1.0, "diarrhea": 1.0},
    feature_names=["fever", "diarrhea"]
)
```

### Bio-Interface API

```bash
# Submit CBS report
curl -X POST http://localhost:8080/api/v1/cbs/report \
  -H "Content-Type: application/json" \
  -d '{
    "location": {"lat": 0.0512, "lng": 40.3129},
    "symptoms": ["fever", "diarrhea"],
    "severity": 8,
    "chv_id": "CHV_AMINA_HASSAN"
  }'

# Submit EMR record
curl -X POST http://localhost:8080/api/v1/emr/record \
  -H "Content-Type: application/json" \
  -d '{
    "patient_id": "PAT_12345",
    "location": {"lat": 0.0512, "lng": 40.3129},
    "diagnosis": "cholera",
    "facility_id": "DADAAB_CLINIC"
  }'
```

## 🚨 Troubleshooting

### CodeQL Workflow Fails

```bash
# Check workflow logs
gh run list --workflow=codeql.yml
gh run view <run-id> --log

# Re-run failed workflow
gh run rerun <run-id>
```

### Gitleaks Detects Secrets

```bash
# View detected secrets
gh run view <run-id> --log

# Add to .gitleaks.toml allowlist if false positive
```

### Branch Protection Issues

```bash
# Check current protection status
gh api repos/:owner/:repo/branches/main/protection

# Re-run setup script
./scripts/setup_branch_protection.sh
```

## 📚 Documentation

Full documentation available at: https://docs.iluminara.health

- [Architecture Overview](https://docs.iluminara.health/architecture/overview)
- [Governance Kernel](https://docs.iluminara.health/governance/overview)
- [Security Stack](https://docs.iluminara.health/security/overview)
- [API Reference](https://docs.iluminara.health/api-reference/overview)
- [Deployment Guide](https://docs.iluminara.health/deployment/overview)

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Run tests and validation
5. Submit a pull request

All contributions must pass:
- CodeQL security scanning
- Gitleaks secret detection
- Fortress validation
- Unit tests

## 📄 License

Copyright © 2025 VISENDI56. All rights reserved.

## 🛡️ Mission

> Transform preventable suffering from statistical inevitability to historical anomaly.

The Sovereign Health Fortress is now built. Deploy with dignity.
