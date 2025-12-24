# iLuminara-Core: Hyper-Law Singularity Implementation Files

## Overview

This directory contains all implementation files for the **Hyper-Law Singularity** - iLuminara-Core's 45+ framework compliance orchestration system.

## Directory Structure

```
repository-files/
├── .github/
│   ├── workflows/
│   │   ├── codeql.yml              # CodeQL SAST scanning
│   │   └── gitleaks.yml            # Secret detection
│   └── dependabot.yml              # Daily security updates
├── .gitleaks.toml                  # Gitleaks configuration
├── governance_kernel/
│   ├── crypto_shredder.py          # IP-02: Data dissolution
│   ├── omni_law_matrix.py          # 45+ framework orchestration
│   ├── ai_governance.py            # EU AI Act + FDA compliance
│   └── global_health_harmonizer.py # IHR 2005 + WHO integration
├── config/
│   └── sovereign_guardrail.yaml    # Compliance configuration
├── scripts/
│   └── validate_fortress.sh        # Fortress validation
├── IMPLEMENTATION_GUIDE_HYPER_LAW.md  # Step-by-step guide
├── DEPLOYMENT_SUMMARY.md           # Complete deployment summary
└── README.md                       # This file
```

## Quick Start

### 1. Copy Files to Your Repository

```bash
# From this directory
cp -r .github/ /path/to/iLuminara-Core/
cp .gitleaks.toml /path/to/iLuminara-Core/
cp -r governance_kernel/ /path/to/iLuminara-Core/
cp -r config/ /path/to/iLuminara-Core/
cp -r scripts/ /path/to/iLuminara-Core/
```

### 2. Install Dependencies

```bash
cd /path/to/iLuminara-Core
pip install -r requirements.txt
```

**Required packages:**
- `cryptography>=41.0.0`
- `shap>=0.42.0`
- `google-cloud-bigquery>=3.11.0`
- `google-cloud-spanner>=3.40.0`

### 3. Run Validation

```bash
chmod +x scripts/validate_fortress.sh
./scripts/validate_fortress.sh
```

### 4. Test Components

```bash
# Test Omni-Law Matrix
python -m governance_kernel.omni_law_matrix

# Test AI Governance
python -m governance_kernel.ai_governance

# Test Global Health Harmonizer
python -m governance_kernel.global_health_harmonizer

# Test Crypto Shredder
python -m governance_kernel.crypto_shredder
```

## File Descriptions

### Security Workflows

#### `.github/workflows/codeql.yml`
- **Purpose**: Continuous SAST security scanning
- **Triggers**: Push to main/develop, PRs, weekly schedule
- **Languages**: Python, JavaScript
- **Compliance**: GDPR Art. 32, ISO 27001 A.12.6

#### `.github/workflows/gitleaks.yml`
- **Purpose**: Secret detection and credential scanning
- **Triggers**: Push to main/develop, daily schedule
- **Features**: SARIF upload, sovereignty violation detection
- **Compliance**: NIST SP 800-53 IA-5, HIPAA §164.312(a)(2)(i)

#### `.github/dependabot.yml`
- **Purpose**: Automated dependency updates
- **Frequency**: Daily for security updates
- **Ecosystems**: pip, GitHub Actions, Docker, npm
- **Features**: Grouped updates, security-only mode

#### `.gitleaks.toml`
- **Purpose**: Secret detection rules
- **Features**: Sovereignty-aware (blocks AWS keys), custom rules for GCP/GitHub
- **Allowlist**: Test files, documentation, examples

### Governance Kernel

#### `governance_kernel/crypto_shredder.py`
- **Purpose**: IP-02 implementation - cryptographic data dissolution
- **Features**:
  - Ephemeral key encryption
  - Auto-shred after retention period
  - Retention policies: HOT (180d), WARM (365d), COLD (1825d)
  - Tamper-proof audit trail
- **Compliance**: GDPR Art. 17, HIPAA §164.530(j), NIST SP 800-88

#### `governance_kernel/omni_law_matrix.py`
- **Purpose**: Dynamic 45+ framework orchestration
- **Features**:
  - Context-aware framework activation
  - AI-actuated compliance triggers
  - Retroactive harmonization
  - Multi-jurisdictional conflict resolution
- **Frameworks**: 45+ across 11 categories

#### `governance_kernel/ai_governance.py`
- **Purpose**: AI compliance for EU AI Act and FDA guidance
- **Features**:
  - High-risk AI conformity assessment
  - SHAP explainability
  - Bias detection and mitigation
  - Post-market performance monitoring
  - Transparency reporting
- **Compliance**: EU AI Act, FDA CDS Software, ISO 42001, IMDRF

#### `governance_kernel/global_health_harmonizer.py`
- **Purpose**: WHO integration and outbreak reporting
- **Features**:
  - IHR 2005 automatic notification (24-hour requirement)
  - PHEIC event detection
  - JEE indicator mapping
  - One Health signal fusion
- **Compliance**: IHR 2005, GHSA, JEE Standards

### Configuration

