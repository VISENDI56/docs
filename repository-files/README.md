# iLuminara-Core Repository Files

This directory contains all the files that need to be copied to your `VISENDI56/iLuminara-Core` repository to implement the complete Sovereign Health Fortress.

## 🚀 Quick Start

### 1. Copy files to your repository

```bash
# Navigate to your iLuminara-Core repository
cd /path/to/iLuminara-Core

# Copy all files from this directory
cp -r /path/to/docs/repository-files/* .
```

### 2. Make scripts executable

```bash
chmod +x scripts/*.sh
```

### 3. Set up branch protection

```bash
# Authenticate with GitHub
gh auth login

# Refresh permissions
gh auth refresh -s workflow,repo,write:packages,admin:repo_hook

# Run branch protection setup
./scripts/setup_branch_protection.sh
```

### 4. Validate the fortress

```bash
./scripts/validate_fortress.sh
```

### 5. Commit and push

```bash
git add .
git commit -m "feat: integrate Sovereign Health Fortress security stack"
git push
```

## 📁 Directory Structure

```
repository-files/
├── .github/
│   ├── workflows/
│   │   ├── codeql.yml              # CodeQL SAST scanning
│   │   └── gitleaks.yml            # Secret scanning
│   └── dependabot.yml              # Daily security updates
├── .gitleaks.toml                  # Gitleaks configuration
├── governance_kernel/
│   └── crypto_shredder.py          # IP-02: Data dissolution
├── cloud_oracle/
│   └── vertex_ai_explainability.py # Vertex AI + SHAP integration
├── edge_node/
│   └── bio_interface_api.py        # Mobile health apps API
├── config/
│   └── sovereign_guardrail.yaml    # Sovereignty configuration
├── scripts/
│   ├── setup_branch_protection.sh  # Automate GitHub security
│   └── validate_fortress.sh        # Validate complete stack
└── README.md                       # This file
```

## 🛡️ Components

### Security Audit Layer

#### CodeQL Workflow (`.github/workflows/codeql.yml`)
- **Purpose:** Static Application Security Testing (SAST)
- **Languages:** Python, JavaScript
- **Schedule:** Weekly + on push/PR
- **Compliance:** GDPR Art. 32, ISO 27001 A.12.6

#### Gitleaks Workflow (`.github/workflows/gitleaks.yml`)
- **Purpose:** Secret scanning
- **Schedule:** Daily at 2 AM UTC
- **Compliance:** NIST SP 800-53 IA-5, HIPAA §164.312(a)(2)(i)

#### Gitleaks Configuration (`.gitleaks.toml`)
- **Purpose:** Custom secret detection rules
- **Features:** GCP, AWS, GitHub token detection
- **Sovereignty:** Flags AWS keys as sovereignty violations

#### Dependabot (`.github/dependabot.yml`)
- **Purpose:** Automated dependency updates
- **Schedule:** Daily security updates
- **Ecosystems:** Python, npm, Docker, GitHub Actions

### Governance Kernel

#### Crypto Shredder (`governance_kernel/crypto_shredder.py`)
- **IP-02:** Data is not deleted; it is cryptographically dissolved
- **Features:**
  - Ephemeral key encryption (AES-256-GCM)
  - Auto-shred after retention period
  - Tamper-proof audit trail
- **Compliance:** GDPR Art. 17, HIPAA §164.530(j), NIST SP 800-88

#### SovereignGuardrail Configuration (`config/sovereign_guardrail.yaml`)
- **Purpose:** Enforce 14 global legal frameworks
- **Frameworks:** GDPR, KDPA, HIPAA, POPIA, EU AI Act, ISO 27001, SOC 2, NIST CSF
- **Features:**
  - Data sovereignty enforcement
  - Cross-border transfer restrictions
  - Retention policies
  - Audit trail configuration

### Cloud Oracle

#### Vertex AI Explainability (`cloud_oracle/vertex_ai_explainability.py`)
- **Purpose:** Right to Explanation for high-risk AI
- **Features:**
  - SHAP value calculation
  - Feature importance ranking
  - Evidence chain generation
  - Compliance validation
- **Compliance:** EU AI Act §6, GDPR Art. 22

### Edge Node

#### Bio-Interface API (`edge_node/bio_interface_api.py`)
- **Purpose:** Mobile health apps integration
- **Features:**
  - Health report submission
  - Golden Thread data fusion
  - Outbreak risk calculation
  - Sovereignty validation
