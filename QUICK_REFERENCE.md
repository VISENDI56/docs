# iLuminara-Core Sovereign Health Fortress - Quick Reference

## 🚀 Quick Start (5 Minutes)

```bash
# 1. Copy files to your repository
cd /path/to/iLuminara-Core
cp -r /path/to/repository-files/* .

# 2. Install dependencies
pip install cryptography shap google-cloud-aiplatform flask-cors

# 3. Set environment variables
export NODE_ID=JOR-47
export JURISDICTION=KDPA_KE
export GOOGLE_CLOUD_PROJECT=your-project-id

# 4. Validate fortress
chmod +x scripts/validate_fortress.sh
./scripts/validate_fortress.sh

# 5. Start services
python api/bio_interface.py
```

## 📋 Essential Commands

### Validation
```bash
# Validate entire fortress
./scripts/validate_fortress.sh

# Test Crypto Shredder
python governance_kernel/crypto_shredder.py

# Test Vertex AI + SHAP
python cloud_oracle/vertex_ai_shap.py
```

### API Testing
```bash
# Health check
curl http://localhost:8081/health

# Submit health data
curl -X POST http://localhost:8081/api/v1/submit-health-data \
  -H "Content-Type: application/json" \
  -d '{"patient_id":"PAT_001","data_type":"symptom_report","data":{"symptoms":["fever"],"severity":7},"location":{"lat":0.05,"lng":40.31,"name":"Dadaab"},"source":"mobile_app","consent_token":"TOKEN","jurisdiction":"KDPA_KE"}'

# Submit outbreak alert
curl -X POST http://localhost:8081/api/v1/submit-outbreak-alert \
  -H "Content-Type: application/json" \
  -d '{"location":{"lat":0.05,"lng":40.31,"name":"Dadaab"},"disease":"cholera","case_count":5,"severity":"HIGH","reporter_id":"CHV_001","jurisdiction":"KDPA_KE"}'
```

### GitHub Workflows
```bash
# Enable workflows
gh auth refresh -s workflow,repo,write:packages,admin:repo_hook

# Commit changes
git add .
git commit -m "feat: integrate SovereignGuardrail and Nuclear IP security stack"
git push

# Enable branch protection
gh api repos/VISENDI56/iLuminara-Core/branches/main/protection \
  --method PUT \
  --field required_status_checks[strict]=true \
  --field required_status_checks[contexts][]=CodeQL \
  --field required_status_checks[contexts][]=Gitleaks
```

## 🔑 Key Files

| File | Purpose | Status |
|------|---------|--------|
| `.github/workflows/codeql.yml` | SAST security scanning | ✅ Ready |
| `.github/workflows/gitleaks.yml` | Secret detection | ✅ Ready |
| `.github/dependabot.yml` | Daily security updates | ✅ Ready |
| `governance_kernel/crypto_shredder.py` | IP-02: Data dissolution | ✅ Ready |
| `config/sovereign_guardrail.yaml` | Sovereignty config | ✅ Ready |
| `cloud_oracle/vertex_ai_shap.py` | AI explainability | ✅ Ready |
| `api/bio_interface.py` | Mobile health API | ✅ Ready |
| `scripts/validate_fortress.sh` | Fortress validation | ✅ Ready |

## 🛡️ Nuclear IP Stack Status

| IP | Name | Status | File |
|----|------|--------|------|
| IP-02 | Crypto Shredder | ✅ Active | `governance_kernel/crypto_shredder.py` |
| IP-03 | Acorn Protocol | ⚠️ Requires hardware | N/A |
| IP-04 | Silent Flux | ⚠️ Requires integration | N/A |
| IP-05 | Golden Thread | ✅ Active | `edge_node/sync_protocol/golden_thread.py` |
| IP-06 | 5DM Bridge | ⚠️ Requires mobile network | N/A |

## 📊 Compliance Quick Check

```bash
# Check CodeQL status
gh api repos/VISENDI56/iLuminara-Core/code-scanning/alerts

# Check Gitleaks status
gh api repos/VISENDI56/iLuminara-Core/secret-scanning/alerts

# Check Dependabot status
gh api repos/VISENDI56/iLuminara-Core/dependabot/alerts
```

## 🔒 Security Checklist

- [ ] CodeQL workflow enabled
- [ ] Gitleaks workflow enabled
- [ ] Dependabot configured
- [ ] Crypto Shredder tested
- [ ] SovereignGuardrail configured
- [ ] Vertex AI + SHAP tested
- [ ] Bio-Interface API running
- [ ] Branch protection enabled
- [ ] Environment variables set
- [ ] Fortress validation passed

## 🚨 Emergency Procedures

### Sovereignty Violation Detected
```bash
# Check audit logs
tail -f governance_kernel/keys/audit.jsonl

# Review violation
python -c "from governance_kernel.vector_ledger import SovereignGuardrail; g = SovereignGuardrail(); print(g.get_tamper_proof_audit_history(limit=10))"
```

### Data Breach Response
```bash
# Immediately shred all keys
python -c "from governance_kernel.crypto_shredder import CryptoShredder; s = CryptoShredder(); s.auto_shred_expired_keys()"

# Review audit trail
python -c "from governance_kernel.vector_ledger import SovereignGuardrail; g = SovereignGuardrail(); print(g.verify_audit_chain_integrity())"
```

### High-Risk AI Inference Without Explanation
```bash
# Check compliance
python -c "from cloud_oracle.vertex_ai_shap import VertexAIExplainer; e = VertexAIExplainer('iluminara-core'); print(e.validate_compliance(result))"
```

## 📞 Support Contacts

- **GitHub Issues:** https://github.com/VISENDI56/iLuminara-Core/issues
- **Documentation:** https://docs.iluminara.health
- **Email:** support@iluminara.health

## 🎯 Success Criteria

✅ **Fortress is OPERATIONAL when:**
- All validation checks pass
- CodeQL and Gitleaks workflows running
- Crypto Shredder encrypting/shredding successfully
- Vertex AI + SHAP providing explanations
- Bio-Interface API accepting submissions
- Golden Thread fusing data streams
- Audit trail tamper-proof and complete

---

**Quick Reference Version 1.0.0**
**Last Updated:** 2025-12-25
