"""Typed application configuration with JSON persistence and env overrides.

Settings are loaded from ~/.skytrack/settings.json on start.
Environment variables override values using the SKYTRACK__ prefix.
See .env.example for available overrides. Never commit .env or secrets.
"""
from __future__ import annotations

from pathlib import Path

from pydantic import BaseModel, Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class WindowSettings(BaseModel):
    width: int = 1520
    height: int = 940
    theme: str = "dark"


class NetworkSettings(BaseModel):
    default_server: str = "dev.skyhigh.local"
    swift_bridge_mode: str = "helper-process"
    bridge_host: str = "127.0.0.1"
    bridge_port: int = 51001


class VoiceSettings(BaseModel):
    mumble_host: str = "voice.skyhigh.local"
    mumble_port: int = 64738
    channel: str = "fgcom-mumble"


class SimSettings(BaseModel):
    xplane_host: str = "127.0.0.1"
    xplane_udp_port: int = 49000
    xplane_beacon_port: int = 49001
    # SimConnect is auto-discovered on Windows; no host/port required.
    preferred_sim: str = "auto"  # 'auto' | 'xplane11' | 'xplane12' | 'msfs2020' | 'msfs2024' | 'none'


class SkyTrackSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_prefix="SKYTRACK_",
        env_nested_delimiter="__",
    )

    profile: str = "dev"
    window: WindowSettings = Field(default_factory=WindowSettings)
    network: NetworkSettings = Field(default_factory=NetworkSettings)
    voice: VoiceSettings = Field(default_factory=VoiceSettings)
    sim: SimSettings = Field(default_factory=SimSettings)

    @classmethod
    def config_dir(cls) -> Path:
        return Path.home() / ".skytrack"

    @classmethod
    def config_path(cls) -> Path:
        return cls.config_dir() / "settings.json"

    def save(self) -> None:
        """Persist settings to ~/.skytrack/settings.json."""
        self.config_dir().mkdir(parents=True, exist_ok=True)
        self.config_path().write_text(self.model_dump_json(indent=2), encoding="utf-8")

    @classmethod
    def load(cls) -> "SkyTrackSettings":
        """Load from disk, falling back to defaults and saving if missing."""
        path = cls.config_path()
        if path.exists():
            return cls.model_validate_json(path.read_text(encoding="utf-8"))
        settings = cls()
        settings.save()
        return settings
