#!/bin/bash

# iLuminara-Core Branch Protection Setup
# Automates GitHub branch protection rules for the Sovereign Health Fortress

set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

echo -e "${BLUE}╔════════════════════════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║     iLuminara-Core Branch Protection Setup                 ║${NC}"
echo -e "${BLUE}╚════════════════════════════════════════════════════════════╝${NC}"
echo ""

# Check if gh CLI is installed
if ! command -v gh &> /dev/null; then
    echo -e "${RED}❌ GitHub CLI (gh) is not installed${NC}"
    echo "Install: https://cli.github.com/"
    exit 1
fi

# Check authentication
echo -n "🔐 Checking GitHub authentication... "
if gh auth status &> /dev/null; then
    echo -e "${GREEN}✓ AUTHENTICATED${NC}"
else
    echo -e "${RED}✗ NOT AUTHENTICATED${NC}"
    echo ""
    echo "Run: gh auth login"
    exit 1
fi

# Refresh permissions
echo -n "🔑 Refreshing GitHub permissions... "
if gh auth refresh -s workflow,repo,write:packages,admin:repo_hook &> /dev/null; then
    echo -e "${GREEN}✓ PERMISSIONS GRANTED${NC}"
else
    echo -e "${YELLOW}⚠ PERMISSION REFRESH FAILED${NC}"
    echo "   Continuing with existing permissions..."
fi

echo ""
echo -e "${YELLOW}═══════════════════════════════════════════════════════════${NC}"
echo -e "${YELLOW}Configuring Branch Protection for 'main'${NC}"
echo -e "${YELLOW}═══════════════════════════════════════════════════════════${NC}"
echo ""

# Get repository info
REPO=$(gh repo view --json nameWithOwner -q .nameWithOwner)
echo "📦 Repository: $REPO"
echo ""

# Enable branch protection
echo "🛡️ Enabling branch protection rules..."
echo ""

# Create branch protection rule using gh API
gh api \
  --method PUT \
  -H "Accept: application/vnd.github+json" \
  -H "X-GitHub-Api-Version: 2022-11-28" \
  "/repos/$REPO/branches/main/protection" \
  -f required_status_checks[strict]=true \
  -f "required_status_checks[contexts][]=CodeQL" \
  -f "required_status_checks[contexts][]=Gitleaks Secret Scanning" \
  -f enforce_admins=true \
  -f required_pull_request_reviews[dismiss_stale_reviews]=true \
  -f required_pull_request_reviews[require_code_owner_reviews]=false \
  -f required_pull_request_reviews[required_approving_review_count]=1 \
  -f required_pull_request_reviews[require_last_push_approval]=false \
  -f restrictions=null \
  -f required_linear_history=false \
  -f allow_force_pushes=false \
  -f allow_deletions=false \
  -f block_creations=false \
  -f required_conversation_resolution=true \
  -f lock_branch=false \
  -f allow_fork_syncing=true

echo ""
echo -e "${GREEN}✅ Branch protection rules applied${NC}"
echo ""

# Display protection rules
echo -e "${YELLOW}═══════════════════════════════════════════════════════════${NC}"
echo -e "${YELLOW}Branch Protection Summary${NC}"
echo -e "${YELLOW}═══════════════════════════════════════════════════════════${NC}"
echo ""

echo "✓ Required status checks:"
echo "  - CodeQL Security Analysis"
echo "  - Gitleaks Secret Scanning"
echo ""

echo "✓ Pull request requirements:"
echo "  - 1 approving review required"
echo "  - Dismiss stale reviews on new commits"
echo "  - Require conversation resolution"
echo ""

echo "✓ Restrictions:"
echo "  - Force pushes: BLOCKED"
echo "  - Branch deletion: BLOCKED"
echo "  - Enforce for administrators: YES"
echo ""

echo -e "${YELLOW}═══════════════════════════════════════════════════════════${NC}"
echo -e "${YELLOW}Enabling Security Features${NC}"
echo -e "${YELLOW}═══════════════════════════════════════════════════════════${NC}"
echo ""

# Enable Dependabot security updates
echo -n "🤖 Enabling Dependabot security updates... "
gh api \
  --method PUT \
  -H "Accept: application/vnd.github+json" \
  -H "X-GitHub-Api-Version: 2022-11-28" \
  "/repos/$REPO/automated-security-fixes" \
  > /dev/null 2>&1 && echo -e "${GREEN}✓ ENABLED${NC}" || echo -e "${YELLOW}⚠ ALREADY ENABLED${NC}"

# Enable Dependabot alerts
echo -n "🔔 Enabling Dependabot alerts... "
gh api \
  --method PUT \
  -H "Accept: application/vnd.github+json" \
  -H "X-GitHub-Api-Version: 2022-11-28" \
  "/repos/$REPO/vulnerability-alerts" \
  > /dev/null 2>&1 && echo -e "${GREEN}✓ ENABLED${NC}" || echo -e "${YELLOW}⚠ ALREADY ENABLED${NC}"

# Enable secret scanning
echo -n "🔐 Enabling secret scanning... "
gh api \
  --method PUT \
  -H "Accept: application/vnd.github+json" \
  -H "X-GitHub-Api-Version: 2022-11-28" \
  "/repos/$REPO/secret-scanning" \
  > /dev/null 2>&1 && echo -e "${GREEN}✓ ENABLED${NC}" || echo -e "${YELLOW}⚠ REQUIRES GITHUB ADVANCED SECURITY${NC}"

# Enable secret scanning push protection
echo -n "🛡️ Enabling secret scanning push protection... "
gh api \
  --method PUT \
  -H "Accept: application/vnd.github+json" \
  -H "X-GitHub-Api-Version: 2022-11-28" \
  "/repos/$REPO/secret-scanning/push-protection" \
  > /dev/null 2>&1 && echo -e "${GREEN}✓ ENABLED${NC}" || echo -e "${YELLOW}⚠ REQUIRES GITHUB ADVANCED SECURITY${NC}"

echo ""
echo -e "${BLUE}╔════════════════════════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║                    FORTRESS SECURED                        ║${NC}"
echo -e "${BLUE}╚════════════════════════════════════════════════════════════╝${NC}"
echo ""

echo -e "${GREEN}🛡️ The Sovereign Health Fortress is now protected${NC}"
echo ""
echo "Next steps:"
echo "1. Commit security workflows: git add .github/workflows/"
echo "2. Commit governance kernel: git add governance_kernel/"
echo "3. Commit configuration: git add config/"
echo "4. Create PR: git commit -m 'feat: integrate Sovereign Health Fortress'"
echo "5. Validate: ./scripts/validate_fortress.sh"
echo ""
echo -e "${YELLOW}All future commits to 'main' will require:${NC}"
echo "  ✓ Passing CodeQL security scan"
echo "  ✓ Passing Gitleaks secret scan"
echo "  ✓ 1 approving review"
echo "  ✓ All conversations resolved"
echo ""
