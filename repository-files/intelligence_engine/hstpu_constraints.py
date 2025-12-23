"""
HSTPU-Bounded Decision Windows
Spatiotemporal constraint protocols for humanitarian decision validity

Compliance:
- WHO IHR (2005) Article 6 (Notification)
- Sphere Standards (Humanitarian Charter)
- UN OCHA Humanitarian Principles
- ISO 22320 (Emergency Management)
"""

import math
from datetime import datetime, timedelta
from typing import Dict, Optional, Tuple, List
from enum import Enum
from dataclasses import dataclass
import logging

logger = logging.getLogger(__name__)


class DecisionStatus(Enum):
    """Decision validity status"""
    VALID = "valid"
    EXPIRED = "expired"
    OUT_OF_BOUNDS = "out_of_bounds"
    REJECTED = "rejected"


class SpatialBoundaryType(Enum):
    """Types of spatial boundaries"""
    OUTBREAK_ZONE = "outbreak_zone"
    REFUGEE_CAMP = "refugee_camp"
    DISTRICT = "district"
    REGION = "region"
    NATIONAL = "national"


@dataclass
class GeospatialPoint:
    """Geographic coordinate"""
    latitude: float
    longitude: float
    
    def __post_init__(self):
        if not -90 <= self.latitude <= 90:
            raise ValueError(f"Invalid latitude: {self.latitude}")
        if not -180 <= self.longitude <= 180:
            raise ValueError(f"Invalid longitude: {self.longitude}")


@dataclass
class SpatiotemporalBounds:
    """Spatiotemporal constraints for decision validity"""
    center: GeospatialPoint
    radius_km: float
    validity_hours: int
    boundary_type: SpatialBoundaryType
    created_at: datetime
    
    def __post_init__(self):
        if self.radius_km <= 0:
            raise ValueError(f"Radius must be positive: {self.radius_km}")
        if self.validity_hours <= 0:
            raise ValueError(f"Validity hours must be positive: {self.validity_hours}")


@dataclass
class HumanitarianDecision:
    """A humanitarian decision with spatiotemporal context"""
    decision_id: str
    decision_type: str
    location: GeospatialPoint
    timestamp: datetime
    bounds: SpatiotemporalBounds
    metadata: Dict
    status: DecisionStatus = DecisionStatus.VALID


