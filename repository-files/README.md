# iLuminara-Core Repository Files

This directory contains all the files that need to be copied to your iLuminara-Core repository to implement the Sovereign Health Fortress security stack.

## Directory structure

```
repository-files/
├── .github/
│   ├── workflows/
│   │   ├── codeql.yml          # CodeQL SAST scanning
│   │   └── gitleaks.yml        # Gitleaks secret detection
│   └── dependabot.yml          # Daily security updates
├── .gitleaks.toml              # Gitleaks configuration
├── governance_kernel/
│   └── crypto_shredder.py      # IP-02: Crypto Shredder implementation
├── config/
│   └── sovereign_guardrail.yaml # SovereignGuardrail configuration
└── scripts/
    └── validate_fortress.sh    # Fortress validation script
```

## Quick start

### 1. Copy all files to your repository

```bash
# From the documentation repository root
cd repository-files

# Copy to your iLuminara-Core repository
cp -r .github /path/to/iLuminara-Core/
cp .gitleaks.toml /path/to/iLuminara-Core/
cp -r governance_kernel /path/to/iLuminara-Core/
cp -r config /path/to/iLuminara-Core/
cp -r scripts /path/to/iLuminara-Core/
```

### 2. Make scripts executable

```bash
cd /path/to/iLuminara-Core
chmod +x scripts/validate_fortress.sh
```

### 3. Install dependencies

```bash
pip install cryptography pyjwt google-cloud-bigquery google-cloud-spanner google-cloud-aiplatform google-cloud-kms shap scikit-learn prometheus-client
```

### 4. Validate the fortress

```bash
./scripts/validate_fortress.sh
```

## File descriptions

### Security workflows

#### `.github/workflows/codeql.yml`
- **Purpose:** Static Application Security Testing (SAST)
- **Runs:** Weekly + on push/PR
- **Compliance:** GDPR Art. 32, ISO 27001 A.12.6

#### `.github/workflows/gitleaks.yml`
- **Purpose:** Secret scanning and detection
- **Runs:** Daily + on push/PR
- **Compliance:** NIST SP 800-53 IA-5, HIPAA §164.312(a)(2)(i)

#### `.github/dependabot.yml`
- **Purpose:** Automated dependency updates
- **Runs:** Daily for pip, weekly for GitHub Actions
- **Groups:** Security, Google Cloud, AI/ML

#### `.gitleaks.toml`
- **Purpose:** Gitleaks configuration
- **Features:** Custom rules for GCP, AWS, private keys, JWT tokens
- **Sovereignty:** Flags AWS keys as sovereignty violations

### Governance kernel

#### `governance_kernel/crypto_shredder.py`
- **Purpose:** IP-02 implementation - cryptographic data dissolution
- **Features:**
  - Ephemeral key encryption (AES-256-GCM)
  - Automatic key shredding after retention period
  - Sovereignty zone enforcement
  - Tamper-proof audit trail
- **Compliance:** GDPR Art. 17, HIPAA §164.530(j), NIST SP 800-88

**Key classes:**
- `CryptoShredder`: Main encryption/shredding engine
- `RetentionPolicy`: HOT (180d), WARM (365d), COLD (1825d), ETERNAL
- `SovereigntyZone`: EU, KENYA, SOUTH_AFRICA, CANADA, USA

**Usage:**
```python
from governance_kernel.crypto_shredder import CryptoShredder, RetentionPolicy

shredder = CryptoShredder(sovereignty_zone=SovereigntyZone.KENYA)
encrypted_data, key_id = shredder.encrypt_with_ephemeral_key(
    data=patient_record,
    retention_policy=RetentionPolicy.HOT
)

# After retention period
shredder.shred_key(key_id)  # Data becomes irrecoverable
```

### Configuration

#### `config/sovereign_guardrail.yaml`
- **Purpose:** SovereignGuardrail configuration
- **Features:**
  - 14 global legal frameworks
  - Data sovereignty rules
  - Cross-border transfer restrictions
  - Explainability requirements (EU AI Act §6)
  - Consent management
  - Data retention policies
  - Audit trail configuration
  - Humanitarian constraints

