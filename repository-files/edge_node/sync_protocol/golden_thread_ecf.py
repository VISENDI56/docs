"""
The Golden Thread: ECF-Enhanced Data Fusion Engine
═════════════════════════════════════════════════════════════════════════════
UPGRADE: Integrates Entangled Correlation Fusion (ECF) for God-Tier fusion.

This enhanced version uses the ECF engine for multi-dimensional correlation
analysis, providing superior signal fusion compared to simple timestamp/location
matching.

Philosophy: "Quantum entanglement logic to fuse vague signals into verified timelines."
"""

from typing import Dict, Any, Optional, List
from datetime import datetime, timedelta
from dataclasses import dataclass
import logging

# Import base Golden Thread
from .golden_thread import (
    GoldenThread,
    TimeseriesRecord,
    DataSourceType,
    VerificationScore
)

# Import ECF Engine
from .ecf_engine import (
    ECFEngine,
    Signal,
    SignalSource,
    FusedEvent,
    CorrelationStrength
)

logger = logging.getLogger(__name__)


class GoldenThreadECF(GoldenThread):
    """
    Enhanced Golden Thread with ECF integration.
    
    Provides backward compatibility with original Golden Thread API
    while leveraging ECF's advanced correlation analysis.
    """
    
    def __init__(
        self,
        enable_ecf: bool = True,
        temporal_window_hours: float = 24.0,
        spatial_threshold_km: float = 50.0,
        min_correlation_score: float = 0.6,
        enable_quantum_weighting: bool = True
    ):
        """
        Initialize ECF-enhanced Golden Thread
        
        Args:
            enable_ecf: Enable ECF engine (fallback to classic if False)
            temporal_window_hours: ECF temporal window
            spatial_threshold_km: ECF spatial threshold
            min_correlation_score: Minimum correlation for fusion
            enable_quantum_weighting: Use quantum-inspired weighting
        """
        # Initialize base Golden Thread
        super().__init__()
        
        # Initialize ECF Engine
        self.enable_ecf = enable_ecf
        if enable_ecf:
            self.ecf_engine = ECFEngine(
                temporal_window_hours=temporal_window_hours,
                spatial_threshold_km=spatial_threshold_km,
                min_correlation_score=min_correlation_score,
                enable_quantum_weighting=enable_quantum_weighting
            )
            logger.info("🔗 Golden Thread ECF mode: ENABLED")
        else:
            self.ecf_engine = None
            logger.info("📊 Golden Thread ECF mode: DISABLED (classic mode)")
    
    def fuse_data_streams(
        self,
        cbs_signal: Optional[Dict[str, Any]] = None,
        emr_record: Optional[Dict[str, Any]] = None,
        idsr_template: Optional[Dict[str, Any]] = None,
        patient_id: str = "UNKNOWN",
    ) -> TimeseriesRecord:
        """
        Fuse data streams using ECF engine (if enabled).
        
        Falls back to classic Golden Thread if ECF is disabled.
        """
        if not self.enable_ecf or self.ecf_engine is None:
            # Fallback to classic Golden Thread
            return super().fuse_data_streams(
                cbs_signal=cbs_signal,
                emr_record=emr_record,
                idsr_template=idsr_template,
                patient_id=patient_id
            )
        
        # ECF-enhanced fusion
        return self._fuse_with_ecf(
            cbs_signal=cbs_signal,
            emr_record=emr_record,
            idsr_template=idsr_template,
            patient_id=patient_id
        )
    
    def _fuse_with_ecf(
        self,
        cbs_signal: Optional[Dict[str, Any]],
        emr_record: Optional[Dict[str, Any]],
        idsr_template: Optional[Dict[str, Any]],
        patient_id: str
    ) -> TimeseriesRecord:
        """
        Perform ECF-enhanced fusion
        """
        # Convert data to ECF signals
        ecf_signals = []
        
        if cbs_signal:
            ecf_signals.append(self._convert_to_ecf_signal(cbs_signal, SignalSource.CBS))
        
        if emr_record:
            ecf_signals.append(self._convert_to_ecf_signal(emr_record, SignalSource.EMR))
        
        if idsr_template:
            ecf_signals.append(self._convert_to_ecf_signal(idsr_template, SignalSource.IDSR))
        
        # Ingest signals into ECF engine
        fused_event = None
        for signal in ecf_signals:
            result = self.ecf_engine.ingest_signal(signal)
            if result:
                fused_event = result
        
        # Convert ECF result to TimeseriesRecord
        if fused_event:
            return self._convert_ecf_to_timeseries(fused_event, patient_id)
        else:
            # No fusion occurred, create single-source record
            return self._create_single_source_record(
                cbs_signal, emr_record, idsr_template, patient_id
            )
    
    def _convert_to_ecf_signal(
        self,
        data: Dict[str, Any],
        source: SignalSource
    ) -> Signal:
        """
        Convert Golden Thread data format to ECF Signal format
        """
        # Parse timestamp
        timestamp_str = data.get("timestamp")
        if timestamp_str:
            timestamp = self._parse_timestamp(data, source.value)
        else:
            timestamp = datetime.utcnow()
        
        # Parse location
        location_str = data.get("location", "0,0")
        if isinstance(location_str, str):
            if "," in location_str:
                lat, lng = map(float, location_str.split(","))
            else:
                lat, lng = 0.0, 0.0
        elif isinstance(location_str, (list, tuple)):
            lat, lng = location_str[0], location_str[1]
        else:
            lat, lng = 0.0, 0.0
        
        # Extract symptom/diagnosis
        symptom = data.get("symptom") or data.get("diagnosis") or "unknown"
        
        # Extract severity (0.0 to 1.0)
        severity = data.get("severity", 0.5)
        if isinstance(severity, str):
            severity = float(severity)
        
        # Extract confidence
        confidence = data.get("confidence", 0.7)
        
        return Signal(
            source=source,
            timestamp=timestamp,
            location=(lat, lng),
            symptom=symptom,
            severity=severity,
            confidence=confidence,
            metadata=data
        )
    
    def _convert_ecf_to_timeseries(
        self,
        fused_event: FusedEvent,
        patient_id: str
    ) -> TimeseriesRecord:
        """
        Convert ECF FusedEvent to Golden Thread TimeseriesRecord
        """
        # Map ECF verification status to Golden Thread verification score
        verification_map = {
            "ENTANGLED": VerificationScore.ENTANGLED.value,
            "CONFIRMED": VerificationScore.CONFIRMED.value,
            "PROBABLE": VerificationScore.PROBABLE.value,
            "POSSIBLE": VerificationScore.POSSIBLE.value,
        }
        verification_score = verification_map.get(
            fused_event.verification_status,
            VerificationScore.UNVERIFIED.value
        )
        
        # Generate record ID
        record_id = self._generate_record_id(patient_id, fused_event.timestamp)
        
        # Extract location string
        location = f"{fused_event.location[0]},{fused_event.location[1]}"
        
        # Build data sources dict
        data_sources = {}
        for signal in fused_event.contributing_signals:
            source_key = signal.source.value
            data_sources[source_key] = signal.metadata
        
        # Build canonical data
        canonical_data = {
            "symptom": fused_event.symptom,
            "severity": fused_event.severity,
            "confidence": fused_event.confidence,
            "location": location,
            "ecf_correlation_score": fused_event.correlation_score,
            "ecf_verification_status": fused_event.verification_status,
        }
        
        # Build confidence chain
        confidence_chain = [
            {
                "step": "ecf_fusion",
                "sources": [s.value for s in fused_event.correlated_sources],
                "timestamp": datetime.utcnow().isoformat(),
                "correlation_score": fused_event.correlation_score,
            },
            {
                "step": "verification_score_calculated",
                "score": verification_score,
                "reasoning": f"ECF {fused_event.verification_status} - Correlation: {fused_event.correlation_score:.2f}",
            },
        ]
        
        # Determine retention status
        retention_status = self._check_retention(fused_event.timestamp)
        
        # Create TimeseriesRecord
        record = TimeseriesRecord(
            record_id=record_id,
            patient_id=patient_id,
            event_type=self._infer_event_type_from_symptom(fused_event.symptom),
            location=location,
            timestamp=fused_event.timestamp,
            data_sources=data_sources,
            verification_score=verification_score,
            canonical_data=canonical_data,
            confidence_chain=confidence_chain,
            retention_status=retention_status,
        )
        
        # Store in fused records
        if patient_id not in self.fused_records:
            self.fused_records[patient_id] = []
        self.fused_records[patient_id].append(record)
        
        # Log fusion event
        self.fusion_log.append({
            "record_id": record_id,
            "patient_id": patient_id,
            "verification_score": verification_score,
            "ecf_correlation_score": fused_event.correlation_score,
            "sources_count": len(fused_event.contributing_signals),
            "timestamp": datetime.utcnow().isoformat(),
            "retention_status": retention_status,
        })
        
        logger.info(
            f"✨ ECF Fusion Complete - Record: {record_id}, "
            f"Correlation: {fused_event.correlation_score:.2f}, "
            f"Status: {fused_event.verification_status}"
        )
        
        return record
    
    def _create_single_source_record(
        self,
        cbs_signal: Optional[Dict],
        emr_record: Optional[Dict],
        idsr_template: Optional[Dict],
        patient_id: str
    ) -> TimeseriesRecord:
        """
        Create record from single source (no fusion occurred)
        """
        # Fallback to classic Golden Thread for single-source records
        return super().fuse_data_streams(
            cbs_signal=cbs_signal,
            emr_record=emr_record,
            idsr_template=idsr_template,
            patient_id=patient_id
        )
    
    def _infer_event_type_from_symptom(self, symptom: str) -> str:
        """Infer event type from symptom"""
        symptom_lower = symptom.lower()
        
        if any(word in symptom_lower for word in ["fever", "cough", "diarrhea"]):
            return "symptom_report"
        elif any(word in symptom_lower for word in ["malaria", "cholera", "covid"]):
            return "diagnosis"
        else:
            return "unknown_event"
    
    def get_ecf_statistics(self) -> Dict[str, Any]:
        """
        Get ECF engine statistics
        """
        if not self.enable_ecf or self.ecf_engine is None:
            return {"ecf_enabled": False}
        
        fused_events = self.ecf_engine.get_fused_events()
        
        # Calculate statistics
        total_events = len(fused_events)
        
        if total_events == 0:
            return {
                "ecf_enabled": True,
                "total_fused_events": 0,
                "average_correlation": 0.0,
                "verification_distribution": {},
            }
        
        avg_correlation = sum(e.correlation_score for e in fused_events) / total_events
        
        verification_dist = {}
        for event in fused_events:
            status = event.verification_status
            verification_dist[status] = verification_dist.get(status, 0) + 1
        
        return {
            "ecf_enabled": True,
            "total_fused_events": total_events,
            "average_correlation": avg_correlation,
            "verification_distribution": verification_dist,
            "signal_buffer_size": len(self.ecf_engine.signal_buffer),
        }
    
    def get_fusion_statistics(self) -> Dict[str, Any]:
        """
        Enhanced statistics including ECF metrics
        """
        base_stats = super().get_fusion_statistics()
        ecf_stats = self.get_ecf_statistics()
        
        return {
            **base_stats,
            "ecf_statistics": ecf_stats,
        }


