# iLuminara-Core Repository Files

This directory contains all the files that should be copied to your **iLuminara-Core** repository to implement the complete Sovereign Health Fortress security stack.

## 📁 Directory Structure

```
repository-files/
├── .github/
│   ├── workflows/
│   │   ├── codeql.yml          # SAST security scanning
│   │   ├── gitleaks.yml        # Secret detection
│   │   └── mintlify.yml        # Documentation deployment
│   └── dependabot.yml          # Daily security updates
├── .gitleaks.toml              # Secret scanning configuration
├── config/
│   └── sovereign_guardrail.yaml # Governance configuration
├── governance_kernel/
│   └── crypto_shredder.py      # IP-02: Data dissolution
└── scripts/
    └── validate_fortress.sh    # Fortress validation script
```

## 🚀 Installation Instructions

### Step 1: Copy files to repository

```bash
# Navigate to your iLuminara-Core repository
cd /path/to/iLuminara-Core

# Copy all files from repository-files/
cp -r /path/to/docs/repository-files/.github .
cp -r /path/to/docs/repository-files/config .
cp -r /path/to/docs/repository-files/governance_kernel .
cp -r /path/to/docs/repository-files/scripts .
cp /path/to/docs/repository-files/.gitleaks.toml .
```

### Step 2: Make scripts executable

```bash
chmod +x scripts/validate_fortress.sh
chmod +x deploy_gcp_prototype.sh
chmod +x launch_all_services.sh
```

### Step 3: Configure GitHub secrets

1. Go to your repository **Settings** → **Secrets and variables** → **Actions**
2. Add the following secrets:
   - `MINTLIFY_API_KEY` - Your Mintlify API key
   - `GITLEAKS_LICENSE` - Your Gitleaks license (optional)

### Step 4: Enable GitHub Actions

1. Go to **Actions** tab in your repository
2. Enable workflows if prompted
3. Workflows will run automatically on push

### Step 5: Configure branch protection

```bash
# Enable branch protection on main
gh api repos/VISENDI56/iLuminara-Core/branches/main/protection \
  -X PUT \
  -H "Accept: application/vnd.github+json" \
  -f required_status_checks[strict]=true \
  -f required_status_checks[contexts][]=CodeQL \
  -f required_status_checks[contexts][]=Gitleaks \
  -f required_pull_request_reviews[required_approving_review_count]=1
```

## 🛡️ Security Workflows

### CodeQL (SAST)

**File:** `.github/workflows/codeql.yml`

**Triggers:**
- Push to `main` or `develop`
- Pull requests to `main`
- Weekly schedule (Sunday midnight UTC)

**Languages:** Python, JavaScript

**Compliance:** GDPR Art. 32, ISO 27001 A.12.6

### Gitleaks (Secret Scanning)

**File:** `.github/workflows/gitleaks.yml`

**Triggers:**
- Push to `main` or `develop`
- Pull requests to `main`
- Daily schedule (2 AM UTC)

**Detects:**
- API keys (GCP, AWS, GitHub, Slack)
- Private keys
- JWT tokens
- Service account credentials

**Compliance:** NIST SP 800-53 (IA-5), HIPAA §164.312(a)(2)(i)

### Mintlify (Documentation)

**File:** `.github/workflows/mintlify.yml`

**Triggers:**
- Push to `main` (docs changes)
- Pull requests (preview)
- Manual workflow dispatch

**Actions:**
- Validate documentation
- Check for broken links
- Build optimized site
- Deploy to Mintlify

### Dependabot (Security Updates)

**File:** `.github/dependabot.yml`

**Schedule:**
- Python dependencies: Daily at 2 AM UTC
- GitHub Actions: Weekly (Monday)
- Docker: Weekly (Tuesday)
- npm: Daily at 2 AM UTC

**Groups:**
- Security updates (cryptography, pyjwt, requests)
- Google Cloud (google-cloud-*)
- AI/ML (tensorflow, torch, scikit-learn, shap)

## 🔐 Crypto Shredder (IP-02)

**File:** `governance_kernel/crypto_shredder.py`

### Features

- ✅ Ephemeral key encryption (AES-256-GCM)
- ✅ Retention policies (HOT/WARM/COLD/ETERNAL)
- ✅ Auto-shred expired keys
- ✅ Sovereignty zone enforcement
- ✅ Tamper-proof audit trail

### Usage

```python
from governance_kernel.crypto_shredder import CryptoShredder, RetentionPolicy, SovereigntyZone

# Initialize
shredder = CryptoShredder(
    sovereignty_zone=SovereigntyZone.KENYA,
    enable_audit=True
)

# Encrypt data
encrypted_data, key_id = shredder.encrypt_with_ephemeral_key(
    data=patient_record,
    retention_policy=RetentionPolicy.HOT,
    metadata={"patient_id": "12345", "jurisdiction": "KDPA_KE"}
)

# Decrypt (while key exists)
decrypted_data = shredder.decrypt_with_key(encrypted_data, key_id)

# Shred key (data becomes irrecoverable)
shredder.shred_key(key_id)

# Auto-shred expired keys
shredded_count = shredder.auto_shred_expired_keys()
```