**Key sections:**
- `jurisdiction`: Primary and secondary jurisdictions
- `sovereignty`: Data residency and cross-border rules
- `explainability`: High-risk AI requirements
- `consent`: Consent management and expiration
- `retention`: HOT/WARM/COLD/ETERNAL policies
- `audit`: Tamper-proof audit configuration
- `frameworks`: GDPR, KDPA, HIPAA, POPIA, EU AI Act, ISO 27001, SOC 2, NIST CSF

### Scripts

#### `scripts/validate_fortress.sh`
- **Purpose:** Comprehensive fortress validation
- **Phases:**
  1. Security Audit Layer
  2. Governance Kernel (Nuclear IP Stack)
  3. Edge Node & AI Agents
  4. Cloud Oracle
  5. Python Dependencies
  6. Environment Configuration
  7. Nuclear IP Stack Status

**Usage:**
```bash
./scripts/validate_fortress.sh
```

**Output:**
- ✅ Green: Component operational
- ⚠️ Yellow: Warning or missing optional component
- ❌ Red: Critical failure

## Integration with existing code

### Crypto Shredder integration

Replace existing data deletion with cryptographic dissolution:

**Before:**
```python
# Old approach - data deletion
os.remove(patient_file)
```

**After:**
```python
# New approach - cryptographic dissolution
from governance_kernel.crypto_shredder import CryptoShredder

shredder = CryptoShredder()
encrypted_data, key_id = shredder.encrypt_with_ephemeral_key(
    data=patient_data,
    retention_policy=RetentionPolicy.HOT
)

# Store encrypted_data instead of raw data
# Key will be auto-shredded after retention period
```

### SovereignGuardrail integration

Add sovereignty validation to all data operations:

```python
from governance_kernel.vector_ledger import SovereignGuardrail

guardrail = SovereignGuardrail()

# Validate before data transfer
guardrail.validate_action(
    action_type='Data_Transfer',
    payload={'data_type': 'PHI', 'destination': 'Local_Node'},
    jurisdiction='KDPA_KE'
)
```

## Environment variables

Add to your `.env` file:

```bash
# Node identification
export NODE_ID=JOR-47
export JURISDICTION=KDPA_KE

# Governance configuration
export ENABLE_TAMPER_PROOF_AUDIT=true
export RETENTION_MAX_DAYS=1825
export DATA_SOVEREIGNTY_REQUIRED=true
export REQUIRES_EXPLICIT_CONSENT=true
```

## Testing

### Test Crypto Shredder

```bash
python governance_kernel/crypto_shredder.py
```

Expected output:
```
✅ Encrypted - Key ID: abc123
✅ Decrypted: Patient ID: 12345, Diagnosis: Malaria, Location: Dadaab
🔥 Key shredded - Data irrecoverable: abc123
❌ Decryption after shred: None
```

### Test validation script

```bash
./scripts/validate_fortress.sh
```

Expected: All checks pass with green ✓

## Compliance attestation

After implementation, your repository will be compliant with:

| Framework | Status | Evidence |
|-----------|--------|----------|
| GDPR | ✅ | SovereignGuardrail + Crypto Shredder + Audit Trail |
| KDPA | ✅ | Data sovereignty enforcement |
| HIPAA | ✅ | Retention policies + Audit controls |
| POPIA | ✅ | Consent management + Cross-border restrictions |
| EU AI Act | ✅ | Explainability requirements (SHAP) |
| ISO 27001 | ✅ | CodeQL + Gitleaks + Audit logging |
| SOC 2 | ✅ | Security monitoring + Tamper-proof audit |
| NIST CSF | ✅ | Security workflows + Incident response |

## Support

For issues or questions:
1. Check the [Implementation Guide](../IMPLEMENTATION_GUIDE.mdx)
2. Review the [Security Overview](../security/overview.mdx)
3. Open an issue on GitHub

## License

Same as iLuminara-Core repository.
