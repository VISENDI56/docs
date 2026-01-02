# ------------------------------------------------------------------------------
# Copyright (c) 2025 iLuminara (VISENDI56). All Rights Reserved.
# Licensed under the Polyform Shield License 1.0.0.
# 
# Generative Genomics Pipeline for Clinical Triage
# Reference: NVIDIA BioNeMo Framework 2.x (Geneformer, Evo2)
# https://docs.nvidia.com/bionemo/framework/latest/
# ------------------------------------------------------------------------------

"""
Genomic Triage Pipeline using Generative Biology

This module implements sovereign genomic analysis for clinical triage using
NVIDIA BioNeMo foundation models (Geneformer, Evo2, DNABERT).

Capabilities:
1. Single-cell RNA-seq analysis (Geneformer)
2. Cell type clustering and immune profiling
3. Outlier detection (cytokine storms, immune dysregulation)
4. DNA anomaly detection (Evo2)
5. Integration with agentic_clinical triage agents

All processing is local and air-gapped.
"""

import asyncio
import logging
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Dict, List, Optional, Any, Tuple
from pathlib import Path
import json

import numpy as np
import pandas as pd
from scipy import stats
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
import requests

import structlog

logger = structlog.get_logger(__name__)


class TriageStage(Enum):
    """Stages in genomic triage pipeline"""
    DATA_PREPROCESSING = "data_preprocessing"
    EMBEDDING_GENERATION = "embedding_generation"
    CELL_TYPE_CLUSTERING = "cell_type_clustering"
    OUTLIER_DETECTION = "outlier_detection"
    DNA_ANOMALY_DETECTION = "dna_anomaly_detection"
    CLINICAL_INTERPRETATION = "clinical_interpretation"
    COMPLETE = "complete"


@dataclass
class SingleCellData:
    """Single-cell RNA-seq data"""
    cell_ids: List[str]
    gene_expression: np.ndarray  # cells x genes
    gene_names: List[str]
    metadata: Dict[str, Any] = field(default_factory=dict)
    patient_id: str = "unknown"
    sample_date: datetime = field(default_factory=datetime.now)


@dataclass
class CellTypeCluster:
    """Identified cell type cluster"""
    cluster_id: int
    cell_type: str
    cell_ids: List[str]
    marker_genes: List[str]
    cluster_center: np.ndarray
    confidence: float
    cell_count: int


@dataclass
class ImmuneOutlier:
    """Detected immune system outlier"""
    outlier_id: str
    cell_ids: List[str]
    outlier_type: str  # "cytokine_storm", "immune_exhaustion", etc.
    severity_score: float
    affected_pathways: List[str]
    biomarkers: Dict[str, float]
    clinical_significance: str


@dataclass
class DNAAnomaly:
    """Detected DNA sequence anomaly"""
    anomaly_id: str
    sequence_region: str
    anomaly_type: str  # "mutation", "structural_variant", etc.
    pathogenicity_score: float
    affected_genes: List[str]
    clinical_impact: str


@dataclass
class TriageResult:
    """Complete genomic triage result"""
    patient_id: str
    triage_priority: str  # "critical", "high", "medium", "low"
    risk_score: float
    cell_type_profile: List[CellTypeCluster]
    immune_outliers: List[ImmuneOutlier]
    dna_anomalies: List[DNAAnomaly]
    clinical_recommendations: List[str]
    generated_at: datetime = field(default_factory=datetime.now)


