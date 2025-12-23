"""
Comprehensive Metrics Tracking System
Tracks: Compliance Accuracy, Reasoning Coherence, Humanitarian Margin Error, 5DM Bridge Latency
"""

import time
from typing import Dict, List
from dataclasses import dataclass, asdict
from datetime import datetime
import json


@dataclass
class ComplianceMetrics:
    """Compliance accuracy metrics"""
    total_actions: int = 0
    compliant_actions: int = 0
    violations: int = 0
    frameworks_checked: List[str] = None
    
    def accuracy(self) -> float:
        if self.total_actions == 0:
            return 0.0
        return self.compliant_actions / self.total_actions
    
    def violation_rate(self) -> float:
        if self.total_actions == 0:
            return 0.0
        return self.violations / self.total_actions


@dataclass
class ReasoningMetrics:
    """Reasoning coherence metrics"""
    total_inferences: int = 0
    coherent_reasoning: int = 0
    avg_reasoning_steps: float = 0.0
    legal_citations_correct: int = 0
    legal_citations_total: int = 0
    
    def coherence_score(self) -> float:
        if self.total_inferences == 0:
            return 0.0
        return self.coherent_reasoning / self.total_inferences
    
    def citation_accuracy(self) -> float:
        if self.legal_citations_total == 0:
            return 0.0
        return self.legal_citations_correct / self.legal_citations_total


@dataclass
class HumanitarianMetrics:
    """Humanitarian margin error metrics"""
    total_decisions: int = 0
    margin_errors: List[float] = None
    avg_margin: float = 0.0
    threshold_violations: int = 0
    
    def mean_absolute_error(self) -> float:
        if not self.margin_errors:
            return 0.0
        return sum(abs(e) for e in self.margin_errors) / len(self.margin_errors)
    
    def threshold_violation_rate(self) -> float:
        if self.total_decisions == 0:
            return 0.0
        return self.threshold_violations / self.total_decisions


@dataclass
class LatencyMetrics:
    """5DM Bridge and system latency metrics"""
    api_latencies: List[float] = None
    bridge_latencies: List[float] = None
    inference_latencies: List[float] = None
    
    def avg_api_latency(self) -> float:
        if not self.api_latencies:
            return 0.0
        return sum(self.api_latencies) / len(self.api_latencies)
    
    def avg_bridge_latency(self) -> float:
        if not self.bridge_latencies:
            return 0.0
        return sum(self.bridge_latencies) / len(self.bridge_latencies)
    
    def p95_latency(self, latencies: List[float]) -> float:
        if not latencies:
            return 0.0
        sorted_latencies = sorted(latencies)
        idx = int(len(sorted_latencies) * 0.95)
        return sorted_latencies[idx]


