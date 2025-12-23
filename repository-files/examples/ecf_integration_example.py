"""
ECF Integration Example
Demonstrates complete Entangled Correlation Fusion workflow
"""

from datetime import datetime, timedelta
from edge_node.sync_protocol.ecf_engine import ECFEngine, Signal, SignalSource
from edge_node.sync_protocol.golden_thread_ecf import GoldenThreadECF


def example_1_basic_ecf():
    """Example 1: Basic ECF signal fusion"""
    print("\n" + "="*70)
    print("EXAMPLE 1: Basic ECF Signal Fusion")
    print("="*70)
    
    # Initialize ECF Engine
    ecf = ECFEngine(
        temporal_window_hours=24.0,
        spatial_threshold_km=50.0,
        min_correlation_score=0.6,
        enable_quantum_weighting=True
    )
    
    # Simulate cholera outbreak signals
    signals = [
        Signal(
            source=SignalSource.CBS,
            timestamp=datetime.utcnow(),
            location=(0.0512, 40.3129),  # Dadaab, Kenya
            symptom="diarrhea",
            severity=0.8,
            confidence=0.7,
            metadata={"chv": "Amina Hassan", "cases": 3}
        ),
        Signal(
            source=SignalSource.EMR,
            timestamp=datetime.utcnow() + timedelta(minutes=30),
            location=(0.0520, 40.3135),  # Nearby clinic
            symptom="cholera",
            severity=0.85,
            confidence=0.95,
            metadata={"clinic": "Dadaab Health Center", "lab_confirmed": True}
        ),
        Signal(
            source=SignalSource.VOICE,
            timestamp=datetime.utcnow() + timedelta(minutes=45),
            location=(0.0515, 40.3130),
            symptom="diarrhea",
            severity=0.75,
            confidence=0.6,
            metadata={"language": "swahili", "chv": "Mohamed Ali"}
        ),
    ]
    
    # Ingest signals
    fused_event = None
    for signal in signals:
        result = ecf.ingest_signal(signal)
        if result:
            fused_event = result
    
    # Display results
    if fused_event:
        print(f"\n✨ Fused Event Created:")
        print(f"   Event ID: {fused_event.event_id}")
        print(f"   Status: {fused_event.verification_status}")
        print(f"   Correlation Score: {fused_event.correlation_score:.3f}")
        print(f"   Confidence: {fused_event.confidence:.3f}")
        print(f"   Primary Source: {fused_event.primary_source.value}")
        print(f"   Contributing Sources: {[s.value for s in fused_event.correlated_sources]}")
        print(f"   Location: {fused_event.location}")
        print(f"   Symptom: {fused_event.symptom}")
        print(f"   Severity: {fused_event.severity:.2f}")
    else:
        print("\n❌ No fusion occurred")


def example_2_golden_thread_ecf():
    """Example 2: Golden Thread with ECF integration"""
    print("\n" + "="*70)
    print("EXAMPLE 2: Golden Thread ECF Integration")
    print("="*70)
    
    # Initialize ECF-enhanced Golden Thread
    gt_ecf = GoldenThreadECF(
        enable_ecf=True,
        temporal_window_hours=24.0,
        spatial_threshold_km=50.0,
        min_correlation_score=0.6,
        enable_quantum_weighting=True
    )
    
    # CBS signal from CHV
    cbs_signal = {
        "location": "0.0512,40.3129",
        "symptom": "diarrhea",
        "timestamp": datetime.utcnow().isoformat(),
        "severity": 0.8,
        "confidence": 0.7,
        "metadata": {"chv": "Amina Hassan"}
    }
    
    # EMR record from clinic
    emr_record = {
        "location": "0.0520,40.3135",
        "diagnosis": "cholera",
        "timestamp": (datetime.utcnow() + timedelta(minutes=30)).isoformat(),
        "severity": 0.85,
        "confidence": 0.95,
        "metadata": {"clinic": "Dadaab Health Center"}
    }
    
    # Fuse with ECF
    fused_record = gt_ecf.fuse_data_streams(
        cbs_signal=cbs_signal,
        emr_record=emr_record,
        patient_id="PATIENT_12345"
    )
    
    # Display results
    print(f"\n✨ Fused Record Created:")
    print(f"   Record ID: {fused_record.record_id}")
    print(f"   Patient ID: {fused_record.patient_id}")
    print(f"   Verification Score: {fused_record.verification_score:.3f}")
    print(f"   ECF Correlation: {fused_record.canonical_data.get('ecf_correlation_score', 'N/A'):.3f}")
    print(f"   ECF Status: {fused_record.canonical_data.get('ecf_verification_status', 'N/A')}")
    print(f"   Location: {fused_record.location}")
    print(f"   Retention Status: {fused_record.retention_status}")
    
    # Get statistics
    stats = gt_ecf.get_fusion_statistics()
    print(f"\n📊 Fusion Statistics:")
    print(f"   Total Records: {stats['total_records_fused']}")
    print(f"   ECF Enabled: {stats['ecf_statistics']['ecf_enabled']}")
    print(f"   ECF Events: {stats['ecf_statistics']['total_fused_events']}")
    print(f"   Avg Correlation: {stats['ecf_statistics'].get('average_correlation', 0):.3f}")


