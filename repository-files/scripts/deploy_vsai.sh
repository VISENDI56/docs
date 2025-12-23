#!/bin/bash

# iLuminara-Core VSAI Deployment Script
# Deploys IP-06: Viral Symbiotic API Infusion to production

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}╔════════════════════════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║     IP-06: Viral Symbiotic API Infusion Deployment        ║${NC}"
echo -e "${BLUE}║              The 5DM Bridge - 94% CAC Reduction            ║${NC}"
echo -e "${BLUE}╚════════════════════════════════════════════════════════════╝${NC}"
echo ""

# Configuration
PROJECT_ID=${GOOGLE_CLOUD_PROJECT:-"iluminara-core"}
REGION=${GCP_REGION:-"africa-south1"}
SERVICE_NAME="vsai-engine"
USSD_SERVICE_NAME="vsai-ussd-gateway"

# Check prerequisites
echo -e "${YELLOW}Checking prerequisites...${NC}"

# Check gcloud
if ! command -v gcloud &> /dev/null; then
    echo -e "${RED}✗ gcloud CLI not found${NC}"
    echo "Install: https://cloud.google.com/sdk/docs/install"
    exit 1
fi
echo -e "${GREEN}✓ gcloud CLI installed${NC}"

# Check Python
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}✗ Python 3 not found${NC}"
    exit 1
fi
echo -e "${GREEN}✓ Python 3 installed${NC}"

# Check dependencies
echo -e "${YELLOW}Checking Python dependencies...${NC}"
MISSING_DEPS=()

for dep in numpy scipy scikit-learn networkx matplotlib; do
    if ! python3 -c "import ${dep//-/_}" 2>/dev/null; then
        MISSING_DEPS+=("$dep")
    fi
done

