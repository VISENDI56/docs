# iLuminara-Core Sovereign Health Fortress Deployment Guide

## 🛡️ The Fortress Initialization Protocol

This guide implements the complete **Nuclear IP Stack** with maximum automation through GitHub Actions and security workflows.

---

## Phase 1: Prerequisites

### 1.1 Elevate GitHub Permissions

```bash
gh auth refresh -s workflow,repo,write:packages,admin:repo_hook
```

### 1.2 Required Tools

- **Python 3.8+**
- **pip** (package manager)
- **git** (version control)
- **gh CLI** (GitHub CLI)
- **Docker** (optional, for containerized deployment)
- **Google Cloud SDK** (optional, for GCP deployment)

### 1.3 Environment Variables

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
export DATA_SOVEREIGNTY_REQUIRED=true
```

---

## Phase 2: Deploy Security Audit Layer

### 2.1 Copy Security Workflows

Copy the following files from `repository-files/` to your iLuminara-Core repository:

```bash
# From this docs repository
cp repository-files/.github/workflows/codeql.yml <your-repo>/.github/workflows/
cp repository-files/.github/workflows/gitleaks.yml <your-repo>/.github/workflows/
cp repository-files/.gitleaks.toml <your-repo>/
cp repository-files/.github/dependabot.yml <your-repo>/.github/
```

### 2.2 Commit and Push

```bash
cd <your-repo>
git add .github/workflows/codeql.yml
git add .github/workflows/gitleaks.yml
git add .gitleaks.toml
git add .github/dependabot.yml
git commit -m "feat: integrate security audit layer (CodeQL, Gitleaks, Dependabot)"
git push origin main
```

### 2.3 Enable GitHub Security Features

```bash
# Enable Dependabot alerts
gh api -X PUT /repos/VISENDI56/iLuminara-Core/vulnerability-alerts

# Enable Dependabot security updates
gh api -X PUT /repos/VISENDI56/iLuminara-Core/automated-security-fixes

# Enable secret scanning
gh api -X PUT /repos/VISENDI56/iLuminara-Core/secret-scanning
```

### 2.4 Configure Branch Protection

```bash
gh api -X PUT /repos/VISENDI56/iLuminara-Core/branches/main/protection \
  -f required_status_checks='{"strict":true,"contexts":["CodeQL","Gitleaks"]}' \
  -f enforce_admins=true \
  -f required_pull_request_reviews='{"required_approving_review_count":1}' \
  -f restrictions=null
```

---

## Phase 3: Deploy Governance Kernel

### 3.1 Copy Governance Files

```bash
# Copy Crypto Shredder (IP-02)
cp repository-files/governance_kernel/crypto_shredder.py <your-repo>/governance_kernel/

# Copy SovereignGuardrail configuration
mkdir -p <your-repo>/config
cp repository-files/config/sovereign_guardrail.yaml <your-repo>/config/
```

### 3.2 Install Dependencies

```bash
cd <your-repo>
pip install cryptography pyyaml
```

### 3.3 Test Crypto Shredder

```bash
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

### 3.4 Commit Governance Kernel

```bash
git add governance_kernel/crypto_shredder.py
git add config/sovereign_guardrail.yaml
git commit -m "feat: implement IP-02 Crypto Shredder and SovereignGuardrail config"
git push origin main
```

---

## Phase 4: Deploy Validation Script

### 4.1 Copy Validation Script

```bash
mkdir -p <your-repo>/scripts
cp repository-files/scripts/validate_fortress.sh <your-repo>/scripts/
chmod +x <your-repo>/scripts/validate_fortress.sh
```

### 4.2 Run Fortress Validation

```bash
cd <your-repo>
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

📄 Checking .github/workflows/codeql.yml... ✓ EXISTS
📄 Checking .github/workflows/gitleaks.yml... ✓ EXISTS
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

### 4.3 Commit Validation Script

```bash
git add scripts/validate_fortress.sh
git commit -m "feat: add fortress validation script"
git push origin main
```

---

## Phase 5: Integrate with Existing Services

### 5.1 Update launch_all_services.sh

Add validation to your existing launch script:

```bash
#!/bin/bash

# Validate fortress before launch
echo "🔍 Validating Sovereign Health Fortress..."
./scripts/validate_fortress.sh --validate-only

if [ $? -ne 0 ]; then
    echo "❌ Fortress validation failed. Aborting launch."
    exit 1
fi

# Continue with existing launch logic...
echo "🚀 Launching all services..."

# Your existing service launch commands here
```

### 5.2 Integrate Crypto Shredder with API

Update `api_service.py` to use Crypto Shredder:

```python
from governance_kernel.crypto_shredder import CryptoShredder, RetentionPolicy, SovereigntyZone

# Initialize Crypto Shredder
shredder = CryptoShredder(
    sovereignty_zone=SovereigntyZone.KENYA,
    enable_audit=True
)

@app.route('/api/v1/patient/register', methods=['POST'])
def register_patient():
    data = request.json
    
    # Encrypt patient data with ephemeral key
    patient_data = json.dumps(data).encode()
    encrypted_data, key_id = shredder.encrypt_with_ephemeral_key(
        data=patient_data,
        retention_policy=RetentionPolicy.HOT,
        metadata={
            'patient_id': data['patient_id'],
            'jurisdiction': 'KDPA_KE',
            'data_type': 'PHI'
        }
    )
    
    # Store encrypted data
    store_encrypted_patient_data(encrypted_data, key_id)
    
    return jsonify({
        'status': 'success',
        'patient_id': data['patient_id'],
        'key_id': key_id,
        'retention_policy': 'HOT (180 days)'
    })
