"""Network service Protocol contract.

Any real network implementation (swift bridge, FSD direct) must satisfy this interface.
"""
from __future__ import annotations

from typing import Protocol

from skytrack.core.models import SessionProfile


class NetworkService(Protocol):
    """Minimal contract for network connectivity."""

    async def connect(self, session: SessionProfile) -> None:
        """Establish a pilot session on the SkyHigh network."""
        ...

    async def disconnect(self) -> None:
        """Gracefully close the pilot session."""
        ...

    async def send_text(self, target: str, message: str) -> None:
        """Send a text message to *target* (callsign, channel, or frequency)."""
        ...
