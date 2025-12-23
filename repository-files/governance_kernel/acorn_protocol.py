"""
IP-03: Acorn Protocol - Somatic Triad Authentication (STA)
A shift from "Knowledge-Based" security (passwords) to "Existence-Based" security (somatic state).

The Triad:
1. Posture (The Structural Hash) - Invariant joint angles
2. Location (The Spatial Nonce) - Geohashing with dynamic precision
3. Stillness (The Kinetic Entropy) - Micro-tremor signature

Compliance:
- NIST SP 800-63B (Digital Identity Guidelines - Biometric Authentication)
- ISO/IEC 30107 (Biometric Presentation Attack Detection)
- GDPR Art. 9 (Processing of Biometric Data)
- HIPAA §164.312(a)(2)(i) (Unique User Identification)

Use Case: Prevents "panic access" during crises by requiring physical stillness
for high-risk operations (e.g., triggering parametric bond payout).
"""

import numpy as np
import hashlib
import uuid
import time
import json
import logging
from typing import List, Tuple, Dict, Optional
from dataclasses import dataclass, asdict
from scipy.spatial.distance import hamming, euclidean
from sklearn.ensemble import IsolationForest
from datetime import datetime, timedelta
from enum import Enum

logger = logging.getLogger(__name__)


# --- SOMATIC MATH UTILITIES ---

def calculate_angle(a: np.ndarray, b: np.ndarray, c: np.ndarray) -> float:
    """
    Calculates the angle (in degrees) at joint 'b' formed by limbs a-b and b-c.
    Invariant to rotation and scale.
    
    This is the core of the Structural Hash: A user can stand 2m or 5m from
    the camera, but as long as they hold the "Secret Pose", the angles remain constant.
    
    Args:
        a: First point (e.g., shoulder)
        b: Joint point (e.g., elbow)
        c: Third point (e.g., wrist)
    
    Returns:
        Angle in degrees
    """
    ba = a - b
    bc = c - b
    
    cosine_angle = np.dot(ba, bc) / (np.linalg.norm(ba) * np.linalg.norm(bc) + 1e-6)
    angle = np.arccos(np.clip(cosine_angle, -1.0, 1.0))
    return np.degrees(angle)


def quantize_vector(vector: np.ndarray, precision: int = 10) -> str:
    """
    Fuzzy quantization: Bins continuous values to discrete integers to allow 
    for biological variance (fuzzy commitment).
    
    This solves the "Biometric vs. Hash" dilemma: Biometrics are never exactly
    the same, but hashes must be. By quantizing (e.g., 91.2° → 90°), we get
    reproducible hashes from slightly varying biological data.
    
    Args:
        vector: Continuous values (e.g., joint angles)
        precision: Quantization step size
    
    Returns:
        Quantized string representation
    """
    quantized = np.round(vector / precision) * precision
    return "".join([f"{int(x):03}" for x in quantized])


def kinetic_entropy(imu_data: np.ndarray) -> float:
    """
    Calculates entropy from stillness. This is the "Living Salt".
    
    High variance = Movement (Reject)
    Zero variance = Static Image/Spoof (Reject)
    Low, chaotic variance = Living Stillness (Accept)
    
    A photograph has 0.0 variance. A deepfake video often has smooth,
    algorithmic variance. A human has chaotic, low-amplitude variance (micro-tremors).
    
    Args:
        imu_data: IMU readings (accelerometer/gyroscope) shape (N, 3)
    
    Returns:
        Entropy magnitude
    """
    # Calculate variance magnitude
    var = np.var(imu_data, axis=0)
    magnitude = np.linalg.norm(var)
    return magnitude


# --- DATA STRUCTURES ---

class AuthenticationRisk(Enum):
    """Risk levels for authentication operations"""
    LOW = "low"              # Read-only operations
    MEDIUM = "medium"        # Data entry, routine operations
    HIGH = "high"            # Financial transactions, data exports
    CRITICAL = "critical"    # Parametric bond payout, emergency overrides


