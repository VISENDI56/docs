# iLuminara-Core Deployment Checklist

Use this checklist to ensure complete implementation of the Sovereign Health Fortress.

## ✅ Pre-Deployment

- [ ] GitHub repository with workflow permissions
- [ ] Python 3.8+ installed
- [ ] Git CLI installed
- [ ] GitHub CLI installed (`gh`)
- [ ] Google Cloud Platform account (for cloud deployment)
- [ ] Access to iLuminara-Core repository

## ✅ Step 1: Permissions

- [ ] Run: `gh auth refresh -s workflow,repo,write:packages,admin:repo_hook`
- [ ] Verify authentication: `gh auth status`

## ✅ Step 2: Copy Files

- [ ] Copy `.github/workflows/codeql.yml`
- [ ] Copy `.github/workflows/gitleaks.yml`
- [ ] Copy `.github/dependabot.yml`
- [ ] Copy `.gitleaks.toml`
- [ ] Copy `config/sovereign_guardrail.yaml`
- [ ] Copy `governance_kernel/crypto_shredder.py`
- [ ] Copy `integrations/vertex_ai_shap.py`
- [ ] Copy `integrations/bio_interface_api.py`
- [ ] Copy `scripts/validate_fortress.sh`

## ✅ Step 3: Make Scripts Executable

- [ ] Run: `chmod +x scripts/validate_fortress.sh`
- [ ] Run: `chmod +x launch_all_services.sh`
- [ ] Run: `chmod +x deploy_gcp_prototype.sh`

## ✅ Step 4: Install Dependencies

- [ ] Install cryptography: `pip install cryptography`
- [ ] Install Flask: `pip install flask flask-cors`
- [ ] Install SHAP: `pip install shap`
- [ ] Install Google Cloud: `pip install google-cloud-aiplatform google-cloud-bigquery google-cloud-spanner`
- [ ] Or install all: `pip install -r requirements.txt`

## ✅ Step 5: Configure Environment

- [ ] Set `NODE_ID`: `export NODE_ID=JOR-47`
- [ ] Set `JURISDICTION`: `export JURISDICTION=KDPA_KE`
- [ ] Set `GOOGLE_CLOUD_PROJECT`: `export GOOGLE_CLOUD_PROJECT=iluminara-health`
- [ ] Set `API_HOST`: `export API_HOST=0.0.0.0`
- [ ] Set `API_PORT`: `export API_PORT=8080`
- [ ] Set `ENABLE_TAMPER_PROOF_AUDIT`: `export ENABLE_TAMPER_PROOF_AUDIT=true`
- [ ] Add to `.bashrc` or `.zshrc` for persistence

## ✅ Step 6: Validate Fortress

- [ ] Run: `./scripts/validate_fortress.sh`
- [ ] Verify output shows "FORTRESS STATUS: OPERATIONAL"
- [ ] Check all components show "✓ OPERATIONAL"
- [ ] Verify Nuclear IP Stack status

## ✅ Step 7: Commit and Push

- [ ] Stage files: `git add .`
- [ ] Commit: `git commit -m "feat: integrate SovereignGuardrail and Nuclear IP security stack"`
- [ ] Push: `git push origin main`
- [ ] Verify push successful

## ✅ Step 8: Enable Branch Protection

- [ ] Go to GitHub Settings → Branches
- [ ] Add rule for `main` branch
- [ ] Enable "Require pull request reviews"
- [ ] Enable "Require status checks" (CodeQL, Gitleaks)
- [ ] Enable "Require branches to be up to date"
- [ ] Save changes

## ✅ Step 9: Test Security Workflows

### CodeQL
- [ ] Trigger workflow: Push a change
- [ ] Check status: `gh run list --workflow=codeql.yml`
- [ ] Verify workflow completes successfully
- [ ] Review any findings

### Gitleaks
- [ ] Trigger workflow: Push a change
- [ ] Check status: `gh run list --workflow=gitleaks.yml`
- [ ] Verify no secrets detected
- [ ] Review any findings

### Dependabot
- [ ] Wait for first PR (within 24 hours)
- [ ] Review and merge security updates
- [ ] Verify daily PRs continue

## ✅ Step 10: Test Crypto Shredder

- [ ] Run Python REPL: `python`
- [ ] Import: `from governance_kernel.crypto_shredder import CryptoShredder`
- [ ] Create instance: `shredder = CryptoShredder()`
- [ ] Test encryption: `encrypted, key_id = shredder.encrypt_with_ephemeral_key(b"test")`
- [ ] Test decryption: `decrypted = shredder.decrypt_with_key(encrypted, key_id)`
- [ ] Test shredding: `shredder.shred_key(key_id)`
- [ ] Verify decryption fails after shred

