# iLuminara-Core Sovereign Health Fortress Implementation Guide

## Overview

This guide provides step-by-step instructions for implementing the complete iLuminara-Core security and compliance stack in your GitHub repository.

## Prerequisites

- GitHub repository with admin access
- GitHub CLI (`gh`) installed
- Python 3.8+ installed
- Google Cloud Platform account (for cloud deployment)

## Step 1: Elevate Agent Permissions

```bash
# Authenticate with required scopes
gh auth refresh -s workflow,repo,write:packages,admin:repo_hook
```

## Step 2: Copy Security Workflows

Copy the following files from `repository-files/` to your iLuminara-Core repository:

### GitHub Actions Workflows

```bash
# Create workflows directory
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

### Governance Kernel

```bash
# Copy Crypto Shredder (IP-02)
cp repository-files/governance_kernel/crypto_shredder.py governance_kernel/

# Copy SovereignGuardrail configuration
mkdir -p config
cp repository-files/config/sovereign_guardrail.yaml config/
```

### Validation Scripts

```bash
# Copy fortress validation script
mkdir -p scripts
cp repository-files/scripts/validate_fortress.sh scripts/
chmod +x scripts/validate_fortress.sh
```

## Step 3: Install Dependencies

```bash
# Install cryptography for Crypto Shredder
pip install cryptography

# Install existing requirements
pip install -r requirements.txt
```

## Step 4: Configure Environment Variables

Add the following to your `.env` file or export them:

```bash
# Node identification
export NODE_ID=JOR-47
export JURISDICTION=KDPA_KE

# API configuration
export API_HOST=0.0.0.0
export API_PORT=8080

# GCP configuration (if using cloud)
export GOOGLE_CLOUD_PROJECT=your-project-id
export GCP_REGION=us-central1

# Governance configuration
export ENABLE_TAMPER_PROOF_AUDIT=true
export RETENTION_MAX_DAYS=1825
export AUDIT_LOG_LEVEL=INFO

# Sovereignty settings
export DATA_SOVEREIGNTY_REQUIRED=true
export REQUIRES_EXPLICIT_CONSENT=true

# AI agents configuration
export ENABLE_OFFLINE_MODE=true
export SYNC_INTERVAL_SECONDS=300

# Federated learning
export FEDERATED_LEARNING_EPSILON=1.0
export FEDERATED_LEARNING_DELTA=1e-5
```

## Step 5: Enable GitHub Security Features

```bash
# Enable CodeQL
gh api repos/:owner/:repo/code-scanning/default-setup \
  -X PATCH \
  -f state=configured

# Enable Dependabot security updates
gh api repos/:owner/:repo/vulnerability-alerts \
  -X PUT

# Enable Dependabot alerts
gh api repos/:owner/:repo/automated-security-fixes \
  -X PUT
```

## Step 6: Configure Branch Protection

```bash
# Protect main branch
gh api repos/:owner/:repo/branches/main/protection \
  -X PUT \
  -f required_status_checks[strict]=true \
  -f required_status_checks[contexts][]=CodeQL \
  -f required_status_checks[contexts][]=Gitleaks \
  -f required_pull_request_reviews[required_approving_review_count]=1 \
  -f enforce_admins=true \
  -f required_linear_history=true \
  -f allow_force_pushes=false \
  -f allow_deletions=false
```

## Step 7: Commit and Push Changes

```bash
# Add all files
git add .

# Commit with descriptive message
git commit -m "feat: integrate SovereignGuardrail and Nuclear IP security stack

- Add CodeQL SAST scanning workflow
- Add Gitleaks secret detection workflow
- Implement IP-02 Crypto Shredder for data dissolution
- Add SovereignGuardrail configuration for 14 global frameworks
- Configure Dependabot for daily security updates
- Add fortress validation script

Compliance:
- GDPR Art. 32 (Security of Processing)
- KDPA Section 25 (Data Protection Principles)
- HIPAA §164.312 (Technical Safeguards)
- ISO 27001 A.12.6 (Technical Vulnerability Management)
- NIST SP 800-53 (IA-5 Authenticator Management)"

# Push to main
git push origin main
```

## Step 8: Validate Fortress Deployment

```bash
# Run validation script
./scripts/validate_fortress.sh

# Expected output:
# ═══════════════════════════════════════════════════════════
# PHASE 1: Security Audit Layer
# ═══════════════════════════════════════════════════════════
# ✓ CodeQL workflow configured
# ✓ Gitleaks workflow configured
# ✓ Dependabot configured
#
# ═══════════════════════════════════════════════════════════
# PHASE 2: Governance Kernel (Nuclear IP Stack)
# ═══════════════════════════════════════════════════════════
# ✓ SovereignGuardrail operational
# ✓ IP-02 Crypto Shredder active
# ✓ Ethical Engine configured
#
# ═══════════════════════════════════════════════════════════
# FORTRESS STATUS: OPERATIONAL
# ═══════════════════════════════════════════════════════════
```

## Step 9: Test Crypto Shredder (IP-02)

```python
from governance_kernel.crypto_shredder import CryptoShredder, RetentionPolicy, SovereigntyZone

# Initialize Crypto Shredder
shredder = CryptoShredder(
    sovereignty_zone=SovereigntyZone.KENYA,
    enable_audit=True
)

