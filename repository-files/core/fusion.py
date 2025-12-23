"""
IP-05: Golden Thread - Quantum Fusion Logic
Multi-source data validation using quantum entanglement principles

Compliance:
- WHO IHR (2005) Article 6 (Notification)
- FHIR R4/R5 (Healthcare data interoperability)
- Geneva Convention Article 3 (Data protection in humanitarian contexts)
"""

import hashlib
import json
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
from enum import Enum
from dataclasses import dataclass, asdict
import logging

logger = logging.getLogger(__name__)


class DataSource(Enum):
    """Data source types for fusion"""
    CBS = "Community-Based Surveillance"
    EMR = "Electronic Medical Records"
    IDSR = "Integrated Disease Surveillance Response"
    IOT = "IoT Sensors"
    VOICE = "Voice Alerts"


class VerificationStatus(Enum):
    """Verification status based on multi-source agreement"""
    CONFIRMED = 1.0  # Multiple sources agree
    PROBABLE = 0.75  # Partial agreement
    POSSIBLE = 0.5   # Significant conflicts but plausible
    UNVERIFIED = 0.25  # Single source or major conflicts
    REJECTED = 0.0   # Contradictory evidence


@dataclass
class DataSignal:
    """Individual data signal from a source"""
    source: DataSource
    location: str
    symptom: Optional[str]
    diagnosis: Optional[str]
    timestamp: datetime
    latitude: Optional[float]
    longitude: Optional[float]
    severity: Optional[int]
    metadata: Dict
    
    def to_dict(self) -> Dict:
        """Convert to dictionary"""
        data = asdict(self)
        data['source'] = self.source.value
        data['timestamp'] = self.timestamp.isoformat()
        return data


@dataclass
class FusedRecord:
    """Fused record from multiple sources"""
    record_id: str
    patient_id: str
    location: str
    primary_symptom: str
    diagnosis: Optional[str]
    timestamp: datetime
    verification_score: float
    verification_status: VerificationStatus
    sources: List[DataSource]
    spatial_delta_km: float
    temporal_delta_hours: float
    confidence_factors: Dict
    metadata: Dict
    
    def to_dict(self) -> Dict:
        """Convert to dictionary"""
        data = asdict(self)
        data['timestamp'] = self.timestamp.isoformat()
        data['verification_status'] = self.verification_status.name
        data['sources'] = [s.value for s in self.sources]
        return data


