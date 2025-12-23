"""
HSTPU-Bounded Decision Windows
Health Spatiotemporal Processing Unit - Constraint Protocol

Enforces spatiotemporal validity bounds for humanitarian decisions:
- 50km radius constraint (geospatial outbreak boundaries)
- 72-hour validity period (lagged humanitarian environments)
- 100% rejection rate for decisions exceeding bounds

Compliance:
- WHO IHR (2005) Article 6 (Notification)
- Sphere Standards (Humanitarian Charter)
- UN OCHA Cluster Coordination
"""

import math
from datetime import datetime, timedelta
from typing import Dict, Optional, Tuple, List
from enum import Enum
from dataclasses import dataclass
import logging

logger = logging.getLogger(__name__)


class DecisionStatus(Enum):
    """Decision validation status"""
    VALID = "valid"
    EXPIRED = "expired"
    OUT_OF_BOUNDS = "out_of_bounds"
    REJECTED = "rejected"


class OutbreakPhase(Enum):
    """Outbreak phases with different constraint profiles"""
    ALERT = "alert"              # Initial detection
    RESPONSE = "response"        # Active intervention
    CONTAINMENT = "containment"  # Spread control
    RECOVERY = "recovery"        # Post-outbreak


@dataclass
class SpatiotemporalBounds:
    """Spatiotemporal constraint configuration"""
    radius_km: float = 50.0      # Default: 50km radius
    validity_hours: int = 72     # Default: 72-hour validity
    strict_enforcement: bool = True
    
    # Phase-specific overrides
    phase_overrides: Dict[OutbreakPhase, Tuple[float, int]] = None
    
    def __post_init__(self):
        if self.phase_overrides is None:
            self.phase_overrides = {
                OutbreakPhase.ALERT: (100.0, 48),      # Wider radius, shorter validity
                OutbreakPhase.RESPONSE: (50.0, 72),    # Standard bounds
                OutbreakPhase.CONTAINMENT: (25.0, 96), # Tighter radius, longer validity
                OutbreakPhase.RECOVERY: (75.0, 168),   # Wider radius, week-long validity
            }


@dataclass
class GeospatialPoint:
    """Geographic coordinate"""
    latitude: float
    longitude: float
    timestamp: datetime
    
    def __post_init__(self):
        # Validate coordinates
        if not (-90 <= self.latitude <= 90):
            raise ValueError(f"Invalid latitude: {self.latitude}")
        if not (-180 <= self.longitude <= 180):
            raise ValueError(f"Invalid longitude: {self.longitude}")


@dataclass
class HumanitarianDecision:
    """Humanitarian decision with spatiotemporal context"""
    decision_id: str
    decision_type: str
    location: GeospatialPoint
    created_at: datetime
    expires_at: datetime
    outbreak_phase: OutbreakPhase
    metadata: Dict
    
    # Validation results
    is_valid: bool = True
    validation_status: DecisionStatus = DecisionStatus.VALID
    rejection_reason: Optional[str] = None


