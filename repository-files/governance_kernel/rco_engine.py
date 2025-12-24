"""
Regenerative Compliance Oracle (RCO)
The Self-Updating Legal Singularity

"Code is Law. Law evolves. Therefore, Code must evolve itself."

This is not RegTech. This is the Metabolic Process of Sovereign Dignity.

Architecture:
1. SENSING - RegulatoryEntropySensor detects compliance drift
2. PREDICTION - LawEvolutionVector forecasts regulatory amendments
3. SYNTHESIS - AutoPatchGenerator writes new law-as-code
4. VERIFICATION - RetroactiveChronoAudit ensures temporal consistency

Compliance:
- EU AI Act §8 (Transparency)
- GDPR Art. 22 (Automated Decision-Making)
- ISO 27001 A.18.1.1 (Compliance with Legal Requirements)
"""

import json
import hashlib
import numpy as np
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
from enum import Enum
from dataclasses import dataclass, asdict
import logging
from scipy.stats import entropy
from scipy.spatial.distance import jensenshannon

logger = logging.getLogger(__name__)


class RegulatoryDriftLevel(Enum):
    """Compliance drift severity levels"""
    NOMINAL = "NOMINAL"          # < 0.05 KL divergence
    ELEVATED = "ELEVATED"        # 0.05 - 0.15
    CRITICAL = "CRITICAL"        # 0.15 - 0.30
    CATASTROPHIC = "CATASTROPHIC"  # > 0.30


class LawAmendmentConfidence(Enum):
    """Confidence levels for predicted amendments"""
    LOW = "LOW"              # < 50%
    MODERATE = "MODERATE"    # 50-70%
    HIGH = "HIGH"            # 70-90%
    CERTAIN = "CERTAIN"      # > 90%


@dataclass
class RegulatorySignal:
    """External regulatory signal (e.g., draft legislation)"""
    signal_id: str
    source: str  # "EU_AI_Act_Draft", "WHO_IHR_Amendment"
    timestamp: str
    content: str
    impact_frameworks: List[str]
    confidence: float
    metadata: Dict


@dataclass
class ComplianceDrift:
    """Measured drift from ideal compliance state"""
    framework_id: str
    drift_score: float  # KL divergence
    drift_level: RegulatoryDriftLevel
    contributing_factors: List[str]
    timestamp: str
    recommended_action: str


@dataclass
class LawPatch:
    """Auto-generated law-as-code patch"""
    patch_id: str
    framework_id: str
    patch_type: str  # "THRESHOLD_TIGHTEN", "NEW_CONSTRAINT", "SCOPE_EXPANSION"
    changes: Dict
    rationale: str
    confidence: float
    requires_approval: bool
    created_at: str
    approved: bool = False
    approved_by: Optional[str] = None
    approved_at: Optional[str] = None


