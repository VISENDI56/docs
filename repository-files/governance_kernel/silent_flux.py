"""
IP-04: Silent Flux - Anxiety-Regulated AI Output

Monitors operator stress levels and automatically adjusts AI output verbosity
to prevent cognitive overload during emergencies.

Stress is calculated via:
- Keystroke cadence analysis
- Error rate monitoring
- Response time patterns
- UI interaction patterns

When stress exceeds threshold, the system transitions to "Essential-only" mode,
reducing information density and preventing catastrophic human error.
"""

import time
import numpy as np
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
from datetime import datetime, timedelta
from enum import Enum
import logging

logger = logging.getLogger(__name__)


class StressLevel(Enum):
    """Operator stress levels"""
    CALM = "calm"              # 0.0 - 0.3
    FOCUSED = "focused"        # 0.3 - 0.5
    ELEVATED = "elevated"      # 0.5 - 0.7
    HIGH = "high"              # 0.7 - 0.85
    CRITICAL = "critical"      # 0.85 - 1.0


class OutputMode(Enum):
    """AI output verbosity modes"""
    FULL = "full"                    # All details, explanations, context
    STANDARD = "standard"            # Normal operation
    CONCISE = "concise"              # Reduced verbosity
    ESSENTIAL = "essential"          # Critical information only
    EMERGENCY = "emergency"          # Absolute minimum, action-oriented


@dataclass
class StressMetrics:
    """Operator stress metrics"""
    keystroke_cadence: float        # Keystrokes per second
    error_rate: float               # Errors per action
    response_time: float            # Average response time (seconds)
    ui_interaction_rate: float      # Interactions per minute
    timestamp: datetime
    
    def calculate_stress_index(self) -> float:
        """
        Calculate composite stress index (0.0 - 1.0)
        
        Higher values indicate higher stress:
        - Very fast or very slow keystrokes = stress
        - High error rate = stress
        - Very fast or very slow responses = stress
        - Erratic UI interaction = stress
        """
        # Normalize keystroke cadence (optimal: 3-5 keys/sec)
        optimal_cadence = 4.0
        cadence_stress = min(abs(self.keystroke_cadence - optimal_cadence) / optimal_cadence, 1.0)
        
        # Error rate (0-1, higher = more stress)
        error_stress = min(self.error_rate, 1.0)
        
        # Response time (optimal: 1-3 seconds)
        optimal_response = 2.0
        response_stress = min(abs(self.response_time - optimal_response) / optimal_response, 1.0)
        
        # UI interaction rate (optimal: 10-20 per minute)
        optimal_interaction = 15.0
        interaction_stress = min(abs(self.ui_interaction_rate - optimal_interaction) / optimal_interaction, 1.0)
        
        # Weighted composite
        stress_index = (
            0.3 * cadence_stress +
            0.4 * error_stress +
            0.2 * response_stress +
            0.1 * interaction_stress
        )
        
        return min(stress_index, 1.0)


@dataclass
class OutputConfig:
    """Configuration for AI output based on stress level"""
    mode: OutputMode
    max_tokens: int
    show_explanations: bool
    show_alternatives: bool
    show_confidence: bool
    show_sources: bool
    alert_style: str  # "detailed", "standard", "minimal", "critical"
    
    @staticmethod
    def for_stress_level(stress_level: StressLevel) -> 'OutputConfig':
        """Get output configuration for stress level"""
        configs = {
            StressLevel.CALM: OutputConfig(
                mode=OutputMode.FULL,
                max_tokens=2000,
                show_explanations=True,
                show_alternatives=True,
                show_confidence=True,
                show_sources=True,
                alert_style="detailed"
            ),
            StressLevel.FOCUSED: OutputConfig(
                mode=OutputMode.STANDARD,
                max_tokens=1000,
                show_explanations=True,
                show_alternatives=True,
                show_confidence=True,
                show_sources=False,
                alert_style="standard"
            ),
            StressLevel.ELEVATED: OutputConfig(
                mode=OutputMode.CONCISE,
                max_tokens=500,
                show_explanations=False,
                show_alternatives=True,
                show_confidence=True,
                show_sources=False,
                alert_style="standard"
            ),
            StressLevel.HIGH: OutputConfig(
                mode=OutputMode.ESSENTIAL,
                max_tokens=200,
                show_explanations=False,
                show_alternatives=False,
                show_confidence=True,
                show_sources=False,
                alert_style="minimal"
            ),
            StressLevel.CRITICAL: OutputConfig(
                mode=OutputMode.EMERGENCY,
                max_tokens=100,
                show_explanations=False,
                show_alternatives=False,
                show_confidence=False,
                show_sources=False,
                alert_style="critical"
            ),
        }
        return configs[stress_level]


