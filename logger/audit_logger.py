"""
SecureDoc – Blockchain-Style Audit Logger
Each log entry is chained: hash(current_data + previous_hash)
This makes the entire log tamper-evident.
"""

import sqlite3
import hashlib
from config import DB_FILE


def init_db() -> None:
    """Initialise the SQLite database and create the audit_logs table if absent."""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS audit_logs (
            id            INTEGER PRIMARY KEY AUTOINCREMENT,
            ref_id        TEXT    NOT NULL,
            file_name     TEXT    NOT NULL,
            action        TEXT    NOT NULL,
            actor         TEXT    NOT NULL,
            timestamp     TEXT    NOT NULL,
            hash          TEXT    NOT NULL,
            previous_hash TEXT    NOT NULL
        )
    """)
    conn.commit()
    conn.close()


def _get_previous_hash() -> str:
    """Fetch the hash of the most recent log entry (genesis hash if empty)."""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("SELECT hash FROM audit_logs ORDER BY id DESC LIMIT 1")
    row = cursor.fetchone()
    conn.close()
    return row[0] if row else "0" * 64


def generate_ref_id(file_path: str, action: str, timestamp: str) -> str:
    """Generate a short 16-char SHA-256 derived reference ID for the event."""
    data = f"{file_path}{action}{timestamp}"
    return hashlib.sha256(data.encode()).hexdigest()[:16]


def log_event(
    ref_id: str,
    file_name: str,
    action: str,
    actor: str,
    timestamp: str,
) -> str:
    """
    Persist an audit event and return the new chain hash.
    current_hash = SHA-256(log_data + previous_hash)
    """
    prev_hash = _get_previous_hash()
    log_data = f"{ref_id}{file_name}{action}{actor}{timestamp}"
    current_hash = hashlib.sha256((log_data + prev_hash).encode()).hexdigest()

    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO audit_logs
            (ref_id, file_name, action, actor, timestamp, hash, previous_hash)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (ref_id, file_name, action, actor, timestamp, current_hash, prev_hash))
    conn.commit()
    conn.close()

    return current_hash