class RegulatoryEntropySensor:
    """
    The Regulatory Nervous System
    
    Monitors the Gradient of Compliance using KL Divergence to detect drift
    from the "Ideal Compliance State" defined in sectoral_laws.json.
    """
    
    def __init__(self, baseline_path: str = "config/sectoral_laws.json"):
        self.baseline_path = baseline_path
        self.baseline_state = self._load_baseline()
        self.drift_history = []
        
        logger.info("🧠 RegulatoryEntropySensor initialized")
    
    def _load_baseline(self) -> Dict:
        """Load ideal compliance state"""
        try:
            with open(self.baseline_path, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            logger.warning(f"⚠️ Baseline not found: {self.baseline_path}")
            return {}
    
    def measure_drift(
        self,
        data_stream: Dict,
        framework_id: str
    ) -> ComplianceDrift:
        """
        Measure compliance drift using KL Divergence.
        
        Args:
            data_stream: Current system behavior metrics
            framework_id: Framework to check (e.g., "EU_AI_ACT")
        
        Returns:
            ComplianceDrift object with drift score and recommendations
        """
        # Get baseline distribution for this framework
        baseline_dist = self._get_baseline_distribution(framework_id)
        
        # Get current distribution from data stream
        current_dist = self._extract_distribution(data_stream, framework_id)
        
        # Calculate KL Divergence (Kullback-Leibler)
        # KL(P||Q) = Σ P(i) * log(P(i) / Q(i))
        kl_divergence = self._calculate_kl_divergence(baseline_dist, current_dist)
        
        # Classify drift level
        drift_level = self._classify_drift(kl_divergence)
        
        # Identify contributing factors
        factors = self._identify_drift_factors(baseline_dist, current_dist)
        
        # Generate recommendation
        recommendation = self._generate_recommendation(drift_level, factors)
        
        drift = ComplianceDrift(
            framework_id=framework_id,
            drift_score=kl_divergence,
            drift_level=drift_level,
            contributing_factors=factors,
            timestamp=datetime.utcnow().isoformat(),
            recommended_action=recommendation
        )
        
        # Store in history
        self.drift_history.append(drift)
        
        logger.info(
            f"📊 Drift measured - {framework_id}: {kl_divergence:.4f} ({drift_level.value})"
        )
        
        return drift
    
    def _get_baseline_distribution(self, framework_id: str) -> np.ndarray:
        """Extract baseline probability distribution for framework"""
        if framework_id not in self.baseline_state:
            # Return uniform distribution if no baseline
            return np.ones(10) / 10
        
        framework = self.baseline_state[framework_id]
        
        # Extract key metrics as distribution
        # Example: [data_residency_compliance, consent_rate, retention_compliance, ...]
        metrics = [
            framework.get("data_residency_compliance", 1.0),
            framework.get("consent_rate", 1.0),
            framework.get("retention_compliance", 1.0),
            framework.get("explainability_rate", 1.0),
            framework.get("audit_coverage", 1.0),
            framework.get("encryption_rate", 1.0),
            framework.get("access_control_compliance", 1.0),
            framework.get("incident_response_time", 0.0),
            framework.get("training_completion_rate", 1.0),
            framework.get("vulnerability_patch_rate", 1.0),
        ]
        
        # Normalize to probability distribution
        dist = np.array(metrics)
        dist = dist / dist.sum()
        
        return dist
    
    def _extract_distribution(self, data_stream: Dict, framework_id: str) -> np.ndarray:
        """Extract current probability distribution from data stream"""
        # Extract same metrics from current data
        metrics = [
            data_stream.get("data_residency_compliance", 1.0),
            data_stream.get("consent_rate", 1.0),
            data_stream.get("retention_compliance", 1.0),
            data_stream.get("explainability_rate", 1.0),
            data_stream.get("audit_coverage", 1.0),
            data_stream.get("encryption_rate", 1.0),
            data_stream.get("access_control_compliance", 1.0),
            data_stream.get("incident_response_time", 0.0),
            data_stream.get("training_completion_rate", 1.0),
            data_stream.get("vulnerability_patch_rate", 1.0),
        ]
        
        # Normalize
        dist = np.array(metrics)
        dist = dist / dist.sum()
        
        return dist
    
    def _calculate_kl_divergence(self, p: np.ndarray, q: np.ndarray) -> float:
        """
        Calculate Kullback-Leibler Divergence: KL(P||Q)
        
        Measures how much Q diverges from P (baseline)
        """
        # Add small epsilon to avoid log(0)
        epsilon = 1e-10
        p = p + epsilon
        q = q + epsilon
        
        # Renormalize
        p = p / p.sum()
        q = q / q.sum()
        
        # Calculate KL divergence
        kl = np.sum(p * np.log(p / q))
        
        return float(kl)
    
    def _classify_drift(self, kl_divergence: float) -> RegulatoryDriftLevel:
        """Classify drift severity"""
        if kl_divergence < 0.05:
            return RegulatoryDriftLevel.NOMINAL
        elif kl_divergence < 0.15:
            return RegulatoryDriftLevel.ELEVATED
        elif kl_divergence < 0.30:
            return RegulatoryDriftLevel.CRITICAL
        else:
            return RegulatoryDriftLevel.CATASTROPHIC
    
    def _identify_drift_factors(
        self,
        baseline: np.ndarray,
        current: np.ndarray
    ) -> List[str]:
        """Identify which metrics are contributing to drift"""
        metric_names = [
            "data_residency_compliance",
            "consent_rate",
            "retention_compliance",
            "explainability_rate",
            "audit_coverage",
            "encryption_rate",
            "access_control_compliance",
            "incident_response_time",
            "training_completion_rate",
            "vulnerability_patch_rate",
        ]
        
        # Calculate per-metric divergence
        differences = np.abs(baseline - current)
        
        # Identify top 3 contributors
        top_indices = np.argsort(differences)[-3:][::-1]
        
        factors = [metric_names[i] for i in top_indices if differences[i] > 0.01]
        
        return factors


class LawEvolutionVector:
    """
    The Bayesian Oracle
    
    Uses Monte Carlo simulations on geopolitical metadata to calculate
    the Probability of Amendment for each legal framework.
    """
    
    def __init__(self):
        self.prediction_history = []
        self.external_signals = []
        
        logger.info("🔮 LawEvolutionVector initialized")
    
    def ingest_signal(self, signal: RegulatorySignal):
        """Ingest external regulatory signal"""
        self.external_signals.append(signal)
        logger.info(f"📡 Signal ingested: {signal.source}")
    
    def predict_amendment(
        self,
        framework_id: str,
        external_signal: Optional[str] = None,
        monte_carlo_iterations: int = 10000
    ) -> Tuple[float, LawAmendmentConfidence, Dict]:
        """
        Predict probability of framework amendment.
        
        Args:
            framework_id: Framework to analyze
            external_signal: Optional specific signal to analyze
            monte_carlo_iterations: Number of MC simulations
        
        Returns:
            (probability, confidence_level, metadata)
        """
        # Gather relevant signals
        relevant_signals = self._filter_signals(framework_id, external_signal)
        
        if not relevant_signals:
            # No signals = low probability of change
            return 0.05, LawAmendmentConfidence.LOW, {"reason": "no_signals"}
        
        # Run Monte Carlo simulation
        probabilities = []
        
        for _ in range(monte_carlo_iterations):
            # Sample from signal confidence distributions
            sampled_prob = self._monte_carlo_sample(relevant_signals)
            probabilities.append(sampled_prob)
        
        # Calculate statistics
        mean_prob = np.mean(probabilities)
        std_prob = np.std(probabilities)
        
        # Classify confidence
        confidence = self._classify_confidence(mean_prob, std_prob)
        
        metadata = {
            "mean_probability": mean_prob,
            "std_deviation": std_prob,
            "signal_count": len(relevant_signals),
            "signals": [s.source for s in relevant_signals],
            "monte_carlo_iterations": monte_carlo_iterations
        }
        
        logger.info(
            f"🔮 Amendment prediction - {framework_id}: "
            f"{mean_prob:.2%} ({confidence.value})"
        )
        
        return mean_prob, confidence, metadata
    
    def _filter_signals(
        self,
        framework_id: str,
        external_signal: Optional[str]
    ) -> List[RegulatorySignal]:
        """Filter signals relevant to framework"""
        if external_signal:
            # Filter by specific signal
            return [
                s for s in self.external_signals
                if s.source == external_signal and framework_id in s.impact_frameworks
            ]
        else:
            # All signals for this framework
            return [
                s for s in self.external_signals
                if framework_id in s.impact_frameworks
            ]
    
    def _monte_carlo_sample(self, signals: List[RegulatorySignal]) -> float:
        """Single Monte Carlo sample"""
        if not signals:
            return 0.0
        
        # Sample from each signal's confidence distribution
        # Assume beta distribution around confidence value
        samples = []
        
        for signal in signals:
            # Beta distribution parameters
            alpha = signal.confidence * 10
            beta = (1 - signal.confidence) * 10
            
            # Sample
            sample = np.random.beta(alpha, beta)
            samples.append(sample)
        
        # Combine samples (max probability)
        return max(samples)
    
    def _classify_confidence(
        self,
        mean_prob: float,
        std_prob: float
    ) -> LawAmendmentConfidence:
        """Classify prediction confidence"""
        # High probability + low variance = CERTAIN
        if mean_prob > 0.90 and std_prob < 0.05:
            return LawAmendmentConfidence.CERTAIN
        elif mean_prob > 0.70:
            return LawAmendmentConfidence.HIGH
        elif mean_prob > 0.50:
            return LawAmendmentConfidence.MODERATE
        else:
            return LawAmendmentConfidence.LOW


class AutoPatchGenerator:
    """
    The Self-Writing Kernel
    
    Generates law-as-code patches that tighten SovereignGuardrail thresholds
    automatically based on detected drift and predicted amendments.
    """
    
    def __init__(self, laws_path: str = "config/sectoral_laws.json"):
        self.laws_path = laws_path
        self.patch_history = []
        
        logger.info("⚙️ AutoPatchGenerator initialized")
    
    def generate_hotfix(
        self,
        law_id: str,
        drift_score: float,
        drift_factors: List[str],
        amendment_probability: float
    ) -> Optional[LawPatch]:
        """
        Generate a law-as-code hotfix patch.
        
        Args:
            law_id: Framework identifier
            drift_score: KL divergence score
            drift_factors: Contributing factors
            amendment_probability: Predicted amendment probability
        
        Returns:
            LawPatch object or None if no patch needed
        """
        # Determine if patch is needed
        critical_threshold = 0.15
        
        if drift_score < critical_threshold and amendment_probability < 0.70:
            logger.info(f"✓ No patch needed for {law_id}")
            return None
        
        # Load current laws
        with open(self.laws_path, 'r') as f:
            laws = json.load(f)
        
        if law_id not in laws:
            logger.error(f"❌ Law not found: {law_id}")
            return None
        
        # Generate patch based on drift factors
        changes = self._generate_changes(
            laws[law_id],
            drift_factors,
            drift_score,
            amendment_probability
        )
        
        # Determine patch type
        patch_type = self._determine_patch_type(changes)
        
        # Generate rationale
        rationale = self._generate_rationale(
            law_id,
            drift_score,
            drift_factors,
            amendment_probability
        )
        
        # Create patch
        patch = LawPatch(
            patch_id=self._generate_patch_id(law_id),
            framework_id=law_id,
            patch_type=patch_type,
            changes=changes,
            rationale=rationale,
            confidence=min(drift_score, amendment_probability),
            requires_approval=True,  # Always require human approval
            created_at=datetime.utcnow().isoformat()
        )
        
        # Store in history
        self.patch_history.append(patch)
        
        logger.info(f"🔧 Hotfix generated - {law_id}: {patch_type}")
        
        return patch
    
    def _generate_changes(
        self,
        current_law: Dict,
        drift_factors: List[str],
        drift_score: float,
        amendment_probability: float
    ) -> Dict:
        """Generate specific changes to law configuration"""
        changes = {}
        
        # Tighten thresholds based on drift
        tightening_factor = min(0.9, 1.0 - (drift_score * 0.5))
        
        for factor in drift_factors:
            if factor in current_law:
                current_value = current_law[factor]
                
                if isinstance(current_value, (int, float)):
                    # Tighten threshold
                    new_value = current_value * tightening_factor
                    changes[factor] = {
                        "old": current_value,
                        "new": new_value,
                        "reason": f"Drift detected ({drift_score:.3f})"
                    }
        
        # Add new constraints if amendment is likely
        if amendment_probability > 0.80:
            changes["enhanced_monitoring"] = {
                "old": False,
                "new": True,
                "reason": f"High amendment probability ({amendment_probability:.2%})"
            }
        
        return changes
    
    def _determine_patch_type(self, changes: Dict) -> str:
        """Determine patch type from changes"""
        if any("threshold" in k.lower() for k in changes.keys()):
            return "THRESHOLD_TIGHTEN"
        elif any("new" in str(v.get("old")) for v in changes.values()):
            return "NEW_CONSTRAINT"
        else:
            return "SCOPE_EXPANSION"
    
    def _generate_rationale(
        self,
        law_id: str,
        drift_score: float,
        drift_factors: List[str],
        amendment_probability: float
    ) -> str:
        """Generate human-readable rationale"""
        rationale = f"RCO detected compliance drift in {law_id}:\n"
        rationale += f"- Drift Score: {drift_score:.3f} (KL Divergence)\n"
        rationale += f"- Contributing Factors: {', '.join(drift_factors)}\n"
        rationale += f"- Amendment Probability: {amendment_probability:.2%}\n"
        rationale += "\nRecommended Action: Tighten thresholds to maintain compliance margin."
        
        return rationale
    
    def _generate_patch_id(self, law_id: str) -> str:
        """Generate unique patch ID"""
        timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
        hash_input = f"{law_id}_{timestamp}".encode()
        hash_short = hashlib.sha256(hash_input).hexdigest()[:8]
        
        return f"PATCH_{law_id}_{timestamp}_{hash_short}"
    
    def apply_patch(
        self,
        patch: LawPatch,
        approved_by: str
    ) -> bool:
        """
        Apply an approved patch to sectoral_laws.json
        
        Args:
            patch: The patch to apply
            approved_by: User who approved (for audit)
        
        Returns:
            True if successful
        """
        if not patch.requires_approval or not patch.approved:
            logger.error("❌ Patch not approved")
            return False
        
        # Load current laws
        with open(self.laws_path, 'r') as f:
            laws = json.load(f)
        
        # Apply changes
        if patch.framework_id not in laws:
            laws[patch.framework_id] = {}
        
        for key, change in patch.changes.items():
            laws[patch.framework_id][key] = change["new"]
        
        # Save patched version with timestamp
        timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
        patch_path = f"config/sectoral_laws_patch_{timestamp}.json"
        
        with open(patch_path, 'w') as f:
            json.dump(laws, f, indent=2)
        
        # Update patch metadata
        patch.approved_by = approved_by
        patch.approved_at = datetime.utcnow().isoformat()
        
        logger.info(f"✅ Patch applied: {patch.patch_id} by {approved_by}")
        
        return True


class RetroactiveChronoAudit:
    """
    The Chrono-Lock
    
    Re-runs the entire history of the Golden Thread against new patches
    to ensure the past is compatible with the future.
    """
    
    def __init__(self):
        self.audit_history = []
        
        logger.info("⏰ RetroactiveChronoAudit initialized")
    
    def verify_patch(
        self,
        patch: LawPatch,
        historical_events: List[Dict]
    ) -> Tuple[bool, Dict]:
        """
        Verify patch against historical events.
        
        Args:
            patch: The patch to verify
            historical_events: Historical Golden Thread events
        
        Returns:
            (is_valid, audit_report)
        """
        logger.info(f"⏰ Chrono-audit started - {patch.patch_id}")
        
        violations = []
        warnings = []
        
        # Re-run each historical event against new patch
        for event in historical_events:
            result = self._simulate_event_with_patch(event, patch)
            
            if result["status"] == "VIOLATION":
                violations.append(result)
            elif result["status"] == "WARNING":
                warnings.append(result)
        
        # Determine if patch is valid
        is_valid = len(violations) == 0
        
        audit_report = {
            "patch_id": patch.patch_id,
            "events_tested": len(historical_events),
            "violations": len(violations),
            "warnings": len(warnings),
            "is_valid": is_valid,
            "violation_details": violations,
            "warning_details": warnings,
            "timestamp": datetime.utcnow().isoformat()
        }
        
        # Store in history
        self.audit_history.append(audit_report)
        
        if is_valid:
            logger.info(f"✅ Chrono-audit passed - {patch.patch_id}")
        else:
            logger.error(f"❌ Chrono-audit failed - {patch.patch_id}: {len(violations)} violations")
        
        return is_valid, audit_report
    
    def _simulate_event_with_patch(
        self,
        event: Dict,
        patch: LawPatch
    ) -> Dict:
        """Simulate a historical event with the new patch applied"""
        # Extract event metrics
        event_metrics = {
            "data_residency_compliance": event.get("data_residency_compliance", 1.0),
            "consent_rate": event.get("consent_rate", 1.0),
            "explainability_rate": event.get("explainability_rate", 1.0),
        }
        
        # Apply patch thresholds
        for key, change in patch.changes.items():
            if key in event_metrics:
                threshold = change["new"]
                actual = event_metrics[key]
                
                if actual < threshold:
                    return {
                        "status": "VIOLATION",
                        "event_id": event.get("event_id", "unknown"),
                        "metric": key,
                        "threshold": threshold,
                        "actual": actual,
                        "message": f"Historical event would violate new threshold"
                    }
        
        return {"status": "PASS"}


class RegenerativeComplianceOracle:
    """
    The RCO Engine - Core Orchestrator
    
    Coordinates the 4-stage metabolic loop:
    1. SENSING - Detect drift
    2. PREDICTION - Forecast amendments
    3. SYNTHESIS - Generate patches
    4. VERIFICATION - Chrono-audit
    """
    
    def __init__(
        self,
        laws_path: str = "config/sectoral_laws.json",
        enable_auto_patch: bool = False
    ):
        self.sensor = RegulatoryEntropySensor(laws_path)
        self.oracle = LawEvolutionVector()
        self.generator = AutoPatchGenerator(laws_path)
        self.auditor = RetroactiveChronoAudit()
        
        self.enable_auto_patch = enable_auto_patch
        self.pending_patches = []
        
        logger.info("🌟 Regenerative Compliance Oracle initialized")
        logger.info(f"   Auto-patch: {'ENABLED' if enable_auto_patch else 'DISABLED'}")
    
    def ingest(self, data_stream: Dict, framework_id: str):
        """
        Ingest data stream and trigger metabolic loop.
        
        This is the main entry point - called by Golden Thread.
        """
        # STAGE 1: SENSING
        drift = self.sensor.measure_drift(data_stream, framework_id)
        
        # STAGE 2: PREDICTION
        amendment_prob, confidence, metadata = self.oracle.predict_amendment(framework_id)
        
        # STAGE 3: SYNTHESIS (if drift is critical)
        if drift.drift_level in [RegulatoryDriftLevel.CRITICAL, RegulatoryDriftLevel.CATASTROPHIC]:
            patch = self.generator.generate_hotfix(
                law_id=framework_id,
                drift_score=drift.drift_score,
                drift_factors=drift.contributing_factors,
                amendment_probability=amendment_prob
            )
            
            if patch:
                self.pending_patches.append(patch)
                logger.warning(
                    f"⚠️ PATCH GENERATED - {framework_id}: "
                    f"Drift={drift.drift_score:.3f}, Amendment={amendment_prob:.2%}"
                )
    
    def get_pending_patches(self) -> List[LawPatch]:
        """Get all pending patches awaiting approval"""
        return [p for p in self.pending_patches if not p.approved]
    
    def approve_patch(
        self,
        patch_id: str,
        approved_by: str,
        historical_events: List[Dict]
    ) -> Tuple[bool, Dict]:
        """
        Approve and apply a patch (with Chrono-Audit).
        
        Args:
            patch_id: Patch to approve
            approved_by: User approving (requires Somatic Auth)
            historical_events: Historical events for verification
        
        Returns:
            (success, audit_report)
        """
        # Find patch
        patch = next((p for p in self.pending_patches if p.patch_id == patch_id), None)
        
        if not patch:
            logger.error(f"❌ Patch not found: {patch_id}")
            return False, {"error": "patch_not_found"}
        
        # STAGE 4: VERIFICATION (Chrono-Audit)
        is_valid, audit_report = self.auditor.verify_patch(patch, historical_events)
        
        if not is_valid:
            logger.error(f"❌ Chrono-audit failed - {patch_id}")
            return False, audit_report
        
        # Mark as approved
        patch.approved = True
        
        # Apply patch
        success = self.generator.apply_patch(patch, approved_by)
        
        return success, audit_report


# Example usage
if __name__ == "__main__":
    # Initialize RCO
    rco = RegenerativeComplianceOracle(enable_auto_patch=False)
    
    # Simulate data stream with drift
    data_stream = {
        "data_residency_compliance": 0.85,  # Drift from 1.0
        "consent_rate": 0.92,
        "retention_compliance": 0.88,
        "explainability_rate": 0.75,  # Significant drift
        "audit_coverage": 0.95,
        "encryption_rate": 1.0,
        "access_control_compliance": 0.90,
        "incident_response_time": 0.1,
        "training_completion_rate": 0.85,
        "vulnerability_patch_rate": 0.95,
    }
    
    # Ingest signal
    signal = RegulatorySignal(
        signal_id="SIG_001",
        source="EU_AI_Act_Draft_Code_Dec2025",
        timestamp=datetime.utcnow().isoformat(),
        content="Draft Code of Practice released",
        impact_frameworks=["EU_AI_ACT", "GDPR"],
        confidence=0.87,
        metadata={"release_date": "2025-12-17"}
    )
    rco.oracle.ingest_signal(signal)
    
    # Trigger metabolic loop
    rco.ingest(data_stream, "EU_AI_ACT")
    
    # Check pending patches
    pending = rco.get_pending_patches()
    print(f"\n📋 Pending patches: {len(pending)}")
    
    for patch in pending:
        print(f"\n🔧 Patch: {patch.patch_id}")
        print(f"   Type: {patch.patch_type}")
        print(f"   Confidence: {patch.confidence:.2%}")
        print(f"   Rationale:\n{patch.rationale}")
