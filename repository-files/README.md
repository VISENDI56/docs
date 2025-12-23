# iLuminara-Core Repository Files

This directory contains all the implementation files for the Sovereign Health Fortress technical evolution (Steps 36-42).

## Directory Structure

```
repository-files/
├── .github/
│   ├── workflows/
│   │   ├── codeql.yml              # SAST security scanning
│   │   └── gitleaks.yml            # Secret detection
│   └── dependabot.yml              # Daily security updates
├── .gitleaks.toml                  # Gitleaks configuration
├── governance_kernel/
│   └── crypto_shredder.py          # IP-02: Data dissolution
├── edge_node/
│   ├── sync_agent.py               # HSML Offline-First Sync
│   └── hsml_reconciler.py          # Conflict resolution
├── config/
│   └── sovereign_guardrail.yaml    # Compliance configuration
└── scripts/
    ├── validate_fortress.sh        # System validation
    └── generate_compliance_bundle.py  # Compliance artifacts
```

## Installation Instructions

### 1. Copy Files to Your Repository

```bash
# From the docs repository root
cd repository-files

# Copy to your iLuminara-Core repository
cp -r .github/* /path/to/iLuminara-Core/.github/
cp .gitleaks.toml /path/to/iLuminara-Core/
cp -r governance_kernel/* /path/to/iLuminara-Core/governance_kernel/
cp -r edge_node/* /path/to/iLuminara-Core/edge_node/
cp -r config/* /path/to/iLuminara-Core/config/
cp -r scripts/* /path/to/iLuminara-Core/scripts/

# Make scripts executable
chmod +x /path/to/iLuminara-Core/scripts/*.sh
```

### 2. Install Dependencies

```bash
cd /path/to/iLuminara-Core

# Core dependencies
pip install cryptography flask streamlit pandas
pip install google-cloud-bigquery google-cloud-spanner google-cloud-kms
pip install transformers peft bitsandbytes accelerate
pip install boto3  # For S3 integration
```

### 3. Configure Environment

```bash
# Node configuration
export NODE_ID=JOR-47
export JURISDICTION=KDPA_KE

# GCP configuration
export GOOGLE_CLOUD_PROJECT=your-project-id
export GCP_REGION=africa-south1

# Security configuration
export ENABLE_TAMPER_PROOF_AUDIT=true
export RETENTION_MAX_DAYS=1825
```

### 4. Validate Installation

```bash
# Run fortress validation
./scripts/validate_fortress.sh

# Generate compliance bundle
python scripts/generate_compliance_bundle.py

# Check output
ls -la compliance/artifacts/
```

## Component Overview

### Security Audit Layer

#### CodeQL Workflow (`.github/workflows/codeql.yml`)
- **Purpose:** SAST security scanning
- **Schedule:** Weekly + on push/PR
- **Languages:** Python, JavaScript
- **Compliance:** GDPR Art. 32, ISO 27001 A.12.6

#### Gitleaks Workflow (`.github/workflows/gitleaks.yml`)
- **Purpose:** Secret detection
- **Schedule:** Daily at 2 AM UTC
- **Compliance:** NIST SP 800-53 IA-5, HIPAA §164.312(a)(2)(i)

#### Dependabot (`.github/dependabot.yml`)
- **Purpose:** Daily security updates
- **Ecosystems:** pip, npm, docker, github-actions
- **Strategy:** Security-only updates

### Governance Kernel

#### Crypto Shredder (`governance_kernel/crypto_shredder.py`)
- **IP-02:** Data dissolution (not deletion)
- **Features:**
  - Ephemeral key encryption (AES-256-GCM)
  - Automatic key shredding
  - Retention policy enforcement
  - Sovereignty zone support
- **Compliance:** GDPR Art. 17, HIPAA §164.530(j), NIST SP 800-88

### Edge Node

#### HSML Sync Agent (`edge_node/sync_agent.py`)
- **Purpose:** Offline-first data synchronization
- **Features:**
  - Vector Clock conflict resolution
  - SQLite local buffer
  - 0% data loss guarantee
  - Automatic reconciliation
- **Compliance:** GDPR Art. 32, HIPAA §164.312(b)

#### HSML Reconciler (`edge_node/hsml_reconciler.py`)
- **Purpose:** Advanced conflict resolution
- **Features:**
  - Three-way merge
  - Semantic conflict detection
  - Automatic resolution strategies
  - Manual review queue
- **Compliance:** GDPR Art. 5, HIPAA §164.312(c)(1)

### Configuration

#### SovereignGuardrail Config (`config/sovereign_guardrail.yaml`)
- **Purpose:** Compliance enforcement configuration
- **Features:**
  - 14 global legal frameworks
  - Data sovereignty rules
  - Consent management
  - Retention policies
  - Audit trail settings

### Scripts

#### Fortress Validator (`scripts/validate_fortress.sh`)
- **Purpose:** System integrity validation
- **Phases:**
  1. Security Audit Layer
  2. Governance Kernel
  3. Edge Node & AI Agents
  4. Cloud Oracle
  5. Python Dependencies
  6. Environment Configuration
  7. Nuclear IP Stack Status

