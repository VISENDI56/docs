"""
HSML Reconciler
Advanced conflict resolution for distributed health data.

Features:
- Three-way merge for concurrent updates
- Semantic conflict detection
- Automatic resolution strategies
- Manual review queue for complex conflicts

Compliance:
- GDPR Art. 5 (Accuracy)
- HIPAA §164.312(c)(1) (Integrity)
- ISO 27001 A.12.2 (Protection from Malware)
"""

import json
import hashlib
from datetime import datetime
from typing import Dict, List, Optional, Tuple
from enum import Enum
from dataclasses import dataclass
import logging

logger = logging.getLogger(__name__)


class ConflictType(Enum):
    """Types of conflicts"""
    NO_CONFLICT = "no_conflict"
    TIMESTAMP_CONFLICT = "timestamp_conflict"
    VALUE_CONFLICT = "value_conflict"
    STRUCTURAL_CONFLICT = "structural_conflict"
    SEMANTIC_CONFLICT = "semantic_conflict"


class ResolutionStrategy(Enum):
    """Conflict resolution strategies"""
    LAST_WRITE_WINS = "last_write_wins"
    FIRST_WRITE_WINS = "first_write_wins"
    MERGE_PAYLOADS = "merge_payloads"
    MANUAL_REVIEW = "manual_review"
    HIGHEST_SEVERITY = "highest_severity"
    MOST_COMPLETE = "most_complete"


@dataclass
class ConflictReport:
    """Detailed conflict analysis"""
    conflict_id: str
    conflict_type: ConflictType
    local_event_id: str
    remote_event_id: str
    conflicting_fields: List[str]
    resolution_strategy: ResolutionStrategy
    resolved_event_id: Optional[str]
    requires_manual_review: bool
    confidence_score: float
    timestamp: str
    
    def to_dict(self) -> Dict:
        return {
            "conflict_id": self.conflict_id,
            "conflict_type": self.conflict_type.value,
            "local_event_id": self.local_event_id,
            "remote_event_id": self.remote_event_id,
            "conflicting_fields": self.conflicting_fields,
            "resolution_strategy": self.resolution_strategy.value,
            "resolved_event_id": self.resolved_event_id,
            "requires_manual_review": self.requires_manual_review,
            "confidence_score": self.confidence_score,
            "timestamp": self.timestamp
        }