class HSTPUConstraintEngine:
    """
    HSTPU-Bounded Decision Windows Engine
    
    Enforces spatiotemporal constraints to ensure decisions remain
    contextually valid in lagged humanitarian environments.
    
    Default constraints:
    - Spatial: 50km radius (outbreak zone boundary)
    - Temporal: 72 hours (humanitarian response window)
    """
    
    # Default HSTPU constraints
    DEFAULT_RADIUS_KM = 50.0  # 50km outbreak zone boundary
    DEFAULT_VALIDITY_HOURS = 72  # 72-hour humanitarian response window
    
    # Earth radius for Haversine calculation
    EARTH_RADIUS_KM = 6371.0
    
    def __init__(
        self,
        default_radius_km: float = DEFAULT_RADIUS_KM,
        default_validity_hours: int = DEFAULT_VALIDITY_HOURS,
        strict_enforcement: bool = True
    ):
        self.default_radius_km = default_radius_km
        self.default_validity_hours = default_validity_hours
        self.strict_enforcement = strict_enforcement
        
        # Decision registry
        self.decisions: Dict[str, HumanitarianDecision] = {}
        
        # Rejection statistics
        self.rejection_stats = {
            "total_decisions": 0,
            "spatial_rejections": 0,
            "temporal_rejections": 0,
            "total_rejections": 0
        }
        
        logger.info(
            f"🌍 HSTPU Constraint Engine initialized - "
            f"Radius: {default_radius_km}km, Validity: {default_validity_hours}h"
        )
    
    def create_decision(
        self,
        decision_id: str,
        decision_type: str,
        location: GeospatialPoint,
        radius_km: Optional[float] = None,
        validity_hours: Optional[int] = None,
        boundary_type: SpatialBoundaryType = SpatialBoundaryType.OUTBREAK_ZONE,
        metadata: Optional[Dict] = None
    ) -> HumanitarianDecision:
        """
        Create a new humanitarian decision with spatiotemporal bounds.
        
        Args:
            decision_id: Unique decision identifier
            decision_type: Type of decision (e.g., "resource_allocation", "evacuation")
            location: Geographic location of decision
            radius_km: Spatial validity radius (default: 50km)
            validity_hours: Temporal validity window (default: 72h)
            boundary_type: Type of spatial boundary
            metadata: Additional decision metadata
        
        Returns:
            HumanitarianDecision with spatiotemporal bounds
        """
        radius_km = radius_km or self.default_radius_km
        validity_hours = validity_hours or self.default_validity_hours
        
        bounds = SpatiotemporalBounds(
            center=location,
            radius_km=radius_km,
            validity_hours=validity_hours,
            boundary_type=boundary_type,
            created_at=datetime.utcnow()
        )
        
        decision = HumanitarianDecision(
            decision_id=decision_id,
            decision_type=decision_type,
            location=location,
            timestamp=datetime.utcnow(),
            bounds=bounds,
            metadata=metadata or {},
            status=DecisionStatus.VALID
        )
        
        self.decisions[decision_id] = decision
        self.rejection_stats["total_decisions"] += 1
        
        logger.info(
            f"✅ Decision created - ID: {decision_id}, "
            f"Type: {decision_type}, Bounds: {radius_km}km/{validity_hours}h"
        )
        
        return decision
    
    def validate_decision(
        self,
        decision_id: str,
        query_location: GeospatialPoint,
        query_time: Optional[datetime] = None
    ) -> Tuple[DecisionStatus, Optional[str]]:
        """
        Validate if a decision is still valid at a given location and time.
        
        Args:
            decision_id: Decision to validate
            query_location: Location to check validity
            query_time: Time to check validity (default: now)
        
        Returns:
            (status, reason) tuple
        """
        if decision_id not in self.decisions:
            return DecisionStatus.REJECTED, f"Decision not found: {decision_id}"
        
        decision = self.decisions[decision_id]
        query_time = query_time or datetime.utcnow()
        
        # Check temporal validity
        time_delta = query_time - decision.timestamp
        if time_delta.total_seconds() / 3600 > decision.bounds.validity_hours:
            decision.status = DecisionStatus.EXPIRED
            self.rejection_stats["temporal_rejections"] += 1
            self.rejection_stats["total_rejections"] += 1
            
            reason = (
                f"Decision expired - Age: {time_delta.total_seconds() / 3600:.1f}h, "
                f"Limit: {decision.bounds.validity_hours}h"
            )
            
            logger.warning(f"⏰ {reason}")
            
            if self.strict_enforcement:
                return DecisionStatus.REJECTED, reason
            return DecisionStatus.EXPIRED, reason
        
        # Check spatial validity
        distance_km = self._haversine_distance(
            decision.bounds.center,
            query_location
        )
        
        if distance_km > decision.bounds.radius_km:
            decision.status = DecisionStatus.OUT_OF_BOUNDS
            self.rejection_stats["spatial_rejections"] += 1
            self.rejection_stats["total_rejections"] += 1
            
            reason = (
                f"Decision out of bounds - Distance: {distance_km:.1f}km, "
                f"Limit: {decision.bounds.radius_km}km"
            )
            
            logger.warning(f"🌍 {reason}")
            
            if self.strict_enforcement:
                return DecisionStatus.REJECTED, reason
            return DecisionStatus.OUT_OF_BOUNDS, reason
        
        # Decision is valid
        logger.info(
            f"✅ Decision valid - ID: {decision_id}, "
            f"Distance: {distance_km:.1f}km, Age: {time_delta.total_seconds() / 3600:.1f}h"
        )
        
        return DecisionStatus.VALID, None
    
    def get_rejection_rate(self) -> float:
        """
        Calculate the rejection rate for decisions.
        
        Returns:
            Rejection rate (0.0 to 1.0)
        """
        if self.rejection_stats["total_decisions"] == 0:
            return 0.0
        
        return (
            self.rejection_stats["total_rejections"] /
            self.rejection_stats["total_decisions"]
        )
    
    def get_active_decisions(
        self,
        location: Optional[GeospatialPoint] = None,
        radius_km: Optional[float] = None
    ) -> List[HumanitarianDecision]:
        """
        Get all active decisions, optionally filtered by location.
        
        Args:
            location: Center point for spatial filter
            radius_km: Radius for spatial filter
        
        Returns:
            List of active decisions
        """
        active = []
        
        for decision in self.decisions.values():
            # Check temporal validity
            age_hours = (datetime.utcnow() - decision.timestamp).total_seconds() / 3600
            if age_hours > decision.bounds.validity_hours:
                continue
            
            # Check spatial filter
            if location and radius_km:
                distance = self._haversine_distance(location, decision.location)
                if distance > radius_km:
                    continue
            
            active.append(decision)
        
        return active
    
    def _haversine_distance(
        self,
        point1: GeospatialPoint,
        point2: GeospatialPoint
    ) -> float:
        """
        Calculate great-circle distance between two points using Haversine formula.
        
        Args:
            point1: First geographic point
            point2: Second geographic point
        
        Returns:
            Distance in kilometers
        """
        # Convert to radians
        lat1 = math.radians(point1.latitude)
        lon1 = math.radians(point1.longitude)
        lat2 = math.radians(point2.latitude)
        lon2 = math.radians(point2.longitude)
        
        # Haversine formula
        dlat = lat2 - lat1
        dlon = lon2 - lon1
        
        a = (
            math.sin(dlat / 2) ** 2 +
            math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2) ** 2
        )
        c = 2 * math.asin(math.sqrt(a))
        
        return self.EARTH_RADIUS_KM * c
    
    def get_statistics(self) -> Dict:
        """Get constraint engine statistics"""
        return {
            "total_decisions": self.rejection_stats["total_decisions"],
            "spatial_rejections": self.rejection_stats["spatial_rejections"],
            "temporal_rejections": self.rejection_stats["temporal_rejections"],
            "total_rejections": self.rejection_stats["total_rejections"],
            "rejection_rate": self.get_rejection_rate(),
            "active_decisions": len(self.get_active_decisions()),
            "default_radius_km": self.default_radius_km,
            "default_validity_hours": self.default_validity_hours
        }


