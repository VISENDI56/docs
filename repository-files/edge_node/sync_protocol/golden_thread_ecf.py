"""
Golden Thread with Entangled Correlation Fusion (ECF)

This module integrates the ECF engine with the existing Golden Thread protocol,
providing backward compatibility while enabling quantum-inspired fusion.

The Golden Thread now operates in two modes:
1. Legacy Mode: Traditional cross-source verification
2. ECF Mode: Quantum-inspired entanglement fusion (default)

Author: iLuminara-Core Team
License: Proprietary - Sovereign Health Fortress
"""

from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
from datetime import datetime
import numpy as np
import logging

from .entangled_correlation_fusion import (
    EntangledCorrelationFusion,
    SignalNode,
    FusionResult
)

logger = logging.getLogger(__name__)


@dataclass
class GoldenThreadRecord:
    """
    A verified health record from the Golden Thread.
    
    This represents the "collapsed wavefunction" - the single most likely reality
    extracted from multiple vague signals.
    """
    patient_id: str
    timestamp: datetime
    location: Tuple[float, float]
    
    # Fused data
    symptoms: List[str]
    diagnosis: Optional[str]
    severity: float  # 0.0 to 1.0
    
    # Verification metrics
    verification_score: float  # 0.0 to 1.0 (ECF coherence strength)
    confidence: float  # 0.0 to 1.0 (Fused confidence)
    
    # Source tracking
    sources: List[str]  # ["CBS", "EMR", "IDSR"]
    signal_ids: List[str]
    
    # ECF metrics
    coherence_strength: float
    system_entropy: float
    timeline_valid: bool
    
    # Metadata
    metadata: Dict
    
    def to_dict(self) -> Dict:
        """Export to dictionary"""
        return {
            "patient_id": self.patient_id,
            "timestamp": self.timestamp.isoformat(),
            "location": self.location,
            "symptoms": self.symptoms,
            "diagnosis": self.diagnosis,
            "severity": self.severity,
            "verification_score": self.verification_score,
            "confidence": self.confidence,
            "sources": self.sources,
            "signal_ids": self.signal_ids,
            "coherence_strength": self.coherence_strength,
            "system_entropy": self.system_entropy,
            "timeline_valid": self.timeline_valid,
            "metadata": self.metadata
        }


