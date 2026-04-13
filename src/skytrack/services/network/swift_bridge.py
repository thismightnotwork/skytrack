"""Swift-compatible helper-process bridge boundary.

Architecture decision: SkyTrack communicates with a local swift helper process
rather than embedding swift internals in Python. The helper exposes a
JSON-RPC or WebSocket API on localhost:51001 by default.

TODO (blocked — see GitHub issue #4):
  - Implement real asyncio WebSocket or JSON-RPC client
  - Define message schema: connect, disconnect, position, text, flightplan, traffic
  - Handle reconnect with exponential back-off
  - Integrate with SkyHigh-specific swift configuration
"""
from __future__ import annotations

from dataclasses import dataclass

from loguru import logger


@dataclass(slots=True)
class SwiftBridgeConfig:
    mode: str = "helper-process"  # 'helper-process' | 'direct-fsd' (future)
    host: str = "127.0.0.1"
    port: int = 51001


class SwiftBridgeClient:
    """Stub bridge client. Replace with real WebSocket/JSON-RPC client.

    When implementing:
    1. Open asyncio WebSocket connection to ws://{host}:{port}/v1/rpc
    2. Send JSON-encoded commands; receive JSON responses and events
    3. Map network events to AppStateStore updates via EventBus
    """

    def __init__(self, config: SwiftBridgeConfig) -> None:
        self.config = config
        logger.debug("SwiftBridgeClient initialised (stub mode, not connected)")

    async def connect(self, callsign: str, server: str) -> dict[str, object]:
        """Stub: returns mock success. Replace with real bridge call."""
        logger.info(f"[STUB] swift bridge connect: callsign={callsign} server={server}")
        return {"ok": True, "mode": self.config.mode, "callsign": callsign, "server": server}

    async def disconnect(self) -> dict[str, object]:
        """Stub: returns mock success. Replace with real bridge call."""
        logger.info("[STUB] swift bridge disconnect")
        return {"ok": True}

    async def send_text(
        self, target: str, message: str, sender: str
    ) -> dict[str, object]:
        """Stub: logs text. Replace with real bridge call."""
        logger.info(f"[STUB] swift bridge text: {sender} -> {target}: {message}")
        return {"ok": True}
