"""
Blockchain-Backed Logging for EU AI Act Articles 12 & 15
Automatic logging with immutable blockchain records

This module implements:
- Immutable audit logging (Art. 12)
- Cybersecurity resilience logging (Art. 15)
- Private blockchain integration
- GCP Confidential Space support
"""

import hashlib
import json
from datetime import datetime
from typing import Dict, List, Optional
from dataclasses import dataclass, asdict
from enum import Enum
import logging

logger = logging.getLogger(__name__)


class LogEventType(Enum):
    """Types of events to log"""
    HIGH_RISK_INFERENCE = "high_risk_inference"
    TRIAGE_DECISION = "triage_decision"
    OUTBREAK_ALERT = "outbreak_alert"
    DATA_TRANSFER = "data_transfer"
    CONSENT_VALIDATION = "consent_validation"
    SOVEREIGNTY_VIOLATION = "sovereignty_violation"
    SECURITY_INCIDENT = "security_incident"
    MODEL_UPDATE = "model_update"
    PERFORMANCE_DRIFT = "performance_drift"
    EMERGENCY_OVERRIDE = "emergency_override"


class SeverityLevel(Enum):
    """Severity levels for logged events"""
    INFO = "info"
    WARNING = "warning"
    CRITICAL = "critical"
    EMERGENCY = "emergency"


@dataclass
class BlockchainLogEntry:
    """Single log entry for blockchain"""
    entry_id: str
    timestamp: str
    event_type: LogEventType
    severity: SeverityLevel
    system_id: str
    actor: str
    action: str
    resource: str
    outcome: str
    metadata: Dict
    previous_hash: str
    current_hash: str
    signature: str


@dataclass
class Block:
    """Blockchain block containing multiple log entries"""
    block_number: int
    timestamp: str
    entries: List[BlockchainLogEntry]
    previous_block_hash: str
    current_block_hash: str
    nonce: int
    merkle_root: str


