"""
SecureDoc – Central Configuration
All values are loaded from environment variables (.env file).
Never hardcode secrets here.
"""

import os
from dotenv import load_dotenv

load_dotenv()

# ── Monitored Directory ────────────────────────────────────────────────────────
MONITORED_DIR: str = os.getenv("MONITORED_DIR", r"C:\SecuredFolder")

# ── Tracked File Extensions ────────────────────────────────────────────────────
TRACKED_EXTENSIONS: list[str] = [".pdf", ".docx", ".txt", ".csv", ".xlsx"]

# ── Stakeholder Bot (Private Alerts) ──────────────────────────────────────────
STAKEHOLDER_BOT_TOKEN: str = os.getenv("STAKEHOLDER_BOT_TOKEN", "")
STAKEHOLDER_CHAT_IDS:  list[str] = [
    cid.strip()
    for cid in os.getenv("STAKEHOLDER_CHAT_IDS", "").split(",")
    if cid.strip()
]

# ── Public Ledger Bot ──────────────────────────────────────────────────────────
PUBLIC_BOT_TOKEN: str = os.getenv("PUBLIC_BOT_TOKEN", "")
PUBLIC_CHAT_IDS:  list[str] = [
    cid.strip()
    for cid in os.getenv("PUBLIC_CHAT_IDS", "").split(",")
    if cid.strip()
]

# ── Database ───────────────────────────────────────────────────────────────────
DB_FILE: str = os.getenv("DB_FILE", "audit_logs.db")
