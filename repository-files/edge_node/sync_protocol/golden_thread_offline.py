"""
IP-05: Golden Thread Offline Buffer
SQLite-based offline sync for edge nodes with intermittent connectivity

Compliance:
- GDPR Art. 32 (Security of Processing)
- HIPAA §164.312 (Technical Safeguards)
- Kenya DPA §37 (Data Sovereignty)
"""

import sqlite3
import json
import hashlib
from datetime import datetime
from typing import Dict, List, Optional
from enum import Enum
import logging

logger = logging.getLogger(__name__)


class DataType(Enum):
    """Types of data in offline buffer"""
    CBS_SIGNAL = "cbs_signal"
    EMR_RECORD = "emr_record"
    VOICE_ALERT = "voice_alert"
    IDSR_REPORT = "idsr_report"
    SENSOR_DATA = "sensor_data"


class SyncStatus(Enum):
    """Sync status for buffered records"""
    PENDING = 0
    SYNCED = 1
    FAILED = 2
    CONFLICT = 3


class GoldenThreadOfflineBuffer:
    """
    Offline buffer for Golden Thread data fusion.
    
    Uses SQLite for local persistence when cloud connectivity is unavailable.
    Automatically syncs when connectivity is restored.
    """
    
    def __init__(self, db_path: str = "/app/data/golden_thread.db"):
        self.db_path = db_path
        self._init_database()
        logger.info(f"🔗 Golden Thread Offline Buffer initialized: {db_path}")
    
    def _init_database(self):
        """Initialize SQLite database schema"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Create offline buffer table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS offline_buffer (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                record_id TEXT UNIQUE NOT NULL,
                timestamp TEXT NOT NULL,
                data_type TEXT NOT NULL,
                payload TEXT NOT NULL,
                hash TEXT NOT NULL,
                synced INTEGER DEFAULT 0,
                sync_attempts INTEGER DEFAULT 0,
                last_sync_attempt TEXT,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Create sync log table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS sync_log (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                record_id TEXT NOT NULL,
                sync_timestamp TEXT NOT NULL,
                status TEXT NOT NULL,
                error_message TEXT,
                FOREIGN KEY (record_id) REFERENCES offline_buffer(record_id)
            )
        """)
        
        # Create indexes
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_synced ON offline_buffer(synced)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_data_type ON offline_buffer(data_type)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_timestamp ON offline_buffer(timestamp)")
        
        conn.commit()
        conn.close()
        
        logger.info("✅ Database schema initialized")
    
    def buffer_record(
        self,
        data_type: DataType,
        payload: Dict,
        record_id: Optional[str] = None
    ) -> str:
        """
        Buffer a record for offline sync.
        
        Args:
            data_type: Type of data being buffered
            payload: Data payload
            record_id: Optional custom record ID
        
        Returns:
            Record ID
        """
        # Generate record ID if not provided
        if not record_id:
            timestamp = datetime.utcnow().isoformat()
            record_id = hashlib.sha256(
                f"{data_type.value}:{timestamp}:{json.dumps(payload)}".encode()
            ).hexdigest()[:16]
        
        # Calculate payload hash
        payload_json = json.dumps(payload, sort_keys=True)
        payload_hash = hashlib.sha256(payload_json.encode()).hexdigest()
        
        # Insert into buffer
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            cursor.execute("""
                INSERT INTO offline_buffer (record_id, timestamp, data_type, payload, hash, synced)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (
                record_id,
                datetime.utcnow().isoformat(),
                data_type.value,
                payload_json,
                payload_hash,
                SyncStatus.PENDING.value
            ))
            
            conn.commit()
            logger.info(f"📦 Buffered record: {record_id} ({data_type.value})")
            
        except sqlite3.IntegrityError:
            logger.warning(f"⚠️ Record already buffered: {record_id}")
        
        finally:
            conn.close()
        
        return record_id
    
    def get_pending_records(
        self,
        data_type: Optional[DataType] = None,
        limit: int = 100
    ) -> List[Dict]:
        """
        Get pending records for sync.
        
        Args:
            data_type: Optional filter by data type
            limit: Maximum number of records to return
        
        Returns:
            List of pending records
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        if data_type:
            cursor.execute("""
                SELECT record_id, timestamp, data_type, payload, hash
                FROM offline_buffer
                WHERE synced = ? AND data_type = ?
                ORDER BY timestamp ASC
                LIMIT ?
            """, (SyncStatus.PENDING.value, data_type.value, limit))
        else:
            cursor.execute("""
                SELECT record_id, timestamp, data_type, payload, hash
                FROM offline_buffer
                WHERE synced = ?
                ORDER BY timestamp ASC
                LIMIT ?
            """, (SyncStatus.PENDING.value, limit))
        
        records = []
        for row in cursor.fetchall():
            records.append({
                "record_id": row[0],
                "timestamp": row[1],
                "data_type": row[2],
                "payload": json.loads(row[3]),
                "hash": row[4]
            })
        
        conn.close()
        
        return records
    
    def mark_synced(self, record_id: str, status: SyncStatus = SyncStatus.SYNCED):
        """Mark a record as synced"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            UPDATE offline_buffer
            SET synced = ?, last_sync_attempt = ?
            WHERE record_id = ?
        """, (status.value, datetime.utcnow().isoformat(), record_id))
        
        # Log sync
        cursor.execute("""
            INSERT INTO sync_log (record_id, sync_timestamp, status)
            VALUES (?, ?, ?)
        """, (record_id, datetime.utcnow().isoformat(), status.name))
        
        conn.commit()
        conn.close()
        
        logger.info(f"✅ Record synced: {record_id} ({status.name})")
    
    def mark_failed(self, record_id: str, error_message: str):
        """Mark a record as failed sync"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            UPDATE offline_buffer
            SET synced = ?, sync_attempts = sync_attempts + 1, last_sync_attempt = ?
            WHERE record_id = ?
        """, (SyncStatus.FAILED.value, datetime.utcnow().isoformat(), record_id))
        
        # Log failure
        cursor.execute("""
            INSERT INTO sync_log (record_id, sync_timestamp, status, error_message)
            VALUES (?, ?, ?, ?)
        """, (record_id, datetime.utcnow().isoformat(), SyncStatus.FAILED.name, error_message))
        
        conn.commit()
        conn.close()
        
        logger.error(f"❌ Record sync failed: {record_id} - {error_message}")
    
    def get_buffer_stats(self) -> Dict:
        """Get buffer statistics"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Total records
        cursor.execute("SELECT COUNT(*) FROM offline_buffer")
        total = cursor.fetchone()[0]
        
        # Pending records
        cursor.execute("SELECT COUNT(*) FROM offline_buffer WHERE synced = ?", (SyncStatus.PENDING.value,))
        pending = cursor.fetchone()[0]
        
        # Synced records
        cursor.execute("SELECT COUNT(*) FROM offline_buffer WHERE synced = ?", (SyncStatus.SYNCED.value,))
        synced = cursor.fetchone()[0]
        
        # Failed records
        cursor.execute("SELECT COUNT(*) FROM offline_buffer WHERE synced = ?", (SyncStatus.FAILED.value,))
        failed = cursor.fetchone()[0]
        
        # By data type
        cursor.execute("""
            SELECT data_type, COUNT(*) 
            FROM offline_buffer 
            WHERE synced = ?
            GROUP BY data_type
        """, (SyncStatus.PENDING.value,))
        
        by_type = {row[0]: row[1] for row in cursor.fetchall()}
        
        conn.close()
        
        return {
            "total": total,
            "pending": pending,
            "synced": synced,
            "failed": failed,
            "by_type": by_type,
            "sync_rate": synced / total if total > 0 else 0
        }
    
    def purge_synced_records(self, older_than_days: int = 7) -> int:
        """
        Purge synced records older than specified days.
        
        Args:
            older_than_days: Delete records older than this many days
        
        Returns:
            Number of records deleted
        """
        from datetime import timedelta
        
        cutoff = (datetime.utcnow() - timedelta(days=older_than_days)).isoformat()
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            DELETE FROM offline_buffer
            WHERE synced = ? AND timestamp < ?
        """, (SyncStatus.SYNCED.value, cutoff))
        
        deleted = cursor.rowcount
        conn.commit()
        conn.close()
        
        logger.info(f"🗑️ Purged {deleted} synced records older than {older_than_days} days")
        
        return deleted


# Example usage
if __name__ == "__main__":
    buffer = GoldenThreadOfflineBuffer()
    
    # Buffer a CBS signal
    record_id = buffer.buffer_record(
        data_type=DataType.CBS_SIGNAL,
        payload={
            "location": "Dadaab",
            "symptom": "fever",
            "timestamp": datetime.utcnow().isoformat(),
            "source": "CHV_AMINA_HASSAN"
        }
    )
    
    print(f"✅ Buffered: {record_id}")
    
    # Get pending records
    pending = buffer.get_pending_records()
    print(f"📦 Pending records: {len(pending)}")
    
    # Get stats
    stats = buffer.get_buffer_stats()
    print(f"📊 Buffer stats: {json.dumps(stats, indent=2)}")
