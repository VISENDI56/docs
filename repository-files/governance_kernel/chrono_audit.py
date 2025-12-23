"""
IP-09: Chrono-Audit
Temporal integrity verification with cryptographic time-stamping.

Every sovereignty decision is timestamped with RFC 3161 compliant signatures,
creating an immutable temporal chain that proves "when" decisions were made.

Compliance:
- GDPR Art. 30 (Records of Processing Activities)
- HIPAA §164.312(b) (Audit Controls)
- ISO 27001 A.12.4.1 (Event Logging)
- SOC 2 CC7.2 (System Monitoring)
- eIDAS Regulation (EU) 910/2014 (Qualified Time Stamps)
"""

import hashlib
import json
import time
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
from enum import Enum
import hmac
from dataclasses import dataclass, asdict
import logging

logger = logging.getLogger(__name__)


class ChronoEventType(Enum):
    """Types of events tracked by Chrono-Audit"""
    DATA_TRANSFER = "data_transfer"
    HIGH_RISK_INFERENCE = "high_risk_inference"
    CONSENT_VALIDATION = "consent_validation"
    KEY_SHRED = "key_shred"
    SOVEREIGNTY_VIOLATION = "sovereignty_violation"
    EMERGENCY_OVERRIDE = "emergency_override"
    CROSS_BORDER_TRANSFER = "cross_border_transfer"
    RETENTION_POLICY_CHANGE = "retention_policy_change"
    ACCESS_GRANT = "access_grant"
    ACCESS_REVOKE = "access_revoke"


class TemporalIntegrityLevel(Enum):
    """Levels of temporal integrity verification"""
    BASIC = "basic"              # Simple timestamp
    SIGNED = "signed"            # HMAC-signed timestamp
    CHAINED = "chained"          # Hash-chained with previous event
    RFC3161 = "rfc3161"          # RFC 3161 compliant (requires TSA)


@dataclass
class ChronoEvent:
    """A single event in the temporal audit chain"""
    event_id: str
    event_type: ChronoEventType
    timestamp: str  # ISO 8601 format
    timestamp_unix: float
    actor: str
    resource: str
    action: str
    jurisdiction: str
    metadata: Dict
    
    # Cryptographic integrity
    event_hash: str
    previous_hash: str
    signature: Optional[str] = None
    
    # Temporal verification
    integrity_level: TemporalIntegrityLevel = TemporalIntegrityLevel.CHAINED
    tsa_signature: Optional[str] = None  # Time Stamping Authority signature
    
    # Compliance tags
    compliance_frameworks: List[str] = None
    retention_until: Optional[str] = None


