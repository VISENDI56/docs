# ------------------------------------------------------------------------------
# Copyright (c) 2025 iLuminara (VISENDI56). All Rights Reserved.
# Licensed under the Polyform Shield License 1.0.0.
# 
# Unit Tests - BioNeMo Integration
# ------------------------------------------------------------------------------

"""
Unit tests for BioNeMo integration components.

Tests cover:
- Protein binder design pipeline
- Genomic triage pipeline
- Bio-threat response agent
- cuEquivariance GNN acceleration
- Model registry and downloader
"""

import asyncio
import pytest
import numpy as np
import torch
from pathlib import Path
from unittest.mock import Mock, patch, AsyncMock

# Import modules to test
import sys
sys.path.append(str(Path(__file__).parent.parent))

from core.research.blueprints.protein_binder import (
    ProteinBinderPipeline,
    NIMClient,
    BinderDesignStatus,
    StructurePredictionModel
)
from core.research.blueprints.genomic_triage import (
    GenomicTriagePipeline,
    TriageLevel,
    ImmuneStatus
)
from agentic_clinical.bio_threat_response import (
    BioThreatResponseAgent,
    PatientZeroProfile,
    ThreatLevel
)


class TestNIMClient:
    """Test suite for NIM client."""
    
    @pytest.fixture
    def nim_client(self):
        """Create NIM client fixture."""
        return NIMClient(base_url="http://localhost", timeout=10, max_retries=1)
    
    @pytest.mark.asyncio
    async def test_predict_structure_success(self, nim_client):
        """Test successful structure prediction."""
        mock_response = {
            "pdb": "MOCK_PDB_STRUCTURE",
            "mean_plddt": 85.5
        }
        
        with patch.object(nim_client.session, 'post') as mock_post:
            mock_post.return_value.json.return_value = mock_response
            mock_post.return_value.raise_for_status = Mock()
            
            result = await nim_client.predict_structure(
                sequence="MKTII",
                model=StructurePredictionModel.ALPHAFOLD2
            )
            
            assert result["pdb"] == "MOCK_PDB_STRUCTURE"
            assert result["mean_plddt"] == 85.5
            mock_post.assert_called_once()
    
    @pytest.mark.asyncio
    async def test_predict_structure_retry(self, nim_client):
        """Test structure prediction with retry logic."""
        with patch.object(nim_client.session, 'post') as mock_post:
            # First call fails, second succeeds
            mock_post.side_effect = [
                Exception("Connection error"),
                Mock(json=lambda: {"pdb": "SUCCESS", "mean_plddt": 80.0})
            ]
            
            with pytest.raises(RuntimeError):
                await nim_client.predict_structure("MKTII")


class TestProteinBinderPipeline:
    """Test suite for protein binder design pipeline."""
    
    @pytest.fixture
    def pipeline(self):
        """Create pipeline fixture."""
        return ProteinBinderPipeline(enable_power_monitoring=False)
    
    def test_pipeline_initialization(self, pipeline):
        """Test pipeline initializes correctly."""
        assert pipeline.nim_client is not None
        assert pipeline.output_dir.exists()
        assert not pipeline.enable_power_monitoring
    
    def test_identify_binding_pockets(self, pipeline):
        """Test binding pocket identification."""
        mock_pdb = "MOCK_PDB_STRUCTURE"
        pockets = pipeline._identify_binding_pockets(mock_pdb)
        
        assert len(pockets) > 0
        assert pockets[0].druggability_score > 0
        assert len(pockets[0].residue_indices) > 0
    
    @pytest.mark.asyncio
    async def test_design_neutralizing_binder_mock(self, pipeline):
        """Test binder design with mocked NIM calls."""
        # Mock NIM client methods
        pipeline.nim_client.predict_structure = AsyncMock(return_value={
            "pdb": "MOCK_TARGET_PDB",
            "mean_plddt": 85.0
        })
        pipeline.nim_client.design_binder = AsyncMock(return_value={
            "designs": [{"pdb": "MOCK_BINDER_PDB"}]
        })
        pipeline.nim_client.optimize_sequence = AsyncMock(return_value={
            "sequences": [{"sequence": "MKTIIALSYIFCLVFA"}]
        })
        pipeline.nim_client.validate_complex = AsyncMock(return_value={
            "pdb": "MOCK_COMPLEX_PDB",
            "mean_plddt": 80.0,
            "interface_pae": 5.0
        })
        
        result = await pipeline.design_neutralizing_binder(
            pathogen_sequence="MKTII" * 20,
            pathogen_id="TEST_PATHOGEN"
        )
        
        assert result.pathogen_id == "TEST_PATHOGEN"
        assert result.pipeline_status == BinderDesignStatus.COMPLETED
        assert len(result.binder_candidates) > 0
        assert result.top_binder is not None


