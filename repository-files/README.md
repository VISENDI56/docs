# iLuminara-Core Sovereign Health Fortress - Implementation Files

This directory contains all the files needed to implement the complete Sovereign Health Fortress security and integration stack for iLuminara-Core.

## 🛡️ The Fortress Stack

| Component | File | Purpose |
|-----------|------|---------|
| **CodeQL SAST** | `.github/workflows/codeql.yml` | Continuous security scanning |
| **Gitleaks** | `.github/workflows/gitleaks.yml` | Secret detection |
| **Gitleaks Config** | `.gitleaks.toml` | Secret scanning rules |
| **Dependabot** | `.github/dependabot.yml` | Daily security updates |
| **Crypto Shredder** | `governance_kernel/crypto_shredder.py` | IP-02: Data dissolution |
| **SovereignGuardrail Config** | `config/sovereign_guardrail.yaml` | 14 global legal frameworks |
| **Fortress Validator** | `scripts/validate_fortress.sh` | Complete stack validation |

## 📋 Installation Instructions

### Step 1: Copy Files to Your Repository

```bash
# Navigate to your iLuminara-Core repository
cd /path/to/iLuminara-Core

# Copy GitHub workflows
mkdir -p .github/workflows
cp repository-files/.github/workflows/codeql.yml .github/workflows/
cp repository-files/.github/workflows/gitleaks.yml .github/workflows/

# Copy Gitleaks config
cp repository-files/.gitleaks.toml .

# Copy Dependabot config
cp repository-files/.github/dependabot.yml .github/

# Copy Crypto Shredder
cp repository-files/governance_kernel/crypto_shredder.py governance_kernel/

# Copy SovereignGuardrail config
mkdir -p config
cp repository-files/config/sovereign_guardrail.yaml config/

# Copy validation script
mkdir -p scripts
cp repository-files/scripts/validate_fortress.sh scripts/
chmod +x scripts/validate_fortress.sh
```

### Step 2: Install Dependencies

```bash
# Install Python dependencies
pip install cryptography google-cloud-kms google-cloud-spanner

# Install GitHub CLI (if not already installed)
# macOS
brew install gh

# Linux
curl -fsSL https://cli.github.com/packages/githubcli-archive-keyring.gpg | sudo dd of=/usr/share/keyrings/githubcli-archive-keyring.gpg
echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/githubcli-archive-keyring.gpg] https://cli.github.com/packages stable main" | sudo tee /etc/apt/sources.list.d/github-cli.list > /dev/null
sudo apt update
sudo apt install gh
```

### Step 3: Authenticate GitHub CLI

```bash
# Authenticate with GitHub
gh auth login

# Refresh with required permissions
gh auth refresh -s workflow,repo,write:packages,admin:repo_hook
```

### Step 4: Enable GitHub Security Features

```bash
# Enable CodeQL
gh api repos/VISENDI56/iLuminara-Core/code-scanning/default-setup -X PATCH -f state=configured

# Enable Dependabot security updates
gh api repos/VISENDI56/iLuminara-Core/vulnerability-alerts -X PUT

# Enable Dependabot alerts
gh api repos/VISENDI56/iLuminara-Core/automated-security-fixes -X PUT
```

### Step 5: Configure Environment Variables

```bash
# Add to your .bashrc or .zshrc
export NODE_ID=JOR-47
export JURISDICTION=KDPA_KE
export GOOGLE_CLOUD_PROJECT=your-project-id
export GCP_REGION=africa-south1
export ENABLE_TAMPER_PROOF_AUDIT=true
```

### Step 6: Commit and Push

```bash
# Add all files
git add .github/ .gitleaks.toml governance_kernel/crypto_shredder.py config/ scripts/

# Commit with fortress message
git commit -m "feat: integrate SovereignGuardrail and Nuclear IP security stack

- Add CodeQL SAST scanning (GDPR Art. 32, ISO 27001 A.12.6)
- Add Gitleaks secret detection (NIST SP 800-53 IA-5)
- Implement IP-02 Crypto Shredder (data dissolution)
- Configure SovereignGuardrail (14 global legal frameworks)
- Add Dependabot daily security updates
- Add fortress validation script

The Sovereign Health Fortress is now operational."

# Push to main
git push origin main
```

### Step 7: Enable Branch Protection

```bash
# Protect main branch
gh api repos/VISENDI56/iLuminara-Core/branches/main/protection -X PUT -f required_status_checks[strict]=true -f required_status_checks[contexts][]=CodeQL -f required_status_checks[contexts][]=Gitleaks -f required_pull_request_reviews[required_approving_review_count]=1 -f enforce_admins=true
```

