"""
RefusalLogic Module - CoT-Based Refusals
Ensures iLuminara knows when to say "No" based on ethical constraints.

Provides Chain-of-Thought explanations for all refusals.
"""

import json
from typing import Dict, Optional, List
from enum import Enum

class RefusalReason(Enum):
    SOVEREIGNTY_VIOLATION = "sovereignty_violation"
    MISSING_CONSENT = "missing_consent"
    CHILD_PROTECTION = "child_protection"
    DISCRIMINATION_RISK = "discrimination_risk"
    DISPROPORTIONATE_ACTION = "disproportionate_action"
    CIVILIAN_HARM_RISK = "civilian_harm_risk"
    INSUFFICIENT_EXPLANATION = "insufficient_explanation"


class SafetyGate:
    """Safety gate with CoT-based refusal logic"""
    
    def __init__(self, ethical_specs_path: str = "governance_kernel/ethical_specifications.json"):
        with open(ethical_specs_path, 'r') as f:
            self.ethical_specs = json.load(f)
        
        self.refusal_templates = self._load_refusal_templates()
    
    def _load_refusal_templates(self) -> Dict[str, str]:
        """Load refusal templates from ethical specifications"""
        templates = {}
        for rule in self.ethical_specs["core_safety_rules"]:
            rule_id = rule["rule_id"]
            templates[rule_id] = rule["refusal_template"]
        return templates
    
    def should_refuse(self, query: Dict) -> Tuple[bool, Optional[str], Optional[List[str]]]:
        """
        Determine if query should be refused with CoT explanation.
        
        Returns:
            (should_refuse, reason, reasoning_chain)
        """
        reasoning_chain = []
        
        # Check 1: Data sovereignty (ESR-01)
        if self._violates_sovereignty(query):
            reasoning_chain.append("STEP 1: Checking data sovereignty...")
            reasoning_chain.append(f"  Destination: {query.get('destination', 'Unknown')}")
            reasoning_chain.append(f"  Jurisdiction: {query.get('jurisdiction', 'Unknown')}")
            reasoning_chain.append("  VIOLATION: Data cannot leave sovereign territory")
            
            refusal = self.refusal_templates["ESR-01"].format(
                destination=query.get('destination', 'Unknown'),
                jurisdiction=query.get('jurisdiction', 'Unknown'),
                legal_citations="GDPR Art. 9, Kenya DPA §37"
            )
            
            return True, refusal, reasoning_chain
        
        # Check 2: Missing consent (ESR-03)
        if not query.get('has_consent', False):
            reasoning_chain.append("STEP 1: Checking consent status...")
            reasoning_chain.append(f"  Consent: {query.get('has_consent', False)}")
            reasoning_chain.append("  VIOLATION: No explicit consent provided")
            
            refusal = self.refusal_templates["ESR-03"].format(
                legal_basis="GDPR Art. 6, POPIA §11",
                consent_status="MISSING",
                consent_scope="N/A"
            )
            
            return True, refusal, reasoning_chain
        
        # Check 3: Child protection (ESR-13)
        if query.get('is_child', False) and not query.get('guardian_consent', False):
            reasoning_chain.append("STEP 1: Checking child protection...")
            reasoning_chain.append(f"  Age: {query.get('age', 'Unknown')}")
            reasoning_chain.append(f"  Guardian consent: {query.get('guardian_consent', False)}")
            reasoning_chain.append("  VIOLATION: Minor requires guardian consent")
            
            refusal = self.refusal_templates["ESR-13"].format(
                legal_basis="UN Convention on Rights of the Child, GDPR Art. 8",
                status="MISSING_GUARDIAN_CONSENT"
            )
            
            return True, refusal, reasoning_chain
        
        # All checks passed
        reasoning_chain.append("STEP 1: All safety checks passed")
        reasoning_chain.append("  ✓ Data sovereignty compliant")
        reasoning_chain.append("  ✓ Consent obtained")
        reasoning_chain.append("  ✓ Child protection satisfied")
        
        return False, None, reasoning_chain
    
    def _violates_sovereignty(self, query: Dict) -> bool:
        """Check if query violates data sovereignty"""
        destination = query.get('destination', '').lower()
        jurisdiction = query.get('jurisdiction', 'GLOBAL_DEFAULT')
        
        # Block transfers to non-compliant regions
        blocked_destinations = ['aws_us', 'azure_asia', 'foreign_cloud']
        
        if any(blocked in destination for blocked in blocked_destinations):
            if jurisdiction in ['KDPA_KE', 'GDPR_EU', 'POPIA_ZA']:
                return True
        
        return False


def main():
    """Test safety gate"""
    gate = SafetyGate()
    
    # Test case 1: Sovereignty violation
    query1 = {
        "destination": "AWS_US",
        "jurisdiction": "KDPA_KE",
        "has_consent": True,
        "data_type": "PHI"
    }
    
    should_refuse, refusal, reasoning = gate.should_refuse(query1)
    
    if should_refuse:
        print("❌ REFUSAL:")
        print(f"   {refusal}")
        print("\n🧠 REASONING CHAIN:")
        for step in reasoning:
            print(f"   {step}")
    else:
        print("✅ APPROVED")
    
    print("\n" + "="*60 + "\n")
    
    # Test case 2: Missing consent
    query2 = {
        "destination": "Local_Node",
        "jurisdiction": "KDPA_KE",
        "has_consent": False,
        "data_type": "PHI"
    }
    
    should_refuse, refusal, reasoning = gate.should_refuse(query2)
    
    if should_refuse:
        print("❌ REFUSAL:")
        print(f"   {refusal}")
        print("\n🧠 REASONING CHAIN:")
        for step in reasoning:
            print(f"   {step}")


if __name__ == "__main__":
    main()