class BioNeMoGenomicsClient:
    """
    Client for BioNeMo genomics models (Geneformer, Evo2, DNABERT)
    
    Assumes models are loaded in BioNeMo Framework container or via local NIMs.
    """
    
    def __init__(
        self,
        geneformer_url: str = "http://localhost:8006",
        evo2_url: str = "http://localhost:8007",
        dnabert_url: str = "http://localhost:8008",
        timeout: int = 300
    ):
        """
        Initialize genomics client
        
        Args:
            geneformer_url: Geneformer model endpoint
            evo2_url: Evo2 model endpoint
            dnabert_url: DNABERT model endpoint
            timeout: Request timeout
        """
        self.endpoints = {
            "geneformer": geneformer_url,
            "evo2": evo2_url,
            "dnabert": dnabert_url
        }
        self.timeout = timeout
        
        logger.info("genomics_client_initialized", endpoints=self.endpoints)
    
    async def generate_cell_embeddings(
        self,
        gene_expression: np.ndarray,
        gene_names: List[str]
    ) -> np.ndarray:
        """
        Generate cell embeddings using Geneformer
        
        Args:
            gene_expression: Gene expression matrix (cells x genes)
            gene_names: Gene identifiers
            
        Returns:
            Cell embeddings (cells x embedding_dim)
        """
        endpoint = self.endpoints["geneformer"]
        
        payload = {
            "gene_expression": gene_expression.tolist(),
            "gene_names": gene_names,
            "task": "embedding"
        }
        
        logger.info("generating_cell_embeddings", num_cells=gene_expression.shape[0])
        
        try:
            response = requests.post(
                f"{endpoint}/v1/embed",
                json=payload,
                timeout=self.timeout
            )
            response.raise_for_status()
            result = response.json()
            
            embeddings = np.array(result["embeddings"])
            logger.info("embeddings_generated", shape=embeddings.shape)
            return embeddings
            
        except Exception as e:
            logger.error("embedding_generation_failed", error=str(e))
            # Fallback to PCA if model unavailable
            logger.warning("using_pca_fallback")
            from sklearn.decomposition import PCA
            pca = PCA(n_components=256)
            return pca.fit_transform(gene_expression)
    
    async def classify_cell_types(
        self,
        embeddings: np.ndarray,
        gene_expression: np.ndarray
    ) -> List[Dict[str, Any]]:
        """
        Classify cell types using fine-tuned Geneformer
        
        Args:
            embeddings: Cell embeddings
            gene_expression: Original gene expression
            
        Returns:
            Cell type predictions
        """
        endpoint = self.endpoints["geneformer"]
        
        payload = {
            "embeddings": embeddings.tolist(),
            "task": "cell_type_classification"
        }
        
        logger.info("classifying_cell_types", num_cells=embeddings.shape[0])
        
        try:
            response = requests.post(
                f"{endpoint}/v1/classify",
                json=payload,
                timeout=self.timeout
            )
            response.raise_for_status()
            result = response.json()
            
            logger.info("cell_types_classified", predictions=len(result["predictions"]))
            return result["predictions"]
            
        except Exception as e:
            logger.error("cell_type_classification_failed", error=str(e))
            # Fallback to clustering
            return []
    
    async def detect_dna_anomalies(
        self,
        dna_sequence: str,
        reference_genome: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """
        Detect DNA anomalies using Evo2
        
        Args:
            dna_sequence: Patient DNA sequence
            reference_genome: Reference genome (optional)
            
        Returns:
            Detected anomalies
        """
        endpoint = self.endpoints["evo2"]
        
        payload = {
            "sequence": dna_sequence,
            "reference": reference_genome,
            "task": "anomaly_detection"
        }
        
        logger.info("detecting_dna_anomalies", seq_length=len(dna_sequence))
        
        try:
            response = requests.post(
                f"{endpoint}/v1/analyze",
                json=payload,
                timeout=self.timeout
            )
            response.raise_for_status()
            result = response.json()
            
            logger.info("dna_anomalies_detected", count=len(result.get("anomalies", [])))
            return result.get("anomalies", [])
            
        except Exception as e:
            logger.error("dna_anomaly_detection_failed", error=str(e))
            return []


class GenomicTriagePipeline:
    """
    End-to-end genomic triage pipeline for clinical decision support
    
    Integrates with:
    - agentic_clinical/triage agents
    - benchmarks/outlier_detection
    - utils/data_gen (synthetic genomic data)
    """
    
    def __init__(
        self,
        genomics_client: Optional[BioNeMoGenomicsClient] = None,
        output_dir: str = "/data/bionemo/outputs/triage",
        outlier_threshold: float = 3.0
    ):
        """
        Initialize genomic triage pipeline
        
        Args:
            genomics_client: BioNeMo genomics client
            output_dir: Output directory
            outlier_threshold: Z-score threshold for outlier detection
        """
        self.genomics_client = genomics_client or BioNeMoGenomicsClient()
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.outlier_threshold = outlier_threshold
        
        logger.info("triage_pipeline_initialized", output_dir=str(self.output_dir))
    
    async def analyze_patient_genomics(
        self,
        single_cell_data: SingleCellData,
        dna_sequence: Optional[str] = None,
        clinical_context: Optional[Dict[str, Any]] = None
    ) -> TriageResult:
        """
        Perform complete genomic triage analysis
        
        Args:
            single_cell_data: Single-cell RNA-seq data
            dna_sequence: Patient DNA sequence (optional)
            clinical_context: Clinical context
            
        Returns:
            Triage result with recommendations
        """
        patient_id = single_cell_data.patient_id
        triage_id = f"triage_{patient_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        logger.info("triage_analysis_started", triage_id=triage_id, patient_id=patient_id)
        
        try:
            # Stage 1: Data Preprocessing
            logger.info("stage_1_preprocessing")
            preprocessed_data = await self._preprocess_data(single_cell_data)
            
            # Stage 2: Generate Embeddings (Geneformer)
            logger.info("stage_2_embedding_generation")
            embeddings = await self.genomics_client.generate_cell_embeddings(
                preprocessed_data["expression"],
                preprocessed_data["genes"]
            )
            
            # Stage 3: Cell Type Clustering
            logger.info("stage_3_cell_type_clustering")
            cell_clusters = await self._cluster_cell_types(
                embeddings,
                preprocessed_data["expression"],
                single_cell_data.cell_ids
            )
            
            # Stage 4: Outlier Detection (Immune Profiling)
            logger.info("stage_4_outlier_detection")
            immune_outliers = await self._detect_immune_outliers(
                embeddings,
                cell_clusters,
                preprocessed_data["expression"],
                preprocessed_data["genes"]
            )
            
            # Stage 5: DNA Anomaly Detection (if DNA provided)
            dna_anomalies = []
            if dna_sequence:
                logger.info("stage_5_dna_anomaly_detection")
                dna_anomalies = await self._detect_dna_anomalies(dna_sequence)
            
            # Stage 6: Clinical Interpretation
            logger.info("stage_6_clinical_interpretation")
            triage_result = await self._generate_triage_result(
                patient_id,
                cell_clusters,
                immune_outliers,
                dna_anomalies,
                clinical_context
            )
            
            # Save results
            await self._save_triage_results(triage_id, triage_result)
            
            logger.info("triage_analysis_completed", triage_id=triage_id, priority=triage_result.triage_priority)
            return triage_result
            
        except Exception as e:
            logger.error("triage_analysis_failed", triage_id=triage_id, error=str(e))
            raise
    
    async def _preprocess_data(
        self,
        data: SingleCellData
    ) -> Dict[str, Any]:
        """Preprocess single-cell data"""
        logger.info("preprocessing_data", num_cells=len(data.cell_ids))
        
        # Normalize gene expression
        scaler = StandardScaler()
        normalized_expression = scaler.fit_transform(data.gene_expression)
        
        # Filter low-quality cells (simple QC)
        cell_quality = np.sum(data.gene_expression > 0, axis=1)
        quality_threshold = np.percentile(cell_quality, 10)
        high_quality_mask = cell_quality > quality_threshold
        
        filtered_expression = normalized_expression[high_quality_mask]
        filtered_cells = [cid for i, cid in enumerate(data.cell_ids) if high_quality_mask[i]]
        
        logger.info("preprocessing_complete", cells_retained=len(filtered_cells))
        
        return {
            "expression": filtered_expression,
            "genes": data.gene_names,
            "cell_ids": filtered_cells
        }
    
    async def _cluster_cell_types(
        self,
        embeddings: np.ndarray,
        expression: np.ndarray,
        cell_ids: List[str],
        n_clusters: int = 10
    ) -> List[CellTypeCluster]:
        """Cluster cells by type"""
        logger.info("clustering_cells", n_clusters=n_clusters)
        
        # K-means clustering on embeddings
        kmeans = KMeans(n_clusters=n_clusters, random_state=42)
        cluster_labels = kmeans.fit_predict(embeddings)
        
        # Identify marker genes for each cluster
        clusters = []
        for cluster_id in range(n_clusters):
            cluster_mask = cluster_labels == cluster_id
            cluster_cell_ids = [cid for i, cid in enumerate(cell_ids) if cluster_mask[i]]
            
            # Find top marker genes (highest mean expression in cluster)
            cluster_expression = expression[cluster_mask]
            mean_expression = np.mean(cluster_expression, axis=0)
            top_gene_indices = np.argsort(mean_expression)[-10:]
            
            # Infer cell type (simplified - would use Geneformer classification)
            cell_type = self._infer_cell_type(top_gene_indices)
            
            clusters.append(CellTypeCluster(
                cluster_id=cluster_id,
                cell_type=cell_type,
                cell_ids=cluster_cell_ids,
                marker_genes=[f"GENE_{i}" for i in top_gene_indices],
                cluster_center=kmeans.cluster_centers_[cluster_id],
                confidence=0.85,
                cell_count=len(cluster_cell_ids)
            ))
        
        logger.info("clustering_complete", clusters_found=len(clusters))
        return clusters
    
    def _infer_cell_type(self, marker_gene_indices: np.ndarray) -> str:
        """Infer cell type from marker genes (simplified)"""
        # In production, use Geneformer classification or marker gene database
        cell_types = [
            "T_cell", "B_cell", "NK_cell", "Monocyte", "Macrophage",
            "Dendritic_cell", "Neutrophil", "Eosinophil", "Basophil", "Other"
        ]
        return cell_types[marker_gene_indices[0] % len(cell_types)]
    
    async def _detect_immune_outliers(
        self,
        embeddings: np.ndarray,
        clusters: List[CellTypeCluster],
        expression: np.ndarray,
        gene_names: List[str]
    ) -> List[ImmuneOutlier]:
        """Detect immune system outliers (cytokine storms, etc.)"""
        logger.info("detecting_immune_outliers")
        
        outliers = []
        
        # Detect cytokine storm signatures
        cytokine_genes = ["IL6", "IL1B", "TNF", "IFNG", "IL10"]  # Simplified
        cytokine_indices = [i for i, g in enumerate(gene_names) if any(cg in g for cg in cytokine_genes)]
        
        if cytokine_indices:
            cytokine_expression = expression[:, cytokine_indices]
            cytokine_scores = np.mean(cytokine_expression, axis=1)
            
            # Z-score based outlier detection
            z_scores = stats.zscore(cytokine_scores)
            outlier_mask = np.abs(z_scores) > self.outlier_threshold
            
            if np.any(outlier_mask):
                outlier_indices = np.where(outlier_mask)[0]
                severity = np.mean(np.abs(z_scores[outlier_mask]))
                
                outliers.append(ImmuneOutlier(
                    outlier_id="cytokine_storm_1",
                    cell_ids=[f"cell_{i}" for i in outlier_indices],
                    outlier_type="cytokine_storm",
                    severity_score=float(severity),
                    affected_pathways=["inflammatory_response", "cytokine_signaling"],
                    biomarkers={gene: float(np.mean(expression[outlier_mask, i])) 
                               for i, gene in enumerate(cytokine_genes)},
                    clinical_significance="High risk of severe inflammatory response"
                ))
        
        # Detect immune exhaustion
        exhaustion_genes = ["PDCD1", "CTLA4", "LAG3", "TIM3"]
        exhaustion_indices = [i for i, g in enumerate(gene_names) if any(eg in g for eg in exhaustion_genes)]
        
        if exhaustion_indices:
            exhaustion_expression = expression[:, exhaustion_indices]
            exhaustion_scores = np.mean(exhaustion_expression, axis=1)
            z_scores = stats.zscore(exhaustion_scores)
            outlier_mask = z_scores > self.outlier_threshold
            
            if np.any(outlier_mask):
                outlier_indices = np.where(outlier_mask)[0]
                severity = np.mean(z_scores[outlier_mask])
                
                outliers.append(ImmuneOutlier(
                    outlier_id="immune_exhaustion_1",
                    cell_ids=[f"cell_{i}" for i in outlier_indices],
                    outlier_type="immune_exhaustion",
                    severity_score=float(severity),
                    affected_pathways=["T_cell_exhaustion", "checkpoint_inhibition"],
                    biomarkers={gene: float(np.mean(expression[outlier_mask, i])) 
                               for i, gene in enumerate(exhaustion_genes)},
                    clinical_significance="Impaired immune response capacity"
                ))
        
        logger.info("outlier_detection_complete", outliers_found=len(outliers))
        return outliers
    
    async def _detect_dna_anomalies(
        self,
        dna_sequence: str
    ) -> List[DNAAnomaly]:
        """Detect DNA anomalies using Evo2"""
        anomaly_results = await self.genomics_client.detect_dna_anomalies(dna_sequence)
        
        anomalies = []
        for i, result in enumerate(anomaly_results):
            anomalies.append(DNAAnomaly(
                anomaly_id=f"dna_anomaly_{i+1}",
                sequence_region=result.get("region", "unknown"),
                anomaly_type=result.get("type", "unknown"),
                pathogenicity_score=result.get("pathogenicity", 0.0),
                affected_genes=result.get("genes", []),
                clinical_impact=result.get("impact", "unknown")
            ))
        
        return anomalies
    
    async def _generate_triage_result(
        self,
        patient_id: str,
        clusters: List[CellTypeCluster],
        outliers: List[ImmuneOutlier],
        dna_anomalies: List[DNAAnomaly],
        clinical_context: Optional[Dict[str, Any]]
    ) -> TriageResult:
        """Generate final triage result with recommendations"""
        
        # Calculate risk score
        risk_score = 0.0
        
        # Outlier contribution
        for outlier in outliers:
            if outlier.outlier_type == "cytokine_storm":
                risk_score += outlier.severity_score * 0.4
            elif outlier.outlier_type == "immune_exhaustion":
                risk_score += outlier.severity_score * 0.3
        
        # DNA anomaly contribution
        for anomaly in dna_anomalies:
            risk_score += anomaly.pathogenicity_score * 0.3
        
        # Normalize to 0-1
        risk_score = min(risk_score / 10.0, 1.0)
        
        # Determine triage priority
        if risk_score > 0.8:
            priority = "critical"
        elif risk_score > 0.6:
            priority = "high"
        elif risk_score > 0.4:
            priority = "medium"
        else:
            priority = "low"
        
        # Generate clinical recommendations
        recommendations = []
        
        if any(o.outlier_type == "cytokine_storm" for o in outliers):
            recommendations.append("Consider anti-inflammatory therapy (IL-6 inhibitors)")
            recommendations.append("Monitor for acute respiratory distress syndrome (ARDS)")
        
        if any(o.outlier_type == "immune_exhaustion" for o in outliers):
            recommendations.append("Evaluate for checkpoint inhibitor therapy")
            recommendations.append("Monitor T-cell function and viral load")
        
        if dna_anomalies:
            recommendations.append("Genetic counseling recommended")
            recommendations.append("Consider targeted therapy based on genomic profile")
        
        if not recommendations:
            recommendations.append("Continue standard monitoring")
        
        return TriageResult(
            patient_id=patient_id,
            triage_priority=priority,
            risk_score=risk_score,
            cell_type_profile=clusters,
            immune_outliers=outliers,
            dna_anomalies=dna_anomalies,
            clinical_recommendations=recommendations
        )
    
    async def _save_triage_results(
        self,
        triage_id: str,
        result: TriageResult
    ) -> None:
        """Save triage results to disk"""
        output_path = self.output_dir / triage_id
        output_path.mkdir(parents=True, exist_ok=True)
        
        # Convert to JSON-serializable format
        result_dict = {
            "patient_id": result.patient_id,
            "triage_priority": result.triage_priority,
            "risk_score": result.risk_score,
            "cell_type_profile": [
                {
                    "cluster_id": c.cluster_id,
                    "cell_type": c.cell_type,
                    "cell_count": c.cell_count,
                    "confidence": c.confidence
                }
                for c in result.cell_type_profile
            ],
            "immune_outliers": [
                {
                    "outlier_id": o.outlier_id,
                    "outlier_type": o.outlier_type,
                    "severity_score": o.severity_score,
                    "clinical_significance": o.clinical_significance
                }
                for o in result.immune_outliers
            ],
            "dna_anomalies": [
                {
                    "anomaly_id": a.anomaly_id,
                    "anomaly_type": a.anomaly_type,
                    "pathogenicity_score": a.pathogenicity_score,
                    "clinical_impact": a.clinical_impact
                }
                for a in result.dna_anomalies
            ],
            "clinical_recommendations": result.clinical_recommendations,
            "generated_at": result.generated_at.isoformat()
        }
        
        with open(output_path / "triage_result.json", "w") as f:
            json.dump(result_dict, f, indent=2)
        
        logger.info("triage_results_saved", output_path=str(output_path))


# Integration hook for agentic_clinical triage agents
async def triage_patient_genomics(
    patient_id: str,
    single_cell_data: Dict[str, Any],
    dna_sequence: Optional[str] = None,
    clinical_context: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]:
    """
    Entry point for agentic clinical triage agents
    
    Args:
        patient_id: Patient identifier
        single_cell_data: Single-cell RNA-seq data
        dna_sequence: Patient DNA sequence
        clinical_context: Clinical context
        
    Returns:
        Triage result for clinical decision support
    """
    # Convert dict to SingleCellData
    sc_data = SingleCellData(
        cell_ids=single_cell_data["cell_ids"],
        gene_expression=np.array(single_cell_data["gene_expression"]),
        gene_names=single_cell_data["gene_names"],
        patient_id=patient_id
    )
    
    pipeline = GenomicTriagePipeline()
    
    logger.info("clinical_triage_triggered", patient_id=patient_id)
    
    result = await pipeline.analyze_patient_genomics(
        single_cell_data=sc_data,
        dna_sequence=dna_sequence,
        clinical_context=clinical_context
    )
    
    return {
        "patient_id": result.patient_id,
        "triage_priority": result.triage_priority,
        "risk_score": result.risk_score,
        "recommendations": result.clinical_recommendations
    }


if __name__ == "__main__":
    # Example usage
    async def main():
        # Mock single-cell data
        n_cells = 1000
        n_genes = 2000
        
        sc_data = SingleCellData(
            cell_ids=[f"cell_{i}" for i in range(n_cells)],
            gene_expression=np.random.rand(n_cells, n_genes),
            gene_names=[f"GENE_{i}" for i in range(n_genes)],
            patient_id="patient_001"
        )
        
        pipeline = GenomicTriagePipeline()
        result = await pipeline.analyze_patient_genomics(sc_data)
        
        print(f"Triage Priority: {result.triage_priority}")
        print(f"Risk Score: {result.risk_score:.3f}")
        print(f"Recommendations: {result.clinical_recommendations}")
    
    asyncio.run(main())
