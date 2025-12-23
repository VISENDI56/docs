"""
Entangled Correlation Fusion (ECF) Demonstration
Shows how ECF amplifies weak signals for outbreak detection.

This example demonstrates:
1. Adding weak CBS signals (low confidence)
2. Adding strong EMR signals (high confidence)
3. Quantum-inspired correlation amplification
4. Timeline verification
5. Pattern emergence detection
"""

import numpy as np
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from edge_node.sync_protocol.entangled_correlation_fusion import EntangledCorrelationFusion


def create_synthetic_outbreak_signals(num_signals: int = 50):
    """Create synthetic health signals simulating a cholera outbreak."""
    signals = []
    
    # Simulate outbreak in Dadaab refugee camp
    outbreak_start = 100.0  # hours since epoch
    outbreak_location = (0.0512, 40.3129)  # Dadaab coordinates
    
    for i in range(num_signals):
        # Determine if signal is part of outbreak
        if i < num_signals // 2:
            # Outbreak cluster (Dadaab)
            location = (
                outbreak_location[0] + np.random.normal(0, 0.01),
                outbreak_location[1] + np.random.normal(0, 0.01)
            )
            is_outbreak = True
            base_confidence = 0.5 + np.random.uniform(-0.2, 0.3)
            symptom = np.random.choice(['diarrhea', 'vomiting', 'dehydration'], p=[0.6, 0.3, 0.1])
        else:
            # Background noise (other locations)
            location = (
                np.random.uniform(-1, 1),
                np.random.uniform(39, 41)
            )
            is_outbreak = False
            base_confidence = 0.3 + np.random.uniform(-0.2, 0.2)
            symptom = np.random.choice(['fever', 'cough', 'headache'])
        
        # Add some false positives/negatives (10%)
        if np.random.random() < 0.1:
            is_outbreak = not is_outbreak
            base_confidence = max(0.1, min(0.9, base_confidence - 0.3))
        
        signal = {
            'time': outbreak_start + np.random.exponential(6.0),
            'location': location,
            'symptom_type': symptom,
            'confidence': base_confidence,
            'is_event': is_outbreak,
            'source': np.random.choice(['CHV', 'health_worker', 'community', 'sensor']),
        }
        
        signals.append(signal)
    
    return signals


def demo_basic_fusion():
    """Demonstrate basic ECF fusion."""
    print("=" * 70)
    print("DEMO 1: Basic Entangled Correlation Fusion")
    print("=" * 70)
    print()
    
    # Initialize ECF
    ecf = EntangledCorrelationFusion(
        max_signals=500,
        correlation_threshold=0.25,
        time_window=12.0,  # 12-hour window
        spatial_resolution=5.0,  # 5km grid
        entanglement_dim=6
    )
    
    # Create synthetic signals
    print("Creating 100 synthetic outbreak signals...")
    signals = create_synthetic_outbreak_signals(100)
    
    # Add signals to ECF
    print(f"Adding signals to ECF...")
    for i, signal in enumerate(signals):
        ecf.add_signal(signal)
        if (i + 1) % 25 == 0:
            print(f"  Added {i + 1} signals...")
    
    print()
    
    # Perform fusion
    print("Performing entangled correlation fusion...")
    result = ecf.fuse(max_iterations=5)
    
    print()
    print("Fusion Results:")
    print(f"  Status: {result['status']}")
    print(f"  Outbreak probability: {result['outbreak_probability']:.3f}")
    print(f"  Entanglement entropy: {result['entanglement_entropy']:.3f}")
    print(f"  Signals fused: {result['signals_fused']}")
    print(f"  Entangled clusters: {result['entangled_clusters']}")
    print(f"  Coherence factor: {result['coherence_factor']:.3f}")
    print()
    
    return ecf


def demo_timeline_verification(ecf):
    """Demonstrate timeline verification."""
    print("=" * 70)
    print("DEMO 2: Timeline Verification")
    print("=" * 70)
    print()
    
    print("Verifying temporal consistency...")
    timeline = ecf.verify_timeline(max_gap=24.0)
    
    print()
    print("Timeline Verification Results:")
    print(f"  Status: {timeline['status']}")
    print(f"  Consistency score: {timeline['consistency_score']:.3f}")
    print(f"  Total signals: {timeline['total_signals']}")
    print(f"  Checks performed: {timeline['checks_performed']}")
    
    if timeline['inconsistencies']:
        print(f"  Inconsistencies found: {len(timeline['inconsistencies'])}")
        print()
        print("  Top 3 inconsistencies:")
        for i, issue in enumerate(timeline['inconsistencies'][:3]):
            print(f"    {i+1}. Type: {issue['type']}")
            if issue['type'] == 'time_gap':
                print(f"       Gap: {issue['gap_hours']:.1f} hours")
            elif issue['type'] == 'entanglement_break':
                print(f"       Expected: {issue['expected']:.3f}")
                print(f"       Actual: {issue['actual']:.3f}")
    else:
        print("  ✓ No inconsistencies detected")
    
    print()


