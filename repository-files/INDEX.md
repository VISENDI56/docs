# Repository Files Index

This directory contains all implementation files for the iLuminara-Core Sovereign Health Fortress.

## 📋 Quick Reference

| File | Purpose | Status |
|------|---------|--------|
| `.github/workflows/codeql.yml` | SAST security scanning | ✅ Ready |
| `.github/workflows/gitleaks.yml` | Secret detection | ✅ Ready |
| `.github/dependabot.yml` | Daily security updates | ✅ Ready |
| `.gitleaks.toml` | Secret scanning rules | ✅ Ready |
| `config/sovereign_guardrail.yaml` | Sovereignty configuration | ✅ Ready |
| `governance_kernel/crypto_shredder.py` | IP-02: Data dissolution | ✅ Ready |
| `integrations/vertex_ai_shap.py` | Vertex AI + SHAP | ✅ Ready |
| `integrations/bio_interface_api.py` | Mobile apps REST API | ✅ Ready |
| `scripts/validate_fortress.sh` | Fortress validation | ✅ Ready |

## 🚀 Installation

```bash
# Copy all files to your iLuminara-Core repository
cp -r .github /path/to/iLuminara-Core/
cp -r config /path/to/iLuminara-Core/
cp -r integrations /path/to/iLuminara-Core/
cp -r scripts /path/to/iLuminara-Core/
cp .gitleaks.toml /path/to/iLuminara-Core/
cp governance_kernel/crypto_shredder.py /path/to/iLuminara-Core/governance_kernel/
```

## 📖 Documentation

See `README.md` in this directory for complete implementation guide.

## ✅ Validation

After copying files, run:

```bash
./scripts/validate_fortress.sh
```

## 🔗 Links

- **Full Documentation:** https://docs.iluminara.health
- **Implementation Guide:** https://docs.iluminara.health/implementation-guide
- **Repository:** https://github.com/VISENDI56/iLuminara-Core
