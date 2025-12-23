#!/bin/bash

# iLuminara-Core Branch Protection Setup Script
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
    echo -e "${RED}✗ GitHub CLI (gh) is not installed${NC}"
    echo "Install from: https://cli.github.com/"
    exit 1
fi

# Check if authenticated
if ! gh auth status &> /dev/null; then
    echo -e "${YELLOW}⚠ Not authenticated with GitHub CLI${NC}"
    echo "Run: gh auth login"
    exit 1
fi

# Get repository info
REPO=$(gh repo view --json nameWithOwner -q .nameWithOwner)
echo -e "${GREEN}✓ Repository: $REPO${NC}"
echo ""

# Enable branch protection for main
echo -e "${YELLOW}═══════════════════════════════════════════════════════════${NC}"
echo -e "${YELLOW}Configuring Branch Protection for 'main'${NC}"
echo -e "${YELLOW}═══════════════════════════════════════════════════════════${NC}"
echo ""

# Create branch protection rule
echo "🔒 Enabling branch protection..."

gh api \
  --method PUT \
  -H "Accept: application/vnd.github+json" \
  -H "X-GitHub-Api-Version: 2022-11-28" \
  "/repos/$REPO/branches/main/protection" \
  -f required_status_checks='{"strict":true,"contexts":["CodeQL","Gitleaks"]}' \
  -f enforce_admins=true \
  -f required_pull_request_reviews='{"dismissal_restrictions":{},"dismiss_stale_reviews":true,"require_code_owner_reviews":true,"required_approving_review_count":1}' \
  -f restrictions=null \
  -f required_linear_history=true \
  -f allow_force_pushes=false \
  -f allow_deletions=false \
  -f block_creations=false \
  -f required_conversation_resolution=true \
  -f lock_branch=false \
  -f allow_fork_syncing=true

echo -e "${GREEN}✓ Branch protection enabled${NC}"
echo ""

# Enable security features
echo -e "${YELLOW}═══════════════════════════════════════════════════════════${NC}"
echo -e "${YELLOW}Enabling Security Features${NC}"
echo -e "${YELLOW}═══════════════════════════════════════════════════════════${NC}"
echo ""

# Enable Dependabot security updates
echo "🔐 Enabling Dependabot security updates..."
gh api \
  --method PUT \
  -H "Accept: application/vnd.github+json" \
  -H "X-GitHub-Api-Version: 2022-11-28" \
  "/repos/$REPO/automated-security-fixes"

echo -e "${GREEN}✓ Dependabot security updates enabled${NC}"

# Enable Dependabot alerts
echo "🔐 Enabling Dependabot alerts..."
gh api \
  --method PUT \
  -H "Accept: application/vnd.github+json" \
  -H "X-GitHub-Api-Version: 2022-11-28" \
  "/repos/$REPO/vulnerability-alerts"

echo -e "${GREEN}✓ Dependabot alerts enabled${NC}"

# Enable secret scanning
echo "🔐 Enabling secret scanning..."
gh api \
  --method PUT \
  -H "Accept: application/vnd.github+json" \
  -H "X-GitHub-Api-Version: 2022-11-28" \
  "/repos/$REPO/secret-scanning"

echo -e "${GREEN}✓ Secret scanning enabled${NC}"

# Enable secret scanning push protection
echo "🔐 Enabling secret scanning push protection..."
gh api \
  --method PUT \
  -H "Accept: application/vnd.github+json" \
  -H "X-GitHub-Api-Version: 2022-11-28" \
  "/repos/$REPO/secret-scanning/push-protection"

echo -e "${GREEN}✓ Secret scanning push protection enabled${NC}"

# Enable code scanning
echo "🔐 Enabling code scanning..."
gh api \
  --method PUT \
  -H "Accept: application/vnd.github+json" \
  -H "X-GitHub-Api-Version: 2022-11-28" \
  "/repos/$REPO/code-scanning/default-setup" \
  -f state='configured' \
  -f languages='["python","javascript"]'

echo -e "${GREEN}✓ Code scanning enabled${NC}"

echo ""
echo -e "${BLUE}╔════════════════════════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║                    SETUP COMPLETE                          ║${NC}"
echo -e "${BLUE}╚════════════════════════════════════════════════════════════╝${NC}"
echo ""

echo -e "${GREEN}✓ Branch protection configured for 'main'${NC}"
echo -e "${GREEN}✓ Required status checks: CodeQL, Gitleaks${NC}"
echo -e "${GREEN}✓ Pull request reviews required: 1 approval${NC}"
echo -e "${GREEN}✓ Dependabot security updates enabled${NC}"
echo -e "${GREEN}✓ Secret scanning enabled${NC}"
echo -e "${GREEN}✓ Code scanning enabled${NC}"
echo ""

echo -e "${YELLOW}Branch Protection Rules:${NC}"
echo "  • Require pull request before merging"
echo "  • Require 1 approval"
echo "  • Dismiss stale reviews"
echo "  • Require code owner reviews"
echo "  • Require status checks to pass (CodeQL, Gitleaks)"
echo "  • Require branches to be up to date"
echo "  • Require conversation resolution"
echo "  • Require linear history"
echo "  • Block force pushes"
echo "  • Block deletions"
echo ""

echo -e "${GREEN}The Sovereign Health Fortress is now protected.${NC}"
echo ""
