# iLuminara-Core Setup Guide
## Sovereign Health Fortress Deployment

This guide walks you through setting up the complete iLuminara-Core security and integration stack.

---

## Phase 1: GitHub Security Configuration

### Step 1: Elevate Agent Permissions

Ensure your GitHub Codespace has the required permissions:

```bash
gh auth refresh -s workflow,repo,write:packages,admin:repo_hook
```

### Step 2: Enable Branch Protection

Protect the `main` branch with required status checks:

```bash
# Enable branch protection
gh api repos/VISENDI56/iLuminara-Core/branches/main/protection \
  --method PUT \
  --field required_status_checks='{"strict":true,"contexts":["CodeQL","Gitleaks"]}' \
  --field enforce_admins=true \
  --field required_pull_request_reviews='{"required_approving_review_count":1}' \
  --field restrictions=null
```

Or configure via GitHub UI:
1. Go to **Settings** → **Branches**
2. Add rule for `main` branch
3. Enable:
   - ✅ Require pull request before merging
   - ✅ Require status checks to pass (CodeQL, Gitleaks)
   - ✅ Require branches to be up to date
   - ✅ Include administrators

### Step 3: Enable Security Features

```bash
# Enable Dependabot alerts
gh api repos/VISENDI56/iLuminara-Core/vulnerability-alerts \
  --method PUT

# Enable Dependabot security updates
gh api repos/VISENDI56/iLuminara-Core/automated-security-fixes \
  --method PUT

# Enable secret scanning
gh api repos/VISENDI56/iLuminara-Core \
  --method PATCH \
  --field security_and_analysis='{"secret_scanning":{"status":"enabled"},"secret_scanning_push_protection":{"status":"enabled"}}'
```

---

## Phase 2: Deploy Security Workflows

### Copy Workflow Files

Copy the following files from `repository-files/` to your iLuminara-Core repository:

```bash
# From your docs repository
cd /path/to/docs/repository-files

# Copy to iLuminara-Core
cp -r .github /path/to/iLuminara-Core/
cp .gitleaks.toml /path/to/iLuminara-Core/
```

**Files to copy:**
- `.github/workflows/codeql.yml` - SAST security scanning
- `.github/workflows/gitleaks.yml` - Secret detection
- `.github/dependabot.yml` - Daily security updates
- `.gitleaks.toml` - Secret scanning configuration

### Commit and Push

```bash
cd /path/to/iLuminara-Core

git add .github/workflows/codeql.yml
git add .github/workflows/gitleaks.yml
git add .github/dependabot.yml
git add .gitleaks.toml

git commit -m "feat: integrate SovereignGuardrail and Nuclear IP security stack"
git push origin main
```

---

## Phase 3: Deploy Governance Kernel

### Copy Governance Files

```bash
# Copy Crypto Shredder (IP-02)
cp repository-files/governance_kernel/crypto_shredder.py /path/to/iLuminara-Core/governance_kernel/

# Copy SovereignGuardrail configuration
mkdir -p /path/to/iLuminara-Core/config
cp repository-files/config/sovereign_guardrail.yaml /path/to/iLuminara-Core/config/
```

### Install Dependencies

```bash
cd /path/to/iLuminara-Core

# Install cryptography library
pip install cryptography

# Or add to requirements.txt
echo "cryptography>=41.0.0" >> requirements.txt
pip install -r requirements.txt
```

### Test Crypto Shredder

```bash
python governance_kernel/crypto_shredder.py
```

Expected output:
```
🔐 Crypto Shredder initialized - Zone: africa-south1
✅ Encrypted - Key ID: abc123def456
✅ Decrypted: Patient ID: 12345, Diagnosis: Malaria, Location: Dadaab
🔥 Key shredded - Data irrecoverable: abc123def456
❌ Decryption after shred: None
```

---

## Phase 4: Configure Environment

### Set Environment Variables

Create `.env` file:

```bash
# Node identification
export NODE_ID=JOR-47
export JURISDICTION=KDPA_KE

# API configuration
export API_HOST=0.0.0.0
export API_PORT=8080

# GCP configuration
export GOOGLE_CLOUD_PROJECT=your-project-id
export GCP_REGION=africa-south1

# Governance settings
export ENABLE_TAMPER_PROOF_AUDIT=true
export RETENTION_MAX_DAYS=1825
export DATA_SOVEREIGNTY_REQUIRED=true
```

Load environment:

```bash
source .env
```

---

## Phase 5: Validate Fortress

### Copy Validation Script

```bash
cp repository-files/scripts/validate_fortress.sh /path/to/iLuminara-Core/scripts/
chmod +x /path/to/iLuminara-Core/scripts/validate_fortress.sh
```

