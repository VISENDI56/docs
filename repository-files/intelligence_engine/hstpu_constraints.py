"""
HSTPU-Bounded Decision Windows
Spatiotemporal constraint protocols for humanitarian decision validity

Ensures decisions remain contextually valid in lagged humanitarian environments
by enforcing strict spatial (50km radius) and temporal (72-hour) bounds.

Compliance:
- WHO IHR (2005) Article 6 (Notification)
- Sphere Standards (Humanitarian Charter)
- UN OCHA Humanitarian Principles
"""

import math
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
from enum import Enum
from dataclasses import dataclass
import logging

logger = logging.getLogger(__name__)


class DecisionStatus(Enum):
    """Decision validity status"""
    VALID = "valid"
    EXPIRED_TEMPORAL = "expired_temporal"
    EXPIRED_SPATIAL = "expired_spatial"
    EXPIRED_BOTH = "expired_both"
    REJECTED = "rejected"


class HumanitarianContext(Enum):
    """Humanitarian operational contexts"""
    REFUGEE_CAMP = "refugee_camp"
    CONFLICT_ZONE = "conflict_zone"
    NATURAL_DISASTER = "natural_disaster"
    DISEASE_OUTBREAK = "disease_outbreak"
    ROUTINE_SURVEILLANCE = "routine_surveillance"


@dataclass
class GeospatialBounds:
    """Geospatial boundary definition"""
    center_lat: float
    center_lng: float
    radius_km: float = 50.0  # Default HSTPU bound
    
    def contains_point(self, lat: float, lng: float) -> bool:
        """Check if point is within bounds using Haversine formula"""
        distance_km = self._haversine_distance(
            self.center_lat, self.center_lng, lat, lng
        )
        return distance_km <= self.radius_km
    
    @staticmethod
    def _haversine_distance(lat1: float, lng1: float, lat2: float, lng2: float) -> float:
        """Calculate distance between two points in km"""
        R = 6371  # Earth radius in km
        
        lat1_rad = math.radians(lat1)
        lat2_rad = math.radians(lat2)
        delta_lat = math.radians(lat2 - lat1)
        delta_lng = math.radians(lng2 - lng1)
        
        a = (math.sin(delta_lat / 2) ** 2 +
             math.cos(lat1_rad) * math.cos(lat2_rad) *
             math.sin(delta_lng / 2) ** 2)
        c = 2 * math.asin(math.sqrt(a))
        
        return R * c


@dataclass
class TemporalBounds:
    """Temporal validity window"""
    created_at: datetime
    validity_hours: float = 72.0  # Default HSTPU bound
    
    def is_valid(self, check_time: Optional[datetime] = None) -> bool:
        """Check if decision is still temporally valid"""
        if check_time is None:
            check_time = datetime.utcnow()
        
        expiration = self.created_at + timedelta(hours=self.validity_hours)
        return check_time <= expiration
    
    def time_remaining(self, check_time: Optional[datetime] = None) -> timedelta:
        """Get remaining validity time"""
        if check_time is None:
            check_time = datetime.utcnow()
        
        expiration = self.created_at + timedelta(hours=self.validity_hours)
        remaining = expiration - check_time
        return remaining if remaining.total_seconds() > 0 else timedelta(0)


@dataclass
class HumanitarianDecision:
    """Humanitarian decision with spatiotemporal bounds"""
    decision_id: str
    decision_type: str
    context: HumanitarianContext
    geospatial_bounds: GeospatialBounds
    temporal_bounds: TemporalBounds
    metadata: Dict
    
    def validate(
        self,
        current_location: Tuple[float, float],
        check_time: Optional[datetime] = None
    ) -> Tuple[DecisionStatus, str]:
        """
        Validate decision against spatiotemporal constraints.
        
        Returns:
            (status, reason)
        """
        lat, lng = current_location
        
        # Check temporal validity
        temporal_valid = self.temporal_bounds.is_valid(check_time)
        
        # Check spatial validity
        spatial_valid = self.geospatial_bounds.contains_point(lat, lng)
        
        # Determine status
        if temporal_valid and spatial_valid:
            return DecisionStatus.VALID, "Decision is valid"
        elif not temporal_valid and not spatial_valid:
            return DecisionStatus.EXPIRED_BOTH, "Decision expired (temporal and spatial)"
        elif not temporal_valid:
            return DecisionStatus.EXPIRED_TEMPORAL, "Decision expired (temporal)"
        else:
            return DecisionStatus.EXPIRED_SPATIAL, "Decision expired (spatial)"