def example_3_multi_source_outbreak():
    """Example 3: Multi-source outbreak detection"""
    print("\n" + "="*70)
    print("EXAMPLE 3: Multi-Source Outbreak Detection")
    print("="*70)
    
    ecf = ECFEngine(
        temporal_window_hours=48.0,  # Longer window for outbreak
        spatial_threshold_km=100.0,  # Larger area
        min_correlation_score=0.5,   # Lower threshold for weak signals
        enable_quantum_weighting=True
    )
    
    # Day 1: Initial CBS reports
    day1_signals = [
        Signal(
            source=SignalSource.CBS,
            timestamp=datetime(2025, 1, 15, 8, 0),
            location=(0.0512, 40.3129),
            symptom="diarrhea",
            severity=0.6,
            confidence=0.6,
            metadata={"chv": "Amina", "cases": 2}
        ),
        Signal(
            source=SignalSource.CBS,
            timestamp=datetime(2025, 1, 15, 10, 0),
            location=(0.0620, 40.3200),  # Different camp
            symptom="diarrhea",
            severity=0.7,
            confidence=0.6,
            metadata={"chv": "Mohamed", "cases": 3}
        ),
    ]
    
    # Day 1: EMR confirmation
    day1_emr = Signal(
        source=SignalSource.EMR,
        timestamp=datetime(2025, 1, 15, 14, 0),
        location=(0.0520, 40.3135),
        symptom="cholera",
        severity=0.9,
        confidence=0.95,
        metadata={"clinic": "Dadaab", "lab_confirmed": True}
    )
    
    # Day 2: IoT sensor alert
    day2_iot = Signal(
        source=SignalSource.IOT,
        timestamp=datetime(2025, 1, 16, 6, 0),
        location=(0.0515, 40.3130),
        symptom="water_contamination",
        severity=0.8,
        confidence=0.85,
        metadata={"sensor_id": "WQ-001", "ecoli_ppm": 450}
    )
    
    # Day 2: More CBS reports
    day2_cbs = Signal(
        source=SignalSource.CBS,
        timestamp=datetime(2025, 1, 16, 9, 0),
        location=(0.0530, 40.3140),
        symptom="diarrhea",
        severity=0.8,
        confidence=0.7,
        metadata={"chv": "Fatima", "cases": 5}
    )
    
    # Ingest all signals
    all_signals = day1_signals + [day1_emr, day2_iot, day2_cbs]
    
    print(f"\n📥 Ingesting {len(all_signals)} signals...")
    
    fused_events = []
    for signal in all_signals:
        result = ecf.ingest_signal(signal)
        if result:
            fused_events.append(result)
            print(f"   ✨ Fusion: {signal.source.value} → Correlation: {result.correlation_score:.3f}")
    
    # Display outbreak summary
    print(f"\n🚨 Outbreak Summary:")
    print(f"   Total Signals: {len(all_signals)}")
    print(f"   Fused Events: {len(fused_events)}")
    
    if fused_events:
        highest_correlation = max(e.correlation_score for e in fused_events)
        print(f"   Highest Correlation: {highest_correlation:.3f}")
        
        # Find ENTANGLED events
        entangled = [e for e in fused_events if e.verification_status == "ENTANGLED"]
        if entangled:
            print(f"   ⚡ ENTANGLED Events: {len(entangled)}")
            print(f"   🔴 OUTBREAK CONFIRMED")
        else:
            print(f"   ⚠️  OUTBREAK PROBABLE")


def example_4_comparison_classic_vs_ecf():
    """Example 4: Compare classic vs ECF fusion"""
    print("\n" + "="*70)
    print("EXAMPLE 4: Classic vs ECF Comparison")
    print("="*70)
    
    # Test data
    cbs_signal = {
        "location": "0.0512,40.3129",
        "symptom": "diarrhea",
        "timestamp": datetime.utcnow().isoformat(),
        "severity": 0.8,
        "confidence": 0.7,
    }
    
    emr_record = {
        "location": "0.0520,40.3135",  # 800m away
        "diagnosis": "cholera",
        "timestamp": (datetime.utcnow() + timedelta(minutes=15)).isoformat(),
        "severity": 0.85,
        "confidence": 0.95,
    }
    
    # Classic Golden Thread
    print("\n📊 Classic Golden Thread:")
    from edge_node.sync_protocol.golden_thread import GoldenThread
    gt_classic = GoldenThread()
    classic_record = gt_classic.fuse_data_streams(
        cbs_signal=cbs_signal,
        emr_record=emr_record,
        patient_id="PATIENT_TEST"
    )
    print(f"   Verification Score: {classic_record.verification_score:.3f}")
    print(f"   Method: Simple location/time matching")
    
    # ECF-Enhanced
    print("\n✨ ECF-Enhanced Golden Thread:")
    gt_ecf = GoldenThreadECF(enable_ecf=True)
    ecf_record = gt_ecf.fuse_data_streams(
        cbs_signal=cbs_signal,
        emr_record=emr_record,
        patient_id="PATIENT_TEST"
    )
    print(f"   Verification Score: {ecf_record.verification_score:.3f}")
    print(f"   ECF Correlation: {ecf_record.canonical_data.get('ecf_correlation_score', 0):.3f}")
    print(f"   ECF Status: {ecf_record.canonical_data.get('ecf_verification_status', 'N/A')}")
    print(f"   Method: Multi-dimensional correlation")
    
    print("\n💡 Insight:")
    print("   ECF captures nuanced correlations that classic matching misses.")
    print("   Even with 800m spatial difference, ECF recognizes strong correlation")
    print("   due to temporal proximity, symptom match, and severity alignment.")


if __name__ == "__main__":
    print("\n" + "="*70)
    print("iLuminara-Core: ECF Integration Examples")
    print("="*70)
    
    # Run all examples
    example_1_basic_ecf()
    example_2_golden_thread_ecf()
    example_3_multi_source_outbreak()
    example_4_comparison_classic_vs_ecf()
    
    print("\n" + "="*70)
    print("✅ All examples completed successfully")
    print("="*70 + "\n")
