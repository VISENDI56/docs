# iLuminara-Core Sovereign Health Fortress Setup Guide

This guide walks you through setting up the complete Nuclear IP Stack with maximum automation.

## 🛡️ The Fortress Architecture

You are not just installing tools; you are initializing a **Sovereign Health Fortress**.

## Step 1: Elevate Agent Permissions

Before starting, ensure your Codespace has the required permissions:

```bash
gh auth refresh -s workflow,repo,write:packages,admin:repo_hook
```

This grants:
- `workflow` - Modify GitHub Actions workflows
- `repo` - Full repository access
- `write:packages` - Publish packages
- `admin:repo_hook` - Configure webhooks and branch protection

## Step 2: Copy Files to Repository

All necessary files have been generated in the `repository-files/` directory. Copy them to your iLuminara-Core repository:

```bash
# Navigate to your iLuminara-Core repository
cd /path/to/iLuminara-Core

# Copy GitHub workflows
mkdir -p .github/workflows
cp /path/to/docs/repository-files/.github/workflows/codeql.yml .github/workflows/
cp /path/to/docs/repository-files/.github/workflows/gitleaks.yml .github/workflows/
cp /path/to/docs/repository-files/.github/dependabot.yml .github/

# Copy Gitleaks configuration
cp /path/to/docs/repository-files/.gitleaks.toml .

# Copy Crypto Shredder implementation
cp /path/to/docs/repository-files/governance_kernel/crypto_shredder.py governance_kernel/

# Copy SovereignGuardrail configuration
mkdir -p config
cp /path/to/docs/repository-files/config/sovereign_guardrail.yaml config/

# Copy validation script
mkdir -p scripts
cp /path/to/docs/repository-files/scripts/validate_fortress.sh scripts/
chmod +x scripts/validate_fortress.sh
```

## Step 3: Commit and Push

```bash
git add .
git commit -m "feat: integrate SovereignGuardrail and Nuclear IP security stack

- Add CodeQL SAST scanning (GDPR Art. 32, ISO 27001 A.12.6)
- Add Gitleaks secret detection (NIST SP 800-53 IA-5)
- Implement IP-02 Crypto Shredder (data dissolution)
- Configure SovereignGuardrail (14 global legal frameworks)
- Add Dependabot daily security updates
- Add fortress validation script"

git push origin main
```

## Step 4: Enable Branch Protection

Use GitHub CLI to enable branch protection on `main`:

```bash
# Require pull requests
gh api repos/:owner/:repo/branches/main/protection \
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
   - ✅ Require pull request reviews (1 approval)
   - ✅ Require status checks to pass (CodeQL, Gitleaks)
   - ✅ Require branches to be up to date
   - ✅ Include administrators

## Step 5: Configure Secrets

Add required secrets to your repository:

```bash
# GitHub token (for workflows)
gh secret set GITHUB_TOKEN --body "$GITHUB_TOKEN"

# GCP credentials (if using cloud)
gh secret set GCP_PROJECT_ID --body "your-project-id"
gh secret set GCP_SA_KEY --body "$(cat service-account-key.json)"

# Slack webhook (for alerts)
gh secret set SLACK_WEBHOOK_URL --body "https://hooks.slack.com/services/..."
```

## Step 6: Validate the Fortress

Run the validation script to ensure all components are operational:

```bash
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
   └─ SAST security scanning (GDPR Art. 32, ISO 27001 A.12.6)
📄 Checking .github/workflows/gitleaks.yml... ✓ EXISTS
   └─ Secret scanning (NIST SP 800-53 IA-5)
📄 Checking .gitleaks.toml... ✓ EXISTS
   └─ Secret detection rules
📄 Checking .github/dependabot.yml... ✓ EXISTS
   └─ Daily security updates

═══════════════════════════════════════════════════════════
PHASE 2: Governance Kernel (Nuclear IP Stack)
═══════════════════════════════════════════════════════════

📁 Checking governance_kernel... ✓ EXISTS
   └─ Law-as-code enforcement engine
📄 Checking governance_kernel/crypto_shredder.py... ✓ EXISTS
   └─ IP-02: Data dissolution (not deletion)

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

## Step 7: Integrated Architecture Implementation

### A. Model Integration (Vertex AI + SHAP)

Configure Vertex AI models to provide "Right to Explanation":