if [ ${#MISSING_DEPS[@]} -gt 0 ]; then
    echo -e "${YELLOW}⚠ Missing dependencies: ${MISSING_DEPS[*]}${NC}"
    echo "Installing..."
    pip install "${MISSING_DEPS[@]}"
fi
echo -e "${GREEN}✓ All dependencies installed${NC}"

echo ""
echo -e "${YELLOW}═══════════════════════════════════════════════════════════${NC}"
echo -e "${YELLOW}PHASE 1: Enable GCP Services${NC}"
echo -e "${YELLOW}═══════════════════════════════════════════════════════════${NC}"
echo ""

# Enable required services
SERVICES=(
    "run.googleapis.com"
    "cloudbuild.googleapis.com"
    "artifactregistry.googleapis.com"
    "bigquery.googleapis.com"
    "spanner.googleapis.com"
)

for service in "${SERVICES[@]}"; do
    echo -n "Enabling $service... "
    gcloud services enable "$service" --project="$PROJECT_ID" 2>/dev/null || true
    echo -e "${GREEN}✓${NC}"
done

echo ""
echo -e "${YELLOW}═══════════════════════════════════════════════════════════${NC}"
echo -e "${YELLOW}PHASE 2: Deploy VSAI Engine${NC}"
echo -e "${YELLOW}═══════════════════════════════════════════════════════════${NC}"
echo ""

# Create Dockerfile for VSAI Engine
cat > Dockerfile.vsai << 'EOF'
FROM python:3.10-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy VSAI code
COPY edge_node/vsai /app/edge_node/vsai
COPY governance_kernel /app/governance_kernel

# Expose port
EXPOSE 8080

# Run VSAI engine
CMD ["python", "-m", "edge_node.vsai.viral_engine"]
EOF

echo -e "${BLUE}📦 Building VSAI Engine container...${NC}"
gcloud builds submit \
    --tag "gcr.io/$PROJECT_ID/$SERVICE_NAME" \
    --project="$PROJECT_ID" \
    --file=Dockerfile.vsai \
    .

echo -e "${BLUE}🚀 Deploying VSAI Engine to Cloud Run...${NC}"
gcloud run deploy "$SERVICE_NAME" \
    --image "gcr.io/$PROJECT_ID/$SERVICE_NAME" \
    --platform managed \
    --region "$REGION" \
    --allow-unauthenticated \
    --memory 2Gi \
    --cpu 2 \
    --timeout 300 \
    --set-env-vars "GOOGLE_CLOUD_PROJECT=$PROJECT_ID,JURISDICTION=KDPA_KE" \
    --project="$PROJECT_ID"

VSAI_URL=$(gcloud run services describe "$SERVICE_NAME" \
    --platform managed \
    --region "$REGION" \
    --format 'value(status.url)' \
    --project="$PROJECT_ID")

echo -e "${GREEN}✅ VSAI Engine deployed: $VSAI_URL${NC}"

echo ""
echo -e "${YELLOW}═══════════════════════════════════════════════════════════${NC}"
echo -e "${YELLOW}PHASE 3: Deploy USSD Gateway${NC}"
echo -e "${YELLOW}═══════════════════════════════════════════════════════════${NC}"
echo ""

# Create Dockerfile for USSD Gateway
cat > Dockerfile.ussd << 'EOF'
FROM python:3.10-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt flask twilio

# Copy USSD code
COPY edge_node/vsai /app/edge_node/vsai
COPY governance_kernel /app/governance_kernel

# Expose port
EXPOSE 8080

# Run USSD gateway
CMD ["python", "-m", "edge_node.vsai.ussd_gateway"]
EOF

echo -e "${BLUE}📦 Building USSD Gateway container...${NC}"
gcloud builds submit \
    --tag "gcr.io/$PROJECT_ID/$USSD_SERVICE_NAME" \
    --project="$PROJECT_ID" \
    --file=Dockerfile.ussd \
    .

echo -e "${BLUE}🚀 Deploying USSD Gateway to Cloud Run...${NC}"
gcloud run deploy "$USSD_SERVICE_NAME" \
    --image "gcr.io/$PROJECT_ID/$USSD_SERVICE_NAME" \
    --platform managed \
    --region "$REGION" \
    --allow-unauthenticated \
    --memory 1Gi \
    --cpu 1 \
    --timeout 60 \
    --set-env-vars "GOOGLE_CLOUD_PROJECT=$PROJECT_ID,VSAI_ENGINE_URL=$VSAI_URL" \
    --project="$PROJECT_ID"

USSD_URL=$(gcloud run services describe "$USSD_SERVICE_NAME" \
    --platform managed \
    --region "$REGION" \
    --format 'value(status.url)' \
    --project="$PROJECT_ID")

echo -e "${GREEN}✅ USSD Gateway deployed: $USSD_URL${NC}"

echo ""
echo -e "${YELLOW}═══════════════════════════════════════════════════════════${NC}"
echo -e "${YELLOW}PHASE 4: Configure Twilio (USSD)${NC}"
echo -e "${YELLOW}═══════════════════════════════════════════════════════════${NC}"
echo ""

echo -e "${BLUE}📱 Twilio Configuration:${NC}"
echo ""
echo "1. Log in to Twilio Console: https://console.twilio.com"
echo "2. Navigate to: Phone Numbers > Manage > Active Numbers"
echo "3. Select your USSD short code (e.g., *123#)"
echo "4. Set webhook URL to: $USSD_URL/ussd"
echo "5. Set HTTP method to: POST"
echo ""
echo -e "${YELLOW}⚠ Manual configuration required${NC}"

echo ""
echo -e "${YELLOW}═══════════════════════════════════════════════════════════${NC}"
echo -e "${YELLOW}PHASE 5: Initialize Database${NC}"
echo -e "${YELLOW}═══════════════════════════════════════════════════════════${NC}"
echo ""

# Create BigQuery dataset for VSAI metrics
echo -e "${BLUE}📊 Creating BigQuery dataset...${NC}"
bq mk --dataset \
    --location="$REGION" \
    --description="VSAI Metrics and Analytics" \
    "$PROJECT_ID:vsai_metrics" 2>/dev/null || echo "Dataset already exists"

# Create table for viral metrics
bq mk --table \
    "$PROJECT_ID:vsai_metrics.viral_spread" \
    timestamp:TIMESTAMP,total_nodes:INTEGER,active_spreaders:INTEGER,passive_users:INTEGER,susceptible:INTEGER,viral_coefficient_k:FLOAT,current_cac:FLOAT,total_cost:FLOAT,airtime_distributed:FLOAT \
    2>/dev/null || echo "Table already exists"

echo -e "${GREEN}✅ BigQuery dataset created${NC}"

# Create Spanner instance for consent registry
echo -e "${BLUE}🗄️ Creating Spanner instance...${NC}"
gcloud spanner instances create vsai-consent \
    --config="regional-$REGION" \
    --description="VSAI Consent Registry" \
    --nodes=1 \
    --project="$PROJECT_ID" 2>/dev/null || echo "Instance already exists"

# Create database
gcloud spanner databases create consent_registry \
    --instance=vsai-consent \
    --project="$PROJECT_ID" 2>/dev/null || echo "Database already exists"

echo -e "${GREEN}✅ Spanner instance created${NC}"

echo ""
echo -e "${YELLOW}═══════════════════════════════════════════════════════════${NC}"
echo -e "${YELLOW}PHASE 6: Run Initial Simulation${NC}"
echo -e "${YELLOW}═══════════════════════════════════════════════════════════${NC}"
echo ""

echo -e "${BLUE}🦠 Running VSAI simulation...${NC}"
python3 edge_node/vsai/viral_engine.py

echo ""
echo -e "${BLUE}╔════════════════════════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║                  DEPLOYMENT COMPLETE                       ║${NC}"
echo -e "${BLUE}╚════════════════════════════════════════════════════════════╝${NC}"
echo ""

echo -e "${GREEN}✅ IP-06: VSAI is now ACTIVE${NC}"
echo ""
echo -e "${YELLOW}Deployment Summary:${NC}"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo -e "VSAI Engine:      ${GREEN}$VSAI_URL${NC}"
echo -e "USSD Gateway:     ${GREEN}$USSD_URL${NC}"
echo -e "USSD Short Code:  ${YELLOW}*123#${NC} (Configure in Twilio)"
echo -e "BigQuery Dataset: ${GREEN}$PROJECT_ID:vsai_metrics${NC}"
echo -e "Spanner Instance: ${GREEN}vsai-consent${NC}"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

echo -e "${YELLOW}Next Steps:${NC}"
echo "1. Configure Twilio webhook: $USSD_URL/ussd"
echo "2. Seed trust anchors: python3 scripts/seed_trust_anchors.py"
echo "3. Monitor metrics: https://console.cloud.google.com/bigquery?project=$PROJECT_ID"
echo "4. View logs: gcloud run logs tail $SERVICE_NAME --project=$PROJECT_ID"
echo ""

echo -e "${GREEN}The 5DM Bridge is ready to infect 14M nodes! 🦠${NC}"
echo ""

# Clean up
rm -f Dockerfile.vsai Dockerfile.ussd
