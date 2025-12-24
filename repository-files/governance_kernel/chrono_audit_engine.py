"""
ChronoAuditEngine: Retroactive Compliance Validation
Part of Governance Kernel v3.0 - The Regulatory Singularity

Enables time-travel compliance auditing:
- Retroactive validation against historical regulations
- Forward-looking compliance forecasting
- Temporal conflict detection
- Regulatory change impact analysis

Compliance:
- GDPR Art. 30 (Records of Processing Activities)
- HIPAA §164.312(b) (Audit Controls)
- SOC 2 (Logging and Monitoring)
- ISO 27001 A.12.4.1 (Event Logging)
"""

import json
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
from enum import Enum
from dataclasses import dataclass, asdict
import hashlib
import logging

logger = logging.getLogger(__name__)


class TemporalDirection(Enum):
    """Direction of temporal compliance validation"""
    RETROACTIVE = "retroactive"  # Validate against past regulations
    CURRENT = "current"  # Validate against current regulations
    PROSPECTIVE = "prospective"  # Validate against future regulations


class ComplianceStatus(Enum):
    """Compliance status at a point in time"""
    COMPLIANT = "compliant"
    NON_COMPLIANT = "non_compliant"
    PARTIALLY_COMPLIANT = "partially_compliant"
    UNKNOWN = "unknown"
    GRANDFATHERED = "grandfathered"  # Exempt due to pre-existing status


@dataclass
class RegulatorySnapshot:
    """Snapshot of regulatory state at a specific time"""
    timestamp: str
    frameworks: List[str]
    requirements: Dict[str, any]
    jurisdiction: str
    version: str
    
    def to_dict(self) -> Dict:
        return asdict(self)


@dataclass
class ComplianceEvent:
    """A compliance-relevant event in the audit trail"""
    event_id: str
    timestamp: str
    action_type: str
    actor: str
    resource: str
    jurisdiction: str
    frameworks_applicable: List[str]
    compliance_status: ComplianceStatus
    metadata: Dict
    
    def to_dict(self) -> Dict:
        result = asdict(self)
        result['compliance_status'] = self.compliance_status.value
        return result


@dataclass
class TemporalComplianceReport:
    """Report of compliance status across time"""
    report_id: str
    generated_at: str
    time_range: Tuple[str, str]
    direction: TemporalDirection
    events_analyzed: int
    compliant_events: int
    non_compliant_events: int
    compliance_rate: float
    violations: List[Dict]
    recommendations: List[str]
    
    def to_dict(self) -> Dict:
        result = asdict(self)
        result['direction'] = self.direction.value
        return result