## ✅ Step 11: Test Vertex AI + SHAP

- [ ] Authenticate: `gcloud auth application-default login`
- [ ] Set project: `gcloud config set project iluminara-health`
- [ ] Run test: `python integrations/vertex_ai_shap.py`
- [ ] Verify SHAP explanations generated
- [ ] Review clinical report output

## ✅ Step 12: Test Bio-Interface API

- [ ] Start API: `python integrations/bio_interface_api.py`
- [ ] Test health: `curl http://localhost:8080/health`
- [ ] Test CBS submit: `curl -X POST http://localhost:8080/api/v1/cbs/submit -d '{...}'`
- [ ] Test EMR submit: `curl -X POST http://localhost:8080/api/v1/emr/submit -d '{...}'`
- [ ] Test data fusion: `curl -X POST http://localhost:8080/api/v1/golden-thread/fuse -d '{...}'`
- [ ] Verify responses

## ✅ Step 13: Deploy to GCP (Optional)

- [ ] Enable required APIs
- [ ] Deploy Bio-Interface API: `gcloud run deploy bio-interface-api ...`
- [ ] Deploy Vertex AI models
- [ ] Configure Cloud Spanner for audit trail
- [ ] Set up BigQuery for data warehouse
- [ ] Configure monitoring and alerts

## ✅ Step 14: Configure Monitoring

- [ ] Set up Prometheus metrics endpoint
- [ ] Configure Grafana dashboards
- [ ] Set up alerting rules
- [ ] Test alert notifications
- [ ] Document monitoring procedures

## ✅ Step 15: Documentation

- [ ] Review implementation guide: https://docs.iluminara.health/implementation-guide
- [ ] Review security stack docs: https://docs.iluminara.health/security/overview
- [ ] Review Vertex AI + SHAP docs: https://docs.iluminara.health/integrations/vertex-ai-shap
- [ ] Review Bio-Interface docs: https://docs.iluminara.health/integrations/bio-interface
- [ ] Update team documentation

## ✅ Step 16: Training

- [ ] Train team on Crypto Shredder usage
- [ ] Train team on SovereignGuardrail configuration
- [ ] Train team on Bio-Interface API
- [ ] Train team on incident response procedures
- [ ] Document training materials

## ✅ Step 17: Compliance Verification

- [ ] Verify GDPR compliance
- [ ] Verify HIPAA compliance
- [ ] Verify KDPA compliance
- [ ] Verify EU AI Act compliance
- [ ] Document compliance attestation

## ✅ Step 18: Production Readiness

- [ ] All tests passing
- [ ] All workflows green
- [ ] No security vulnerabilities
- [ ] Monitoring configured
- [ ] Alerts configured
- [ ] Team trained
- [ ] Documentation complete
- [ ] Compliance verified

## ✅ Post-Deployment

- [ ] Monitor CodeQL scans
- [ ] Monitor Gitleaks scans
- [ ] Review Dependabot PRs daily
- [ ] Monitor sovereignty violations
- [ ] Review audit logs weekly
- [ ] Update documentation as needed

## 🎯 Success Criteria

Your deployment is successful when:

- ✅ Validation script reports "OPERATIONAL"
- ✅ CodeQL workflow runs successfully
- ✅ Gitleaks finds no secrets
- ✅ Dependabot creates daily PRs
- ✅ Crypto Shredder encrypts/shreds data
- ✅ Vertex AI + SHAP explains high-risk inferences
- ✅ Bio-Interface API accepts submissions
- ✅ SovereignGuardrail blocks violations
- ✅ All tests passing
- ✅ Team trained
- ✅ Documentation complete

## 🆘 Troubleshooting

If any step fails, refer to:

- **Implementation Guide:** https://docs.iluminara.health/implementation-guide
- **GitHub Issues:** https://github.com/VISENDI56/iLuminara-Core/issues
- **Repository README:** `repository-files/README.md`

## 📊 Metrics to Track

- [ ] CodeQL scan results
- [ ] Gitleaks scan results
- [ ] Dependabot PR count
- [ ] Sovereignty violations
- [ ] High-risk inferences
- [ ] Keys shredded
- [ ] API request volume
- [ ] Verification scores

---

**The Fortress is not built. It is continuously attested.**

Print this checklist and check off items as you complete them.