#### `config/sovereign_guardrail.yaml`
- **Purpose**: Central compliance configuration
- **Sections**:
  - Jurisdiction settings
  - Data sovereignty rules
  - Explainability requirements
  - Consent management
  - Data retention policies
  - Audit trail configuration
  - Humanitarian constraints
  - Framework activation
  - Enforcement actions

### Scripts

#### `scripts/validate_fortress.sh`
- **Purpose**: Complete fortress validation
- **Phases**:
  1. Security Audit Layer
  2. Governance Kernel
  3. Edge Node & AI Agents
  4. Cloud Oracle
  5. Python Dependencies
  6. Environment Configuration
  7. Nuclear IP Stack Status
- **Output**: Detailed validation report with pass/fail status

## Integration Examples

### Example 1: Validate AI Prediction

```python
from governance_kernel.omni_law_matrix import OmniLawMatrix, ComplianceContext
from governance_kernel.ai_governance import AIGovernance

# Initialize
matrix = OmniLawMatrix(enable_ai_triggers=True)
governance = AIGovernance(enable_shap=True)

# Define context
context = ComplianceContext(
    action_type="prediction",
    data_type="PHI",
    jurisdiction="Kenya",
    ai_involved=True,
    high_risk=True,
    outbreak_context=True
)

# Validate
result = matrix.validate_action(context)

if not result['compliant']:
    print(f"Violations: {result['violations']}")
    print(f"Recommendations: {result['recommendations']}")
```

### Example 2: Process Outbreak Event

```python
from governance_kernel.global_health_harmonizer import GlobalHealthHarmonizer, OutbreakEvent
from datetime import datetime

# Initialize
harmonizer = GlobalHealthHarmonizer(
    national_focal_point="kenya.nfp@health.go.ke",
    country_code="KE",
    enable_auto_notification=True
)

# Create event
event = OutbreakEvent(
    event_id="KE-CHOLERA-2025-001",
    disease="cholera",
    location={"name": "Dadaab", "border_proximity": True},
    case_count=156,
    death_count=12,
    r_effective=2.8,
    severity_score=0.75,
    detection_timestamp=datetime.utcnow().isoformat()
)

# Process (auto-notifies WHO if required)
result = harmonizer.process_outbreak_event(event)
```

### Example 3: Encrypt with Crypto Shredder

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

# After retention period, shred key
shredder.shred_key(key_id)

# Data is now cryptographically irrecoverable
```

## Environment Variables

Required environment variables:

```bash
# Node Configuration
export NODE_ID=JOR-47
export JURISDICTION=KDPA_KE

# API Configuration
export API_HOST=0.0.0.0
export API_PORT=8080

# GCP Configuration (if using cloud)
export GOOGLE_CLOUD_PROJECT=your-project-id
export GCP_REGION=us-central1

# Governance Configuration
export ENABLE_TAMPER_PROOF_AUDIT=true
export RETENTION_MAX_DAYS=1825
export AUDIT_LOG_LEVEL=INFO

# AI Governance
export ENABLE_SHAP_EXPLAINABILITY=true
export ENABLE_BIAS_DETECTION=true

# Global Health Security
export NATIONAL_FOCAL_POINT=your.nfp@health.gov
export ENABLE_WHO_NOTIFICATION=true
```

## Testing

### Unit Tests

```bash
# Test Omni-Law Matrix
python -m pytest tests/test_omni_law_matrix.py

# Test AI Governance
python -m pytest tests/test_ai_governance.py

# Test Global Health Harmonizer
python -m pytest tests/test_global_health_harmonizer.py

# Test Crypto Shredder
python -m pytest tests/test_crypto_shredder.py
```

### Integration Tests

```bash
# Run full validation
./scripts/validate_fortress.sh

# Test with demo data
python examples/hyper_law_demo.py
```

## Compliance Matrix

| Framework | Module | Status |
|-----------|--------|--------|
| EU AI Act | `ai_governance.py` | ✅ Active |
| IHR 2005 | `global_health_harmonizer.py` | ✅ Active |
| GDPR | `omni_law_matrix.py` | ✅ Active |
| KDPA | `omni_law_matrix.py` | ✅ Active |
| Malabo Convention | `omni_law_matrix.py` | ✅ Active |
| IFRS S1/S2 | `omni_law_matrix.py` | ✅ Active |
| All 45+ Frameworks | `omni_law_matrix.py` | ✅ Active |

## Documentation

- **Implementation Guide**: `IMPLEMENTATION_GUIDE_HYPER_LAW.md`
- **Deployment Summary**: `DEPLOYMENT_SUMMARY.md`
- **Online Docs**: https://docs.iluminara.health

## Support

For issues or questions:

- **GitHub Issues**: https://github.com/VISENDI56/iLuminara-Core/issues
- **Documentation**: https://docs.iluminara.health
- **Email**: support@iluminara.health

## License

iLuminara-Core is licensed under the MIT License.

---

**The Sovereign Health Fortress is ready for deployment.**

Transform preventable suffering from statistical inevitability to historical anomaly.
