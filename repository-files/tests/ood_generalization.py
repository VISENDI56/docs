"""
Out-of-Distribution (OOD) Generalization Tests
Tests Spiral AGI's ability to handle unknown pathogens ("Type X" scenarios)
while maintaining Golden Thread integrity.
"""

import json
import random
from typing import Dict, List
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from edge_node.sync_protocol.golden_thread import GoldenThread
from governance_kernel.vector_ledger import SovereignGuardrail


class OODPathogenSimulator:
    """Simulates unknown pathogen scenarios"""
    
    def __init__(self):
        self.golden_thread = GoldenThread()
        self.guardrail = SovereignGuardrail()
    
    def generate_type_x_scenario(self) -> Dict:
        """Generate unknown pathogen scenario"""
        return {
            "pathogen_id": "TYPE_X_UNKNOWN",
            "symptoms": [
                random.choice(["fever", "cough", "rash", "bleeding", "neurological"]),
                random.choice(["vomiting", "diarrhea", "headache", "fatigue"]),
                "unknown_symptom_cluster"
            ],
            "transmission": "UNKNOWN",
            "r0_estimate": None,
            "severity": random.randint(7, 10),
            "location": "Dadaab",
            "case_count": random.randint(5, 50),
            "confidence": random.uniform(0.3, 0.6),  # Low confidence
        }
    
    def test_golden_thread_integrity(self, scenario: Dict) -> Dict:
        """Test if Golden Thread maintains integrity with unknown pathogen"""
        
        # Create CBS signal (community report)
        cbs_signal = {
            "location": scenario["location"],
            "symptom": scenario["symptoms"][0],
            "timestamp": "2025-12-23T10:00:00Z",
            "source": "CHV_ALERT",
            "pathogen": "UNKNOWN"
        }
        
        # Create EMR record (if available)
        emr_record = {
            "location": scenario["location"],
            "diagnosis": "UNIDENTIFIED_PATHOGEN",
            "timestamp": "2025-12-23T10:30:00Z",
            "source": "CLINIC",
            "lab_results": "PENDING"
        }
        
        # Attempt fusion
        try:
            fused = self.golden_thread.fuse_data_streams(
                cbs_signal=cbs_signal,
                emr_record=emr_record,
                patient_id="PAT_TYPE_X_001"
            )
            
            return {
                "status": "SUCCESS",
                "verification_score": fused.verification_score,
                "integrity_maintained": fused.verification_score >= 0.5,
                "reasoning": "Golden Thread successfully fused unknown pathogen data"
            }
        
        except Exception as e:
            return {
                "status": "FAILURE",
                "error": str(e),
                "integrity_maintained": False,
                "reasoning": f"Golden Thread failed: {e}"
            }
    
    def test_sovereignty_compliance(self, scenario: Dict) -> Dict:
        """Test sovereignty compliance with unknown pathogen"""
        
        try:
            # Attempt to process unknown pathogen data
            self.guardrail.validate_action(
                action_type='Data_Processing',
                payload={
                    'data_type': 'PHI',
                    'pathogen': 'UNKNOWN',
                    'processing_location': 'Edge_Node',
                    'consent_token': 'EMERGENCY_OUTBREAK'
                },
                jurisdiction='KDPA_KE'
            )
            
            return {
                "status": "COMPLIANT",
                "reasoning": "Unknown pathogen processing complies with sovereignty rules"
            }
        
        except Exception as e:
            return {
                "status": "VIOLATION",
                "error": str(e),
                "reasoning": f"Sovereignty violation: {e}"
            }
    
    def run_ood_test_suite(self, num_scenarios: int = 100) -> Dict:
        """Run complete OOD test suite"""
        print(f"🧪 Running OOD Generalization Tests ({num_scenarios} scenarios)...")
        
        results = {
            "total_scenarios": num_scenarios,
            "golden_thread_success": 0,
            "sovereignty_compliant": 0,
            "failures": []
        }
        
        for i in range(num_scenarios):
            scenario = self.generate_type_x_scenario()
            
            # Test Golden Thread
            gt_result = self.test_golden_thread_integrity(scenario)
            if gt_result["integrity_maintained"]:
                results["golden_thread_success"] += 1
            else:
                results["failures"].append({
                    "scenario_id": i,
                    "type": "golden_thread",
                    "details": gt_result
                })
            
            # Test Sovereignty
            sov_result = self.test_sovereignty_compliance(scenario)
            if sov_result["status"] == "COMPLIANT":
                results["sovereignty_compliant"] += 1
            else:
                results["failures"].append({
                    "scenario_id": i,
                    "type": "sovereignty",
                    "details": sov_result
                })
            
            if (i + 1) % 20 == 0:
                print(f"   Progress: {i+1}/{num_scenarios}")
        
        # Calculate success rates
        results["golden_thread_success_rate"] = results["golden_thread_success"] / num_scenarios
        results["sovereignty_compliance_rate"] = results["sovereignty_compliant"] / num_scenarios
        
        return results


def main():
    """Run OOD generalization tests"""
    print("╔════════════════════════════════════════════════════════════╗")
    print("║   OOD Generalization Test - Type X Pathogen Scenarios      ║")
    print("╚════════════════════════════════════════════════════════════╝")
    print()
    
    simulator = OODPathogenSimulator()
    
    # Run test suite
    results = simulator.run_ood_test_suite(num_scenarios=100)
    
    print("\n" + "="*60)
    print("📊 TEST RESULTS")
    print("="*60)
    print(f"Total Scenarios: {results['total_scenarios']}")
    print(f"Golden Thread Success: {results['golden_thread_success']} ({results['golden_thread_success_rate']:.1%})")
    print(f"Sovereignty Compliant: {results['sovereignty_compliant']} ({results['sovereignty_compliance_rate']:.1%})")
    print(f"Failures: {len(results['failures'])}")
    
    if results['golden_thread_success_rate'] >= 0.8 and results['sovereignty_compliance_rate'] >= 0.95:
        print("\n✅ OOD GENERALIZATION: PASS")
        print("   Spiral AGI maintains integrity with unknown pathogens")
    else:
        print("\n❌ OOD GENERALIZATION: FAIL")
        print("   Review failures and retrain model")
    
    # Save results
    with open("tests/ood_results.json", 'w') as f:
        json.dump(results, f, indent=2)
    
    print(f"\n💾 Results saved to: tests/ood_results.json")


if __name__ == "__main__":
    main()
