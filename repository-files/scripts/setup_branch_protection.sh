#!/bin/bash

# iLuminara-Core Branch Protection Setup
# Configures GitHub branch protection rules for the Sovereign Health Fortress

set -e

# Colors for output
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

# Check if authenticated
if ! gh auth status &> /dev/null; then
    echo -e "${YELLOW}⚠️  Not authenticated with GitHub${NC}"
    echo "Run: gh auth login"
    exit 1
fi

# Get repository info
REPO=$(gh repo view --json nameWithOwner -q .nameWithOwner)

if [ -z "$REPO" ]; then
    echo -e "${RED}❌ Could not determine repository${NC}"
    echo "Make sure you're in a git repository"
    exit 1
fi

echo -e "${GREEN}📦 Repository: $REPO${NC}"
echo ""

# Refresh auth with required scopes
echo -e "${YELLOW}🔐 Refreshing GitHub authentication with required scopes...${NC}"
gh auth refresh -s workflow,repo,write:packages,admin:repo_hook

echo ""
echo -e "${YELLOW}═══════════════════════════════════════════════════════════${NC}"
echo -e "${YELLOW}Configuring Branch Protection for 'main'${NC}"
echo -e "${YELLOW}═══════════════════════════════════════════════════════════${NC}"
echo ""

# Enable branch protection for main
echo -e "${BLUE}🛡️  Enabling branch protection...${NC}"

# Create branch protection rule
gh api \
  --method PUT \
  -H "Accept: application/vnd.github+json" \
  -H "X-GitHub-Api-Version: 2022-11-28" \
  "/repos/$REPO/branches/main/protection" \
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

echo -e "${GREEN}✅ Branch protection enabled for 'main'${NC}"
echo ""

echo -e "${YELLOW}═══════════════════════════════════════════════════════════${NC}"
echo -e "${YELLOW}Branch Protection Rules Summary${NC}"
echo -e "${YELLOW}═══════════════════════════════════════════════════════════${NC}"
echo ""

echo -e "${GREEN}✓${NC} Require pull request before merging"
echo -e "${GREEN}✓${NC} Require 1 approval"
echo -e "${GREEN}✓${NC} Dismiss stale reviews"
echo -e "${GREEN}✓${NC} Require status checks to pass:"
echo "  - CodeQL (SAST security scanning)"
echo "  - Gitleaks (Secret detection)"
echo -e "${GREEN}✓${NC} Require conversation resolution"
echo -e "${GREEN}✓${NC} Enforce for administrators"
echo -e "${GREEN}✓${NC} Block force pushes"
echo -e "${GREEN}✓${NC} Block deletions"

echo ""
echo -e "${YELLOW}═══════════════════════════════════════════════════════════${NC}"
echo -e "${YELLOW}Enabling Security Features${NC}"
echo -e "${YELLOW}═══════════════════════════════════════════════════════════${NC}"
echo ""

# Enable Dependabot security updates
echo -e "${BLUE}🤖 Enabling Dependabot security updates...${NC}"
gh api \
  --method PUT \
  -H "Accept: application/vnd.github+json" \
  -H "X-GitHub-Api-Version: 2022-11-28" \
  "/repos/$REPO/automated-security-fixes"

echo -e "${GREEN}✅ Dependabot security updates enabled${NC}"

# Enable Dependabot alerts
echo -e "${BLUE}🔔 Enabling Dependabot alerts...${NC}"
gh api \
  --method PUT \
  -H "Accept: application/vnd.github+json" \
  -H "X-GitHub-Api-Version: 2022-11-28" \
  "/repos/$REPO/vulnerability-alerts"

echo -e "${GREEN}✅ Dependabot alerts enabled${NC}"

# Enable secret scanning
echo -e "${BLUE}🔐 Enabling secret scanning...${NC}"
gh api \
  --method PUT \
  -H "Accept: application/vnd.github+json" \
  -H "X-GitHub-Api-Version: 2022-11-28" \
  "/repos/$REPO/secret-scanning"

echo -e "${GREEN}✅ Secret scanning enabled${NC}"

# Enable secret scanning push protection
echo -e "${BLUE}🛡️  Enabling secret scanning push protection...${NC}"
gh api \
  --method PUT \
  -H "Accept: application/vnd.github+json" \
  -H "X-GitHub-Api-Version: 2022-11-28" \
  "/repos/$REPO/secret-scanning/push-protection"

echo -e "${GREEN}✅ Secret scanning push protection enabled${NC}"

echo ""
echo -e "${BLUE}╔════════════════════════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║                    FORTRESS SECURED                        ║${NC}"
echo -e "${BLUE}╚════════════════════════════════════════════════════════════╝${NC}"
echo ""

echo -e "${GREEN}🛡️  The Sovereign Health Fortress is now protected:${NC}"
echo ""
echo "✓ Branch protection active on 'main'"
echo "✓ Required status checks: CodeQL, Gitleaks"
echo "✓ Pull request reviews required"
echo "✓ Dependabot security updates enabled"
echo "✓ Secret scanning enabled"
echo "✓ Push protection enabled"
echo ""
echo -e "${YELLOW}Next steps:${NC}"
echo "1. Ensure .github/workflows/codeql.yml exists"
echo "2. Ensure .github/workflows/gitleaks.yml exists"
echo "3. Ensure .github/dependabot.yml exists"
echo "4. Create a pull request to test the protection"
echo ""
echo -e "${GREEN}The Fortress is operational.${NC}"
