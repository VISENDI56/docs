"""
IP-09: Chrono-Audit
Retroactive compliance verification when laws change

Allows iLuminara to:
1. Re-audit historical actions against new legal frameworks
2. Prove compliance at the time of action (even if law changed later)
3. Generate compliance reports for any point in time
4. Handle regulatory changes without data migration

Compliance:
- GDPR Art. 30 (Records of Processing Activities)
- ISO 27001 A.18.1.5 (Regulation of Cryptographic Controls)
- SOC 2 (Logical and Physical Access Controls)
"""

import json
import hashlib
from datetime import datetime, timedelta
from typing import Dict, List, Optional
from enum import Enum
import logging

logger = logging.getLogger(__name__)


class LawChangeType(Enum):
    """Types of legal framework changes"""
    NEW_LAW = "new_law"
    AMENDMENT = "amendment"
    REPEAL = "repeal"
    INTERPRETATION_CHANGE = "interpretation_change"
    THRESHOLD_CHANGE = "threshold_change"


class ChronoAudit:
    """
    IP-09: Chrono-Audit for retroactive compliance verification
    
    Maintains a temporal ledger of:
    - All actions taken by the system
    - Legal frameworks in effect at time of action
    - Compliance decisions made
    - Law changes over time
    
    Enables:
    - Retroactive audits when laws change
    - Proof of compliance at time of action
    - Historical compliance reports
    - Regulatory change impact analysis
    """
    
    def __init__(
        self,
        storage_path: str = "./chrono_audit",
        enable_cryptographic_proof: bool = True
    ):
        self.storage_path = storage_path
        self.enable_cryptographic_proof = enable_cryptographic_proof
        
        # Temporal ledger
        self.action_ledger = []
        self.law_version_ledger = []
        self.compliance_decision_ledger = []
        
        # Hash chain for tamper-proof audit
        self.previous_hash = "0" * 64  # Genesis hash
        
        logger.info("⏰ IP-09 Chrono-Audit initialized")
    
    def log_action(
        self,
        action_type: str,
        payload: Dict,
        context: str,
        jurisdiction: str,
        actor: str
    ) -> str:
        """
        Log an action to the temporal ledger
        
        Args:
            action_type: Type of action (Data_Transfer, High_Risk_Inference, etc.)
            payload: Action payload
            context: Sectoral context
            jurisdiction: Legal jurisdiction
            actor: Who performed the action
        
        Returns:
            Action ID (hash)
        """
        timestamp = datetime.utcnow()
        
        action_record = {
            "action_id": None,  # Will be set after hashing
            "timestamp": timestamp.isoformat(),
            "action_type": action_type,
            "payload": payload,
            "context": context,
            "jurisdiction": jurisdiction,
            "actor": actor,
            "applicable_laws_at_time": self._get_applicable_laws(timestamp, context, jurisdiction),
            "previous_hash": self.previous_hash
        }
        
        # Generate action ID (hash of record)
        action_id = self._hash_record(action_record)
        action_record["action_id"] = action_id
        
        # Update hash chain
        self.previous_hash = action_id
        
        # Store in ledger
        self.action_ledger.append(action_record)
        
        logger.info(f"📝 Action logged: {action_id[:16]}... ({action_type})")
        
        return action_id
    
    def log_compliance_decision(
        self,
        action_id: str,
        framework_id: str,
        compliant: bool,
        violations: List[Dict],
        decision_rationale: str
    ):
        """
        Log a compliance decision for an action
        
        Args:
            action_id: ID of the action being evaluated
            framework_id: Legal framework being checked
            compliant: Whether action was compliant
            violations: List of violations (if any)
            decision_rationale: Explanation of decision
        """
        timestamp = datetime.utcnow()
        
        decision_record = {
            "decision_id": None,
            "timestamp": timestamp.isoformat(),
            "action_id": action_id,
            "framework_id": framework_id,
            "framework_version": self._get_law_version(framework_id, timestamp),
            "compliant": compliant,
            "violations": violations,
            "decision_rationale": decision_rationale,
            "previous_hash": self.previous_hash
        }
        
        # Generate decision ID
        decision_id = self._hash_record(decision_record)
        decision_record["decision_id"] = decision_id
        
        # Update hash chain
        self.previous_hash = decision_id
        
        # Store in ledger
        self.compliance_decision_ledger.append(decision_record)
        
        logger.info(f"⚖️ Compliance decision logged: {decision_id[:16]}... (Compliant: {compliant})")
    
    def log_law_change(
        self,
        framework_id: str,
        change_type: LawChangeType,
        effective_date: datetime,
        changes: Dict,
        description: str
    ):
        """
        Log a change to a legal framework
        
        Args:
            framework_id: ID of the framework being changed
            change_type: Type of change
            effective_date: When the change takes effect
            changes: Dictionary of specific changes
            description: Human-readable description
        """
        timestamp = datetime.utcnow()
        
        law_change_record = {
            "change_id": None,
            "timestamp": timestamp.isoformat(),
            "framework_id": framework_id,
            "change_type": change_type.value,
            "effective_date": effective_date.isoformat(),
            "changes": changes,
            "description": description,
            "previous_hash": self.previous_hash
        }
        
        # Generate change ID
        change_id = self._hash_record(law_change_record)
        law_change_record["change_id"] = change_id
        
        # Update hash chain
        self.previous_hash = change_id
        
        # Store in ledger
        self.law_version_ledger.append(law_change_record)
        
        logger.info(f"📜 Law change logged: {change_id[:16]}... ({framework_id})")
        
        # Trigger retroactive audit
        self._trigger_retroactive_audit(framework_id, effective_date)
    
    def retroactive_audit(
        self,
        framework_id: str,
        start_date: datetime,
        end_date: Optional[datetime] = None
    ) -> Dict:
        """
        Perform retroactive audit of actions against a framework
        
        Args:
            framework_id: Framework to audit against
            start_date: Start of audit period
            end_date: End of audit period (default: now)
        
        Returns:
            Audit report with compliance status
        """
        if end_date is None:
            end_date = datetime.utcnow()
        
        logger.info(f"🔍 Starting retroactive audit: {framework_id} ({start_date} to {end_date})")
        
        # Find all actions in time period
        actions_in_period = [
            action for action in self.action_ledger
            if start_date <= datetime.fromisoformat(action["timestamp"]) <= end_date
        ]
        
        # Re-evaluate each action against current framework version
        audit_results = {
            "framework_id": framework_id,
            "audit_period": {
                "start": start_date.isoformat(),
                "end": end_date.isoformat()
            },
            "total_actions": len(actions_in_period),
            "compliant_then": 0,
            "compliant_now": 0,
            "newly_non_compliant": [],
            "newly_compliant": [],
            "unchanged": 0
        }
        
        for action in actions_in_period:
            # Get original compliance decision
            original_decision = self._get_compliance_decision(action["action_id"], framework_id)
            
            # Re-evaluate with current framework version
            current_evaluation = self._evaluate_action_against_framework(
                action,
                framework_id,
                datetime.utcnow()  # Use current framework version
            )
            
            # Compare
            if original_decision:
                was_compliant = original_decision["compliant"]
                is_compliant = current_evaluation["compliant"]
                
                if was_compliant:
                    audit_results["compliant_then"] += 1
                
                if is_compliant:
                    audit_results["compliant_now"] += 1
                
                if was_compliant and not is_compliant:
                    audit_results["newly_non_compliant"].append({
                        "action_id": action["action_id"],
                        "timestamp": action["timestamp"],
                        "action_type": action["action_type"],
                        "violations": current_evaluation["violations"]
                    })
                elif not was_compliant and is_compliant:
                    audit_results["newly_compliant"].append({
                        "action_id": action["action_id"],
                        "timestamp": action["timestamp"],
                        "action_type": action["action_type"]
                    })
                else:
                    audit_results["unchanged"] += 1
        
        logger.info(f"✅ Retroactive audit complete: {audit_results['compliant_now']}/{audit_results['total_actions']} compliant")
        
        return audit_results
    
    def generate_compliance_report(
        self,
        start_date: datetime,
        end_date: datetime,
        frameworks: Optional[List[str]] = None
    ) -> Dict:
        """
        Generate compliance report for a time period
        
        Args:
            start_date: Start of report period
            end_date: End of report period
            frameworks: Specific frameworks to report on (default: all)
        
        Returns:
            Comprehensive compliance report
        """
        logger.info(f"📊 Generating compliance report: {start_date} to {end_date}")
        
        # Find all actions in period
        actions_in_period = [
            action for action in self.action_ledger
            if start_date <= datetime.fromisoformat(action["timestamp"]) <= end_date
        ]
        
        # Find all compliance decisions in period
        decisions_in_period = [
            decision for decision in self.compliance_decision_ledger
            if start_date <= datetime.fromisoformat(decision["timestamp"]) <= end_date
        ]
        
        # Filter by frameworks if specified
        if frameworks:
            decisions_in_period = [
                d for d in decisions_in_period
                if d["framework_id"] in frameworks
            ]
        
        # Calculate statistics
        total_decisions = len(decisions_in_period)
        compliant_decisions = len([d for d in decisions_in_period if d["compliant"]])
        non_compliant_decisions = total_decisions - compliant_decisions
        
        # Group by framework
        by_framework = {}
        for decision in decisions_in_period:
            framework_id = decision["framework_id"]
            if framework_id not in by_framework:
                by_framework[framework_id] = {
                    "total": 0,
                    "compliant": 0,
                    "non_compliant": 0,
                    "violations": []
                }
            
            by_framework[framework_id]["total"] += 1
            if decision["compliant"]:
                by_framework[framework_id]["compliant"] += 1
            else:
                by_framework[framework_id]["non_compliant"] += 1
                by_framework[framework_id]["violations"].extend(decision["violations"])
        
        report = {
            "report_period": {
                "start": start_date.isoformat(),
                "end": end_date.isoformat()
            },
            "summary": {
                "total_actions": len(actions_in_period),
                "total_compliance_checks": total_decisions,
                "compliant": compliant_decisions,
                "non_compliant": non_compliant_decisions,
                "compliance_rate": compliant_decisions / total_decisions if total_decisions > 0 else 0
            },
            "by_framework": by_framework,
            "generated_at": datetime.utcnow().isoformat()
        }
        
        logger.info(f"✅ Compliance report generated: {compliant_decisions}/{total_decisions} compliant")
        
        return report
    
    def prove_compliance_at_time(
        self,
        action_id: str,
        framework_id: str
    ) -> Dict:
        """
        Prove that an action was compliant at the time it was taken
        
        Args:
            action_id: ID of the action
            framework_id: Framework to prove compliance against
        
        Returns:
            Compliance proof with cryptographic verification
        """
        # Find action
        action = next((a for a in self.action_ledger if a["action_id"] == action_id), None)
        if not action:
            return {"error": "Action not found"}
        
        # Find compliance decision
        decision = self._get_compliance_decision(action_id, framework_id)
        if not decision:
            return {"error": "Compliance decision not found"}
        
        # Get framework version at time of action
        action_time = datetime.fromisoformat(action["timestamp"])
        framework_version = self._get_law_version(framework_id, action_time)
        
        # Generate cryptographic proof
        proof = {
            "action_id": action_id,
            "action_timestamp": action["timestamp"],
            "framework_id": framework_id,
            "framework_version_at_time": framework_version,
            "compliant_at_time": decision["compliant"],
            "decision_rationale": decision["decision_rationale"],
            "cryptographic_proof": self._generate_cryptographic_proof(action, decision)
        }
        
        logger.info(f"🔐 Compliance proof generated for action {action_id[:16]}...")
        
        return proof
    
    def verify_chain_integrity(self) -> Dict:
        """
        Verify the integrity of the hash chain
        
        Returns:
            Verification result
        """
        logger.info("🔍 Verifying hash chain integrity...")
        
        all_records = (
            self.action_ledger +
            self.compliance_decision_ledger +
            self.law_version_ledger
        )
        
        # Sort by timestamp
        all_records.sort(key=lambda r: r["timestamp"])
        
        # Verify chain
        expected_hash = "0" * 64  # Genesis hash
        for record in all_records:
            if record["previous_hash"] != expected_hash:
                return {
                    "valid": False,
                    "error": f"Hash chain broken at record {record.get('action_id') or record.get('decision_id') or record.get('change_id')}",
                    "expected_hash": expected_hash,
                    "actual_hash": record["previous_hash"]
                }
            
            # Calculate expected next hash
            expected_hash = self._hash_record(record)
        
        logger.info("✅ Hash chain integrity verified")
        
        return {
            "valid": True,
            "total_records": len(all_records),
            "chain_length": len(all_records)
        }
    
    # ========== INTERNAL METHODS ==========
    
    def _hash_record(self, record: Dict) -> str:
        """Generate SHA-256 hash of a record"""
        # Remove hash fields before hashing
        record_copy = record.copy()
        record_copy.pop("action_id", None)
        record_copy.pop("decision_id", None)
        record_copy.pop("change_id", None)
        
        record_json = json.dumps(record_copy, sort_keys=True)
        return hashlib.sha256(record_json.encode()).hexdigest()
    
    def _get_applicable_laws(
        self,
        timestamp: datetime,
        context: str,
        jurisdiction: str
    ) -> List[str]:
        """Get list of laws applicable at a specific time"""
        # In production, this would query the law version ledger
        # For now, return a static list
        return ["GDPR", "KDPA", "HIPAA", "POPIA"]
    
    def _get_law_version(self, framework_id: str, timestamp: datetime) -> str:
        """Get version of a law at a specific time"""
        # Find most recent law change before timestamp
        applicable_changes = [
            change for change in self.law_version_ledger
            if change["framework_id"] == framework_id
            and datetime.fromisoformat(change["effective_date"]) <= timestamp
        ]
        
        if applicable_changes:
            # Sort by effective date and get most recent
            applicable_changes.sort(key=lambda c: c["effective_date"], reverse=True)
            return applicable_changes[0]["change_id"]
        
        return "original"
    
    def _get_compliance_decision(self, action_id: str, framework_id: str) -> Optional[Dict]:
        """Get compliance decision for an action and framework"""
        return next(
            (d for d in self.compliance_decision_ledger
             if d["action_id"] == action_id and d["framework_id"] == framework_id),
            None
        )
    
    def _evaluate_action_against_framework(
        self,
        action: Dict,
        framework_id: str,
        evaluation_time: datetime
    ) -> Dict:
        """Re-evaluate an action against a framework at a specific time"""
        # In production, this would use the actual compliance checker
        # For now, return a mock evaluation
        return {
            "compliant": True,
            "violations": []
        }
    
    def _generate_cryptographic_proof(self, action: Dict, decision: Dict) -> str:
        """Generate cryptographic proof of compliance"""
        proof_data = {
            "action_hash": action["action_id"],
            "decision_hash": decision["decision_id"],
            "chain_verification": self.verify_chain_integrity()["valid"]
        }
        
        proof_json = json.dumps(proof_data, sort_keys=True)
        return hashlib.sha256(proof_json.encode()).hexdigest()
    
    def _trigger_retroactive_audit(self, framework_id: str, effective_date: datetime):
        """Trigger retroactive audit when a law changes"""
        logger.info(f"🔄 Triggering retroactive audit for {framework_id} (effective: {effective_date})")
        
        # Audit all actions from 1 year before effective date to now
        start_date = effective_date - timedelta(days=365)
        audit_result = self.retroactive_audit(framework_id, start_date)
        
        # Log audit result
        logger.info(f"📊 Retroactive audit complete: {audit_result['newly_non_compliant'].__len__()} newly non-compliant actions")


# Example usage
if __name__ == "__main__":
    chrono = ChronoAudit()
    
    # Log an action
    action_id = chrono.log_action(
        action_type="Data_Transfer",
        payload={"data_type": "PHI", "destination": "Cloud_Storage"},
        context="supply_chain",
        jurisdiction="GDPR_EU",
        actor="system"
    )
    
    # Log compliance decision
    chrono.log_compliance_decision(
        action_id=action_id,
        framework_id="GDPR",
        compliant=True,
        violations=[],
        decision_rationale="Data transfer within EU, compliant with GDPR Art. 9"
    )
    
    # Simulate law change
    chrono.log_law_change(
        framework_id="GDPR",
        change_type=LawChangeType.AMENDMENT,
        effective_date=datetime.utcnow(),
        changes={"article_9": "New interpretation of special categories"},
        description="GDPR Art. 9 interpretation updated by EDPB"
    )
    
    # Generate compliance report
    report = chrono.generate_compliance_report(
        start_date=datetime.utcnow() - timedelta(days=30),
        end_date=datetime.utcnow()
    )
    
    print(json.dumps(report, indent=2))
    
    # Verify chain integrity
    integrity = chrono.verify_chain_integrity()
    print(f"Chain integrity: {integrity}")
