# iLuminara-Core Quick Reference Guide
## Sovereign Health Fortress - Command Cheat Sheet

---

## 🚀 Quick Start (5 Minutes)

```bash
# 1. Copy all files to your repository
cd /path/to/iLuminara-Core
cp -r /path/to/docs/repository-files/* .

# 2. Make scripts executable
chmod +x scripts/*.sh

# 3. Set up branch protection
./scripts/setup_branch_protection.sh

# 4. Validate installation
./scripts/validate_fortress.sh

# 5. Commit and push
git add .
git commit -m "feat: integrate Sovereign Health Fortress"
git push origin main
```

---

## 📁 File Locations

| Component | File Path |
|-----------|-----------|
| **CodeQL Workflow** | `.github/workflows/codeql.yml` |
| **Gitleaks Workflow** | `.github/workflows/gitleaks.yml` |
| **Dependabot Config** | `.github/dependabot.yml` |
| **Gitleaks Config** | `.gitleaks.toml` |
| **Crypto Shredder** | `governance_kernel/crypto_shredder.py` |
| **SovereignGuardrail Config** | `config/sovereign_guardrail.yaml` |
| **Vertex AI + SHAP** | `cloud_oracle/vertex_ai_shap.py` |
| **Bio-Interface API** | `edge_node/bio_interface_api.py` |
| **Fortress Validator** | `scripts/validate_fortress.sh` |
| **Branch Protection Setup** | `scripts/setup_branch_protection.sh` |

---

## 🧪 Testing Commands

### Test Crypto Shredder
```bash
python governance_kernel/crypto_shredder.py
```

### Test Vertex AI + SHAP
```bash
export GOOGLE_CLOUD_PROJECT=your-project-id
python cloud_oracle/vertex_ai_shap.py
```

### Test Bio-Interface API
```bash
export NODE_ID=BIO-INTERFACE-01
export JURISDICTION=KDPA_KE
python edge_node/bio_interface_api.py
```

### Validate Fortress
```bash
./scripts/validate_fortress.sh
```

---

## 🔐 Security Workflows

### Check CodeQL Status
```bash
gh run list --workflow=codeql.yml
```

### Check Gitleaks Status
```bash
gh run list --workflow=gitleaks.yml
```

### Re-run Failed Workflow
```bash
gh run rerun RUN_ID
```

### View Workflow Logs
```bash
gh run view RUN_ID --log
```

---

## 🛡️ Branch Protection

### Enable Branch Protection
```bash
./scripts/setup_branch_protection.sh
```

### Create Feature Branch
```bash
git checkout -b feature/my-feature
git push origin feature/my-feature
```

### Create Pull Request
```bash
gh pr create \
  --title "feat: my feature" \
  --body "Description of changes"
```

### Merge Pull Request
```bash
gh pr merge PR_NUMBER --squash
```

---

## 🔑 Crypto Shredder Usage

### Encrypt Data
```python
from governance_kernel.crypto_shredder import CryptoShredder, RetentionPolicy

shredder = CryptoShredder()
encrypted_data, key_id = shredder.encrypt_with_ephemeral_key(
    data=b"sensitive data",
    retention_policy=RetentionPolicy.HOT
)
```

### Decrypt Data
```python
decrypted_data = shredder.decrypt_with_key(encrypted_data, key_id)
```

### Shred Key
```python
shredder.shred_key(key_id)
```

### Auto-Shred Expired Keys
```python
shredded_count = shredder.auto_shred_expired_keys()
```

---

## 🧠 Vertex AI + SHAP Usage

### Make Prediction with Explanation
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

print(f"Prediction: {result['prediction']}")
print(f"Confidence: {result['confidence']}")
print(f"Compliant: {result['compliant']}")
```

### Visualize Explanation
```python
print(explainer.visualize_explanation(result))
```

---

## 📱 Bio-Interface API Usage

### Start API
```bash
export NODE_ID=BIO-INTERFACE-01
export JURISDICTION=KDPA_KE
export BIO_INTERFACE_PORT=8081
python edge_node/bio_interface_api.py
```

### Health Check
```bash
curl http://localhost:8081/health
```

### Submit CBS Signal
```bash
curl -X POST http://localhost:8081/api/v1/submit-cbs \
  -H "Content-Type: application/json" \
  -d '{
    "chv_id": "CHV_AMINA_HASSAN",
    "location": {"lat": 0.0512, "lng": 40.3129},
    "symptom": "diarrhea",
    "severity": 8,
    "timestamp": "2025-12-25T10:00:00Z"
  }'
```

### Submit EMR Record
```bash
curl -X POST http://localhost:8081/api/v1/submit-emr \
  -H "Content-Type: application/json" \
  -d '{
    "facility_id": "DADAAB_CLINIC",
    "patient_id": "PAT_12345",
    "location": {"lat": 0.0512, "lng": 40.3129},
    "diagnosis": "cholera",
    "timestamp": "2025-12-25T10:30:00Z"
  }'
