"""
Step 37: IP-07 Signal Decay & Lifecycle Automation
Automates Golden Thread signal transition from Hot → Cold storage

Compliance:
- GDPR Art. 17 (Right to Erasure)
- Kenya DPA §34 (Data Retention)
- HIPAA §164.530(j) (Documentation Retention)
"""

import logging
from datetime import datetime, timedelta
from typing import Dict, List, Optional
from enum import Enum
from google.cloud import bigtable
from google.cloud import storage
from governance_kernel.crypto_shredder import CryptoShredder, RetentionPolicy

logger = logging.getLogger(__name__)


class StorageTier(Enum):
    """Storage tiers for signal lifecycle"""
    HOT = "hot"  # Bigtable - Active operational data (≤6 months)
    COLD = "cold"  # GCS Archive - Historical data (>6 months)
    SHREDDED = "shredded"  # Cryptographically irrecoverable


class SignalDecayManager:
    """
    IP-07: Manages lifecycle of Golden Thread signals.
    
    Lifecycle stages:
    1. HOT (0-180 days): Active in Bigtable, fast queries
    2. COLD (180+ days): Archived to GCS, compliance retention
    3. SHREDDED (>retention): Crypto Shredder invoked, data dissolved
    """
    
    def __init__(
        self,
        project_id: str,
        bigtable_instance_id: str,
        bigtable_table_id: str,
        gcs_bucket_name: str,
        crypto_shredder: Optional[CryptoShredder] = None
    ):
        self.project_id = project_id
        self.bigtable_instance_id = bigtable_instance_id
        self.bigtable_table_id = bigtable_table_id
        self.gcs_bucket_name = gcs_bucket_name
        
        # Initialize clients
        self.bigtable_client = bigtable.Client(project=project_id, admin=True)
        self.bigtable_instance = self.bigtable_client.instance(bigtable_instance_id)
        self.bigtable_table = self.bigtable_instance.table(bigtable_table_id)
        
        self.storage_client = storage.Client(project=project_id)
        self.gcs_bucket = self.storage_client.bucket(gcs_bucket_name)
        
        # Crypto Shredder for PII dissolution
        self.crypto_shredder = crypto_shredder or CryptoShredder()
        
        # Thresholds
        self.HOT_THRESHOLD_DAYS = 180  # 6 months
        self.COLD_RETENTION_DAYS = 1825  # 5 years (GDPR Art. 17)
        
        logger.info(f"🔄 Signal Decay Manager initialized - Project: {project_id}")
    
    def scan_hot_storage_for_decay(self) -> List[Dict]:
        """
        Scan Bigtable for signals exceeding HOT threshold.
        
        Returns:
            List of signals ready for cold storage transition
        """
        now = datetime.utcnow()
        threshold_date = now - timedelta(days=self.HOT_THRESHOLD_DAYS)
        
        signals_to_archive = []
        
        # Scan Bigtable rows
        row_set = bigtable.row_set.RowSet()
        row_filter = bigtable.row_filters.TimestampRangeFilter(
            bigtable.row_filters.TimestampRange(
                end=threshold_date
            )
        )
        
        rows = self.bigtable_table.read_rows(row_set=row_set, filter_=row_filter)
        
        for row_key, row_data in rows.items():
            # Extract signal data
            signal = {
                "row_key": row_key.decode('utf-8'),
                "timestamp": None,
                "data": {},
                "contains_pii": False
            }
            
            # Parse row data
            for column_family_id, columns in row_data.items():
                for column_id, cells in columns.items():
                    cell_value = cells[0].value.decode('utf-8')
                    signal["data"][f"{column_family_id}:{column_id}"] = cell_value
                    
                    # Check for PII markers
                    if "patient_id" in column_id or "phi" in column_id:
                        signal["contains_pii"] = True
                    
                    # Extract timestamp
                    if column_id == b"timestamp":
                        signal["timestamp"] = datetime.fromisoformat(cell_value)
            
            signals_to_archive.append(signal)
        
        logger.info(f"📊 Found {len(signals_to_archive)} signals ready for cold storage")
        return signals_to_archive
    
    def transition_to_cold_storage(self, signal: Dict) -> bool:
        """
        Transition signal from HOT (Bigtable) to COLD (GCS Archive).
        
        Args:
            signal: Signal data to archive
        
        Returns:
            True if successful
        """
        row_key = signal["row_key"]
        
        try:
            # Step 1: Encrypt PII with Crypto Shredder if present
            if signal["contains_pii"]:
                logger.info(f"🔐 Encrypting PII for signal: {row_key}")
                
                # Serialize signal data
                import json
                signal_json = json.dumps(signal["data"]).encode('utf-8')
                
                # Encrypt with ephemeral key
                encrypted_data, key_id = self.crypto_shredder.encrypt_with_ephemeral_key(
                    data=signal_json,
                    retention_policy=RetentionPolicy.COLD,
                    metadata={
                        "signal_id": row_key,
                        "transition_date": datetime.utcnow().isoformat(),
                        "storage_tier": StorageTier.COLD.value
                    }
                )
                
                # Store encrypted data
                archive_data = {
                    "encrypted": True,
                    "key_id": key_id,
                    "data": encrypted_data.hex()
                }
            else:
                # No PII - store as-is
                archive_data = {
                    "encrypted": False,
                    "data": signal["data"]
                }
            
            # Step 2: Write to GCS Archive
            import json
            blob_name = f"cold_storage/{signal['timestamp'].year}/{signal['timestamp'].month}/{row_key}.json"
            blob = self.gcs_bucket.blob(blob_name)
            blob.upload_from_string(
                json.dumps(archive_data, indent=2),
                content_type="application/json"
            )
            
            # Set storage class to ARCHIVE
            blob.update_storage_class("ARCHIVE")
            
            logger.info(f"✅ Archived to GCS: {blob_name}")
            
            # Step 3: Delete from Bigtable (HOT storage)
            row = self.bigtable_table.row(row_key.encode('utf-8'))
            row.delete()
            row.commit()
            
            logger.info(f"🗑️ Deleted from Bigtable: {row_key}")
            
            return True
        
        except Exception as e:
            logger.error(f"❌ Failed to transition signal {row_key}: {e}")
            return False
    
    def scan_cold_storage_for_expiration(self) -> List[str]:
        """
        Scan GCS Archive for signals exceeding COLD retention period.
        
        Returns:
            List of blob names ready for shredding
        """
        now = datetime.utcnow()
        expiration_date = now - timedelta(days=self.COLD_RETENTION_DAYS)
        
        blobs_to_shred = []
        
        # List all blobs in cold storage
        blobs = self.gcs_bucket.list_blobs(prefix="cold_storage/")
        
        for blob in blobs:
            # Check blob creation time
            if blob.time_created < expiration_date:
                blobs_to_shred.append(blob.name)
        
        logger.info(f"🔥 Found {len(blobs_to_shred)} signals ready for shredding")
        return blobs_to_shred
    
    def shred_expired_signal(self, blob_name: str) -> bool:
        """
        Shred expired signal using Crypto Shredder (IP-02).
        
        Args:
            blob_name: GCS blob name
        
        Returns:
            True if successful
        """
        try:
            # Step 1: Read blob
            blob = self.gcs_bucket.blob(blob_name)
            
            import json
            archive_data = json.loads(blob.download_as_text())
            
            # Step 2: Shred encryption key if encrypted
            if archive_data.get("encrypted"):
                key_id = archive_data["key_id"]
                self.crypto_shredder.shred_key(key_id)
                logger.info(f"🔥 Shredded key: {key_id}")
            
            # Step 3: Delete blob from GCS
            blob.delete()
            logger.info(f"🗑️ Deleted blob: {blob_name}")
            
            return True
        
        except Exception as e:
            logger.error(f"❌ Failed to shred signal {blob_name}: {e}")
            return False
    
    def run_lifecycle_automation(self) -> Dict:
        """
        Execute full lifecycle automation cycle.
        
        Returns:
            Automation report
        """
        logger.info("🔄 Starting lifecycle automation cycle...")
        
        report = {
            "timestamp": datetime.utcnow().isoformat(),
            "hot_to_cold": {"scanned": 0, "transitioned": 0, "failed": 0},
            "cold_to_shredded": {"scanned": 0, "shredded": 0, "failed": 0}
        }
        
        # Phase 1: HOT → COLD
        signals_to_archive = self.scan_hot_storage_for_decay()
        report["hot_to_cold"]["scanned"] = len(signals_to_archive)
        
        for signal in signals_to_archive:
            if self.transition_to_cold_storage(signal):
                report["hot_to_cold"]["transitioned"] += 1
            else:
                report["hot_to_cold"]["failed"] += 1
        
        # Phase 2: COLD → SHREDDED
        blobs_to_shred = self.scan_cold_storage_for_expiration()
        report["cold_to_shredded"]["scanned"] = len(blobs_to_shred)
        
        for blob_name in blobs_to_shred:
            if self.shred_expired_signal(blob_name):
                report["cold_to_shredded"]["shredded"] += 1
            else:
                report["cold_to_shredded"]["failed"] += 1
        
        logger.info(f"✅ Lifecycle automation complete: {report}")
        return report
    
    def get_storage_statistics(self) -> Dict:
        """
        Get storage tier statistics.
        
        Returns:
            Storage statistics
        """
        # Count HOT storage (Bigtable)
        hot_count = 0
        rows = self.bigtable_table.read_rows()
        for _ in rows:
            hot_count += 1
        
        # Count COLD storage (GCS)
        cold_count = 0
        blobs = self.gcs_bucket.list_blobs(prefix="cold_storage/")
        for _ in blobs:
            cold_count += 1
        
        return {
            "hot_storage": {
                "count": hot_count,
                "tier": StorageTier.HOT.value,
                "backend": "Bigtable",
                "retention_days": self.HOT_THRESHOLD_DAYS
            },
            "cold_storage": {
                "count": cold_count,
                "tier": StorageTier.COLD.value,
                "backend": "GCS Archive",
                "retention_days": self.COLD_RETENTION_DAYS
            }
        }


# Example usage
if __name__ == "__main__":
    manager = SignalDecayManager(
        project_id="iluminara-core",
        bigtable_instance_id="golden-thread",
        bigtable_table_id="signals",
        gcs_bucket_name="iluminara-cold-storage"
    )
    
    # Run lifecycle automation
    report = manager.run_lifecycle_automation()
    print(f"📊 Lifecycle Report: {report}")
    
    # Get storage statistics
    stats = manager.get_storage_statistics()
    print(f"📈 Storage Statistics: {stats}")