class HSTPUConstraintEngine:
    """
    HSTPU-Bounded Decision Windows Engine
    
    Enforces 50km spatial radius and 72-hour temporal validity for all
    humanitarian decisions to ensure contextual relevance in lagged environments.
    """
    
    def __init__(
        self,
        default_radius_km: float = 50.0,
        default_validity_hours: float = 72.0,
        strict_mode: bool = True
    ):
        """
        Initialize HSTPU Constraint Engine.
        
        Args:
            default_radius_km: Default spatial radius (50km HSTPU standard)
            default_validity_hours: Default temporal validity (72h HSTPU standard)
            strict_mode: If True, 100% rejection for violations
        """
        self.default_radius_km = default_radius_km
        self.default_validity_hours = default_validity_hours
        self.strict_mode = strict_mode
        
        # Decision registry
        self.active_decisions: Dict[str, HumanitarianDecision] = {}
        
        # Metrics
        self.metrics = {
            "decisions_created": 0,
            "decisions_validated": 0,
            "decisions_rejected_temporal": 0,
            "decisions_rejected_spatial": 0,
            "decisions_rejected_both": 0,
        }
        
        logger.info(
            f"🌍 HSTPU Constraint Engine initialized - "
            f"Radius: {default_radius_km}km, Validity: {default_validity_hours}h, "
            f"Strict: {strict_mode}"
        )
    
    def create_decision(
        self,
        decision_id: str,
        decision_type: str,
        context: HumanitarianContext,
        center_location: Tuple[float, float],
        metadata: Optional[Dict] = None,
        custom_radius_km: Optional[float] = None,
        custom_validity_hours: Optional[float] = None
    ) -> HumanitarianDecision:
        """
        Create a new humanitarian decision with spatiotemporal bounds.
        
        Args:
            decision_id: Unique decision identifier
            decision_type: Type of decision (e.g., "outbreak_response")
            context: Humanitarian context
            center_location: (lat, lng) center point
            metadata: Additional metadata
            custom_radius_km: Override default radius
            custom_validity_hours: Override default validity
        
        Returns:
            HumanitarianDecision object
        """
        lat, lng = center_location
        
        # Create geospatial bounds
        geospatial_bounds = GeospatialBounds(
            center_lat=lat,
            center_lng=lng,
            radius_km=custom_radius_km or self.default_radius_km
        )
        
        # Create temporal bounds
        temporal_bounds = TemporalBounds(
            created_at=datetime.utcnow(),
            validity_hours=custom_validity_hours or self.default_validity_hours
        )
        
        # Create decision
        decision = HumanitarianDecision(
            decision_id=decision_id,
            decision_type=decision_type,
            context=context,
            geospatial_bounds=geospatial_bounds,
            temporal_bounds=temporal_bounds,
            metadata=metadata or {}
        )
        
        # Register decision
        self.active_decisions[decision_id] = decision
        self.metrics["decisions_created"] += 1
        
        logger.info(
            f"✅ Decision created: {decision_id} - "
            f"Type: {decision_type}, Context: {context.value}, "
            f"Location: ({lat:.4f}, {lng:.4f}), "
            f"Radius: {geospatial_bounds.radius_km}km, "
            f"Validity: {temporal_bounds.validity_hours}h"
        )
        
        return decision
    
    def validate_decision(
        self,
        decision_id: str,
        current_location: Tuple[float, float],
        check_time: Optional[datetime] = None
    ) -> Tuple[bool, DecisionStatus, str]:
        """
        Validate a decision against spatiotemporal constraints.
        
        Args:
            decision_id: Decision to validate
            current_location: Current (lat, lng) location
            check_time: Time to check validity (default: now)
        
        Returns:
            (is_valid, status, reason)
        """
        if decision_id not in self.active_decisions:
            return False, DecisionStatus.REJECTED, "Decision not found"
        
        decision = self.active_decisions[decision_id]
        status, reason = decision.validate(current_location, check_time)
        
        self.metrics["decisions_validated"] += 1
        
        # Update rejection metrics
        if status == DecisionStatus.EXPIRED_TEMPORAL:
            self.metrics["decisions_rejected_temporal"] += 1
        elif status == DecisionStatus.EXPIRED_SPATIAL:
            self.metrics["decisions_rejected_spatial"] += 1
        elif status == DecisionStatus.EXPIRED_BOTH:
            self.metrics["decisions_rejected_both"] += 1
        
        # Strict mode: 100% rejection for violations
        is_valid = status == DecisionStatus.VALID
        
        if not is_valid and self.strict_mode:
            logger.warning(
                f"❌ Decision REJECTED: {decision_id} - "
                f"Status: {status.value}, Reason: {reason}"
            )
        elif is_valid:
            logger.info(
                f"✅ Decision VALID: {decision_id} - "
                f"Location: {current_location}, Time remaining: "
                f"{decision.temporal_bounds.time_remaining()}"
            )
        
        return is_valid, status, reason
    
    def get_rejection_rate(self) -> float:
        """Calculate rejection rate for violations"""
        total_validations = self.metrics["decisions_validated"]
        if total_validations == 0:
            return 0.0
        
        total_rejections = (
            self.metrics["decisions_rejected_temporal"] +
            self.metrics["decisions_rejected_spatial"] +
            self.metrics["decisions_rejected_both"]
        )
        
        return total_rejections / total_validations
    
    def get_active_decisions(
        self,
        context: Optional[HumanitarianContext] = None
    ) -> List[HumanitarianDecision]:
        """Get all active decisions, optionally filtered by context"""
        decisions = list(self.active_decisions.values())
        
        if context:
            decisions = [d for d in decisions if d.context == context]
        
        return decisions
    
    def cleanup_expired_decisions(self) -> int:
        """Remove expired decisions from registry"""
        now = datetime.utcnow()
        expired_ids = []
        
        for decision_id, decision in self.active_decisions.items():
            if not decision.temporal_bounds.is_valid(now):
                expired_ids.append(decision_id)
        
        for decision_id in expired_ids:
            del self.active_decisions[decision_id]
        
        logger.info(f"🧹 Cleaned up {len(expired_ids)} expired decisions")
        return len(expired_ids)
    
    def get_metrics(self) -> Dict:
        """Get engine metrics"""
        return {
            **self.metrics,
            "active_decisions": len(self.active_decisions),
            "rejection_rate": self.get_rejection_rate()
        }


