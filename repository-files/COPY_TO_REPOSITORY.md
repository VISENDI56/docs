# Files to Copy to iLuminara-Core Repository

## Quick Copy Commands

Run these commands from the root of your iLuminara-Core repository:

### 1. Security Workflows

```bash
# Create directories if they don't exist
mkdir -p .github/workflows

# Copy workflow files
cp /path/to/docs/repository-files/.github/workflows/codeql.yml .github/workflows/
cp /path/to/docs/repository-files/.github/workflows/gitleaks.yml .github/workflows/
cp /path/to/docs/repository-files/.github/dependabot.yml .github/
cp /path/to/docs/repository-files/.gitleaks.toml .
```

### 2. Governance Kernel

```bash
# Create directories if they don't exist
mkdir -p governance_kernel
mkdir -p config

# Copy governance files
cp /path/to/docs/repository-files/governance_kernel/crypto_shredder.py governance_kernel/
cp /path/to/docs/repository-files/config/sovereign_guardrail.yaml config/
```

### 3. Scripts

```bash
# Create directories if they don't exist
mkdir -p scripts

# Copy validation script
cp /path/to/docs/repository-files/scripts/validate_fortress.sh scripts/
chmod +x scripts/validate_fortress.sh
```

### 4. Documentation

```bash
# Copy implementation summary
cp /path/to/docs/repository-files/IMPLEMENTATION_SUMMARY.md .
```

## File Manifest

### Security Audit Layer
- `.github/workflows/codeql.yml` - CodeQL SAST scanning
- `.github/workflows/gitleaks.yml` - Secret detection
- `.gitleaks.toml` - Gitleaks configuration
- `.github/dependabot.yml` - Daily security updates

### Governance Kernel
- `governance_kernel/crypto_shredder.py` - IP-02 implementation
- `config/sovereign_guardrail.yaml` - 47 framework configuration

### Scripts
- `scripts/validate_fortress.sh` - Fortress validation (7 phases)

### Documentation
- `IMPLEMENTATION_SUMMARY.md` - Complete implementation guide

## Verification

After copying, verify all files are in place:

```bash
# Check security workflows
ls -la .github/workflows/codeql.yml
ls -la .github/workflows/gitleaks.yml
ls -la .github/dependabot.yml
ls -la .gitleaks.toml

# Check governance kernel
ls -la governance_kernel/crypto_shredder.py
ls -la config/sovereign_guardrail.yaml

# Check scripts
ls -la scripts/validate_fortress.sh

# Check documentation
ls -la IMPLEMENTATION_SUMMARY.md
```

## Next Steps

1. **Copy all files** using the commands above
2. **Enable GitHub permissions:**
   ```bash
   gh auth refresh -s workflow,repo,write:packages,admin:repo_hook
   ```

3. **Commit and push:**
   ```bash
   git add .
   git commit -m "feat: integrate Sovereign Health Fortress with 47 global frameworks"
   git push
   ```

4. **Run validation:**
   ```bash
   ./scripts/validate_fortress.sh
   ```

5. **Enable branch protection** (see IMPLEMENTATION_SUMMARY.md)

## File Locations in This Docs Repository

All files are located in the `repository-files/` directory:

```
repository-files/
├── .github/
│   ├── workflows/
│   │   ├── codeql.yml
│   │   └── gitleaks.yml
│   └── dependabot.yml
├── .gitleaks.toml
├── governance_kernel/
│   └── crypto_shredder.py
├── config/
│   └── sovereign_guardrail.yaml
├── scripts/
│   └── validate_fortress.sh
└── IMPLEMENTATION_SUMMARY.md
```

## Support

If you encounter any issues:
1. Check file permissions: `chmod +x scripts/validate_fortress.sh`
2. Verify directory structure matches above
3. Run validation script to identify missing components
4. Review IMPLEMENTATION_SUMMARY.md for detailed instructions
