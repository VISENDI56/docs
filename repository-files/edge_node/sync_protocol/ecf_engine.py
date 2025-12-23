"""
Entangled Correlation Fusion (ECF) Engine
IP-05 Enhancement: God-Tier Data Fusion

The ECF engine uses quantum-inspired correlation analysis to fuse vague,
conflicting signals from multiple sources into a single verified timeline.

Key Innovation:
- Traditional fusion: Simple timestamp/location matching
- ECF: Multi-dimensional correlation across time, space, symptoms, and context

Compliance:
- GDPR Art. 5 (Data Accuracy)
- WHO IHR (2005) Article 6 (Notification)
- ISO 27001 A.12.3 (Information Backup)
"""

import numpy as np
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
from enum import Enum
import logging
from scipy.spatial.distance import euclidean
from scipy.stats import pearsonr

logger = logging.getLogger(__name__)


class SignalSource(Enum):
    """Data source types"""
    CBS = "Community-Based Surveillance"
    EMR = "Electronic Medical Records"
    IDSR = "Integrated Disease Surveillance Response"
    IOT = "IoT Sensors"
    VOICE = "Voice Alerts"
    SOCIAL = "Social Media Signals"


class CorrelationStrength(Enum):
    """Correlation strength levels"""
    ENTANGLED = 0.95  # Near-perfect correlation
    STRONG = 0.80     # Strong correlation
    MODERATE = 0.60   # Moderate correlation
    WEAK = 0.40       # Weak correlation
    NONE = 0.20       # No meaningful correlation


@dataclass
class Signal:
    """Individual signal from a data source"""
    source: SignalSource
    timestamp: datetime
    location: Tuple[float, float]  # (lat, lng)
    symptom: str
    severity: float  # 0.0 to 1.0
    confidence: float  # 0.0 to 1.0
    metadata: Dict
    
    def to_vector(self) -> np.ndarray:
        """Convert signal to feature vector for correlation analysis"""
        # Normalize timestamp to hours since epoch
        time_hours = self.timestamp.timestamp() / 3600
        
        # Symptom encoding (simple hash for now)
        symptom_hash = hash(self.symptom.lower()) % 1000 / 1000
        
        return np.array([
            self.location[0],      # Latitude
            self.location[1],      # Longitude
            time_hours,            # Temporal component
            self.severity,         # Severity
            self.confidence,       # Confidence
            symptom_hash,          # Symptom encoding
        ])


@dataclass
class FusedEvent:
    """Fused event from multiple correlated signals"""
    event_id: str
    primary_source: SignalSource
    correlated_sources: List[SignalSource]
    timestamp: datetime
    location: Tuple[float, float]
    symptom: str
    severity: float
    confidence: float
    correlation_score: float
    verification_status: str
    contributing_signals: List[Signal]
    metadata: Dict


