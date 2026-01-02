#!/bin/bash
# ------------------------------------------------------------------------------
# Copyright (c) 2025 iLuminara (VISENDI56). All Rights Reserved.
# Licensed under the Polyform Shield License 1.0.0.
# 
# BioNeMo Framework Setup Script - Air-Gapped Sovereign Deployment
# Reference: NVIDIA BioNeMo Framework 2.x Documentation
# https://docs.nvidia.com/bionemo/framework/latest/
# ------------------------------------------------------------------------------

set -euo pipefail

# Configuration
BIONEMO_VERSION="${BIONEMO_VERSION:-2.0}"
NGC_REGISTRY="nvcr.io/nvidia/clara"
BIONEMO_IMAGE="${NGC_REGISTRY}/bionemo-framework:${BIONEMO_VERSION}"
LOCAL_DATA_DIR="${LOCAL_DATA_DIR:-/data/bionemo}"
LOCAL_MODELS_DIR="${LOCAL_MODELS_DIR:-/models/bionemo}"
LOCAL_CACHE_DIR="${LOCAL_CACHE_DIR:-/cache/bionemo}"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

log_info() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

log_warn() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check prerequisites
check_prerequisites() {
    log_info "Checking prerequisites..."
    
    # Check Docker
    if ! command -v docker &> /dev/null; then
        log_error "Docker is not installed. Please install Docker first."
        exit 1
    fi
    
    # Check NVIDIA Docker runtime
    if ! docker run --rm --gpus all nvidia/cuda:12.3.0-base-ubuntu22.04 nvidia-smi &> /dev/null; then
        log_error "NVIDIA Docker runtime not available. Please install nvidia-container-toolkit."
        exit 1
    fi
    
    # Check GPU availability
    if ! nvidia-smi &> /dev/null; then
        log_error "No NVIDIA GPU detected. BioNeMo requires NVIDIA GPUs."
        exit 1
    fi
    
    log_info "Prerequisites check passed ✓"
}

# Create local directories
setup_directories() {
    log_info "Setting up local directories..."
    
    mkdir -p "${LOCAL_DATA_DIR}"
    mkdir -p "${LOCAL_MODELS_DIR}"
    mkdir -p "${LOCAL_CACHE_DIR}"
    mkdir -p "${LOCAL_DATA_DIR}/inputs"
    mkdir -p "${LOCAL_DATA_DIR}/outputs"
    mkdir -p "${LOCAL_DATA_DIR}/checkpoints"
    
    log_info "Directories created ✓"
}

# Pull BioNeMo Framework container (air-gapped: manual NGC sync)
pull_bionemo_container() {
    log_info "Pulling BioNeMo Framework container..."
    log_warn "For air-gapped deployment, ensure this image is pre-cached via NGC CLI"
    
    # Check if image exists locally
    if docker images | grep -q "bionemo-framework"; then
        log_info "BioNeMo Framework image already exists locally ✓"
        return 0
    fi
    
    # Attempt to pull (will fail in air-gapped environment)
    if docker pull "${BIONEMO_IMAGE}"; then
        log_info "BioNeMo Framework image pulled successfully ✓"
    else
        log_warn "Failed to pull image. For air-gapped deployment:"
        log_warn "1. On internet-connected machine: docker pull ${BIONEMO_IMAGE}"
        log_warn "2. Save image: docker save ${BIONEMO_IMAGE} -o bionemo-framework.tar"
        log_warn "3. Transfer to air-gapped system"
        log_warn "4. Load image: docker load -i bionemo-framework.tar"
    fi
}

# Configure container runtime settings
configure_runtime() {
    log_info "Configuring container runtime settings..."
    
    # Create docker-compose override for BioNeMo
    cat > docker-compose.bionemo.yml <<EOF
version: '3.8'

services:
  bionemo-framework:
    image: ${BIONEMO_IMAGE}
    container_name: iluminara-bionemo-framework
    runtime: nvidia
    ipc: host
    ulimits:
      memlock: -1
      stack: 67108864
    environment:
      - NVIDIA_VISIBLE_DEVICES=all
      - CUDA_VISIBLE_DEVICES=0,1,2,3,4,5,6,7
      - NCCL_DEBUG=INFO
      - NCCL_IB_DISABLE=0
      - NCCL_NET_GDR_LEVEL=5
      - PYTORCH_CUDA_ALLOC_CONF=max_split_size_mb:512
      - BIONEMO_HOME=/workspace/bionemo
    volumes:
      - ${LOCAL_DATA_DIR}:/data
      - ${LOCAL_MODELS_DIR}:/models
      - ${LOCAL_CACHE_DIR}:/cache
      - ./configs:/workspace/configs
      - ../core/research:/workspace/research
    shm_size: '32gb'
    deploy:
      resources:
        reservations:
          devices:
            - driver: nvidia
              count: all
              capabilities: [gpu]
    command: /bin/bash -c "tail -f /dev/null"
    networks:
      - iluminara-net

networks:
  iluminara-net:
    external: true
EOF
    
    log_info "Runtime configuration created ✓"
}