class TestGenomicTriagePipeline:
    """Test suite for genomic triage pipeline."""
    
    @pytest.fixture
    def pipeline(self):
        """Create pipeline fixture."""
        return GenomicTriagePipeline(enable_power_monitoring=False)
    
    def test_pipeline_initialization(self, pipeline):
        """Test pipeline initializes correctly."""
        assert pipeline.geneformer is not None
        assert pipeline.evo2 is not None
        assert pipeline.output_dir.exists()
    
    def test_cluster_cell_types(self, pipeline):
        """Test cell type clustering."""
        # Mock embeddings
        embeddings = np.random.randn(100, 256)
        
        labels, profiles = pipeline._cluster_cell_types(embeddings, n_clusters=5)
        
        assert len(labels) == 100
        assert len(profiles) == 5
        assert all(p.cell_count > 0 for p in profiles)
        assert all(0 <= p.activation_score <= 1 for p in profiles)
    
    def test_detect_outlier_cells(self, pipeline):
        """Test outlier cell detection."""
        # Create embeddings with known outliers
        normal_cells = np.random.randn(90, 256)
        outlier_cells = np.random.randn(10, 256) * 5  # Scaled outliers
        embeddings = np.vstack([normal_cells, outlier_cells])
        
        outliers = pipeline._detect_outlier_cells(embeddings, threshold=2.0)
        
        assert len(outliers) > 0
        assert len(outliers) <= 20  # Should detect some outliers
    
    def test_assess_immune_status(self, pipeline):
        """Test immune status assessment."""
        # Mock cell type profiles
        profiles = [
            Mock(activation_score=0.8, cell_type="T cells"),
            Mock(activation_score=0.6, cell_type="B cells"),
            Mock(activation_score=0.9, cell_type="Monocytes")
        ]
        outliers = list(range(15))  # 15% outlier rate
        
        immune_profile = pipeline._assess_immune_status(profiles, outliers, 100)
        
        assert immune_profile.status in ImmuneStatus
        assert 0 <= immune_profile.cytokine_storm_risk <= 1
        assert 0 <= immune_profile.t_cell_exhaustion_score <= 1
    
    def test_determine_triage_level(self, pipeline):
        """Test triage level determination."""
        # High risk profile
        high_risk_profile = Mock(
            cytokine_storm_risk=0.85,
            status=ImmuneStatus.HYPERACTIVE,
            outlier_cells=list(range(20))
        )
        
        level = pipeline._determine_triage_level(high_risk_profile, [])
        assert level == TriageLevel.CRITICAL
        
        # Normal profile
        normal_profile = Mock(
            cytokine_storm_risk=0.1,
            status=ImmuneStatus.NORMAL,
            outlier_cells=[]
        )
        
        level = pipeline._determine_triage_level(normal_profile, [])
        assert level == TriageLevel.NORMAL
    
    @pytest.mark.asyncio
    async def test_analyze_patient_genomics_mock(self, pipeline):
        """Test genomic analysis with mocked models."""
        # Mock Geneformer embeddings
        pipeline.geneformer.embed_cells = AsyncMock(return_value=np.random.randn(100, 256))
        
        # Mock Evo2 anomaly detection
        pipeline.evo2.detect_anomalies = AsyncMock(return_value=[])
        
        # Generate mock data
        gene_expression = np.random.lognormal(0, 1, (100, 500))
        gene_names = [f"GENE_{i}" for i in range(500)]
        
        result = await pipeline.analyze_patient_genomics(
            patient_id="TEST_PATIENT",
            gene_expression_matrix=gene_expression,
            gene_names=gene_names
        )
        
        assert result.patient_id == "TEST_PATIENT"
        assert result.triage_level in TriageLevel
        assert result.immune_profile.status in ImmuneStatus
        assert result.confidence_score >= 0