# Example usage
if __name__ == "__main__":
    # Initialize engine
    engine = HSTPUConstraintEngine(strict_mode=True)
    
    # Create outbreak response decision for Dadaab
    decision = engine.create_decision(
        decision_id="OUTBREAK_DADAAB_001",
        decision_type="cholera_response",
        context=HumanitarianContext.DISEASE_OUTBREAK,
        center_location=(0.0512, 40.3129),  # Dadaab coordinates
        metadata={
            "disease": "cholera",
            "severity": "high",
            "population_at_risk": 200000
        }
    )
    
    # Validate within bounds (should pass)
    is_valid, status, reason = engine.validate_decision(
        decision_id="OUTBREAK_DADAAB_001",
        current_location=(0.0600, 40.3200)  # ~10km away
    )
    print(f"✅ Validation 1: {is_valid} - {reason}")
    
    # Validate outside spatial bounds (should fail)
    is_valid, status, reason = engine.validate_decision(
        decision_id="OUTBREAK_DADAAB_001",
        current_location=(0.5000, 40.8000)  # ~60km away
    )
    print(f"❌ Validation 2: {is_valid} - {reason}")
    
    # Validate outside temporal bounds (should fail)
    future_time = datetime.utcnow() + timedelta(hours=80)
    is_valid, status, reason = engine.validate_decision(
        decision_id="OUTBREAK_DADAAB_001",
        current_location=(0.0600, 40.3200),
        check_time=future_time
    )
    print(f"❌ Validation 3: {is_valid} - {reason}")
    
    # Get metrics
    metrics = engine.get_metrics()
    print(f"\n📊 Metrics: {metrics}")
    print(f"📊 Rejection Rate: {metrics['rejection_rate']:.1%}")
