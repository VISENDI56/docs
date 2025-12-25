# iLuminara-Core Sovereign Health Fortress - Implementation Files

This directory contains all the implementation files for the iLuminara-Core Sovereign Health Fortress security and integration stack.

## 🛡️ What's Included

### Security Audit Layer
- `.github/workflows/codeql.yml` - CodeQL SAST security scanning
- `.github/workflows/gitleaks.yml` - Gitleaks secret detection
- `.gitleaks.toml` - Secret detection configuration
- `.github/dependabot.yml` - Daily security updates

### Nuclear IP Stack
- `governance_kernel/crypto_shredder.py` - IP-02: Cryptographic data dissolution
- `config/sovereign_guardrail.yaml` - SovereignGuardrail configuration (14 global legal frameworks)

### Integrations
- `cloud_oracle/vertex_ai_shap.py` - Vertex AI + SHAP explainability (EU AI Act §6)
- `api/bio_interface.py` - Bio-Interface REST API for mobile health apps

### Validation & Deployment
- `scripts/validate_fortress.sh` - Comprehensive fortress validation script

## 📋 Installation Instructions

### Step 1: Copy Files to Your Repository

```bash
# Navigate to your iLuminara-Core repository
cd /path/to/iLuminara-Core

# Copy all files (preserving directory structure)
cp -r /path/to/repository-files/* .
```

### Step 2: Install Dependencies

```bash
# Install Python dependencies
pip install -r requirements.txt

# Additional dependencies for new features
pip install cryptography shap google-cloud-aiplatform flask-cors
```

### Step 3: Configure Environment

```bash
# Set environment variables
export NODE_ID=JOR-47
export JURISDICTION=KDPA_KE
export GOOGLE_CLOUD_PROJECT=your-project-id
export BIO_INTERFACE_PORT=8081
export ENABLE_TAMPER_PROOF_AUDIT=true
```

### Step 4: Validate the Fortress

```bash
# Make validation script executable
chmod +x scripts/validate_fortress.sh

# Run validation
./scripts/validate_fortress.sh
```

### Step 5: Enable GitHub Workflows

```bash
# Authenticate with GitHub CLI
gh auth refresh -s workflow,repo,write:packages,admin:repo_hook

# Commit and push changes
git add .
git commit -m "feat: integrate SovereignGuardrail and Nuclear IP security stack"
git push

# Enable branch protection on main
gh api repos/VISENDI56/iLuminara-Core/branches/main/protection \
  --method PUT \
  --field required_status_checks[strict]=true \
  --field required_status_checks[contexts][]=CodeQL \
  --field required_status_checks[contexts][]=Gitleaks \
  --field required_pull_request_reviews[required_approving_review_count]=1
```

### Step 6: Deploy Services

```bash
# Start Bio-Interface API
python api/bio_interface.py

# Start all services (includes dashboards)
chmod +x launch_all_services.sh
./launch_all_services.sh
```

## 🧪 Testing

### Test Crypto Shredder (IP-02)

```bash
python governance_kernel/crypto_shredder.py
```

**Expected output:**
```
🔐 Crypto Shredder initialized - Zone: africa-south1
✅ Encrypted - Key ID: a1b2c3d4e5f6g7h8
✅ Decrypted: Patient ID: 12345, Diagnosis: Malaria, Location: Dadaab
🔥 Key shredded - Data irrecoverable: a1b2c3d4e5f6g7h8
❌ Decryption after shred: None
```

### Test Vertex AI + SHAP

```bash
python cloud_oracle/vertex_ai_shap.py
```

**Expected output:**
```
🧠 Vertex AI Explainer initialized - Model: cholera-outbreak-predictor
🔍 High-risk inference detected (confidence: 95%) - Generating explanation
✅ Explanation logged to audit trail
🎯 Prediction: [[0.95, 0.05]]
📊 Confidence: 95%
⚠️ Risk Level: CRITICAL

🔍 Explanation:
   Method: SHAP
   
   Evidence Chain:
   - Primary factor: fever (35% contribution)
   - Secondary factor: diarrhea (28% contribution)
   - Contributing factor: location_risk (22% contribution)
```

### Test Bio-Interface API