# Encrypt patient data
patient_data = b"Patient ID: 12345, Diagnosis: Malaria, Location: Dadaab"
encrypted_data, key_id = shredder.encrypt_with_ephemeral_key(
    data=patient_data,
    retention_policy=RetentionPolicy.HOT,
    metadata={
        "patient_id": "12345",
        "jurisdiction": "KDPA_KE",
        "data_type": "PHI"
    }
)

print(f"✅ Encrypted - Key ID: {key_id}")

# Decrypt (while key exists)
decrypted_data = shredder.decrypt_with_key(encrypted_data, key_id)
print(f"✅ Decrypted: {decrypted_data.decode()}")

# Shred key (data becomes irrecoverable)
shredder.shred_key(key_id)
print(f"🔥 Key shredded - Data irrecoverable")

# Try to decrypt after shredding
decrypted_data = shredder.decrypt_with_key(encrypted_data, key_id)
print(f"❌ Decryption after shred: {decrypted_data}")  # None
```

## Step 10: Test SovereignGuardrail

```python
from governance_kernel.vector_ledger import SovereignGuardrail, SovereigntyViolationError

guardrail = SovereignGuardrail()

# Test 1: Valid processing
try:
    guardrail.validate_action(
        action_type='Data_Processing',
        payload={
            'data_type': 'PHI',
            'processing_location': 'Edge_Node',
            'consent_token': 'VALID_TOKEN'
        },
        jurisdiction='KDPA_KE'
    )
    print("✅ Valid processing approved")
except SovereigntyViolationError as e:
    print(f"❌ {e}")

# Test 2: Invalid cross-border transfer
try:
    guardrail.validate_action(
        action_type='Data_Transfer',
        payload={
            'data_type': 'PHI',
            'destination': 'AWS_US'
        },
        jurisdiction='KDPA_KE'
    )
except SovereigntyViolationError as e:
    print(f"✅ Sovereignty violation blocked: {e}")
```

## Step 11: Configure Compliance Monitoring

### Prometheus Metrics

Add to your `prometheus.yml`:

```yaml
scrape_configs:
  - job_name: 'iluminara'
    static_configs:
      - targets: ['localhost:9090']
    metrics_path: '/metrics'
    scrape_interval: 15s
```

### Grafana Dashboards

Import the following dashboards:

1. **Sovereignty Compliance Dashboard**
   - Sovereignty violations over time
   - Cross-border transfers by jurisdiction
   - Consent validation success rate

2. **Audit Trail Dashboard**
   - Audit events by type
   - Chain integrity verification
   - Tamper detection alerts

3. **Data Retention Dashboard**
   - Keys by retention policy
   - Auto-shred operations
   - Storage by sovereignty zone

## Step 12: Launch All Services

```bash
# Make launch script executable
chmod +x launch_all_services.sh

# Launch with validation
./launch_all_services.sh --validate-only

# Launch all services
./launch_all_services.sh
```

## Verification Checklist

- [ ] CodeQL workflow running on push/PR
- [ ] Gitleaks scanning for secrets
- [ ] Dependabot creating security PRs
- [ ] Crypto Shredder encrypting/shredding data
- [ ] SovereignGuardrail blocking violations
- [ ] Branch protection enforcing status checks
- [ ] Fortress validation passing all phases
- [ ] Prometheus metrics exposed
- [ ] Grafana dashboards configured
- [ ] All services launching successfully

## Troubleshooting

### CodeQL Workflow Fails

```bash
# Check workflow logs
gh run list --workflow=codeql.yml

# View specific run
gh run view <run-id>

# Common fix: Update CodeQL action version
# Edit .github/workflows/codeql.yml and update to latest version
```

### Gitleaks Detects False Positives

Add to `.gitleaks.toml`:

```toml
[allowlist]
regexes = [
  '''your-false-positive-pattern'''
]
```

### Crypto Shredder Import Error

```bash
# Install cryptography
pip install cryptography

# Verify installation
python -c "from cryptography.hazmat.primitives.ciphers import Cipher; print('✅ Cryptography installed')"
```

### SovereignGuardrail Configuration Error

```bash
# Verify YAML syntax
python -c "import yaml; yaml.safe_load(open('config/sovereign_guardrail.yaml'))"

# Check environment variables
env | grep -E '(NODE_ID|JURISDICTION|GOOGLE_CLOUD_PROJECT)'
```

## Next Steps

1. **Deploy to GCP**: Follow [GCP Deployment Guide](/deployment/gcp)
2. **Configure AI Agents**: See [AI Agents Documentation](/ai-agents/overview)
3. **Set up Monitoring**: Configure [Prometheus and Grafana](/deployment/monitoring)
4. **Train Team**: Review [Compliance Documentation](/governance/compliance/matrix)

## Support

- **Documentation**: https://docs.iluminara.health
- **GitHub Issues**: https://github.com/VISENDI56/iLuminara-Core/issues
- **Security**: security@iluminara.health

## The Fortress is Built

```
╔════════════════════════════════════════════════════════════╗
║     iLuminara-Core Sovereign Health Fortress               ║
║                                                            ║
║  🛡️  Security Audit Layer: ACTIVE                         ║
║  ⚡ Nuclear IP Stack: OPERATIONAL                         ║
║  🔐 Crypto Shredder (IP-02): ENFORCING                    ║
║  🌍 14 Global Frameworks: COMPLIANT                       ║
║  📊 Golden Thread: FUSING DATA                            ║
║                                                            ║
║  Transform preventable suffering from statistical         ║
║  inevitability to historical anomaly.                     ║
╚════════════════════════════════════════════════════════════╝
```

Your Sovereign Health Fortress is now operational. 🚀