class ChronoAuditEngine:
    """
    Time-travel compliance auditing engine.
    
    Validates actions against:
    1. Historical regulations (retroactive compliance)
    2. Current regulations (real-time compliance)
    3. Upcoming regulations (prospective compliance)
    """
    
    def __init__(
        self,
        audit_storage_path: str = "./audit_trail",
        regulatory_history_path: str = "./regulatory_history"
    ):
        self.audit_storage_path = audit_storage_path
        self.regulatory_history_path = regulatory_history_path
        
        # In-memory audit trail
        self.audit_trail: List[ComplianceEvent] = []
        
        # Regulatory snapshots indexed by timestamp
        self.regulatory_snapshots: Dict[str, RegulatorySnapshot] = {}
        
        logger.info("⏰ ChronoAuditEngine initialized")
    
    def record_event(
        self,
        action_type: str,
        actor: str,
        resource: str,
        jurisdiction: str,
        frameworks_applicable: List[str],
        metadata: Optional[Dict] = None
    ) -> ComplianceEvent:
        """
        Record a compliance event in the audit trail.
        
        Args:
            action_type: Type of action (Data_Transfer, High_Risk_Inference, etc.)
            actor: Who performed the action
            resource: What was acted upon
            jurisdiction: Applicable jurisdiction
            frameworks_applicable: Legal frameworks that apply
            metadata: Additional context
        
        Returns:
            ComplianceEvent with compliance status
        """
        timestamp = datetime.utcnow().isoformat()
        event_id = hashlib.sha256(
            f"{timestamp}{action_type}{actor}{resource}".encode()
        ).hexdigest()[:16]
        
        # Validate against current regulations
        compliance_status = self._validate_current_compliance(
            action_type=action_type,
            jurisdiction=jurisdiction,
            frameworks=frameworks_applicable,
            metadata=metadata or {}
        )
        
        event = ComplianceEvent(
            event_id=event_id,
            timestamp=timestamp,
            action_type=action_type,
            actor=actor,
            resource=resource,
            jurisdiction=jurisdiction,
            frameworks_applicable=frameworks_applicable,
            compliance_status=compliance_status,
            metadata=metadata or {}
        )
        
        self.audit_trail.append(event)
        
        logger.info(f"📝 Event recorded: {event_id} - Status: {compliance_status.value}")
        
        return event
    
    def retroactive_audit(
        self,
        start_date: str,
        end_date: str,
        jurisdiction: Optional[str] = None,
        frameworks: Optional[List[str]] = None
    ) -> TemporalComplianceReport:
        """
        Perform retroactive compliance audit.
        
        Validates historical events against regulations that were in effect
        at the time of the event.
        
        Args:
            start_date: Start of audit period (ISO format)
            end_date: End of audit period (ISO format)
            jurisdiction: Filter by jurisdiction
            frameworks: Filter by frameworks
        
        Returns:
            TemporalComplianceReport with findings
        """
        logger.info(f"🔍 Starting retroactive audit: {start_date} to {end_date}")
        
        # Filter events in time range
        events = self._filter_events(
            start_date=start_date,
            end_date=end_date,
            jurisdiction=jurisdiction,
            frameworks=frameworks
        )
        
        violations = []
        compliant_count = 0
        non_compliant_count = 0
        
        for event in events:
            # Get regulatory snapshot at event time
            snapshot = self._get_regulatory_snapshot(event.timestamp)
            
            # Re-validate event against historical regulations
            historical_status = self._validate_against_snapshot(event, snapshot)
            
            if historical_status == ComplianceStatus.COMPLIANT:
                compliant_count += 1
            elif historical_status == ComplianceStatus.NON_COMPLIANT:
                non_compliant_count += 1
                violations.append({
                    "event_id": event.event_id,
                    "timestamp": event.timestamp,
                    "action_type": event.action_type,
                    "violation": f"Non-compliant with {snapshot.frameworks}",
                    "severity": "HIGH"
                })
        
        compliance_rate = compliant_count / len(events) if events else 0.0
        
        # Generate recommendations
        recommendations = self._generate_recommendations(violations)
        
        report = TemporalComplianceReport(
            report_id=hashlib.sha256(f"{start_date}{end_date}".encode()).hexdigest()[:16],
            generated_at=datetime.utcnow().isoformat(),
            time_range=(start_date, end_date),
            direction=TemporalDirection.RETROACTIVE,
            events_analyzed=len(events),
            compliant_events=compliant_count,
            non_compliant_events=non_compliant_count,
            compliance_rate=compliance_rate,
            violations=violations,
            recommendations=recommendations
        )
        
        logger.info(f"✅ Retroactive audit complete - Compliance rate: {compliance_rate:.1%}")
        
        return report
    
    def prospective_audit(
        self,
        upcoming_regulation: Dict,
        effective_date: str,
        jurisdiction: str
    ) -> TemporalComplianceReport:
        """
        Perform prospective compliance audit.
        
        Validates current operations against upcoming regulations to identify
        gaps before they become violations.
        
        Args:
            upcoming_regulation: Details of new regulation
            effective_date: When regulation takes effect
            jurisdiction: Applicable jurisdiction
        
        Returns:
            TemporalComplianceReport with gap analysis
        """
        logger.info(f"🔮 Starting prospective audit for {upcoming_regulation.get('name')}")
        
        # Get recent events (last 30 days)
        end_date = datetime.utcnow()
        start_date = end_date - timedelta(days=30)
        
        events = self._filter_events(
            start_date=start_date.isoformat(),
            end_date=end_date.isoformat(),
            jurisdiction=jurisdiction
        )
        
        violations = []
        compliant_count = 0
        non_compliant_count = 0
        
        for event in events:
            # Validate against upcoming regulation
            future_status = self._validate_against_future_regulation(
                event, upcoming_regulation
            )
            
            if future_status == ComplianceStatus.COMPLIANT:
                compliant_count += 1
            elif future_status == ComplianceStatus.NON_COMPLIANT:
                non_compliant_count += 1
                violations.append({
                    "event_id": event.event_id,
                    "timestamp": event.timestamp,
                    "action_type": event.action_type,
                    "violation": f"Will violate {upcoming_regulation.get('name')} on {effective_date}",
                    "severity": "MEDIUM",
                    "time_to_compliance": self._calculate_days_until(effective_date)
                })
        
        compliance_rate = compliant_count / len(events) if events else 0.0
        
        # Generate proactive recommendations
        recommendations = self._generate_proactive_recommendations(
            violations, upcoming_regulation, effective_date
        )
        
        report = TemporalComplianceReport(
            report_id=hashlib.sha256(f"prospective{effective_date}".encode()).hexdigest()[:16],
            generated_at=datetime.utcnow().isoformat(),
            time_range=(start_date.isoformat(), end_date.isoformat()),
            direction=TemporalDirection.PROSPECTIVE,
            events_analyzed=len(events),
            compliant_events=compliant_count,
            non_compliant_events=non_compliant_count,
            compliance_rate=compliance_rate,
            violations=violations,
            recommendations=recommendations
        )
        
        logger.info(f"✅ Prospective audit complete - {len(violations)} gaps identified")
        
        return report
    
    def detect_temporal_conflicts(
        self,
        event: ComplianceEvent,
        time_window_days: int = 365
    ) -> List[Dict]:
        """
        Detect conflicts between event and regulations across time.
        
        Args:
            event: Event to analyze
            time_window_days: How far back/forward to check
        
        Returns:
            List of temporal conflicts
        """
        conflicts = []
        
        event_time = datetime.fromisoformat(event.timestamp)
        
        # Check past regulations
        for days_back in range(0, time_window_days, 30):
            check_time = event_time - timedelta(days=days_back)
            snapshot = self._get_regulatory_snapshot(check_time.isoformat())
            
            status = self._validate_against_snapshot(event, snapshot)
            
            if status == ComplianceStatus.NON_COMPLIANT:
                conflicts.append({
                    "type": "RETROACTIVE_CONFLICT",
                    "timestamp": check_time.isoformat(),
                    "frameworks": snapshot.frameworks,
                    "severity": "HIGH"
                })
        
        return conflicts
    
    def _validate_current_compliance(
        self,
        action_type: str,
        jurisdiction: str,
        frameworks: List[str],
        metadata: Dict
    ) -> ComplianceStatus:
        """Validate against current regulations"""
        # Simplified validation logic
        # In production, this would integrate with SovereignGuardrail
        
        if action_type == "Data_Transfer" and "Foreign_Cloud" in str(metadata):
            return ComplianceStatus.NON_COMPLIANT
        
        return ComplianceStatus.COMPLIANT
    
    def _filter_events(
        self,
        start_date: str,
        end_date: str,
        jurisdiction: Optional[str] = None,
        frameworks: Optional[List[str]] = None
    ) -> List[ComplianceEvent]:
        """Filter events by criteria"""
        filtered = []
        
        start = datetime.fromisoformat(start_date)
        end = datetime.fromisoformat(end_date)
        
        for event in self.audit_trail:
            event_time = datetime.fromisoformat(event.timestamp)
            
            if not (start <= event_time <= end):
                continue
            
            if jurisdiction and event.jurisdiction != jurisdiction:
                continue
            
            if frameworks and not any(f in event.frameworks_applicable for f in frameworks):
                continue
            
            filtered.append(event)
        
        return filtered
    
    def _get_regulatory_snapshot(self, timestamp: str) -> RegulatorySnapshot:
        """Get regulatory state at a specific time"""
        # In production, this would query regulatory history database
        # For now, return current snapshot
        
        return RegulatorySnapshot(
            timestamp=timestamp,
            frameworks=["GDPR", "KDPA", "HIPAA"],
            requirements={"data_residency": True, "consent_required": True},
            jurisdiction="GLOBAL",
            version="1.0"
        )
    
    def _validate_against_snapshot(
        self,
        event: ComplianceEvent,
        snapshot: RegulatorySnapshot
    ) -> ComplianceStatus:
        """Validate event against historical regulatory snapshot"""
        # Simplified validation
        if event.compliance_status == ComplianceStatus.COMPLIANT:
            return ComplianceStatus.COMPLIANT
        
        return ComplianceStatus.NON_COMPLIANT
    
    def _validate_against_future_regulation(
        self,
        event: ComplianceEvent,
        regulation: Dict
    ) -> ComplianceStatus:
        """Validate event against upcoming regulation"""
        # Simplified validation
        required_fields = regulation.get("required_fields", [])
        
        for field in required_fields:
            if field not in event.metadata:
                return ComplianceStatus.NON_COMPLIANT
        
        return ComplianceStatus.COMPLIANT
    
    def _calculate_days_until(self, future_date: str) -> int:
        """Calculate days until future date"""
        future = datetime.fromisoformat(future_date)
        now = datetime.utcnow()
        return (future - now).days
    
    def _generate_recommendations(self, violations: List[Dict]) -> List[str]:
        """Generate recommendations from violations"""
        recommendations = []
        
        if violations:
            recommendations.append(
                "Review and remediate historical compliance violations"
            )
            recommendations.append(
                "Implement automated compliance checks for similar actions"
            )
            recommendations.append(
                "Update training materials to prevent future violations"
            )
        
        return recommendations
    
    def _generate_proactive_recommendations(
        self,
        violations: List[Dict],
        regulation: Dict,
        effective_date: str
    ) -> List[str]:
        """Generate proactive recommendations for upcoming regulation"""
        recommendations = []
        
        days_until = self._calculate_days_until(effective_date)
        
        recommendations.append(
            f"Prepare for {regulation.get('name')} - {days_until} days remaining"
        )
        
        if violations:
            recommendations.append(
                f"Update {len(violations)} processes to comply with new requirements"
            )
            recommendations.append(
                "Conduct staff training on new regulatory requirements"
            )
            recommendations.append(
                "Implement automated compliance validation before effective date"
            )
        
        return recommendations
    
    def export_audit_trail(self, output_path: str):
        """Export complete audit trail to JSON"""
        with open(output_path, 'w') as f:
            json.dump(
                [event.to_dict() for event in self.audit_trail],
                f,
                indent=2
            )
        
        logger.info(f"📤 Audit trail exported to {output_path}")


# Example usage
if __name__ == "__main__":
    engine = ChronoAuditEngine()
    
    # Record some events
    event1 = engine.record_event(
        action_type="Data_Transfer",
        actor="ml_system",
        resource="patient_data",
        jurisdiction="KDPA_KE",
        frameworks_applicable=["KDPA", "GDPR"],
        metadata={"destination": "Local_Node", "data_type": "PHI"}
    )
    
    # Retroactive audit
    report = engine.retroactive_audit(
        start_date="2024-01-01T00:00:00",
        end_date="2025-12-31T23:59:59",
        jurisdiction="KDPA_KE"
    )
    
    print(f"✅ Compliance Rate: {report.compliance_rate:.1%}")
    print(f"📊 Events Analyzed: {report.events_analyzed}")
    print(f"⚠️  Violations: {report.non_compliant_events}")