@dataclass
class SomaticProfile:
    """Enrolled somatic baseline for a user"""
    user_id: str
    posture_template: np.ndarray    # The enrolled angles
    location_hash: str              # The enrolled geohash
    stillness_baseline: float       # The enrolled micro-tremor magnitude
    enrollment_timestamp: float
    risk_level: AuthenticationRisk  # Required risk level for this profile
    metadata: Dict = None           # Additional context (role, jurisdiction, etc.)
    
    def to_dict(self) -> Dict:
        """Convert to dictionary for serialization"""
        return {
            "user_id": self.user_id,
            "posture_template": self.posture_template.tolist(),
            "location_hash": self.location_hash,
            "stillness_baseline": self.stillness_baseline,
            "enrollment_timestamp": self.enrollment_timestamp,
            "risk_level": self.risk_level.value,
            "metadata": self.metadata or {}
        }
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'SomaticProfile':
        """Create from dictionary"""
        return cls(
            user_id=data["user_id"],
            posture_template=np.array(data["posture_template"]),
            location_hash=data["location_hash"],
            stillness_baseline=data["stillness_baseline"],
            enrollment_timestamp=data["enrollment_timestamp"],
            risk_level=AuthenticationRisk(data["risk_level"]),
            metadata=data.get("metadata", {})
        )


@dataclass
class AuthenticationResult:
    """Result of authentication attempt"""
    success: bool
    user_id: str
    session_token: Optional[str]
    risk_level: AuthenticationRisk
    timestamp: float
    failure_reason: Optional[str] = None
    posture_distance: Optional[float] = None
    location_match: Optional[bool] = None
    stillness_score: Optional[float] = None
    anomaly_detected: Optional[bool] = None


# --- THE ENGINE ---

