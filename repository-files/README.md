# iLuminara-Core Repository Files

This directory contains all the files needed to implement the **Sovereign Health Fortress** security and integration stack for iLuminara-Core.

## 📁 Directory Structure

```
repository-files/
├── .github/
│   ├── workflows/
│   │   ├── codeql.yml          # SAST security scanning
│   │   └── gitleaks.yml        # Secret detection
│   └── dependabot.yml          # Daily security updates
├── .gitleaks.toml              # Gitleaks configuration
├── governance_kernel/
│   └── crypto_shredder.py      # IP-02: Data dissolution
├── config/
│   └── sovereign_guardrail.yaml # SovereignGuardrail configuration
├── scripts/
│   └── validate_fortress.sh    # Fortress validation script
├── SETUP_GUIDE.md              # Complete setup instructions
└── README.md                   # This file
```

## 🛡️ What's Included

### Security Audit Layer

1. **CodeQL Workflow** (`.github/workflows/codeql.yml`)
   - SAST security scanning for Python and JavaScript
   - Runs on push, PR, and weekly schedule
   - Compliance: GDPR Art. 32, ISO 27001 A.12.6

2. **Gitleaks Workflow** (`.github/workflows/gitleaks.yml`)
   - Secret detection for API keys, tokens, credentials
   - Runs daily at 2 AM UTC
   - Compliance: NIST SP 800-53 IA-5, HIPAA §164.312(a)(2)(i)

3. **Gitleaks Configuration** (`.gitleaks.toml`)
   - Custom rules for GCP, AWS, GitHub, Slack tokens
   - Sovereignty violation detection
   - Allowlist for test files

4. **Dependabot** (`.github/dependabot.yml`)
   - Daily security updates for Python, npm, Docker
   - Grouped updates for security, Google Cloud, AI/ML
   - Auto-merge for security patches

### Governance Kernel

5. **Crypto Shredder** (`governance_kernel/crypto_shredder.py`)
   - IP-02: Data is not deleted; it is cryptographically dissolved
   - Ephemeral key encryption with auto-shred
   - Retention policies: HOT (180d), WARM (365d), COLD (1825d)
   - Compliance: GDPR Art. 17, HIPAA §164.530(j), NIST SP 800-88

6. **SovereignGuardrail Config** (`config/sovereign_guardrail.yaml`)
   - 14 global legal frameworks enforcement
   - Data sovereignty rules (allowed/blocked zones)
   - Right to Explanation (SHAP integration)
   - Consent management and retention policies
   - Tamper-proof audit configuration

### Validation & Setup

7. **Fortress Validator** (`scripts/validate_fortress.sh`)
   - 7-phase validation of complete stack
   - Security audit, governance kernel, edge node, cloud oracle
   - Nuclear IP stack status check
   - Environment configuration validation

8. **Setup Guide** (`SETUP_GUIDE.md`)
   - Step-by-step implementation instructions
   - Branch protection configuration
   - Secrets management
   - Integrated architecture examples

## 🚀 Quick Start

### 1. Copy Files to Your Repository

```bash
# Navigate to your iLuminara-Core repository
cd /path/to/iLuminara-Core

# Copy all files
cp -r /path/to/docs/repository-files/.github .
cp /path/to/docs/repository-files/.gitleaks.toml .
cp /path/to/docs/repository-files/governance_kernel/crypto_shredder.py governance_kernel/
mkdir -p config
cp /path/to/docs/repository-files/config/sovereign_guardrail.yaml config/
mkdir -p scripts
cp /path/to/docs/repository-files/scripts/validate_fortress.sh scripts/
chmod +x scripts/validate_fortress.sh
```

### 2. Commit and Push

```bash
git add .
git commit -m "feat: integrate SovereignGuardrail and Nuclear IP security stack"
git push origin main
```

### 3. Validate the Fortress

```bash
./scripts/validate_fortress.sh
```

## 📋 Implementation Checklist

- [ ] Copy all files to repository
- [ ] Commit and push changes
- [ ] Enable branch protection on `main`
- [ ] Configure GitHub secrets (GCP_PROJECT_ID, SLACK_WEBHOOK_URL)
- [ ] Run fortress validation script
- [ ] Verify CodeQL workflow runs successfully
- [ ] Verify Gitleaks workflow runs successfully
- [ ] Test Crypto Shredder with sample data
- [ ] Configure SovereignGuardrail for your jurisdiction
- [ ] Deploy to GCP (optional)

## 🔐 Security Workflows

### CodeQL (SAST)

- **Trigger**: Push to main/develop, PR, weekly schedule
- **Languages**: Python, JavaScript
- **Queries**: security-extended, security-and-quality
- **Compliance**: GDPR Art. 32, ISO 27001 A.12.6