# Example usage
if __name__ == "__main__":
    # Initialize ECF-enhanced Golden Thread
    gt_ecf = GoldenThreadECF(
        enable_ecf=True,
        temporal_window_hours=24.0,
        spatial_threshold_km=50.0,
        min_correlation_score=0.6,
        enable_quantum_weighting=True
    )
    
    # Simulate CBS signal
    cbs_signal = {
        "location": "0.0512,40.3129",  # Dadaab
        "symptom": "diarrhea",
        "timestamp": datetime.utcnow().isoformat(),
        "severity": 0.8,
        "confidence": 0.7,
    }
    
    # Simulate EMR record
    emr_record = {
        "location": "0.0520,40.3135",  # Nearby clinic
        "diagnosis": "cholera",
        "timestamp": (datetime.utcnow() + timedelta(minutes=30)).isoformat(),
        "severity": 0.85,
        "confidence": 0.95,
    }
    
    # Fuse with ECF
    fused_record = gt_ecf.fuse_data_streams(
        cbs_signal=cbs_signal,
        emr_record=emr_record,
        patient_id="PATIENT_12345"
    )
    
    print(f"\n✨ ECF-Enhanced Fusion Complete")
    print(f"   Record ID: {fused_record.record_id}")
    print(f"   Verification Score: {fused_record.verification_score}")
    print(f"   ECF Correlation: {fused_record.canonical_data.get('ecf_correlation_score', 'N/A')}")
    print(f"   Status: {fused_record.canonical_data.get('ecf_verification_status', 'N/A')}")
    
    # Get statistics
    stats = gt_ecf.get_fusion_statistics()
    print(f"\n📊 Fusion Statistics:")
    print(f"   Total Records: {stats['total_records_fused']}")
    print(f"   ECF Enabled: {stats['ecf_statistics']['ecf_enabled']}")
    print(f"   ECF Events: {stats['ecf_statistics']['total_fused_events']}")
    print(f"   Avg Correlation: {stats['ecf_statistics']['average_correlation']:.2f}")
