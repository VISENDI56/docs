"""
Quantum Nexus - Conflict Resolution Engine
Harmonizes conflicting regulatory mandates using priority logic and ethical reasoning.

The harmonizer that resolves conflicts (e.g., "Data Sovereignty vs. Cloud Processing").
"""

import json
import logging
from typing import Dict, List, Optional, Any, Tuple
from enum import Enum
from datetime import datetime
from pathlib import Path

logger = logging.getLogger(__name__)


class ConflictPriority(Enum):
    """Priority levels for conflict resolution"""
    SAFETY_CRITICAL = 1  # Life and death
    SOVEREIGNTY = 2  # Data sovereignty and national security
    PRIVACY = 3  # Individual privacy rights
    TRANSPARENCY = 4  # Public health transparency
    EFFICIENCY = 5  # Operational efficiency


class ConflictResolution:
    """Result of conflict resolution"""
    
    def __init__(
        self,
        conflict_id: str,
        frameworks_in_conflict: List[str],
        resolution: str,
        rationale: str,
        priority_applied: ConflictPriority,
        mitigation_measures: List[str],
        metadata: Optional[Dict] = None
    ):
        self.conflict_id = conflict_id
        self.frameworks_in_conflict = frameworks_in_conflict
        self.resolution = resolution
        self.rationale = rationale
        self.priority_applied = priority_applied
        self.mitigation_measures = mitigation_measures
        self.metadata = metadata or {}
        self.timestamp = datetime.utcnow().isoformat()
    
    def to_dict(self) -> Dict:
        return {
            "conflict_id": self.conflict_id,
            "frameworks_in_conflict": self.frameworks_in_conflict,
            "resolution": self.resolution,
            "rationale": self.rationale,
            "priority_applied": self.priority_applied.name,
            "mitigation_measures": self.mitigation_measures,
            "metadata": self.metadata,
            "timestamp": self.timestamp
        }


