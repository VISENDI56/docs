"""
HSTPU-Bounded Decision Windows
Health Spatiotemporal Processing Unit - Constraint Protocol

Enforces spatiotemporal validity bounds for humanitarian decisions:
- 50km radius constraint (spatial)
- 72-hour validity period (temporal)
- 100% rejection for out-of-bounds decisions

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
class SpatialBounds:
    """Spatial constraint definition"""
    center_lat: float
    center_lng: float
    radius_km: float = 50.0  # Default 50km radius
    
    def contains(self, lat: float, lng: float) -> bool:
        """Check if coordinates are within bounds"""
        distance = self._haversine_distance(
            self.center_lat, self.center_lng,
            lat, lng
        )
        return distance <= self.radius_km
    
    @staticmethod
    def _haversine_distance(lat1: float, lng1: float, lat2: float, lng2: float) -> float:
        """Calculate distance between two points using Haversine formula"""
        R = 6371  # Earth radius in km
        
        dlat = math.radians(lat2 - lat1)
        dlng = math.radians(lng2 - lng1)
        
        a = (math.sin(dlat / 2) ** 2 +
             math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) *
             math.sin(dlng / 2) ** 2)
        
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
        
        return R * c


@dataclass
class TemporalBounds:
    """Temporal constraint definition"""
    created_at: datetime
    validity_hours: float = 72.0  # Default 72-hour validity
    
    def is_valid(self, check_time: Optional[datetime] = None) -> bool:
        """Check if decision is still temporally valid"""
        if check_time is None:
            check_time = datetime.utcnow()
        
        expiration = self.created_at + timedelta(hours=self.validity_hours)
        return check_time <= expiration
    
    def time_remaining(self, check_time: Optional[datetime] = None) -> float:
        """Get remaining validity time in hours"""
        if check_time is None:
            check_time = datetime.utcnow()
        
        expiration = self.created_at + timedelta(hours=self.validity_hours)
        remaining = (expiration - check_time).total_seconds() / 3600
        
        return max(0.0, remaining)


@dataclass
class HumanitarianDecision:
    """Humanitarian decision with spatiotemporal bounds"""
    decision_id: str
    decision_type: str
    spatial_bounds: SpatialBounds
    temporal_bounds: TemporalBounds
    outbreak_phase: OutbreakPhase
    metadata: Dict
    
    def validate(
        self,
        target_lat: float,
        target_lng: float,
        check_time: Optional[datetime] = None
    ) -> Tuple[DecisionStatus, str]:
        """
        Validate decision against spatiotemporal constraints.
        
        Returns:
            (status, reason)
        """
        # Check temporal validity
        if not self.temporal_bounds.is_valid(check_time):
            remaining = self.temporal_bounds.time_remaining(check_time)
            return (
                DecisionStatus.EXPIRED,
                f"Decision expired {abs(remaining):.1f} hours ago"
            )
        
        # Check spatial validity
        if not self.spatial_bounds.contains(target_lat, target_lng):
            distance = SpatialBounds._haversine_distance(
                self.spatial_bounds.center_lat,
                self.spatial_bounds.center_lng,
                target_lat,
                target_lng
            )
            return (
                DecisionStatus.OUT_OF_BOUNDS,
                f"Target {distance:.1f}km from decision center "
                f"(max: {self.spatial_bounds.radius_km}km)"
            )
        
        return (DecisionStatus.VALID, "Decision valid for target location and time")


class HSTPUConstraintEngine:
    """
    Health Spatiotemporal Processing Unit - Constraint Engine
    
    Enforces spatiotemporal validity for humanitarian decisions in
    lagged environments where connectivity and coordination are limited.
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
            default_radius_km: Default spatial radius (50km)
            default_validity_hours: Default temporal validity (72 hours)
            strict_mode: If True, 100% rejection for out-of-bounds decisions
        """
        self.default_radius_km = default_radius_km
        self.default_validity_hours = default_validity_hours
        self.strict_mode = strict_mode
        
        # Active decisions registry
        self.active_decisions: Dict[str, HumanitarianDecision] = {}
        
        # Rejection statistics
        self.rejection_stats = {
            "total_validations": 0,
            "spatial_rejections": 0,
            "temporal_rejections": 0,
            "valid_decisions": 0
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
        center_lat: float,
        center_lng: float,
        outbreak_phase: OutbreakPhase,
        radius_km: Optional[float] = None,
        validity_hours: Optional[float] = None,
        metadata: Optional[Dict] = None
    ) -> HumanitarianDecision:
        """
        Create a new spatiotemporally-bounded humanitarian decision.
        
        Args:
            decision_id: Unique decision identifier
            decision_type: Type of decision (e.g., "vaccination_campaign")
            center_lat: Center latitude
            center_lng: Center longitude
            outbreak_phase: Current outbreak phase
            radius_km: Spatial radius (default: 50km)
            validity_hours: Temporal validity (default: 72h)
            metadata: Additional metadata
        
        Returns:
            HumanitarianDecision object
        """
        spatial_bounds = SpatialBounds(
            center_lat=center_lat,
            center_lng=center_lng,
            radius_km=radius_km or self.default_radius_km
        )
        
        temporal_bounds = TemporalBounds(
            created_at=datetime.utcnow(),
            validity_hours=validity_hours or self.default_validity_hours
        )
        
        decision = HumanitarianDecision(
            decision_id=decision_id,
            decision_type=decision_type,
            spatial_bounds=spatial_bounds,
            temporal_bounds=temporal_bounds,
            outbreak_phase=outbreak_phase,
            metadata=metadata or {}
        )
        
        # Register decision
        self.active_decisions[decision_id] = decision
        
        logger.info(
            f"✅ Decision created: {decision_id} - "
            f"Center: ({center_lat:.4f}, {center_lng:.4f}), "
            f"Radius: {spatial_bounds.radius_km}km, "
            f"Valid for: {temporal_bounds.validity_hours}h"
        )
        
        return decision
    
    def validate_decision(
        self,
        decision_id: str,
        target_lat: float,
        target_lng: float,
        check_time: Optional[datetime] = None
    ) -> Tuple[bool, DecisionStatus, str]:
        """
        Validate a decision against spatiotemporal constraints.
        
        Args:
            decision_id: Decision to validate
            target_lat: Target latitude
            target_lng: Target longitude
            check_time: Time to check validity (default: now)
        
        Returns:
            (is_valid, status, reason)
        """
        self.rejection_stats["total_validations"] += 1
        
        # Check if decision exists
        if decision_id not in self.active_decisions:
            logger.error(f"❌ Decision not found: {decision_id}")
            return (False, DecisionStatus.REJECTED, "Decision not found")
        
        decision = self.active_decisions[decision_id]
        
        # Validate
        status, reason = decision.validate(target_lat, target_lng, check_time)
        
        # Update statistics
        if status == DecisionStatus.VALID:
            self.rejection_stats["valid_decisions"] += 1
            logger.info(f"✅ Decision valid: {decision_id} - {reason}")
            return (True, status, reason)
        
        elif status == DecisionStatus.EXPIRED:
            self.rejection_stats["temporal_rejections"] += 1
            logger.warning(f"⏰ Decision expired: {decision_id} - {reason}")
            
            if self.strict_mode:
                return (False, status, reason)
            else:
                # Permissive mode: allow with warning
                return (True, status, f"WARNING: {reason}")
        
        elif status == DecisionStatus.OUT_OF_BOUNDS:
            self.rejection_stats["spatial_rejections"] += 1
            logger.warning(f"🌍 Decision out of bounds: {decision_id} - {reason}")
            
            if self.strict_mode:
                # 100% rejection in strict mode
                return (False, status, reason)
            else:
                # Permissive mode: allow with warning
                return (True, status, f"WARNING: {reason}")
        
        return (False, DecisionStatus.REJECTED, reason)
    
    def get_rejection_rate(self) -> Dict[str, float]:
        """Calculate rejection rates"""
        total = self.rejection_stats["total_validations"]
        
        if total == 0:
            return {
                "total_rejection_rate": 0.0,
                "spatial_rejection_rate": 0.0,
                "temporal_rejection_rate": 0.0
            }
        
        return {
            "total_rejection_rate": (
                (self.rejection_stats["spatial_rejections"] +
                 self.rejection_stats["temporal_rejections"]) / total
            ),
            "spatial_rejection_rate": (
                self.rejection_stats["spatial_rejections"] / total
            ),
            "temporal_rejection_rate": (
                self.rejection_stats["temporal_rejections"] / total
            )
        }
    
    def cleanup_expired_decisions(self) -> int:
        """Remove expired decisions from registry"""
        expired_count = 0
        expired_ids = []
        
        for decision_id, decision in self.active_decisions.items():
            if not decision.temporal_bounds.is_valid():
                expired_ids.append(decision_id)
                expired_count += 1
        
        for decision_id in expired_ids:
            del self.active_decisions[decision_id]
        
        if expired_count > 0:
            logger.info(f"🧹 Cleaned up {expired_count} expired decisions")
        
        return expired_count
    
    def get_active_decisions_for_location(
        self,
        lat: float,
        lng: float,
        check_time: Optional[datetime] = None
    ) -> List[HumanitarianDecision]:
        """Get all valid decisions for a location"""
        valid_decisions = []
        
        for decision in self.active_decisions.values():
            is_valid, status, _ = self.validate_decision(
                decision.decision_id,
                lat,
                lng,
                check_time
            )
            
            if is_valid and status == DecisionStatus.VALID:
                valid_decisions.append(decision)
        
        return valid_decisions


# Example usage
if __name__ == "__main__":
    # Initialize HSTPU engine
    engine = HSTPUConstraintEngine(
        default_radius_km=50.0,
        default_validity_hours=72.0,
        strict_mode=True
    )
    
    # Create decision for Dadaab refugee camp
    decision = engine.create_decision(
        decision_id="CHOLERA_RESPONSE_001",
        decision_type="vaccination_campaign",
        center_lat=0.0512,
        center_lng=40.3129,
        outbreak_phase=OutbreakPhase.RESPONSE,
        metadata={
            "disease": "cholera",
            "target_population": 200000,
            "resources_allocated": True
        }
    )
    
    # Validate decision for nearby location (within 50km)
    is_valid, status, reason = engine.validate_decision(
        decision_id="CHOLERA_RESPONSE_001",
        target_lat=0.0600,  # ~10km away
        target_lng=40.3200
    )
    print(f"✅ Nearby location: {is_valid} - {reason}")
    
    # Validate decision for distant location (>50km)
    is_valid, status, reason = engine.validate_decision(
        decision_id="CHOLERA_RESPONSE_001",
        target_lat=0.5000,  # ~50km away
        target_lng=40.8000
    )
    print(f"❌ Distant location: {is_valid} - {reason}")
    
    # Check rejection rates
    rates = engine.get_rejection_rate()
    print(f"\n📊 Rejection Rates:")
    print(f"   Total: {rates['total_rejection_rate']:.1%}")
    print(f"   Spatial: {rates['spatial_rejection_rate']:.1%}")
    print(f"   Temporal: {rates['temporal_rejection_rate']:.1%}")
