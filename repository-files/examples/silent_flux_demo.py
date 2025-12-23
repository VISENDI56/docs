"""
Silent Flux (IP-04) Demonstration
Shows how Adaptive Serenity Flow regulates AI output based on user anxiety.
"""

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import time
import textwrap
from edge_node.silent_flux.adaptive_serenity_flow import (
    AdaptiveSerenityFlow,
    InteractionMetrics,
    SerenityConfig,
    SilentFluxMiddleware
)


def print_section(title: str):
    """Print formatted section header"""
    print("\n" + "=" * 70)
    print(f"  {title}")
    print("=" * 70 + "\n")


def print_output(output: dict):
    """Print regulated output"""
    print(f"Mode: {output['mode']}")
    print(f"Anxiety Score: {output['anxiety_score']:.2f}")
    print(f"Entropy Delta: {output.get('entropy_delta', 'N/A')}")
    print("\nDelivered Content:")
    print("-" * 70)
    print(textwrap.fill(output['text'], width=70))
    print("-" * 70)
    
    if 'raw_hidden' in output:
        print(f"\n[Hidden content available: {len(output['raw_hidden'])} chars]")


def demo_basic_scenarios():
    """Demonstrate the three regulation modes"""
    print_section("DEMO 1: Basic Regulation Modes")
    
    asf = AdaptiveSerenityFlow()
    
    # Dense epidemiological report
    dense_report = (
        "The epidemiological vector analysis indicates a stochastic surge in R0 values "
        "correlated with the spatiotemporal clustering of sub-variants in Sector 7. "
        "We advise immediate quarantine protocols involving negative pressure isolation "
        "and a rigorous contact tracing heuristic applying Bayesian updates to 2nd degree nodes. "
        "The case fatality rate has increased by 3.2% over the baseline, suggesting immune escape. "
        "Genomic sequencing reveals 12 novel mutations in the spike protein region."
    )
    
    # Scenario 1: Calm user
    print("Scenario 1: CALM USER")
    print("-" * 70)
    
    metrics_calm = InteractionMetrics(
        timestamp=time.time(),
        typing_speed_cpm=180,
        error_rate=0.02,
        scroll_velocity=10.0,
        session_duration=300,
        pause_duration=8.0
    )
    
    asf.infer_anxiety(metrics_calm)
    output_calm = asf.regulate_output(dense_report)
    print_output(output_calm)
    
    # Scenario 2: Moderately stressed user
    print("\n\nScenario 2: MODERATELY STRESSED USER")
    print("-" * 70)
    
    metrics_moderate = InteractionMetrics(
        timestamp=time.time(),
        typing_speed_cpm=350,
        error_rate=0.08,
        scroll_velocity=60.0,
        session_duration=600,
        biometric_hr=95
    )
    
    asf.infer_anxiety(metrics_moderate)
    output_moderate = asf.regulate_output(dense_report)
    print_output(output_moderate)
    
    # Scenario 3: Highly anxious user
    print("\n\nScenario 3: HIGHLY ANXIOUS USER")
    print("-" * 70)
    
    metrics_anxious = InteractionMetrics(
        timestamp=time.time(),
        typing_speed_cpm=550,
        error_rate=0.18,
        scroll_velocity=150.0,
        session_duration=1200,
        biometric_hr=110
    )
    
    asf.infer_anxiety(metrics_anxious)
    output_anxious = asf.regulate_output(dense_report)
    print_output(output_anxious)