- **Endpoints:**
  - `POST /api/v1/report` - Submit health report
  - `GET /api/v1/report/:id` - Get report status
  - `POST /api/v1/outbreak/risk` - Calculate outbreak risk
  - `POST /api/v1/sync` - Sync Golden Thread

### Scripts

#### Branch Protection Setup (`scripts/setup_branch_protection.sh`)
- **Purpose:** Automate GitHub security configuration
- **Features:**
  - Branch protection rules
  - Required status checks (CodeQL, Gitleaks)
  - Pull request requirements
  - Dependabot enablement
  - Secret scanning enablement

#### Fortress Validation (`scripts/validate_fortress.sh`)
- **Purpose:** Validate complete security stack
- **Phases:**
  1. Security Audit Layer
  2. Governance Kernel
  3. Edge Node & AI Agents
  4. Cloud Oracle
  5. Python Dependencies
  6. Environment Configuration
  7. Nuclear IP Stack Status

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

# API
export API_HOST=0.0.0.0
export API_PORT=8080
```

### Sovereignty Configuration

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
      - "africa-south1"
    enforcement_level: "STRICT"
```

## 📊 Nuclear IP Stack

| IP | Name | Status | Implementation |
|----|------|--------|----------------|
| IP-02 | Crypto Shredder | ✅ Active | `governance_kernel/crypto_shredder.py` |
| IP-03 | Acorn Protocol | ⚠️ Requires Hardware | TPM attestation needed |
| IP-04 | Silent Flux | ⚠️ Requires Integration | Anxiety monitoring needed |
| IP-05 | Golden Thread | ✅ Active | `edge_node/sync_protocol/` |
| IP-06 | 5DM Bridge | ⚠️ Requires Mobile Network | Mobile integration needed |

## 🧪 Testing

### Test Crypto Shredder

```bash
python governance_kernel/crypto_shredder.py
```

### Test Vertex AI Explainability

```bash
python cloud_oracle/vertex_ai_explainability.py
```

### Test Bio-Interface API

```bash
# Start API
python edge_node/bio_interface_api.py

# Test health report submission
curl -X POST http://localhost:8080/api/v1/report \
  -H "Content-Type: application/json" \
  -d '{
    "location": {"lat": 0.4221, "lng": 40.2255},
    "symptoms": ["fever", "cough"],
    "severity": 7,
    "source": "mobile_app"
  }'
```

## 🔒 Security

### Branch Protection

All commits to `main` require:
- ✅ Passing CodeQL scan
- ✅ Passing Gitleaks scan
- ✅ 1 approving review
- ✅ All conversations resolved

### Secret Scanning

Gitleaks detects:
- GCP API keys
- AWS access keys (flagged as sovereignty violation)
- GitHub tokens
- Private keys
- JWT tokens

### Dependabot

Daily security updates for:
- Python packages
- npm packages
- Docker images
- GitHub Actions

## 📚 Documentation

Complete documentation available at: [https://docs.iluminara.health](https://docs.iluminara.health)

### Key Pages

- **Quick Start:** `/quickstart`
- **Architecture:** `/architecture/overview`
- **Governance:** `/governance/overview`
- **Security:** `/security/overview`
- **API Reference:** `/api-reference/overview`
- **Deployment:** `/deployment/overview`

## 🚨 Compliance

The Sovereign Health Fortress enforces 14 global legal frameworks:

| Framework | Region | Status |
|-----------|--------|--------|
| GDPR | 🇪🇺 EU | ✅ Enforced |
| KDPA | 🇰🇪 Kenya | ✅ Enforced |
| HIPAA | 🇺🇸 USA | ✅ Enforced |
| POPIA | 🇿🇦 South Africa | ✅ Enforced |
| EU AI Act | 🇪🇺 EU | ✅ Enforced |
| ISO 27001 | 🌐 Global | ✅ Enforced |
| SOC 2 | 🇺🇸 USA | ✅ Enforced |
| NIST CSF | 🇺🇸 USA | ✅ Enforced |

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

All PRs must pass:
- CodeQL security scan
- Gitleaks secret scan
- Code review

## 📄 License

See LICENSE file in the main repository.

## 🆘 Support

- **Documentation:** https://docs.iluminara.health
- **Issues:** https://github.com/VISENDI56/iLuminara-Core/issues
- **Email:** support@iluminara.health

## 🎯 Mission

> Transform preventable suffering from statistical inevitability to historical anomaly.

---

**The Fortress is not built. It is continuously attested.**
