"""
IP-02: Crypto Shredder
Data is not deleted; it is cryptographically dissolved.

Compliance:
- GDPR Art. 17 (Right to Erasure)
- HIPAA §164.530(j) (Standard: Documentation)
- NIST SP 800-88 (Guidelines for Media Sanitization)
- ISO 27001 A.8.3.2 (Disposal of Media)
"""

import os
import hashlib
import secrets
from datetime import datetime, timedelta
from typing import Dict, Optional, Tuple
from enum import Enum
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import json
import logging

logger = logging.getLogger(__name__)


class RetentionPolicy(Enum):
    """Data retention policies aligned with global frameworks"""
    HOT = 180  # 6 months - Active operational data
    WARM = 365  # 1 year - Compliance minimum (HIPAA)
    COLD = 1825  # 5 years - Legal hold maximum (GDPR Art. 17)
    ETERNAL = -1  # Never expires (requires explicit justification)


class SovereigntyZone(Enum):
    """Geographic sovereignty zones for data residency"""
    EU = "eu-west1"  # GDPR jurisdiction
    KENYA = "africa-south1"  # KDPA jurisdiction
    SOUTH_AFRICA = "africa-south1"  # POPIA jurisdiction
    CANADA = "northamerica-northeast1"  # PIPEDA jurisdiction
    USA = "us-central1"  # HIPAA jurisdiction


