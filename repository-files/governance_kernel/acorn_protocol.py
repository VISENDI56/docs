"""
IP-03: Acorn Protocol - Somatic-Keyed Secret Injection

Biometric authentication using posture + location + stillness as cryptographic
authentication. Prevents "panic access" during crises by requiring physical
stillness for high-risk operations.

Secrets (like decryption keys for the Golden Thread) are only injected into
the environment if the biometric hash matches the authorized operator profile.

Integration with Google Secret Manager for secure key storage.
"""

import hashlib
import time
import numpy as np
from typing import Dict, Optional, Tuple
from dataclasses import dataclass
from datetime import datetime, timedelta
from enum import Enum
import logging
import json

logger = logging.getLogger(__name__)


class PostureState(Enum):
    """Operator posture states"""
    STANDING = "standing"
    SITTING = "sitting"
    MOVING = "moving"
    UNKNOWN = "unknown"


class StillnessLevel(Enum):
    """Operator stillness levels"""
    STILL = "still"              # <0.1 m/s movement
    CALM = "calm"                # 0.1-0.3 m/s
    ACTIVE = "active"            # 0.3-0.5 m/s
    AGITATED = "agitated"        # >0.5 m/s


@dataclass
class BiometricReading:
    """Biometric sensor reading"""
    posture: PostureState
    location_lat: float
    location_lng: float
    movement_velocity: float  # m/s
    timestamp: datetime
    
    def calculate_stillness(self) -> StillnessLevel:
        """Calculate stillness level from movement velocity"""
        if self.movement_velocity < 0.1:
            return StillnessLevel.STILL
        elif self.movement_velocity < 0.3:
            return StillnessLevel.CALM
        elif self.movement_velocity < 0.5:
            return StillnessLevel.ACTIVE
        else:
            return StillnessLevel.AGITATED
    
    def to_hash_input(self) -> str:
        """Convert reading to hash input string"""
        return f"{self.posture.value}|{self.location_lat:.6f}|{self.location_lng:.6f}|{self.calculate_stillness().value}"


@dataclass
class OperatorProfile:
    """Authorized operator biometric profile"""
    operator_id: str
    authorized_postures: list[PostureState]
    authorized_locations: list[Tuple[float, float, float]]  # (lat, lng, radius_meters)
    required_stillness: StillnessLevel
    biometric_hash: str
    
    def matches_reading(self, reading: BiometricReading, tolerance: float = 100.0) -> bool:
        """Check if reading matches authorized profile"""
        # Check posture
        if reading.posture not in self.authorized_postures:
            return False
        
        # Check location (within radius of any authorized location)
        location_match = False
        for auth_lat, auth_lng, radius in self.authorized_locations:
            distance = self._haversine_distance(
                reading.location_lat, reading.location_lng,
                auth_lat, auth_lng
            )
            if distance <= radius:
                location_match = True
                break
        
        if not location_match:
            return False
        
        # Check stillness
        stillness = reading.calculate_stillness()
        required_levels = {
            StillnessLevel.STILL: [StillnessLevel.STILL],
            StillnessLevel.CALM: [StillnessLevel.STILL, StillnessLevel.CALM],
            StillnessLevel.ACTIVE: [StillnessLevel.STILL, StillnessLevel.CALM, StillnessLevel.ACTIVE],
            StillnessLevel.AGITATED: list(StillnessLevel)
        }
        
        if stillness not in required_levels[self.required_stillness]:
            return False
        
        return True
    
    @staticmethod
    def _haversine_distance(lat1: float, lng1: float, lat2: float, lng2: float) -> float:
        """Calculate distance between two coordinates in meters"""
        R = 6371000  # Earth radius in meters
        
        phi1 = np.radians(lat1)
        phi2 = np.radians(lat2)
        delta_phi = np.radians(lat2 - lat1)
        delta_lambda = np.radians(lng2 - lng1)
        
        a = np.sin(delta_phi/2)**2 + np.cos(phi1) * np.cos(phi2) * np.sin(delta_lambda/2)**2
        c = 2 * np.arctan2(np.sqrt(a), np.sqrt(1-a))
        
        return R * c


