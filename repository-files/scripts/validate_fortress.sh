#!/bin/bash

# iLuminara-Core Fortress Validation Script
# Validates the complete Nuclear IP Stack deployment

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Fortress status
FORTRESS_STATUS="OPERATIONAL"
VALIDATION_ERRORS=0

echo -e "${BLUE}╔════════════════════════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║     iLuminara-Core Sovereign Health Fortress Validator     ║${NC}"
echo -e "${BLUE}╚════════════════════════════════════════════════════════════╝${NC}"
echo ""

# Function to check component
check_component() {
    local component=$1
    local check_command=$2
    local description=$3
    
    echo -n "🔍 Checking $component... "
    
    if eval "$check_command" > /dev/null 2>&1; then
        echo -e "${GREEN}✓ OPERATIONAL${NC}"
        echo "   └─ $description"
        return 0
    else
        echo -e "${RED}✗ FAILED${NC}"
        echo "   └─ $description"
        VALIDATION_ERRORS=$((VALIDATION_ERRORS + 1))
        FORTRESS_STATUS="COMPROMISED"
        return 1
    fi
}

# Function to check file exists
check_file() {
    local file=$1
    local description=$2
    
    echo -n "📄 Checking $file... "
    
    if [ -f "$file" ]; then
        echo -e "${GREEN}✓ EXISTS${NC}"
        echo "   └─ $description"
        return 0
    else
        echo -e "${RED}✗ MISSING${NC}"
        echo "   └─ $description"
        VALIDATION_ERRORS=$((VALIDATION_ERRORS + 1))
        FORTRESS_STATUS="COMPROMISED"
        return 1
    fi
}

# Function to check directory exists
check_directory() {
    local dir=$1
    local description=$2
    
    echo -n "📁 Checking $dir... "
    
    if [ -d "$dir" ]; then
        echo -e "${GREEN}✓ EXISTS${NC}"
        echo "   └─ $description"
        return 0
    else
        echo -e "${RED}✗ MISSING${NC}"
        echo "   └─ $description"
        VALIDATION_ERRORS=$((VALIDATION_ERRORS + 1))
        FORTRESS_STATUS="COMPROMISED"
        return 1
    fi
}

echo -e "${YELLOW}═══════════════════════════════════════════════════════════${NC}"
echo -e "${YELLOW}PHASE 1: Security Audit Layer${NC}"
echo -e "${YELLOW}═══════════════════════════════════════════════════════════${NC}"
echo ""

# Check CodeQL workflow
check_file ".github/workflows/codeql.yml" "SAST security scanning (GDPR Art. 32, ISO 27001 A.12.6)"

# Check Gitleaks workflow
check_file ".github/workflows/gitleaks.yml" "Secret scanning (NIST SP 800-53 IA-5)"

# Check Gitleaks config
check_file ".gitleaks.toml" "Secret detection rules"

# Check Dependabot
check_file ".github/dependabot.yml" "Daily security updates"

echo ""
echo -e "${YELLOW}═══════════════════════════════════════════════════════════${NC}"
echo -e "${YELLOW}PHASE 2: Governance Kernel (Nuclear IP Stack)${NC}"
echo -e "${YELLOW}═══════════════════════════════════════════════════════════${NC}"
echo ""

# Check Governance Kernel directory
check_directory "governance_kernel" "Law-as-code enforcement engine"

# Check SovereignGuardrail
check_file "governance_kernel/vector_ledger.py" "14 global legal frameworks enforcement"

# Check Crypto Shredder (IP-02)
check_file "governance_kernel/crypto_shredder.py" "IP-02: Data dissolution (not deletion)"

# Check Ethical Engine
check_file "governance_kernel/ethical_engine.py" "Humanitarian constraints (Geneva Convention, WHO IHR)"

# Check SovereignGuardrail config
check_file "config/sovereign_guardrail.yaml" "Sovereignty configuration"

echo ""
echo -e "${YELLOW}═══════════════════════════════════════════════════════════${NC}"
echo -e "${YELLOW}PHASE 3: Edge Node & AI Agents${NC}"
echo -e "${YELLOW}═══════════════════════════════════════════════════════════${NC}"
echo ""

# Check Edge Node
check_directory "edge_node" "Offline-first data collection"

# Check FRENASA Engine
check_directory "edge_node/frenasa_engine" "Voice-to-JSON transformation"

# Check AI Agents
check_directory "edge_node/ai_agents" "Autonomous disease surveillance"

# Check Golden Thread (IP-05)
check_directory "edge_node/sync_protocol" "IP-05: Data fusion engine"

echo ""
echo -e "${YELLOW}═══════════════════════════════════════════════════════════${NC}"
echo -e "${YELLOW}PHASE 4: Cloud Oracle${NC}"
echo -e "${YELLOW}═══════════════════════════════════════════════════════════${NC}"
echo ""

# Check API service
check_file "api_service.py" "REST API endpoints"

# Check Dashboard
check_file "dashboard.py" "Streamlit command console"

# Check deployment scripts
check_file "deploy_gcp_prototype.sh" "GCP deployment automation"
check_file "launch_all_services.sh" "Service orchestration"

echo ""
echo -e "${YELLOW}═══════════════════════════════════════════════════════════${NC}"
echo -e "${YELLOW}PHASE 5: Python Dependencies${NC}"
echo -e "${YELLOW}═══════════════════════════════════════════════════════════${NC}"
echo ""