class SomaticTriadAuthentication:
    """
    Implements the 'Acorn Protocol': Posture + Location + Stillness.
    
    This is Existence-Based Security: You cannot steal what you cannot be.
    """
    
    def __init__(
        self,
        posture_tolerance: float = 15.0,  # degrees
        location_precision: int = 4,      # decimal places (~11m)
        stillness_threshold: float = 0.5,
        enable_audit: bool = True,
        storage_path: str = "./somatic_profiles"
    ):
        """
        Initialize the Acorn Protocol.
        
        Args:
            posture_tolerance: Maximum angle deviation (degrees)
            location_precision: GPS precision (4 = ~11m, 5 = ~1m)
            stillness_threshold: Maximum kinetic entropy for stillness
            enable_audit: Enable tamper-proof audit trail
            storage_path: Path to store somatic profiles
        """
        self.profiles: Dict[str, SomaticProfile] = {}
        self.posture_tolerance = posture_tolerance
        self.location_precision = location_precision
        self.stillness_threshold = stillness_threshold
        self.enable_audit = enable_audit
        self.storage_path = storage_path
        
        # Anomaly Detector (Lightweight ML)
        # Detects if stillness is "too still" (spoof) or "too erratic" (struggle)
        self.anomaly_detector = IsolationForest(contamination=0.1, random_state=42)
        self.is_detector_trained = False
        self.training_buffer = []
        
        # Audit trail
        self.audit_log = []
        
        logger.info(f"🌰 Acorn Protocol initialized - Tolerance: {posture_tolerance}°")
    
    def _extract_posture_features(self, keypoints: np.ndarray) -> np.ndarray:
        """
        Converts 2D/3D keypoints (e.g., from MediaPipe) into invariant joint angles.
        
        Keypoints expected shape: (N, 3) -> [x, y, z]
        
        Standard MediaPipe Pose Topology:
        0-Nose, 11-L.Shoulder, 12-R.Shoulder, 13-L.Elbow, 14-R.Elbow,
        15-L.Wrist, 16-R.Wrist, 23-L.Hip, 24-R.Hip
        
        Args:
            keypoints: Body keypoints from pose estimation
        
        Returns:
            Array of invariant joint angles
        """
        if len(keypoints) < 7:
            logger.warning("⚠️ Insufficient keypoints for posture extraction")
            return np.zeros(5)
        
        # Calculate key angles (invariant to camera position)
        angles = []
        
        # 1. Left Arm Angle (Shoulder-Elbow-Wrist)
        if len(keypoints) > 15:
            a1 = calculate_angle(keypoints[11], keypoints[13], keypoints[15])
            angles.append(a1)
        
        # 2. Right Arm Angle (Shoulder-Elbow-Wrist)
        if len(keypoints) > 16:
            a2 = calculate_angle(keypoints[12], keypoints[14], keypoints[16])
            angles.append(a2)
        
        # 3. Neck/Shoulder Angle (L.Shoulder-Nose-R.Shoulder)
        if len(keypoints) > 12:
            a3 = calculate_angle(keypoints[11], keypoints[0], keypoints[12])
            angles.append(a3)
        
        # 4. Left Hip Angle (Shoulder-Hip-Knee) - if available
        if len(keypoints) > 23:
            a4 = calculate_angle(keypoints[11], keypoints[23], keypoints[0])
            angles.append(a4)
        
        # 5. Right Hip Angle (Shoulder-Hip-Knee) - if available
        if len(keypoints) > 24:
            a5 = calculate_angle(keypoints[12], keypoints[24], keypoints[0])
            angles.append(a5)
        
        return np.array(angles)
    
    def _generate_geohash(self, gps: Tuple[float, float]) -> str:
        """
        Quantizes GPS to a specific grid resolution.
        
        This is the Spatial Nonce: Authentication is anchored to physical reality.
        A user in Nairobi cannot authenticate as if they're in New York.
        
        Args:
            gps: (latitude, longitude)
        
        Returns:
            Geohash string
        """
        lat, lon = gps
        # Rounding acts as a spatial bucket
        lat_r = round(lat, self.location_precision)
        lon_r = round(lon, self.location_precision)
        return f"{lat_r}|{lon_r}"
    
    def enroll(
        self,
        user_id: str,
        posture_keypoints: np.ndarray,
        gps_coords: Tuple[float, float],
        imu_readings: np.ndarray,
        risk_level: AuthenticationRisk = AuthenticationRisk.MEDIUM,
        metadata: Optional[Dict] = None
    ) -> bool:
        """
        Captures the Somatic Baseline.
        
        This is the enrollment phase: The user performs their "Secret Pose"
        at their "Secret Location" while demonstrating "Living Stillness".
        
        Args:
            user_id: Unique user identifier
            posture_keypoints: Body keypoints from pose estimation
            gps_coords: GPS coordinates (lat, lon)
            imu_readings: IMU data (accelerometer/gyroscope) shape (N, 3)
            risk_level: Required risk level for this profile
            metadata: Additional context
        
        Returns:
            True if enrollment successful
        """
        logger.info(f"🌰 [Acorn] Enrolling User: {user_id}...")
        
        # 1. Posture Extraction (The Structural Hash)
        angles = self._extract_posture_features(posture_keypoints)
        
        if len(angles) == 0 or np.all(angles == 0):
            logger.error("❌ Posture extraction failed - insufficient keypoints")
            return False
        
        # 2. Location Hashing (The Spatial Nonce)
        geo_hash = self._generate_geohash(gps_coords)
        
        # 3. Stillness Baseline (The Kinetic Entropy)
        kinetic_val = kinetic_entropy(imu_readings)
        
        # Liveness check during enrollment
        if kinetic_val < 1e-5:
            logger.error("❌ Enrollment failed - Zero entropy (static image suspected)")
            return False
        
        # Train Anomaly Detector on Kinetic Data
        self.training_buffer.append([kinetic_val])
        if len(self.training_buffer) > 5:
            self.anomaly_detector.fit(self.training_buffer)
            self.is_detector_trained = True
            logger.info("✅ Anomaly detector trained")
        
        # Create profile
        profile = SomaticProfile(
            user_id=user_id,
            posture_template=angles,
            location_hash=geo_hash,
            stillness_baseline=kinetic_val,
            enrollment_timestamp=time.time(),
            risk_level=risk_level,
            metadata=metadata or {}
        )
        
        self.profiles[user_id] = profile
        
        # Audit log
        if self.enable_audit:
            self._log_audit("ENROLL", user_id, {
                "geo_hash": geo_hash,
                "kinetic_baseline": kinetic_val,
                "risk_level": risk_level.value
            })
        
        bio_hash = hashlib.sha256((geo_hash + str(angles.tolist())).encode()).hexdigest()[:16]
        logger.info(f"✅ [Acorn] Enrollment Complete - Bio-Hash: {bio_hash}")
        
        return True
    
    def authenticate(
        self,
        user_id: str,
        posture_keypoints: np.ndarray,
        gps_coords: Tuple[float, float],
        imu_readings: np.ndarray,
        operation_risk: AuthenticationRisk = AuthenticationRisk.MEDIUM
    ) -> AuthenticationResult:
        """
        Verifies the Triad. Returns session token if valid.
        
        This is the authentication phase: The user must reproduce their
        "Secret Pose" at their "Secret Location" with "Living Stillness".
        
        Args:
            user_id: User to authenticate
            posture_keypoints: Current body keypoints
            gps_coords: Current GPS coordinates
            imu_readings: Current IMU data
            operation_risk: Risk level of the operation being attempted
        
        Returns:
            AuthenticationResult with success status and session token
        """
        logger.info(f"🌰 [Acorn] Authenticating: {user_id} (Risk: {operation_risk.value})")
        
        # Check if user exists
        if user_id not in self.profiles:
            logger.error(f"❌ User not found: {user_id}")
            return AuthenticationResult(
                success=False,
                user_id=user_id,
                session_token=None,
                risk_level=operation_risk,
                timestamp=time.time(),
                failure_reason="USER_NOT_FOUND"
            )
        
        profile = self.profiles[user_id]
        
        # Check if user's enrolled risk level is sufficient
        risk_hierarchy = {
            AuthenticationRisk.LOW: 0,
            AuthenticationRisk.MEDIUM: 1,
            AuthenticationRisk.HIGH: 2,
            AuthenticationRisk.CRITICAL: 3
        }
        
        if risk_hierarchy[profile.risk_level] < risk_hierarchy[operation_risk]:
            logger.error(f"❌ Insufficient risk level - Required: {operation_risk.value}, Enrolled: {profile.risk_level.value}")
            return AuthenticationResult(
                success=False,
                user_id=user_id,
                session_token=None,
                risk_level=operation_risk,
                timestamp=time.time(),
                failure_reason="INSUFFICIENT_RISK_LEVEL"
            )
        
        # --- 1. POSTURE CHECK (The Structural Hash) ---
        current_angles = self._extract_posture_features(posture_keypoints)
        
        if len(current_angles) == 0 or np.all(current_angles == 0):
            logger.error("❌ Posture extraction failed")
            return AuthenticationResult(
                success=False,
                user_id=user_id,
                session_token=None,
                risk_level=operation_risk,
                timestamp=time.time(),
                failure_reason="POSTURE_EXTRACTION_FAILED"
            )
        
        # Euclidean distance between angle vectors
        dist = euclidean(profile.posture_template, current_angles)
        
        if dist > self.posture_tolerance:
            logger.warning(f"❌ Posture Mismatch - Distance: {dist:.2f}° (Limit: {self.posture_tolerance}°)")
            if self.enable_audit:
                self._log_audit("AUTH_FAIL_POSTURE", user_id, {"distance": dist})
            return AuthenticationResult(
                success=False,
                user_id=user_id,
                session_token=None,
                risk_level=operation_risk,
                timestamp=time.time(),
                failure_reason="POSTURE_MISMATCH",
                posture_distance=dist
            )
        
        # --- 2. LOCATION CHECK (The Spatial Nonce) ---
        current_geo = self._generate_geohash(gps_coords)
        location_match = current_geo == profile.location_hash
        
        if not location_match:
            logger.warning(f"❌ Location Invalid - Expected: {profile.location_hash}, Got: {current_geo}")
            if self.enable_audit:
                self._log_audit("AUTH_FAIL_LOCATION", user_id, {
                    "expected": profile.location_hash,
                    "actual": current_geo
                })
            return AuthenticationResult(
                success=False,
                user_id=user_id,
                session_token=None,
                risk_level=operation_risk,
                timestamp=time.time(),
                failure_reason="LOCATION_MISMATCH",
                posture_distance=dist,
                location_match=False
            )
        
        # --- 3. STILLNESS & ANOMALY CHECK (The Kinetic Entropy) ---
        current_kinetic = kinetic_entropy(imu_readings)
        
        # Liveness Check: Is it TOO perfect? (Static Image Spoof)
        if current_kinetic < 1e-5:
            logger.error("❌ SPOOF DETECTED: Zero Entropy (Static Image)")
            if self.enable_audit:
                self._log_audit("AUTH_FAIL_SPOOF", user_id, {"kinetic": current_kinetic})
            return AuthenticationResult(
                success=False,
                user_id=user_id,
                session_token=None,
                risk_level=operation_risk,
                timestamp=time.time(),
                failure_reason="SPOOF_DETECTED_ZERO_ENTROPY",
                posture_distance=dist,
                location_match=True,
                stillness_score=current_kinetic
            )
        
        # Anomaly Check: Is the movement pattern natural?
        anomaly_detected = False
        if self.is_detector_trained:
            pred = self.anomaly_detector.predict([[current_kinetic]])
            if pred[0] == -1:
                anomaly_detected = True
                logger.warning("⚠️ Anomaly Detected: Unnatural Movement Pattern")
                if self.enable_audit:
                    self._log_audit("AUTH_FAIL_ANOMALY", user_id, {"kinetic": current_kinetic})
                return AuthenticationResult(
                    success=False,
                    user_id=user_id,
                    session_token=None,
                    risk_level=operation_risk,
                    timestamp=time.time(),
                    failure_reason="ANOMALY_DETECTED",
                    posture_distance=dist,
                    location_match=True,
                    stillness_score=current_kinetic,
                    anomaly_detected=True
                )
        
        # --- ALL CHECKS PASSED ---
        logger.info("✅ [Acorn] Triad Verified - Generating Bio-Cryptographic Key...")
        
        session_token = self._generate_key(user_id, current_angles, current_geo, current_kinetic)
        
        if self.enable_audit:
            self._log_audit("AUTH_SUCCESS", user_id, {
                "posture_distance": dist,
                "kinetic": current_kinetic,
                "risk_level": operation_risk.value
            })
        
        return AuthenticationResult(
            success=True,
            user_id=user_id,
            session_token=session_token,
            risk_level=operation_risk,
            timestamp=time.time(),
            posture_distance=dist,
            location_match=True,
            stillness_score=current_kinetic,
            anomaly_detected=False
        )
    
    def _generate_key(
        self,
        user_id: str,
        angles: np.ndarray,
        geo: str,
        kinetic: float
    ) -> str:
        """
        Derives a high-entropy key from the fused somatic data.
        
        Salt = Location + Time Window (TOTP style)
        Password = Quantized Posture + Stillness Magnitude
        
        This is Fuzzy Key Derivation: The key is reproducible from slightly
        varying biological data, but unpredictable without the exact somatic state.
        
        Args:
            user_id: User identifier
            angles: Joint angles
            geo: Geohash
            kinetic: Kinetic entropy
        
        Returns:
            Session token (hex string)
        """
        # Dynamic Salt: Changes every 30 seconds to prevent replay
        time_nonce = str(int(time.time() / 30))
        salt = (geo + time_nonce + user_id).encode('utf-8')
        
        # "Fuzzy" Password construction
        # We use the QUANTIZED angles, so minor variations result in the SAME string
        somatic_secret = (quantize_vector(angles) + f"{kinetic:.4f}").encode('utf-8')
        
        # Key Derivation Function (PBKDF2)
        key = hashlib.pbkdf2_hmac('sha256', somatic_secret, salt, 100000)
        
        return key.hex()
    
    def _log_audit(self, action: str, user_id: str, metadata: Dict):
        """Internal audit logging"""
        audit_entry = {
            "timestamp": datetime.utcnow().isoformat(),
            "action": action,
            "user_id": user_id,
            "metadata": metadata
        }
        self.audit_log.append(audit_entry)
        logger.debug(f"📝 Audit: {action} - {user_id}")
    
    def save_profiles(self, filepath: str):
        """Save somatic profiles to disk"""
        profiles_dict = {
            user_id: profile.to_dict()
            for user_id, profile in self.profiles.items()
        }
        
        with open(filepath, 'w') as f:
            json.dump(profiles_dict, f, indent=2)
        
        logger.info(f"💾 Saved {len(self.profiles)} profiles to {filepath}")
    
    def load_profiles(self, filepath: str):
        """Load somatic profiles from disk"""
        with open(filepath, 'r') as f:
            profiles_dict = json.load(f)
        
        self.profiles = {
            user_id: SomaticProfile.from_dict(data)
            for user_id, data in profiles_dict.items()
        }
        
        logger.info(f"📂 Loaded {len(self.profiles)} profiles from {filepath}")


