# iLuminara-Core: Singularity Phase Implementation Files

## 🛡️ The Sovereign Health Fortress

This directory contains all implementation files for the **Singularity Phase** (Steps 23-35) of iLuminara-Core, transforming the system from a static security fortress into a dynamic, self-correcting organism.

## 📦 Package Contents

### Security Workflows (`.github/workflows/`)
- **codeql.yml** - SAST security scanning (GDPR Art. 32, ISO 27001 A.12.6)
- **gitleaks.yml** - Secret scanning (NIST SP 800-53 IA-5)

### Configuration Files
- **.gitleaks.toml** - Secret detection rules with sovereignty awareness
- **.github/dependabot.yml** - Daily security updates
- **config/sovereign_guardrail.yaml** - 14 global legal frameworks configuration

### Governance Kernel (`governance_kernel/`)
- **compliance_matrix.py** - Unified regulatory mapping for 14 global data laws
- **crypto_shredder.py** - IP-02: Data dissolution (not deletion)
- **silent_flux.py** - IP-04: Anxiety-regulated AI output
- **acorn_protocol.py** - IP-03: Somatic-keyed secret injection
- **ethical_engine.py** - Humanitarian constraints (Geneva Convention, WHO IHR)
- **vector_ledger.py** - SovereignGuardrail enforcement engine

### Scripts (`scripts/`)
- **validate_fortress.sh** - Complete fortress validation (7 phases)
- **generate_system_integrity.sh** - Nuclear IP Stack attestation
- **launch_compassionate_ui.sh** - Multi-port dashboard activation
- **lock_fortress.sh** - Final repository lockdown

## 🚀 Quick Start

### 1. Copy Files to Your Repository

```bash
# Navigate to your iLuminara-Core repository
cd /path/to/iLuminara-Core

# Copy all files
cp -r /path/to/docs/repository-files/* .

# Make scripts executable
chmod +x scripts/*.sh
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt

# Additional Singularity Phase dependencies
pip install cryptography google-cloud-secret-manager numpy
```

### 3. Configure Environment

```bash
export NODE_ID=JOR-47
export JURISDICTION=KDPA_KE
export GOOGLE_CLOUD_PROJECT=your-project-id
export ENABLE_TAMPER_PROOF_AUDIT=true
export RETENTION_MAX_DAYS=1825
```

### 4. Validate Fortress

```bash
./scripts/validate_fortress.sh
```

Expected output:
```
╔════════════════════════════════════════════════════════════╗
║     iLuminara-Core Sovereign Health Fortress Validator     ║
╚════════════════════════════════════════════════════════════╝

PHASE 1: Security Audit Layer
✓ CodeQL workflow
✓ Gitleaks workflow
✓ Dependabot configuration

PHASE 2: Governance Kernel (Nuclear IP Stack)
✓ SovereignGuardrail
✓ Crypto Shredder (IP-02)
✓ Ethical Engine

...

🛡️  FORTRESS STATUS: OPERATIONAL
✓  All critical components validated
```

### 5. Initialize Components

```python
# Initialize ComplianceMatrix
from governance_kernel.compliance_matrix import get_compliance_matrix
matrix = get_compliance_matrix()

# Initialize Silent Flux
from governance_kernel.silent_flux import get_silent_flux
flux = get_silent_flux()

# Initialize Acorn Protocol
from governance_kernel.acorn_protocol import get_acorn_protocol
acorn = get_acorn_protocol()

# Initialize Crypto Shredder
from governance_kernel.crypto_shredder import CryptoShredder
shredder = CryptoShredder()
```

## 📋 Implementation Checklist

### Phase 1: Security Foundation ✅
- [x] CodeQL SAST scanning
- [x] Gitleaks secret detection
- [x] Dependabot daily updates
- [x] Crypto Shredder (IP-02)
- [x] SovereignGuardrail configuration

### Phase 2: Singularity Components ✅
- [x] ComplianceMatrix (14 laws)
- [x] Silent Flux (IP-04)
- [x] Acorn Protocol (IP-03)
- [x] Automated Sovereignty Lockout
- [x] Vector Ledger Sync
- [x] SHAP Ethical Audit
- [x] 5DM Bridge (IP-06)
- [x] Retention Policy Manager
- [x] Humanitarian Margin Verification

### Phase 3: Integration & Attestation ✅
- [x] Compassionate UI multi-port
- [x] System integrity signature
- [x] Continuous audit loop
- [x] Fortress lockdown script

## 🔧 Component Details

### ComplianceMatrix (Step 23)

Encodes 14 global data laws with cross-referencing logic.

**The 14 Laws:**
1. GDPR (EU)
2. HIPAA (USA)
3. Kenya DPA
4. POPIA (South Africa)
5. NDPR (Nigeria)
6. APPI (Japan)
7. PIPEDA (Canada)
8. LGPD (Brazil)
9. CCPA (California)
10. WHO IHR (2005)
11. Geneva Conventions
12. EU AI Act
13. AU Malabo Convention
14. FHIR R4/R5

**Usage:**
```python
result = matrix.check_compliance(
    operation=DataHandlingOperation.CROSS_BORDER_TRANSFER,
    context={"data_type": "PHI", "destination": "USA"},
    jurisdiction=DataLaw.KENYA_DPA
)
```

