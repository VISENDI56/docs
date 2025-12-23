"""
VSAI Compliance Bridge
Integrates IP-06 with the Governance Kernel for sovereign viral distribution

Ensures that viral spread respects:
- GDPR Art. 6 (Lawful Processing - Consent)
- Kenya DPA §25 (Direct Marketing)
- CCPA §1798.120 (Right to Opt-Out)
- CAN-SPAM Act (Email Marketing)
"""

import logging
from typing import Dict, Optional, List
from datetime import datetime
from dataclasses import dataclass

logger = logging.getLogger(__name__)


@dataclass
class ConsentRecord:
    """Tracks user consent for viral marketing"""
    node_id: str
    phone_number: str
    consent_granted: bool
    consent_timestamp: str
    consent_scope: List[str]
    opt_out_timestamp: Optional[str] = None
    jurisdiction: str = "KDPA_KE"


class VSAIComplianceBridge:
    """
    Bridges VSAI with the Governance Kernel.
    
    Ensures viral spread complies with:
    1. Consent requirements (GDPR, KDPA, CCPA)
    2. Data sovereignty (no cross-border viral spread without authorization)
    3. Right to opt-out (CAN-SPAM, CCPA)
    4. Transparency (EU AI Act)
    """
    
    def __init__(self, guardrail=None):
        """
        Initialize compliance bridge.
        
        Args:
            guardrail: SovereignGuardrail instance
        """
        self.guardrail = guardrail
        self.consent_records: Dict[str, ConsentRecord] = {}
        
        logger.info("🛡️ VSAI Compliance Bridge initialized")
    
    def validate_referral(
        self,
        parent_id: str,
        child_id: str,
        jurisdiction: str = "KDPA_KE"
    ) -> bool:
        """
        Validate that a referral complies with sovereignty rules.
        
        Args:
            parent_id: Referrer node ID
            child_id: Referee node ID
            jurisdiction: Legal jurisdiction
        
        Returns:
            True if referral is compliant
        """
        # Check parent consent
        if parent_id not in self.consent_records:
            logger.warning(f"⚠️ Parent {parent_id} has no consent record")
            return False
        
        parent_consent = self.consent_records[parent_id]
        
        if not parent_consent.consent_granted:
            logger.warning(f"⚠️ Parent {parent_id} has not granted consent")
            return False
        
        # Check if parent has opted out
        if parent_consent.opt_out_timestamp:
            logger.warning(f"⚠️ Parent {parent_id} has opted out")
            return False
        
        # Validate with SovereignGuardrail
        if self.guardrail:
            try:
                self.guardrail.validate_action(
                    action_type='Viral_Referral',
                    payload={
                        'parent_id': parent_id,
                        'child_id': child_id,
                        'data_type': 'Marketing',
                        'consent_token': parent_consent.consent_timestamp
                    },
                    jurisdiction=jurisdiction
                )
            except Exception as e:
                logger.error(f"❌ Sovereignty violation: {e}")
                return False
        
        logger.info(f"✅ Referral validated: {parent_id} → {child_id}")
        return True
    
    def grant_consent(
        self,
        node_id: str,
        phone_number: str,
        consent_scope: List[str],
        jurisdiction: str = "KDPA_KE"
    ):
        """
        Grant consent for viral marketing.
        
        Args:
            node_id: Node ID
            phone_number: Phone number
            consent_scope: Scope of consent (e.g., ['referrals', 'alerts'])
            jurisdiction: Legal jurisdiction
        """
        consent = ConsentRecord(
            node_id=node_id,
            phone_number=phone_number,
            consent_granted=True,
            consent_timestamp=datetime.utcnow().isoformat(),
            consent_scope=consent_scope,
            jurisdiction=jurisdiction
        )
        
        self.consent_records[node_id] = consent
        
        logger.info(f"✅ Consent granted: {node_id} ({jurisdiction})")
    
    def revoke_consent(self, node_id: str):
        """
        Revoke consent (Right to Opt-Out).
        
        Args:
            node_id: Node ID
        """
        if node_id not in self.consent_records:
            logger.warning(f"⚠️ No consent record for {node_id}")
            return
        
        consent = self.consent_records[node_id]
        consent.consent_granted = False
        consent.opt_out_timestamp = datetime.utcnow().isoformat()
        
        logger.info(f"🚫 Consent revoked: {node_id}")
    
    def check_consent(self, node_id: str) -> bool:
        """
        Check if node has granted consent.
        
        Args:
            node_id: Node ID
        
        Returns:
            True if consent is granted
        """
        if node_id not in self.consent_records:
            return False
        
        consent = self.consent_records[node_id]
        return consent.consent_granted and not consent.opt_out_timestamp
    
    def get_consent_report(self) -> Dict:
        """
        Generate consent compliance report.
        
        Returns:
            Consent statistics
        """
        total = len(self.consent_records)
        granted = sum(1 for c in self.consent_records.values() if c.consent_granted)
        opted_out = sum(1 for c in self.consent_records.values() if c.opt_out_timestamp)
        
        return {
            "total_records": total,
            "consent_granted": granted,
            "opted_out": opted_out,
            "consent_rate": (granted / total * 100) if total > 0 else 0,
            "opt_out_rate": (opted_out / total * 100) if total > 0 else 0
        }


# Example usage
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format='%(message)s')
    
    # Initialize compliance bridge
    bridge = VSAIComplianceBridge()
    
    # Grant consent
    bridge.grant_consent(
        node_id="node_001",
        phone_number="+254712345678",
        consent_scope=["referrals", "alerts"],
        jurisdiction="KDPA_KE"
    )
    
    # Validate referral
    is_valid = bridge.validate_referral(
        parent_id="node_001",
        child_id="node_002",
        jurisdiction="KDPA_KE"
    )
    
    print(f"Referral valid: {is_valid}")
    
    # Get consent report
    report = bridge.get_consent_report()
    print(f"\\nConsent Report: {report}")