### Run Validation

```bash
cd /path/to/iLuminara-Core
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
🔍 Checking .github/workflows/gitleaks.yml... ✓ OPERATIONAL
📄 Checking .gitleaks.toml... ✓ EXISTS
📄 Checking .github/dependabot.yml... ✓ EXISTS

...

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

---

## Phase 6: Deploy to GCP (Optional)

### Prerequisites

```bash
# Install gcloud CLI
curl https://sdk.cloud.google.com | bash
exec -l $SHELL

# Authenticate
gcloud auth login
gcloud config set project YOUR_PROJECT_ID
```

### Deploy Services

```bash
chmod +x deploy_gcp_prototype.sh
./deploy_gcp_prototype.sh
```

This deploys:
- FRENASA AI Engine (Cloud Run)
- HSTPU Forecaster (Vertex AI)
- HSML Ledger (Cloud Spanner)
- Dashboard (Cloud Run)

---

## Phase 7: Launch Services

### Local Development

```bash
chmod +x launch_all_services.sh
./launch_all_services.sh
```

This launches:
- **Command Console**: http://localhost:8501
- **Transparency Audit**: http://localhost:8502
- **Field Validation**: http://localhost:8503
- **API Service**: http://localhost:8080

### Validate Services

```bash
# Check API health
curl http://localhost:8080/health

# Check dashboard
curl http://localhost:8501/_stcore/health
```

---

## Phase 8: Test the Stack

### Test Voice Processing

```bash
# Generate test audio
python generate_test_audio.py

# Process voice alert
curl -X POST http://localhost:8080/process-voice \
  -H "Content-Type: audio/wav" \
  --data-binary @swahili-symptom.wav
```

### Test Outbreak Prediction

```bash
curl -X POST http://localhost:8080/predict \
  -H "Content-Type: application/json" \
  -d '{
    "location": {"lat": 0.4221, "lng": 40.2255},
    "symptoms": ["diarrhea", "vomiting"]
  }'
```

### Test Governance Kernel

```python
from governance_kernel.vector_ledger import SovereignGuardrail, SovereigntyViolationError

guardrail = SovereignGuardrail()

# Try to export health data (should fail)
try:
    guardrail.validate_action(
        action_type='Data_Transfer',
        payload={'data_type': 'PHI', 'destination': 'AWS_US'},
        jurisdiction='GDPR_EU'
    )
except SovereigntyViolationError as e:
    print(f"✅ Sovereignty protection working: {e}")
```

---

## Troubleshooting

### CodeQL Workflow Fails

**Issue:** CodeQL analysis fails with "No code to analyze"

**Solution:**
```bash
# Ensure Python files exist
ls -la *.py

# Check workflow configuration
cat .github/workflows/codeql.yml
```

### Gitleaks Finds Secrets

**Issue:** Gitleaks detects hardcoded secrets

**Solution:**
```bash
# Review detected secrets
cat results.sarif

# Remove secrets from code
git filter-branch --force --index-filter \
  "git rm --cached --ignore-unmatch path/to/secret/file" \
  --prune-empty --tag-name-filter cat -- --all

# Use environment variables instead
export API_KEY="your-key"
```

### Crypto Shredder Import Error

**Issue:** `ModuleNotFoundError: No module named 'cryptography'`

**Solution:**
```bash
pip install cryptography
```

### Validation Script Fails

**Issue:** Permission denied when running validation script

**Solution:**
```bash
chmod +x scripts/validate_fortress.sh
```

---

## Next Steps

1. **Configure Compliance**: Edit `config/sovereign_guardrail.yaml` for your jurisdiction
2. **Deploy AI Agents**: Set up autonomous surveillance agents
3. **Integrate Mobile Apps**: Use Bio-Interface REST API
4. **Set Up Monitoring**: Configure Prometheus and Grafana
5. **Train Operators**: Conduct war room demo training

---

## Support

- **Documentation**: https://docs.iluminara.health
- **GitHub Issues**: https://github.com/VISENDI56/iLuminara-Core/issues
- **Email**: support@iluminara.health

---

## Compliance Checklist

- [ ] CodeQL workflow enabled
- [ ] Gitleaks secret scanning enabled
- [ ] Dependabot security updates enabled
- [ ] Branch protection configured
- [ ] Crypto Shredder deployed
- [ ] SovereignGuardrail configured
- [ ] Environment variables set
- [ ] Fortress validation passed
- [ ] Services launched successfully
- [ ] Test suite passed

**Status:** 🛡️ Sovereign Health Fortress is OPERATIONAL