```

### Batch Submit
```bash
curl -X POST http://localhost:8081/api/v1/batch-submit \
  -H "Content-Type: application/json" \
  -d '{
    "signals": [
      {"type": "cbs", "data": {...}},
      {"type": "emr", "data": {...}}
    ]
  }'
```

---

## ⚙️ Configuration

### Set Environment Variables
```bash
export NODE_ID=JOR-47
export JURISDICTION=KDPA_KE
export GOOGLE_CLOUD_PROJECT=iluminara-core
export GCP_REGION=us-central1
export ENABLE_TAMPER_PROOF_AUDIT=true
export RETENTION_MAX_DAYS=1825
```

### Configure Jurisdiction
Edit `config/sovereign_guardrail.yaml`:
```yaml
jurisdiction:
  primary: "KDPA_KE"  # Change to your jurisdiction
  secondary:
    - "GDPR_EU"
    - "HIPAA_US"
```

---

## 🚀 Deployment

### Deploy to Google Cloud Run
```bash
# Deploy FRENASA Engine
gcloud run deploy frenasa-engine \
  --source=./edge_node/frenasa_engine \
  --region=us-central1

# Deploy Bio-Interface API
gcloud run deploy bio-interface-api \
  --source=./edge_node \
  --region=us-central1 \
  --set-env-vars NODE_ID=BIO-INTERFACE-01,JURISDICTION=KDPA_KE
```

### Deploy Vertex AI Model
```bash
gcloud ai models upload \
  --region=us-central1 \
  --display-name=outbreak-forecaster \
  --container-image-uri=gcr.io/iluminara-core/outbreak-model:latest
```

---

## 📊 Monitoring

### View Security Alerts
```bash
gh api /repos/VISENDI56/iLuminara-Core/code-scanning/alerts
```

### View Dependabot Alerts
```bash
gh api /repos/VISENDI56/iLuminara-Core/dependabot/alerts
```

### View Secret Scanning Alerts
```bash
gh api /repos/VISENDI56/iLuminara-Core/secret-scanning/alerts
```

---

## 🐛 Troubleshooting

### CodeQL Fails
```bash
# Check logs
gh run list --workflow=codeql.yml
gh run view RUN_ID --log

# Re-run
gh run rerun RUN_ID
```

### Gitleaks False Positive
Add to `.gitleaks.toml`:
```toml
[allowlist]
paths = [
  '''.*_test\\.py''',
  '''.*\\.example'''
]
```

### Branch Protection Blocks Push
```bash
# Create PR instead
git checkout -b feature/my-changes
git push origin feature/my-changes
gh pr create
```

### Import Error
```bash
pip install -r requirements.txt
```

---

## 📚 Documentation Links

- **Implementation Guide:** `repository-files/IMPLEMENTATION_GUIDE.md`
- **Repository README:** `repository-files/README.md`
- **Deployment Summary:** `DEPLOYMENT_SUMMARY.md`
- **Online Docs:** https://docs.iluminara.health
- **Security Stack:** https://docs.iluminara.health/security/overview
- **Vertex AI + SHAP:** https://docs.iluminara.health/integrations/vertex-ai-shap
- **Bio-Interface API:** https://docs.iluminara.health/integrations/bio-interface

---

## ✅ Verification Checklist

```bash
# 1. Check files exist
ls -la .github/workflows/codeql.yml
ls -la .github/workflows/gitleaks.yml
ls -la governance_kernel/crypto_shredder.py
ls -la cloud_oracle/vertex_ai_shap.py
ls -la edge_node/bio_interface_api.py

# 2. Run validator
./scripts/validate_fortress.sh

# 3. Check workflows
gh run list

# 4. Check branch protection
gh api /repos/VISENDI56/iLuminara-Core/branches/main/protection

# 5. Test components
python governance_kernel/crypto_shredder.py
python cloud_oracle/vertex_ai_shap.py
python edge_node/bio_interface_api.py
```

---

## 🆘 Quick Help

| Issue | Solution |
|-------|----------|
| **Cannot push to main** | Create PR: `gh pr create` |
| **CodeQL fails** | Check logs: `gh run view RUN_ID --log` |
| **Gitleaks false positive** | Add to `.gitleaks.toml` allowlist |
| **Import error** | Install deps: `pip install -r requirements.txt` |
| **API not starting** | Check env vars: `echo $NODE_ID` |
| **Validation fails** | Review errors in validator output |

---

## 🎯 Common Tasks

### Add New Compliance Framework
Edit `config/sovereign_guardrail.yaml`:
```yaml
frameworks:
  NEW_FRAMEWORK:
    enabled: true
    articles: ["Art. 1", "Art. 2"]
```

### Change Retention Policy
Edit `config/sovereign_guardrail.yaml`:
```yaml
retention:
  policies:
    HOT:
      days: 180  # Change as needed
```

### Add New API Endpoint
Edit `edge_node/bio_interface_api.py`:
```python
@app.route('/api/v1/new-endpoint', methods=['POST'])
def new_endpoint():
    # Implementation
    pass
```

---

**The Fortress is operational. Use this guide for quick reference.**
