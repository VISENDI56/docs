# iLuminara-Core Sovereign Health Fortress Deployment Guide

## 🛡️ Overview

This guide will help you deploy the complete Nuclear IP Stack security infrastructure to your iLuminara-Core repository.

## 📋 Prerequisites

1. **GitHub CLI installed and authenticated:**
   ```bash
   gh auth refresh -s workflow,repo,write:packages,admin:repo_hook
   ```

2. **Repository cloned:**
   ```bash
   git clone https://github.com/VISENDI56/iLuminara-Core.git
   cd iLuminara-Core
   ```

3. **Python 3.8+ installed:**
   ```bash
   python3 --version
   ```

## 🚀 Deployment Steps

### Step 1: Copy Security Workflows

```bash
# Create .github/workflows directory if it doesn't exist
mkdir -p .github/workflows

# Copy CodeQL workflow
cp repository-files/.github/workflows/codeql.yml .github/workflows/

# Copy Gitleaks workflow
cp repository-files/.github/workflows/gitleaks.yml .github/workflows/

# Copy Gitleaks configuration
cp repository-files/.gitleaks.toml .gitleaks.toml

# Copy Dependabot configuration
cp repository-files/.github/dependabot.yml .github/dependabot.yml
```

### Step 2: Deploy Governance Kernel

```bash
# Copy Crypto Shredder (IP-02)
cp repository-files/governance_kernel/crypto_shredder.py governance_kernel/

# Copy SovereignGuardrail configuration
mkdir -p config
cp repository-files/config/sovereign_guardrail.yaml config/
```

### Step 3: Deploy Validation Scripts

```bash
# Create scripts directory
mkdir -p scripts

# Copy validation script
cp repository-files/scripts/validate_fortress.sh scripts/

# Make executable
chmod +x scripts/validate_fortress.sh
```

### Step 4: Install Python Dependencies

```bash
# Install cryptography for Crypto Shredder
pip install cryptography

# Or update requirements.txt
echo "cryptography>=41.0.0" >> requirements.txt
pip install -r requirements.txt
```

### Step 5: Configure Environment Variables

```bash
# Set node identification
export NODE_ID=JOR-47
export JURISDICTION=KDPA_KE

# Set GCP configuration (if using cloud)
export GOOGLE_CLOUD_PROJECT=your-project-id
export GCP_REGION=us-central1

# Set governance configuration
export ENABLE_TAMPER_PROOF_AUDIT=true
export RETENTION_MAX_DAYS=1825
```

Add to `.bashrc` or `.zshrc` for persistence:

```bash
cat >> ~/.bashrc << 'EOF'
# iLuminara-Core Configuration
export NODE_ID=JOR-47
export JURISDICTION=KDPA_KE
export GOOGLE_CLOUD_PROJECT=your-project-id
export ENABLE_TAMPER_PROOF_AUDIT=true
EOF

source ~/.bashrc
```

### Step 6: Validate the Fortress

```bash
# Run validation
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
📄 Checking .github/workflows/gitleaks.yml... ✓ OPERATIONAL
...

🛡️  FORTRESS STATUS: OPERATIONAL
✓  All critical components validated
✓  Security audit layer active
✓  Governance kernel operational
✓  Nuclear IP stack initialized

The Sovereign Health Fortress is ready for deployment.
```

### Step 7: Commit and Push

```bash
# Stage all changes
git add .

# Commit with fortress signature
git commit -m "feat: integrate Sovereign Health Fortress and Nuclear IP security stack

- Add CodeQL SAST scanning (GDPR Art. 32, ISO 27001 A.12.6)
- Add Gitleaks secret detection (NIST SP 800-53 IA-5)
- Implement IP-02 Crypto Shredder (data dissolution)
- Configure SovereignGuardrail (14 global legal frameworks)
- Add Dependabot daily security updates
- Add fortress validation script

Compliance: GDPR, KDPA, HIPAA, POPIA, EU AI Act, ISO 27001, SOC 2"

# Push to repository
git push origin main
```

### Step 8: Enable Branch Protection

```bash
# Enable branch protection on main
gh api repos/VISENDI56/iLuminara-Core/branches/main/protection \
  --method PUT \
  --field required_status_checks[strict]=true \
  --field required_status_checks[contexts][]=CodeQL \
  --field required_status_checks[contexts][]=Gitleaks \
  --field enforce_admins=true \
  --field required_pull_request_reviews[required_approving_review_count]=1
```

