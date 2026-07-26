"""
SecureDoc – Telegram Alert Service
Dispatches alerts in parallel via daemon threads.

  • Stakeholder Bot  →  full alert (file, actor, ref ID)
  • Public Ledger Bot →  anonymised audit entry (ref ID only)
"""

import threading
import requests
from config import (
    STAKEHOLDER_BOT_TOKEN,
    STAKEHOLDER_CHAT_IDS,
    PUBLIC_BOT_TOKEN,
    PUBLIC_CHAT_IDS,
)

_TIMEOUT = 4  # seconds per HTTP request


def _send(bot_token: str, chat_id: str, text: str) -> None:
    """Fire-and-forget single Telegram message. Silently swallows errors."""
    try:
        requests.post(
            f"https://api.telegram.org/bot{bot_token}/sendMessage",
            data={"chat_id": chat_id, "text": text},
            timeout=_TIMEOUT,
        )
    except Exception:
        pass


def _dispatch(bot_token: str, chat_ids: list[str], text: str) -> None:
    """Spin up one daemon thread per recipient for zero-latency delivery."""
    for chat_id in chat_ids:
        threading.Thread(
            target=_send,
            args=(bot_token, chat_id, text),
            daemon=True,
        ).start()


def broadcast_event(
    action: str,
    file_name: str,
    actor: str,
    ref_id: str,
    timestamp: str,
) -> None:
    """
    Send alerts to both channels concurrently.
    Stakeholder channel includes the file name and actor.
    Public channel is anonymised — ref ID and action only.
    """
    stakeholder_msg = (
        f"🚨 DOCUMENT ALERT\n"
        f"Action : {action}\n"
        f"File   : {file_name}\n"
        f"Actor  : {actor}\n"
        f"Ref ID : {ref_id}\n"
        f"Time   : {timestamp}"
    )

    public_msg = (
        f"🔒 PUBLIC AUDIT ENTRY\n"
        f"Ref ID : {ref_id}\n"
        f"Action : {action}\n"
        f"Time   : {timestamp}"
    )

    _dispatch(STAKEHOLDER_BOT_TOKEN, STAKEHOLDER_CHAT_IDS, stakeholder_msg)
    _dispatch(PUBLIC_BOT_TOKEN, PUBLIC_CHAT_IDS, public_msg)