class HSTPUConstraintEngine:
    """
    Health Spatiotemporal Processing Unit - Constraint Engine
    
    Enforces spatiotemporal validity bounds for humanitarian decisions
    to ensure contextual relevance in lagged environments.
    """
    
    def __init__(
        self,
        bounds: Optional[SpatiotemporalBounds] = None,
        enable_audit: bool = True
    ):
        self.bounds = bounds or SpatiotemporalBounds()
        self.enable_audit = enable_audit
        
        # Audit trail
        self.audit_log: List[Dict] = []
        
        # Statistics
        self.stats = {
            "total_decisions": 0,
            "valid_decisions": 0,
            "expired_decisions": 0,
            "out_of_bounds_decisions": 0,
            "rejected_decisions": 0,
        }
        
        logger.info(f"🌍 HSTPU Constraint Engine initialized - Radius: {self.bounds.radius_km}km, Validity: {self.bounds.validity_hours}h")
    
    def haversine_distance(
        self,
        point1: GeospatialPoint,
        point2: GeospatialPoint
    ) -> float:
        """
        Calculate great-circle distance between two points using Haversine formula.
        
        Returns:
            Distance in kilometers
        """
        # Earth radius in kilometers
        R = 6371.0
        
        # Convert to radians
        lat1 = math.radians(point1.latitude)
        lon1 = math.radians(point1.longitude)
        lat2 = math.radians(point2.latitude)
        lon2 = math.radians(point2.longitude)
        
        # Haversine formula
        dlat = lat2 - lat1
        dlon = lon2 - lon1
        
        a = math.sin(dlat / 2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2)**2
        c = 2 * math.asin(math.sqrt(a))
        
        distance = R * c
        return distance
    
    def validate_temporal_bounds(
        self,
        decision: HumanitarianDecision,
        current_time: Optional[datetime] = None
    ) -> Tuple[bool, Optional[str]]:
        """
        Validate temporal bounds (72-hour validity period).
        
        Returns:
            (is_valid, rejection_reason)
        """
        current_time = current_time or datetime.utcnow()
        
        # Check if decision has expired
        if current_time > decision.expires_at:
            time_delta = current_time - decision.expires_at
            return False, f"Decision expired {time_delta.total_seconds() / 3600:.1f} hours ago"
        
        # Check if decision is too far in the future (sanity check)
        max_future = current_time + timedelta(days=30)
        if decision.expires_at > max_future:
            return False, f"Decision expiration too far in future: {decision.expires_at}"
        
        return True, None
    
    def validate_spatial_bounds(
        self,
        decision: HumanitarianDecision,
        reference_point: GeospatialPoint
    ) -> Tuple[bool, Optional[str]]:
        """
        Validate spatial bounds (50km radius constraint).
        
        Returns:
            (is_valid, rejection_reason)
        """
        # Get phase-specific bounds
        radius_km, _ = self.bounds.phase_overrides.get(
            decision.outbreak_phase,
            (self.bounds.radius_km, self.bounds.validity_hours)
        )
        
        # Calculate distance
        distance = self.haversine_distance(decision.location, reference_point)
        
        # Check if within bounds
        if distance > radius_km:
            return False, f"Decision location {distance:.1f}km from reference (max: {radius_km}km)"
        
        return True, None
    
    def validate_decision(
        self,
        decision: HumanitarianDecision,
        reference_point: GeospatialPoint,
        current_time: Optional[datetime] = None
    ) -> HumanitarianDecision:
        """
        Validate a humanitarian decision against spatiotemporal constraints.
        
        Enforces:
        - 50km radius constraint (geospatial outbreak boundaries)
        - 72-hour validity period (lagged humanitarian environments)
        - 100% rejection rate for decisions exceeding bounds
        
        Args:
            decision: Decision to validate
            reference_point: Reference location (e.g., outbreak epicenter)
            current_time: Current timestamp (default: now)
        
        Returns:
            Updated decision with validation results
        """
        current_time = current_time or datetime.utcnow()
        
        self.stats["total_decisions"] += 1
        
        # Validate temporal bounds
        temporal_valid, temporal_reason = self.validate_temporal_bounds(decision, current_time)
        
        if not temporal_valid:
            decision.is_valid = False
            decision.validation_status = DecisionStatus.EXPIRED
            decision.rejection_reason = temporal_reason
            self.stats["expired_decisions"] += 1
            
            if self.enable_audit:
                self._log_audit("TEMPORAL_REJECTION", decision, temporal_reason)
            
            logger.warning(f"⏰ Decision {decision.decision_id} EXPIRED: {temporal_reason}")
            return decision
        
        # Validate spatial bounds
        spatial_valid, spatial_reason = self.validate_spatial_bounds(decision, reference_point)
        
        if not spatial_valid:
            decision.is_valid = False
            decision.validation_status = DecisionStatus.OUT_OF_BOUNDS
            decision.rejection_reason = spatial_reason
            self.stats["out_of_bounds_decisions"] += 1
            
            if self.enable_audit:
                self._log_audit("SPATIAL_REJECTION", decision, spatial_reason)
            
            logger.warning(f"🌍 Decision {decision.decision_id} OUT OF BOUNDS: {spatial_reason}")
            return decision
        
        # Decision is valid
        decision.is_valid = True
        decision.validation_status = DecisionStatus.VALID
        self.stats["valid_decisions"] += 1
        
        if self.enable_audit:
            self._log_audit("VALIDATED", decision, "Decision within spatiotemporal bounds")
        
        logger.info(f"✅ Decision {decision.decision_id} VALID")
        return decision
    
    def create_decision(
        self,
        decision_id: str,
        decision_type: str,
        location: GeospatialPoint,
        outbreak_phase: OutbreakPhase = OutbreakPhase.RESPONSE,
        metadata: Optional[Dict] = None
    ) -> HumanitarianDecision:
        """
        Create a new humanitarian decision with automatic expiration.
        
        Args:
            decision_id: Unique decision identifier
            decision_type: Type of decision (e.g., "resource_allocation", "evacuation")
            location: Decision location
            outbreak_phase: Current outbreak phase
            metadata: Additional metadata
        
        Returns:
            New humanitarian decision
        """
        # Get phase-specific bounds
        _, validity_hours = self.bounds.phase_overrides.get(
            outbreak_phase,
            (self.bounds.radius_km, self.bounds.validity_hours)
        )
        
        created_at = datetime.utcnow()
        expires_at = created_at + timedelta(hours=validity_hours)
        
        decision = HumanitarianDecision(
            decision_id=decision_id,
            decision_type=decision_type,
            location=location,
            created_at=created_at,
            expires_at=expires_at,
            outbreak_phase=outbreak_phase,
            metadata=metadata or {}
        )
        
        logger.info(f"📋 Created decision {decision_id} - Expires: {expires_at} ({validity_hours}h)")
        return decision
    
    def batch_validate(
        self,
        decisions: List[HumanitarianDecision],
        reference_point: GeospatialPoint,
        current_time: Optional[datetime] = None
    ) -> List[HumanitarianDecision]:
        """
        Validate multiple decisions in batch.
        
        Returns:
            List of validated decisions
        """
        validated = []
        
        for decision in decisions:
            validated_decision = self.validate_decision(decision, reference_point, current_time)
            validated.append(validated_decision)
        
        # Log batch statistics
        valid_count = sum(1 for d in validated if d.is_valid)
        invalid_count = len(validated) - valid_count
        
        logger.info(f"📊 Batch validation complete - Valid: {valid_count}, Invalid: {invalid_count}")
        
        return validated
    
    def get_statistics(self) -> Dict:
        """Get validation statistics"""
        total = self.stats["total_decisions"]
        
        if total == 0:
            return self.stats
        
        return {
            **self.stats,
            "valid_rate": self.stats["valid_decisions"] / total,
            "expired_rate": self.stats["expired_decisions"] / total,
            "out_of_bounds_rate": self.stats["out_of_bounds_decisions"] / total,
            "rejection_rate": (self.stats["expired_decisions"] + self.stats["out_of_bounds_decisions"]) / total,
        }
    
    def _log_audit(self, action: str, decision: HumanitarianDecision, reason: str):
        """Internal audit logging"""
        audit_entry = {
            "timestamp": datetime.utcnow().isoformat(),
            "action": action,
            "decision_id": decision.decision_id,
            "decision_type": decision.decision_type,
            "location": {
                "lat": decision.location.latitude,
                "lng": decision.location.longitude
            },
            "outbreak_phase": decision.outbreak_phase.value,
            "validation_status": decision.validation_status.value,
            "reason": reason
        }
        self.audit_log.append(audit_entry)