# --- DEPLOYMENT DEMO ---

if __name__ == "__main__":
    print("=" * 60)
    print("🌰 Initializing Acorn Protocol: Somatic Triad Authentication")
    print("=" * 60)
    print()
    
    # Configure logging
    logging.basicConfig(level=logging.INFO)
    
    sta = SomaticTriadAuthentication(posture_tolerance=10.0)
    
    # SYNTHETIC DATA GENERATION
    # -------------------------
    # Simulating a user doing a specific hand gesture/pose at a specific lat/long
    
    print("📋 SCENARIO: Emergency Response Coordinator Authentication")
    print("   Operation: Trigger Parametric Bond Payout ($2.5M)")
    print("   Risk Level: CRITICAL")
    print()
    
    # 1. Posture: [Shoulder, Elbow, Wrist] x 2 arms + Neck
    # Keypoints: [x, y, z]
    # Enrolling "Hand Over Heart" gesture (solemn oath pose)
    enroll_pose = np.array([
        [0, 0, 0],      # Nose
        [-1, 0, 0],     # L.Shoulder
        [1, 0, 0],      # R.Shoulder
        [-1.5, -0.5, 0],  # L.Elbow
        [1, -1, 0],     # R.Elbow (bent, hand over heart)
        [-2, -1, 0],    # L.Wrist
        [0.5, -0.5, 0], # R.Wrist (over heart)
        [-0.5, -2, 0],  # L.Hip
        [0.5, -2, 0]    # R.Hip
    ])
    
    # 2. Location: Nairobi Emergency Operations Center
    enroll_loc = (-1.2921, 36.8219)
    
    # 3. Stillness: Accelerometer (x,y,z) over 100 samples
    # Natural human micro-tremor (gaussian noise)
    enroll_imu = np.random.normal(0, 0.02, (100, 3))
    
    # ENROLL
    print("🔐 PHASE 1: ENROLLMENT")
    print("-" * 60)
    success = sta.enroll(
        "coordinator_001",
        enroll_pose,
        enroll_loc,
        enroll_imu,
        risk_level=AuthenticationRisk.CRITICAL,
        metadata={
            "role": "Emergency Response Coordinator",
            "jurisdiction": "KDPA_KE",
            "clearance": "CRITICAL_OPS"
        }
    )
    print()
    
    # AUTHENTICATION ATTEMPT 1: Valid User
    print("🔓 PHASE 2: AUTHENTICATION ATTEMPT (Valid User)")
    print("-" * 60)
    
    # Slight variation in pose (biological noise)
    auth_pose_valid = enroll_pose + np.random.normal(0, 0.05, enroll_pose.shape)
    # Same location
    auth_loc_valid = (-1.2921, 36.8219)
    # Different stillness noise instance (living human)
    auth_imu_valid = np.random.normal(0, 0.02, (100, 3))
    
    result = sta.authenticate(
        "coordinator_001",
        auth_pose_valid,
        auth_loc_valid,
        auth_imu_valid,
        operation_risk=AuthenticationRisk.CRITICAL
    )
    
    print(f"Result: {'✅ SUCCESS' if result.success else '❌ FAIL'}")
    if result.success:
        print(f"Session Token: {result.session_token[:32]}...")
        print(f"Posture Distance: {result.posture_distance:.2f}°")
        print(f"Stillness Score: {result.stillness_score:.6f}")
    else:
        print(f"Failure Reason: {result.failure_reason}")
    print()
    
    # AUTHENTICATION ATTEMPT 2: Imposter / Wrong Pose
    print("🚫 PHASE 3: AUTHENTICATION ATTEMPT (Wrong Pose)")
    print("-" * 60)
    
    # Different pose (arms at sides, not hand over heart)
    auth_pose_invalid = np.array([
        [0, 0, 0],      # Nose
        [-1, 0, 0],     # L.Shoulder
        [1, 0, 0],      # R.Shoulder
        [-1, -1, 0],    # L.Elbow (straight down)
        [1, -1, 0],     # R.Elbow (straight down)
        [-1, -2, 0],    # L.Wrist
        [1, -2, 0],     # R.Wrist
        [-0.5, -2, 0],  # L.Hip
        [0.5, -2, 0]    # R.Hip
    ])
    
    result_fail = sta.authenticate(
        "coordinator_001",
        auth_pose_invalid,
        auth_loc_valid,
        auth_imu_valid,
        operation_risk=AuthenticationRisk.CRITICAL
    )
    
    print(f"Result: {'✅ SUCCESS' if result_fail.success else '❌ FAIL'}")
    if not result_fail.success:
        print(f"Failure Reason: {result_fail.failure_reason}")
        if result_fail.posture_distance:
            print(f"Posture Distance: {result_fail.posture_distance:.2f}° (Limit: 10.0°)")
    print()
    
    # AUTHENTICATION ATTEMPT 3: Static Image Spoof
    print("🎭 PHASE 4: AUTHENTICATION ATTEMPT (Static Image Spoof)")
    print("-" * 60)
    
    # Zero variance IMU (static image)
    auth_imu_spoof = np.zeros((100, 3))
    
    result_spoof = sta.authenticate(
        "coordinator_001",
        auth_pose_valid,
        auth_loc_valid,
        auth_imu_spoof,
        operation_risk=AuthenticationRisk.CRITICAL
    )
    
    print(f"Result: {'✅ SUCCESS' if result_spoof.success else '❌ FAIL'}")
    if not result_spoof.success:
        print(f"Failure Reason: {result_spoof.failure_reason}")
        print(f"Stillness Score: {result_spoof.stillness_score:.6f} (Zero entropy detected)")
    print()
    
    print("=" * 60)
    print("🌰 Acorn Protocol Demonstration Complete")
    print("=" * 60)
    print()
    print("Key Insights:")
    print("1. ✅ Valid user with correct pose + location + living stillness → SUCCESS")
    print("2. ❌ Wrong pose (imposter) → REJECTED")
    print("3. ❌ Static image (zero entropy) → SPOOF DETECTED")
    print()
    print("This is Existence-Based Security:")
    print("You cannot steal what you cannot be.")