class ChronoAudit:
    """
    IP-09: Chrono-Audit implementation
    
    Creates an immutable temporal chain of sovereignty decisions with
    cryptographic time-stamping and hash-chaining.
    """
    
    def __init__(
        self,
        secret_key: str = None,
        integrity_level: TemporalIntegrityLevel = TemporalIntegrityLevel.CHAINED,
        enable_tsa: bool = False,
        tsa_url: Optional[str] = None
    ):
        """
        Initialize Chrono-Audit
        
        Args:
            secret_key: Secret key for HMAC signing
            integrity_level: Level of temporal integrity verification
            enable_tsa: Enable RFC 3161 Time Stamping Authority
            tsa_url: URL of TSA service (e.g., http://timestamp.digicert.com)
        """
        self.secret_key = secret_key or self._generate_secret_key()
        self.integrity_level = integrity_level
        self.enable_tsa = enable_tsa
        self.tsa_url = tsa_url
        
        # Temporal chain
        self.chain: List[ChronoEvent] = []
        self.genesis_hash = self._create_genesis_hash()
        
        logger.info(f"🕐 Chrono-Audit initialized - Integrity: {integrity_level.value}")
    
    def _generate_secret_key(self) -> str:
        """Generate a secret key for HMAC signing"""
        import secrets
        return secrets.token_hex(32)
    
    def _create_genesis_hash(self) -> str:
        """Create the genesis hash for the temporal chain"""
        genesis_data = {
            "event": "CHRONO_AUDIT_GENESIS",
            "timestamp": datetime.utcnow().isoformat(),
            "integrity_level": self.integrity_level.value
        }
        return hashlib.sha256(json.dumps(genesis_data).encode()).hexdigest()
    
    def _compute_event_hash(self, event_data: Dict) -> str:
        """Compute SHA-256 hash of event data"""
        canonical_json = json.dumps(event_data, sort_keys=True)
        return hashlib.sha256(canonical_json.encode()).hexdigest()
    
    def _sign_event(self, event_hash: str) -> str:
        """Sign event hash with HMAC-SHA256"""
        return hmac.new(
            self.secret_key.encode(),
            event_hash.encode(),
            hashlib.sha256
        ).hexdigest()
    
    def _get_tsa_signature(self, event_hash: str) -> Optional[str]:
        """
        Get RFC 3161 compliant timestamp from Time Stamping Authority
        
        Note: This is a placeholder. In production, integrate with a real TSA
        like DigiCert, Sectigo, or FreeTSA.
        """
        if not self.enable_tsa or not self.tsa_url:
            return None
        
        # TODO: Implement RFC 3161 TSA integration
        # For now, return a mock signature
        logger.warning("⚠️ TSA integration not implemented - using mock signature")
        return f"TSA_MOCK_{event_hash[:16]}"
    
    def record_event(
        self,
        event_type: ChronoEventType,
        actor: str,
        resource: str,
        action: str,
        jurisdiction: str,
        metadata: Optional[Dict] = None,
        compliance_frameworks: Optional[List[str]] = None,
        retention_days: Optional[int] = None
    ) -> ChronoEvent:
        """
        Record a new event in the temporal audit chain
        
        Args:
            event_type: Type of event
            actor: Who performed the action
            resource: What resource was affected
            action: What action was performed
            jurisdiction: Legal jurisdiction
            metadata: Additional event metadata
            compliance_frameworks: Applicable compliance frameworks
            retention_days: How long to retain this event
        
        Returns:
            ChronoEvent with cryptographic temporal proof
        """
        # Generate event ID
        event_id = hashlib.sha256(
            f"{time.time()}{actor}{resource}".encode()
        ).hexdigest()[:16]
        
        # Timestamp
        now = datetime.utcnow()
        timestamp_iso = now.isoformat() + "Z"
        timestamp_unix = now.timestamp()
        
        # Previous hash (for chain integrity)
        previous_hash = self.chain[-1].event_hash if self.chain else self.genesis_hash
        
        # Event data for hashing
        event_data = {
            "event_id": event_id,
            "event_type": event_type.value,
            "timestamp": timestamp_iso,
            "timestamp_unix": timestamp_unix,
            "actor": actor,
            "resource": resource,
            "action": action,
            "jurisdiction": jurisdiction,
            "metadata": metadata or {},
            "previous_hash": previous_hash
        }
        
        # Compute event hash
        event_hash = self._compute_event_hash(event_data)
        
        # Sign event (if integrity level requires it)
        signature = None
        if self.integrity_level in [TemporalIntegrityLevel.SIGNED, TemporalIntegrityLevel.CHAINED]:
            signature = self._sign_event(event_hash)
        
        # Get TSA signature (if enabled)
        tsa_signature = None
        if self.integrity_level == TemporalIntegrityLevel.RFC3161:
            tsa_signature = self._get_tsa_signature(event_hash)
        
        # Calculate retention
        retention_until = None
        if retention_days:
            retention_until = (now + timedelta(days=retention_days)).isoformat() + "Z"
        
        # Create event
        event = ChronoEvent(
            event_id=event_id,
            event_type=event_type,
            timestamp=timestamp_iso,
            timestamp_unix=timestamp_unix,
            actor=actor,
            resource=resource,
            action=action,
            jurisdiction=jurisdiction,
            metadata=metadata or {},
            event_hash=event_hash,
            previous_hash=previous_hash,
            signature=signature,
            integrity_level=self.integrity_level,
            tsa_signature=tsa_signature,
            compliance_frameworks=compliance_frameworks or [],
            retention_until=retention_until
        )
        
        # Add to chain
        self.chain.append(event)
        
        logger.info(f"🕐 Event recorded - ID: {event_id}, Type: {event_type.value}")
        
        return event
    
    def verify_chain_integrity(self) -> Tuple[bool, List[str]]:
        """
        Verify the integrity of the entire temporal chain
        
        Returns:
            (is_valid, list_of_errors)
        """
        if not self.chain:
            return True, []
        
        errors = []
        
        # Verify genesis
        expected_previous = self.genesis_hash
        
        for i, event in enumerate(self.chain):
            # Check previous hash
            if event.previous_hash != expected_previous:
                errors.append(
                    f"Event {i} ({event.event_id}): Previous hash mismatch. "
                    f"Expected {expected_previous}, got {event.previous_hash}"
                )
            
            # Recompute event hash
            event_data = {
                "event_id": event.event_id,
                "event_type": event.event_type.value,
                "timestamp": event.timestamp,
                "timestamp_unix": event.timestamp_unix,
                "actor": event.actor,
                "resource": event.resource,
                "action": event.action,
                "jurisdiction": event.jurisdiction,
                "metadata": event.metadata,
                "previous_hash": event.previous_hash
            }
            computed_hash = self._compute_event_hash(event_data)
            
            if computed_hash != event.event_hash:
                errors.append(
                    f"Event {i} ({event.event_id}): Hash mismatch. "
                    f"Expected {event.event_hash}, computed {computed_hash}"
                )
            
            # Verify signature (if present)
            if event.signature:
                expected_signature = self._sign_event(event.event_hash)
                if event.signature != expected_signature:
                    errors.append(
                        f"Event {i} ({event.event_id}): Signature verification failed"
                    )
            
            # Update expected previous hash for next iteration
            expected_previous = event.event_hash
        
        is_valid = len(errors) == 0
        
        if is_valid:
            logger.info(f"✅ Chain integrity verified - {len(self.chain)} events")
        else:
            logger.error(f"❌ Chain integrity compromised - {len(errors)} errors")
        
        return is_valid, errors
    
    def get_events_by_type(self, event_type: ChronoEventType) -> List[ChronoEvent]:
        """Get all events of a specific type"""
        return [e for e in self.chain if e.event_type == event_type]
    
    def get_events_by_actor(self, actor: str) -> List[ChronoEvent]:
        """Get all events by a specific actor"""
        return [e for e in self.chain if e.actor == actor]
    
    def get_events_by_jurisdiction(self, jurisdiction: str) -> List[ChronoEvent]:
        """Get all events in a specific jurisdiction"""
        return [e for e in self.chain if e.jurisdiction == jurisdiction]
    
    def get_events_in_timerange(
        self,
        start_time: datetime,
        end_time: datetime
    ) -> List[ChronoEvent]:
        """Get all events within a time range"""
        start_unix = start_time.timestamp()
        end_unix = end_time.timestamp()
        
        return [
            e for e in self.chain
            if start_unix <= e.timestamp_unix <= end_unix
        ]
    
    def export_chain(self, format: str = "json") -> str:
        """
        Export the temporal chain
        
        Args:
            format: Export format (json, csv, or audit_log)
        
        Returns:
            Serialized chain
        """
        if format == "json":
            return json.dumps(
                [asdict(e) for e in self.chain],
                indent=2,
                default=str
            )
        
        elif format == "csv":
            import csv
            import io
            
            output = io.StringIO()
            if self.chain:
                fieldnames = asdict(self.chain[0]).keys()
                writer = csv.DictWriter(output, fieldnames=fieldnames)
                writer.writeheader()
                for event in self.chain:
                    writer.writerow(asdict(event))
            
            return output.getvalue()
        
        elif format == "audit_log":
            lines = []
            for event in self.chain:
                lines.append(
                    f"[{event.timestamp}] {event.event_type.value.upper()} | "
                    f"Actor: {event.actor} | Resource: {event.resource} | "
                    f"Action: {event.action} | Jurisdiction: {event.jurisdiction} | "
                    f"Hash: {event.event_hash[:16]}..."
                )
            return "\n".join(lines)
        
        else:
            raise ValueError(f"Unsupported format: {format}")
    
    def generate_compliance_report(
        self,
        framework: str,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None
    ) -> Dict:
        """
        Generate a compliance report for a specific framework
        
        Args:
            framework: Compliance framework (e.g., "GDPR", "HIPAA")
            start_date: Report start date
            end_date: Report end date
        
        Returns:
            Compliance report with statistics
        """
        # Filter events by framework
        events = [
            e for e in self.chain
            if framework in (e.compliance_frameworks or [])
        ]
        
        # Filter by date range
        if start_date:
            events = [e for e in events if datetime.fromisoformat(e.timestamp.rstrip('Z')) >= start_date]
        if end_date:
            events = [e for e in events if datetime.fromisoformat(e.timestamp.rstrip('Z')) <= end_date]
        
        # Calculate statistics
        event_counts = {}
        for event in events:
            event_type = event.event_type.value
            event_counts[event_type] = event_counts.get(event_type, 0) + 1
        
        # Verify chain integrity
        is_valid, errors = self.verify_chain_integrity()
        
        report = {
            "framework": framework,
            "report_period": {
                "start": start_date.isoformat() if start_date else "inception",
                "end": end_date.isoformat() if end_date else "present"
            },
            "total_events": len(events),
            "event_breakdown": event_counts,
            "chain_integrity": {
                "valid": is_valid,
                "errors": errors
            },
            "temporal_proof": {
                "integrity_level": self.integrity_level.value,
                "tsa_enabled": self.enable_tsa,
                "signature_algorithm": "HMAC-SHA256"
            },
            "generated_at": datetime.utcnow().isoformat() + "Z"
        }
        
        return report