class HSMLReconciler:
    """
    Advanced reconciliation engine for HSML events.
    
    Implements intelligent conflict resolution with semantic understanding.
    """
    
    def __init__(
        self,
        auto_resolve_threshold: float = 0.8,
        enable_semantic_analysis: bool = True
    ):
        self.auto_resolve_threshold = auto_resolve_threshold
        self.enable_semantic_analysis = enable_semantic_analysis
        
        # Conflict resolution rules
        self.resolution_rules = {
            "severity": ResolutionStrategy.HIGHEST_SEVERITY,
            "diagnosis": ResolutionStrategy.MANUAL_REVIEW,
            "location": ResolutionStrategy.MANUAL_REVIEW,
            "timestamp": ResolutionStrategy.LAST_WRITE_WINS,
            "reporter": ResolutionStrategy.MERGE_PAYLOADS
        }
        
        logger.info("🔀 HSML Reconciler initialized")
    
    def detect_conflict(
        self,
        local_payload: Dict,
        remote_payload: Dict
    ) -> Tuple[ConflictType, List[str]]:
        """
        Detect type and scope of conflict.
        
        Args:
            local_payload: Local event payload
            remote_payload: Remote event payload
        
        Returns:
            (conflict_type, conflicting_fields)
        """
        conflicting_fields = []
        
        # Check for structural differences
        local_keys = set(local_payload.keys())
        remote_keys = set(remote_payload.keys())
        
        if local_keys != remote_keys:
            return ConflictType.STRUCTURAL_CONFLICT, list(local_keys ^ remote_keys)
        
        # Check for value differences
        for key in local_keys:
            if local_payload[key] != remote_payload[key]:
                conflicting_fields.append(key)
        
        if not conflicting_fields:
            return ConflictType.NO_CONFLICT, []
        
        # Semantic conflict detection
        if self.enable_semantic_analysis:
            if self._is_semantic_conflict(local_payload, remote_payload, conflicting_fields):
                return ConflictType.SEMANTIC_CONFLICT, conflicting_fields
        
        # Value conflict
        return ConflictType.VALUE_CONFLICT, conflicting_fields
    
    def _is_semantic_conflict(
        self,
        local_payload: Dict,
        remote_payload: Dict,
        conflicting_fields: List[str]
    ) -> bool:
        """
        Detect semantic conflicts (e.g., contradictory diagnoses).
        
        Examples:
        - "malaria" vs "typhoid" (semantic conflict)
        - "fever" vs "high fever" (not semantic conflict)
        """
        semantic_fields = ["diagnosis", "symptom", "disease"]
        
        for field in conflicting_fields:
            if field in semantic_fields:
                local_value = str(local_payload.get(field, "")).lower()
                remote_value = str(remote_payload.get(field, "")).lower()
                
                # Check if values are contradictory
                if local_value and remote_value and local_value != remote_value:
                    # Simple heuristic: if neither is substring of the other
                    if local_value not in remote_value and remote_value not in local_value:
                        return True
        
        return False
    
    def select_resolution_strategy(
        self,
        conflict_type: ConflictType,
        conflicting_fields: List[str],
        local_payload: Dict,
        remote_payload: Dict
    ) -> ResolutionStrategy:
        """
        Select appropriate resolution strategy based on conflict type.
        
        Args:
            conflict_type: Type of conflict
            conflicting_fields: Fields with conflicts
            local_payload: Local event payload
            remote_payload: Remote event payload
        
        Returns:
            Resolution strategy
        """
        # Structural conflicts require manual review
        if conflict_type == ConflictType.STRUCTURAL_CONFLICT:
            return ResolutionStrategy.MANUAL_REVIEW
        
        # Semantic conflicts require manual review
        if conflict_type == ConflictType.SEMANTIC_CONFLICT:
            return ResolutionStrategy.MANUAL_REVIEW
        
        # Apply field-specific rules
        for field in conflicting_fields:
            if field in self.resolution_rules:
                strategy = self.resolution_rules[field]
                
                # If any field requires manual review, escalate
                if strategy == ResolutionStrategy.MANUAL_REVIEW:
                    return ResolutionStrategy.MANUAL_REVIEW
        
        # Default: merge payloads
        return ResolutionStrategy.MERGE_PAYLOADS
    
    def resolve_conflict(
        self,
        local_event: Dict,
        remote_event: Dict,
        strategy: ResolutionStrategy
    ) -> Tuple[Dict, float]:
        """
        Resolve conflict using specified strategy.
        
        Args:
            local_event: Local event
            remote_event: Remote event
            strategy: Resolution strategy
        
        Returns:
            (resolved_payload, confidence_score)
        """
        if strategy == ResolutionStrategy.LAST_WRITE_WINS:
            return self._last_write_wins(local_event, remote_event)
        
        elif strategy == ResolutionStrategy.FIRST_WRITE_WINS:
            return self._first_write_wins(local_event, remote_event)
        
        elif strategy == ResolutionStrategy.MERGE_PAYLOADS:
            return self._merge_payloads(local_event, remote_event)
        
        elif strategy == ResolutionStrategy.HIGHEST_SEVERITY:
            return self._highest_severity(local_event, remote_event)
        
        elif strategy == ResolutionStrategy.MOST_COMPLETE:
            return self._most_complete(local_event, remote_event)
        
        else:  # MANUAL_REVIEW
            return self._create_conflict_marker(local_event, remote_event)
    
    def _last_write_wins(
        self,
        local_event: Dict,
        remote_event: Dict
    ) -> Tuple[Dict, float]:
        """Last write wins strategy"""
        local_ts = datetime.fromisoformat(local_event["timestamp"])
        remote_ts = datetime.fromisoformat(remote_event["timestamp"])
        
        if local_ts > remote_ts:
            return local_event["payload"], 0.9
        else:
            return remote_event["payload"], 0.9
    
    def _first_write_wins(
        self,
        local_event: Dict,
        remote_event: Dict
    ) -> Tuple[Dict, float]:
        """First write wins strategy"""
        local_ts = datetime.fromisoformat(local_event["timestamp"])
        remote_ts = datetime.fromisoformat(remote_event["timestamp"])
        
        if local_ts < remote_ts:
            return local_event["payload"], 0.9
        else:
            return remote_event["payload"], 0.9
    
    def _merge_payloads(
        self,
        local_event: Dict,
        remote_event: Dict
    ) -> Tuple[Dict, float]:
        """Merge payloads with conflict markers"""
        merged = {}
        local_payload = local_event["payload"]
        remote_payload = remote_event["payload"]
        
        all_keys = set(local_payload.keys()) | set(remote_payload.keys())
        
        for key in all_keys:
            local_value = local_payload.get(key)
            remote_value = remote_payload.get(key)
            
            if local_value == remote_value:
                merged[key] = local_value
            elif local_value is None:
                merged[key] = remote_value
            elif remote_value is None:
                merged[key] = local_value
            else:
                # Conflict - keep both with markers
                merged[key] = {
                    "_conflict": True,
                    "_local": local_value,
                    "_remote": remote_value,
                    "_merged_at": datetime.utcnow().isoformat()
                }
        
        # Confidence depends on number of conflicts
        conflict_count = sum(1 for v in merged.values() if isinstance(v, dict) and v.get("_conflict"))
        confidence = max(0.5, 1.0 - (conflict_count / len(merged)))
        
        return merged, confidence
    
    def _highest_severity(
        self,
        local_event: Dict,
        remote_event: Dict
    ) -> Tuple[Dict, float]:
        """Choose event with highest severity"""
        local_severity = local_event["payload"].get("severity", 0)
        remote_severity = remote_event["payload"].get("severity", 0)
        
        if local_severity >= remote_severity:
            return local_event["payload"], 0.85
        else:
            return remote_event["payload"], 0.85
    
    def _most_complete(
        self,
        local_event: Dict,
        remote_event: Dict
    ) -> Tuple[Dict, float]:
        """Choose event with most complete data"""
        local_fields = sum(1 for v in local_event["payload"].values() if v is not None)
        remote_fields = sum(1 for v in remote_event["payload"].values() if v is not None)
        
        if local_fields >= remote_fields:
            return local_event["payload"], 0.8
        else:
            return remote_event["payload"], 0.8
    
    def _create_conflict_marker(
        self,
        local_event: Dict,
        remote_event: Dict
    ) -> Tuple[Dict, float]:
        """Create conflict marker for manual review"""
        conflict_payload = {
            "_requires_manual_review": True,
            "_conflict_type": "manual_review_required",
            "_local_event": local_event,
            "_remote_event": remote_event,
            "_created_at": datetime.utcnow().isoformat()
        }
        
        return conflict_payload, 0.0
    
    def reconcile(
        self,
        local_event: Dict,
        remote_event: Dict
    ) -> ConflictReport:
        """
        Full reconciliation workflow.
        
        Args:
            local_event: Local event
            remote_event: Remote event
        
        Returns:
            ConflictReport with resolution details
        """
        # Detect conflict
        conflict_type, conflicting_fields = self.detect_conflict(
            local_event["payload"],
            remote_event["payload"]
        )
        
        # Select strategy
        strategy = self.select_resolution_strategy(
            conflict_type,
            conflicting_fields,
            local_event["payload"],
            remote_event["payload"]
        )
        
        # Resolve conflict
        resolved_payload, confidence = self.resolve_conflict(
            local_event,
            remote_event,
            strategy
        )
        
        # Generate conflict ID
        conflict_id = hashlib.sha256(
            f"{local_event['event_id']}:{remote_event['event_id']}".encode()
        ).hexdigest()[:16]
        
        # Determine if manual review is required
        requires_manual_review = (
            strategy == ResolutionStrategy.MANUAL_REVIEW
            or confidence < self.auto_resolve_threshold
        )
        
        # Generate resolved event ID
        resolved_event_id = None
        if not requires_manual_review:
            resolved_event_id = hashlib.sha256(
                json.dumps(resolved_payload, sort_keys=True).encode()
            ).hexdigest()[:16]
        
        # Create conflict report
        report = ConflictReport(
            conflict_id=conflict_id,
            conflict_type=conflict_type,
            local_event_id=local_event["event_id"],
            remote_event_id=remote_event["event_id"],
            conflicting_fields=conflicting_fields,
            resolution_strategy=strategy,
            resolved_event_id=resolved_event_id,
            requires_manual_review=requires_manual_review,
            confidence_score=confidence,
            timestamp=datetime.utcnow().isoformat()
        )
        
        logger.info(
            f"🔀 Reconciliation complete - "
            f"Conflict: {conflict_type.value}, "
            f"Strategy: {strategy.value}, "
            f"Confidence: {confidence:.2f}"
        )
        
        return report


# Example usage
if __name__ == "__main__":
    reconciler = HSMLReconciler()
    
    # Example: Conflicting severity reports
    local_event = {
        "event_id": "local_001",
        "timestamp": "2025-12-23T10:00:00Z",
        "payload": {
            "location": "Dadaab",
            "symptom": "diarrhea",
            "severity": 8,
            "reporter": "CHV_AMINA"
        }
    }
    
    remote_event = {
        "event_id": "remote_001",
        "timestamp": "2025-12-23T10:05:00Z",
        "payload": {
            "location": "Dadaab",
            "symptom": "diarrhea",
            "severity": 9,
            "reporter": "CHV_HASSAN"
        }
    }
    
    # Reconcile
    report = reconciler.reconcile(local_event, remote_event)
    print(json.dumps(report.to_dict(), indent=2))
