# iLuminara-Core: Sovereign Health Fortress Implementation Files

This directory contains all the implementation files for the **Cognitive Hardening** phase and **Security Stack** of iLuminara-Core.

## 📁 Directory Structure

```
repository-files/
├── .github/
│   ├── workflows/
│   │   ├── codeql.yml              # SAST security scanning
│   │   └── gitleaks.yml            # Secret detection
│   └── dependabot.yml              # Daily security updates
├── config/
│   └── sovereign_guardrail.yaml    # Sovereignty configuration
├── core/
│   └── safety_gate.py              # CoT-based refusal logic
├── governance_kernel/
│   ├── ethical_specifications.json # 14 core safety rules
│   ├── crypto_shredder.py          # IP-02: Data dissolution
│   └── metrics.py                  # Comprehensive metrics tracking
├── intelligence_engine/
│   ├── train_cot.py                # Chain-of-Thought fine-tuning
│   └── rl_optimizer.py             # Humanitarian reward model
├── scripts/
│   ├── generate_synthetic_humanitarian_data.py  # Synthetic data generator
│   └── validate_fortress.sh        # Fortress validation script
├── tests/
│   └── ood_generalization.py       # Out-of-distribution tests
└── .gitleaks.toml                  # Gitleaks configuration
```

## 🚀 Quick Start

### 1. Copy Files to Your Repository

```bash
# From your iLuminara-Core repository root
cp -r /path/to/repository-files/* .
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

Required packages:
- `cryptography` - For IP-02 Crypto Shredder
- `torch` - For Spiral AGI training
- `transformers` - For CoT fine-tuning
- `google-cloud-*` - For GCP integration

### 3. Validate the Fortress

```bash
chmod +x scripts/validate_fortress.sh
./scripts/validate_fortress.sh
```

Expected output:
```
🛡️  FORTRESS STATUS: OPERATIONAL
✓  All critical components validated
✓  Security audit layer active
✓  Governance kernel operational
✓  Nuclear IP stack initialized
```

## 🔐 Security Stack

### CodeQL SAST Scanning

Continuous static application security testing.

**File:** `.github/workflows/codeql.yml`

**Compliance:**
- GDPR Art. 32 (Security of Processing)
- ISO 27001 A.12.6 (Technical Vulnerability Management)

**Trigger:** Push to main/develop, PRs, Weekly schedule

### Gitleaks Secret Scanning

Detects hardcoded secrets and credentials.

**File:** `.github/workflows/gitleaks.yml`

**Compliance:**
- NIST SP 800-53 (IA-5 Authenticator Management)
- HIPAA §164.312(a)(2)(i)

**Trigger:** Push to main/develop, Daily at 2 AM UTC

### Dependabot Security Updates

Daily automated dependency updates.

**File:** `.github/dependabot.yml`

**Features:**
- Daily Python dependency updates
- Weekly GitHub Actions updates
- Security-only updates for production
- Grouped updates by category

## 🧠 Cognitive Hardening

### 1. Ethical Specifications

**File:** `governance_kernel/ethical_specifications.json`

Defines 14 core safety rules with:
- Legal basis (GDPR, KDPA, HIPAA, etc.)
- Edge case scenarios
- Conflict resolution hierarchy
- Humanitarian margin calculations

### 2. Synthetic Data Generation

**File:** `scripts/generate_synthetic_humanitarian_data.py`

Generates 10,000 synthetic patient/outbreak records with:
- 30% edge cases
- Validation against SovereignGuardrail
- Context distillation for training

**Usage:**
```bash
python scripts/generate_synthetic_humanitarian_data.py
```

**Output:**
- `data/synthetic/humanitarian_training_data.jsonl`
- `data/synthetic/dataset_metadata.json`

### 3. Chain-of-Thought Fine-Tuning

**File:** `intelligence_engine/train_cot.py`

Supervised Fine-Tuning with:
- Golden Thread reasoning embedded in weights
- IP-04 Silent Flux anxiety regulation
- Legal citation training
- Humanitarian margin calculations

**Usage:**
```bash
python intelligence_engine/train_cot.py
```

**Requirements:**
- GPU recommended (CUDA)
- 16GB+ RAM
- ~50GB disk space for model

### 4. RL Optimization

**File:** `intelligence_engine/rl_optimizer.py`

Proximal Policy Optimization with humanitarian reward model:
- +1.0 for Geneva Convention alignment
- -5.0 for PII exposure violations
- +0.5 for correct legal citations
- -2.0 for discrimination

**Usage:**
```bash
python intelligence_engine/rl_optimizer.py
```

### 5. Refusal Logic

**File:** `core/safety_gate.py`

CoT-based refusal system with:
- Sovereignty violation detection
- Consent validation
- Child protection checks
- Detailed reasoning chains

**Usage:**
```python
from core.safety_gate import SafetyGate

