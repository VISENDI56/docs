# iLuminara-Core: Sovereign Health Fortress Implementation Files

This directory contains all the implementation files for deploying the complete iLuminara-Core security and compliance stack.

## 🛡️ The Fortress Components

### Security Audit Layer
- `.github/workflows/codeql.yml` - CodeQL SAST security scanning
- `.github/workflows/gitleaks.yml` - Secret detection and scanning
- `.gitleaks.toml` - Gitleaks configuration with sovereignty rules
- `.github/dependabot.yml` - Daily automated security updates

### Governance Kernel (Nuclear IP Stack)
- `governance_kernel/crypto_shredder.py` - **IP-02**: Data dissolution (not deletion)
- `governance_kernel/chrono_audit.py` - **IP-09**: Temporal integrity with RFC 3161
- `governance_kernel/sectoral/ofac_sanctions.py` - OFAC sanctions checking
- `governance_kernel/sectoral/cbam_carbon.py` - EU CBAM carbon emissions
- `governance_kernel/sectoral/mdr_pharma.py` - EU MDR pharma compliance
- `config/sovereign_guardrail.yaml` - 29-framework configuration

### Validation & Testing
- `scripts/validate_fortress.sh` - Complete fortress validation script
- `tests/test_sectoral_compliance.py` - Comprehensive test suite for all 29 frameworks

## 📋 Deployment Instructions

### Step 1: Copy Files to Your Repository

```bash
# Navigate to your iLuminara-Core repository
cd /path/to/iLuminara-Core

# Copy all files from this directory
cp -r /path/to/docs/repository-files/* .
```

### Step 2: Set Up GitHub Workflows

```bash
# Ensure workflows directory exists
mkdir -p .github/workflows

# Copy workflow files
cp repository-files/.github/workflows/* .github/workflows/

# Copy Dependabot config
cp repository-files/.github/dependabot.yml .github/

# Copy Gitleaks config
cp repository-files/.gitleaks.toml .
```

### Step 3: Install Governance Kernel

```bash
# Copy governance kernel files
cp -r repository-files/governance_kernel/* governance_kernel/

# Copy configuration
mkdir -p config
cp repository-files/config/sovereign_guardrail.yaml config/
```

### Step 4: Set Up Validation Scripts

```bash
# Copy validation script
mkdir -p scripts
cp repository-files/scripts/validate_fortress.sh scripts/
chmod +x scripts/validate_fortress.sh

# Copy test suite
mkdir -p tests
cp repository-files/tests/test_sectoral_compliance.py tests/
```

### Step 5: Install Dependencies

```bash
# Install required Python packages
pip install cryptography flask streamlit pandas google-cloud-bigquery google-cloud-spanner pyyaml
```

### Step 6: Configure Environment

```bash
# Set environment variables
export NODE_ID=JOR-47
export JURISDICTION=KDPA_KE
export GOOGLE_CLOUD_PROJECT=your-project-id
export ENABLE_TAMPER_PROOF_AUDIT=true
```

### Step 7: Validate the Fortress

```bash
# Run validation
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

🔍 Checking .github/workflows/codeql.yml... ✓ OPERATIONAL
   └─ SAST security scanning (GDPR Art. 32, ISO 27001 A.12.6)

🔍 Checking .github/workflows/gitleaks.yml... ✓ OPERATIONAL
   └─ Secret scanning (NIST SP 800-53 IA-5)

...

🛡️  FORTRESS STATUS: OPERATIONAL
✓  All critical components validated
✓  Security audit layer active
✓  Governance kernel operational
✓  Nuclear IP stack initialized

The Sovereign Health Fortress is ready for deployment.
```

### Step 8: Run Tests

```bash
# Run sectoral compliance tests
python tests/test_sectoral_compliance.py
```

Expected output:
```
======================================================================
SECTORAL COMPLIANCE TEST SUMMARY
======================================================================
Tests run: 45
Successes: 45
Failures: 0
Errors: 0
======================================================================
```

### Step 9: Enable GitHub Security Features

```bash
# Authenticate with GitHub CLI
gh auth refresh -s workflow,repo,write:packages,admin:repo_hook

# Enable branch protection
gh api repos/:owner/:repo/branches/main/protection \
  --method PUT \
  --field required_status_checks[strict]=true \
  --field required_status_checks[contexts][]=CodeQL \
  --field required_status_checks[contexts][]=Gitleaks \
  --field enforce_admins=true \
  --field required_pull_request_reviews[required_approving_review_count]=1
```