# Example usage
if __name__ == "__main__":
    # Initialize HSTPU Constraint Engine
    engine = HSTPUConstraintEngine()
    
    # Define outbreak epicenter (Dadaab, Kenya)
    epicenter = GeospatialPoint(
        latitude=0.0512,
        longitude=40.3129,
        timestamp=datetime.utcnow()
    )
    
    # Create decision within bounds
    decision_valid = engine.create_decision(
        decision_id="DEC_001",
        decision_type="resource_allocation",
        location=GeospatialPoint(
            latitude=0.0600,  # ~10km from epicenter
            longitude=40.3200,
            timestamp=datetime.utcnow()
        ),
        outbreak_phase=OutbreakPhase.RESPONSE,
        metadata={"resource": "ORS", "quantity": 1000}
    )
    
    # Validate decision
    validated = engine.validate_decision(decision_valid, epicenter)
    print(f"✅ Decision {validated.decision_id}: {validated.validation_status.value}")
    
    # Create decision out of bounds
    decision_invalid = engine.create_decision(
        decision_id="DEC_002",
        decision_type="evacuation",
        location=GeospatialPoint(
            latitude=1.0000,  # ~100km from epicenter
            longitude=41.0000,
            timestamp=datetime.utcnow()
        ),
        outbreak_phase=OutbreakPhase.RESPONSE
    )
    
    # Validate decision (should be rejected)
    validated_invalid = engine.validate_decision(decision_invalid, epicenter)
    print(f"❌ Decision {validated_invalid.decision_id}: {validated_invalid.validation_status.value}")
    print(f"   Reason: {validated_invalid.rejection_reason}")
    
    # Get statistics
    stats = engine.get_statistics()
    print(f"\n📊 Statistics:")
    print(f"   Total: {stats['total_decisions']}")
    print(f"   Valid: {stats['valid_decisions']}")
    print(f"   Rejection Rate: {stats['rejection_rate']:.1%}")
