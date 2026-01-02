#!/bin/bash
# ------------------------------------------------------------------------------
# Copyright (c) 2025 iLuminara (VISENDI56). All Rights Reserved.
# Licensed under the Polyform Shield License 1.0.0.
# 
# BioNeMo Model Downloader - Air-Gapped Deployment Script
# Downloads models from NGC for transfer to air-gapped systems
# ------------------------------------------------------------------------------

set -euo pipefail

# Configuration
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REGISTRY_FILE="${SCRIPT_DIR}/registry.yaml"
MODELS_BASE_DIR="${MODELS_BASE_DIR:-/models/bionemo}"
DOWNLOAD_DIR="${DOWNLOAD_DIR:-/tmp/bionemo_downloads}"
NGC_CLI="${NGC_CLI:-ngc}"

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

# Logging functions
log_info() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

log_warn() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

log_step() {
    echo -e "${BLUE}[STEP]${NC} $1"
}

# Check prerequisites
check_prerequisites() {
    log_step "Checking prerequisites..."
    
    # Check if running on internet-connected system
    if ! ping -c 1 google.com &> /dev/null; then
        log_warn "No internet connection detected. This script requires internet access."
        log_warn "For air-gapped systems, use the transfer instructions instead."
        exit 1
    fi
    
    # Check NGC CLI
    if ! command -v ${NGC_CLI} &> /dev/null; then
        log_error "NGC CLI not found. Installing..."
        install_ngc_cli
    fi
    
    # Check NGC authentication
    if ! ${NGC_CLI} config current &> /dev/null; then
        log_error "NGC CLI not configured. Please run: ngc config set"
        exit 1
    fi
    
    # Check disk space
    available_space=$(df -BG "${DOWNLOAD_DIR}" 2>/dev/null | awk 'NR==2 {print $4}' | sed 's/G//')
    if [ "${available_space}" -lt 500 ]; then
        log_warn "Low disk space: ${available_space}GB available. Recommended: 500GB+"
    fi
    
    log_info "Prerequisites check passed ✓"
}

# Install NGC CLI
install_ngc_cli() {
    log_info "Installing NGC CLI..."
    
    cd /tmp
    wget --content-disposition https://ngc.nvidia.com/downloads/ngccli_linux.zip
    unzip -o ngccli_linux.zip
    chmod +x ngc-cli/ngc
    
    # Move to system path
    sudo mv ngc-cli/ngc /usr/local/bin/ngc
    
    log_info "NGC CLI installed. Please configure: ngc config set"
    exit 0
}

# Parse model list from registry
parse_model_list() {
    local collection="$1"
    
    log_info "Parsing model registry..."
    
    # Extract model sources from registry.yaml
    # This is a simplified parser - in production, use yq or python
    if [ "${collection}" == "all" ]; then
        models=(
            "nvcr.io/nvidia/clara/alphafold2:latest"
            "nvcr.io/nvidia/clara/esmfold:latest"
            "nvcr.io/nvidia/clara/rfdiffusion:latest"
            "nvcr.io/nvidia/clara/proteinmpnn:latest"
            "nvcr.io/nvidia/clara/diffdock:latest"
            "nvcr.io/nvidia/clara/esm2:3b"
            "nvcr.io/nvidia/clara/evo2:70b"
            "nvcr.io/nvidia/clara/geneformer:106m"
            "nvcr.io/nvidia/clara/dnabert:2.0"
            "nvcr.io/nvidia/clara/megamolbart:latest"
            "nvcr.io/nvidia/clara/moimim:latest"
        )
    elif [ "${collection}" == "bio_threat" ]; then
        models=(
            "nvcr.io/nvidia/clara/alphafold2:latest"
            "nvcr.io/nvidia/clara/esmfold:latest"
            "nvcr.io/nvidia/clara/rfdiffusion:latest"
            "nvcr.io/nvidia/clara/proteinmpnn:latest"
        )
    elif [ "${collection}" == "genomic_triage" ]; then
        models=(
            "nvcr.io/nvidia/clara/geneformer:106m"
            "nvcr.io/nvidia/clara/evo2:70b"
            "nvcr.io/nvidia/clara/dnabert:2.0"
        )
    else
        log_error "Unknown collection: ${collection}"
        exit 1
    fi
    
    echo "${models[@]}"
}