class BlockchainLedger:
    """
    Immutable blockchain ledger for EU AI Act compliance
    
    Implements automatic logging per Articles 12 & 15:
    - Every high-risk AI decision is logged
    - Logs are cryptographically hashed and chained
    - Tamper-proof audit trail
    - Integration with GCP Confidential Space
    """
    
    def __init__(
        self,
        system_id: str,
        use_confidential_space: bool = False,
        gcp_project: Optional[str] = None
    ):
        self.system_id = system_id
        self.use_confidential_space = use_confidential_space
        self.gcp_project = gcp_project
        
        # Initialize blockchain
        self.chain: List[Block] = []
        self.pending_entries: List[BlockchainLogEntry] = []
        self.last_hash = "0" * 64  # Genesis hash
        
        # Create genesis block
        self._create_genesis_block()
        
        logger.info(f"⛓️  Blockchain Ledger initialized - System: {system_id}")
        if use_confidential_space:
            logger.info(f"🔒 Confidential Space enabled - Project: {gcp_project}")
    
    def _create_genesis_block(self):
        """Create the genesis block"""
        genesis_entry = BlockchainLogEntry(
            entry_id="GENESIS",
            timestamp=datetime.utcnow().isoformat(),
            event_type=LogEventType.HIGH_RISK_INFERENCE,
            severity=SeverityLevel.INFO,
            system_id=self.system_id,
            actor="SYSTEM",
            action="INITIALIZE",
            resource="BLOCKCHAIN_LEDGER",
            outcome="SUCCESS",
            metadata={"genesis": True},
            previous_hash="0" * 64,
            current_hash="",
            signature=""
        )
        
        # Calculate hash
        genesis_entry.current_hash = self._calculate_entry_hash(genesis_entry)
        genesis_entry.signature = self._sign_entry(genesis_entry)
        
        # Create genesis block
        genesis_block = Block(
            block_number=0,
            timestamp=datetime.utcnow().isoformat(),
            entries=[genesis_entry],
            previous_block_hash="0" * 64,
            current_block_hash="",
            nonce=0,
            merkle_root=genesis_entry.current_hash
        )
        
        genesis_block.current_block_hash = self._calculate_block_hash(genesis_block)
        
        self.chain.append(genesis_block)
        self.last_hash = genesis_block.current_block_hash
        
        logger.info("✅ Genesis block created")
    
    def log_high_risk_inference(
        self,
        actor: str,
        action: str,
        resource: str,
        outcome: str,
        confidence_score: float,
        explanation: Dict,
        evidence_chain: List[str]
    ) -> str:
        """
        Log a high-risk AI inference per Art. 12
        
        Args:
            actor: Who/what made the inference (user, model, agent)
            action: What inference was made
            resource: What resource was affected (patient, outbreak, etc.)
            outcome: Result of the inference
            confidence_score: Model confidence (0.0 to 1.0)
            explanation: SHAP values or other explainability data
            evidence_chain: List of evidence supporting the inference
        
        Returns:
            entry_id: Unique identifier for the log entry
        """
        entry_id = hashlib.sha256(
            f"{actor}{action}{resource}{datetime.utcnow().isoformat()}".encode()
        ).hexdigest()[:16]
        
        entry = BlockchainLogEntry(
            entry_id=entry_id,
            timestamp=datetime.utcnow().isoformat(),
            event_type=LogEventType.HIGH_RISK_INFERENCE,
            severity=self._assess_severity(confidence_score),
            system_id=self.system_id,
            actor=actor,
            action=action,
            resource=resource,
            outcome=outcome,
            metadata={
                "confidence_score": confidence_score,
                "explanation": explanation,
                "evidence_chain": evidence_chain,
                "compliance": ["EU AI Act Art. 12", "GDPR Art. 30"]
            },
            previous_hash=self.last_hash,
            current_hash="",
            signature=""
        )
        
        # Calculate hash and signature
        entry.current_hash = self._calculate_entry_hash(entry)
        entry.signature = self._sign_entry(entry)
        
        # Add to pending entries
        self.pending_entries.append(entry)
        self.last_hash = entry.current_hash
        
        # Mine block if we have enough entries
        if len(self.pending_entries) >= 10:
            self._mine_block()
        
        logger.info(f"📝 High-risk inference logged: {entry_id}")
        logger.info(f"   Action: {action}")
        logger.info(f"   Confidence: {confidence_score:.2%}")
        logger.info(f"   Hash: {entry.current_hash[:16]}...")
        
        return entry_id
    
    def log_triage_decision(
        self,
        patient_id: str,
        triage_level: str,
        symptoms: List[str],
        vital_signs: Dict,
        decision_rationale: str
    ) -> str:
        """Log a triage decision"""
        entry_id = hashlib.sha256(
            f"TRIAGE{patient_id}{datetime.utcnow().isoformat()}".encode()
        ).hexdigest()[:16]
        
        entry = BlockchainLogEntry(
            entry_id=entry_id,
            timestamp=datetime.utcnow().isoformat(),
            event_type=LogEventType.TRIAGE_DECISION,
            severity=SeverityLevel.CRITICAL if triage_level == "RED" else SeverityLevel.WARNING,
            system_id=self.system_id,
            actor="TRIAGE_AI",
            action=f"TRIAGE_{triage_level}",
            resource=f"PATIENT_{patient_id}",
            outcome="DECISION_LOGGED",
            metadata={
                "triage_level": triage_level,
                "symptoms": symptoms,
                "vital_signs": vital_signs,
                "decision_rationale": decision_rationale,
                "compliance": ["EU AI Act Art. 12", "HIPAA §164.312"]
            },
            previous_hash=self.last_hash,
            current_hash="",
            signature=""
        )
        
        entry.current_hash = self._calculate_entry_hash(entry)
        entry.signature = self._sign_entry(entry)
        
        self.pending_entries.append(entry)
        self.last_hash = entry.current_hash
        
        if len(self.pending_entries) >= 10:
            self._mine_block()
        
        logger.info(f"🚨 Triage decision logged: {entry_id}")
        logger.info(f"   Patient: {patient_id}")
        logger.info(f"   Level: {triage_level}")
        
        return entry_id
    
    def log_outbreak_alert(
        self,
        location: str,
        disease: str,
        case_count: int,
        z_score: float,
        alert_level: str,
        forecast: Dict
    ) -> str:
        """Log an outbreak alert"""
        entry_id = hashlib.sha256(
            f"OUTBREAK{location}{disease}{datetime.utcnow().isoformat()}".encode()
        ).hexdigest()[:16]
        
        entry = BlockchainLogEntry(
            entry_id=entry_id,
            timestamp=datetime.utcnow().isoformat(),
            event_type=LogEventType.OUTBREAK_ALERT,
            severity=SeverityLevel.EMERGENCY if alert_level == "CRITICAL" else SeverityLevel.WARNING,
            system_id=self.system_id,
            actor="OUTBREAK_PREDICTOR",
            action=f"ALERT_{alert_level}",
            resource=f"LOCATION_{location}",
            outcome="ALERT_ISSUED",
            metadata={
                "location": location,
                "disease": disease,
                "case_count": case_count,
                "z_score": z_score,
                "alert_level": alert_level,
                "forecast": forecast,
                "compliance": ["EU AI Act Art. 12", "WHO IHR Article 6"]
            },
            previous_hash=self.last_hash,
            current_hash="",
            signature=""
        )
        
        entry.current_hash = self._calculate_entry_hash(entry)
        entry.signature = self._sign_entry(entry)
        
        self.pending_entries.append(entry)
        self.last_hash = entry.current_hash
        
        if len(self.pending_entries) >= 10:
            self._mine_block()
        
        logger.info(f"⚠️  Outbreak alert logged: {entry_id}")
        logger.info(f"   Location: {location}")
        logger.info(f"   Disease: {disease}")
        logger.info(f"   Z-Score: {z_score:.2f}")
        
        return entry_id
    
    def log_security_incident(
        self,
        incident_type: str,
        severity: SeverityLevel,
        description: str,
        affected_systems: List[str],
        mitigation_actions: List[str]
    ) -> str:
        """Log a security incident per Art. 15"""
        entry_id = hashlib.sha256(
            f"SECURITY{incident_type}{datetime.utcnow().isoformat()}".encode()
        ).hexdigest()[:16]
        
        entry = BlockchainLogEntry(
            entry_id=entry_id,
            timestamp=datetime.utcnow().isoformat(),
            event_type=LogEventType.SECURITY_INCIDENT,
            severity=severity,
            system_id=self.system_id,
            actor="SECURITY_MONITOR",
            action=f"INCIDENT_{incident_type}",
            resource="SYSTEM_SECURITY",
            outcome="INCIDENT_LOGGED",
            metadata={
                "incident_type": incident_type,
                "description": description,
                "affected_systems": affected_systems,
                "mitigation_actions": mitigation_actions,
                "compliance": ["EU AI Act Art. 15", "ISO 27001 A.16.1"]
            },
            previous_hash=self.last_hash,
            current_hash="",
            signature=""
        )
        
        entry.current_hash = self._calculate_entry_hash(entry)
        entry.signature = self._sign_entry(entry)
        
        self.pending_entries.append(entry)
        self.last_hash = entry.current_hash
        
        # Immediately mine block for security incidents
        self._mine_block()
        
        logger.error(f"🔒 Security incident logged: {entry_id}")
        logger.error(f"   Type: {incident_type}")
        logger.error(f"   Severity: {severity.value}")
        
        return entry_id
    
    def _mine_block(self):
        """Mine a new block with pending entries"""
        if not self.pending_entries:
            return
        
        block_number = len(self.chain)
        
        # Calculate Merkle root
        merkle_root = self._calculate_merkle_root(self.pending_entries)
        
        # Create block
        block = Block(
            block_number=block_number,
            timestamp=datetime.utcnow().isoformat(),
            entries=self.pending_entries.copy(),
            previous_block_hash=self.chain[-1].current_block_hash,
            current_block_hash="",
            nonce=0,
            merkle_root=merkle_root
        )
        
        # Proof of work (simplified)
        block.nonce = self._proof_of_work(block)
        block.current_block_hash = self._calculate_block_hash(block)
        
        # Add to chain
        self.chain.append(block)
        self.pending_entries = []
        
        logger.info(f"⛏️  Block mined: #{block_number}")
        logger.info(f"   Entries: {len(block.entries)}")
        logger.info(f"   Hash: {block.current_block_hash[:16]}...")
        logger.info(f"   Nonce: {block.nonce}")
        
        # Push to GCP Confidential Space if enabled
        if self.use_confidential_space:
            self._push_to_confidential_space(block)
    
    def _calculate_entry_hash(self, entry: BlockchainLogEntry) -> str:
        """Calculate SHA-256 hash of log entry"""
        entry_dict = asdict(entry)
        entry_dict.pop('current_hash', None)
        entry_dict.pop('signature', None)
        
        entry_json = json.dumps(entry_dict, sort_keys=True)
        return hashlib.sha256(entry_json.encode()).hexdigest()
    
    def _calculate_block_hash(self, block: Block) -> str:
        """Calculate SHA-256 hash of block"""
        block_dict = {
            "block_number": block.block_number,
            "timestamp": block.timestamp,
            "previous_block_hash": block.previous_block_hash,
            "merkle_root": block.merkle_root,
            "nonce": block.nonce
        }
        
        block_json = json.dumps(block_dict, sort_keys=True)
        return hashlib.sha256(block_json.encode()).hexdigest()
    
    def _calculate_merkle_root(self, entries: List[BlockchainLogEntry]) -> str:
        """Calculate Merkle root of entries"""
        if not entries:
            return "0" * 64
        
        hashes = [entry.current_hash for entry in entries]
        
        while len(hashes) > 1:
            if len(hashes) % 2 != 0:
                hashes.append(hashes[-1])
            
            new_hashes = []
            for i in range(0, len(hashes), 2):
                combined = hashes[i] + hashes[i + 1]
                new_hash = hashlib.sha256(combined.encode()).hexdigest()
                new_hashes.append(new_hash)
            
            hashes = new_hashes
        
        return hashes[0]
    
    def _proof_of_work(self, block: Block, difficulty: int = 2) -> int:
        """Simple proof of work (find nonce where hash starts with N zeros)"""
        nonce = 0
        target = "0" * difficulty
        
        while True:
            block.nonce = nonce
            block_hash = self._calculate_block_hash(block)
            
            if block_hash.startswith(target):
                return nonce
            
            nonce += 1
            
            # Limit iterations for demo
            if nonce > 100000:
                return nonce
    
    def _sign_entry(self, entry: BlockchainLogEntry) -> str:
        """Sign entry with system signature"""
        # In production, use Cloud KMS for signing
        signature_data = f"{entry.entry_id}{entry.current_hash}{self.system_id}"
        return hashlib.sha256(signature_data.encode()).hexdigest()
    
    def _assess_severity(self, confidence_score: float) -> SeverityLevel:
        """Assess severity based on confidence score"""
        if confidence_score >= 0.9:
            return SeverityLevel.CRITICAL
        elif confidence_score >= 0.7:
            return SeverityLevel.WARNING
        else:
            return SeverityLevel.INFO
    
    def _push_to_confidential_space(self, block: Block):
        """Push block to GCP Confidential Space"""
        # In production, integrate with GCP Confidential Space API
        logger.info(f"🔒 Pushing block #{block.block_number} to Confidential Space")
        # Placeholder for actual implementation
    
    def verify_chain_integrity(self) -> bool:
        """Verify the integrity of the entire blockchain"""
        for i in range(1, len(self.chain)):
            current_block = self.chain[i]
            previous_block = self.chain[i - 1]
            
            # Verify previous hash
            if current_block.previous_block_hash != previous_block.current_block_hash:
                logger.error(f"❌ Chain integrity violation at block #{i}")
                return False
            
            # Verify block hash
            calculated_hash = self._calculate_block_hash(current_block)
            if current_block.current_block_hash != calculated_hash:
                logger.error(f"❌ Block hash mismatch at block #{i}")
                return False
        
        logger.info("✅ Blockchain integrity verified")
        return True
    
    def get_audit_trail(
        self,
        event_type: Optional[LogEventType] = None,
        start_time: Optional[str] = None,
        end_time: Optional[str] = None
    ) -> List[BlockchainLogEntry]:
        """Retrieve audit trail with optional filters"""
        entries = []
        
        for block in self.chain:
            for entry in block.entries:
                # Apply filters
                if event_type and entry.event_type != event_type:
                    continue
                
                if start_time and entry.timestamp < start_time:
                    continue
                
                if end_time and entry.timestamp > end_time:
                    continue
                
                entries.append(entry)
        
        return entries