### Gitleaks (Secret Scanning)

- **Trigger**: Push to main/develop, PR, daily schedule
- **Detection**: API keys, tokens, credentials, private keys
- **Compliance**: NIST SP 800-53 IA-5, HIPAA §164.312(a)(2)(i)

### Dependabot (Security Updates)

- **Frequency**: Daily for Python/npm, weekly for GitHub Actions/Docker
- **Groups**: security, google-cloud, ai-ml
- **Auto-merge**: Security patches only

## 🌍 Sovereignty Enforcement

The SovereignGuardrail enforces data sovereignty across 14 global legal frameworks:

| Framework | Region | Key Articles |
|-----------|--------|--------------|
| GDPR | 🇪🇺 EU | Art. 9, 17, 22, 30, 32 |
| KDPA | 🇰🇪 Kenya | §37, §42 |
| HIPAA | 🇺🇸 USA | §164.312, §164.530(j) |
| POPIA | 🇿🇦 South Africa | §11, §14 |
| EU AI Act | 🇪🇺 EU | §6, §8, §12 |
| ISO 27001 | 🌐 Global | A.8.3.2, A.12.4, A.12.6 |
| SOC 2 | 🇺🇸 USA | Security, Availability, Processing Integrity |
| NIST CSF | 🇺🇸 USA | Identify, Protect, Detect, Respond, Recover |

## ⚡ Nuclear IP Stack

### IP-02: Crypto Shredder ✅
Data is not deleted; it is cryptographically dissolved.

### IP-03: Acorn Protocol ⚠️
Somatic security (posture + location + stillness). Requires hardware attestation.

### IP-04: Silent Flux ⚠️
Anxiety-regulated AI output. Requires integration with operator monitoring.

### IP-05: Golden Thread ✅
Quantum entanglement logic to fuse vague signals into verified timelines.

### IP-06: 5DM Bridge ⚠️
API-level injection into 14M+ African mobile nodes. Requires mobile network integration.

## 📊 Validation Phases

The fortress validator checks:

1. **Security Audit Layer** - CodeQL, Gitleaks, Dependabot
2. **Governance Kernel** - SovereignGuardrail, Crypto Shredder, Ethical Engine
3. **Edge Node & AI Agents** - FRENASA Engine, Golden Thread
4. **Cloud Oracle** - API service, Dashboard, Deployment scripts
5. **Python Dependencies** - Critical packages installed
6. **Environment Configuration** - NODE_ID, JURISDICTION, GCP_PROJECT_ID
7. **Nuclear IP Stack Status** - IP-02, IP-05 active

## 🔧 Configuration

### Environment Variables

```bash
# Node identification
export NODE_ID=JOR-47
export JURISDICTION=KDPA_KE

# GCP configuration
export GOOGLE_CLOUD_PROJECT=your-project-id
export GCP_REGION=us-central1

# Governance
export ENABLE_TAMPER_PROOF_AUDIT=true
export RETENTION_MAX_DAYS=1825
```

### SovereignGuardrail

Edit `config/sovereign_guardrail.yaml`:

```yaml
jurisdiction:
  primary: "KDPA_KE"  # Your primary jurisdiction
  secondary:
    - "GDPR_EU"
    - "POPIA_ZA"

sovereignty:
  data_residency:
    enabled: true
    allowed_zones:
      - "africa-south1"  # Your allowed zones
    enforcement_level: "STRICT"
```

## 📚 Documentation

- **Setup Guide**: `SETUP_GUIDE.md` - Complete implementation instructions
- **Security Stack**: `/security/overview.mdx` - Security architecture
- **Crypto Shredder**: `/security/crypto-shredder.mdx` - IP-02 deep dive
- **Vertex AI + SHAP**: `/security/vertex-ai-shap.mdx` - Right to Explanation
- **Bio-Interface API**: `/api-reference/bio-interface.mdx` - Mobile app integration

## 🆘 Troubleshooting

### CodeQL fails
```bash
# Reduce analysis scope in .github/workflows/codeql.yml
paths-ignore:
  - '**/test/**'
  - '**/node_modules/**'
```

### Gitleaks false positives
```bash
# Add to .gitleaks.toml allowlist
[allowlist]
paths = ['''.*_test\.py''']
```

### Branch protection blocks pushes
```bash
# Create feature branch
git checkout -b feature/my-changes
git push origin feature/my-changes
# Create PR via GitHub UI
```

## 📞 Support

- **Documentation**: https://docs.iluminara.health
- **GitHub Issues**: https://github.com/VISENDI56/iLuminara-Core/issues
- **Security**: security@iluminara.health

---

**The Fortress is ready.** Follow `SETUP_GUIDE.md` to complete the implementation.