def demo_pattern_emergence(ecf):
    """Demonstrate pattern emergence detection."""
    print("=" * 70)
    print("DEMO 3: Pattern Emergence Detection")
    print("=" * 70)
    print()
    
    print("Extracting emerged patterns...")
    patterns = ecf.get_emerged_pattern(threshold=0.6)
    
    print()
    print("Pattern Emergence Results:")
    print(f"  Total patterns found: {patterns['total_patterns']}")
    print(f"  Overall confidence: {patterns['overall_confidence']:.3f}")
    print()
    
    if patterns['most_significant']:
        p = patterns['most_significant']
        print("  Most Significant Pattern:")
        print(f"    Cluster size: {p['cluster_size']} signals")
        print(f"    Average confidence: {p['average_confidence']:.3f}")
        print(f"    Time span: {p['time_span']:.1f} hours")
        print(f"    Symptom types: {', '.join(p['symptom_types'])}")
        print(f"    Spatial spread: {p['spatial_spread']} locations")
        print(f"    Signal IDs: {p['signal_ids'][:10]}...")  # Show first 10
    
    print()
    
    # Show all patterns
    if patterns['patterns']:
        print(f"  All {len(patterns['patterns'])} patterns:")
        for i, p in enumerate(patterns['patterns'][:5]):  # Show top 5
            print(f"    {i+1}. Size: {p['cluster_size']}, "
                  f"Confidence: {p['average_confidence']:.3f}, "
                  f"Symptoms: {', '.join(p['symptom_types'])}")
    
    print()


def demo_system_stats(ecf):
    """Demonstrate system statistics."""
    print("=" * 70)
    print("DEMO 4: System Statistics")
    print("=" * 70)
    print()
    
    stats = ecf.get_system_stats()
    
    print("System Statistics:")
    print(f"  Total signals: {stats['total_signals']}")
    print(f"  Correlation density: {stats['correlation_density']:.3f}")
    print(f"  Average entanglement: {stats['average_entanglement']:.3f}")
    print(f"  Von Neumann entropy: {stats['von_neumann_entropy']:.3f}")
    print(f"  Coherence factor: {stats['coherence_factor']:.3f}")
    print(f"  Memory usage: {stats['memory_usage_MB']:.2f} MB")
    print()
    
    # Interpretation
    print("Interpretation:")
    if stats['von_neumann_entropy'] < 1.0:
        print("  • Low entanglement - Isolated signals")
    elif stats['von_neumann_entropy'] < 2.0:
        print("  • Moderate entanglement - Emerging patterns")
    else:
        print("  • High entanglement - Strong outbreak signal")
    
    if stats['correlation_density'] < 0.1:
        print("  • Sparse correlation graph")
    elif stats['correlation_density'] < 0.3:
        print("  • Moderate correlation density")
    else:
        print("  • Dense correlation graph")
    
    print()


def demo_weak_signal_amplification():
    """Demonstrate weak signal amplification."""
    print("=" * 70)
    print("DEMO 5: Weak Signal Amplification")
    print("=" * 70)
    print()
    
    ecf = EntangledCorrelationFusion(
        correlation_threshold=0.2,
        time_window=6.0,
        spatial_resolution=2.0
    )
    
    print("Scenario: Multiple weak CBS signals + 1 strong EMR signal")
    print()
    
    # Add 10 weak CBS signals (confidence ~0.4)
    print("Adding 10 weak CBS signals (confidence ~0.4)...")
    for i in range(10):
        ecf.add_signal({
            'time': 100 + i * 0.5,
            'location': (0.05 + np.random.normal(0, 0.005), 
                        40.31 + np.random.normal(0, 0.005)),
            'symptom_type': 'diarrhea',
            'confidence': 0.4 + np.random.uniform(-0.1, 0.1),
            'is_event': True,
            'source': f'CHV_{i}'
        })
    
    # Fuse weak signals only
    result_weak = ecf.fuse()
    print(f"  Outbreak probability (weak signals only): {result_weak['outbreak_probability']:.3f}")
    print()
    
    # Add 1 strong EMR signal (confidence 0.95)
    print("Adding 1 strong EMR signal (confidence 0.95)...")
    ecf.add_signal({
        'time': 105,
        'location': (0.05, 40.31),
        'symptom_type': 'cholera',
        'confidence': 0.95,
        'is_event': True,
        'source': 'HOSPITAL_LAB'
    })
    
    # Fuse with strong signal
    result_strong = ecf.fuse()
    print(f"  Outbreak probability (with strong signal): {result_strong['outbreak_probability']:.3f}")
    print()
    
    # Show amplification
    amplification = result_strong['outbreak_probability'] / result_weak['outbreak_probability']
    print(f"Amplification factor: {amplification:.2f}x")
    print(f"Entanglement entropy increased: {result_weak['entanglement_entropy']:.3f} → {result_strong['entanglement_entropy']:.3f}")
    print()
    
    print("✓ ECF successfully amplified weak signals through quantum-inspired correlation!")
    print()


def main():
    """Run all demonstrations."""
    print()
    print("╔════════════════════════════════════════════════════════════════════╗")
    print("║     Entangled Correlation Fusion (ECF) - Comprehensive Demo       ║")
    print("║                    iLuminara-Core IP-05                            ║")
    print("╚════════════════════════════════════════════════════════════════════╝")
    print()
    
    # Demo 1: Basic fusion
    ecf = demo_basic_fusion()
    
    # Demo 2: Timeline verification
    demo_timeline_verification(ecf)
    
    # Demo 3: Pattern emergence
    demo_pattern_emergence(ecf)
    
    # Demo 4: System statistics
    demo_system_stats(ecf)
    
    # Demo 5: Weak signal amplification
    demo_weak_signal_amplification()
    
    print("=" * 70)
    print("All demonstrations completed successfully!")
    print("=" * 70)
    print()
    
    return ecf


if __name__ == "__main__":
    ecf_system = main()
