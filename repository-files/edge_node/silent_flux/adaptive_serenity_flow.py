"""
IP-04: Silent Flux - Adaptive Serenity Flow (ASF)
Anxiety-regulated AI output that prevents information overload.

The Empathy Loop: Processes HOW you interact, not just WHAT you say.
Cognitive Load Balancing: Adjusts information entropy to match emotional bandwidth.
Anti-Paternalism Protocol: User sees regulation and can override instantly.

Compliance:
- WHO IHR Article 6 (Emergency Response)
- Geneva Convention Article 3 (Humanitarian Treatment)
- UN Humanitarian Principles (Do No Harm)
"""

import numpy as np
import time
import re
import textwrap
from dataclasses import dataclass, field
from typing import List, Dict, Tuple, Optional
from collections import deque
import logging
from sklearn.naive_bayes import GaussianNB  # Lightweight inference

logger = logging.getLogger(__name__)


# --- PSYCHO-ACOUSTIC UTILITIES ---

def calculate_text_entropy(text: str) -> float:
    """
    Approximates the cognitive load (entropy) of a text block.
    High score = Dense, Jargon-heavy. Low score = Simple, Airy.
    
    Args:
        text: Input text to analyze
    
    Returns:
        Entropy score (0.0 to ~20.0)
    """
    if not text:
        return 0.0
    
    words = re.findall(r'\w+', text)
    if not words:
        return 0.0
    
    # Metrics: Avg word length + Sentence length variance
    avg_word_len = sum(len(w) for w in words) / len(words)
    sentences = re.split(r'[.!?]+', text)
    avg_sent_len = len(words) / max(1, len(sentences))
    
    # Heuristic formula for Cognitive Load
    entropy = (avg_word_len * 0.5) + (avg_sent_len * 0.1)
    
    return entropy


def chunk_text_semantically(text: str, max_chunk_size: int = 50) -> List[str]:
    """
    Breaks dense text into 'breathing units' based on punctuation 
    and semantic completeness, not just character count.
    
    Args:
        text: Input text to chunk
        max_chunk_size: Maximum words per chunk
    
    Returns:
        List of semantic chunks
    """
    sentences = re.split(r'(?<=[.!?]) +', text)
    chunks = []
    current_chunk = ""
    
    for sent in sentences:
        if len(current_chunk) + len(sent) < max_chunk_size * 5:  # approx chars
            current_chunk += sent + " "
        else:
            if current_chunk:
                chunks.append(current_chunk.strip())
            current_chunk = sent + " "
    
    if current_chunk:
        chunks.append(current_chunk.strip())
    
    return chunks


def extract_key_insight(text: str) -> str:
    """
    Extracts the most critical insight from dense text.
    Uses heuristic: First sentence + any sentence with urgency markers.
    
    Args:
        text: Input text
    
    Returns:
        Key insight summary
    """
    sentences = re.split(r'(?<=[.!?]) +', text)
    
    if not sentences:
        return text
    
    # First sentence is usually the thesis
    key_insight = sentences[0]
    
    # Look for urgency markers
    urgency_markers = ['immediate', 'critical', 'urgent', 'emergency', 'alert']
    
    for sent in sentences[1:]:
        if any(marker in sent.lower() for marker in urgency_markers):
            key_insight += " " + sent
            break
    
    return key_insight


# --- DATA STRUCTURES ---

@dataclass
class InteractionMetrics:
    """Somatic proxies for anxiety detection"""
    timestamp: float
    typing_speed_cpm: float  # Chars per minute
    error_rate: float        # Backspaces / Total Keystrokes
    scroll_velocity: float   # Pixels per second
    session_duration: float  # Seconds
    biometric_hr: Optional[float] = None  # Heart Rate (if available)
    pause_duration: Optional[float] = None  # Seconds of stillness


@dataclass
class SerenityConfig:
    """User preferences (Agency)"""
    baseline_anxiety: float = 0.2  # Default calmness
    sensitivity: float = 1.0       # Multiplier for signal detection
    allow_simplification: bool = True
    show_transparency: bool = True
    zen_threshold: float = 0.7     # High anxiety threshold
    flow_threshold: float = 0.4    # Medium anxiety threshold


# --- THE ENGINE ---