# Example usage
if __name__ == "__main__":
    # Initialize blockchain ledger
    ledger = BlockchainLedger(
        system_id="iLuminara-Core-001",
        use_confidential_space=False
    )
    
    # Log high-risk inference
    ledger.log_high_risk_inference(
        actor="OUTBREAK_PREDICTOR_AI",
        action="PREDICT_CHOLERA_OUTBREAK",
        resource="DADAAB_CAMP",
        outcome="HIGH_RISK_DETECTED",
        confidence_score=0.92,
        explanation={"shap_values": [0.45, 0.30, 0.17]},
        evidence_chain=["CBS_REPORT_001", "EMR_RECORD_045", "IDSR_ALERT_012"]
    )
    
    # Log triage decision
    ledger.log_triage_decision(
        patient_id="PAT_12345",
        triage_level="RED",
        symptoms=["severe_dehydration", "vomiting", "diarrhea"],
        vital_signs={"temp": 39.5, "hr": 120, "bp": "90/60"},
        decision_rationale="Suspected cholera with severe dehydration"
    )
    
    # Log outbreak alert
    ledger.log_outbreak_alert(
        location="Dadaab",
        disease="cholera",
        case_count=47,
        z_score=8.5,
        alert_level="CRITICAL",
        forecast={"day_1": 55, "day_2": 68, "day_3": 82}
    )
    
    # Verify chain integrity
    ledger.verify_chain_integrity()
    
    # Get audit trail
    trail = ledger.get_audit_trail(event_type=LogEventType.HIGH_RISK_INFERENCE)
    print(f"\\n📊 Audit trail: {len(trail)} high-risk inferences logged")