```

### 5.3 Schedule Auto-Shred

Add cron job for automatic key shredding:

```bash
# Add to crontab
crontab -e

# Add this line (runs daily at 2 AM)
0 2 * * * cd /path/to/iluminara-core && python -c "from governance_kernel.crypto_shredder import CryptoShredder; CryptoShredder().auto_shred_expired_keys()"
```

---

## Phase 6: Deploy to Production

### 6.1 Local Development

```bash
# Install dependencies
pip install -r requirements.txt

# Launch all services
./launch_all_services.sh
```

### 6.2 Google Cloud Platform

```bash
# Deploy to GCP
./deploy_gcp_prototype.sh
```

This script:
1. Enables required GCP services
2. Deploys FRENASA AI Engine to Cloud Run
3. Sets up HSTPU Forecaster on Vertex AI
4. Creates HSML Ledger using Cloud Spanner
5. Generates demo outbreak data in BigQuery
6. Launches dashboard on Cloud Run

### 6.3 Docker

```bash
# Build and run
docker-compose up -d
```

---

## Phase 7: Verify Deployment

### 7.1 Check Security Workflows

Visit your GitHub repository:
- **Actions** tab → Verify CodeQL and Gitleaks workflows are running
- **Security** tab → Check Dependabot alerts
- **Settings** → **Branches** → Verify branch protection rules

### 7.2 Test API Endpoints

```bash
# Health check
curl http://localhost:8080/health

# Test voice processing
curl -X POST http://localhost:8080/process-voice \
  -H "Content-Type: audio/wav" \
  --data-binary @swahili-symptom.wav

# Test outbreak prediction
curl -X POST http://localhost:8080/predict \
  -H "Content-Type: application/json" \
  -d '{"location": {"lat": 0.4221, "lng": 40.2255}, "symptoms": ["diarrhea", "vomiting"]}'
```

### 7.3 Verify Crypto Shredder

```python
from governance_kernel.crypto_shredder import CryptoShredder

shredder = CryptoShredder()

# Check key status
status = shredder.get_key_status('your_key_id')
print(status)

# Run auto-shred
shredded_count = shredder.auto_shred_expired_keys()
print(f"Shredded {shredded_count} expired keys")
```

---

## Phase 8: Monitoring & Maintenance

### 8.1 Prometheus Metrics

Access metrics at: `http://localhost:9090/metrics`

Key metrics:
- `sovereignty_violations_total`
- `cross_border_transfers_total`
- `high_risk_inferences_total`
- `keys_shredded_total`

### 8.2 Grafana Dashboards

Access dashboards at: `http://localhost:3000`

Dashboards:
- **Sovereignty Compliance** - Real-time compliance monitoring
- **Audit Trail** - Tamper-proof audit visualization
- **Data Retention** - Key lifecycle and auto-shred status

### 8.3 Log Monitoring

```bash
# View API logs
tail -f logs/api.log

# View dashboard logs
tail -f logs/dashboard.log

# View audit logs
tail -f logs/audit.log
```

---

## The 10/10 Security Stack Summary

| Component | Status | Benefit |
|-----------|--------|---------|
| **CodeQL SAST** | ✅ Active | Continuous security scanning |
| **Gitleaks** | ✅ Active | Secret detection |
| **Dependabot** | ✅ Active | Daily security updates |
| **IP-02 Crypto Shredder** | ✅ Active | Data dissolution |
| **SovereignGuardrail** | ✅ Active | 14 global frameworks enforced |
| **Tamper-proof Audit** | ✅ Active | Immutable audit trail |
| **IP-05 Golden Thread** | ✅ Active | Data fusion engine |
| **Branch Protection** | ✅ Active | PR + status checks required |
| **Hardware Attestation** | ⚠️ Pending | Requires TPM integration |
| **IP-06 5DM Bridge** | ⚠️ Pending | Requires mobile network |

---

## Troubleshooting

### Issue: CodeQL workflow fails

**Solution:** Ensure Python 3.8+ is installed and all dependencies are in `requirements.txt`

### Issue: Gitleaks detects false positives

**Solution:** Add patterns to `.gitleaks.toml` allowlist

### Issue: Crypto Shredder key not found

**Solution:** Check `./keys` directory exists and has proper permissions

### Issue: SovereignGuardrail blocks legitimate action

**Solution:** Review `config/sovereign_guardrail.yaml` and adjust enforcement level

---

## Next Steps

1. **Configure Jurisdiction** - Update `config/sovereign_guardrail.yaml` for your region
2. **Enable Hardware Attestation** - Integrate TPM for Acorn Protocol (IP-03)
3. **Deploy Mobile Apps** - Integrate Bio-Interface API with Flutter/React apps
4. **Set Up Monitoring** - Configure Prometheus + Grafana dashboards
5. **Train Operators** - Conduct fortress validation drills

---

## Support

- **Documentation:** https://docs.iluminara.health
- **GitHub Issues:** https://github.com/VISENDI56/iLuminara-Core/issues
- **Security:** security@iluminara.health

---

**The Fortress is now built. Your Sovereign Health Architecture is operational.**

🛡️ **FORTRESS STATUS: OPERATIONAL**