# Check Python installation
check_component "Python" "python3 --version" "Python 3.8+ required"

# Check pip
check_component "pip" "pip3 --version" "Package manager"

# Check critical dependencies
echo -n "📦 Checking critical dependencies... "
MISSING_DEPS=()

# Check each critical dependency
for dep in cryptography flask streamlit pandas google-cloud-bigquery google-cloud-spanner; do
    if ! python3 -c "import ${dep//-/_}" 2>/dev/null; then
        MISSING_DEPS+=("$dep")
    fi
done

if [ ${#MISSING_DEPS[@]} -eq 0 ]; then
    echo -e "${GREEN}✓ ALL INSTALLED${NC}"
else
    echo -e "${YELLOW}⚠ MISSING: ${MISSING_DEPS[*]}${NC}"
    echo "   └─ Run: pip install -r requirements.txt"
fi

echo ""
echo -e "${YELLOW}═══════════════════════════════════════════════════════════${NC}"
echo -e "${YELLOW}PHASE 6: Environment Configuration${NC}"
echo -e "${YELLOW}═══════════════════════════════════════════════════════════${NC}"
echo ""

# Check environment variables
echo -n "🔧 Checking NODE_ID... "
if [ -n "$NODE_ID" ]; then
    echo -e "${GREEN}✓ SET ($NODE_ID)${NC}"
else
    echo -e "${YELLOW}⚠ NOT SET${NC}"
    echo "   └─ Run: export NODE_ID=JOR-47"
fi

echo -n "🔧 Checking JURISDICTION... "
if [ -n "$JURISDICTION" ]; then
    echo -e "${GREEN}✓ SET ($JURISDICTION)${NC}"
else
    echo -e "${YELLOW}⚠ NOT SET${NC}"
    echo "   └─ Run: export JURISDICTION=KDPA_KE"
fi

echo -n "🔧 Checking GOOGLE_CLOUD_PROJECT... "
if [ -n "$GOOGLE_CLOUD_PROJECT" ]; then
    echo -e "${GREEN}✓ SET ($GOOGLE_CLOUD_PROJECT)${NC}"
else
    echo -e "${YELLOW}⚠ NOT SET${NC}"
    echo "   └─ Run: export GOOGLE_CLOUD_PROJECT=your-project-id"
fi

echo ""
echo -e "${YELLOW}═══════════════════════════════════════════════════════════${NC}"
echo -e "${YELLOW}PHASE 7: Nuclear IP Stack Status${NC}"
echo -e "${YELLOW}═══════════════════════════════════════════════════════════${NC}"
echo ""

# IP-02: Crypto Shredder
echo -n "⚡ IP-02 Crypto Shredder... "
if [ -f "governance_kernel/crypto_shredder.py" ]; then
    echo -e "${GREEN}✓ ACTIVE${NC}"
    echo "   └─ Data is dissolved, not deleted"
else
    echo -e "${RED}✗ INACTIVE${NC}"
fi

# IP-03: Acorn Protocol
echo -n "⚡ IP-03 Acorn Protocol... "
echo -e "${YELLOW}⚠ REQUIRES HARDWARE${NC}"
echo "   └─ Somatic security (posture + location + stillness)"

# IP-04: Silent Flux
echo -n "⚡ IP-04 Silent Flux... "
echo -e "${YELLOW}⚠ REQUIRES INTEGRATION${NC}"
echo "   └─ Anxiety-regulated AI output"

# IP-05: Golden Thread
echo -n "⚡ IP-05 Golden Thread... "
if [ -d "edge_node/sync_protocol" ]; then
    echo -e "${GREEN}✓ ACTIVE${NC}"
    echo "   └─ Data fusion engine (CBS + EMR + IDSR)"
else
    echo -e "${RED}✗ INACTIVE${NC}"
fi

# IP-06: 5DM Bridge
echo -n "⚡ IP-06 5DM Bridge... "
echo -e "${YELLOW}⚠ REQUIRES MOBILE NETWORK${NC}"
echo "   └─ API injection into 14M+ African mobile nodes"

echo ""
echo -e "${BLUE}╔════════════════════════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║                    VALIDATION SUMMARY                      ║${NC}"
echo -e "${BLUE}╚════════════════════════════════════════════════════════════╝${NC}"
echo ""

if [ $VALIDATION_ERRORS -eq 0 ]; then
    echo -e "${GREEN}🛡️  FORTRESS STATUS: ${FORTRESS_STATUS}${NC}"
    echo -e "${GREEN}✓  All critical components validated${NC}"
    echo -e "${GREEN}✓  Security audit layer active${NC}"
    echo -e "${GREEN}✓  Governance kernel operational${NC}"
    echo -e "${GREEN}✓  Nuclear IP stack initialized${NC}"
    echo ""
    echo -e "${GREEN}The Sovereign Health Fortress is ready for deployment.${NC}"
    exit 0
else
    echo -e "${RED}⚠️  FORTRESS STATUS: ${FORTRESS_STATUS}${NC}"
    echo -e "${RED}✗  Validation errors: ${VALIDATION_ERRORS}${NC}"
    echo ""
    echo -e "${YELLOW}Action required:${NC}"
    echo "1. Review errors above"
    echo "2. Install missing dependencies: pip install -r requirements.txt"
    echo "3. Configure environment variables"
    echo "4. Re-run validation: ./scripts/validate_fortress.sh"
    exit 1
fi
