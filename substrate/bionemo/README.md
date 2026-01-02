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
```bash
./setup.sh
```

### 2. Start BioNeMo Framework Container
```bash
docker-compose -f docker-compose.bionemo.yml up -d
```

### 3. Access Container
```bash
docker exec -it iluminara-bionemo-framework bash
```

### 4. Run Training
```bash
# Inside container
cd /workspace
python -m bionemo.train --config /workspace/configs/fsdp_training.yaml
```

## Training Workflows

### Local Fine-Tuning (FSDP)
Fine-tune foundation models on sovereign genomic data:

```bash
# Geneformer fine-tuning for cell type classification
python -m bionemo.finetune \
  --model geneformer \
  --config configs/finetune_config.yaml \
  --data /data/single_cell_data \
  --output /data/checkpoints/geneformer_finetuned
```

### 5D Parallelism Configuration
For multi-GPU training on Blackwell cluster:

- **Tensor Parallelism**: 4-way (split attention heads)
- **Pipeline Parallelism**: 2-way (split layers)
- **Data Parallelism**: 8-way (FSDP)
- **Sequence Parallelism**: Enabled (long sequences)
- **Expert Parallelism**: 1-way (MoE models)

### FP8 Mixed Precision
Blackwell-optimized training with FP8:

```yaml
precision:
  fp8: true
  fp8_margin: 0
  fp8_interval: 1
```

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
```bash
# Save container image
docker save nvcr.io/nvidia/clara/bionemo-framework:2.0 -o bionemo.tar

# Transfer to air-gapped system
scp bionemo.tar airgapped-system:/tmp/

# Load on air-gapped system
docker load -i /tmp/bionemo.tar
```

## Integration with iLuminara

### Protein Binder Design
```python
from core.research.blueprints.protein_binder import ProteinBinderPipeline

pipeline = ProteinBinderPipeline()
binder = await pipeline.design_neutralizing_binder(
    pathogen_sequence="MKTII...",
    target_epitope="RBD"
)
```

### Genomic Triage
```python
from core.research.blueprints.genomic_triage import GenomicTriagePipeline

pipeline = GenomicTriagePipeline()
triage = await pipeline.analyze_patient_genomics(
    single_cell_data=sc_data,
    clinical_context=context
)
```

## Performance Optimization

### Blackwell-Specific Tuning
- **FP8 Tensor Cores**: Enabled by default
- **Flash Attention**: Memory-efficient attention
- **Tensor Parallelism**: Optimized for NVLink
- **CUDA Graphs**: Reduced kernel launch overhead

### Memory Management
```bash
# Set CUDA memory allocator
export PYTORCH_CUDA_ALLOC_CONF=max_split_size_mb:512

# Enable memory pooling
export CUDA_LAUNCH_BLOCKING=0
```

## Monitoring

### NVML Power Monitoring
```python
import pynvml

pynvml.nvmlInit()
handle = pynvml.nvmlDeviceGetHandleByIndex(0)
power = pynvml.nvmlDeviceGetPowerUsage(handle) / 1000.0  # Watts
```

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