class GoldenThreadECF:
    """
    Golden Thread with Entangled Correlation Fusion.
    
    This is the production-ready integration of ECF into iLuminara's
    data fusion pipeline.
    """
    
    def __init__(
        self,
        feature_dimension: int = 8,
        enable_ecf: bool = True,
        enable_audit: bool = True
    ):
        """
        Initialize Golden Thread with ECF.
        
        Args:
            feature_dimension: Dimension of feature space
            enable_ecf: Enable ECF mode (vs legacy mode)
            enable_audit: Enable audit logging
        """
        self.enable_ecf = enable_ecf
        self.enable_audit = enable_audit
        
        # Initialize ECF engine
        if enable_ecf:
            self.ecf = EntangledCorrelationFusion(
                feature_dimension=feature_dimension,
                enable_audit=enable_audit
            )
        else:
            self.ecf = None
        
        # Storage
        self.records: Dict[str, GoldenThreadRecord] = {}
        
        logger.info(f"🧵 Golden Thread initialized - ECF: {enable_ecf}")
    
    def ingest_cbs_signal(
        self,
        patient_id: str,
        timestamp: float,
        location: Tuple[float, float],
        symptoms: List[str],
        confidence: float = 0.5,
        metadata: Optional[Dict] = None
    ) -> str:
        """
        Ingest a Community-Based Surveillance (CBS) signal.
        
        Args:
            patient_id: Patient identifier
            timestamp: Unix timestamp
            location: (latitude, longitude)
            symptoms: List of symptoms
            confidence: Initial confidence
            metadata: Additional metadata
        
        Returns:
            Signal ID
        """
        # Convert symptoms to feature vector
        features = self._symptoms_to_features(symptoms)
        
        if self.enable_ecf:
            return self.ecf.add_signal(
                features=features,
                timestamp=timestamp,
                location=location,
                confidence=confidence,
                source="CBS",
                patient_id=patient_id,
                metadata=metadata
            )
        else:
            # Legacy mode (not implemented in this version)
            raise NotImplementedError("Legacy mode not implemented")
    
    def ingest_emr_record(
        self,
        patient_id: str,
        timestamp: float,
        location: Tuple[float, float],
        diagnosis: str,
        symptoms: List[str],
        confidence: float = 0.8,
        metadata: Optional[Dict] = None
    ) -> str:
        """
        Ingest an Electronic Medical Record (EMR) entry.
        
        Args:
            patient_id: Patient identifier
            timestamp: Unix timestamp
            location: (latitude, longitude)
            diagnosis: Clinical diagnosis
            symptoms: List of symptoms
            confidence: Initial confidence (EMR typically higher)
            metadata: Additional metadata
        
        Returns:
            Signal ID
        """
        # Convert symptoms + diagnosis to feature vector
        features = self._symptoms_to_features(symptoms)
        
        # Add diagnosis weight
        if diagnosis:
            features = self._add_diagnosis_weight(features, diagnosis)
        
        if self.enable_ecf:
            return self.ecf.add_signal(
                features=features,
                timestamp=timestamp,
                location=location,
                confidence=confidence,
                source="EMR",
                patient_id=patient_id,
                metadata={**(metadata or {}), "diagnosis": diagnosis}
            )
        else:
            raise NotImplementedError("Legacy mode not implemented")
    
    def ingest_idsr_report(
        self,
        patient_id: str,
        timestamp: float,
        location: Tuple[float, float],
        disease: str,
        case_count: int,
        confidence: float = 0.7,
        metadata: Optional[Dict] = None
    ) -> str:
        """
        Ingest an Integrated Disease Surveillance Response (IDSR) report.
        
        Args:
            patient_id: Patient identifier (or aggregate ID)
            timestamp: Unix timestamp
            location: (latitude, longitude)
            disease: Disease name
            case_count: Number of cases
            confidence: Initial confidence
            metadata: Additional metadata
        
        Returns:
            Signal ID
        """
        # Convert disease to feature vector
        features = self._disease_to_features(disease, case_count)
        
        if self.enable_ecf:
            return self.ecf.add_signal(
                features=features,
                timestamp=timestamp,
                location=location,
                confidence=confidence,
                source="IDSR",
                patient_id=patient_id,
                metadata={**(metadata or {}), "disease": disease, "case_count": case_count}
            )
        else:
            raise NotImplementedError("Legacy mode not implemented")
    
    def fuse_and_verify(self) -> GoldenThreadRecord:
        """
        Perform ECF fusion and extract the Golden Thread record.
        
        This is the core operation that transforms vague signals into
        verified truth.
        
        Returns:
            GoldenThreadRecord with fused data
        """
        if not self.enable_ecf:
            raise NotImplementedError("Legacy mode not implemented")
        
        # Perform ECF fusion
        result = self.ecf.fuse()
        
        # Extract the emerged pattern
        pattern = result.emerged_pattern
        
        # Find the most confident signal (the "anchor")
        max_conf_id = max(result.fused_confidences, key=result.fused_confidences.get)
        anchor_signal = self.ecf.get_signal(max_conf_id)
        
        # Extract symptoms from pattern
        symptoms = self._features_to_symptoms(pattern)
        
        # Calculate severity from pattern magnitude
        severity = float(np.linalg.norm(pattern) / np.sqrt(self.ecf.feature_dim))
        
        # Collect all sources
        sources = list(set([self.ecf.get_signal(sid).source for sid in result.fused_confidences.keys()]))
        
        # Create Golden Thread record
        record = GoldenThreadRecord(
            patient_id=anchor_signal.patient_id or "AGGREGATE",
            timestamp=datetime.utcnow(),
            location=tuple(anchor_signal.location),
            symptoms=symptoms,
            diagnosis=anchor_signal.metadata.get("diagnosis"),
            severity=severity,
            verification_score=result.coherence_strength,
            confidence=result.fused_confidences[max_conf_id],
            sources=sources,
            signal_ids=list(result.fused_confidences.keys()),
            coherence_strength=result.coherence_strength,
            system_entropy=result.system_entropy,
            timeline_valid=result.timeline_valid,
            metadata={
                "fusion_timestamp": result.timestamp.isoformat(),
                "num_signals": len(result.fused_confidences)
            }
        )
        
        # Store record
        self.records[anchor_signal.patient_id or "AGGREGATE"] = record
        
        logger.info(f"🧵 Golden Thread extracted - Patient: {record.patient_id}, Verification: {record.verification_score:.3f}")
        
        return record
    
    def get_system_state(self) -> Dict:
        """Get complete system state"""
        if self.enable_ecf:
            return self.ecf.get_system_state()
        else:
            return {}
    
    def _symptoms_to_features(self, symptoms: List[str]) -> List[float]:
        """
        Convert symptom list to feature vector.
        
        Feature mapping:
        [0] Fever
        [1] Cough
        [2] Rash
        [3] Nausea
        [4] Diarrhea
        [5] Vomiting
        [6] Fatigue
        [7] Headache
        """
        feature_map = {
            "fever": 0,
            "cough": 1,
            "rash": 2,
            "nausea": 3,
            "diarrhea": 4,
            "vomiting": 5,
            "fatigue": 6,
            "headache": 7
        }
        
        features = [0.0] * 8
        for symptom in symptoms:
            symptom_lower = symptom.lower()
            if symptom_lower in feature_map:
                features[feature_map[symptom_lower]] = 1.0
        
        return features
    
    def _features_to_symptoms(self, features: np.ndarray) -> List[str]:
        """Convert feature vector back to symptom list"""
        symptom_names = [
            "fever", "cough", "rash", "nausea",
            "diarrhea", "vomiting", "fatigue", "headache"
        ]
        
        symptoms = []
        for i, val in enumerate(features[:8]):
            if val > 0.3:  # Threshold
                symptoms.append(symptom_names[i])
        
        return symptoms
    
    def _add_diagnosis_weight(self, features: List[float], diagnosis: str) -> List[float]:
        """Add diagnosis-specific weighting to features"""
        # Simple implementation - in production, use disease ontology
        diagnosis_weights = {
            "malaria": [1.5, 0.5, 0.5, 1.0, 0.5, 0.5, 1.5, 1.5],  # Fever, fatigue, headache
            "cholera": [0.5, 0.5, 0.5, 1.5, 2.0, 2.0, 1.0, 0.5],  # Diarrhea, vomiting
            "measles": [1.5, 1.5, 2.0, 0.5, 0.5, 0.5, 1.0, 0.5],  # Fever, cough, rash
        }
        
        weights = diagnosis_weights.get(diagnosis.lower(), [1.0] * 8)
        return [f * w for f, w in zip(features, weights)]
    
    def _disease_to_features(self, disease: str, case_count: int) -> List[float]:
        """Convert disease name to feature vector"""
        # Map disease to typical symptom profile
        disease_profiles = {
            "malaria": [0.9, 0.3, 0.2, 0.5, 0.2, 0.2, 0.8, 0.8],
            "cholera": [0.5, 0.2, 0.1, 0.8, 0.9, 0.9, 0.6, 0.3],
            "measles": [0.9, 0.8, 0.9, 0.3, 0.2, 0.2, 0.5, 0.4],
            "covid-19": [0.8, 0.9, 0.1, 0.3, 0.3, 0.2, 0.9, 0.7],
        }
        
        profile = disease_profiles.get(disease.lower(), [0.5] * 8)
        
        # Scale by case count (log scale)
        scale = min(1.0, np.log10(case_count + 1) / 3.0)
        return [p * scale for p in profile]


