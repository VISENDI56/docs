#!/bin/bash
# ------------------------------------------------------------------------------
# Copyright (c) 2025 iLuminara (VISENDI56). All Rights Reserved.
# Licensed under the Polyform Shield License 1.0.0.
# 
# BioNeMo Model Downloader - Air-Gapped NGC Sync
# ------------------------------------------------------------------------------

set -euo pipefail

# Configuration
NGC_CLI="${NGC_CLI:-ngc}"
MODELS_DIR="${MODELS_DIR:-/models/bionemo}"
CACHE_DIR="${CACHE_DIR:-/cache/ngc}"
REGISTRY_FILE="${REGISTRY_FILE:-./registry.yaml}"
VERIFY_CHECKSUMS="${VERIFY_CHECKSUMS:-true}"

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

log_info() { echo -e "${GREEN}[INFO]${NC} $1"; }
log_warn() { echo -e "${YELLOW}[WARN]${NC} $1"; }
log_error() { echo -e "${RED}[ERROR]${NC} $1"; }
log_step() { echo -e "${BLUE}[STEP]${NC} $1"; }

# Model definitions (from registry.yaml)
declare -A MODELS=(
    ["alphafold2"]="nvidia/clara/alphafold2:latest"
    ["esmfold"]="nvidia/clara/esmfold:latest"
    ["rfdiffusion"]="nvidia/clara/rfdiffusion:latest"
    ["proteinmpnn"]="nvidia/clara/proteinmpnn:latest"
    ["diffdock"]="nvidia/clara/diffdock:latest"
)

# Check prerequisites
check_prerequisites() {
    log_step "Checking prerequisites..."
    
    if ! command -v ${NGC_CLI} &> /dev/null; then
        log_error "NGC CLI not found. Install from: https://ngc.nvidia.com/setup/installers/cli"
        exit 1
    fi
    
    if ! ${NGC_CLI} config current &> /dev/null; then
        log_error "NGC CLI not configured. Run: ngc config set"
        exit 1
    fi
    
    log_info "Prerequisites check passed ✓"
}

# Create directories
setup_directories() {
    log_step "Setting up directories..."
    mkdir -p "${MODELS_DIR}"
    mkdir -p "${CACHE_DIR}"
    log_info "Directories created ✓"
}

# Download single model
download_model() {
    local model_name=$1
    local model_path=$2
    
    log_step "Downloading ${model_name}..."
    
    local output_dir="${MODELS_DIR}/${model_name}"
    mkdir -p "${output_dir}"
    
    # Download using NGC CLI
    if ${NGC_CLI} registry model download-version "${model_path}" \
        --dest "${output_dir}" 2>&1 | tee "${CACHE_DIR}/${model_name}_download.log"; then
        log_info "${model_name} downloaded successfully ✓"
        return 0
    else
        log_error "${model_name} download failed"
        return 1
    fi
}

