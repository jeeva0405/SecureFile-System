<div align="center">

<img src="https://capsule-render.vercel.app/api?type=waving&color=0:1a1a2e,50:16213e,100:0f3460&height=250&section=header&text=SecureFile-System&fontSize=72&animation=fadeIn&fontColor=e94560&fontAlignY=38&desc=Tamper-Evident%20File%20Audit%20System&descAlignY=54&descAlign=50&descColor=a8dadc" width="100%" />

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![Watchdog](https://img.shields.io/badge/Watchdog-File%20Monitor-green?style=for-the-badge&logo=files&logoColor=white)](https://github.com/gorakhargosh/watchdog)
[![Telegram](https://img.shields.io/badge/Telegram-Dual%20Alerts-26A5E4?style=for-the-badge&logo=telegram&logoColor=white)](https://core.telegram.org/bots)
[![SQLite](https://img.shields.io/badge/SQLite-Blockchain%20Log-003B57?style=for-the-badge&logo=sqlite&logoColor=white)](https://sqlite.org)
[![License](https://img.shields.io/badge/License-MIT-yellow?style=for-the-badge)](LICENSE)

<br/>

<p align="center">
  <img src="https://readme-typing-svg.demolab.com?font=Fira+Code&weight=600&size=20&pause=1000&color=E94560&center=true&vCenter=true&width=680&lines=Real-time+document+access+detection;Blockchain-style+tamper-evident+logs;Instant+Telegram+alerts+to+stakeholders;Privacy-first+public+audit+ledger;Zero+secrets+in+code+%E2%80%94+env-driven+config" alt="Typing SVG" />
</p>

</div>

---

## <img src="https://raw.githubusercontent.com/Tarikul-Islam-Anik/Animated-Fluent-Emojis/master/Emojis/Smilies/Star-Struck.png" alt="Star-Struck" width="25" height="25" /> Features

- <img src="https://raw.githubusercontent.com/Tarikul-Islam-Anik/Animated-Fluent-Emojis/master/Emojis/Travel%20and%20places/High%20Voltage.png" width="20"/> **Real-Time Monitoring** — Instantly detects `CREATED`, `MODIFIED`, `DELETED`, `RENAMED`, and `ACCESSED` events on any document in the watched folder.
- <img src="https://raw.githubusercontent.com/Tarikul-Islam-Anik/Animated-Fluent-Emojis/master/Emojis/Objects/Lock.png" width="20"/> **Blockchain-Style Audit Log** — Every event is SHA-256 chained (`hash = SHA256(log_data + prev_hash)`), making the log tamper-evident and cryptographically verifiable.
- <img src="https://raw.githubusercontent.com/Tarikul-Islam-Anik/Animated-Fluent-Emojis/master/Emojis/Objects/Bell.png" width="20"/> **Dual Telegram Channels** — A private **Stakeholder Bot** receives full alerts (file, actor, ref ID). A **Public Ledger Bot** broadcasts anonymised entries for transparency.
- <img src="https://raw.githubusercontent.com/Tarikul-Islam-Anik/Animated-Fluent-Emojis/master/Emojis/Smilies/Ghost.png" width="20"/> **Smart Noise Filtering** — Debounces duplicate events (2 s window) and ignores MS Office temp/lock files (`~$*`, `*.tmp`) automatically.
- <img src="https://raw.githubusercontent.com/Tarikul-Islam-Anik/Animated-Fluent-Emojis/master/Emojis/Travel%20and%20places/Rocket.png" width="20"/> **Parallel Alert Dispatch** — All Telegram messages fire concurrently via daemon threads — zero blocking, zero latency.
- <img src="https://raw.githubusercontent.com/Tarikul-Islam-Anik/Animated-Fluent-Emojis/master/Emojis/Objects/Shield.png" width="20"/> **Zero Secrets in Code** — Credentials and paths are loaded exclusively from `.env`; nothing sensitive ever enters the repository.

<br/>

## <img src="https://raw.githubusercontent.com/Tarikul-Islam-Anik/Animated-Fluent-Emojis/master/Emojis/Objects/File%20Folder.png" width="25"/> Project Structure

```
SecureFile System/
│
├── assets/                        # Screenshots & media
│   ├── public_ledger.png          #   Public Ledger Bot preview
│   └── stakeholder_bot.png        #   Stakeholder Bot preview
│
├── config/                        # ⚙️  Central configuration package
│   ├── __init__.py                #   Re-exports all settings
│   └── settings.py                #   Env-var driven settings
│
├── logger/                        # 🔗  Blockchain-style audit logger
│   ├── __init__.py
│   └── audit_logger.py            #   SQLite chained event persistence
│
├── monitor/                       # 👁  Real-time filesystem watcher
│   ├── __init__.py
│   └── file_monitor.py            #   Watchdog handler + access detection
│
├── telegram/                      # 📡  Telegram alert dispatcher
│   ├── __init__.py
│   └── alert_service.py           #   Dual-channel parallel dispatch
│
├── main.py                        # 🚀  Entry point
├── requirements.txt               # 📦  Python dependencies
├── .env.example                   # 🔑  Env variable template
└── .gitignore
```

<br/>

## <img src="https://raw.githubusercontent.com/Tarikul-Islam-Anik/Animated-Fluent-Emojis/master/Emojis/Objects/Gear.png" width="25"/> How It Works

```
File Event
    │
    ▼
_FileEventHandler (watchdog)       detect_access thread
    │  CREATED / MODIFIED              │  polls os.rename() trick
    │  DELETED  / RENAMED              │  PermissionError → file open
    └─────────────┬─────────────────── ┘
                  ▼
           trigger(action, path)
                  │
         ┌────────┴──────────┐
         ▼                   ▼
    log_event()        broadcast_event()
  (SQLite chain)     (Telegram threads)
         │                   │
   SHA-256 hash         Stakeholder Bot  →  full alert
   prev → current      Public Ledger Bot →  anonymised
```

<br/>

## <img src="https://raw.githubusercontent.com/Tarikul-Islam-Anik/Animated-Fluent-Emojis/master/Emojis/Travel%20and%20places/Rocket.png" width="30"/> Getting Started

### <img src="https://raw.githubusercontent.com/Tarikul-Islam-Anik/Animated-Fluent-Emojis/master/Emojis/Objects/Clipboard.png" width="22"/> Prerequisites

- [Python 3.8+](https://python.org/)
- Two Telegram bots — create via [@BotFather](https://t.me/BotFather)
- Windows OS (access detection relies on the Windows file-lock mechanism)

---

### <img src="https://raw.githubusercontent.com/Tarikul-Islam-Anik/Animated-Fluent-Emojis/master/Emojis/Objects/Hammer%20and%20Wrench.png" width="22"/> Installation

<img align="right" src="https://raw.githubusercontent.com/Tarikul-Islam-Anik/Animated-Fluent-Emojis/master/Emojis/Objects/Laptop.png" width="130" alt="Laptop"/>

**1. Clone the repository**
```bash
git clone https://github.com/jeeva0405/SecureFile-System.git
cd SecureFile System
```

**2. Install dependencies**
```bash
pip install -r requirements.txt
```

**3. Configure environment variables**

Copy the template and fill in your values:
```bash
cp .env.example .env
```

```env
# Folder to watch
MONITORED_DIR=C:\Path\To\Your\SecuredFolder

# Stakeholder Bot  (receives full alerts — file name + actor)
STAKEHOLDER_BOT_TOKEN=your_stakeholder_bot_token
STAKEHOLDER_CHAT_IDS=chat_id_1,chat_id_2

# Public Ledger Bot  (receives anonymised audit entries)
PUBLIC_BOT_TOKEN=your_public_bot_token
PUBLIC_CHAT_IDS=chat_id_1,chat_id_2,chat_id_3

# Database file (relative path)
DB_FILE=audit_logs.db
```

**4. Run**
```bash
python main.py
```

<br/>

## <img src="https://raw.githubusercontent.com/Tarikul-Islam-Anik/Animated-Fluent-Emojis/master/Emojis/Objects/Memo.png" width="25"/> Audit Log Schema

| Column | Type | Description |
| :--- | :--- | :--- |
| `id` | INTEGER | Auto-increment primary key |
| `ref_id` | TEXT | 16-char SHA-256 derived event identifier |
| `file_name` | TEXT | Name of the affected file |
| `action` | TEXT | `CREATED` · `MODIFIED` · `DELETED` · `RENAMED` · `ACCESSED` |
| `actor` | TEXT | OS username of the user who triggered the event |
| `timestamp` | TEXT | `YYYY-MM-DD HH:MM:SS` |
| `hash` | TEXT | SHA-256 of current log entry + previous hash |
| `previous_hash` | TEXT | Hash of the preceding log entry (chain link) |

<br/>


## <img src="https://raw.githubusercontent.com/Tarikul-Islam-Anik/Animated-Fluent-Emojis/master/Emojis/Hand%20gestures/Handshake.png" width="30"/> Contributing

Pull requests are welcome! Please open an issue first to discuss what you'd like to change.

<br/>

<div align="center">

<img src="https://raw.githubusercontent.com/Tarikul-Islam-Anik/Animated-Fluent-Emojis/master/Emojis/Objects/Shield.png" width="50" alt="Shield"/>

### Built with ❤️ for document security and compliance

<img src="https://capsule-render.vercel.app/api?type=waving&color=0:1a1a2e,50:16213e,100:0f3460&height=100&section=footer" width="100%"/>

</div>