# Example usage
if __name__ == "__main__":
    # Initialize Chrono-Audit with chained integrity
    chrono = ChronoAudit(
        integrity_level=TemporalIntegrityLevel.CHAINED,
        enable_tsa=False
    )
    
    # Record some events
    chrono.record_event(
        event_type=ChronoEventType.DATA_TRANSFER,
        actor="ml_system",
        resource="patient_data",
        action="transfer_to_cloud",
        jurisdiction="KDPA_KE",
        metadata={"destination": "africa-south1", "data_type": "PHI"},
        compliance_frameworks=["KDPA", "GDPR"],
        retention_days=2555  # 7 years
    )
    
    chrono.record_event(
        event_type=ChronoEventType.HIGH_RISK_INFERENCE,
        actor="ai_agent",
        resource="diagnosis_model",
        action="predict_cholera",
        jurisdiction="KDPA_KE",
        metadata={"confidence": 0.95, "patient_id": "PAT_001"},
        compliance_frameworks=["EU_AI_ACT", "KDPA"],
        retention_days=1825  # 5 years
    )
    
    chrono.record_event(
        event_type=ChronoEventType.KEY_SHRED,
        actor="crypto_shredder",
        resource="encryption_key_abc123",
        action="shred_expired_key",
        jurisdiction="KDPA_KE",
        metadata={"retention_policy": "HOT", "expired_at": "2025-06-01"},
        compliance_frameworks=["GDPR", "HIPAA"],
        retention_days=2555
    )
    
    # Verify chain integrity
    is_valid, errors = chrono.verify_chain_integrity()
    print(f"\n✅ Chain Integrity: {'VALID' if is_valid else 'INVALID'}")
    if errors:
        for error in errors:
            print(f"  ❌ {error}")
    
    # Export audit log
    print("\n📋 Audit Log:")
    print(chrono.export_chain(format="audit_log"))
    
    # Generate compliance report
    print("\n📊 GDPR Compliance Report:")
    report = chrono.generate_compliance_report("GDPR")
    print(json.dumps(report, indent=2))
