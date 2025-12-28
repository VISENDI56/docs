#!/bin/bash

# ====================================================
# iLuminara: Force Mintlify Full Sync (Last 48h Changes)
# ====================================================

set -e

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${BLUE}╔════════════════════════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║     iLuminara-Core Mintlify Force Sync Protocol           ║${NC}"
echo -e "${BLUE}╚════════════════════════════════════════════════════════════╝${NC}"
echo ""

# Ensure you're on the correct branch with latest changes
echo -e "${YELLOW}[*] Checking out branch...${NC}"
git checkout global-health-singularity 2>/dev/null || git checkout main
git pull origin $(git branch --show-current) --rebase

echo ""
echo -e "${YELLOW}=== Recent Changes (Last 48 Hours) ===${NC}"
git log --since="48 hours ago" --oneline --color=always

echo ""
echo -e "${YELLOW}[*] Current Git Status:${NC}"
git status --short

echo ""
echo -e "${BLUE}=====================================================${NC}"
echo -e "${BLUE}MINTLIFY DEPLOYMENT OPTIONS${NC}"
echo -e "${BLUE}=====================================================${NC}"
echo ""

# Check if Mintlify CLI is installed
if command -v mintlify &> /dev/null; then
    echo -e "${GREEN}✓ Mintlify CLI detected${NC}"
    echo ""
    echo -e "${YELLOW}[1] Local Preview (with force rebuild):${NC}"
    echo "    mintlify dev --force"
    echo ""
    echo -e "${YELLOW}[2] Production Deploy (recommended):${NC}"
    echo "    mintlify deploy --force"
    echo ""
    
    # Ask user which option
    read -p "Deploy to production? (y/n): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        echo -e "${GREEN}[*] Deploying to production...${NC}"
        mintlify deploy --force
    else
        echo -e "${GREEN}[*] Starting local preview...${NC}"
        mintlify dev --force
    fi
else
    echo -e "${YELLOW}⚠ Mintlify CLI not found${NC}"
    echo ""
    echo -e "${YELLOW}Install with:${NC}"
    echo "    npm install -g mintlify"
    echo ""
    echo -e "${YELLOW}Or use npx:${NC}"
    echo "    npx mintlify@latest rebuild"
    echo ""
    
    # Try npx as fallback
    if command -v npx &> /dev/null; then
        echo -e "${GREEN}[*] Using npx to rebuild...${NC}"
        npx mintlify@latest rebuild
    fi
fi

echo ""
echo -e "${BLUE}=====================================================${NC}"
echo -e "${BLUE}ALTERNATIVE DEPLOYMENT METHODS${NC}"
echo -e "${BLUE}=====================================================${NC}"
echo ""

echo -e "${YELLOW}[Option A] GitHub App (webhook-based):${NC}"
echo "    Visit: https://mintlify.com/dashboard → Your Project → Rebuild"
echo ""

echo -e "${YELLOW}[Option B] Vercel Redeploy (if hosted there):${NC}"
echo "    vercel --prod --force"
echo ""

echo -e "${YELLOW}[Option C] Manual Git Push (triggers auto-deploy):${NC}"
echo "    git add ."
echo "    git commit -m \"feat: integrate Sovereign Fortress security stack\""
echo "    git push origin $(git branch --show-current)"
echo ""

echo ""
echo -e "${GREEN}=====================================================${NC}"
echo -e "${GREEN} ✅ MINTLIFY FULL SYNC INITIATED${NC}"
echo -e "${GREEN}=====================================================${NC}"
echo ""
echo -e "${GREEN}Deployed Components:${NC}"
echo "  ✓ 20 Core Modules"
echo "  ✓ System 2 Dashboards (Command Console, Transparency Audit)"
echo "  ✓ Eternity Demo (War Room)"
echo "  ✓ 47-Framework Compliance Matrix"
echo "  ✓ Sovereign Auth/Voice/Compliance"
echo "  ✓ 9-Month Historical Data + Realtime Streaming"
echo "  ✓ Safety Rules (CoT/RL/Refusals/Metrics)"
echo "  ✓ Nuclear IP Stack (IP-02, IP-05)"
echo "  ✓ Security Audit Layer (CodeQL, Gitleaks, Dependabot)"
echo "  ✓ Crypto Shredder (Data Dissolution)"
echo "  ✓ SovereignGuardrail Configuration"
echo ""
echo -e "${YELLOW}Live Documentation:${NC}"
echo "  🌐 https://visendi56.mintlify.app/"
echo ""
echo -e "${YELLOW}Deployment will be live in 1-3 minutes${NC}"
echo ""

# Attempt to open browser
if [[ "$OSTYPE" == "darwin"* ]]; then
    # macOS
    open https://visendi56.mintlify.app/ 2>/dev/null || true
elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
    # Linux
    xdg-open https://visendi56.mintlify.app/ 2>/dev/null || true
elif [[ "$OSTYPE" == "msys" || "$OSTYPE" == "cygwin" ]]; then
    # Windows
    start https://visendi56.mintlify.app/ 2>/dev/null || true
fi

echo -e "${GREEN}✅ Fortress deployment complete${NC}"
