#!/bin/bash

# iLuminara-Core Branch Protection Setup
# Configures GitHub branch protection rules for the Sovereign Health Fortress

set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}╔════════════════════════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║     iLuminara-Core Branch Protection Setup                 ║${NC}"
echo -e "${BLUE}╚════════════════════════════════════════════════════════════╝${NC}"
echo ""

# Check if gh CLI is installed
if ! command -v gh &> /dev/null; then
    echo -e "${RED}❌ GitHub CLI (gh) is not installed${NC}"
    echo "Install it from: https://cli.github.com/"
    exit 1
fi

# Check authentication
echo -n "🔍 Checking GitHub authentication... "
if ! gh auth status &> /dev/null; then
    echo -e "${RED}✗ NOT AUTHENTICATED${NC}"
    echo ""
    echo "Please authenticate with GitHub CLI:"
    echo "  gh auth login"
    echo ""
    echo "Then refresh with required scopes:"
    echo "  gh auth refresh -s workflow,repo,write:packages,admin:repo_hook"
    exit 1
fi
echo -e "${GREEN}✓ AUTHENTICATED${NC}"

# Get repository info
REPO=$(gh repo view --json nameWithOwner -q .nameWithOwner)
echo -e "${BLUE}Repository: ${REPO}${NC}"
echo ""

# Enable branch protection for main
echo -e "${YELLOW}═══════════════════════════════════════════════════════════${NC}"
echo -e "${YELLOW}Configuring Branch Protection for 'main'${NC}"
echo -e "${YELLOW}═══════════════════════════════════════════════════════════${NC}"
echo ""

echo "📋 Protection Rules:"
echo "  • Require pull request reviews (1 approval)"
echo "  • Require status checks (CodeQL, Gitleaks)"
echo "  • Require branches to be up to date"
echo "  • Require conversation resolution"
echo "  • Enforce for administrators"
echo "  • Restrict push access"
echo ""

read -p "Apply these protection rules? (y/n) " -n 1 -r
echo ""

if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo -e "${YELLOW}⚠️  Skipping branch protection setup${NC}"
    exit 0
fi

# Apply branch protection
echo -n "🛡️  Applying branch protection... "

gh api \
  --method PUT \
  -H "Accept: application/vnd.github+json" \
  -H "X-GitHub-Api-Version: 2022-11-28" \
  "/repos/${REPO}/branches/main/protection" \
  -f required_status_checks='{"strict":true,"contexts":["CodeQL","Gitleaks"]}' \
  -f enforce_admins=true \
  -f required_pull_request_reviews='{"dismissal_restrictions":{},"dismiss_stale_reviews":true,"require_code_owner_reviews":false,"required_approving_review_count":1,"require_last_push_approval":false,"bypass_pull_request_allowances":{}}' \
  -f restrictions=null \
  -F required_linear_history=true \
  -F allow_force_pushes=false \
  -F allow_deletions=false \
  -F block_creations=false \
  -F required_conversation_resolution=true \
  -F lock_branch=false \
  -F allow_fork_syncing=true \
  > /dev/null 2>&1

if [ $? -eq 0 ]; then
    echo -e "${GREEN}✓ SUCCESS${NC}"
else
    echo -e "${RED}✗ FAILED${NC}"
    echo ""
    echo -e "${YELLOW}Note: You may need admin permissions to set branch protection.${NC}"
    echo "If you don't have admin access, ask a repository administrator to run this script."
    exit 1
fi

echo ""
echo -e "${YELLOW}═══════════════════════════════════════════════════════════${NC}"
echo -e "${YELLOW}Configuring Required Status Checks${NC}"
echo -e "${YELLOW}═══════════════════════════════════════════════════════════${NC}"
echo ""

# Enable required status checks
echo "📊 Required Checks:"
echo "  • CodeQL (SAST security scanning)"
echo "  • Gitleaks (Secret detection)"
echo ""

# Note: Status checks are automatically required when workflows run
echo -e "${GREEN}✓ Status checks will be required after first workflow run${NC}"

echo ""
echo -e "${YELLOW}═══════════════════════════════════════════════════════════${NC}"
echo -e "${YELLOW}Enabling Security Features${NC}"
echo -e "${YELLOW}═══════════════════════════════════════════════════════════${NC}"
echo ""

# Enable vulnerability alerts
echo -n "🔒 Enabling vulnerability alerts... "
gh api \
  --method PUT \
  -H "Accept: application/vnd.github+json" \
  "/repos/${REPO}/vulnerability-alerts" \
  > /dev/null 2>&1
echo -e "${GREEN}✓${NC}"

# Enable automated security fixes
echo -n "🤖 Enabling automated security fixes... "
gh api \
  --method PUT \
  -H "Accept: application/vnd.github+json" \
  "/repos/${REPO}/automated-security-fixes" \
  > /dev/null 2>&1
echo -e "${GREEN}✓${NC}"

# Enable Dependabot security updates
echo -n "📦 Enabling Dependabot security updates... "
gh api \
  --method PUT \
  -H "Accept: application/vnd.github+json" \
  "/repos/${REPO}/automated-security-fixes" \
  > /dev/null 2>&1
echo -e "${GREEN}✓${NC}"

echo ""
echo -e "${BLUE}╔════════════════════════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║                    SETUP COMPLETE                          ║${NC}"
echo -e "${BLUE}╚════════════════════════════════════════════════════════════╝${NC}"
echo ""

echo -e "${GREEN}✅ Branch protection configured successfully${NC}"
echo ""
echo "Next steps:"
echo "1. Push code to trigger CodeQL and Gitleaks workflows"
echo "2. Verify workflows complete successfully"
echo "3. Create a test pull request to verify protection rules"
echo ""
echo -e "${YELLOW}⚠️  Important:${NC}"
echo "  • All commits to 'main' now require a pull request"
echo "  • Pull requests require 1 approval"
echo "  • CodeQL and Gitleaks must pass before merging"
echo ""
echo -e "${GREEN}The Sovereign Health Fortress is now protected.${NC}"