```bash
# Health check
curl http://localhost:8081/health

# Submit health data
curl -X POST http://localhost:8081/api/v1/submit-health-data \
  -H "Content-Type: application/json" \
  -d '{
    "patient_id": "PAT_12345",
    "data_type": "symptom_report",
    "data": {
      "symptoms": ["fever", "cough"],
      "severity": 7
    },
    "location": {"lat": 0.0512, "lng": 40.3129, "name": "Dadaab"},
    "source": "mobile_app",
    "consent_token": "CONSENT_TOKEN_123",
    "jurisdiction": "KDPA_KE"
  }'
```

**Expected output:**
```json
{
  "status": "success",
  "submission_id": "SUB_20251220100500",
  "golden_thread_id": "GT_456",
  "verification_score": 0.8,
  "timestamp": "2025-12-20T10:05:00Z",
  "compliance": {
    "frameworks": ["GDPR Art. 6", "KDPA §37", "HIPAA §164.312"],
    "audit_trail": true,
    "sovereignty_validated": true
  }
}
```

## 📊 The 10/10 Security Stack

| Component | Protocol | Status | Benefit |
|-----------|----------|--------|---------|
| **Security Audit** | Gitleaks + CodeQL | ✅ Active | Continuous attestation of the Fortress |
| **Data Lifecycle** | IP-02 Crypto Shredder | ✅ Active | Data is dissolved, not deleted |
| **Intelligence** | IP-04 Silent Flux | ⚠️ Requires integration | AI output regulated by anxiety |
| **Connectivity** | IP-06 5DM Bridge | ⚠️ Requires mobile network | 14M+ African mobile nodes |
| **Data Fusion** | IP-05 Golden Thread | ✅ Active | Verified timelines from multiple sources |
| **Explainability** | Vertex AI + SHAP | ✅ Active | Right to Explanation (EU AI Act §6) |
| **Mobile Integration** | Bio-Interface API | ✅ Active | Golden Thread protocol for mobile apps |
| **Sovereignty** | SovereignGuardrail | ✅ Active | 14 global legal frameworks enforced |

## 🔒 Compliance Coverage

### Frameworks Enforced

- ✅ **GDPR (EU)** - Art. 6, 9, 17, 22, 30, 32
- ✅ **KDPA (Kenya)** - §37, §42
- ✅ **HIPAA (USA)** - §164.312, §164.524, §164.530(j)
- ✅ **EU AI Act** - §6, §8, §12
- ✅ **ISO 27001** - A.8.3.2, A.12.4, A.12.6
- ✅ **SOC 2** - Security, Availability, Processing Integrity
- ✅ **NIST CSF** - Identify, Protect, Detect, Respond, Recover
- ✅ **WHO IHR** - Article 6 (Notification)

## 📁 File Structure

```
.
├── .github/
│   ├── workflows/
│   │   ├── codeql.yml              # SAST security scanning
│   │   └── gitleaks.yml            # Secret scanning
│   └── dependabot.yml              # Daily security updates
├── .gitleaks.toml                  # Secret detection rules
├── config/
│   └── sovereign_guardrail.yaml    # Sovereignty configuration
├── governance_kernel/
│   └── crypto_shredder.py          # IP-02: Data dissolution
├── cloud_oracle/
│   └── vertex_ai_shap.py           # Vertex AI + SHAP integration
├── api/
│   └── bio_interface.py            # Bio-Interface REST API
└── scripts/
    └── validate_fortress.sh        # Fortress validation
```

## 🚀 Next Steps

1. **Deploy to production** - Follow the deployment guide
2. **Configure monitoring** - Set up Prometheus and Grafana
3. **Train operators** - Provide training on the Fortress architecture
4. **Conduct security audit** - Perform external security audit
5. **Enable IP-03 Acorn Protocol** - Integrate hardware attestation (TPM)
6. **Enable IP-04 Silent Flux** - Integrate operator anxiety monitoring
7. **Enable IP-06 5DM Bridge** - Integrate with mobile network operators

## 📚 Documentation

Full documentation is available at:
- **Implementation Summary:** `IMPLEMENTATION_SUMMARY.mdx`
- **Security Stack:** `security/overview.mdx`
- **Vertex AI + SHAP:** `integrations/vertex-ai-shap.mdx`
- **Bio-Interface API:** `integrations/bio-interface.mdx`

## 🆘 Support

For questions or issues:
- **GitHub Issues:** https://github.com/VISENDI56/iLuminara-Core/issues
- **Documentation:** https://docs.iluminara.health
- **Email:** support@iluminara.health

---

**The Fortress is built. Your mission: Deploy with dignity.**

🛡️ **FORTRESS STATUS: OPERATIONAL**