class SilentFlux:
    """
    IP-04: Silent Flux - Anxiety-Regulated AI Output
    
    Monitors operator stress and dynamically adjusts AI output to prevent
    cognitive overload during emergencies.
    """
    
    def __init__(
        self,
        stress_threshold: float = 0.7,
        window_size: int = 10,
        enable_auto_regulation: bool = True
    ):
        """
        Initialize Silent Flux monitor
        
        Args:
            stress_threshold: Stress level to trigger output reduction (0.0-1.0)
            window_size: Number of recent metrics to consider
            enable_auto_regulation: Automatically adjust output based on stress
        """
        self.stress_threshold = stress_threshold
        self.window_size = window_size
        self.enable_auto_regulation = enable_auto_regulation
        
        # Metrics history
        self.metrics_history: List[StressMetrics] = []
        
        # Current state
        self.current_stress_level = StressLevel.CALM
        self.current_output_config = OutputConfig.for_stress_level(StressLevel.CALM)
        
        # Keystroke tracking
        self.keystroke_times: List[float] = []
        self.error_count = 0
        self.action_count = 0
        self.response_times: List[float] = []
        self.interaction_times: List[float] = []
        
        logger.info(f"⚡ Silent Flux initialized - Threshold: {stress_threshold}")
    
    def record_keystroke(self, timestamp: Optional[float] = None):
        """Record a keystroke event"""
        if timestamp is None:
            timestamp = time.time()
        
        self.keystroke_times.append(timestamp)
        
        # Keep only recent keystrokes (last 10 seconds)
        cutoff = timestamp - 10.0
        self.keystroke_times = [t for t in self.keystroke_times if t > cutoff]
    
    def record_error(self):
        """Record an error event"""
        self.error_count += 1
        self.action_count += 1
    
    def record_action(self):
        """Record a successful action"""
        self.action_count += 1
    
    def record_response_time(self, response_time: float):
        """Record response time for an action"""
        self.response_times.append(response_time)
        
        # Keep only recent responses (last 20)
        if len(self.response_times) > 20:
            self.response_times = self.response_times[-20:]
    
    def record_interaction(self, timestamp: Optional[float] = None):
        """Record a UI interaction"""
        if timestamp is None:
            timestamp = time.time()
        
        self.interaction_times.append(timestamp)
        
        # Keep only recent interactions (last 60 seconds)
        cutoff = timestamp - 60.0
        self.interaction_times = [t for t in self.interaction_times if t > cutoff]
    
    def calculate_current_metrics(self) -> StressMetrics:
        """Calculate current stress metrics"""
        now = time.time()
        
        # Keystroke cadence (keys per second)
        if len(self.keystroke_times) >= 2:
            time_span = self.keystroke_times[-1] - self.keystroke_times[0]
            keystroke_cadence = len(self.keystroke_times) / max(time_span, 0.1)
        else:
            keystroke_cadence = 0.0
        
        # Error rate
        error_rate = self.error_count / max(self.action_count, 1)
        
        # Average response time
        if self.response_times:
            response_time = np.mean(self.response_times)
        else:
            response_time = 2.0  # Default optimal
        
        # UI interaction rate (per minute)
        if len(self.interaction_times) >= 2:
            time_span = (self.interaction_times[-1] - self.interaction_times[0]) / 60.0
            ui_interaction_rate = len(self.interaction_times) / max(time_span, 0.1)
        else:
            ui_interaction_rate = 15.0  # Default optimal
        
        return StressMetrics(
            keystroke_cadence=keystroke_cadence,
            error_rate=error_rate,
            response_time=response_time,
            ui_interaction_rate=ui_interaction_rate,
            timestamp=datetime.utcnow()
        )
    
    def update_stress_level(self) -> Tuple[StressLevel, float]:
        """
        Update current stress level based on recent metrics
        
        Returns:
            (stress_level, stress_index)
        """
        # Calculate current metrics
        metrics = self.calculate_current_metrics()
        stress_index = metrics.calculate_stress_index()
        
        # Add to history
        self.metrics_history.append(metrics)
        if len(self.metrics_history) > self.window_size:
            self.metrics_history = self.metrics_history[-self.window_size:]
        
        # Calculate moving average stress
        if len(self.metrics_history) >= 3:
            recent_stress = [m.calculate_stress_index() for m in self.metrics_history[-3:]]
            avg_stress = np.mean(recent_stress)
        else:
            avg_stress = stress_index
        
        # Determine stress level
        if avg_stress < 0.3:
            stress_level = StressLevel.CALM
        elif avg_stress < 0.5:
            stress_level = StressLevel.FOCUSED
        elif avg_stress < 0.7:
            stress_level = StressLevel.ELEVATED
        elif avg_stress < 0.85:
            stress_level = StressLevel.HIGH
        else:
            stress_level = StressLevel.CRITICAL
        
        # Update current state
        old_level = self.current_stress_level
        self.current_stress_level = stress_level
        
        # Update output configuration if auto-regulation enabled
        if self.enable_auto_regulation:
            self.current_output_config = OutputConfig.for_stress_level(stress_level)
            
            if old_level != stress_level:
                logger.info(
                    f"⚡ Silent Flux: Stress level changed {old_level.value} → {stress_level.value} "
                    f"(index: {avg_stress:.2f}, mode: {self.current_output_config.mode.value})"
                )
        
        return stress_level, avg_stress
    
    def regulate_output(self, text: str, force_mode: Optional[OutputMode] = None) -> str:
        """
        Regulate AI output based on current stress level
        
        Args:
            text: Original AI output
            force_mode: Force specific output mode (overrides auto-regulation)
        
        Returns:
            Regulated output text
        """
        # Determine output mode
        if force_mode:
            config = OutputConfig.for_stress_level(
                {
                    OutputMode.FULL: StressLevel.CALM,
                    OutputMode.STANDARD: StressLevel.FOCUSED,
                    OutputMode.CONCISE: StressLevel.ELEVATED,
                    OutputMode.ESSENTIAL: StressLevel.HIGH,
                    OutputMode.EMERGENCY: StressLevel.CRITICAL,
                }[force_mode]
            )
        else:
            config = self.current_output_config
        
        # Apply token limit
        words = text.split()
        if len(words) > config.max_tokens:
            # Truncate to essential information
            text = ' '.join(words[:config.max_tokens]) + "..."
        
        # Remove explanations if needed
        if not config.show_explanations:
            # Remove sentences with explanation markers
            sentences = text.split('. ')
            filtered = [
                s for s in sentences 
                if not any(marker in s.lower() for marker in [
                    'because', 'this is', 'the reason', 'explanation', 'note that'
                ])
            ]
            text = '. '.join(filtered)
        
        return text
    
    def get_alert_format(self, alert_data: Dict) -> Dict:
        """
        Format alert based on current stress level
        
        Args:
            alert_data: Raw alert data
        
        Returns:
            Formatted alert appropriate for stress level
        """
        config = self.current_output_config
        
        if config.alert_style == "critical":
            # Emergency mode: Action only
            return {
                "action": alert_data.get("action", "UNKNOWN"),
                "priority": alert_data.get("priority", "HIGH")
            }
        
        elif config.alert_style == "minimal":
            # Essential mode: Action + location
            return {
                "action": alert_data.get("action", "UNKNOWN"),
                "location": alert_data.get("location", "UNKNOWN"),
                "priority": alert_data.get("priority", "HIGH")
            }
        
        elif config.alert_style == "standard":
            # Standard mode: Core information
            return {
                "action": alert_data.get("action"),
                "location": alert_data.get("location"),
                "priority": alert_data.get("priority"),
                "confidence": alert_data.get("confidence") if config.show_confidence else None,
                "timestamp": alert_data.get("timestamp")
            }
        
        else:  # detailed
            # Full mode: All information
            return alert_data
    
    def get_status(self) -> Dict:
        """Get current Silent Flux status"""
        stress_level, stress_index = self.update_stress_level()
        
        return {
            "stress_level": stress_level.value,
            "stress_index": stress_index,
            "output_mode": self.current_output_config.mode.value,
            "max_tokens": self.current_output_config.max_tokens,
            "auto_regulation_enabled": self.enable_auto_regulation,
            "metrics": {
                "keystroke_cadence": self.calculate_current_metrics().keystroke_cadence,
                "error_rate": self.calculate_current_metrics().error_rate,
                "response_time": self.calculate_current_metrics().response_time,
                "ui_interaction_rate": self.calculate_current_metrics().ui_interaction_rate
            }
        }
    
    def reset_metrics(self):
        """Reset all metrics (e.g., at shift change)"""
        self.keystroke_times.clear()
        self.error_count = 0
        self.action_count = 0
        self.response_times.clear()
        self.interaction_times.clear()
        self.metrics_history.clear()
        
        self.current_stress_level = StressLevel.CALM
        self.current_output_config = OutputConfig.for_stress_level(StressLevel.CALM)
        
        logger.info("⚡ Silent Flux: Metrics reset")


