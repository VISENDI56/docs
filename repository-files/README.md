# iLuminara-Core Repository Files

This directory contains all the implementation files for the **Sovereign Health Fortress** security and integration stack.

## 📁 Directory structure

```
repository-files/
├── .github/
│   ├── workflows/
│   │   ├── codeql.yml              # SAST security scanning
│   │   └── gitleaks.yml            # Secret detection
│   └── dependabot.yml              # Daily security updates
├── .gitleaks.toml                  # Secret detection rules
├── config/
│   ├── sovereign_guardrail.yaml    # Basic configuration
│   └── sovereign_guardrail_47_frameworks.yaml  # Complete 47-framework config
├── governance_kernel/
│   └── crypto_shredder.py          # IP-02: Data dissolution
├── cloud_oracle/
│   └── vertex_ai_shap.py           # Vertex AI + SHAP integration
└── scripts/
    └── validate_fortress.sh        # Fortress validation script
```

## 🚀 Quick start

### 1. Copy files to your repository

```bash
# From this directory
cp -r .github /path/to/iLuminara-Core/
cp -r config /path/to/iLuminara-Core/
cp -r governance_kernel /path/to/iLuminara-Core/
cp -r cloud_oracle /path/to/iLuminara-Core/
cp -r scripts /path/to/iLuminara-Core/
cp .gitleaks.toml /path/to/iLuminara-Core/
```

### 2. Make scripts executable

```bash
cd /path/to/iLuminara-Core
chmod +x scripts/validate_fortress.sh
chmod +x launch_all_services.sh
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
pip install shap google-cloud-aiplatform cryptography
```

### 4. Configure environment

```bash
export NODE_ID=JOR-47
export JURISDICTION=KDPA_KE
export GOOGLE_CLOUD_PROJECT=your-project-id
export GCP_REGION=us-central1
export ENABLE_TAMPER_PROOF_AUDIT=true
```

### 5. Validate fortress

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

### 6. Enable GitHub workflows

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

## 📊 What's included

### Security audit layer

- **CodeQL** - SAST security scanning (weekly + on push/PR)
- **Gitleaks** - Secret detection (daily + on push/PR)
- **Dependabot** - Daily security updates for Python, npm, Docker, GitHub Actions

**Compliance:**
- GDPR Art. 32 (Security of Processing)
- ISO 27001 A.12.6 (Technical Vulnerability Management)
- NIST SP 800-53 (IA-5 Authenticator Management)

### Governance kernel

- **Crypto Shredder (IP-02)** - Data dissolution, not deletion
- **47 global legal frameworks** - Complete compliance enforcement
- **Tamper-proof audit trail** - SHA-256 hash chain + Cloud KMS
- **Retention policies** - HOT (180d), WARM (365d), COLD (1825d), ETERNAL

**Compliance:**
- GDPR Art. 17 (Right to Erasure)
- HIPAA §164.530(j) (Documentation)
- NIST SP 800-88 (Media Sanitization)

### AI explainability

- **Vertex AI + SHAP** - Right to Explanation for high-risk inferences
- **Automatic compliance validation** - SovereignGuardrail integration
- **Multiple explainer methods** - TreeExplainer, KernelExplainer, DeepExplainer

**Compliance:**
- EU AI Act §6 (High-Risk AI Systems)
- GDPR Art. 22 (Right to Explanation)
- NIST AI RMF (Explainable and Interpretable)

### Validation

- **Fortress validation script** - 7-phase validation
- **Component health checks** - Security, governance, edge, cloud
- **Nuclear IP stack status** - IP-02, IP-03, IP-04, IP-05, IP-06

## 🔧 Configuration

### SovereignGuardrail

Edit `config/sovereign_guardrail_47_frameworks.yaml`:

```yaml
jurisdiction:
  primary: "KDPA_KE"  # Your primary jurisdiction
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

### Vertex AI + SHAP

```python
from cloud_oracle.vertex_ai_shap import VertexAIExplainer

explainer = VertexAIExplainer(
    project_id="iluminara-core",
    high_risk_threshold=0.7,
    enable_compliance=True
)

result = explainer.predict_with_explanation(
    endpoint_id="projects/123/locations/us-central1/endpoints/456",
    instances=[{"fever": 1, "cough": 1, "age": 35}],
    feature_names=["fever", "cough", "age"],
    jurisdiction="EU_AI_ACT"
)
```

## 📚 Documentation

Complete documentation is available at the documentation site:

- **Security Stack** - `security/overview.mdx`
- **47 Frameworks** - `governance/47-frameworks.mdx`
- **Vertex AI + SHAP** - `ai-agents/vertex-ai-shap.mdx`
- **Bio-Interface API** - `api-reference/bio-interface.mdx`
- **Implementation Summary** - `IMPLEMENTATION_SUMMARY.mdx`

## 🎯 Next steps

1. ✅ Copy files to repository
2. ✅ Run validation script
3. ✅ Enable GitHub workflows
4. ✅ Configure SovereignGuardrail
5. 🚧 Deploy to GCP production
6. 🚧 Train team on new features

## 🔗 Resources

- **Repository:** https://github.com/VISENDI56/iLuminara-Core
- **Documentation:** (Your documentation site)
- **Validation Script:** `scripts/validate_fortress.sh`
- **Configuration:** `config/sovereign_guardrail_47_frameworks.yaml`

## ✨ The Fortress is ready

**The Sovereign Health Fortress is now operational. Sovereign dignity is preserved.**
