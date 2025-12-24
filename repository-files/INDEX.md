# iLuminara-Core Repository Files - Quick Reference

## 📁 File Structure

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
│   └── sovereign_guardrail.yaml # 14 legal frameworks
├── scripts/
│   └── validate_fortress.sh    # Fortress validation
├── README.md                   # Installation guide
├── IMPLEMENTATION_SUMMARY.md   # Complete summary
└── INDEX.md                    # This file
```

## 🚀 Quick Start (13 minutes)

```bash
# 1. Copy files (5 min)
cd /path/to/iLuminara-Core
cp -r repository-files/.github .
cp repository-files/.gitleaks.toml .
cp repository-files/governance_kernel/crypto_shredder.py governance_kernel/
cp -r repository-files/config .
cp -r repository-files/scripts .
chmod +x scripts/validate_fortress.sh

# 2. Install dependencies (2 min)
pip install cryptography>=41.0.0 pyyaml>=6.0

# 3. Enable GitHub security (3 min)
gh auth refresh -s workflow,repo,write:packages,admin:repo_hook
gh api repos/VISENDI56/iLuminara-Core/branches/main/protection -X PUT \
  -f required_status_checks[strict]=true \
  -f required_status_checks[contexts][]=CodeQL \
  -f required_status_checks[contexts][]=Gitleaks

# 4. Validate (1 min)
./scripts/validate_fortress.sh

# 5. Commit & push (2 min)
git add .
git commit -m "feat: integrate SovereignGuardrail and Nuclear IP security stack"
git push origin main
```

## 📋 File Descriptions

### Security Workflows

#### `.github/workflows/codeql.yml`
- **Purpose:** SAST security scanning
- **Frequency:** Weekly + on push/PR
- **Languages:** Python, JavaScript
- **Compliance:** GDPR Art. 32, ISO 27001 A.12.6

#### `.github/workflows/gitleaks.yml`
- **Purpose:** Secret detection
- **Frequency:** Daily + on push/PR
- **Detection:** API keys, tokens, credentials
- **Compliance:** NIST SP 800-53 IA-5, HIPAA §164.312

#### `.github/dependabot.yml`
- **Purpose:** Daily security updates
- **Scope:** Python, npm, Docker, GitHub Actions
- **Priority:** Security updates first

#### `.gitleaks.toml`
- **Purpose:** Gitleaks configuration
- **Rules:** GCP, AWS, GitHub, JWT, Private keys
- **Allowlist:** Test files, documentation

### Nuclear IP Stack

#### `governance_kernel/crypto_shredder.py`
- **Protocol:** IP-02
- **Purpose:** Data dissolution (not deletion)
- **Features:**
  - Ephemeral key encryption
  - Retention policies (HOT, WARM, COLD, ETERNAL)
  - Auto-shred expired keys
  - Tamper-proof audit
- **Compliance:** GDPR Art. 17, HIPAA §164.530(j), NIST SP 800-88

### Configuration

#### `config/sovereign_guardrail.yaml`
- **Purpose:** SovereignGuardrail configuration
- **Frameworks:** 14 global legal frameworks
- **Features:**
  - Data sovereignty rules
  - Cross-border transfer controls
  - Right to explanation
  - Consent management
  - Data retention policies
  - Audit trail configuration
  - Humanitarian constraints

### Validation

#### `scripts/validate_fortress.sh`
- **Purpose:** Complete fortress validation
- **Phases:**
  1. Security Audit Layer
  2. Governance Kernel
  3. Edge Node & AI Agents
  4. Cloud Oracle
  5. Python Dependencies
  6. Environment Configuration
  7. Nuclear IP Stack Status
- **Output:** OPERATIONAL or COMPROMISED

## 🔐 Nuclear IP Stack

| Protocol | File | Status |
|----------|------|--------|
| IP-02 Crypto Shredder | `governance_kernel/crypto_shredder.py` | ✅ Ready |
| IP-03 Acorn Protocol | - | ⚠️ Requires Hardware |
| IP-04 Silent Flux | - | ⚠️ Requires Integration |
| IP-05 Golden Thread | `edge_node/sync_protocol/` | ✅ Active |
| IP-06 5DM Bridge | - | ⚠️ Requires Mobile Network |

## 📊 Compliance Coverage

| Framework | Region | Status |
|-----------|--------|--------|
| GDPR | 🇪🇺 EU | ✅ Enforced |
| KDPA | 🇰🇪 Kenya | ✅ Enforced |
| HIPAA | 🇺🇸 USA | ✅ Enforced |
| POPIA | 🇿🇦 South Africa | ✅ Enforced |
| PIPEDA | 🇨🇦 Canada | ✅ Enforced |
| CCPA | 🇺🇸 California | ✅ Enforced |
| EU AI Act | 🇪🇺 EU | ✅ Enforced |
| ISO 27001 | 🌐 Global | ✅ Enforced |
| SOC 2 | 🇺🇸 USA | ✅ Enforced |
| NIST CSF | 🇺🇸 USA | ✅ Enforced |

## 🧪 Testing

### Test Individual Components

```bash
# Test Crypto Shredder
python governance_kernel/crypto_shredder.py

# Test SovereignGuardrail
python -c "
from governance_kernel.vector_ledger import SovereignGuardrail
guardrail = SovereignGuardrail()
print('✅ SovereignGuardrail loaded')
"

# Validate entire fortress
./scripts/validate_fortress.sh
```

## 📚 Documentation

| Document | Description |
|----------|-------------|
| `README.md` | Complete installation guide |
| `IMPLEMENTATION_SUMMARY.md` | Full implementation summary |
| `INDEX.md` | This quick reference |

## 🔗 External Documentation

- **Security Stack:** `/security/overview`
- **Crypto Shredder:** `/security/crypto-shredder`
- **Governance Kernel:** `/governance/overview`
- **Vertex AI + SHAP:** `/ai-agents/vertex-ai-shap`
- **Bio-Interface API:** `/api-reference/bio-interface`
- **Golden Thread:** `/architecture/golden-thread`
- **Quick Start:** `/quickstart`

## 🆘 Common Issues

### Issue: CodeQL workflow fails
**Solution:**
```bash
python3 --version  # Requires 3.8+
pip install -r requirements.txt
```

### Issue: Gitleaks false positives
**Solution:** Edit `.gitleaks.toml` allowlist

### Issue: Crypto Shredder import error
**Solution:**
```bash
pip install cryptography>=41.0.0
```

### Issue: Validation script not executable
**Solution:**
```bash
chmod +x scripts/validate_fortress.sh
```

## 📞 Support

- **GitHub Issues:** https://github.com/VISENDI56/iLuminara-Core/issues
- **Documentation:** https://docs.iluminara.health
- **Email:** support@iluminara.health

---

**🛡️ FORTRESS STATUS: READY FOR DEPLOYMENT**