# --- EXAMPLE USAGE ---

if __name__ == "__main__":
    print("=" * 60)
    print("Golden Thread with ECF - Integration Demo")
    print("=" * 60)
    print()
    
    # Initialize Golden Thread
    gt = GoldenThreadECF(feature_dimension=8, enable_ecf=True)
    
    print("📡 Ingesting signals from multiple sources...")
    print()
    
    # CBS Signal: Community health volunteer report
    gt.ingest_cbs_signal(
        patient_id="PAT_001",
        timestamp=10.0,
        location=(-1.2, 36.8),
        symptoms=["fever", "cough", "fatigue"],
        confidence=0.5,
        metadata={"chv_name": "Amina Hassan", "village": "Ifo Camp"}
    )
    
    # EMR Record: Clinic diagnosis
    gt.ingest_emr_record(
        patient_id="PAT_001",
        timestamp=10.5,
        location=(-1.21, 36.81),
        diagnosis="malaria",
        symptoms=["fever", "headache", "fatigue"],
        confidence=0.8,
        metadata={"clinic": "Dadaab Primary Health Center"}
    )
    
    # IDSR Report: Government surveillance
    gt.ingest_idsr_report(
        patient_id="AGGREGATE_DADAAB",
        timestamp=11.0,
        location=(-1.2, 36.8),
        disease="malaria",
        case_count=15,
        confidence=0.7,
        metadata={"district": "Dadaab", "week": 52}
    )
    
    print()
    print("─" * 60)
    print("🌌 Performing ECF Fusion...")
    print("─" * 60)
    print()
    
    # Fuse and verify
    record = gt.fuse_and_verify()
    
    print()
    print("=" * 60)
    print("🧵 GOLDEN THREAD EXTRACTED")
    print("=" * 60)
    print()
    print(f"Patient ID: {record.patient_id}")
    print(f"Location: {record.location}")
    print(f"Symptoms: {', '.join(record.symptoms)}")
    print(f"Diagnosis: {record.diagnosis}")
    print(f"Severity: {record.severity:.2f}")
    print()
    print(f"✓ Verification Score: {record.verification_score:.3f}")
    print(f"✓ Confidence: {record.confidence:.3f}")
    print(f"✓ Coherence Strength: {record.coherence_strength:.3f}")
    print(f"✓ System Entropy: {record.system_entropy:.3f} nats")
    print(f"✓ Timeline Valid: {record.timeline_valid}")
    print()
    print(f"Sources: {', '.join(record.sources)}")
    print(f"Signals: {len(record.signal_ids)}")
    print()
    print("=" * 60)
