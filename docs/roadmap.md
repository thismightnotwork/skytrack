# SkyTrack Roadmap

This document tracks the phased development plan for SkyTrack.
Priority order: Clean architecture → Stable radio/network integration → Premium UI/UX → Extensibility → Performance → Cross-platform.

---

## Phase 1 — Foundation (MVP) ✅ In progress

**Goal:** Runnable desktop pilot client with real internal logic and adapter-backed external integrations.

- [x] PySide6 main window with sidebar navigation
- [x] Premium dark aviation-ops theme
- [x] Top status bar: NET / VOICE / SIM chips, callsign
- [x] Network connection panel (callsign, server, connect/disconnect)
- [x] COM1 / COM2 radio stack with swap, volume, power, monitor toggles
- [x] Frequency validation (VHF COM band, 8.33 spacing groundwork)
- [x] Audio / devices panel (input, output, PTT key)
- [x] Messages panel with nearby traffic list
- [x] Settings panel
- [x] Diagnostics panel with live state dump
- [x] Docked event log (bottom)
- [x] Typed pydantic config with JSON persistence and env overrides
- [x] Loguru structured logging with rotating file output
- [x] Central AppStateStore + EventBus
- [x] Mock network service backed by SwiftBridgeClient boundary
- [x] Mock Mumble service backed by MumbleService interface
- [x] Real radio state model (RadioService, NormalizedRadioPacket, FgcomBridge)
- [x] PTT keyboard shortcut (Ctrl+Space) stub
- [x] Sim adapter base interface (SimAdapter Protocol)
- [x] X-Plane stub adapter (XPlane11/12)
- [x] MSFS 2020 stub adapter
- [x] MSFS 2024 stub adapter
- [x] Unit tests for core modules
- [x] Ruff + mypy linting configured

---

## Phase 2 — Sim connectors (priority: MSFS + XP) 🚧 Next

**Goal:** Real live position, altitude, and frequency data from simulators.

### X-Plane 11 / 12
- [ ] UDP datagram receive loop (XPlane UDP protocol, port 49000)
- [ ] Parse RPOS packet for lat/lon/alt/heading/speed
- [ ] Parse COM1/COM2 frequencies from DREF `sim/cockpit2/radios/actuators/*`
- [ ] Push position + frequencies into `AppStateStore` on each cycle (~4 Hz)
- [ ] XP11 vs XP12 version detection and packet variant handling
- [ ] Sim link status chip update
- [ ] Dependency: `xpc3` or raw socket (no external SDK required)

### MSFS 2020
- [ ] SimConnect client via `SimConnect` Python package
- [ ] Subscribe to `PLANE_LATITUDE`, `PLANE_LONGITUDE`, `PLANE_ALTITUDE`, `HEADING_INDICATOR`
- [ ] Subscribe to `COM_ACTIVE_FREQUENCY:1/2`, `COM_STANDBY_FREQUENCY:1/2`
- [ ] Feed real-time position and radio state into `AppStateStore`
- [ ] Handle SimConnect reconnect on sim restart
- [ ] **Dependency blocked:** `SimConnect` Python package (Windows SDK). See [#1](../../issues/1)

### MSFS 2024
- [ ] Verify `SimConnect` SDK version compatibility with MSFS 2024
- [ ] Confirm variable names unchanged vs MSFS 2020 (expected same, verify)
- [ ] Unified MSFS adapter class covering both 2020 and 2024 if API identical
- [ ] **Dependency blocked:** MSFS 2024 SimConnect SDK version confirmation. See [#2](../../issues/2)

### Shared sim work
- [ ] `SimAdapterManager` — auto-detect active sim and activate appropriate adapter
- [ ] Graceful fallback to manual position entry when no sim connected
- [ ] Radio frequency sync: if sim changes COM freq, update `RadioService`
- [ ] Two-way sync: if SkyTrack changes freq, push back to sim via DataRef/SimConnect write

---

## Phase 3 — Voice and FGCom integration 🚧 Planned

**Goal:** Real voice communication via Mumble + FGCom-mumble compatibility.

- [ ] Replace `MockMumbleService` with real Mumble transport
  - Option A: `pymumble` (evaluate maintenance status first)
  - Option B: native helper process using libmumble or stock Mumble + plugin
- [ ] PTT service: low-latency push/release, hardware binding
- [ ] Audio device enumeration with sounddevice or PySide6 audio API
- [ ] FGCom bridge: translate `NormalizedRadioPacket` to FGCom UDP/plugin format
- [ ] FGCom geographic channel separation support
- [ ] Frequency-based channel routing (match fgcom-mumble channel naming)
- [ ] Receive indicator per radio (who is transmitting on active freq)
- [ ] Mute / deafen controls wired to real audio
- [ ] Voice connection diagnostics: ping, jitter, packet loss display
- [ ] **Dependency blocked:** FGCom-mumble plugin UDP format spec. See [#3](../../issues/3)

---

## Phase 4 — Swift network bridge 🚧 Planned

**Goal:** Real SkyHigh network connection via swift-compatible pilot session.

- [ ] Define localhost bridge protocol (JSON-RPC over WebSocket on 127.0.0.1:51001)
- [ ] Build or integrate swift bridge helper process
- [ ] Connect / disconnect with callsign, server, real name
- [ ] Send and receive pilot position updates
- [ ] Text message receive and transmit (unicom, private, ATC)
- [ ] Nearby traffic / controller list from network
- [ ] Flight plan filing form wired to network service
- [ ] Squawk code management
- [ ] **Dependency blocked:** SkyHigh swift bridge process. See [#4](../../issues/4)

---

## Phase 5 — Polish, packaging, and advanced features 🚧 Planned

- [ ] PyInstaller spec file for Windows distribution
- [ ] Windows installer (NSIS or Inno Setup)
- [ ] Light mode theme
- [ ] Dockable / detachable radio panel
- [ ] 8.33 kHz channel spacing full validation and display
- [ ] Dual-watch radio monitoring
- [ ] Radio receive noise / quality simulation
- [ ] ATIS autotuning
- [ ] Aircraft profile presets
- [ ] In-app update checker
- [ ] Linux packaging (AppImage or Flatpak)
- [ ] CI/CD pipeline (GitHub Actions: lint, test, build on push)

---

## Known blocked items (open issues)

| # | Item | Blocker |
|---|---|---|
| 1 | MSFS 2020 SimConnect adapter | `SimConnect` Python SDK, Windows-only install |
| 2 | MSFS 2024 SimConnect adapter | SDK version compatibility confirmation required |
| 3 | FGCom UDP bridge | FGCom-mumble plugin port / message format spec |
| 4 | Swift network bridge | SkyHigh-compatible swift bridge helper process |
| 5 | Real Mumble voice transport | Mumble library maintenance / native helper decision |