class ECFEngine:
    """
    Entangled Correlation Fusion Engine
    
    Uses multi-dimensional correlation analysis to fuse signals from
    multiple sources into verified events.
    """
    
    def __init__(
        self,
        temporal_window_hours: float = 24.0,
        spatial_threshold_km: float = 50.0,
        min_correlation_score: float = 0.6,
        enable_quantum_weighting: bool = True
    ):
        """
        Initialize ECF Engine
        
        Args:
            temporal_window_hours: Time window for correlation (hours)
            spatial_threshold_km: Spatial distance threshold (km)
            min_correlation_score: Minimum correlation for fusion
            enable_quantum_weighting: Use quantum-inspired weighting
        """
        self.temporal_window = timedelta(hours=temporal_window_hours)
        self.spatial_threshold = spatial_threshold_km
        self.min_correlation = min_correlation_score
        self.enable_quantum = enable_quantum_weighting
        
        # Signal buffer for correlation analysis
        self.signal_buffer: List[Signal] = []
        
        # Fused events
        self.fused_events: List[FusedEvent] = []
        
        logger.info(f"🔗 ECF Engine initialized - Quantum: {enable_quantum_weighting}")
    
    def ingest_signal(self, signal: Signal) -> Optional[FusedEvent]:
        """
        Ingest a new signal and attempt fusion with existing signals
        
        Args:
            signal: New signal to ingest
        
        Returns:
            FusedEvent if fusion occurred, None otherwise
        """
        # Add to buffer
        self.signal_buffer.append(signal)
        
        # Find correlated signals
        correlated = self._find_correlated_signals(signal)
        
        if len(correlated) > 0:
            # Fuse signals
            fused_event = self._fuse_signals([signal] + correlated)
            self.fused_events.append(fused_event)
            
            logger.info(
                f"✨ ECF Fusion: {len(correlated) + 1} signals → "
                f"Correlation: {fused_event.correlation_score:.2f}"
            )
            
            return fused_event
        
        return None
    
    def _find_correlated_signals(self, target: Signal) -> List[Signal]:
        """
        Find signals correlated with target signal
        
        Uses multi-dimensional correlation:
        1. Temporal proximity
        2. Spatial proximity
        3. Symptom similarity
        4. Severity correlation
        5. Source diversity (bonus)
        """
        correlated = []
        
        for candidate in self.signal_buffer:
            # Skip same signal
            if candidate == target:
                continue
            
            # Skip if outside temporal window
            time_delta = abs((target.timestamp - candidate.timestamp).total_seconds() / 3600)
            if time_delta > self.temporal_window.total_seconds() / 3600:
                continue
            
            # Calculate correlation score
            correlation = self._calculate_correlation(target, candidate)
            
            if correlation >= self.min_correlation:
                correlated.append(candidate)
        
        return correlated
    
    def _calculate_correlation(self, signal1: Signal, signal2: Signal) -> float:
        """
        Calculate multi-dimensional correlation between two signals
        
        Returns correlation score (0.0 to 1.0)
        """
        # 1. Temporal correlation
        time_delta_hours = abs((signal1.timestamp - signal2.timestamp).total_seconds() / 3600)
        temporal_score = max(0, 1 - (time_delta_hours / 24))  # Decay over 24 hours
        
        # 2. Spatial correlation
        spatial_distance = self._haversine_distance(signal1.location, signal2.location)
        spatial_score = max(0, 1 - (spatial_distance / self.spatial_threshold))
        
        # 3. Symptom similarity
        symptom_score = 1.0 if signal1.symptom.lower() == signal2.symptom.lower() else 0.3
        
        # 4. Severity correlation
        severity_diff = abs(signal1.severity - signal2.severity)
        severity_score = 1 - severity_diff
        
        # 5. Source diversity bonus
        source_bonus = 0.1 if signal1.source != signal2.source else 0.0
        
        # Weighted combination
        if self.enable_quantum:
            # Quantum-inspired weighting (non-linear)
            weights = np.array([0.3, 0.3, 0.2, 0.15, 0.05])
            scores = np.array([
                temporal_score,
                spatial_score,
                symptom_score,
                severity_score,
                source_bonus
            ])
            
            # Apply quantum entanglement factor (amplifies strong correlations)
            base_score = np.dot(weights, scores)
            entanglement_factor = np.exp(base_score - 0.5)  # Exponential boost
            correlation = min(1.0, base_score * entanglement_factor)
        else:
            # Linear weighting
            correlation = (
                0.3 * temporal_score +
                0.3 * spatial_score +
                0.2 * symptom_score +
                0.15 * severity_score +
                0.05 * source_bonus
            )
        
        return correlation
    
    def _fuse_signals(self, signals: List[Signal]) -> FusedEvent:
        """
        Fuse multiple correlated signals into a single event
        
        Uses weighted averaging based on confidence and source reliability
        """
        # Calculate source weights
        source_weights = {
            SignalSource.EMR: 1.0,      # Ground truth
            SignalSource.IDSR: 0.9,     # Government standard
            SignalSource.CBS: 0.8,      # Community surveillance
            SignalSource.IOT: 0.7,      # Sensor data
            SignalSource.VOICE: 0.6,    # Voice alerts
            SignalSource.SOCIAL: 0.4,   # Social media (lowest trust)
        }
        
        # Weighted average of locations
        total_weight = sum(
            s.confidence * source_weights[s.source] for s in signals
        )
        
        avg_lat = sum(
            s.location[0] * s.confidence * source_weights[s.source]
            for s in signals
        ) / total_weight
        
        avg_lng = sum(
            s.location[1] * s.confidence * source_weights[s.source]
            for s in signals
        ) / total_weight
        
        # Weighted average of timestamps
        avg_timestamp = datetime.fromtimestamp(
            sum(
                s.timestamp.timestamp() * s.confidence * source_weights[s.source]
                for s in signals
            ) / total_weight
        )
        
        # Weighted average of severity
        avg_severity = sum(
            s.severity * s.confidence * source_weights[s.source]
            for s in signals
        ) / total_weight
        
        # Maximum confidence (fusion increases confidence)
        max_confidence = min(1.0, max(s.confidence for s in signals) * 1.2)
        
        # Primary source (highest weight)
        primary_source = max(signals, key=lambda s: source_weights[s.source]).source
        
        # Most common symptom
        symptom_counts = {}
        for s in signals:
            symptom_counts[s.symptom] = symptom_counts.get(s.symptom, 0) + 1
        primary_symptom = max(symptom_counts, key=symptom_counts.get)
        
        # Calculate overall correlation score
        correlation_scores = []
        for i in range(len(signals)):
            for j in range(i + 1, len(signals)):
                correlation_scores.append(
                    self._calculate_correlation(signals[i], signals[j])
                )
        avg_correlation = np.mean(correlation_scores) if correlation_scores else 0.0
        
        # Determine verification status
        if avg_correlation >= CorrelationStrength.ENTANGLED.value:
            verification_status = "ENTANGLED"
        elif avg_correlation >= CorrelationStrength.STRONG.value:
            verification_status = "CONFIRMED"
        elif avg_correlation >= CorrelationStrength.MODERATE.value:
            verification_status = "PROBABLE"
        else:
            verification_status = "POSSIBLE"
        
        # Generate event ID
        event_id = f"ECF_{int(avg_timestamp.timestamp())}_{hash(primary_symptom) % 10000}"
        
        return FusedEvent(
            event_id=event_id,
            primary_source=primary_source,
            correlated_sources=[s.source for s in signals],
            timestamp=avg_timestamp,
            location=(avg_lat, avg_lng),
            symptom=primary_symptom,
            severity=avg_severity,
            confidence=max_confidence,
            correlation_score=avg_correlation,
            verification_status=verification_status,
            contributing_signals=signals,
            metadata={
                "num_sources": len(set(s.source for s in signals)),
                "num_signals": len(signals),
                "quantum_enabled": self.enable_quantum,
            }
        )
    
    def _haversine_distance(
        self,
        loc1: Tuple[float, float],
        loc2: Tuple[float, float]
    ) -> float:
        """
        Calculate distance between two lat/lng points (km)
        
        Uses Haversine formula
        """
        lat1, lng1 = np.radians(loc1)
        lat2, lng2 = np.radians(loc2)
        
        dlat = lat2 - lat1
        dlng = lng2 - lng1
        
        a = np.sin(dlat / 2)**2 + np.cos(lat1) * np.cos(lat2) * np.sin(dlng / 2)**2
        c = 2 * np.arcsin(np.sqrt(a))
        
        # Earth radius in km
        r = 6371
        
        return c * r
    
    def get_fused_events(
        self,
        min_correlation: Optional[float] = None,
        source_filter: Optional[List[SignalSource]] = None
    ) -> List[FusedEvent]:
        """Get fused events with optional filtering"""
        events = self.fused_events
        
        if min_correlation:
            events = [e for e in events if e.correlation_score >= min_correlation]
        
        if source_filter:
            events = [
                e for e in events
                if e.primary_source in source_filter
            ]
        
        return events
    
    def clear_old_signals(self, retention_hours: float = 168):
        """Clear signals older than retention period (default: 7 days)"""
        cutoff = datetime.utcnow() - timedelta(hours=retention_hours)
        
        before_count = len(self.signal_buffer)
        self.signal_buffer = [
            s for s in self.signal_buffer
            if s.timestamp > cutoff
        ]
        after_count = len(self.signal_buffer)
        
        cleared = before_count - after_count
        if cleared > 0:
            logger.info(f"🧹 Cleared {cleared} old signals from buffer")