### Silent Flux (Step 24)

Anxiety-regulated AI output that prevents cognitive overload.

**Stress Levels:**
- CALM (0.0-0.3) → FULL output (2000 tokens)
- FOCUSED (0.3-0.5) → STANDARD output (1000 tokens)
- ELEVATED (0.5-0.7) → CONCISE output (500 tokens)
- HIGH (0.7-0.85) → ESSENTIAL output (200 tokens)
- CRITICAL (0.85-1.0) → EMERGENCY output (100 tokens)

**Usage:**
```python
flux.record_keystroke()
flux.record_action()
status = flux.get_status()
regulated = flux.regulate_output(ai_output)
```

### Acorn Protocol (Step 25)

Somatic-keyed secret injection using posture + location + stillness.

**Authentication Factors:**
- Authorized posture (sitting, standing)
- Authorized location (within radius)
- Required stillness (<0.3 m/s)
- Stillness duration (3+ seconds)

**Usage:**
```python
acorn.register_operator(
    operator_id="DR_AMINA",
    authorized_postures=[PostureState.SITTING],
    authorized_locations=[(0.0512, 40.3129, 100.0)],
    required_stillness=StillnessLevel.CALM
)

secret = acorn.inject_secret("DR_AMINA", "GOLDEN_THREAD_KEY", reading)
```

### Crypto Shredder (IP-02)

Data is not deleted; it is cryptographically dissolved.

**Retention Policies:**
- HOT: 180 days (active operational data)
- WARM: 365 days (compliance minimum)
- COLD: 1825 days (legal hold maximum)
- ETERNAL: Never expires (requires justification)

**Usage:**
```python
encrypted_data, key_id = shredder.encrypt_with_ephemeral_key(
    data=patient_record,
    retention_policy=RetentionPolicy.HOT
)

# After retention period
shredder.shred_key(key_id)  # Data becomes irrecoverable
```

## 🔍 Validation & Testing

### Run Fortress Validation

```bash
./scripts/validate_fortress.sh
```

Validates:
1. Security Audit Layer
2. Governance Kernel
3. Edge Node & AI Agents
4. Cloud Oracle
5. Python Dependencies
6. Environment Configuration
7. Nuclear IP Stack Status

### Run Unit Tests

```bash
# Test ComplianceMatrix
python -m pytest tests/test_compliance_matrix.py

# Test Silent Flux
python -m pytest tests/test_silent_flux.py

# Test Acorn Protocol
python -m pytest tests/test_acorn_protocol.py

# Test Crypto Shredder
python -m pytest tests/test_crypto_shredder.py
```

### Run Integration Tests

```bash
# Full integration test suite
python -m pytest tests/integration/

# Specific integration tests
python tests/test_sovereignty_lockout.py
python tests/test_golden_thread_sync.py
```

## 📊 Monitoring

### Prometheus Metrics

```
# ComplianceMatrix
sovereignty_violations_total
cross_border_transfers_blocked_total
compliance_checks_total

# Silent Flux
operator_stress_level
output_mode_changes_total
cognitive_overload_prevented_total

# Acorn Protocol
authentication_attempts_total
authentication_failures_total
panic_access_blocked_total

# Crypto Shredder
keys_shredded_total
retention_policy_violations_total
auto_shred_runs_total
```

### Grafana Dashboards

1. **Sovereignty Compliance** - Real-time violation monitoring
2. **Operator Wellness** - Silent Flux stress levels
3. **Security Attestation** - Acorn Protocol authentication
4. **Data Lifecycle** - Crypto Shredder key management

## 🚨 Troubleshooting

### Issue: ComplianceMatrix violations not blocking operations
**Solution:** Ensure `enforcement_level: STRICT` in `config/sovereign_guardrail.yaml`

### Issue: Silent Flux not regulating output
**Solution:** Check `enable_auto_regulation: true` and verify stress metrics are being recorded

### Issue: Acorn Protocol authentication failing
**Solution:** Verify biometric readings match authorized profile (posture, location, stillness)

### Issue: Crypto Shredder not auto-shredding
**Solution:** Ensure cron job is running: `0 2 * * * python governance_kernel/crypto_shredder.py --auto-shred`

## 📚 Documentation

Full documentation available at: https://docs.iluminara.health

- [Architecture Overview](https://docs.iluminara.health/architecture/overview)
- [Governance Kernel](https://docs.iluminara.health/governance/overview)
- [Security Stack](https://docs.iluminara.health/security/overview)
- [Singularity Phase](https://docs.iluminara.health/security/singularity-phase)
- [API Reference](https://docs.iluminara.health/api-reference/overview)

## 🤝 Support

- **GitHub Issues:** https://github.com/VISENDI56/iLuminara-Core/issues
- **Email:** compliance@iluminara.health
- **Documentation:** https://docs.iluminara.health

## 📄 License

iLuminara-Core is licensed under the Apache License 2.0 with additional humanitarian use clauses.

---

**"The Fortress is not built. It is continuously attested."**

🛡️ iLuminara-Core: Sovereign Health Fortress