### Step 10: Commit and Push

```bash
# Add all files
git add .

# Commit with fortress signature
git commit -m "feat: integrate Sovereign Health Fortress with 29-framework compliance

- Add CodeQL SAST scanning (GDPR Art. 32, ISO 27001 A.12.6)
- Add Gitleaks secret detection (NIST SP 800-53 IA-5)
- Implement IP-02 Crypto Shredder (data dissolution)
- Implement IP-09 Chrono-Audit (temporal integrity)
- Add sectoral compliance for 29 global frameworks
- Add OFAC sanctions checking
- Add CBAM carbon emissions calculation
- Add EU MDR pharma compliance
- Add comprehensive test suite

Compliance coverage:
- 14 Data Privacy frameworks (GDPR, KDPA, HIPAA, LGPD, NDPR, APPI, etc.)
- 1 AI Governance (EU AI Act)
- 4 Supply Chain (CSDDD, LkSG, UFLPA, Dodd-Frank)
- 3 ESG & Carbon (CBAM, Paris Agreement, ICVCM)
- 4 Humanitarian Finance (FATF, OFAC, UN Sanctions, IASC)
- 4 Healthcare & Pharma (EU MDR, FDA 21 CFR Part 11, EU CTR, FHIR)
- 2 Cybersecurity (NIS2, CRA)
- 3 Humanitarian & Interop (WHO IHR, Geneva Conventions, AU Malabo)

The Fortress is now operational."

# Push to repository
git push origin main
```

## 🔐 Nuclear IP Stack Status

| IP Protocol | Status | File Location |
|-------------|--------|---------------|
| **IP-02: Crypto Shredder** | ✅ Active | `governance_kernel/crypto_shredder.py` |
| **IP-03: Acorn Protocol** | ⚠️ Requires Hardware | Not included (TPM required) |
| **IP-04: Silent Flux** | ⚠️ Requires Integration | Not included (anxiety monitoring) |
| **IP-05: Golden Thread** | ✅ Active | `edge_node/sync_protocol/` (existing) |
| **IP-06: 5DM Bridge** | ⚠️ Requires Mobile Network | Not included (mobile integration) |
| **IP-09: Chrono-Audit** | ✅ Active | `governance_kernel/chrono_audit.py` |

## 📊 Compliance Matrix

### 29 Global Frameworks Implemented

#### I. Data Privacy & Sovereignty (14 frameworks)
- GDPR (EU)
- KDPA (Kenya)
- HIPAA (USA)
- HITECH (USA)
- PIPEDA (Canada)
- POPIA (South Africa)
- CCPA (California)
- NIST CSF (USA)
- ISO 27001 (Global)
- SOC 2 (USA)
- EU AI Act (EU)
- LGPD (Brazil)
- NDPR (Nigeria)
- APPI (Japan)

#### II. AI Governance (1 framework)
- EU AI Act

#### III. Supply Chain (4 frameworks)
- CSDDD (EU)
- LkSG (Germany)
- UFLPA (USA)
- Dodd-Frank §1502 (USA)

#### IV. ESG & Carbon (3 frameworks)
- CBAM (EU)
- Paris Agreement Art. 6.2
- ICVCM CCP

#### V. Humanitarian Finance (4 frameworks)
- FATF R8
- OFAC Sanctions (USA)
- UN Sanctions
- IASC Data Responsibility

#### VI. Healthcare & Pharma (4 frameworks)
- EU MDR
- FDA 21 CFR Part 11 (USA)
- EU CTR
- FHIR R4/R5

#### VII. Cybersecurity (2 frameworks)
- NIS2 (EU)
- CRA (EU)

#### VIII. Humanitarian & Interop (3 frameworks)
- WHO IHR
- Geneva Conventions
- AU Malabo Convention

## 🧪 Testing

### Run All Tests

```bash
# Run sectoral compliance tests
python tests/test_sectoral_compliance.py

# Run with verbose output
python tests/test_sectoral_compliance.py -v
```

### Test Individual Sectors

```python
# Test data privacy compliance
python -m unittest tests.test_sectoral_compliance.TestDataPrivacyCompliance

# Test supply chain compliance
python -m unittest tests.test_sectoral_compliance.TestSupplyChainCompliance

# Test ESG carbon compliance
python -m unittest tests.test_sectoral_compliance.TestESGCarbonCompliance
```

## 📖 Usage Examples