### Compliance

- GDPR Art. 17 (Right to Erasure)
- HIPAA §164.530(j) (Documentation)
- NIST SP 800-88 (Media Sanitization)
- ISO 27001 A.8.3.2 (Disposal of Media)

## ⚙️ SovereignGuardrail Configuration

**File:** `config/sovereign_guardrail.yaml`

### Key Settings

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

### Customization

1. **Set your jurisdiction:**
   ```yaml
   jurisdiction:
     primary: "YOUR_JURISDICTION"
   ```

2. **Configure allowed zones:**
   ```yaml
   sovereignty:
     data_residency:
       allowed_zones:
         - "your-region-1"
         - "your-region-2"
   ```

3. **Adjust retention policies:**
   ```yaml
   retention:
     policies:
       HOT:
         days: 180  # Customize as needed
   ```

## 🔍 Fortress Validation

**File:** `scripts/validate_fortress.sh`

### What it checks

1. **Security Audit Layer**
   - CodeQL workflow
   - Gitleaks workflow
   - Dependabot configuration

2. **Governance Kernel**
   - SovereignGuardrail
   - Crypto Shredder
   - Ethical Engine
   - Configuration files

3. **Edge Node & AI Agents**
   - FRENASA Engine
   - AI Agents
   - Golden Thread

4. **Cloud Oracle**
   - API service
   - Dashboard
   - Deployment scripts

5. **Python Dependencies**
   - Python installation
   - Critical packages

6. **Environment Configuration**
   - NODE_ID
   - JURISDICTION
   - GOOGLE_CLOUD_PROJECT

7. **Nuclear IP Stack Status**
   - IP-02: Crypto Shredder
   - IP-03: Acorn Protocol
   - IP-04: Silent Flux
   - IP-05: Golden Thread
   - IP-06: 5DM Bridge

### Run validation

```bash
./scripts/validate_fortress.sh
```

**Expected output:**
```
🛡️ FORTRESS STATUS: OPERATIONAL
✓ All critical components validated
✓ Security audit layer active
✓ Governance kernel operational
✓ Nuclear IP stack initialized
```

## 📊 Monitoring

### Prometheus Metrics

The security stack exposes metrics at `:9090/metrics`:

```
sovereignty_violations_total
cross_border_transfers_total
high_risk_inferences_total
keys_shredded_total
```

### Grafana Dashboards

Import dashboards from `monitoring/grafana/`:
- Sovereignty Compliance
- Audit Trail
- Data Retention

## 🚨 Incident Response

### Security Violation Detected

1. **Automatic actions:**
   - SovereignGuardrail blocks the action
   - Alert sent to compliance team
   - Audit log entry created

2. **Manual investigation:**
   ```bash
   # View audit logs
   cat governance_kernel/keys/audit.jsonl | grep "SOVEREIGNTY_VIOLATION"
   
   # Check key status
   python -c "from governance_kernel.crypto_shredder import CryptoShredder; \
              shredder = CryptoShredder(); \
              print(shredder.get_key_status('KEY_ID'))"
   ```

3. **Remediation:**
   ```bash
   # Shred compromised keys
   python scripts/emergency_shred.py --key-id KEY_ID
   
   # Re-validate fortress
   ./scripts/validate_fortress.sh
   ```

## 🔄 Continuous Integration

### Pre-commit Hooks

Add to `.git/hooks/pre-commit`:

```bash
#!/bin/bash

# Run Gitleaks
gitleaks detect --source . --verbose

# Run fortress validation
./scripts/validate_fortress.sh --quick

# Run tests
python -m pytest tests/
```

### Pull Request Checklist

- [ ] CodeQL scan passes
- [ ] Gitleaks scan passes
- [ ] Fortress validation passes
- [ ] Documentation updated
- [ ] Tests added/updated
- [ ] Changelog updated

## 📚 Additional Resources

- **Documentation:** https://visendi56.mintlify.app
- **Repository:** https://github.com/VISENDI56/iLuminara-Core
- **Issues:** https://github.com/VISENDI56/iLuminara-Core/issues
- **Slack:** https://iluminara.slack.com

## 🤝 Support

For questions or issues:

1. Check the [documentation](https://visendi56.mintlify.app)
2. Search [existing issues](https://github.com/VISENDI56/iLuminara-Core/issues)
3. Create a [new issue](https://github.com/VISENDI56/iLuminara-Core/issues/new)
4. Join our [Slack community](https://iluminara.slack.com)

## 📄 License

All files in this directory are part of iLuminara-Core and are licensed under the Sovereign Health License v1.0.