#### Compliance Bundle Generator (`scripts/generate_compliance_bundle.py`)
- **Purpose:** Automated compliance evidence
- **Generates:**
  - Encryption proofs
  - IAM logs
  - SovereignGuardrail stats
  - NIST SP 800-53 mappings
  - ISO 27001 Annex A mappings
  - SOC 2 Trust Criteria mappings
  - Executive summary

## Usage Examples

### Example 1: Create Offline Event

```python
from edge_node.sync_agent import HSMLSyncAgent, EventType

# Initialize agent
agent = HSMLSyncAgent(node_id="JOR-47")

# Create event while offline
event = agent.create_event(
    event_type=EventType.CBS_REPORT,
    payload={
        "location": "Dadaab",
        "symptom": "diarrhea",
        "severity": 8,
        "reporter": "CHV_AMINA_HASSAN"
    }
)

# Check buffer stats
stats = agent.get_buffer_stats()
print(f"Pending events: {stats.get('pending', 0)}")

# Sync when connectivity returns
# stats = agent.sync_to_golden_thread(golden_thread_client)
```

### Example 2: Encrypt with Crypto Shredder

```python
from governance_kernel.crypto_shredder import CryptoShredder, RetentionPolicy, SovereigntyZone

# Initialize shredder
shredder = CryptoShredder(
    sovereignty_zone=SovereigntyZone.KENYA,
    enable_audit=True
)

# Encrypt patient data
patient_data = b"Patient ID: 12345, Diagnosis: Malaria"
encrypted_data, key_id = shredder.encrypt_with_ephemeral_key(
    data=patient_data,
    retention_policy=RetentionPolicy.HOT,
    metadata={
        "patient_id": "12345",
        "jurisdiction": "KDPA_KE",
        "data_type": "PHI"
    }
)

print(f"Encrypted with key: {key_id}")

# After retention period, shred key
# shredder.shred_key(key_id)
```

### Example 3: Generate Compliance Bundle

```bash
# Generate full compliance pack
python scripts/generate_compliance_bundle.py

# Output files:
# - compliance/artifacts/encryption_proofs.json
# - compliance/artifacts/iam_least_privilege_logs.json
# - compliance/artifacts/sovereign_guardrail_stats.json
# - compliance/artifacts/nist_sp_800_53_mapping.json
# - compliance/artifacts/iso_27001_annex_a_mapping.json
# - compliance/artifacts/soc2_trust_criteria_mapping.json
# - compliance/artifacts/EXECUTIVE_SUMMARY.md
```

### Example 4: Validate Fortress

```bash
# Run complete validation
./scripts/validate_fortress.sh

# Expected output:
# ✅ Security Audit Layer: OPERATIONAL
# ✅ Governance Kernel: OPERATIONAL
# ✅ Edge Node: OPERATIONAL
# ✅ Nuclear IP Stack: ACTIVE
# 🛡️ FORTRESS STATUS: OPERATIONAL
```

## GitHub Workflow Setup

### Enable Workflows

```bash
# Refresh GitHub permissions
gh auth refresh -s workflow,repo,write:packages,admin:repo_hook

# Commit and push workflows
git add .github/
git commit -m "feat: add security workflows (CodeQL, Gitleaks, Dependabot)"
git push
```

### Enable Branch Protection

```bash
# Require status checks
gh api repos/:owner/:repo/branches/main/protection \
  -X PUT \
  -f required_status_checks[strict]=true \
  -f required_status_checks[contexts][]=CodeQL \
  -f required_status_checks[contexts][]=Gitleaks

# Require pull request reviews
gh api repos/:owner/:repo/branches/main/protection \
  -X PUT \
  -f required_pull_request_reviews[required_approving_review_count]=1
```

## Testing

### Unit Tests

```bash
# Test Crypto Shredder
python -m pytest tests/test_crypto_shredder.py

# Test HSML Sync Agent
python -m pytest tests/test_sync_agent.py

# Test HSML Reconciler
python -m pytest tests/test_reconciler.py
```

### Integration Tests

```bash
# Test full offline workflow
python tests/integration/test_offline_workflow.py

# Test compliance bundle generation
python tests/integration/test_compliance_bundle.py
```

## Troubleshooting

### Issue: CodeQL workflow fails

**Solution:** Ensure Python 3.8+ is installed and all dependencies are in `requirements.txt`

### Issue: Gitleaks detects false positives

**Solution:** Add patterns to `.gitleaks.toml` allowlist:

```toml
[allowlist]
regexes = [
  '''your-pattern-here'''
]
```

### Issue: Crypto Shredder key storage permission denied

**Solution:** Ensure key storage directory is writable:

```bash
mkdir -p ./keys
chmod 700 ./keys
```

### Issue: HSML Sync Agent database locked

**Solution:** Close any open connections to `hsml_buffer.db`:

```python
# Ensure proper connection cleanup
agent = HSMLSyncAgent(node_id="JOR-47")
# ... use agent ...
# Connection auto-closes when agent goes out of scope
```

## Support

For implementation assistance:
- **Technical Support:** tech@iluminara.health
- **Compliance Questions:** compliance@iluminara.health
- **Security Issues:** security@iluminara.health

## License

Copyright © 2025 iLuminara-Core. All rights reserved.