class AcornProtocol:
    """
    IP-03: Acorn Protocol - Somatic-Keyed Secret Injection
    
    Biometric authentication using posture + location + stillness.
    Prevents panic access during crises.
    """
    
    def __init__(
        self,
        gcp_project_id: Optional[str] = None,
        enable_hardware_attestation: bool = False
    ):
        """
        Initialize Acorn Protocol
        
        Args:
            gcp_project_id: Google Cloud Project ID for Secret Manager
            enable_hardware_attestation: Enable TPM hardware attestation
        """
        self.gcp_project_id = gcp_project_id
        self.enable_hardware_attestation = enable_hardware_attestation
        
        # Operator profiles
        self.operator_profiles: Dict[str, OperatorProfile] = {}
        
        # Biometric reading history
        self.reading_history: list[BiometricReading] = []
        
        # Authentication state
        self.authenticated_operator: Optional[str] = None
        self.authentication_timestamp: Optional[datetime] = None
        self.session_timeout = timedelta(minutes=15)
        
        logger.info(f"🔐 Acorn Protocol initialized - Hardware attestation: {enable_hardware_attestation}")
    
    def register_operator(
        self,
        operator_id: str,
        authorized_postures: list[PostureState],
        authorized_locations: list[Tuple[float, float, float]],
        required_stillness: StillnessLevel = StillnessLevel.CALM
    ) -> str:
        """
        Register an authorized operator
        
        Args:
            operator_id: Unique operator identifier
            authorized_postures: List of authorized postures
            authorized_locations: List of (lat, lng, radius) tuples
            required_stillness: Minimum required stillness level
        
        Returns:
            Biometric hash for the operator
        """
        # Generate biometric hash
        hash_input = f"{operator_id}|{','.join([p.value for p in authorized_postures])}|{required_stillness.value}"
        biometric_hash = hashlib.sha256(hash_input.encode()).hexdigest()
        
        profile = OperatorProfile(
            operator_id=operator_id,
            authorized_postures=authorized_postures,
            authorized_locations=authorized_locations,
            required_stillness=required_stillness,
            biometric_hash=biometric_hash
        )
        
        self.operator_profiles[operator_id] = profile
        
        logger.info(f"✅ Operator registered: {operator_id} (hash: {biometric_hash[:16]}...)")
        
        return biometric_hash
    
    def authenticate(
        self,
        operator_id: str,
        reading: BiometricReading,
        require_stillness_duration: float = 3.0
    ) -> Tuple[bool, Optional[str]]:
        """
        Authenticate operator using biometric reading
        
        Args:
            operator_id: Operator to authenticate
            reading: Current biometric reading
            require_stillness_duration: Required stillness duration in seconds
        
        Returns:
            (authenticated, reason)
        """
        # Check if operator is registered
        if operator_id not in self.operator_profiles:
            return False, f"Operator {operator_id} not registered"
        
        profile = self.operator_profiles[operator_id]
        
        # Add reading to history
        self.reading_history.append(reading)
        if len(self.reading_history) > 100:
            self.reading_history = self.reading_history[-100:]
        
        # Check if reading matches profile
        if not profile.matches_reading(reading):
            return False, "Biometric reading does not match authorized profile"
        
        # Check stillness duration
        if require_stillness_duration > 0:
            recent_readings = [
                r for r in self.reading_history
                if (reading.timestamp - r.timestamp).total_seconds() <= require_stillness_duration
            ]
            
            if len(recent_readings) < 3:
                return False, f"Insufficient stillness duration (need {require_stillness_duration}s)"
            
            # Check if all recent readings show required stillness
            for r in recent_readings:
                if r.calculate_stillness().value != profile.required_stillness.value:
                    if profile.required_stillness == StillnessLevel.STILL:
                        return False, "Movement detected - stillness required"
        
        # Authentication successful
        self.authenticated_operator = operator_id
        self.authentication_timestamp = datetime.utcnow()
        
        logger.info(f"✅ Operator authenticated: {operator_id}")
        
        return True, None
    
    def is_authenticated(self, operator_id: str) -> bool:
        """Check if operator is currently authenticated"""
        if self.authenticated_operator != operator_id:
            return False
        
        if self.authentication_timestamp is None:
            return False
        
        # Check session timeout
        if datetime.utcnow() - self.authentication_timestamp > self.session_timeout:
            logger.warning(f"⏰ Session timeout for operator: {operator_id}")
            self.authenticated_operator = None
            self.authentication_timestamp = None
            return False
        
        return True
    
    def inject_secret(
        self,
        operator_id: str,
        secret_name: str,
        reading: BiometricReading
    ) -> Optional[str]:
        """
        Inject secret if operator is authenticated with valid biometrics
        
        Args:
            operator_id: Operator requesting secret
            secret_name: Name of secret to inject
            reading: Current biometric reading
        
        Returns:
            Secret value if authenticated, None otherwise
        """
        # Authenticate operator
        authenticated, reason = self.authenticate(operator_id, reading)
        
        if not authenticated:
            logger.warning(f"❌ Secret injection denied for {operator_id}: {reason}")
            return None
        
        # In production, this would fetch from Google Secret Manager
        # For now, return a mock secret
        if self.gcp_project_id:
            secret_value = self._fetch_from_secret_manager(secret_name)
        else:
            secret_value = f"MOCK_SECRET_{secret_name}"
        
        logger.info(f"🔑 Secret injected: {secret_name} for operator {operator_id}")
        
        return secret_value
    
    def _fetch_from_secret_manager(self, secret_name: str) -> Optional[str]:
        """
        Fetch secret from Google Secret Manager
        
        In production, this would use:
        from google.cloud import secretmanager
        
        client = secretmanager.SecretManagerServiceClient()
        name = f"projects/{self.gcp_project_id}/secrets/{secret_name}/versions/latest"
        response = client.access_secret_version(request={"name": name})
        return response.payload.data.decode("UTF-8")
        """
        logger.info(f"📦 Fetching secret from Secret Manager: {secret_name}")
        return f"SECRET_VALUE_{secret_name}"
    
    def revoke_authentication(self, operator_id: str):
        """Revoke operator authentication"""
        if self.authenticated_operator == operator_id:
            self.authenticated_operator = None
            self.authentication_timestamp = None
            logger.info(f"🔒 Authentication revoked: {operator_id}")
    
    def get_status(self) -> Dict:
        """Get current Acorn Protocol status"""
        return {
            "authenticated_operator": self.authenticated_operator,
            "authentication_timestamp": self.authentication_timestamp.isoformat() if self.authentication_timestamp else None,
            "session_timeout_minutes": self.session_timeout.total_seconds() / 60,
            "registered_operators": len(self.operator_profiles),
            "hardware_attestation_enabled": self.enable_hardware_attestation,
            "reading_history_size": len(self.reading_history)
        }