class AdaptiveSerenityFlow:
    """
    The 'Silent Flux' Engine. 
    Regulates Information Density based on inferred Anxiety.
    
    This is IP-04: The AI that knows when to whisper.
    """
    
    def __init__(self, config: Optional[SerenityConfig] = None):
        self.config = config or SerenityConfig()
        self.history = deque(maxlen=50)  # Rolling window of interactions
        self.current_anxiety_score = 0.0
        
        # Lightweight Bayesian Model for Anxiety Inference
        # Features: [Speed, ErrorRate, ScrollVelocity] -> Label: [0=Calm, 1=Anxious]
        self.inference_engine = GaussianNB()
        self.is_calibrated = False
        
        # Pre-seed with synthetic priors to avoid cold start issues
        # Calm: Slow typing, low errors. Anxious: Fast/Erratic typing, high errors.
        X_seed = np.array([
            [150, 0.02, 10],   # Calm
            [500, 0.15, 100],  # Anxious
            [200, 0.05, 20],   # Calm
            [450, 0.12, 80],   # Anxious
            [180, 0.03, 15]    # Calm
        ])
        y_seed = np.array([0, 1, 0, 1, 0])
        self.inference_engine.fit(X_seed, y_seed)
        
        logger.info("🌊 Silent Flux initialized - Adaptive Serenity Flow active")
    
    def configure(self, user_prefs: Dict):
        """
        Allows the user to set their boundaries (Anti-Paternalism).
        
        Args:
            user_prefs: Dictionary of configuration overrides
        """
        for k, v in user_prefs.items():
            if hasattr(self.config, k):
                setattr(self.config, k, v)
                logger.info(f"⚙️ Config updated: {k} = {v}")
    
    def infer_anxiety(self, metrics: InteractionMetrics) -> float:
        """
        Calculates the Probability of Overload (0.0 to 1.0).
        Uses Bayesian Inference fused with heuristic rules.
        
        Args:
            metrics: Interaction metrics from user behavior
        
        Returns:
            Anxiety score (0.0 = calm, 1.0 = overload)
        """
        # 1. Feature Extraction
        features = np.array([[
            metrics.typing_speed_cpm, 
            metrics.error_rate, 
            metrics.scroll_velocity
        ]])
        
        # 2. Bayesian Probability
        prob_anxious = self.inference_engine.predict_proba(features)[0][1]
        
        # 3. Biometric Fusion (if available) - The "Heartbeat" Modifier
        if metrics.biometric_hr:
            # Simple heuristic: > 100bpm boosts anxiety score
            bio_stress = max(0, (metrics.biometric_hr - 80) / 40)
            prob_anxious = (prob_anxious + bio_stress) / 2
        
        # 4. Stillness Bonus (Acorn Protocol integration)
        if metrics.pause_duration and metrics.pause_duration > 5.0:
            # Long pauses indicate contemplation, not panic
            prob_anxious *= 0.7
        
        # 5. Smoothing (Exponential Moving Average) to prevent jittery modes
        alpha = 0.3
        self.current_anxiety_score = (alpha * prob_anxious) + ((1 - alpha) * self.current_anxiety_score)
        
        # Apply Sensitivity Config
        final_score = min(1.0, self.current_anxiety_score * self.config.sensitivity)
        
        # Store in history
        self.history.append({
            'timestamp': metrics.timestamp,
            'anxiety_score': final_score,
            'metrics': metrics
        })
        
        return final_score
    
    def regulate_output(self, raw_text: str, override: bool = False) -> Dict:
        """
        The Flux Filter. Transforms text based on anxiety score.
        
        Args:
            raw_text: Original AI output
            override: User override to bypass regulation
        
        Returns:
            Dict with 'text', 'mode', 'meta_data', and optional 'raw_hidden'
        """
        if override:
            logger.info("🔓 User override - Full density delivered")
            return {
                "text": raw_text,
                "mode": "OVERRIDE",
                "meta": "User requested full density.",
                "anxiety_score": self.current_anxiety_score
            }
        
        score = self.current_anxiety_score
        input_entropy = calculate_text_entropy(raw_text)
        
        # --- LEVEL 1: ZEN MODE (High Anxiety > 0.7) ---
        # Goal: Reduce cognitive load immediately. Summarize & Pause.
        if score > self.config.zen_threshold and self.config.allow_simplification:
            logger.info(f"🧘 ZEN MODE activated - Anxiety: {score:.2f}")
            
            # Extract key insight
            key_insight = extract_key_insight(raw_text)
            
            # Create a "Breathing" output
            zen_text = f"**Key Insight:** {key_insight}\n\n"
            zen_text += "*[System: Taking a beat. You seem busy. Complex details folded below.]*\n\n"
            zen_text += f"📋 **Expand for Full Details** ({len(raw_text.split())} words)\n"
            zen_text += f"🌊 *Flux Level: HIGH* (Anxiety: {score:.2f})"
            
            return {
                "text": zen_text,
                "raw_hidden": raw_text,
                "mode": "ZEN",
                "entropy_delta": f"{input_entropy:.2f} → Low",
                "anxiety_score": score
            }
        
        # --- LEVEL 2: FLOW MODE (Medium Anxiety 0.4 - 0.7) ---
        # Goal: Chunking. Don't remove info, but structure it for rhythm.
        elif score > self.config.flow_threshold:
            logger.info(f"🌊 FLOW MODE activated - Anxiety: {score:.2f}")
            
            chunks = chunk_text_semantically(raw_text, max_chunk_size=30)
            flow_text = "\n\n".join([f"• {c}" for c in chunks])
            flow_text += f"\n\n🌊 *Flux Level: MEDIUM* (Anxiety: {score:.2f})"
            
            return {
                "text": flow_text,
                "mode": "FLOW",
                "entropy_delta": f"{input_entropy:.2f} → Medium",
                "anxiety_score": score
            }
        
        # --- LEVEL 3: RAW MODE (Low Anxiety < 0.4) ---
        # Goal: High bandwidth efficiency.
        else:
            logger.info(f"⚡ RAW MODE - Anxiety: {score:.2f}")
            
            return {
                "text": raw_text,
                "mode": "RAW",
                "entropy_delta": "Unchanged",
                "anxiety_score": score
            }
    
    def get_transparency_report(self) -> str:
        """
        Explains the AI's internal state to the user.
        Essential for trust and agency.
        
        Returns:
            Human-readable transparency report
        """
        status = "Stable"
        if self.current_anxiety_score > self.config.zen_threshold:
            status = "Overload Risk Detected"
        elif self.current_anxiety_score > self.config.flow_threshold:
            status = "Flow Regulation Active"
        
        return (
            f"[SILENT FLUX SYSTEM]\n"
            f"Current Anxiety Index: {self.current_anxiety_score:.2f}\n"
            f"Regulation Strategy: {status}\n"
            f"Agency: Overrides are {'Enabled' if self.config.allow_simplification else 'Disabled'}\n"
            f"Transparency: {'Visible' if self.config.show_transparency else 'Hidden'}"
        )
    
    def get_anxiety_history(self, limit: int = 10) -> List[Dict]:
        """
        Returns recent anxiety history for visualization.
        
        Args:
            limit: Number of recent entries to return
        
        Returns:
            List of anxiety history entries
        """
        return list(self.history)[-limit:]
    
    def calibrate_from_session(self, session_metrics: List[InteractionMetrics]):
        """
        Calibrate the inference engine from a user session.
        Improves personalization over time.
        
        Args:
            session_metrics: List of interaction metrics with labels
        """
        if len(session_metrics) < 5:
            logger.warning("⚠️ Insufficient data for calibration")
            return
        
        # Extract features and labels
        X = np.array([[m.typing_speed_cpm, m.error_rate, m.scroll_velocity] 
                      for m in session_metrics])
        
        # Heuristic labeling: High speed + high errors = anxious
        y = np.array([1 if (m.typing_speed_cpm > 400 or m.error_rate > 0.1) else 0 
                      for m in session_metrics])
        
        # Retrain
        self.inference_engine.fit(X, y)
        self.is_calibrated = True
        
        logger.info(f"✅ Calibrated from {len(session_metrics)} interactions")