```python
from google.cloud import aiplatform
import shap

# Initialize Vertex AI
aiplatform.init(project='your-project-id', location='us-central1')

# Every high-risk inference triggers SHAP analysis
endpoint = aiplatform.Endpoint('projects/.../endpoints/...')
prediction = endpoint.predict(instances=[patient_features])

# Generate SHAP explanation
explainer = shap.TreeExplainer(model)
shap_values = explainer.shap_values(patient_features)

# Validate with SovereignGuardrail
from governance_kernel.vector_ledger import SovereignGuardrail

guardrail = SovereignGuardrail()
guardrail.validate_action(
    action_type='High_Risk_Inference',
    payload={
        'inference': 'cholera_diagnosis',
        'confidence_score': 0.92,
        'explanation': shap_values,
        'evidence_chain': ['fever', 'diarrhea', 'dehydration']
    },
    jurisdiction='EU_AI_ACT'
)
```

### B. App Integration (Bio-Interface)

Set up the REST API for Mobile Health Apps:

```python
from flask import Flask, request, jsonify
from edge_node.sync_protocol.golden_thread import GoldenThread
from governance_kernel.vector_ledger import SovereignGuardrail

app = Flask(__name__)
gt = GoldenThread()
guardrail = SovereignGuardrail()

@app.route('/v1/cbs/report', methods=['POST'])
def submit_cbs_report():
    data = request.json
    
    # Validate sovereignty
    guardrail.validate_action(
        action_type='Data_Transfer',
        payload={
            'data_type': 'PHI',
            'source': 'Mobile_App',
            'destination': 'Edge_Node',
            'consent_token': data['consent_token']
        },
        jurisdiction=data['jurisdiction']
    )
    
    # Create CBS signal
    fused = gt.fuse_data_streams(
        cbs_signal={
            'location': data['location'],
            'symptom': data['symptoms'][0],
            'timestamp': data['timestamp']
        },
        patient_id=data['patient_id']
    )
    
    return jsonify({
        'status': 'success',
        'verification_score': fused.verification_score,
        'alert_level': 'HIGH' if fused.verification_score > 0.8 else 'MEDIUM'
    })
```

### C. Compliance & Protection (The Shield)

The SovereignGuardrail automatically blocks any PII/PHI from leaving sovereign territory:

```python
from governance_kernel.vector_ledger import SovereignGuardrail, SovereigntyViolationError

guardrail = SovereignGuardrail()

# This will BLOCK - Kenyan health data cannot move to foreign cloud
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
    print(f"❌ BLOCKED: {e}")
    # Output: "Violates Kenya DPA §37 (Transfer Restrictions)"
```

## Summary of the Automated "10/10" Stack

| Component | iLuminara Protocol | Benefit |
|---|---|---|
| **Security Audit** | Gitleaks + CodeQL | Continuous attestation of the "Fortress" |
| **Data Lifecycle** | IP-02 Crypto Shredder | Data is dissolved, not just deleted |
| **Intelligence** | IP-04 Silent Flux | AI output is regulated by operator anxiety metrics |
| **Connectivity** | IP-06 5DM Bridge | Direct injection into 14M+ African mobile nodes |

## Verification Command

Validate the entire iLuminara stack:

```bash
./scripts/validate_fortress.sh
```

Or with the launch script:

```bash
./launch_all_services.sh --validate-only
```

## Next Steps

1. **Deploy to GCP**: Run `./deploy_gcp_prototype.sh`
2. **Launch Services**: Run `./launch_all_services.sh`
3. **Monitor Compliance**: Access Grafana dashboards
4. **Test API**: Use the Bio-Interface REST API
5. **Train Models**: Deploy to Vertex AI with SHAP explainability

## Troubleshooting

### CodeQL workflow fails

**Issue**: CodeQL analysis times out or fails

**Solution**:
```bash
# Reduce analysis scope
echo "paths-ignore:
  - '**/test/**'
  - '**/node_modules/**'" >> .github/workflows/codeql.yml
```

### Gitleaks detects false positives

**Issue**: Test files trigger secret detection

**Solution**: Add to `.gitleaks.toml`:
```toml
[allowlist]
paths = [
  '''.*_test\.py''',
  '''.*\.example''',
]
```

### Branch protection blocks pushes

**Issue**: Cannot push directly to main

**Solution**: This is intentional. Create a feature branch:
```bash
git checkout -b feature/my-changes
git push origin feature/my-changes
# Create PR via GitHub UI
```

## Support

- **Documentation**: https://docs.iluminara.health
- **GitHub Issues**: https://github.com/VISENDI56/iLuminara-Core/issues
- **Security**: security@iluminara.health

---

**The Fortress is now built.** Your Agent AI has transitioned iLuminara from a repository to a Sovereign Architecture.