# Singleton instance
_silent_flux = None

def get_silent_flux() -> SilentFlux:
    """Get the global SilentFlux instance"""
    global _silent_flux
    if _silent_flux is None:
        _silent_flux = SilentFlux()
    return _silent_flux


# Example usage
if __name__ == "__main__":
    flux = SilentFlux(stress_threshold=0.7, enable_auto_regulation=True)
    
    # Simulate calm operator
    print("=== Simulating CALM operator ===")
    for i in range(10):
        flux.record_keystroke()
        flux.record_action()
        flux.record_response_time(2.0)
        flux.record_interaction()
        time.sleep(0.25)
    
    status = flux.get_status()
    print(f"Stress Level: {status['stress_level']}")
    print(f"Stress Index: {status['stress_index']:.2f}")
    print(f"Output Mode: {status['output_mode']}")
    
    # Simulate stressed operator
    print("\n=== Simulating STRESSED operator ===")
    for i in range(20):
        flux.record_keystroke()
        if i % 3 == 0:
            flux.record_error()
        else:
            flux.record_action()
        flux.record_response_time(0.5)  # Very fast responses
        flux.record_interaction()
        time.sleep(0.05)  # Rapid keystrokes
    
    status = flux.get_status()
    print(f"Stress Level: {status['stress_level']}")
    print(f"Stress Index: {status['stress_index']:.2f}")
    print(f"Output Mode: {status['output_mode']}")
    
    # Test output regulation
    long_text = """
    This is a detailed explanation of the outbreak situation. The cholera outbreak 
    has been detected in the Dadaab refugee camp. This is because of contaminated 
    water sources. The reason for the rapid spread is overcrowding. Note that we 
    need immediate intervention. We recommend deploying medical teams, setting up 
    treatment centers, and distributing ORS kits. The confidence level is 95% based 
    on laboratory confirmation. Historical data shows similar patterns in 2019.
    """
    
    print("\n=== Output Regulation ===")
    print("Original:", long_text[:100] + "...")
    print("\nRegulated:", flux.regulate_output(long_text))
