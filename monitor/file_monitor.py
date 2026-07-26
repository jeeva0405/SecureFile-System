"""
SecureDoc – Real-Time File Monitor
Uses watchdog for filesystem events (CREATE / MODIFY / DELETE / RENAME)
and a background thread for native Windows file-lock access detection.

Access detection trick:
  os.rename(path, path) raises PermissionError when Windows has the file
  locked by another process (e.g. Adobe, Word, Chrome). This costs 0% CPU
  and requires zero external libraries.
"""

import os
import time
import getpass
import datetime
import threading

from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

from logger import generate_ref_id, log_event
from telegram import broadcast_event
from config import TRACKED_EXTENSIONS

# ── Debounce window (seconds) ─────────────────────────────────────────────────
_DEBOUNCE = 2.0
_POLL_INTERVAL = 0.5


class _FileEventHandler(FileSystemEventHandler):
    """Watchdog handler that filters noise and triggers the audit pipeline."""

    def __init__(self) -> None:
        self._last_event: dict[str, float] = {}
        self._file_sizes: dict[str, int] = {}

    # ── Public pipeline ───────────────────────────────────────────────────────

    def trigger(self, action: str, path: str) -> None:
        """Validate, debounce, then log + broadcast the event."""
        if action != "DELETED" and not os.path.exists(path):
            return

        now = time.time()
        key = f"{path}_{action}"

        if (now - self._last_event.get(key, 0)) < _DEBOUNCE:
            return
        self._last_event[key] = now

        actor     = getpass.getuser()
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        file_name = os.path.basename(path)
        ref_id    = generate_ref_id(path, action, timestamp)

        print(f"  [{timestamp}]  {action:<10}  {file_name}")

        log_event(ref_id, file_name, action, actor, timestamp)
        broadcast_event(action, file_name, actor, ref_id, timestamp)

    def access(self, path: str) -> None:
        """Called from the access-detection thread for ACCESSED events."""
        if self._is_tracked(path):
            self.trigger("ACCESSED", path)

    # ── Watchdog callbacks ────────────────────────────────────────────────────

    def on_created(self, event) -> None:
        if event.is_directory:
            return
        path = event.src_path
        if self._is_junk(path) or not self._is_tracked(path):
            return
        try:
            self._file_sizes[path] = os.path.getsize(path)
        except OSError:
            pass
        self.trigger("CREATED", path)

    def on_modified(self, event) -> None:
        if event.is_directory:
            return
        path = event.src_path
        if self._is_junk(path) or not self._is_tracked(path):
            return
        try:
            new_size = os.path.getsize(path)
        except OSError:
            return
        old_size = self._file_sizes.get(path)
        self._file_sizes[path] = new_size
        if old_size is None or new_size != old_size:
            self.trigger("MODIFIED", path)

    def on_deleted(self, event) -> None:
        if event.is_directory:
            return
        path = event.src_path
        if self._is_junk(path) or not self._is_tracked(path):
            return
        self.trigger("DELETED", path)

    def on_moved(self, event) -> None:
        if event.is_directory:
            return
        dest = getattr(event, "dest_path", event.src_path)
        if self._is_junk(dest) or not self._is_tracked(dest):
            return
        self.trigger("RENAMED", dest)

    # ── Helpers ───────────────────────────────────────────────────────────────

    @staticmethod
    def _is_junk(path: str) -> bool:
        """Return True for MS Office temp / lock files."""
        name = os.path.basename(path)
        return name.startswith("~$") or name.startswith("~") or name.endswith(".tmp")

    @staticmethod
    def _is_tracked(path: str) -> bool:
        return os.path.splitext(path)[1].lower() in TRACKED_EXTENSIONS


def _access_detection_loop(handler: _FileEventHandler, folder: str) -> None:
    """
    Background thread: poll the watched folder and detect file opens
    via Windows file-lock (PermissionError on os.rename to itself).
    """
    opened: set[str] = set()

    while True:
        current: set[str] = set()
        try:
            for entry in os.scandir(folder):
                if not entry.is_file():
                    continue
                path = entry.path
                if (
                    os.path.basename(path).startswith("~")
                    or path.endswith(".tmp")
                    or os.path.splitext(path)[1].lower() not in TRACKED_EXTENSIONS
                ):
                    continue
                try:
                    os.rename(path, path)
                except PermissionError:
                    current.add(path)
                except OSError:
                    pass
        except Exception:
            pass

        for f in current - opened:
            handler.access(f)

        opened = current
        time.sleep(_POLL_INTERVAL)


def start_monitoring(path: str) -> None:
    """Entry point: create the watched directory if needed, then start all threads."""
    os.makedirs(path, exist_ok=True)

    print("=" * 60)
    print(f"  ✅  Tracked types : {TRACKED_EXTENSIONS}")
    print(f"  📁  Watching      : {path}")
    print("=" * 60)
    print("  🚀  Monitoring STARTED — waiting for events...\n")

    handler = _FileEventHandler()

    threading.Thread(
        target=_access_detection_loop,
        args=(handler, path),
        daemon=True,
    ).start()

    observer = Observer()
    observer.schedule(handler, path, recursive=True)
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n  🛑  Monitoring stopped.")
        observer.stop()

    observer.join()
