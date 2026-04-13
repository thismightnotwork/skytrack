# SkyTrack

> **Production-quality desktop pilot client for the SkyHigh virtual aviation network.**

SkyTrack is a Windows-first (Linux-ready architecture) Python/PySide6 desktop application combining:

- Pilot session management, FSD-style network connection, and text communications
- Integrated COM1/COM2 radio stack with real frequency validation and FGCom-style state logic
- Mumble-based voice communication with FGCom-mumble compatibility boundary
- X-Plane 11/12 and MSFS 2020/2024 simulator data connectors
- Swift-compatible network bridge interface
- Premium aviation-ops dark UI with status chips, docked event log, and panel navigation

---

## Quick start

### Requirements

- Python 3.12+
- Windows 10/11 (primary target) or Linux (architecture supported)
- Microphone + headset recommended for voice

### Install

```bash
git clone https://github.com/thismightnotwork/skytrack.git
cd skytrack
python -m venv .venv

# Windows PowerShell
.venv\Scripts\Activate.ps1
# Linux / macOS
source .venv/bin/activate

pip install -e .
```

### Run

```bash
skytrack
```

Or directly:

```bash
python -m skytrack.app.main
```

### Development install (with lint / test tools)

```bash
pip install -e ".[dev]"
```

---

## Configuration

SkyTrack writes typed JSON settings to `~/.skytrack/settings.json` on first run.

Environment overrides are supported via `.env` (copy `.env.example`, never commit secrets).

```json
{
  "profile": "dev",
  "network": {
    "default_server": "dev.skyhigh.local",
    "swift_bridge_mode": "helper-process",
    "bridge_host": "127.0.0.1",
    "bridge_port": 51001
  },
  "voice": {
    "mumble_host": "voice.skyhigh.local",
    "mumble_port": 64738
  }
}
```

---

## Project structure

```text
skytrack/
├── pyproject.toml
├── README.md
├── AGENTS.md
├── docs/
│   └── roadmap.md
└── src/
    └── skytrack/
        ├── app/          # Entrypoint, DI container bootstrap
        ├── core/         # Config, state store, events, models, logging
        ├── ui/           # PySide6 main window, theme, all panels
        ├── services/
        │   ├── network/  # Network service, swift bridge boundary
        │   ├── voice/    # Mumble adapter, audio devices, PTT
        │   ├── radio/    # Radio state model, FGCom bridge
        │   └── sim/      # Sim adapters: XPlane 11/12, MSFS 2020/2024
        ├── integrations/ # Bridge notes: swift, mumble, fgcom
        └── tests/
```

---

## Integration status

| Component | Status | Notes |
|---|---|---|
| Core UI / radio stack | ✅ Implemented | Fully functional in MVP |
| Config / settings | ✅ Implemented | JSON persistence + env overrides |
| Network service | ⚠️ Mock / bridge boundary | Awaits swift helper process |
| Voice / Mumble | ⚠️ Mock / bridge boundary | Awaits native Mumble adapter |
| FGCom bridge | ⚠️ Interface defined | Awaits UDP/plugin bridge |
| X-Plane 11 adapter | ⚠️ Stub with interface | UDP ExtPlane/XPC integration |
| X-Plane 12 adapter | ⚠️ Stub with interface | UDP ExtPlane/XPC integration |
| MSFS 2020 adapter | ⚠️ Stub with interface | SimConnect SDK required |
| MSFS 2024 adapter | ⚠️ Stub with interface | SimConnect SDK required |

---

## Packaging

Use PyInstaller for Windows distribution:

```bash
pip install pyinstaller
pyinstaller --onedir --windowed --name SkyTrack src/skytrack/app/main.py
```

A `.spec` file will be added in a later milestone.

---

## Contributing

See [AGENTS.md](AGENTS.md) for AI-agent coding conventions, branch strategy, and integration extension points.
See [docs/roadmap.md](docs/roadmap.md) for the phased feature plan.

---

## Licence

MIT — see [LICENSE](LICENSE) (to be added).