class QuantumNexus:
    """
    The harmonizer that resolves conflicts between regulatory frameworks.
    
    Example conflicts:
    - GDPR says "Minimize" but MDR says "Retain for Safety"
    - Data Sovereignty vs. Cloud Processing
    - IHR Transparency vs. Patient Privacy
    - OFAC Sanctions vs. Humanitarian Imperative
    """
    
    def __init__(self, laws_path: Optional[str] = None):
        """
        Initialize the Quantum Nexus.
        
        Args:
            laws_path: Path to sectoral_laws.json
        """
        if laws_path is None:
            laws_path = Path(__file__).parent / "sectoral_laws.json"
        
        with open(laws_path, 'r') as f:
            self.laws_registry = json.load(f)
        
        self.conflict_rules = self.laws_registry.get("conflict_resolution_rules", {})
        self.resolution_history = []
        
        logger.info("⚛️ Quantum Nexus initialized - Conflict harmonizer active")
    
    def harmonize_risk_vectors(
        self,
        frameworks: List[Dict],
        context: str,
        payload: Dict[str, Any]
    ) -> ConflictResolution:
        """
        Resolve conflicts between multiple frameworks.
        
        Args:
            frameworks: List of applicable frameworks
            context: Operational context
            payload: Operation payload
        
        Returns:
            ConflictResolution with harmonized decision
        """
        logger.info(f"⚛️ Harmonizing {len(frameworks)} frameworks for context: {context}")
        
        # Identify conflicts
        conflicts = self._identify_conflicts(frameworks, context, payload)
        
        if not conflicts:
            logger.info("✅ No conflicts detected")
            return ConflictResolution(
                conflict_id="NO_CONFLICT",
                frameworks_in_conflict=[],
                resolution="All frameworks aligned",
                rationale="No conflicting requirements detected",
                priority_applied=ConflictPriority.EFFICIENCY,
                mitigation_measures=[],
                metadata={"frameworks_count": len(frameworks)}
            )
        
        # Resolve each conflict
        resolutions = []
        for conflict in conflicts:
            resolution = self._resolve_conflict(conflict, context, payload)
            resolutions.append(resolution)
            self.resolution_history.append(resolution)
        
        # Return primary resolution
        return resolutions[0] if resolutions else None
    
    def _identify_conflicts(
        self,
        frameworks: List[Dict],
        context: str,
        payload: Dict[str, Any]
    ) -> List[Dict]:
        """
        Identify conflicts between frameworks.
        
        Returns:
            List of conflict definitions
        """
        conflicts = []
        
        framework_ids = [f.get("id") for f in frameworks]
        
        # Check for known conflicts
        for rule in self.conflict_rules.get("rules", []):
            conflict_name = rule.get("conflict", "")
            
            # GDPR Minimization vs MDR Safety Retention
            if "GDPR" in conflict_name and "MDR" in conflict_name:
                if "GDPR" in framework_ids and "EU_MDR" in framework_ids:
                    if payload.get("data_type") == "safety_critical":
                        conflicts.append({
                            "type": "GDPR_Minimization_vs_MDR_Safety_Retention",
                            "frameworks": ["GDPR", "EU_MDR"],
                            "rule": rule
                        })
            
            # Data Sovereignty vs Cloud Processing
            elif "Sovereignty" in conflict_name and "Cloud" in conflict_name:
                if payload.get("processing_location") == "cloud":
                    if any("MALABO" in fid or "KDPA" in fid or "POPIA" in fid for fid in framework_ids):
                        conflicts.append({
                            "type": "Data_Sovereignty_vs_Cloud_Processing",
                            "frameworks": [fid for fid in framework_ids if "MALABO" in fid or "KDPA" in fid or "POPIA" in fid],
                            "rule": rule
                        })
            
            # IHR Transparency vs Patient Privacy
            elif "IHR" in conflict_name and "Privacy" in conflict_name:
                if "IHR_2005_2025" in framework_ids and ("GDPR" in framework_ids or "HIPAA" in framework_ids):
                    if payload.get("outbreak_detected"):
                        conflicts.append({
                            "type": "IHR_Transparency_vs_Patient_Privacy",
                            "frameworks": ["IHR_2005_2025", "GDPR"],
                            "rule": rule
                        })
            
            # OFAC Sanctions vs Humanitarian Imperative
            elif "OFAC" in conflict_name and "Humanitarian" in conflict_name:
                if "OFAC_SANCTIONS" in framework_ids:
                    if payload.get("transaction_involves_sanctioned_entity"):
                        conflicts.append({
                            "type": "OFAC_Sanctions_vs_Humanitarian_Imperative",
                            "frameworks": ["OFAC_SANCTIONS"],
                            "rule": rule
                        })
        
        return conflicts
    
    def _resolve_conflict(
        self,
        conflict: Dict,
        context: str,
        payload: Dict[str, Any]
    ) -> ConflictResolution:
        """
        Resolve a specific conflict using priority logic.
        
        Args:
            conflict: Conflict definition
            context: Operational context
            payload: Operation payload
        
        Returns:
            ConflictResolution
        """
        conflict_type = conflict.get("type")
        rule = conflict.get("rule", {})
        
        logger.info(f"⚛️ Resolving conflict: {conflict_type}")
        
        # GDPR Minimization vs MDR Safety Retention
        if conflict_type == "GDPR_Minimization_vs_MDR_Safety_Retention":
            return ConflictResolution(
                conflict_id=conflict_type,
                frameworks_in_conflict=conflict.get("frameworks", []),
                resolution=rule.get("resolution", "Prioritize MDR for safety-critical data, but apply GDPR encryption"),
                rationale=rule.get("rationale", "Safety > Privacy when lives are at stake"),
                priority_applied=ConflictPriority.SAFETY_CRITICAL,
                mitigation_measures=[
                    "Retain safety-critical data as required by MDR",
                    "Apply AES-256 encryption (GDPR Art. 32)",
                    "Implement strict access controls",
                    "Minimize retention period to MDR minimum",
                    "Anonymize data after safety review period"
                ],
                metadata={
                    "data_type": payload.get("data_type"),
                    "retention_period_days": payload.get("retention_period_days", 1825)
                }
            )
        
        # Data Sovereignty vs Cloud Processing
        elif conflict_type == "Data_Sovereignty_vs_Cloud_Processing":
            return ConflictResolution(
                conflict_id=conflict_type,
                frameworks_in_conflict=conflict.get("frameworks", []),
                resolution=rule.get("resolution", "Use regional cloud zones with data residency guarantees"),
                rationale=rule.get("rationale", "Sovereignty is non-negotiable; technology must adapt"),
                priority_applied=ConflictPriority.SOVEREIGNTY,
                mitigation_measures=[
                    "Deploy to regional cloud zone (e.g., africa-south1)",
                    "Enable data residency guarantees",
                    "Implement edge processing for sensitive operations",
                    "Use local encryption keys (Cloud KMS regional)",
                    "Audit cross-border data flows"
                ],
                metadata={
                    "processing_location": payload.get("processing_location"),
                    "recommended_zone": self._get_sovereign_zone(payload)
                }
            )
        
        # IHR Transparency vs Patient Privacy
        elif conflict_type == "IHR_Transparency_vs_Patient_Privacy":
            return ConflictResolution(
                conflict_id=conflict_type,
                frameworks_in_conflict=conflict.get("frameworks", []),
                resolution=rule.get("resolution", "Anonymize data for IHR reporting, retain identifiable data locally"),
                rationale=rule.get("rationale", "Public health requires transparency, but individual privacy must be protected"),
                priority_applied=ConflictPriority.TRANSPARENCY,
                mitigation_measures=[
                    "Anonymize patient data for WHO reporting",
                    "Use k-anonymity (k≥5) for case data",
                    "Retain identifiable data locally with consent",
                    "Apply differential privacy for aggregate statistics",
                    "Implement secure multi-party computation for cross-border analysis"
                ],
                metadata={
                    "outbreak_detected": payload.get("outbreak_detected"),
                    "anonymization_method": "k-anonymity",
                    "k_value": 5
                }
            )
        
        # OFAC Sanctions vs Humanitarian Imperative
        elif conflict_type == "OFAC_Sanctions_vs_Humanitarian_Imperative":
            return ConflictResolution(
                conflict_id=conflict_type,
                frameworks_in_conflict=conflict.get("frameworks", []),
                resolution=rule.get("resolution", "Apply humanitarian exemptions for medicine, food, and emergency aid"),
                rationale=rule.get("rationale", "Sanctions must not prevent life-saving humanitarian assistance"),
                priority_applied=ConflictPriority.SAFETY_CRITICAL,
                mitigation_measures=[
                    "Verify humanitarian exemption category",
                    "Document exemption justification",
                    "Implement enhanced due diligence",
                    "Report to OFAC if required",
                    "Maintain audit trail of humanitarian transactions"
                ],
                metadata={
                    "exemption_type": payload.get("exemption_type"),
                    "sanctioned_entity": payload.get("sanctioned_entity"),
                    "humanitarian_justification": payload.get("humanitarian_justification")
                }
            )
        
        # Default resolution
        else:
            return ConflictResolution(
                conflict_id=conflict_type,
                frameworks_in_conflict=conflict.get("frameworks", []),
                resolution="Apply most restrictive requirement",
                rationale="When in doubt, prioritize compliance with strictest framework",
                priority_applied=ConflictPriority.PRIVACY,
                mitigation_measures=[
                    "Review conflict manually",
                    "Consult legal counsel",
                    "Document decision rationale"
                ],
                metadata={"conflict_type": conflict_type}
            )
    
    def _get_sovereign_zone(self, payload: Dict[str, Any]) -> str:
        """Get recommended sovereign cloud zone based on jurisdiction"""
        jurisdiction = payload.get("jurisdiction", "")
        
        zone_mapping = {
            "KENYA": "africa-south1",
            "SOUTH_AFRICA": "africa-south1",
            "NIGERIA": "africa-south1",
            "EU": "europe-west1",
            "GERMANY": "europe-west4",
            "USA": "us-central1",
            "CANADA": "northamerica-northeast1"
        }
        
        return zone_mapping.get(jurisdiction, "africa-south1")
    
    def retroactive_alignment_engine(
        self,
        historical_transactions: List[Dict],
        new_law: Dict
    ) -> List[Dict]:
        """
        Scan historical transactions against new laws.
        
        Args:
            historical_transactions: List of past transactions
            new_law: New law to check against
        
        Returns:
            List of non-compliant transactions requiring remediation
        """
        logger.info(f"⚛️ Running retroactive alignment for {new_law.get('id')}")
        
        non_compliant = []
        
        for transaction in historical_transactions:
            # Check if new law is retroactive
            if not new_law.get("retroactive", False):
                continue
            
            # Check if transaction falls within retroactive window
            retroactive_window_days = new_law.get("retroactive_window_days", 90)
            transaction_date = datetime.fromisoformat(transaction.get("timestamp"))
            days_ago = (datetime.utcnow() - transaction_date).days
            
            if days_ago > retroactive_window_days:
                continue
            
            # Check if transaction would violate new law
            # This is simplified - in production, use full compliance engine
            if self._would_violate_new_law(transaction, new_law):
                non_compliant.append({
                    "transaction": transaction,
                    "law": new_law.get("id"),
                    "violation": f"Transaction does not comply with {new_law.get('name')}",
                    "remediation_required": True
                })
        
        logger.info(f"⚛️ Found {len(non_compliant)} non-compliant historical transactions")
        
        return non_compliant
    
    def _would_violate_new_law(self, transaction: Dict, new_law: Dict) -> bool:
        """Check if a transaction would violate a new law"""
        # Simplified check - in production, use full compliance engine
        law_id = new_law.get("id")
        
        if law_id == "IHR_2005_2025":
            # Check if outbreak was detected but not reported
            if transaction.get("outbreak_detected") and not transaction.get("ihr_notification_sent"):
                return True
        
        return False
    
    def get_resolution_history(self, limit: int = 10) -> List[Dict]:
        """Get recent conflict resolutions"""
        return [r.to_dict() for r in self.resolution_history[-limit:]]
    
    def get_conflict_statistics(self) -> Dict:
        """Get statistics on conflict resolutions"""
        if not self.resolution_history:
            return {
                "total_conflicts": 0,
                "by_priority": {},
                "by_type": {}
            }
        
        by_priority = {}
        by_type = {}
        
        for resolution in self.resolution_history:
            # Count by priority
            priority = resolution.priority_applied.name
            by_priority[priority] = by_priority.get(priority, 0) + 1
            
            # Count by type
            conflict_type = resolution.conflict_id
            by_type[conflict_type] = by_type.get(conflict_type, 0) + 1
        
        return {
            "total_conflicts": len(self.resolution_history),
            "by_priority": by_priority,
            "by_type": by_type
        }