## 🔧 Configuration

### SovereignGuardrail Configuration

Edit `config/sovereign_guardrail.yaml` to customize:

```yaml
jurisdiction:
  primary: "KDPA_KE"  # Change to your jurisdiction
  secondary:
    - "GDPR_EU"
    - "POPIA_ZA"

sovereignty:
  data_residency:
    enabled: true
    allowed_zones:
      - "africa-south1"  # Add your allowed zones
    enforcement_level: "STRICT"
```

### Crypto Shredder Usage

```python
from governance_kernel.crypto_shredder import CryptoShredder, RetentionPolicy, SovereigntyZone

# Initialize
shredder = CryptoShredder(
    sovereignty_zone=SovereigntyZone.KENYA,
    enable_audit=True
)

# Encrypt patient data
encrypted_data, key_id = shredder.encrypt_with_ephemeral_key(
    data=patient_record,
    retention_policy=RetentionPolicy.HOT,
    metadata={"patient_id": "12345", "jurisdiction": "KDPA_KE"}
)

# Auto-shred expired keys
shredder.auto_shred_expired_keys()
```

## 🧪 Testing

### Test CodeQL Workflow

```bash
# Trigger CodeQL scan
gh workflow run codeql.yml
```

### Test Gitleaks Workflow

```bash
# Trigger Gitleaks scan
gh workflow run gitleaks.yml
```

### Test Crypto Shredder

```bash
# Run example
python governance_kernel/crypto_shredder.py
```

Expected output:
```
🔐 Crypto Shredder initialized - Zone: africa-south1
✅ Encrypted - Key ID: a1b2c3d4e5f6g7h8
✅ Decrypted: Patient ID: 12345, Diagnosis: Malaria, Location: Dadaab
🔥 Key shredded - Data irrecoverable: a1b2c3d4e5f6g7h8
❌ Decryption after shred: None
```

## 📊 Monitoring

### View Security Alerts

```bash
# View CodeQL alerts
gh api repos/VISENDI56/iLuminara-Core/code-scanning/alerts

# View Dependabot alerts
gh api repos/VISENDI56/iLuminara-Core/dependabot/alerts
```

### View Workflow Runs

```bash
# View recent workflow runs
gh run list --limit 10
```

## 🚨 Troubleshooting

### CodeQL Workflow Fails

**Issue:** CodeQL analysis fails with "No code to analyze"

**Solution:**
```bash
# Ensure Python files exist in repository
find . -name "*.py" | head -5

# Check CodeQL configuration
cat .github/workflows/codeql.yml
```

### Gitleaks Detects False Positives

**Issue:** Gitleaks flags test data as secrets

**Solution:** Add to `.gitleaks.toml`:
```toml
[allowlist]
paths = [
  '''.*_test\.py''',
  '''.*\.example''',
]
```

### Crypto Shredder Import Error

**Issue:** `ModuleNotFoundError: No module named 'cryptography'`

**Solution:**
```bash
pip install cryptography>=41.0.0
```

### Validation Script Fails

**Issue:** Permission denied when running validation script

**Solution:**
```bash
chmod +x scripts/validate_fortress.sh
./scripts/validate_fortress.sh
```

## 📚 Next Steps

1. **Configure Vertex AI + SHAP Integration**
   - See: `docs/ai-agents/explainability.md`

2. **Set Up Bio-Interface REST API**
   - See: `docs/api-reference/bio-interface.md`

3. **Deploy to Google Cloud Platform**
   - See: `docs/deployment/gcp.md`

4. **Configure Monitoring & Alerting**
   - See: `docs/deployment/monitoring.md`

## 🛡️ Compliance Checklist

- [ ] CodeQL SAST scanning enabled
- [ ] Gitleaks secret detection enabled
- [ ] Dependabot daily updates configured
- [ ] Branch protection rules active
- [ ] SovereignGuardrail configured for jurisdiction
- [ ] Crypto Shredder tested and operational
- [ ] Tamper-proof audit trail enabled
- [ ] Environment variables configured
- [ ] Fortress validation passing

## 📞 Support

For issues or questions:
- GitHub Issues: https://github.com/VISENDI56/iLuminara-Core/issues
- Documentation: https://docs.iluminara.health

---

**The Fortress is now built. Your repository has transitioned from code to Sovereign Architecture.**
