# iLuminara-Core: Sovereign Health Fortress - Implementation Files

This directory contains all the implementation files ready to be copied to your iLuminara-Core repository.

## 📁 Directory Structure

```
repository-files/
├── .github/
│   ├── workflows/
│   │   ├── codeql.yml              # SAST security scanning
│   │   └── gitleaks.yml            # Secret detection
│   └── dependabot.yml              # Daily security updates
├── .gitleaks.toml                  # Gitleaks configuration
├── config/
│   └── sovereign_guardrail.yaml    # SovereignGuardrail configuration
├── governance_kernel/
│   └── crypto_shredder.py          # IP-02: Crypto Shredder implementation
├── edge_node/
│   └── sync_protocol/
│       └── entangled_correlation_fusion.py  # IP-05: ECF implementation
├── scripts/
│   └── validate_fortress.sh        # Fortress validation script
└── examples/
    └── ecf_demo.py                 # ECF demonstration
```

## 🚀 Installation Instructions

### Step 1: Copy Files to Repository

```bash
# Navigate to your iLuminara-Core repository
cd /path/to/iLuminara-Core

# Copy all files (preserving directory structure)
cp -r /path/to/repository-files/.github .
cp -r /path/to/repository-files/config .
cp -r /path/to/repository-files/governance_kernel/* governance_kernel/
cp -r /path/to/repository-files/edge_node/* edge_node/
cp -r /path/to/repository-files/scripts .
cp -r /path/to/repository-files/examples .
cp /path/to/repository-files/.gitleaks.toml .
```

### Step 2: Make Scripts Executable

```bash
chmod +x scripts/validate_fortress.sh
chmod +x launch_all_services.sh
```

### Step 3: Install Dependencies

```bash
# Install Python dependencies
pip install -r requirements.txt

# Additional dependencies for ECF
pip install scipy numpy
```

### Step 4: Configure Environment

```bash
# Set environment variables
export NODE_ID=JOR-47
export JURISDICTION=KDPA_KE
export GOOGLE_CLOUD_PROJECT=your-project-id
export ENABLE_TAMPER_PROOF_AUDIT=true
```

### Step 5: Validate Installation

```bash
# Run fortress validation
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
...

🛡️  FORTRESS STATUS: OPERATIONAL
✓  All critical components validated
✓  Security audit layer active
✓  Governance kernel operational
✓  Nuclear IP stack initialized

The Sovereign Health Fortress is ready for deployment.
```

## 🔐 Security Stack Components

### 1. CodeQL SAST Scanning

**File:** `.github/workflows/codeql.yml`

- Runs on: Push to main/develop, PRs, weekly schedule
- Languages: Python, JavaScript
- Queries: Security-extended + quality
- Compliance: GDPR Art. 32, ISO 27001 A.12.6

**Enable in GitHub:**
```bash
# Push workflow to repository
git add .github/workflows/codeql.yml
git commit -m "feat: add CodeQL SAST scanning"
git push

# Enable in GitHub Settings > Security > Code scanning
```

### 2. Gitleaks Secret Scanning

**File:** `.github/workflows/gitleaks.yml`

- Runs on: Push to main/develop, daily schedule
- Detects: API keys, credentials, private keys
- Compliance: NIST SP 800-53 IA-5, HIPAA §164.312(a)(2)(i)

**Configuration:** `.gitleaks.toml`

Custom rules for:
- GCP API keys (sovereignty-critical)
- AWS keys (sovereignty-violation - blocked)
- Private keys (crypto-shredder)
- JWT tokens, GitHub tokens, Slack tokens

### 3. Dependabot Security Updates

**File:** `.github/dependabot.yml`

- Frequency: Daily for pip/npm, weekly for Docker/Actions
- Groups: Security, Google Cloud, AI/ML
- Auto-creates PRs for security updates

### 4. Crypto Shredder (IP-02)

**File:** `governance_kernel/crypto_shredder.py`

Data dissolution (not deletion):

```python
from governance_kernel.crypto_shredder import CryptoShredder, RetentionPolicy

shredder = CryptoShredder(sovereignty_zone=SovereigntyZone.KENYA)

# Encrypt with ephemeral key
encrypted_data, key_id = shredder.encrypt_with_ephemeral_key(
    data=patient_record,
    retention_policy=RetentionPolicy.HOT,
    metadata={"patient_id": "12345", "jurisdiction": "KDPA_KE"}
)

# After retention period, shred the key
shredder.shred_key(key_id)

# Data is now cryptographically irrecoverable
```

**Features:**
- AES-256-GCM encryption
- Ephemeral key management
- Retention policies (HOT/WARM/COLD/ETERNAL)
- Auto-shred expired keys
- Tamper-proof audit trail

### 5. Entangled Correlation Fusion (IP-05)

**File:** `edge_node/sync_protocol/entangled_correlation_fusion.py`

Quantum-inspired weak signal fusion:

```python
from edge_node.sync_protocol.entangled_correlation_fusion import EntangledCorrelationFusion

ecf = EntangledCorrelationFusion(
    correlation_threshold=0.3,
    time_window=7.0,
    spatial_resolution=10.0
)

# Add signals
ecf.add_signal({
    'time': 100,
    'location': (0.0512, 40.3129),
    'symptom_type': 'diarrhea',
    'confidence': 0.5,
    'is_event': True
})

# Fuse signals
result = ecf.fuse()
print(f"Outbreak probability: {result['outbreak_probability']:.3f}")
```