gate = SafetyGate()
should_refuse, refusal, reasoning = gate.should_refuse(query)
```

### 6. OOD Generalization Tests

**File:** `tests/ood_generalization.py`

Tests unknown pathogen scenarios ("Type X"):
- Golden Thread integrity
- Sovereignty compliance
- Reasoning coherence

**Usage:**
```bash
python tests/ood_generalization.py
```

**Success Criteria:**
- Golden Thread: ≥80% success
- Sovereignty: ≥95% compliance

## 📊 Metrics Tracking

**File:** `governance_kernel/metrics.py`

Tracks four key dimensions:

1. **Compliance Accuracy** - vs 14 legal frameworks
2. **Reasoning Coherence** - CoT logic quality
3. **Humanitarian Margin Error** - Ethical calculation accuracy
4. **Latency** - API, 5DM Bridge, inference

**Usage:**
```python
from governance_kernel.metrics import get_metrics_tracker

tracker = get_metrics_tracker()
tracker.record_compliance_check(True, "GDPR")
summary = tracker.get_summary()
```

**Prometheus Export:**
```python
metrics = tracker.export_prometheus_metrics()
```

## 🛡️ IP-02: Crypto Shredder

**File:** `governance_kernel/crypto_shredder.py`

Data is not deleted; it is cryptographically dissolved.

**Features:**
- Ephemeral key encryption (AES-256-GCM)
- Retention policies (HOT, WARM, COLD, ETERNAL)
- Auto-shred expired keys
- Tamper-proof audit trail

**Usage:**
```python
from governance_kernel.crypto_shredder import CryptoShredder, RetentionPolicy

shredder = CryptoShredder(sovereignty_zone=SovereigntyZone.KENYA)

# Encrypt
encrypted_data, key_id = shredder.encrypt_with_ephemeral_key(
    data=patient_record,
    retention_policy=RetentionPolicy.HOT
)

# Shred key (data becomes irrecoverable)
shredder.shred_key(key_id)
```

## ⚙️ Configuration

### SovereignGuardrail Configuration

**File:** `config/sovereign_guardrail.yaml`

Configure:
- Jurisdiction (primary and secondary)
- Data residency rules
- Cross-border transfer policies
- Consent management
- Retention policies
- Audit settings
- Humanitarian constraints

**Example:**
```yaml
jurisdiction:
  primary: "KDPA_KE"
  secondary:
    - "GDPR_EU"
    - "POPIA_ZA"

sovereignty:
  data_residency:
    enabled: true
    enforcement_level: "STRICT"
```

## 🧪 Testing

### Run All Tests

```bash
# Validate fortress
./scripts/validate_fortress.sh

# Test OOD generalization
python tests/ood_generalization.py

# Test safety gate
python core/safety_gate.py

# Test metrics
python governance_kernel/metrics.py
```

### Expected Results

All tests should pass with:
- ✅ Fortress validation: OPERATIONAL
- ✅ OOD generalization: ≥80% success
- ✅ Safety gate: Correct refusals
- ✅ Metrics: Accurate tracking

## 📝 Deployment Checklist

- [ ] Copy all files to repository
- [ ] Install dependencies
- [ ] Configure `config/sovereign_guardrail.yaml`
- [ ] Set environment variables (NODE_ID, JURISDICTION)
- [ ] Run fortress validation
- [ ] Generate synthetic data
- [ ] Train CoT model
- [ ] Run RL optimization
- [ ] Test OOD generalization
- [ ] Enable GitHub workflows
- [ ] Configure Dependabot
- [ ] Set up Prometheus monitoring

## 🔗 Integration Points

### With Existing iLuminara Components

1. **Governance Kernel** - Integrates with existing `vector_ledger.py`
2. **Edge Node** - Uses Golden Thread for data fusion
3. **Cloud Oracle** - Metrics exported to Prometheus
4. **Dashboard** - CoT reasoning displayed in UI
5. **API Service** - Safety gate validates all requests

## 📚 Documentation

Full documentation available at:
- **Security Stack:** `/security/overview`
- **Cognitive Hardening:** `/cognitive-hardening/overview`
- **Governance Kernel:** `/governance/overview`
- **AI Agents:** `/ai-agents/overview`

## 🆘 Troubleshooting

### Fortress Validation Fails

```bash
# Check missing dependencies
pip install -r requirements.txt

# Verify file structure
ls -la governance_kernel/
ls -la .github/workflows/
```

### Training Fails (GPU)

```bash
# Check CUDA availability
python -c "import torch; print(torch.cuda.is_available())"

# Use CPU fallback
export CUDA_VISIBLE_DEVICES=""
```

### Metrics Not Tracking

```bash
# Initialize metrics tracker
python -c "from governance_kernel.metrics import get_metrics_tracker; tracker = get_metrics_tracker(); print(tracker.get_summary())"
```

## 🎯 Next Steps

1. **Deploy to Production**
   ```bash
   ./deploy_gcp_prototype.sh
   ```

2. **Monitor Metrics**
   ```bash
   curl http://localhost:9090/metrics
   ```

3. **Continuous Improvement**
   - Review audit logs daily
   - Retrain models monthly
   - Update ethical specifications quarterly

## 📞 Support

For issues or questions:
- GitHub Issues: https://github.com/VISENDI56/iLuminara-Core/issues
- Documentation: https://docs.iluminara.health

---

**The Sovereign Health Fortress is now operational.**

Transform preventable suffering from statistical inevitability to historical anomaly.