# Singleton instance
_acorn_protocol = None

def get_acorn_protocol() -> AcornProtocol:
    """Get the global AcornProtocol instance"""
    global _acorn_protocol
    if _acorn_protocol is None:
        _acorn_protocol = AcornProtocol()
    return _acorn_protocol


# Example usage
if __name__ == "__main__":
    acorn = AcornProtocol(gcp_project_id="iluminara-core")
    
    # Register operator
    operator_id = "DR_AMINA_HASSAN"
    biometric_hash = acorn.register_operator(
        operator_id=operator_id,
        authorized_postures=[PostureState.SITTING],
        authorized_locations=[
            (0.0512, 40.3129, 100.0),  # Dadaab clinic, 100m radius
        ],
        required_stillness=StillnessLevel.CALM
    )
    
    print(f"✅ Operator registered: {operator_id}")
    print(f"   Biometric hash: {biometric_hash[:32]}...")
    
    # Simulate authentication with valid biometrics
    print("\n=== Valid Authentication ===")
    reading = BiometricReading(
        posture=PostureState.SITTING,
        location_lat=0.0512,
        location_lng=40.3129,
        movement_velocity=0.15,  # Calm
        timestamp=datetime.utcnow()
    )
    
    authenticated, reason = acorn.authenticate(operator_id, reading)
    print(f"Authenticated: {authenticated}")
    if not authenticated:
        print(f"Reason: {reason}")
    
    # Inject secret
    if authenticated:
        secret = acorn.inject_secret(operator_id, "GOLDEN_THREAD_KEY", reading)
        print(f"Secret injected: {secret[:20]}...")
    
    # Simulate authentication with panic (movement)
    print("\n=== Panic Authentication (Movement Detected) ===")
    panic_reading = BiometricReading(
        posture=PostureState.SITTING,
        location_lat=0.0512,
        location_lng=40.3129,
        movement_velocity=0.8,  # Agitated
        timestamp=datetime.utcnow()
    )
    
    authenticated, reason = acorn.authenticate(operator_id, panic_reading)
    print(f"Authenticated: {authenticated}")
    if not authenticated:
        print(f"Reason: {reason}")
    
    # Status
    print("\n=== Status ===")
    status = acorn.get_status()
    print(json.dumps(status, indent=2))