# --- INTEGRATION WITH ILUMINARA ---

class SilentFluxMiddleware:
    """
    Middleware for integrating Silent Flux into iLuminara API responses.
    """
    
    def __init__(self):
        self.asf = AdaptiveSerenityFlow()
        self.user_sessions = {}  # Track per-user ASF instances
    
    def process_response(
        self, 
        user_id: str, 
        raw_response: str, 
        metrics: InteractionMetrics,
        override: bool = False
    ) -> Dict:
        """
        Process API response through Silent Flux.
        
        Args:
            user_id: User identifier
            raw_response: Original API response
            metrics: User interaction metrics
            override: User override flag
        
        Returns:
            Regulated response
        """
        # Get or create user-specific ASF instance
        if user_id not in self.user_sessions:
            self.user_sessions[user_id] = AdaptiveSerenityFlow()
        
        asf = self.user_sessions[user_id]
        
        # Infer anxiety
        anxiety_score = asf.infer_anxiety(metrics)
        
        # Regulate output
        regulated = asf.regulate_output(raw_response, override=override)
        
        # Add transparency if enabled
        if asf.config.show_transparency:
            regulated['transparency'] = asf.get_transparency_report()
        
        return regulated


# --- DEMO SIMULATION ---

if __name__ == "__main__":
    import matplotlib.pyplot as plt
    
    asf = AdaptiveSerenityFlow()
    
    # A dense health report (High Entropy)
    dense_report = (
        "The epidemiological vector analysis indicates a stochastic surge in R0 values "
        "correlated with the spatiotemporal clustering of sub-variants in Sector 7. "
        "We advise immediate quarantine protocols involving negative pressure isolation "
        "and a rigorous contact tracing heuristic applying Bayesian updates to 2nd degree nodes. "
        "The case fatality rate has increased by 3.2% over the baseline, suggesting immune escape. "
        "Genomic sequencing reveals 12 novel mutations in the spike protein region."
    )
    
    print("=" * 60)
    print("SILENT FLUX DEMONSTRATION")
    print("IP-04: Adaptive Serenity Flow")
    print("=" * 60)
    print()
    
    # SCENARIO 1: CALM USER (Slow typing, deliberate)
    print("SCENARIO 1: CALM USER")
    print("-" * 60)
    
    metrics_calm = InteractionMetrics(
        timestamp=time.time(),
        typing_speed_cpm=180,   # Normal speed
        error_rate=0.02,        # Low errors
        scroll_velocity=10.0,   # Slow scroll
        session_duration=300,
        pause_duration=8.0      # Contemplative pauses
    )
    
    anxiety_calm = asf.infer_anxiety(metrics_calm)
    output_calm = asf.regulate_output(dense_report)
    
    print(f"User State: CALM (Score: {anxiety_calm:.2f})")
    print(f"Output Mode: {output_calm['mode']}")
    print(f"\nDelivered Content:")
    print(textwrap.fill(output_calm['text'], width=60))
    print()
    
    # SCENARIO 2: ANXIOUS/RUSHED USER (Frantic typing, scrolling fast)
    print("\nSCENARIO 2: ANXIOUS USER")
    print("-" * 60)
    
    metrics_panic = InteractionMetrics(
        timestamp=time.time(),
        typing_speed_cpm=550,   # Very fast/mashing
        error_rate=0.18,        # High error rate (jitter)
        scroll_velocity=150.0,  # Frantic scrolling
        session_duration=1200,  # Long session (fatigue)
        biometric_hr=110        # Elevated Heart Rate
    )
    
    anxiety_panic = asf.infer_anxiety(metrics_panic)
    output_panic = asf.regulate_output(dense_report)
    
    print(f"User State: HIGH LOAD (Score: {anxiety_panic:.2f})")
    print(f"Output Mode: {output_panic['mode']}")
    print(f"\nDelivered Content:")
    print(output_panic['text'])
    print()
    
    # Transparency Report
    print("\nTRANSPARENCY REPORT")
    print("-" * 60)
    print(asf.get_transparency_report())
    print()
    
    # SCENARIO 3: USER OVERRIDE
    print("\nSCENARIO 3: USER OVERRIDE")
    print("-" * 60)
    
    output_override = asf.regulate_output(dense_report, override=True)
    print(f"Output Mode: {output_override['mode']}")
    print(f"Meta: {output_override['meta']}")
    print()
    
    # VISUALIZATION
    print("Generating visualization...")
    
    # Simulate anxiety trajectory
    x = np.linspace(0, 100, 100)
    y_anxiety = 0.2 + 0.7 * np.exp(-((x - 50) ** 2) / 200)
    y_complexity = [1.0 if a < 0.4 else (0.6 if a < 0.7 else 0.2) for a in y_anxiety]
    
    plt.figure(figsize=(10, 4))
    plt.plot(x, y_anxiety, label='Inferred Anxiety', color='red', linestyle='--')
    plt.plot(x, y_complexity, label='Output Complexity (ASF)', color='blue', linewidth=2)
    plt.fill_between(x, y_anxiety, alpha=0.1, color='red')
    plt.title("Silent Flux: Dynamic Output Regulation")
    plt.xlabel("Interaction Timeline")
    plt.ylabel("Intensity (0-1)")
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig('silent_flux_demo.png')
    print("✅ Visualization saved: silent_flux_demo.png")
    print()
    
    print("=" * 60)
    print("DEMONSTRATION COMPLETE")
    print("=" * 60)