class MetricsTracker:
    """Central metrics tracking system"""
    
    def __init__(self):
        self.compliance = ComplianceMetrics(frameworks_checked=[])
        self.reasoning = ReasoningMetrics()
        self.humanitarian = HumanitarianMetrics(margin_errors=[])
        self.latency = LatencyMetrics(api_latencies=[], bridge_latencies=[], inference_latencies=[])
        
        self.start_time = time.time()
    
    def record_compliance_check(self, compliant: bool, framework: str):
        """Record compliance check result"""
        self.compliance.total_actions += 1
        if compliant:
            self.compliance.compliant_actions += 1
        else:
            self.compliance.violations += 1
        
        if framework not in self.compliance.frameworks_checked:
            self.compliance.frameworks_checked.append(framework)
    
    def record_reasoning(self, coherent: bool, num_steps: int, citation_correct: bool):
        """Record reasoning metrics"""
        self.reasoning.total_inferences += 1
        if coherent:
            self.reasoning.coherent_reasoning += 1
        
        # Update average reasoning steps
        total_steps = self.reasoning.avg_reasoning_steps * (self.reasoning.total_inferences - 1) + num_steps
        self.reasoning.avg_reasoning_steps = total_steps / self.reasoning.total_inferences
        
        self.reasoning.legal_citations_total += 1
        if citation_correct:
            self.reasoning.legal_citations_correct += 1
    
    def record_humanitarian_margin(self, actual_margin: float, expected_margin: float, threshold: float = 0.15):
        """Record humanitarian margin"""
        self.humanitarian.total_decisions += 1
        error = actual_margin - expected_margin
        self.humanitarian.margin_errors.append(error)
        
        # Update average margin
        total_margin = self.humanitarian.avg_margin * (self.humanitarian.total_decisions - 1) + actual_margin
        self.humanitarian.avg_margin = total_margin / self.humanitarian.total_decisions
        
        if actual_margin < threshold:
            self.humanitarian.threshold_violations += 1
    
    def record_latency(self, latency_ms: float, latency_type: str = "api"):
        """Record latency measurement"""
        if latency_type == "api":
            self.latency.api_latencies.append(latency_ms)
        elif latency_type == "bridge":
            self.latency.bridge_latencies.append(latency_ms)
        elif latency_type == "inference":
            self.latency.inference_latencies.append(latency_ms)
    
    def get_summary(self) -> Dict:
        """Get comprehensive metrics summary"""
        uptime = time.time() - self.start_time
        
        return {
            "timestamp": datetime.utcnow().isoformat(),
            "uptime_seconds": uptime,
            "compliance": {
                "accuracy": self.compliance.accuracy(),
                "violation_rate": self.compliance.violation_rate(),
                "total_actions": self.compliance.total_actions,
                "frameworks_checked": self.compliance.frameworks_checked
            },
            "reasoning": {
                "coherence_score": self.reasoning.coherence_score(),
                "citation_accuracy": self.reasoning.citation_accuracy(),
                "avg_reasoning_steps": self.reasoning.avg_reasoning_steps,
                "total_inferences": self.reasoning.total_inferences
            },
            "humanitarian": {
                "mean_absolute_error": self.humanitarian.mean_absolute_error(),
                "avg_margin": self.humanitarian.avg_margin,
                "threshold_violation_rate": self.humanitarian.threshold_violation_rate(),
                "total_decisions": self.humanitarian.total_decisions
            },
            "latency": {
                "avg_api_latency_ms": self.latency.avg_api_latency(),
                "avg_bridge_latency_ms": self.latency.avg_bridge_latency(),
                "p95_api_latency_ms": self.latency.p95_latency(self.latency.api_latencies),
                "p95_bridge_latency_ms": self.latency.p95_latency(self.latency.bridge_latencies)
            }
        }
    
    def export_prometheus_metrics(self) -> str:
        """Export metrics in Prometheus format"""
        summary = self.get_summary()
        
        metrics = []
        metrics.append(f"# HELP iluminara_compliance_accuracy Compliance accuracy rate")
        metrics.append(f"# TYPE iluminara_compliance_accuracy gauge")
        metrics.append(f"iluminara_compliance_accuracy {summary['compliance']['accuracy']}")
        
        metrics.append(f"# HELP iluminara_reasoning_coherence Reasoning coherence score")
        metrics.append(f"# TYPE iluminara_reasoning_coherence gauge")
        metrics.append(f"iluminara_reasoning_coherence {summary['reasoning']['coherence_score']}")
        
        metrics.append(f"# HELP iluminara_humanitarian_margin_error Mean absolute error in humanitarian margin")
        metrics.append(f"# TYPE iluminara_humanitarian_margin_error gauge")
        metrics.append(f"iluminara_humanitarian_margin_error {summary['humanitarian']['mean_absolute_error']}")
        
        metrics.append(f"# HELP iluminara_api_latency_ms Average API latency in milliseconds")
        metrics.append(f"# TYPE iluminara_api_latency_ms gauge")
        metrics.append(f"iluminara_api_latency_ms {summary['latency']['avg_api_latency_ms']}")
        
        return "\n".join(metrics)


# Global metrics tracker instance
_metrics_tracker = None

def get_metrics_tracker() -> MetricsTracker:
    """Get global metrics tracker instance"""
    global _metrics_tracker
    if _metrics_tracker is None:
        _metrics_tracker = MetricsTracker()
    return _metrics_tracker


def main():
    """Test metrics tracking"""
    tracker = get_metrics_tracker()
    
    # Simulate some metrics
    tracker.record_compliance_check(True, "GDPR")
    tracker.record_compliance_check(True, "KDPA")
    tracker.record_compliance_check(False, "HIPAA")
    
    tracker.record_reasoning(True, 6, True)
    tracker.record_reasoning(True, 5, True)
    tracker.record_reasoning(False, 3, False)
    
    tracker.record_humanitarian_margin(0.85, 0.80)
    tracker.record_humanitarian_margin(0.12, 0.15)  # Below threshold
    
    tracker.record_latency(45.2, "api")
    tracker.record_latency(120.5, "bridge")
    tracker.record_latency(230.1, "inference")
    
    # Get summary
    summary = tracker.get_summary()
    print(json.dumps(summary, indent=2))
    
    print("\n" + "="*60)
    print("PROMETHEUS METRICS")
    print("="*60)
    print(tracker.export_prometheus_metrics())


if __name__ == "__main__":
    main()
