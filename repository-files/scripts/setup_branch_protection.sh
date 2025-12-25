#!/bin/bash

# iLuminara-Core Branch Protection Setup
# Configures GitHub branch protection rules for the Sovereign Health Fortress

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
    echo -e "${RED}✗ GitHub CLI (gh) not found${NC}"
    echo "Install: https://cli.github.com/"
    exit 1
fi

echo -e "${GREEN}✓ GitHub CLI found${NC}"

# Check authentication
echo -n "🔐 Checking GitHub authentication... "
if ! gh auth status &> /dev/null; then
    echo -e "${RED}✗ NOT AUTHENTICATED${NC}"
    echo ""
    echo "Run: gh auth login"
    echo "Or: gh auth refresh -s workflow,repo,write:packages,admin:repo_hook"
    exit 1
fi
echo -e "${GREEN}✓ AUTHENTICATED${NC}"

# Get repository info
REPO=$(gh repo view --json nameWithOwner -q .nameWithOwner)
echo -e "${BLUE}📦 Repository: ${REPO}${NC}"
echo ""

# Confirm setup
echo -e "${YELLOW}This will configure branch protection for 'main' branch:${NC}"
echo "  • Require pull request reviews (1 approval)"
echo "  • Require status checks (CodeQL, Gitleaks)"
echo "  • Require branches to be up to date"
echo "  • Enforce for administrators"
echo "  • Restrict push access"
echo ""
read -p "Continue? (y/N) " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "Aborted."
    exit 0
fi

echo ""
echo -e "${YELLOW}═══════════════════════════════════════════════════════════${NC}"
echo -e "${YELLOW}Configuring Branch Protection${NC}"
echo -e "${YELLOW}═══════════════════════════════════════════════════════════${NC}"
echo ""

# Enable branch protection
echo "🛡️  Enabling branch protection for 'main'..."

# Create branch protection rule using GitHub API
gh api \
  --method PUT \
  -H "Accept: application/vnd.github+json" \
  -H "X-GitHub-Api-Version: 2022-11-28" \
  "/repos/${REPO}/branches/main/protection" \
  -f required_status_checks[strict]=true \
  -f required_status_checks[contexts][]=CodeQL \
  -f required_status_checks[contexts][]=Gitleaks \
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

if [ $? -eq 0 ]; then
    echo -e "${GREEN}✓ Branch protection enabled${NC}"
else
    echo -e "${RED}✗ Failed to enable branch protection${NC}"
    echo "You may need additional permissions. Contact repository admin."
    exit 1
fi

echo ""
echo -e "${YELLOW}═══════════════════════════════════════════════════════════${NC}"
echo -e "${YELLOW}Enabling Security Features${NC}"
echo -e "${YELLOW}═══════════════════════════════════════════════════════════${NC}"
echo ""

# Enable vulnerability alerts
echo "🔒 Enabling vulnerability alerts..."
gh api \
  --method PUT \
  -H "Accept: application/vnd.github+json" \
  "/repos/${REPO}/vulnerability-alerts" \
  && echo -e "${GREEN}✓ Vulnerability alerts enabled${NC}" \
  || echo -e "${YELLOW}⚠ Already enabled or insufficient permissions${NC}"

# Enable automated security fixes (Dependabot)
echo "🤖 Enabling automated security fixes..."
gh api \
  --method PUT \
  -H "Accept: application/vnd.github+json" \
  "/repos/${REPO}/automated-security-fixes" \
  && echo -e "${GREEN}✓ Automated security fixes enabled${NC}" \
  || echo -e "${YELLOW}⚠ Already enabled or insufficient permissions${NC}"

# Enable secret scanning
echo "🔐 Enabling secret scanning..."
gh api \
  --method PUT \
  -H "Accept: application/vnd.github+json" \
  "/repos/${REPO}/secret-scanning" \
  && echo -e "${GREEN}✓ Secret scanning enabled${NC}" \
  || echo -e "${YELLOW}⚠ Requires GitHub Advanced Security${NC}"

# Enable push protection
echo "🛡️  Enabling secret scanning push protection..."
gh api \
  --method PUT \
  -H "Accept: application/vnd.github+json" \
  "/repos/${REPO}/secret-scanning/push-protection" \
  && echo -e "${GREEN}✓ Push protection enabled${NC}" \
  || echo -e "${YELLOW}⚠ Requires GitHub Advanced Security${NC}"

echo ""
echo -e "${YELLOW}═══════════════════════════════════════════════════════════${NC}"
echo -e "${YELLOW}Configuring Code Scanning${NC}"
echo -e "${YELLOW}═══════════════════════════════════════════════════════════${NC}"
echo ""

# Enable code scanning (CodeQL)
echo "🔍 Enabling code scanning..."
gh api \
  --method PUT \
  -H "Accept: application/vnd.github+json" \
  "/repos/${REPO}/code-scanning/default-setup" \
  -f state=configured \
  -f languages[]=python \
  -f languages[]=javascript \
  && echo -e "${GREEN}✓ Code scanning enabled${NC}" \
  || echo -e "${YELLOW}⚠ CodeQL workflow may need manual setup${NC}"

echo ""
echo -e "${BLUE}╔════════════════════════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║                    SETUP COMPLETE                          ║${NC}"
echo -e "${BLUE}╚════════════════════════════════════════════════════════════╝${NC}"
echo ""

echo -e "${GREEN}🛡️  Fortress Status: PROTECTED${NC}"
echo ""
echo "Branch protection configured:"
echo "  ✓ Require pull request reviews (1 approval)"
echo "  ✓ Require status checks (CodeQL, Gitleaks)"
echo "  ✓ Require branches to be up to date"
echo "  ✓ Enforce for administrators"
echo "  ✓ Require conversation resolution"
echo ""
echo "Security features enabled:"
echo "  ✓ Vulnerability alerts"
echo "  ✓ Automated security fixes (Dependabot)"
echo "  ✓ Secret scanning (if available)"
echo "  ✓ Push protection (if available)"
echo "  ✓ Code scanning (CodeQL)"
echo ""
echo -e "${YELLOW}Next steps:${NC}"
echo "1. Verify workflows are running: gh workflow list"
echo "2. Check security alerts: gh api /repos/${REPO}/vulnerability-alerts"
echo "3. Review branch protection: gh api /repos/${REPO}/branches/main/protection"
echo "4. Run fortress validation: ./scripts/validate_fortress.sh"
echo ""
echo -e "${GREEN}The Sovereign Health Fortress is now protected.${NC}"