### Step 8: Validate the Fortress

```bash
# Run validation script
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

📄 Checking .github/workflows/codeql.yml... ✓ OPERATIONAL
   └─ SAST security scanning (GDPR Art. 32, ISO 27001 A.12.6)
📄 Checking .github/workflows/gitleaks.yml... ✓ OPERATIONAL
   └─ Secret scanning (NIST SP 800-53 IA-5)
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

## 🔐 Nuclear IP Stack Status

| IP | Name | Status | File |
|----|------|--------|------|
| **IP-02** | Crypto Shredder | ✅ ACTIVE | `governance_kernel/crypto_shredder.py` |
| **IP-03** | Acorn Protocol | ⚠️ REQUIRES HARDWARE | TPM integration needed |
| **IP-04** | Silent Flux | ⚠️ REQUIRES INTEGRATION | Anxiety monitoring needed |
| **IP-05** | Golden Thread | ✅ ACTIVE | `edge_node/sync_protocol/` |
| **IP-06** | 5DM Bridge | ⚠️ REQUIRES MOBILE NETWORK | API injection needed |

## 📊 Compliance Coverage

The Fortress enforces 14 global legal frameworks:

| Framework | Status | Configuration |
|-----------|--------|---------------|
| GDPR (EU) | ✅ Enforced | `config/sovereign_guardrail.yaml` |
| KDPA (Kenya) | ✅ Enforced | `config/sovereign_guardrail.yaml` |
| HIPAA (USA) | ✅ Enforced | `config/sovereign_guardrail.yaml` |
| POPIA (South Africa) | ✅ Enforced | `config/sovereign_guardrail.yaml` |
| PIPEDA (Canada) | ✅ Enforced | `config/sovereign_guardrail.yaml` |
| EU AI Act | ✅ Enforced | `config/sovereign_guardrail.yaml` |
| ISO 27001 | ✅ Enforced | CodeQL + Gitleaks |
| SOC 2 | ✅ Enforced | Tamper-proof audit |
| NIST CSF | ✅ Enforced | Security workflows |
| CCPA (California) | ✅ Enforced | `config/sovereign_guardrail.yaml` |
| HITECH (USA) | ✅ Enforced | `config/sovereign_guardrail.yaml` |

## 🚀 Next Steps

1. **Configure GCP Integration**
   ```bash
   # Set up Cloud KMS for production key management
   gcloud kms keyrings create iluminara-keys --location=africa-south1
   gcloud kms keys create crypto-shredder-key --location=africa-south1 --keyring=iluminara-keys --purpose=encryption
   ```

2. **Enable Tamper-Proof Audit**
   ```bash
   # Create Cloud Spanner instance for audit trail
   gcloud spanner instances create iluminara-audit --config=regional-africa-south1 --nodes=1
   gcloud spanner databases create audit-trail --instance=iluminara-audit
   ```

3. **Deploy to Production**
   ```bash
   # Run GCP deployment script
   chmod +x deploy_gcp_prototype.sh
   ./deploy_gcp_prototype.sh
   ```

4. **Monitor Security**
   - View CodeQL results: https://github.com/VISENDI56/iLuminara-Core/security/code-scanning
   - View Dependabot alerts: https://github.com/VISENDI56/iLuminara-Core/security/dependabot
   - View Gitleaks results: https://github.com/VISENDI56/iLuminara-Core/security/secret-scanning

## 📚 Documentation

Complete documentation is available at:
- **Security Stack**: `/security/overview`
- **Crypto Shredder**: `/security/crypto-shredder`
- **Vertex AI + SHAP**: `/integration/vertex-ai-shap`
- **Bio-Interface API**: `/integration/bio-interface`

## 🆘 Troubleshooting

### CodeQL workflow fails
```bash
# Check workflow logs
gh run list --workflow=codeql.yml
gh run view <run-id> --log
```

### Gitleaks detects false positives
Edit `.gitleaks.toml` to add allowlist patterns:
```toml
[allowlist]
regexes = [
  '''your-false-positive-pattern'''
]
```

### Crypto Shredder key storage issues
```bash
# Ensure keys directory exists
mkdir -p ./keys
chmod 700 ./keys
```

## 🔗 Related Resources

- [iLuminara-Core Repository](https://github.com/VISENDI56/iLuminara-Core)
- [Documentation Site](https://docs.iluminara.health)
- [Command Console](https://iluminara-war-room.streamlit.app)
- [Transparency Audit](https://iluminara-audit.streamlit.app)

---

**The Fortress is not built. It is continuously attested.**

🛡️ iLuminara-Core Sovereign Health Fortress