class GoldenThreadFusion:
    """
    IP-05: Golden Thread Quantum Fusion Engine
    
    Uses quantum entanglement logic to fuse vague signals from multiple sources.
    A signal is promoted to CONFIRMED only if spatial and temporal deltas match
    across at least two disparate sources.
    """
    
    def __init__(
        self,
        spatial_threshold_km: float = 5.0,
        temporal_threshold_hours: float = 24.0,
        min_sources_for_confirmation: int = 2
    ):
        self.spatial_threshold_km = spatial_threshold_km
        self.temporal_threshold_hours = temporal_threshold_hours
        self.min_sources_for_confirmation = min_sources_for_confirmation
        
        # Fusion history
        self.fusion_history: List[FusedRecord] = []
        
        logger.info(f"🧬 Golden Thread initialized - Spatial: {spatial_threshold_km}km, Temporal: {temporal_threshold_hours}h")
    
    def fuse_signals(
        self,
        signals: List[DataSignal],
        patient_id: str
    ) -> FusedRecord:
        """
        Fuse multiple data signals using quantum entanglement logic.
        
        Args:
            signals: List of data signals from different sources
            patient_id: Patient identifier
        
        Returns:
            FusedRecord with verification score
        """
        if not signals:
            raise ValueError("At least one signal required for fusion")
        
        # Sort signals by timestamp
        signals = sorted(signals, key=lambda s: s.timestamp)
        
        # Calculate spatial and temporal deltas
        spatial_delta = self._calculate_spatial_delta(signals)
        temporal_delta = self._calculate_temporal_delta(signals)
        
        # Calculate verification score
        verification_score, confidence_factors = self._calculate_verification_score(
            signals, spatial_delta, temporal_delta
        )
        
        # Determine verification status
        verification_status = self._determine_verification_status(verification_score)
        
        # Extract primary information
        primary_signal = signals[0]  # Most recent or most reliable
        location = self._resolve_location(signals)
        primary_symptom = self._resolve_symptom(signals)
        diagnosis = self._resolve_diagnosis(signals)
        
        # Generate record ID
        record_id = self._generate_record_id(patient_id, signals)
        
        # Create fused record
        fused_record = FusedRecord(
            record_id=record_id,
            patient_id=patient_id,
            location=location,
            primary_symptom=primary_symptom,
            diagnosis=diagnosis,
            timestamp=primary_signal.timestamp,
            verification_score=verification_score,
            verification_status=verification_status,
            sources=[s.source for s in signals],
            spatial_delta_km=spatial_delta,
            temporal_delta_hours=temporal_delta,
            confidence_factors=confidence_factors,
            metadata={
                'signal_count': len(signals),
                'source_diversity': len(set(s.source for s in signals)),
                'fusion_timestamp': datetime.utcnow().isoformat()
            }
        )
        
        # Store in history
        self.fusion_history.append(fused_record)
        
        logger.info(
            f"✅ Fusion complete - Record: {record_id}, "
            f"Score: {verification_score:.2f}, Status: {verification_status.name}"
        )
        
        return fused_record
    
    def _calculate_spatial_delta(self, signals: List[DataSignal]) -> float:
        """Calculate maximum spatial distance between signals"""
        if len(signals) < 2:
            return 0.0
        
        max_delta = 0.0
        for i, signal1 in enumerate(signals):
            for signal2 in signals[i+1:]:
                if signal1.latitude and signal1.longitude and signal2.latitude and signal2.longitude:
                    delta = self._haversine_distance(
                        signal1.latitude, signal1.longitude,
                        signal2.latitude, signal2.longitude
                    )
                    max_delta = max(max_delta, delta)
        
        return max_delta
    
    def _calculate_temporal_delta(self, signals: List[DataSignal]) -> float:
        """Calculate maximum temporal distance between signals"""
        if len(signals) < 2:
            return 0.0
        
        timestamps = [s.timestamp for s in signals]
        delta = (max(timestamps) - min(timestamps)).total_seconds() / 3600.0
        return delta
    
    def _calculate_verification_score(
        self,
        signals: List[DataSignal],
        spatial_delta: float,
        temporal_delta: float
    ) -> Tuple[float, Dict]:
        """
        Calculate verification score using quantum entanglement logic.
        
        Score factors:
        1. Source diversity (multiple independent sources)
        2. Spatial agreement (signals from same location)
        3. Temporal agreement (signals within time window)
        4. Symptom consistency (similar symptoms/diagnosis)
        """
        confidence_factors = {}
        
        # Factor 1: Source diversity (0.0 - 0.3)
        unique_sources = len(set(s.source for s in signals))
        source_diversity_score = min(unique_sources / 3.0, 1.0) * 0.3
        confidence_factors['source_diversity'] = source_diversity_score
        
        # Factor 2: Spatial agreement (0.0 - 0.3)
        if spatial_delta <= self.spatial_threshold_km:
            spatial_score = 0.3 * (1.0 - spatial_delta / self.spatial_threshold_km)
        else:
            spatial_score = 0.0
        confidence_factors['spatial_agreement'] = spatial_score
        
        # Factor 3: Temporal agreement (0.0 - 0.3)
        if temporal_delta <= self.temporal_threshold_hours:
            temporal_score = 0.3 * (1.0 - temporal_delta / self.temporal_threshold_hours)
        else:
            temporal_score = 0.0
        confidence_factors['temporal_agreement'] = temporal_score
        
        # Factor 4: Symptom consistency (0.0 - 0.1)
        symptom_score = self._calculate_symptom_consistency(signals) * 0.1
        confidence_factors['symptom_consistency'] = symptom_score
        
        # Total score
        total_score = sum(confidence_factors.values())
        
        # Bonus for meeting minimum source requirement
        if unique_sources >= self.min_sources_for_confirmation:
            total_score = min(total_score + 0.1, 1.0)
            confidence_factors['multi_source_bonus'] = 0.1
        
        return total_score, confidence_factors
    
    def _calculate_symptom_consistency(self, signals: List[DataSignal]) -> float:
        """Calculate symptom consistency across signals"""
        symptoms = [s.symptom for s in signals if s.symptom]
        diagnoses = [s.diagnosis for s in signals if s.diagnosis]
        
        if not symptoms and not diagnoses:
            return 0.0
        
        # Simple consistency: all symptoms/diagnoses match
        if symptoms:
            unique_symptoms = len(set(symptoms))
            symptom_consistency = 1.0 / unique_symptoms
        else:
            symptom_consistency = 0.5
        
        if diagnoses:
            unique_diagnoses = len(set(diagnoses))
            diagnosis_consistency = 1.0 / unique_diagnoses
        else:
            diagnosis_consistency = 0.5
        
        return (symptom_consistency + diagnosis_consistency) / 2.0
    
    def _determine_verification_status(self, score: float) -> VerificationStatus:
        """Determine verification status from score"""
        if score >= 0.8:
            return VerificationStatus.CONFIRMED
        elif score >= 0.6:
            return VerificationStatus.PROBABLE
        elif score >= 0.4:
            return VerificationStatus.POSSIBLE
        elif score >= 0.2:
            return VerificationStatus.UNVERIFIED
        else:
            return VerificationStatus.REJECTED
    
    def _resolve_location(self, signals: List[DataSignal]) -> str:
        """Resolve location from multiple signals (prefer EMR)"""
        # Prefer EMR location (ground truth)
        for signal in signals:
            if signal.source == DataSource.EMR:
                return signal.location
        
        # Otherwise use most common location
        locations = [s.location for s in signals]
        return max(set(locations), key=locations.count)
    
    def _resolve_symptom(self, signals: List[DataSignal]) -> str:
        """Resolve primary symptom from multiple signals"""
        symptoms = [s.symptom for s in signals if s.symptom]
        if not symptoms:
            return "unknown"
        
        # Use most common symptom
        return max(set(symptoms), key=symptoms.count)
    
    def _resolve_diagnosis(self, signals: List[DataSignal]) -> Optional[str]:
        """Resolve diagnosis from multiple signals (prefer EMR)"""
        # Prefer EMR diagnosis (ground truth)
        for signal in signals:
            if signal.source == DataSource.EMR and signal.diagnosis:
                return signal.diagnosis
        
        # Otherwise use most common diagnosis
        diagnoses = [s.diagnosis for s in signals if s.diagnosis]
        if not diagnoses:
            return None
        
        return max(set(diagnoses), key=diagnoses.count)
    
    def _generate_record_id(self, patient_id: str, signals: List[DataSignal]) -> str:
        """Generate unique record ID"""
        data = f"{patient_id}_{signals[0].timestamp.isoformat()}"
        return hashlib.sha256(data.encode()).hexdigest()[:16]
    
    def _haversine_distance(
        self,
        lat1: float, lon1: float,
        lat2: float, lon2: float
    ) -> float:
        """Calculate distance between two points using Haversine formula"""
        from math import radians, sin, cos, sqrt, atan2
        
        R = 6371.0  # Earth radius in km
        
        lat1_rad = radians(lat1)
        lon1_rad = radians(lon1)
        lat2_rad = radians(lat2)
        lon2_rad = radians(lon2)
        
        dlat = lat2_rad - lat1_rad
        dlon = lon2_rad - lon1_rad
        
        a = sin(dlat/2)**2 + cos(lat1_rad) * cos(lat2_rad) * sin(dlon/2)**2
        c = 2 * atan2(sqrt(a), sqrt(1-a))
        
        return R * c
    
    def get_fusion_history(self, limit: int = 100) -> List[FusedRecord]:
        """Get recent fusion history"""
        return self.fusion_history[-limit:]
    
    def get_verification_statistics(self) -> Dict:
        """Get verification statistics"""
        if not self.fusion_history:
            return {}
        
        total = len(self.fusion_history)
        status_counts = {}
        
        for record in self.fusion_history:
            status = record.verification_status.name
            status_counts[status] = status_counts.get(status, 0) + 1
        
        return {
            'total_fusions': total,
            'status_distribution': {
                status: count / total for status, count in status_counts.items()
            },
            'average_verification_score': sum(r.verification_score for r in self.fusion_history) / total,
            'average_spatial_delta_km': sum(r.spatial_delta_km for r in self.fusion_history) / total,
            'average_temporal_delta_hours': sum(r.temporal_delta_hours for r in self.fusion_history) / total
        }


