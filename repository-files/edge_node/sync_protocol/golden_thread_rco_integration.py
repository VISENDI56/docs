"""
Golden Thread + RCO Integration
Every health signal doubles as a legal signal.

This module hooks the Regenerative Compliance Oracle into the Golden Thread
data fusion engine, enabling real-time compliance drift detection.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from governance_kernel.rco_engine import RegenerativeComplianceOracle
from typing import Dict, Optional
import logging

logger = logging.getLogger(__name__)


class GoldenThreadRCOBridge:
    """
    Bridge between Golden Thread and RCO.
    
    Every fused event is ingested by RCO for compliance monitoring.
    """
    
    def __init__(self, enable_rco: bool = True):
        self.enable_rco = enable_rco
        
        if enable_rco:
            self.rco = RegenerativeComplianceOracle(
                laws_path="config/sectoral_laws.json",
                enable_auto_patch=False  # Require human approval
            )
            logger.info("🌉 Golden Thread <-> RCO Bridge initialized")
        else:
            self.rco = None
            logger.info("⚠️ RCO disabled")
    
    def ingest_fused_event(
        self,
        fused_event: Dict,
        jurisdiction: str = "KDPA_KE"
    ):
        """
        Ingest a fused Golden Thread event into RCO.
        
        Args:
            fused_event: Fused event from Golden Thread
            jurisdiction: Primary jurisdiction framework
        """
        if not self.enable_rco or not self.rco:
            return
        
        # Extract compliance metrics from fused event
        data_stream = self._extract_compliance_metrics(fused_event)
        
        # Determine applicable frameworks
        frameworks = self._determine_frameworks(fused_event, jurisdiction)
        
        # Ingest into RCO for each framework
        for framework_id in frameworks:
            try:
                self.rco.ingest(data_stream, framework_id)
            except Exception as e:
                logger.error(f"❌ RCO ingestion failed for {framework_id}: {e}")
    
    def _extract_compliance_metrics(self, fused_event: Dict) -> Dict:
        """Extract compliance metrics from fused event"""
        
        # Default metrics
        metrics = {
            "data_residency_compliance": 1.0,
            "consent_rate": 1.0,
            "retention_compliance": 1.0,
            "explainability_rate": 1.0,
            "audit_coverage": 1.0,
            "encryption_rate": 1.0,
            "access_control_compliance": 1.0,
            "incident_response_time": 0.0,
            "training_completion_rate": 1.0,
            "vulnerability_patch_rate": 1.0,
        }
        
        # Extract from fused event
        if "verification_score" in fused_event:
            # Lower verification = potential compliance issue
            verification = fused_event["verification_score"]
            metrics["audit_coverage"] = verification
            metrics["data_residency_compliance"] = verification
        
        if "consent_token" in fused_event:
            # Check consent validity
            consent_valid = fused_event.get("consent_valid", True)
            metrics["consent_rate"] = 1.0 if consent_valid else 0.0
        
        if "explainability" in fused_event:
            # Check if high-risk inference has explanation
            has_explanation = bool(fused_event.get("explainability"))
            metrics["explainability_rate"] = 1.0 if has_explanation else 0.0
        
        if "timestamp" in fused_event:
            # Check retention compliance
            from datetime import datetime
            event_time = datetime.fromisoformat(fused_event["timestamp"])
            age_days = (datetime.utcnow() - event_time).days
            
            # Flag if approaching retention limit
            if age_days > 150:  # Approaching 180-day HOT limit
                metrics["retention_compliance"] = 0.85
        
        return metrics
    
    def _determine_frameworks(
        self,
        fused_event: Dict,
        primary_jurisdiction: str
    ) -> list:
        """Determine which frameworks apply to this event"""
        
        frameworks = [primary_jurisdiction]
        
        # Add GDPR if EU data subject
        if fused_event.get("data_subject_region") == "EU":
            frameworks.append("GDPR")
            frameworks.append("EU_AI_ACT")
        
        # Add HIPAA if US healthcare data
        if fused_event.get("data_type") == "PHI" and fused_event.get("region") == "US":
            frameworks.append("HIPAA")
        
        # Add WHO IHR if outbreak-related
        if fused_event.get("event_type") == "outbreak":
            frameworks.append("WHO_IHR")
        
        # Add Geneva Convention if conflict zone
        if fused_event.get("conflict_zone", False):
            frameworks.append("GENEVA_CONVENTION")
        
        return list(set(frameworks))  # Remove duplicates
    
    def get_pending_patches(self):
        """Get pending RCO patches"""
        if not self.rco:
            return []
        
        return self.rco.get_pending_patches()
    
    def approve_patch(
        self,
        patch_id: str,
        approved_by: str,
        historical_events: list
    ):
        """Approve an RCO patch"""
        if not self.rco:
            return False, {"error": "rco_disabled"}
        
        return self.rco.approve_patch(patch_id, approved_by, historical_events)


# Example integration with existing Golden Thread
def integrate_rco_with_golden_thread():
    """
    Example of how to integrate RCO with existing Golden Thread code.
    
    Add this to your golden_thread.py:
    """
    
    example_code = '''
# In golden_thread.py

from edge_node.sync_protocol.golden_thread_rco_integration import GoldenThreadRCOBridge

class GoldenThread:
    def __init__(self):
        # ... existing init code ...
        
        # Initialize RCO bridge
        self.rco_bridge = GoldenThreadRCOBridge(enable_rco=True)
    
    def fuse_data_streams(self, cbs_signal, emr_record=None, patient_id=None):
        # ... existing fusion logic ...
        
        fused_event = {
            "verification_score": verification_score,
            "timestamp": timestamp,
            "location": location,
            "data_type": "PHI",
            "event_type": event_type,
            # ... other fields ...
        }
        
        # Ingest into RCO
        self.rco_bridge.ingest_fused_event(
            fused_event=fused_event,
            jurisdiction="KDPA_KE"
        )
        
        return fused_event
    
    def get_rco_status(self):
        """Get RCO compliance status"""
        pending_patches = self.rco_bridge.get_pending_patches()
        
        return {
            "pending_patches": len(pending_patches),
            "patches": [
                {
                    "patch_id": p.patch_id,
                    "framework": p.framework_id,
                    "type": p.patch_type,
                    "confidence": p.confidence,
                    "rationale": p.rationale
                }
                for p in pending_patches
            ]
        }
'''
    
    return example_code


if __name__ == "__main__":
    # Test integration
    bridge = GoldenThreadRCOBridge(enable_rco=True)
    
    # Simulate fused event
    fused_event = {
        "verification_score": 0.85,  # Slight drift
        "timestamp": "2025-12-24T00:00:00Z",
        "location": "Dadaab",
        "data_type": "PHI",
        "event_type": "outbreak",
        "consent_token": "VALID_TOKEN",
        "consent_valid": True,
        "explainability": None,  # Missing explanation!
        "data_subject_region": "KE"
    }
    
    # Ingest
    bridge.ingest_fused_event(fused_event, jurisdiction="KDPA_KE")
    
    # Check pending patches
    pending = bridge.get_pending_patches()
    print(f"\n📋 Pending patches: {len(pending)}")
    
    for patch in pending:
        print(f"\n🔧 {patch.patch_id}")
        print(f"   Framework: {patch.framework_id}")
        print(f"   Type: {patch.patch_type}")
        print(f"   Confidence: {patch.confidence:.2%}")