class CryptoShredder:
    """
    Implements IP-02: Cryptographic data dissolution.
    
    Instead of deleting data, we:
    1. Encrypt with ephemeral key
    2. Store encrypted data
    3. Shred the key after retention period
    4. Data becomes cryptographically irrecoverable
    """
    
    def __init__(
        self,
        key_storage_path: str = "./keys",
        sovereignty_zone: SovereigntyZone = SovereigntyZone.KENYA,
        enable_audit: bool = True
    ):
        self.key_storage_path = key_storage_path
        self.sovereignty_zone = sovereignty_zone
        self.enable_audit = enable_audit
        
        # Create key storage directory
        os.makedirs(key_storage_path, exist_ok=True)
        
        # Audit trail
        self.audit_log = []
        
        logger.info(f"🔐 Crypto Shredder initialized - Zone: {sovereignty_zone.value}")
    
    def encrypt_with_ephemeral_key(
        self,
        data: bytes,
        retention_policy: RetentionPolicy = RetentionPolicy.HOT,
        metadata: Optional[Dict] = None
    ) -> Tuple[bytes, str]:
        """
        Encrypt data with an ephemeral key that will be shredded after retention period.
        
        Args:
            data: Raw data to encrypt
            retention_policy: How long to retain the key
            metadata: Additional metadata (patient_id, jurisdiction, etc.)
        
        Returns:
            (encrypted_data, key_id)
        """
        # Generate ephemeral key
        key = secrets.token_bytes(32)  # 256-bit key
        key_id = hashlib.sha256(key).hexdigest()[:16]
        
        # Generate IV
        iv = secrets.token_bytes(16)
        
        # Encrypt data using AES-256-GCM
        cipher = Cipher(
            algorithms.AES(key),
            modes.GCM(iv),
            backend=default_backend()
        )
        encryptor = cipher.encryptor()
        encrypted_data = encryptor.update(data) + encryptor.finalize()
        
        # Calculate expiration
        if retention_policy == RetentionPolicy.ETERNAL:
            expiration = None
        else:
            expiration = datetime.utcnow() + timedelta(days=retention_policy.value)
        
        # Store key with metadata
        key_metadata = {
            "key_id": key_id,
            "key": key.hex(),
            "iv": iv.hex(),
            "tag": encryptor.tag.hex(),
            "created_at": datetime.utcnow().isoformat(),
            "expires_at": expiration.isoformat() if expiration else None,
            "retention_policy": retention_policy.name,
            "sovereignty_zone": self.sovereignty_zone.value,
            "metadata": metadata or {},
            "shredded": False
        }
        
        # Save key to disk
        key_path = os.path.join(self.key_storage_path, f"{key_id}.json")
        with open(key_path, 'w') as f:
            json.dump(key_metadata, f, indent=2)
        
        # Audit log
        if self.enable_audit:
            self._log_audit("ENCRYPT", key_id, metadata)
        
        logger.info(f"✅ Data encrypted - Key ID: {key_id}, Expires: {expiration}")
        
        # Return encrypted data with IV and tag prepended
        return iv + encryptor.tag + encrypted_data, key_id
    
    def decrypt_with_key(self, encrypted_data: bytes, key_id: str) -> Optional[bytes]:
        """
        Decrypt data using stored key (if not shredded).
        
        Args:
            encrypted_data: Encrypted data (IV + tag + ciphertext)
            key_id: Key identifier
        
        Returns:
            Decrypted data or None if key is shredded
        """
        # Load key metadata
        key_path = os.path.join(self.key_storage_path, f"{key_id}.json")
        
        if not os.path.exists(key_path):
            logger.error(f"❌ Key not found: {key_id}")
            return None
        
        with open(key_path, 'r') as f:
            key_metadata = json.load(f)
        
        # Check if key is shredded
        if key_metadata["shredded"]:
            logger.warning(f"🔥 Key shredded - Data irrecoverable: {key_id}")
            if self.enable_audit:
                self._log_audit("DECRYPT_FAILED_SHREDDED", key_id, None)
            return None
        
        # Check expiration
        if key_metadata["expires_at"]:
            expiration = datetime.fromisoformat(key_metadata["expires_at"])
            if datetime.utcnow() > expiration:
                logger.warning(f"⏰ Key expired - Auto-shredding: {key_id}")
                self.shred_key(key_id)
                return None
        
        # Extract IV, tag, and ciphertext
        iv = bytes.fromhex(key_metadata["iv"])
        tag = bytes.fromhex(key_metadata["tag"])
        key = bytes.fromhex(key_metadata["key"])
        
        # Decrypt
        cipher = Cipher(
            algorithms.AES(key),
            modes.GCM(iv, tag),
            backend=default_backend()
        )
        decryptor = cipher.decryptor()
        
        try:
            # Skip IV and tag in encrypted_data
            ciphertext = encrypted_data[32:]  # 16 bytes IV + 16 bytes tag
            decrypted_data = decryptor.update(ciphertext) + decryptor.finalize()
            
            if self.enable_audit:
                self._log_audit("DECRYPT", key_id, key_metadata["metadata"])
            
            logger.info(f"✅ Data decrypted - Key ID: {key_id}")
            return decrypted_data
        
        except Exception as e:
            logger.error(f"❌ Decryption failed: {e}")
            return None
    
    def shred_key(self, key_id: str) -> bool:
        """
        Cryptographically shred a key, making data irrecoverable.
        
        This is the core of IP-02: Data is not deleted, it is dissolved.
        
        Args:
            key_id: Key identifier to shred
        
        Returns:
            True if shredded successfully
        """
        key_path = os.path.join(self.key_storage_path, f"{key_id}.json")
        
        if not os.path.exists(key_path):
            logger.error(f"❌ Key not found: {key_id}")
            return False
        
        # Load metadata
        with open(key_path, 'r') as f:
            key_metadata = json.load(f)
        
        # Overwrite key with random data (DoD 5220.22-M standard)
        key_metadata["key"] = secrets.token_hex(32)  # Overwrite with random
        key_metadata["iv"] = secrets.token_hex(16)
        key_metadata["tag"] = secrets.token_hex(16)
        key_metadata["shredded"] = True
        key_metadata["shredded_at"] = datetime.utcnow().isoformat()
        
        # Save shredded metadata
        with open(key_path, 'w') as f:
            json.dump(key_metadata, f, indent=2)
        
        # Audit log
        if self.enable_audit:
            self._log_audit("SHRED", key_id, key_metadata["metadata"])
        
        logger.info(f"🔥 Key shredded - Data irrecoverable: {key_id}")
        return True
    
    def auto_shred_expired_keys(self) -> int:
        """
        Automatically shred all expired keys.
        
        Returns:
            Number of keys shredded
        """
        shredded_count = 0
        
        for filename in os.listdir(self.key_storage_path):
            if not filename.endswith('.json'):
                continue
            
            key_path = os.path.join(self.key_storage_path, filename)
            
            with open(key_path, 'r') as f:
                key_metadata = json.load(f)
            
            # Skip already shredded keys
            if key_metadata["shredded"]:
                continue
            
            # Check expiration
            if key_metadata["expires_at"]:
                expiration = datetime.fromisoformat(key_metadata["expires_at"])
                if datetime.utcnow() > expiration:
                    key_id = key_metadata["key_id"]
                    self.shred_key(key_id)
                    shredded_count += 1
        
        logger.info(f"🔥 Auto-shred complete - {shredded_count} keys shredded")
        return shredded_count
    
    def get_key_status(self, key_id: str) -> Optional[Dict]:
        """Get status of a key"""
        key_path = os.path.join(self.key_storage_path, f"{key_id}.json")
        
        if not os.path.exists(key_path):
            return None
        
        with open(key_path, 'r') as f:
            key_metadata = json.load(f)
        
        # Remove sensitive key material
        safe_metadata = key_metadata.copy()
        safe_metadata.pop("key", None)
        safe_metadata.pop("iv", None)
        safe_metadata.pop("tag", None)
        
        return safe_metadata
    
    def _log_audit(self, action: str, key_id: str, metadata: Optional[Dict]):
        """Internal audit logging"""
        audit_entry = {
            "timestamp": datetime.utcnow().isoformat(),
            "action": action,
            "key_id": key_id,
            "sovereignty_zone": self.sovereignty_zone.value,
            "metadata": metadata
        }
        self.audit_log.append(audit_entry)
        
        # Persist audit log
        audit_path = os.path.join(self.key_storage_path, "audit.jsonl")
        with open(audit_path, 'a') as f:
            f.write(json.dumps(audit_entry) + '\n')


# Example usage
if __name__ == "__main__":
    # Initialize Crypto Shredder
    shredder = CryptoShredder(
        sovereignty_zone=SovereigntyZone.KENYA,
        enable_audit=True
    )
    
    # Encrypt patient data
    patient_data = b"Patient ID: 12345, Diagnosis: Malaria, Location: Dadaab"
    encrypted_data, key_id = shredder.encrypt_with_ephemeral_key(
        data=patient_data,
        retention_policy=RetentionPolicy.HOT,
        metadata={
            "patient_id": "12345",
            "jurisdiction": "KDPA_KE",
            "data_type": "PHI"
        }
    )
    
    print(f"✅ Encrypted - Key ID: {key_id}")
    
    # Decrypt (while key exists)
    decrypted_data = shredder.decrypt_with_key(encrypted_data, key_id)
    print(f"✅ Decrypted: {decrypted_data.decode()}")
    
    # Shred key (data becomes irrecoverable)
    shredder.shred_key(key_id)
    
    # Try to decrypt after shredding
    decrypted_data = shredder.decrypt_with_key(encrypted_data, key_id)
    print(f"❌ Decryption after shred: {decrypted_data}")  # None
    
    # Check key status
    status = shredder.get_key_status(key_id)
    print(f"📊 Key Status: {json.dumps(status, indent=2)}")