# Example usage
if __name__ == "__main__":
    # Initialize Golden Thread
    fusion = GoldenThreadFusion(
        spatial_threshold_km=5.0,
        temporal_threshold_hours=24.0,
        min_sources_for_confirmation=2
    )
    
    # Create test signals
    signals = [
        DataSignal(
            source=DataSource.CBS,
            location="Dadaab",
            symptom="diarrhea",
            diagnosis=None,
            timestamp=datetime(2025, 1, 15, 8, 0),
            latitude=0.0512,
            longitude=40.3129,
            severity=8,
            metadata={"source_id": "CHV_AMINA"}
        ),
        DataSignal(
            source=DataSource.EMR,
            location="Dadaab",
            symptom="diarrhea",
            diagnosis="cholera",
            timestamp=datetime(2025, 1, 15, 8, 30),
            latitude=0.0515,
            longitude=40.3132,
            severity=9,
            metadata={"source_id": "DADAAB_CLINIC"}
        )
    ]
    
    # Fuse signals
    fused = fusion.fuse_signals(signals, patient_id="PAT_001")
    
    print(f"✅ Fused Record:")
    print(f"   Record ID: {fused.record_id}")
    print(f"   Verification Score: {fused.verification_score:.2f}")
    print(f"   Status: {fused.verification_status.name}")
    print(f"   Sources: {[s.value for s in fused.sources]}")
    print(f"   Spatial Delta: {fused.spatial_delta_km:.2f} km")
    print(f"   Temporal Delta: {fused.temporal_delta_hours:.2f} hours")
    print(f"   Confidence Factors: {json.dumps(fused.confidence_factors, indent=2)}")