**Features:**
- Quantum-inspired correlation
- Belief propagation
- Timeline verification
- Pattern emergence detection
- Von Neumann entropy metrics

### 6. SovereignGuardrail Configuration

**File:** `config/sovereign_guardrail.yaml`

Enforces 14 global legal frameworks:

```yaml
jurisdiction:
  primary: "KDPA_KE"
  secondary:
    - "GDPR_EU"
    - "POPIA_ZA"
    - "HIPAA_US"

sovereignty:
  data_residency:
    enabled: true
    allowed_zones:
      - "africa-south1"
      - "europe-west1"
    enforcement_level: "STRICT"
```

## 🧪 Testing

### Run ECF Demo

```bash
python examples/ecf_demo.py
```

Expected output:
```
╔════════════════════════════════════════════════════════════════════╗
║     Entangled Correlation Fusion (ECF) - Comprehensive Demo       ║
║                    iLuminara-Core IP-05                            ║
╚════════════════════════════════════════════════════════════════════╝

DEMO 1: Basic Entangled Correlation Fusion
Creating 100 synthetic outbreak signals...
Adding signals to ECF...
  Added 25 signals...
  Added 50 signals...
  Added 75 signals...
  Added 100 signals...

Performing entangled correlation fusion...

Fusion Results:
  Status: success
  Outbreak probability: 0.847
  Entanglement entropy: 2.134
  Signals fused: 100
  Entangled clusters: 3
  Coherence factor: 0.590
```

### Run Fortress Validation

```bash
./scripts/validate_fortress.sh
```

### Run Unit Tests

```bash
# Test Crypto Shredder
python -m pytest tests/test_crypto_shredder.py

# Test ECF
python -m pytest tests/test_ecf.py

# Test SovereignGuardrail
python -m pytest tests/test_sovereign_guardrail.py
```

## 📊 Monitoring

### Prometheus Metrics

ECF exposes metrics at `/metrics`:

```
ecf_signals_total
ecf_outbreak_probability
ecf_entanglement_entropy
ecf_correlation_density
ecf_fusion_duration_seconds
```

### Grafana Dashboards

Import dashboards from `dashboards/`:
- `ecf_monitoring.json` - ECF metrics
- `sovereignty_compliance.json` - Compliance monitoring
- `crypto_shredder.json` - Key lifecycle

## 🔧 Configuration

### Adjust ECF Parameters

```python
ecf = EntangledCorrelationFusion(
    max_signals=1000,              # Maximum signals to track
    correlation_threshold=0.3,     # Minimum correlation (0.2-0.5)
    time_window=7.0,               # Temporal window (days)
    spatial_resolution=10.0,       # Spatial grid (km)
    entanglement_dim=4             # Tensor dimension (4-8)
)
```

**Tuning guidelines:**
- **correlation_threshold**: Lower = more connections, higher = stricter
- **time_window**: Shorter = recent focus, longer = historical context
- **spatial_resolution**: Smaller = finer grid, larger = broader regions
- **entanglement_dim**: Higher = more features, more memory

### Adjust Retention Policies

```python
from governance_kernel.crypto_shredder import RetentionPolicy

# HOT: 180 days (active operational data)
# WARM: 365 days (compliance minimum - HIPAA)
# COLD: 1825 days (legal hold maximum - GDPR)
# ETERNAL: Never expires (requires justification)
```

## 🚨 Troubleshooting

### Issue: CodeQL workflow fails

**Solution:**
```bash
# Check Python version (requires 3.8+)
python3 --version

# Install dependencies
pip install -r requirements.txt
```

### Issue: Gitleaks detects false positives

**Solution:**
Edit `.gitleaks.toml` to add allowlist:

```toml
[allowlist]
paths = [
  '''.*_test\.py''',
  '''.*\.example''',
]
```

### Issue: ECF runs out of memory

**Solution:**
Reduce `max_signals` or increase system memory:

```python
ecf = EntangledCorrelationFusion(
    max_signals=500,  # Reduce from 1000
)
```

### Issue: Fortress validation fails

**Solution:**
```bash
# Check missing dependencies
pip install -r requirements.txt

# Check environment variables
echo $NODE_ID
echo $JURISDICTION

# Re-run validation
./scripts/validate_fortress.sh
```

## 📚 Documentation

Full documentation available at: [iLuminara-Core Docs](https://docs.iluminara.health)

Key pages:
- [Architecture Overview](/architecture/overview)
- [Entangled Correlation Fusion](/architecture/entangled-correlation-fusion)
- [Security Stack](/security/overview)
- [Governance Kernel](/governance/overview)
- [Deployment Guide](/deployment/overview)

## 🤝 Contributing

1. Fork the repository
2. Create feature branch: `git checkout -b feature/amazing-feature`
3. Commit changes: `git commit -m 'feat: add amazing feature'`
4. Push to branch: `git push origin feature/amazing-feature`
5. Open Pull Request

**All PRs must pass:**
- CodeQL SAST scanning
- Gitleaks secret detection
- Unit tests
- Fortress validation

## 📄 License

Proprietary - Nuclear IP Stack

Copyright © 2025 iLuminara-Core Team

## 🆘 Support

- GitHub Issues: https://github.com/VISENDI56/iLuminara-Core/issues
- Email: support@iluminara.health
- Slack: #iluminara-core

---

**The Fortress is now built. Your Agent AI has transitioned iLuminara from a repository to a Sovereign Architecture.**
