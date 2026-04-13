# AGENTS.md — SkyTrack AI Agent Conventions

This file defines conventions, constraints, and context for any AI coding agent working in this repository.

---

## Repository overview

SkyTrack is a Python 3.12+ / PySide6 desktop pilot client for the SkyHigh virtual aviation network.
It targets Windows 10/11 first with a Linux-compatible architecture.

---

## Branch strategy

| Branch prefix | Purpose |
|---|---|
| `main` | Stable, tested, release-ready code only |
| `feat/<name>` | New feature work |
| `fix/<name>` | Bug fixes |
| `chore/<name>` | Tooling, deps, CI, non-feature work |
| `docs/<name>` | Documentation only |

- Always branch off `main`.
- Open a **draft PR** as soon as the first commit lands on a feature branch.
- Convert to ready for review only when tests pass and ruff/mypy are clean.
- Use small, descriptive commits. Do not squash to a single commit.
- Never force-push to `main`.

---

## Commit message format

```
<type>(<scope>): <short description>

[optional body]

[optional footers]
```

Types: `feat`, `fix`, `chore`, `docs`, `test`, `refactor`, `style`, `perf`.
Scopes: `core`, `ui`, `network`, `voice`, `radio`, `sim`, `config`, `docs`, `tests`.

Examples:
- `feat(radio): add 8.33 kHz channel spacing validation`
- `fix(sim): guard against None position update in XPlane adapter`
- `docs(roadmap): update phase 2 milestone targets`

---

## Coding conventions

- Python 3.12+, type hints everywhere.
- `pydantic` for all settings and data models that cross service boundaries.
- `dataclasses` with `slots=True` for internal pure-data objects.
- No `TypeVar` workarounds — use `type X = ...` syntax (Python 3.12 style alias).
- Never use `Any` unless absolutely unavoidable and documented with a `# type: ignore` comment explaining why.
- `loguru` for all logging. Never `print()` in production code paths.
- All async service methods use `asyncio`. Never `threading` unless wrapping a blocking C-extension.
- UI code in `ui/` must not import from `services/` directly — wire through the `AppStateStore` and signal/slot contracts.
- Services must not import from `ui/`.
- Keep files under 300 lines. Split if needed.

---

## Security rules (hard stops)

- NEVER commit secrets, tokens, passwords, certificates, or private server credentials.
- NEVER hardcode IP addresses, hostnames, or port numbers outside `core/config.py` defaults.
- NEVER disable the `.gitignore` rules for `.env`, `*.pem`, `*.key`, or similar files.
- Scan new files for secrets before committing (see `services/network/swift_bridge.py` for the config pattern).
- Use `.env.example` to document required environment variables. Use `.env` locally. Commit only `.env.example`.

---

## Testing conventions

- Tests live in `tests/`. Mirror `src/skytrack/` package structure.
- Use `pytest`. Use `pytest-qt` for any widget tests.
- Every new service module must have at least one unit test.
- Mock external I/O (network sockets, audio devices, file system) in tests.
- Run before every PR checkpoint: `ruff check src tests && mypy src && pytest`.

---

## Integration extension points

The following modules have **adapter/bridge boundaries** — they are intentionally stubbed and documented for later completion. When extending them, implement the full Protocol interface and replace the mock/stub class.

### swift bridge
- File: `src/skytrack/services/network/swift_bridge.py`
- Pattern: localhost helper process, JSON-RPC or WebSocket over `127.0.0.1:51001` by default.
- What to implement: real socket/WS client, message serialisation, reconnect logic.
- References: `integrations/swift/README.md`

### FGCom bridge
- File: `src/skytrack/services/radio/fgcom_bridge.py`
- Pattern: translate `NormalizedRadioPacket` to FGCom-mumble UDP or plugin format.
- What to implement: UDP socket send to fgcom-mumble plugin listener, or pipe to native helper.
- References: `integrations/fgcom/README.md`, https://github.com/hbeni/fgcom-mumble

### Mumble service
- File: `src/skytrack/services/voice/mumble_service.py`
- Pattern: `MumbleService` Protocol. Replace `MockMumbleService` with a real implementation.
- Options: `pymumble` (see note in file), native helper process, or libmumble-based adapter.
- References: `integrations/mumble/README.md`

### X-Plane 11 adapter
- File: `src/skytrack/services/sim/xplane_adapter.py`
- Pattern: `SimAdapter` Protocol. Implement UDP ExtPlane or X-Plane Connect (XPC) client.
- Blocked by: `xpc3` or `ExtPlane` Python client dependency. See issue tracker.

### X-Plane 12 adapter
- File: `src/skytrack/services/sim/xplane12_adapter.py`
- Pattern: same as XP11 but may use updated UDP packet format and FMOD paths.
- Blocked by: XP12 Connect / XPUIPC or native UDP testing.

### MSFS 2020 adapter
- File: `src/skytrack/services/sim/msfs2020_adapter.py`
- Pattern: `SimAdapter` Protocol. Implement SimConnect via `SimConnect` Python package.
- Blocked by: `SimConnect` SDK availability (Windows only). See issue tracker.

### MSFS 2024 adapter
- File: `src/skytrack/services/sim/msfs2024_adapter.py`
- Pattern: Same SimConnect interface; verify compatible SDK version for MSFS 2024.
- Blocked by: MSFS 2024 SimConnect SDK availability. See issue tracker.

---

## Do not break

- `AppStateStore.update()` must remain the only way to mutate application state.
- `RadioService` must remain isolated from UI. Never pass a Qt widget into a service.
- `core/config.py` must be the single source of truth for all defaults and profiles.
- `core/events.py` `EventBus` must remain decoupled from Qt signals (it is testable without Qt).

---

## Roadmap reference

See [docs/roadmap.md](docs/roadmap.md) for phased milestones and priority order.