# Example usage
if __name__ == "__main__":
    nexus = QuantumNexus()
    
    # Example 1: GDPR vs MDR conflict
    frameworks = [
        {"id": "GDPR", "name": "GDPR"},
        {"id": "EU_MDR", "name": "EU Medical Device Regulation"}
    ]
    
    resolution = nexus.harmonize_risk_vectors(
        frameworks=frameworks,
        context="medical_device_data_retention",
        payload={
            "data_type": "safety_critical",
            "retention_period_days": 1825
        }
    )
    
    print(f"\n{'='*60}")
    print("Example 1: GDPR Minimization vs MDR Safety Retention")
    print(f"{'='*60}")
    print(f"Resolution: {resolution.resolution}")
    print(f"Rationale: {resolution.rationale}")
    print(f"Priority: {resolution.priority_applied.name}")
    print(f"Mitigation Measures:")
    for measure in resolution.mitigation_measures:
        print(f"  - {measure}")
    
    # Example 2: Data Sovereignty vs Cloud Processing
    frameworks = [
        {"id": "AU_MALABO_CONVENTION", "name": "AU Malabo Convention"},
        {"id": "KENYA_DPA", "name": "Kenya Data Protection Act"}
    ]
    
    resolution = nexus.harmonize_risk_vectors(
        frameworks=frameworks,
        context="cloud_data_processing",
        payload={
            "processing_location": "cloud",
            "jurisdiction": "KENYA",
            "data_type": "PHI"
        }
    )
    
    print(f"\n{'='*60}")
    print("Example 2: Data Sovereignty vs Cloud Processing")
    print(f"{'='*60}")
    print(f"Resolution: {resolution.resolution}")
    print(f"Recommended Zone: {resolution.metadata.get('recommended_zone')}")
    print(f"Mitigation Measures:")
    for measure in resolution.mitigation_measures:
        print(f"  - {measure}")
    
    # Get statistics
    stats = nexus.get_conflict_statistics()
    print(f"\n{'='*60}")
    print("Conflict Resolution Statistics")
    print(f"{'='*60}")
    print(f"Total Conflicts Resolved: {stats['total_conflicts']}")
    print(f"By Priority: {stats['by_priority']}")
    print(f"By Type: {stats['by_type']}")