# Download single model
download_model() {
    local model_source="$1"
    local model_name=$(echo "${model_source}" | awk -F'/' '{print $NF}' | sed 's/:/-/g')
    
    log_step "Downloading ${model_name}..."
    
    mkdir -p "${DOWNLOAD_DIR}/${model_name}"
    
    # Download using NGC CLI
    if ${NGC_CLI} registry model download-version "${model_source}" \
        --dest "${DOWNLOAD_DIR}/${model_name}"; then
        log_info "Downloaded ${model_name} ✓"
        
        # Generate checksum
        log_info "Generating checksum for ${model_name}..."
        find "${DOWNLOAD_DIR}/${model_name}" -type f -exec sha256sum {} \; > \
            "${DOWNLOAD_DIR}/${model_name}/checksums.txt"
        
        return 0
    else
        log_error "Failed to download ${model_name}"
        return 1
    fi
}

# Download all models in collection
download_collection() {
    local collection="$1"
    
    log_step "Downloading collection: ${collection}"
    
    models=($(parse_model_list "${collection}"))
    total=${#models[@]}
    current=0
    failed=0
    
    for model in "${models[@]}"; do
        current=$((current + 1))
        log_info "Progress: ${current}/${total}"
        
        if ! download_model "${model}"; then
            failed=$((failed + 1))
        fi
    done
    
    log_info "Download complete: $((total - failed))/${total} successful"
    
    if [ ${failed} -gt 0 ]; then
        log_warn "${failed} models failed to download"
        return 1
    fi
    
    return 0
}

# Package models for transfer
package_models() {
    log_step "Packaging models for air-gapped transfer..."
    
    local package_name="bionemo_models_$(date +%Y%m%d_%H%M%S).tar.gz"
    local package_path="${DOWNLOAD_DIR}/${package_name}"
    
    log_info "Creating archive: ${package_path}"
    
    tar -czf "${package_path}" -C "${DOWNLOAD_DIR}" .
    
    local package_size=$(du -h "${package_path}" | cut -f1)
    log_info "Package created: ${package_path} (${package_size})"
    
    # Generate transfer instructions
    cat > "${DOWNLOAD_DIR}/TRANSFER_INSTRUCTIONS.txt" <<EOF
BioNeMo Models - Air-Gapped Transfer Instructions
==================================================

Package: ${package_name}
Size: ${package_size}
Created: $(date)

Transfer Steps:
---------------

1. Copy package to air-gapped system:
   scp ${package_path} airgapped-system:/tmp/

2. On air-gapped system, extract:
   sudo mkdir -p ${MODELS_BASE_DIR}
   sudo tar -xzf /tmp/${package_name} -C ${MODELS_BASE_DIR}

3. Verify checksums:
   cd ${MODELS_BASE_DIR}
   find . -name "checksums.txt" -exec sh -c 'cd \$(dirname {}) && sha256sum -c checksums.txt' \;

4. Set permissions:
   sudo chown -R \$(whoami):\$(whoami) ${MODELS_BASE_DIR}
   sudo chmod -R 755 ${MODELS_BASE_DIR}

5. Verify installation:
   python -m ml_ops.models.model_downloader --verify

Security Notes:
---------------
- Verify package integrity before transfer
- Use secure transfer methods (SCP, physical media)
- Validate checksums on air-gapped system
- Scan for vulnerabilities before deployment

Support:
--------
For issues, contact: iluminara-core@visendi.ai
EOF
    
    log_info "Transfer instructions: ${DOWNLOAD_DIR}/TRANSFER_INSTRUCTIONS.txt"
    log_info "Package ready for transfer ✓"
}

# Verify models on air-gapped system
verify_models() {
    log_step "Verifying installed models..."
    
    if [ ! -d "${MODELS_BASE_DIR}" ]; then
        log_error "Models directory not found: ${MODELS_BASE_DIR}"
        exit 1
    fi
    
    local verified=0
    local failed=0
    
    # Check each model directory
    for model_dir in "${MODELS_BASE_DIR}"/*; do
        if [ -d "${model_dir}" ]; then
            model_name=$(basename "${model_dir}")
            
            if [ -f "${model_dir}/checksums.txt" ]; then
                log_info "Verifying ${model_name}..."
                
                if (cd "${model_dir}" && sha256sum -c checksums.txt &> /dev/null); then
                    log_info "${model_name} ✓"
                    verified=$((verified + 1))
                else
                    log_error "${model_name} checksum verification failed"
                    failed=$((failed + 1))
                fi
            else
                log_warn "${model_name} has no checksum file"
            fi
        fi
    done
    
    log_info "Verification complete: ${verified} verified, ${failed} failed"
    
    if [ ${failed} -gt 0 ]; then
        return 1
    fi
    
    return 0
}

# List available models
list_models() {
    log_step "Available models in registry:"
    echo ""
    
    cat <<EOF
Protein Structure Prediction:
  - alphafold2    : AlphaFold2 structure prediction
  - esmfold       : ESMFold fast structure prediction

Protein Design:
  - rfdiffusion   : RFdiffusion binder design
  - proteinmpnn   : ProteinMPNN sequence optimization

Molecular Docking:
  - diffdock      : DiffDock molecular docking

Protein Language Models:
  - esm2          : ESM-2 protein embeddings
  - amplify       : AMPLIFY protein language model

Genomics:
  - evo2          : Evo2 DNA foundation model (70B)
  - geneformer    : Geneformer single-cell analysis
  - dnabert       : DNABERT DNA language model

Small Molecules:
  - megamolbart   : MegaMolBART molecular generation
  - moimim        : MoIMIM property prediction

Collections:
  - all           : All models
  - bio_threat    : Bio-threat neutralization pipeline
  - genomic_triage: Genomic triage pipeline
  - drug_discovery: Drug discovery pipeline
EOF
    echo ""
}

# Show usage
usage() {
    cat <<EOF
BioNeMo Model Downloader - Air-Gapped Deployment

Usage: $0 [OPTIONS] COMMAND

Commands:
  download <collection>  Download model collection (all, bio_threat, genomic_triage)
  package               Package downloaded models for transfer
  verify                Verify installed models on air-gapped system
  list                  List available models
  install-ngc           Install NGC CLI

Options:
  -h, --help           Show this help message
  -d, --download-dir   Download directory (default: /tmp/bionemo_downloads)
  -m, --models-dir     Models installation directory (default: /models/bionemo)

Examples:
  # Download all models
  $0 download all

  # Download bio-threat neutralization models
  $0 download bio_threat

  # Package for transfer
  $0 package

  # Verify on air-gapped system
  $0 verify

Environment Variables:
  MODELS_BASE_DIR      Base directory for models
  DOWNLOAD_DIR         Temporary download directory
  NGC_CLI              Path to NGC CLI binary

Air-Gapped Workflow:
  1. On internet-connected system:
     ./model_downloader.sh download all
     ./model_downloader.sh package

  2. Transfer package to air-gapped system

  3. On air-gapped system:
     tar -xzf bionemo_models_*.tar.gz -C /models/bionemo
     ./model_downloader.sh verify
EOF
}

# Main execution
main() {
    if [ $# -eq 0 ]; then
        usage
        exit 0
    fi
    
    # Parse options
    while [[ $# -gt 0 ]]; do
        case $1 in
            -h|--help)
                usage
                exit 0
                ;;
            -d|--download-dir)
                DOWNLOAD_DIR="$2"
                shift 2
                ;;
            -m|--models-dir)
                MODELS_BASE_DIR="$2"
                shift 2
                ;;
            download)
                if [ -z "${2:-}" ]; then
                    log_error "Collection name required"
                    usage
                    exit 1
                fi
                check_prerequisites
                mkdir -p "${DOWNLOAD_DIR}"
                download_collection "$2"
                exit $?
                ;;
            package)
                package_models
                exit $?
                ;;
            verify)
                verify_models
                exit $?
                ;;
            list)
                list_models
                exit 0
                ;;
            install-ngc)
                install_ngc_cli
                exit $?
                ;;
            *)
                log_error "Unknown command: $1"
                usage
                exit 1
                ;;
        esac
    done
}

# Run main
main "$@"