class TestBioThreatResponseAgent:
    """Test suite for bio-threat response agent."""
    
    @pytest.fixture
    def agent(self):
        """Create agent fixture."""
        return BioThreatResponseAgent(enable_auto_response=True)
    
    def test_agent_initialization(self, agent):
        """Test agent initializes correctly."""
        assert agent.binder_pipeline is not None
        assert agent.triage_pipeline is not None
        assert agent.enable_auto_response
        assert len(agent.active_responses) == 0
    
    def test_assess_threat_level(self, agent):
        """Test threat level assessment."""
        # Critical threat
        critical_patient = PatientZeroProfile(
            patient_id="CRITICAL",
            pathogen_sequence="MKTII",
            gene_expression_data=None,
            gene_names=None,
            dna_sequence=None,
            clinical_symptoms=["respiratory_failure", "cytokine_storm"],
            exposure_history={"airborne": True}
        )
        
        level = agent._assess_threat_level(critical_patient)
        assert level in [ThreatLevel.OUTBREAK, ThreatLevel.PANDEMIC]
        
        # Isolated threat
        isolated_patient = PatientZeroProfile(
            patient_id="ISOLATED",
            pathogen_sequence=None,
            gene_expression_data=None,
            gene_names=None,
            dna_sequence=None,
            clinical_symptoms=["fever"],
            exposure_history={}
        )
        
        level = agent._assess_threat_level(isolated_patient)
        assert level == ThreatLevel.ISOLATED
    
    def test_generate_containment_measures(self, agent):
        """Test containment measure generation."""
        patient = PatientZeroProfile(
            patient_id="TEST",
            pathogen_sequence=None,
            gene_expression_data=None,
            gene_names=None,
            dna_sequence=None,
            clinical_symptoms=[],
            exposure_history={}
        )
        
        # Pandemic level
        measures = agent._generate_containment_measures(ThreatLevel.PANDEMIC, patient)
        assert len(measures) > 0
        assert any("pandemic" in m.lower() for m in measures)
        
        # Isolated level
        measures = agent._generate_containment_measures(ThreatLevel.ISOLATED, patient)
        assert len(measures) > 0
        assert any("isolate" in m.lower() for m in measures)
    
    @pytest.mark.asyncio
    async def test_respond_to_patient_zero_mock(self, agent):
        """Test patient zero response with mocked pipelines."""
        # Mock pipelines
        agent.triage_pipeline.analyze_patient_genomics = AsyncMock(return_value=Mock(
            triage_level=TriageLevel.HIGH,
            immune_profile=Mock(
                status=ImmuneStatus.HYPERACTIVE,
                cytokine_storm_risk=0.75,
                t_cell_exhaustion_score=0.3,
                inflammatory_markers={},
                cell_type_profiles=[],
                outlier_cells=[]
            ),
            recommended_interventions=["Test intervention"],
            energy_consumed_joules=100.0
        ))
        
        agent.binder_pipeline.design_neutralizing_binder = AsyncMock(return_value=Mock(
            pipeline_status=BinderDesignStatus.COMPLETED,
            top_binder=Mock(
                sequence="MKTII",
                binding_affinity=-25.0,
                confidence_score=0.85
            ),
            binder_candidates=[],
            energy_consumed_joules=200.0
        ))
        
        patient_zero = PatientZeroProfile(
            patient_id="PATIENT_ZERO",
            pathogen_sequence="MKTII" * 20,
            gene_expression_data=np.random.randn(100, 500),
            gene_names=[f"GENE_{i}" for i in range(500)],
            dna_sequence=None,
            clinical_symptoms=["fever", "respiratory_distress"],
            exposure_history={}
        )
        
        response = await agent.respond_to_patient_zero(patient_zero)
        
        assert response.patient_zero.patient_id == "PATIENT_ZERO"
        assert response.threat_level in ThreatLevel
        assert len(response.clinical_interventions) > 0
        assert len(response.containment_measures) > 0