# Download all models
download_all_models() {
    log_step "Downloading all models..."
    
    local failed_models=()
    
    for model_name in "${!MODELS[@]}"; do
        if ! download_model "${model_name}" "${MODELS[$model_name]}"; then
            failed_models+=("${model_name}")
        fi
    done
    
    if [ ${#failed_models[@]} -eq 0 ]; then
        log_info "All models downloaded successfully ✓"
    else
        log_warn "Failed to download: ${failed_models[*]}"
    fi
}

# Verify checksums
verify_checksums() {
    log_step "Verifying checksums..."
    
    # Generate checksums file
    find "${MODELS_DIR}" -type f -exec sha256sum {} \; > "${MODELS_DIR}/checksums.txt"
    
    log_info "Checksums generated: ${MODELS_DIR}/checksums.txt"
    log_warn "Verify checksums against registry.yaml manually"
}

# Create model manifest
create_manifest() {
    log_step "Creating model manifest..."
    
    cat > "${MODELS_DIR}/manifest.json" <<EOF
{
  "generated_at": "$(date -u +%Y-%m-%dT%H:%M:%SZ)",
  "models_dir": "${MODELS_DIR}",
  "models": [
$(for model in "${!MODELS[@]}"; do
    echo "    {\"name\": \"${model}\", \"path\": \"${MODELS_DIR}/${model}\"},"
done | sed '$ s/,$//')
  ]
}
EOF
    
    log_info "Manifest created: ${MODELS_DIR}/manifest.json"
}

# Package for air-gapped transfer
package_for_transfer() {
    log_step "Packaging models for air-gapped transfer..."
    
    local archive_name="bionemo_models_$(date +%Y%m%d).tar.gz"
    
    tar -czf "${archive_name}" -C "$(dirname ${MODELS_DIR})" "$(basename ${MODELS_DIR})"
    
    log_info "Archive created: ${archive_name}"
    log_info "Transfer this file to air-gapped system"
    log_info "Extract with: tar -xzf ${archive_name} -C /models/"
}

# Usage information
usage() {
    cat <<EOF
Usage: $0 [OPTIONS]

Download BioNeMo models from NGC for air-gapped deployment.

OPTIONS:
    --models MODEL1,MODEL2    Download specific models (comma-separated)
    --all                     Download all models
    --verify-checksums        Verify checksums after download
    --package                 Create archive for air-gapped transfer
    --help                    Show this help message

EXAMPLES:
    # Download all models
    $0 --all --verify-checksums --package
    
    # Download specific models
    $0 --models alphafold2,esmfold
    
    # Air-gapped workflow
    # 1. On internet-connected system:
    $0 --all --package
    
    # 2. Transfer archive to air-gapped system
    scp bionemo_models_*.tar.gz airgapped:/tmp/
    
    # 3. On air-gapped system:
    tar -xzf /tmp/bionemo_models_*.tar.gz -C /models/

ENVIRONMENT VARIABLES:
    NGC_CLI           Path to NGC CLI (default: ngc)
    MODELS_DIR        Models directory (default: /models/bionemo)
    CACHE_DIR         Cache directory (default: /cache/ngc)
    VERIFY_CHECKSUMS  Verify checksums (default: true)

EOF
}

# Main execution
main() {
    local download_all=false
    local specific_models=()
    local do_package=false
    
    # Parse arguments
    while [[ $# -gt 0 ]]; do
        case $1 in
            --all)
                download_all=true
                shift
                ;;
            --models)
                IFS=',' read -ra specific_models <<< "$2"
                shift 2
                ;;
            --verify-checksums)
                VERIFY_CHECKSUMS=true
                shift
                ;;
            --package)
                do_package=true
                shift
                ;;
            --help)
                usage
                exit 0
                ;;
            *)
                log_error "Unknown option: $1"
                usage
                exit 1
                ;;
        esac
    done
    
    log_info "BioNeMo Model Downloader - Air-Gapped NGC Sync"
    log_info "================================================"
    
    check_prerequisites
    setup_directories
    
    if [ "$download_all" = true ]; then
        download_all_models
    elif [ ${#specific_models[@]} -gt 0 ]; then
        for model in "${specific_models[@]}"; do
            if [ -n "${MODELS[$model]}" ]; then
                download_model "${model}" "${MODELS[$model]}"
            else
                log_warn "Unknown model: ${model}"
            fi
        done
    else
        log_error "No models specified. Use --all or --models"
        usage
        exit 1
    fi
    
    if [ "$VERIFY_CHECKSUMS" = true ]; then
        verify_checksums
    fi
    
    create_manifest
    
    if [ "$do_package" = true ]; then
        package_for_transfer
    fi
    
    log_info "================================================"
    log_info "Download complete! ✓"
    log_info "Models location: ${MODELS_DIR}"
    log_info "Next steps:"
    log_info "  1. Verify checksums against registry.yaml"
    log_info "  2. Transfer to air-gapped system (if needed)"
    log_info "  3. Update paths in blackwell_bionemo_config.yaml"
}

main "$@"
