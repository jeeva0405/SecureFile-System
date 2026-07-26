"""
SecureDoc Audit System (SAS) – Entry Point
Run:  python main.py
"""

from logger import init_db
from monitor import start_monitoring
from config import MONITORED_DIR


def main() -> None:
    print()
    print("  ╔══════════════════════════════════════════════╗")
    print("  ║      SecureDoc Audit System  v1.0            ║")
    print("  ╚══════════════════════════════════════════════╝")
    print()
    print("  Initialising audit database...")
    init_db()

    print(f"  Target directory : {MONITORED_DIR}")
    print("  Starting real-time file monitoring...\n")

    start_monitoring(MONITORED_DIR)


if __name__ == "__main__":
    main()