class TestCuEquivarianceWrapper:
    """Test suite for cuEquivariance GNN acceleration."""
    
    @pytest.mark.skipif(
        not torch.cuda.is_available(),
        reason="CUDA not available"
    )
    def test_accelerated_gnn_initialization(self):
        """Test accelerated GNN initializes correctly."""
        try:
            from core.gnn_acceleration.cuequivariance_wrapper import AcceleratedGNN
            
            model = AcceleratedGNN(
                in_channels=64,
                hidden_channels=128,
                out_channels=32,
                num_layers=3
            ).cuda()
            
            assert model.in_channels == 64
            assert model.hidden_channels == 128
            assert model.out_channels == 32
            assert model.num_layers == 3
        except ImportError:
            pytest.skip("cuEquivariance not available")
    
    @pytest.mark.skipif(
        not torch.cuda.is_available(),
        reason="CUDA not available"
    )
    def test_accelerated_gnn_forward(self):
        """Test accelerated GNN forward pass."""
        try:
            from core.gnn_acceleration.cuequivariance_wrapper import AcceleratedGNN
            
            model = AcceleratedGNN(
                in_channels=64,
                hidden_channels=128,
                out_channels=32,
                num_layers=2
            ).cuda()
            
            # Mock graph data
            x = torch.randn(100, 64).cuda()
            edge_index = torch.randint(0, 100, (2, 500)).cuda()
            
            output = model(x, edge_index)
            
            assert output.shape == (100, 32)
            assert not torch.isnan(output).any()
        except ImportError:
            pytest.skip("cuEquivariance not available")


class TestModelRegistry:
    """Test suite for model registry."""
    
    def test_registry_file_exists(self):
        """Test registry file exists and is valid."""
        registry_path = Path("ml_ops/models/registry.yaml")
        assert registry_path.exists()
        
        # Try to parse YAML
        import yaml
        with open(registry_path) as f:
            registry = yaml.safe_load(f)
        
        assert "registry" in registry
        assert "protein_structure" in registry
        assert "genomics" in registry
    
    def test_model_downloader_script_exists(self):
        """Test model downloader script exists."""
        script_path = Path("ml_ops/models/model_downloader.sh")
        assert script_path.exists()
        assert script_path.stat().st_mode & 0o111  # Executable


# Integration tests
class TestIntegration:
    """Integration tests for complete workflows."""
    
    @pytest.mark.integration
    @pytest.mark.asyncio
    async def test_end_to_end_bio_threat_response(self):
        """Test complete bio-threat response workflow."""
        # This would require actual NIM services running
        # For now, we test with mocked components
        pytest.skip("Requires running NIM services")
    
    @pytest.mark.integration
    def test_docker_compose_config(self):
        """Test docker-compose configuration is valid."""
        compose_path = Path("substrate/docker-compose.yaml")
        assert compose_path.exists()
        
        # Try to parse YAML
        import yaml
        with open(compose_path) as f:
            compose = yaml.safe_load(f)
        
        assert "services" in compose
        assert "alphafold2" in compose["services"]
        assert "geneformer" in compose["services"]
        assert "evo2" in compose["services"]


# Pytest configuration
def pytest_configure(config):
    """Configure pytest with custom markers."""
    config.addinivalue_line(
        "markers", "integration: mark test as integration test"
    )
    config.addinivalue_line(
        "markers", "slow: mark test as slow running"
    )


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