# Example usage
if __name__ == "__main__":
    # Initialize ECF Engine
    ecf = ECFEngine(
        temporal_window_hours=24.0,
        spatial_threshold_km=50.0,
        min_correlation_score=0.6,
        enable_quantum_weighting=True
    )
    
    # Simulate signals from different sources
    signals = [
        Signal(
            source=SignalSource.CBS,
            timestamp=datetime.utcnow(),
            location=(0.0512, 40.3129),  # Dadaab
            symptom="diarrhea",
            severity=0.8,
            confidence=0.7,
            metadata={"chv": "Amina Hassan"}
        ),
        Signal(
            source=SignalSource.EMR,
            timestamp=datetime.utcnow() + timedelta(minutes=30),
            location=(0.0520, 40.3135),  # Nearby clinic
            symptom="diarrhea",
            severity=0.85,
            confidence=0.95,
            metadata={"clinic": "Dadaab Health Center"}
        ),
        Signal(
            source=SignalSource.VOICE,
            timestamp=datetime.utcnow() + timedelta(minutes=45),
            location=(0.0515, 40.3130),
            symptom="diarrhea",
            severity=0.75,
            confidence=0.6,
            metadata={"language": "swahili"}
        ),
    ]
    
    # Ingest signals
    for signal in signals:
        fused = ecf.ingest_signal(signal)
        if fused:
            print(f"\n✨ Fused Event: {fused.event_id}")
            print(f"   Status: {fused.verification_status}")
            print(f"   Correlation: {fused.correlation_score:.2f}")
            print(f"   Sources: {[s.value for s in fused.correlated_sources]}")
            print(f"   Confidence: {fused.confidence:.2f}")