### Example 1: Crypto Shredder (IP-02)

```python
from governance_kernel.crypto_shredder import CryptoShredder, RetentionPolicy, SovereigntyZone

# Initialize
shredder = CryptoShredder(
    sovereignty_zone=SovereigntyZone.KENYA,
    enable_audit=True
)

# Encrypt patient data
patient_data = b"Patient ID: 12345, Diagnosis: Malaria"
encrypted_data, key_id = shredder.encrypt_with_ephemeral_key(
    data=patient_data,
    retention_policy=RetentionPolicy.HOT,
    metadata={"patient_id": "12345", "jurisdiction": "KDPA_KE"}
)

# After retention period, shred the key
shredder.shred_key(key_id)

# Data is now cryptographically irrecoverable
```

### Example 2: Chrono-Audit (IP-09)

```python
from governance_kernel.chrono_audit import ChronoAudit, ChronoEventType, TemporalIntegrityLevel

# Initialize
chrono = ChronoAudit(
    integrity_level=TemporalIntegrityLevel.CHAINED,
    enable_tsa=False
)

# Record event
event = chrono.record_event(
    event_type=ChronoEventType.DATA_TRANSFER,
    actor="ml_system",
    resource="patient_data",
    action="transfer_to_cloud",
    jurisdiction="KDPA_KE",
    metadata={"destination": "africa-south1"},
    compliance_frameworks=["KDPA", "GDPR"],
    retention_days=2555
)

# Verify chain integrity
is_valid, errors = chrono.verify_chain_integrity()
print(f"Chain valid: {is_valid}")

# Generate compliance report
report = chrono.generate_compliance_report("GDPR")
```

### Example 3: OFAC Sanctions Checking

```python
from governance_kernel.sectoral.ofac_sanctions import OFACSanctionsChecker

# Initialize
ofac = OFACSanctionsChecker()

# Check entity
is_sanctioned, match_score = ofac.check_entity("VLADIMIR PUTIN")
print(f"Sanctioned: {is_sanctioned}, Score: {match_score}")

# Fuzzy matching
is_sanctioned, match_score = ofac.check_entity("Vladmir Puttin")  # Typo
print(f"Sanctioned: {is_sanctioned}, Score: {match_score}")
```

### Example 4: CBAM Carbon Emissions

```python
from governance_kernel.sectoral.cbam_carbon import CBAMCalculator

# Initialize
cbam = CBAMCalculator()

# Calculate emissions
emissions = cbam.calculate_embedded_emissions(
    logistics_hops=[
        {"mode": "truck", "distance_km": 500, "fuel_type": "diesel"},
        {"mode": "ship", "distance_km": 5000, "fuel_type": "heavy_fuel_oil"},
        {"mode": "truck", "distance_km": 200, "fuel_type": "diesel"}
    ],
    product_weight_kg=1000
)

print(f"Total CO2e: {emissions['total_co2e_kg']} kg")
```

### Example 5: Sectoral Compliance Matrix

```python
from governance_kernel.compliance_matrix import ComplianceMatrix, SectoralContext

matrix = ComplianceMatrix()

# Check KDPA compliance
result = matrix.check_sectoral_compliance(
    context=SectoralContext.DATA_PRIVACY,
    payload={
        "region": "Kenya",
        "data_type": "HIV_Status",
        "target_server": "USA"
    }
)

if result["status"] == "VIOLATION":
    for violation in result["violations"]:
        print(f"❌ {violation['framework']}: {violation['message']}")
```

## 🚀 Next Steps

1. **Review the validation output** - Ensure all components are operational
2. **Run the test suite** - Verify all 29 frameworks are enforced
3. **Configure your jurisdiction** - Update `config/sovereign_guardrail.yaml`
4. **Enable GitHub security features** - Branch protection, CodeQL, Gitleaks
5. **Deploy to production** - Follow the deployment guide in the documentation

## 📚 Documentation

Full documentation is available at: [Your Documentation URL]

- [Governance Kernel](/governance/overview)
- [Security Stack](/security/overview)
- [AI Agents](/ai-agents/overview)
- [Deployment Guide](/deployment/overview)

## 🆘 Support

For issues or questions:
- GitHub Issues: https://github.com/VISENDI56/iLuminara-Core/issues
- Email: compliance@iluminara.health

## 📄 License

[Your License]

---

**The Sovereign Health Fortress is now operational. Transform preventable suffering from statistical inevitability to historical anomaly.**
