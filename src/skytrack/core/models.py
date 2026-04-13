"""Pure data models for application state. No Qt, no I/O."""
from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Literal


class ConnectionState(str, Enum):
    """Lifecycle states for any external connection (network, voice, sim)."""

    DISCONNECTED = "disconnected"
    CONNECTING = "connecting"
    CONNECTED = "connected"
    DEGRADED = "degraded"


@dataclass(slots=True)
class SessionProfile:
    """Pilot identity for the current session."""

    callsign: str = "SKY123"
    server: str = "dev.skyhigh.local"
    real_name: str = "Pilot"


@dataclass(slots=True)
class AudioDeviceState:
    """Selected audio devices and PTT configuration."""

    input_device: str = "Default Microphone"
    output_device: str = "Default Headset"
    ptt_key: str = "CTRL+SPACE"
    muted: bool = False
    deafened: bool = False


@dataclass(slots=True)
class RadioState:
    """State for a single VHF COM radio."""

    name: Literal["COM1", "COM2"]
    active: str = "118.000"
    standby: str = "121.800"
    volume: int = 75
    power: bool = True
    monitor: bool = False
    transmitting: bool = False
    receiving: bool = False


@dataclass(slots=True)
class AircraftPosition:
    """Live aircraft position received from a simulator adapter."""

    lat: float = 51.4706   # Gatwick default
    lon: float = -0.4619
    altitude_ft: int = 0
    heading_deg: float = 0.0
    groundspeed_kt: float = 0.0
    source: str = "manual"  # 'xplane11' | 'xplane12' | 'msfs2020' | 'msfs2024' | 'manual'


@dataclass(slots=True)
class MessageEntry:
    """A single entry in the event log."""

    source: str
    text: str
    level: Literal["info", "warn", "error"] = "info"


@dataclass(slots=True)
class AppState:
    """Immutable snapshot of the full application state."""

    session: SessionProfile = field(default_factory=SessionProfile)
    network_state: ConnectionState = ConnectionState.DISCONNECTED
    voice_state: ConnectionState = ConnectionState.DISCONNECTED
    sim_link_state: ConnectionState = ConnectionState.DISCONNECTED
    active_sim: str = "none"  # 'xplane11' | 'xplane12' | 'msfs2020' | 'msfs2024' | 'none'
    audio: AudioDeviceState = field(default_factory=AudioDeviceState)
    com1: RadioState = field(default_factory=lambda: RadioState(name="COM1"))
    com2: RadioState = field(
        default_factory=lambda: RadioState(
            name="COM2", active="121.900", standby="122.800"
        )
    )
    messages: list[MessageEntry] = field(default_factory=list)
    nearby: list[str] = field(default_factory=lambda: ["EGKK_TWR", "EGLL_APP", "BAW402"])
    position: AircraftPosition = field(default_factory=AircraftPosition)