# Example usage
if __name__ == "__main__":
    # Initialize HSTPU engine
    engine = HSTPUConstraintEngine(
        default_radius_km=50.0,
        default_validity_hours=72,
        strict_enforcement=True
    )
    
    # Create decision for Dadaab refugee camp
    dadaab_location = GeospatialPoint(latitude=0.0512, longitude=40.3129)
    
    decision = engine.create_decision(
        decision_id="DEC_001",
        decision_type="resource_allocation",
        location=dadaab_location,
        boundary_type=SpatialBoundaryType.REFUGEE_CAMP,
        metadata={
            "resource": "ORS_supplies",
            "quantity": 10000,
            "priority": "CRITICAL"
        }
    )
    
    print(f"✅ Decision created: {decision.decision_id}")
    
    # Validate at same location (should be valid)
    status, reason = engine.validate_decision(
        "DEC_001",
        dadaab_location
    )
    print(f"Status: {status.value}, Reason: {reason}")
    
    # Validate at distant location (should be rejected)
    nairobi_location = GeospatialPoint(latitude=-1.2921, longitude=36.8219)
    status, reason = engine.validate_decision(
        "DEC_001",
        nairobi_location
    )
    print(f"Status: {status.value}, Reason: {reason}")
    
    # Get statistics
    stats = engine.get_statistics()
    print(f"\n📊 Statistics:")
    print(f"   Total Decisions: {stats['total_decisions']}")
    print(f"   Rejection Rate: {stats['rejection_rate']:.1%}")
    print(f"   Spatial Rejections: {stats['spatial_rejections']}")
    print(f"   Temporal Rejections: {stats['temporal_rejections']}")