def demo_user_override():
    """Demonstrate anti-paternalism protocol"""
    print_section("DEMO 2: Anti-Paternalism Protocol (User Override)")
    
    asf = AdaptiveSerenityFlow()
    
    # Simulate anxious state
    metrics_anxious = InteractionMetrics(
        timestamp=time.time(),
        typing_speed_cpm=550,
        error_rate=0.18,
        scroll_velocity=150.0,
        session_duration=1200,
        biometric_hr=110
    )
    
    asf.infer_anxiety(metrics_anxious)
    
    dense_report = (
        "The epidemiological vector analysis indicates a stochastic surge in R0 values "
        "correlated with the spatiotemporal clustering of sub-variants in Sector 7."
    )
    
    print("Without Override (ZEN mode active):")
    print("-" * 70)
    output_regulated = asf.regulate_output(dense_report, override=False)
    print_output(output_regulated)
    
    print("\n\nWith Override (User requests full density):")
    print("-" * 70)
    output_override = asf.regulate_output(dense_report, override=True)
    print_output(output_override)


def demo_transparency():
    """Demonstrate transparency reporting"""
    print_section("DEMO 3: Transparency Reporting")
    
    asf = AdaptiveSerenityFlow()
    
    # Simulate various anxiety states
    states = [
        ("Calm", InteractionMetrics(time.time(), 180, 0.02, 10.0, 300)),
        ("Moderate", InteractionMetrics(time.time(), 350, 0.08, 60.0, 600, 95)),
        ("Anxious", InteractionMetrics(time.time(), 550, 0.18, 150.0, 1200, 110))
    ]
    
    for state_name, metrics in states:
        asf.infer_anxiety(metrics)
        print(f"\n{state_name} State:")
        print("-" * 70)
        print(asf.get_transparency_report())


def demo_middleware():
    """Demonstrate API middleware integration"""
    print_section("DEMO 4: API Middleware Integration")
    
    middleware = SilentFluxMiddleware()
    
    # Simulate API response
    api_response = (
        "Outbreak detected in Dadaab refugee camp. "
        "Cholera cases: 47. R0 estimate: 2.8. "
        "Immediate response required: ORS distribution, water chlorination, "
        "contact tracing for 2nd degree contacts."
    )
    
    # User 1: Calm CHW
    print("User 1: Calm Community Health Worker")
    print("-" * 70)
    
    metrics_calm = InteractionMetrics(
        timestamp=time.time(),
        typing_speed_cpm=180,
        error_rate=0.02,
        scroll_velocity=10.0,
        session_duration=300
    )
    
    regulated_1 = middleware.process_response(
        user_id="CHV_AMINA_HASSAN",
        raw_response=api_response,
        metrics=metrics_calm
    )
    
    print_output(regulated_1)
    
    if 'transparency' in regulated_1:
        print("\nTransparency Report:")
        print(regulated_1['transparency'])
    
    # User 2: Stressed CHW
    print("\n\nUser 2: Stressed Community Health Worker")
    print("-" * 70)
    
    metrics_stressed = InteractionMetrics(
        timestamp=time.time(),
        typing_speed_cpm=500,
        error_rate=0.15,
        scroll_velocity=120.0,
        session_duration=900,
        biometric_hr=105
    )
    
    regulated_2 = middleware.process_response(
        user_id="CHV_FATIMA_OMAR",
        raw_response=api_response,
        metrics=metrics_stressed
    )
    
    print_output(regulated_2)
    
    if 'transparency' in regulated_2:
        print("\nTransparency Report:")
        print(regulated_2['transparency'])


def demo_calibration():
    """Demonstrate personalized calibration"""
    print_section("DEMO 5: Personalized Calibration")
    
    asf = AdaptiveSerenityFlow()
    
    print("Before Calibration:")
    print("-" * 70)
    
    # Test metrics
    test_metrics = InteractionMetrics(
        timestamp=time.time(),
        typing_speed_cpm=300,
        error_rate=0.10,
        scroll_velocity=50.0,
        session_duration=600
    )
    
    anxiety_before = asf.infer_anxiety(test_metrics)
    print(f"Anxiety Score: {anxiety_before:.2f}")
    
    # Simulate user session for calibration
    print("\nCollecting session data for calibration...")
    session_metrics = [
        InteractionMetrics(time.time(), 200, 0.03, 15.0, 300),
        InteractionMetrics(time.time(), 180, 0.02, 12.0, 350),
        InteractionMetrics(time.time(), 450, 0.14, 90.0, 800),
        InteractionMetrics(time.time(), 500, 0.16, 110.0, 900),
        InteractionMetrics(time.time(), 190, 0.04, 18.0, 400),
    ]
    
    asf.calibrate_from_session(session_metrics)
    
    print("\nAfter Calibration:")
    print("-" * 70)
    
    anxiety_after = asf.infer_anxiety(test_metrics)
    print(f"Anxiety Score: {anxiety_after:.2f}")
    print(f"Delta: {anxiety_after - anxiety_before:+.2f}")


