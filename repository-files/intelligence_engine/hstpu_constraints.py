"""
HSTPU-Bounded Decision Windows
Spatiotemporal constraint protocols for humanitarian decision validity

Enforces:
- 50km radius spatial constraint
- 72-hour temporal validity window
- 100% rejection for out-of-bounds decisions
- Geospatial outbreak boundary alignment

Compliance:
- WHO IHR (2005) Article 6 (Notification)
- Sphere Standards (Humanitarian Charter)
- UN OCHA Humanitarian Principles
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
    """Outbreak progression phases"""
    ALERT = "alert"
    RESPONSE = "response"
    CONTAINMENT = "containment"
    RECOVERY = "recovery"


@dataclass
class SpatiotemporalBounds:
    """Spatiotemporal constraint boundaries"""
    center_lat: float
    center_lng: float
    radius_km: float = 50.0  # Default 50km radius
    validity_hours: int = 72  # Default 72-hour window
    created_at: datetime = None
    
    def __post_init__(self):
        if self.created_at is None:
            self.created_at = datetime.utcnow()


@dataclass
class Decision:
    """Humanitarian decision with spatiotemporal context"""
    decision_id: str
    decision_type: str
    location: Tuple[float, float]  # (lat, lng)
    timestamp: datetime
    outbreak_phase: OutbreakPhase
    confidence_score: float
    metadata: Dict
    
    # Spatiotemporal validation
    bounds: Optional[SpatiotemporalBounds] = None
    status: DecisionStatus = DecisionStatus.VALID


class HSTPUConstraints:
    """
    Health Spatiotemporal Processing Unit (HSTPU) Constraints
    
    Enforces spatiotemporal validity for humanitarian decisions in
    lagged environments where connectivity and data freshness vary.
    """
    
    # Hard-coded constraints (immutable)
    DEFAULT_RADIUS_KM = 50.0
    DEFAULT_VALIDITY_HOURS = 72
    EARTH_RADIUS_KM = 6371.0
    
    def __init__(
        self,
        enable_strict_mode: bool = True,
        enable_audit: bool = True
    ):
        self.enable_strict_mode = enable_strict_mode
        self.enable_audit = enable_audit
        
        # Audit trail
        self.audit_log = []
        
        # Rejection statistics
        self.stats = {
            "total_decisions": 0,
            "valid_decisions": 0,
            "expired_decisions": 0,
            "out_of_bounds_decisions": 0,
            "rejected_decisions": 0
        }
        
        logger.info(f"🌍 HSTPU Constraints initialized - Strict Mode: {enable_strict_mode}")
    
    def create_bounds(
        self,
        center_lat: float,
        center_lng: float,
        radius_km: float = None,
        validity_hours: int = None
    ) -> SpatiotemporalBounds:
        """
        Create spatiotemporal bounds for a decision context.
        
        Args:
            center_lat: Center latitude
            center_lng: Center longitude
            radius_km: Spatial radius (default: 50km)
            validity_hours: Temporal validity (default: 72h)
        
        Returns:
            SpatiotemporalBounds object
        """
        return SpatiotemporalBounds(
            center_lat=center_lat,
            center_lng=center_lng,
            radius_km=radius_km or self.DEFAULT_RADIUS_KM,
            validity_hours=validity_hours or self.DEFAULT_VALIDITY_HOURS
        )
    
    def haversine_distance(
        self,
        lat1: float,
        lng1: float,
        lat2: float,
        lng2: float
    ) -> float:
        """
        Calculate great-circle distance between two points using Haversine formula.
        
        Args:
            lat1, lng1: First point coordinates
            lat2, lng2: Second point coordinates
        
        Returns:
            Distance in kilometers
        """
        # Convert to radians
        lat1_rad = math.radians(lat1)
        lng1_rad = math.radians(lng1)
        lat2_rad = math.radians(lat2)
        lng2_rad = math.radians(lng2)
        
        # Haversine formula
        dlat = lat2_rad - lat1_rad
        dlng = lng2_rad - lng1_rad
        
        a = (math.sin(dlat / 2) ** 2 +
             math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(dlng / 2) ** 2)
        c = 2 * math.asin(math.sqrt(a))
        
        distance_km = self.EARTH_RADIUS_KM * c
        return distance_km
    
    def validate_spatial_bounds(
        self,
        decision: Decision,
        bounds: SpatiotemporalBounds
    ) -> Tuple[bool, float]:
        """
        Validate decision is within spatial bounds.
        
        Args:
            decision: Decision to validate
            bounds: Spatiotemporal bounds
        
        Returns:
            (is_valid, distance_km)
        """
        lat, lng = decision.location
        
        distance_km = self.haversine_distance(
            lat, lng,
            bounds.center_lat, bounds.center_lng
        )
        
        is_valid = distance_km <= bounds.radius_km
        
        return is_valid, distance_km
    
    def validate_temporal_bounds(
        self,
        decision: Decision,
        bounds: SpatiotemporalBounds
    ) -> Tuple[bool, float]:
        """
        Validate decision is within temporal bounds.
        
        Args:
            decision: Decision to validate
            bounds: Spatiotemporal bounds
        
        Returns:
            (is_valid, age_hours)
        """
        age = datetime.utcnow() - decision.timestamp
        age_hours = age.total_seconds() / 3600
        
        is_valid = age_hours <= bounds.validity_hours
        
        return is_valid, age_hours
    
    def validate_decision(
        self,
        decision: Decision,
        bounds: SpatiotemporalBounds
    ) -> Dict:
        """
        Validate decision against spatiotemporal bounds.
        
        100% rejection rate for out-of-bounds decisions in strict mode.
        
        Args:
            decision: Decision to validate
            bounds: Spatiotemporal bounds
        
        Returns:
            Validation result with status and metrics
        """
        self.stats["total_decisions"] += 1
        
        # Validate spatial bounds
        spatial_valid, distance_km = self.validate_spatial_bounds(decision, bounds)
        
        # Validate temporal bounds
        temporal_valid, age_hours = self.validate_temporal_bounds(decision, bounds)
        
        # Determine status
        if not temporal_valid:
            status = DecisionStatus.EXPIRED
            self.stats["expired_decisions"] += 1
        elif not spatial_valid:
            status = DecisionStatus.OUT_OF_BOUNDS
            self.stats["out_of_bounds_decisions"] += 1
        else:
            status = DecisionStatus.VALID
            self.stats["valid_decisions"] += 1
        
        # Strict mode: 100% rejection for invalid decisions
        if self.enable_strict_mode and status != DecisionStatus.VALID:
            status = DecisionStatus.REJECTED
            self.stats["rejected_decisions"] += 1
        
        # Update decision status
        decision.status = status
        decision.bounds = bounds
        
        # Build result
        result = {
            "decision_id": decision.decision_id,
            "status": status.value,
            "spatial_valid": spatial_valid,
            "temporal_valid": temporal_valid,
            "distance_km": round(distance_km, 2),
            "age_hours": round(age_hours, 2),
            "bounds": {
                "center": (bounds.center_lat, bounds.center_lng),
                "radius_km": bounds.radius_km,
                "validity_hours": bounds.validity_hours
            },
            "strict_mode": self.enable_strict_mode
        }
        
        # Audit log
        if self.enable_audit:
            self._log_audit(decision, result)
        
        # Log validation
        if status == DecisionStatus.VALID:
            logger.info(f"✅ Decision {decision.decision_id} VALID - "
                       f"Distance: {distance_km:.2f}km, Age: {age_hours:.2f}h")
        else:
            logger.warning(f"❌ Decision {decision.decision_id} {status.value.upper()} - "
                          f"Distance: {distance_km:.2f}km, Age: {age_hours:.2f}h")
        
        return result
    
    def validate_outbreak_boundary(
        self,
        decision: Decision,
        outbreak_center: Tuple[float, float],
        outbreak_radius_km: float
    ) -> Dict:
        """
        Validate decision aligns with geospatial outbreak boundaries.
        
        Args:
            decision: Decision to validate
            outbreak_center: Outbreak epicenter (lat, lng)
            outbreak_radius_km: Outbreak radius
        
        Returns:
            Validation result
        """
        lat, lng = decision.location
        center_lat, center_lng = outbreak_center
        
        distance_km = self.haversine_distance(lat, lng, center_lat, center_lng)
        
        is_within_outbreak = distance_km <= outbreak_radius_km
        
        result = {
            "decision_id": decision.decision_id,
            "within_outbreak_boundary": is_within_outbreak,
            "distance_from_epicenter_km": round(distance_km, 2),
            "outbreak_radius_km": outbreak_radius_km,
            "outbreak_center": outbreak_center
        }
        
        if is_within_outbreak:
            logger.info(f"✅ Decision {decision.decision_id} within outbreak boundary - "
                       f"Distance from epicenter: {distance_km:.2f}km")
        else:
            logger.warning(f"⚠️ Decision {decision.decision_id} outside outbreak boundary - "
                          f"Distance from epicenter: {distance_km:.2f}km")
        
        return result
    
    def get_rejection_rate(self) -> float:
        """Calculate rejection rate"""
        if self.stats["total_decisions"] == 0:
            return 0.0
        
        return self.stats["rejected_decisions"] / self.stats["total_decisions"]
    
    def get_statistics(self) -> Dict:
        """Get validation statistics"""
        total = self.stats["total_decisions"]
        
        if total == 0:
            return {**self.stats, "rejection_rate": 0.0}
        
        return {
            **self.stats,
            "rejection_rate": round(self.get_rejection_rate(), 4),
            "valid_rate": round(self.stats["valid_decisions"] / total, 4),
            "expired_rate": round(self.stats["expired_decisions"] / total, 4),
            "out_of_bounds_rate": round(self.stats["out_of_bounds_decisions"] / total, 4)
        }
    
    def _log_audit(self, decision: Decision, result: Dict):
        """Internal audit logging"""
        audit_entry = {
            "timestamp": datetime.utcnow().isoformat(),
            "decision_id": decision.decision_id,
            "decision_type": decision.decision_type,
            "status": result["status"],
            "spatial_valid": result["spatial_valid"],
            "temporal_valid": result["temporal_valid"],
            "distance_km": result["distance_km"],
            "age_hours": result["age_hours"]
        }
        self.audit_log.append(audit_entry)


# Example usage
if __name__ == "__main__":
    # Initialize HSTPU Constraints
    hstpu = HSTPUConstraints(enable_strict_mode=True)
    
    # Create spatiotemporal bounds for Dadaab refugee camp
    bounds = hstpu.create_bounds(
        center_lat=0.0512,
        center_lng=40.3129,
        radius_km=50.0,
        validity_hours=72
    )
    
    # Decision 1: Valid (within bounds)
    decision1 = Decision(
        decision_id="DEC_001",
        decision_type="cholera_response",
        location=(0.0600, 40.3200),  # ~10km from center
        timestamp=datetime.utcnow() - timedelta(hours=24),
        outbreak_phase=OutbreakPhase.RESPONSE,
        confidence_score=0.92,
        metadata={"priority": "high"}
    )
    
    result1 = hstpu.validate_decision(decision1, bounds)
    print(f"\n✅ Decision 1: {result1['status']}")
    print(f"   Distance: {result1['distance_km']}km, Age: {result1['age_hours']}h")
    
    # Decision 2: Expired (>72 hours old)
    decision2 = Decision(
        decision_id="DEC_002",
        decision_type="malaria_surveillance",
        location=(0.0550, 40.3150),
        timestamp=datetime.utcnow() - timedelta(hours=80),
        outbreak_phase=OutbreakPhase.ALERT,
        confidence_score=0.85,
        metadata={"priority": "medium"}
    )
    
    result2 = hstpu.validate_decision(decision2, bounds)
    print(f"\n❌ Decision 2: {result2['status']}")
    print(f"   Distance: {result2['distance_km']}km, Age: {result2['age_hours']}h")
    
    # Decision 3: Out of bounds (>50km)
    decision3 = Decision(
        decision_id="DEC_003",
        decision_type="emergency_response",
        location=(0.5000, 40.8000),  # ~70km from center
        timestamp=datetime.utcnow() - timedelta(hours=12),
        outbreak_phase=OutbreakPhase.CONTAINMENT,
        confidence_score=0.78,
        metadata={"priority": "critical"}
    )
    
    result3 = hstpu.validate_decision(decision3, bounds)
    print(f"\n❌ Decision 3: {result3['status']}")
    print(f"   Distance: {result3['distance_km']}km, Age: {result3['age_hours']}h")
    
    # Validate outbreak boundary alignment
    outbreak_result = hstpu.validate_outbreak_boundary(
        decision1,
        outbreak_center=(0.0512, 40.3129),
        outbreak_radius_km=30.0
    )
    print(f"\n🌍 Outbreak Boundary: {outbreak_result['within_outbreak_boundary']}")
    
    # Statistics
    stats = hstpu.get_statistics()
    print(f"\n📊 HSTPU Statistics:")
    print(f"   Total Decisions: {stats['total_decisions']}")
    print(f"   Valid: {stats['valid_decisions']} ({stats['valid_rate']:.1%})")
    print(f"   Rejected: {stats['rejected_decisions']} ({stats['rejection_rate']:.1%})")
    print(f"   Expired: {stats['expired_decisions']} ({stats['expired_rate']:.1%})")
    print(f"   Out of Bounds: {stats['out_of_bounds_decisions']} ({stats['out_of_bounds_rate']:.1%})")