# Download pretrained models (air-gapped: manual sync)
download_models() {
    log_info "Setting up model registry..."
    log_warn "For air-gapped deployment, models must be manually synced from NGC"
    
    cat > "${LOCAL_MODELS_DIR}/README.md" <<EOF
# BioNeMo Model Registry - Air-Gapped Deployment

## Required Models for iLuminara Sovereign Arsenal

### Protein Structure Prediction
- **AlphaFold2**: \`nvcr.io/nvidia/clara/alphafold2:latest\`
- **ESMFold**: \`nvcr.io/nvidia/clara/esmfold:latest\`

### Protein Design
- **RFdiffusion**: \`nvcr.io/nvidia/clara/rfdiffusion:latest\`
- **ProteinMPNN**: \`nvcr.io/nvidia/clara/proteinmpnn:latest\`

### Molecular Docking
- **DiffDock**: \`nvcr.io/nvidia/clara/diffdock:latest\`

### Genomics
- **Evo2**: BioNeMo Framework pretrained (70B parameters)
- **Geneformer**: BioNeMo Framework pretrained
- **DNABERT**: BioNeMo Framework pretrained

### Small Molecules
- **MegaMolBART**: BioNeMo Framework pretrained
- **MoIMIM**: BioNeMo Framework pretrained

## Air-Gapped Sync Instructions

1. **On Internet-Connected System:**
   \`\`\`bash
   # Login to NGC
   ngc config set
   
   # Download models
   ngc registry model download-version nvidia/clara/alphafold2:latest
   ngc registry model download-version nvidia/clara/esmfold:latest
   # ... repeat for all models
   \`\`\`

2. **Transfer to Air-Gapped System:**
   \`\`\`bash
   rsync -avz --progress models/ airgapped-system:/models/bionemo/
   \`\`\`

3. **Verify Models:**
   \`\`\`bash
   ls -lh /models/bionemo/
   \`\`\`

## Model Paths
All models should be placed in: \`${LOCAL_MODELS_DIR}/\`

Directory structure:
\`\`\`
/models/bionemo/
├── alphafold2/
├── esmfold/
├── rfdiffusion/
├── proteinmpnn/
├── diffdock/
├── evo2/
├── geneformer/
├── dnabert/
├── megamolbart/
└── moimim/
\`\`\`
EOF
    
    log_info "Model registry documentation created ✓"
}

# Create training configuration templates
create_training_configs() {
    log_info "Creating training configuration templates..."
    
    mkdir -p configs
    
    # FSDP training config
    cat > configs/fsdp_training.yaml <<EOF
# BioNeMo Framework FSDP Training Configuration
# Reference: https://docs.nvidia.com/bionemo/framework/latest/training.html

training:
  # 5D Parallelism Configuration
  parallelism:
    tensor_model_parallel_size: 4
    pipeline_model_parallel_size: 2
    data_parallel_size: 8
    sequence_parallel: true
    expert_model_parallel_size: 1
  
  # FSDP Configuration
  fsdp:
    enabled: true
    sharding_strategy: "FULL_SHARD"  # FULL_SHARD, SHARD_GRAD_OP, NO_SHARD
    cpu_offload: false
    backward_prefetch: "BACKWARD_PRE"
    forward_prefetch: true
    limit_all_gathers: true
  
  # Mixed Precision (FP8 on Blackwell)
  precision:
    fp8: true
    fp8_margin: 0
    fp8_interval: 1
    fp8_amax_history_len: 1024
    fp8_amax_compute_algo: "max"
  
  # Optimization
  optimizer:
    type: "adamw"
    lr: 1.0e-4
    weight_decay: 0.01
    betas: [0.9, 0.999]
    eps: 1.0e-8
  
  # Learning Rate Schedule
  lr_scheduler:
    type: "cosine"
    warmup_steps: 1000
    total_steps: 100000
    min_lr: 1.0e-6
  
  # Checkpointing
  checkpoint:
    save_interval: 1000
    save_top_k: 3
    monitor: "val_loss"
    mode: "min"
  
  # Logging
  logging:
    log_interval: 10
    val_check_interval: 500
    tensorboard: true
    wandb: false  # Disabled for air-gapped

# Data Configuration
data:
  train_path: "/data/train"
  val_path: "/data/val"
  batch_size: 32
  num_workers: 8
  prefetch_factor: 2
  pin_memory: true

# Model Configuration
model:
  architecture: "esm2"
  num_layers: 33
  hidden_size: 1280
  num_attention_heads: 20
  intermediate_size: 5120
  max_position_embeddings: 1024
  vocab_size: 33

# Blackwell Optimization
blackwell:
  fp8_compute: true
  tensor_cores: true
  flash_attention: true
  memory_efficient_attention: true
EOF
    
    # Fine-tuning config
    cat > configs/finetune_config.yaml <<EOF
# BioNeMo Fine-Tuning Configuration for Sovereign Genomics

finetuning:
  # Base Model
  base_model: "evo2-70b"
  base_model_path: "/models/bionemo/evo2"
  
  # LoRA Configuration (Parameter-Efficient Fine-Tuning)
  lora:
    enabled: true
    rank: 16
    alpha: 32
    dropout: 0.1
    target_modules: ["q_proj", "v_proj", "k_proj", "o_proj"]
  
  # Task-Specific Configuration
  task:
    type: "genomic_triage"
    num_classes: 10
    task_head: "classification"
  
  # Training
  training:
    epochs: 10
    batch_size: 16
    gradient_accumulation_steps: 4
    max_grad_norm: 1.0
    early_stopping_patience: 3
  
  # Data Augmentation
  augmentation:
    enabled: true
    techniques:
      - "reverse_complement"
      - "random_mutation"
      - "sequence_masking"
    augmentation_prob: 0.3

# Evaluation
evaluation:
  metrics:
    - "accuracy"
    - "f1_score"
    - "auroc"
    - "precision"
    - "recall"
  test_path: "/data/test"
EOF
    
    log_info "Training configurations created ✓"
}

# Create README with instructions
create_readme() {
    log_info "Creating README documentation..."
    
    cat > README.md <<EOF
# BioNeMo Framework Integration - iLuminara Sovereign Health OS

## Overview
This directory contains the NVIDIA BioNeMo Framework integration for sovereign generative biology capabilities, optimized for Blackwell B300 GPUs with air-gapped deployment.

## Architecture
- **Framework**: NVIDIA BioNeMo Framework 2.x
- **Compute**: Blackwell B300 (FP8, 5D Parallelism)
- **Deployment**: Air-gapped, local-only execution
- **Models**: ESM-2, Evo2, Geneformer, AlphaFold2, RFdiffusion, ProteinMPNN

## Quick Start

### 1. Setup Environment
\`\`\`bash
./setup.sh
\`\`\`

### 2. Start BioNeMo Framework Container
\`\`\`bash
docker-compose -f docker-compose.bionemo.yml up -d
\`\`\`

### 3. Access Container
\`\`\`bash
docker exec -it iluminara-bionemo-framework bash
\`\`\`

### 4. Run Training
\`\`\`bash
# Inside container
cd /workspace
python -m bionemo.train --config /workspace/configs/fsdp_training.yaml
\`\`\`

## Training Workflows

### Local Fine-Tuning (FSDP)
Fine-tune foundation models on sovereign genomic data:

\`\`\`bash
# Geneformer fine-tuning for cell type classification
python -m bionemo.finetune \\
  --model geneformer \\
  --config configs/finetune_config.yaml \\
  --data /data/single_cell_data \\
  --output /data/checkpoints/geneformer_finetuned
\`\`\`

### 5D Parallelism Configuration
For multi-GPU training on Blackwell cluster:

- **Tensor Parallelism**: 4-way (split attention heads)
- **Pipeline Parallelism**: 2-way (split layers)
- **Data Parallelism**: 8-way (FSDP)
- **Sequence Parallelism**: Enabled (long sequences)
- **Expert Parallelism**: 1-way (MoE models)

### FP8 Mixed Precision
Blackwell-optimized training with FP8:

\`\`\`yaml
precision:
  fp8: true
  fp8_margin: 0
  fp8_interval: 1
\`\`\`

Benefits:
- 2x memory reduction
- 2-3x throughput increase
- Maintained accuracy with proper scaling

## Air-Gapped Deployment

### Model Synchronization
1. **Internet-connected system**: Download models from NGC
2. **Transfer**: Use secure file transfer to air-gapped system
3. **Verify**: Check model integrity with checksums

### Container Management
\`\`\`bash
# Save container image
docker save nvcr.io/nvidia/clara/bionemo-framework:2.0 -o bionemo.tar

# Transfer to air-gapped system
scp bionemo.tar airgapped-system:/tmp/

# Load on air-gapped system
docker load -i /tmp/bionemo.tar
\`\`\`

## Integration with iLuminara

### Protein Binder Design
\`\`\`python
from core.research.blueprints.protein_binder import ProteinBinderPipeline

pipeline = ProteinBinderPipeline()
binder = await pipeline.design_neutralizing_binder(
    pathogen_sequence="MKTII...",
    target_epitope="RBD"
)
\`\`\`

### Genomic Triage
\`\`\`python
from core.research.blueprints.genomic_triage import GenomicTriagePipeline

pipeline = GenomicTriagePipeline()
triage = await pipeline.analyze_patient_genomics(
    single_cell_data=sc_data,
    clinical_context=context
)
\`\`\`

## Performance Optimization

### Blackwell-Specific Tuning
- **FP8 Tensor Cores**: Enabled by default
- **Flash Attention**: Memory-efficient attention
- **Tensor Parallelism**: Optimized for NVLink
- **CUDA Graphs**: Reduced kernel launch overhead

### Memory Management
\`\`\`bash
# Set CUDA memory allocator
export PYTORCH_CUDA_ALLOC_CONF=max_split_size_mb:512

# Enable memory pooling
export CUDA_LAUNCH_BLOCKING=0
\`\`\`

## Monitoring

### NVML Power Monitoring
\`\`\`python
import pynvml

pynvml.nvmlInit()
handle = pynvml.nvmlDeviceGetHandleByIndex(0)
power = pynvml.nvmlDeviceGetPowerUsage(handle) / 1000.0  # Watts
\`\`\`

### Training Metrics
- Loss curves: TensorBoard at http://localhost:6006
- GPU utilization: nvidia-smi dmon
- Memory usage: nvidia-smi --query-gpu=memory.used --format=csv

## Troubleshooting

### Out of Memory (OOM)
1. Reduce batch size
2. Enable gradient checkpointing
3. Increase pipeline parallelism
4. Enable CPU offloading

### Slow Training
1. Verify FP8 is enabled
2. Check NCCL configuration
3. Enable Flash Attention
4. Optimize data loading (increase num_workers)

### Model Loading Errors
1. Verify model paths in configs
2. Check NGC credentials (if not air-gapped)
3. Validate model checksums

## References
- [BioNeMo Framework Documentation](https://docs.nvidia.com/bionemo/framework/latest/)
- [NVIDIA NGC Catalog](https://catalog.ngc.nvidia.com/)
- [Blackwell Architecture Guide](https://www.nvidia.com/en-us/data-center/technologies/blackwell-architecture/)
- [FSDP Training Guide](https://pytorch.org/tutorials/intermediate/FSDP_tutorial.html)

## Support
For sovereign deployment support, contact: iluminara-core@visendi.ai

---
**Security Notice**: This system operates in air-gapped mode. No external API calls are made during inference or training.
EOF
    
    log_info "README created ✓"
}

# Create requirements file
create_requirements() {
    log_info "Creating requirements file..."
    
    cat > requirements-bionemo.txt <<EOF
# BioNeMo Framework Dependencies
# Note: Most dependencies are included in the NGC container
# These are additional packages for iLuminara integration

# Core ML/DL (versions compatible with BioNeMo 2.x)
torch>=2.1.0
nvidia-cuda-runtime-cu12>=12.3.0
nvidia-cudnn-cu12>=8.9.0
nvidia-nccl-cu12>=2.19.0

# BioNeMo-specific (installed in container)
# bionemo-framework>=2.0.0  # Included in NGC container

# Protein/Genomics Libraries
biopython>=1.81
biotite>=0.38.0
prody>=2.4.0

# Molecular Visualization (optional, for debugging)
py3Dmol>=2.0.0
nglview>=3.0.0

# Scientific Computing
numpy>=1.24.0
scipy>=1.11.0
pandas>=2.0.0
scikit-learn>=1.3.0

# Monitoring
pynvml>=11.5.0
psutil>=5.9.0

# Logging
structlog>=23.1.0
python-json-logger>=2.0.0

# API Integration (for NIM endpoints)
requests>=2.31.0
httpx>=0.25.0
aiohttp>=3.9.0

# Configuration
pyyaml>=6.0
omegaconf>=2.3.0

# Testing
pytest>=7.4.0
pytest-asyncio>=0.21.0
pytest-mock>=3.11.0

# Type Checking
mypy>=1.5.0
types-requests>=2.31.0
types-PyYAML>=6.0.0
EOF
    
    log_info "Requirements file created ✓"
}

# Main execution
main() {
    log_info "Starting BioNeMo Framework setup for iLuminara..."
    
    check_prerequisites
    setup_directories
    pull_bionemo_container
    configure_runtime
    download_models
    create_training_configs
    create_readme
    create_requirements
    
    log_info "========================================="
    log_info "BioNeMo Framework setup complete! ✓"
    log_info "========================================="
    log_info ""
    log_info "Next steps:"
    log_info "1. Review README.md for detailed instructions"
    log_info "2. Sync models from NGC (see ${LOCAL_MODELS_DIR}/README.md)"
    log_info "3. Start framework: docker-compose -f docker-compose.bionemo.yml up -d"
    log_info "4. Run training: docker exec -it iluminara-bionemo-framework bash"
    log_info ""
    log_info "For air-gapped deployment, ensure all models are pre-cached."
}

# Run main function
main "$@"