def demo_configuration():
    """Demonstrate user configuration"""
    print_section("DEMO 6: User Configuration")
    
    # Default config
    print("Default Configuration:")
    print("-" * 70)
    
    asf_default = AdaptiveSerenityFlow()
    print(f"Baseline Anxiety: {asf_default.config.baseline_anxiety}")
    print(f"Sensitivity: {asf_default.config.sensitivity}")
    print(f"Allow Simplification: {asf_default.config.allow_simplification}")
    print(f"Show Transparency: {asf_default.config.show_transparency}")
    print(f"ZEN Threshold: {asf_default.config.zen_threshold}")
    print(f"FLOW Threshold: {asf_default.config.flow_threshold}")
    
    # Custom config for expert user
    print("\n\nExpert User Configuration (No Simplification):")
    print("-" * 70)
    
    expert_config = SerenityConfig(
        baseline_anxiety=0.1,
        sensitivity=0.5,
        allow_simplification=False,
        show_transparency=False
    )
    
    asf_expert = AdaptiveSerenityFlow(config=expert_config)
    print(f"Baseline Anxiety: {asf_expert.config.baseline_anxiety}")
    print(f"Sensitivity: {asf_expert.config.sensitivity}")
    print(f"Allow Simplification: {asf_expert.config.allow_simplification}")
    print(f"Show Transparency: {asf_expert.config.show_transparency}")
    
    # Custom config for training mode
    print("\n\nTraining Mode Configuration (More Chunking):")
    print("-" * 70)
    
    training_config = SerenityConfig(
        baseline_anxiety=0.3,
        sensitivity=1.2,
        allow_simplification=True,
        show_transparency=True,
        zen_threshold=0.6,
        flow_threshold=0.2
    )
    
    asf_training = AdaptiveSerenityFlow(config=training_config)
    print(f"Baseline Anxiety: {asf_training.config.baseline_anxiety}")
    print(f"Sensitivity: {asf_training.config.sensitivity}")
    print(f"ZEN Threshold: {asf_training.config.zen_threshold}")
    print(f"FLOW Threshold: {asf_training.config.flow_threshold}")


def main():
    """Run all demonstrations"""
    print("\n")
    print("╔" + "=" * 68 + "╗")
    print("║" + " " * 15 + "SILENT FLUX DEMONSTRATION" + " " * 28 + "║")
    print("║" + " " * 12 + "IP-04: Adaptive Serenity Flow" + " " * 26 + "║")
    print("╚" + "=" * 68 + "╝")
    
    demo_basic_scenarios()
    demo_user_override()
    demo_transparency()
    demo_middleware()
    demo_calibration()
    demo_configuration()
    
    print("\n")
    print("╔" + "=" * 68 + "╗")
    print("║" + " " * 20 + "DEMONSTRATION COMPLETE" + " " * 25 + "║")
    print("╚" + "=" * 68 + "╝")
    print("\n")
    print("Key Takeaways:")
    print("  • Silent Flux adapts to user anxiety in real-time")
    print("  • Three modes: ZEN (high anxiety), FLOW (medium), RAW (low)")
    print("  • Users can always override regulation (anti-paternalism)")
    print("  • Transparency reports show internal state")
    print("  • Personalized calibration improves over time")
    print("  • Configurable for different user types (expert, training, etc.)")
    print("\n")


if __name__ == "__main__":
    main()
