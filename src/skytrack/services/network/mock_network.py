"""Mock network service backed by SwiftBridgeClient stub.

Used in MVP until a real swift bridge process is available.
Replace by injecting a SwiftBridgeClient with a real transport.
"""
from __future__ import annotations

import asyncio

from loguru import logger

from skytrack.core.events import EventBus
from skytrack.core.models import ConnectionState, MessageEntry, SessionProfile
from skytrack.core.state import AppStateStore
from skytrack.services.network.swift_bridge import SwiftBridgeClient


class MockNetworkService:
    """[MOCK] Simulates connect/disconnect/send with artificial delays."""

    def __init__(
        self,
        store: AppStateStore,
        bus: EventBus,
        bridge: SwiftBridgeClient,
    ) -> None:
        self.store = store
        self.bus = bus
        self.bridge = bridge

    async def connect(self, session: SessionProfile) -> None:
        logger.info(f"Network connecting: {session.callsign}@{session.server}")
        self.store.update(network_state=ConnectionState.CONNECTING)
        self.store.append_message(
            MessageEntry("network", f"Connecting {session.callsign} → {session.server}")
        )
        await asyncio.sleep(0.6)
        await self.bridge.connect(session.callsign, session.server)
        self.store.update(network_state=ConnectionState.CONNECTED)
        self.store.append_message(
            MessageEntry("network", f"Session active: {session.callsign} on {session.server}")
        )

    async def disconnect(self) -> None:
        logger.info("Network disconnecting")
        await asyncio.sleep(0.2)
        await self.bridge.disconnect()
        self.store.update(network_state=ConnectionState.DISCONNECTED)
        self.store.append_message(
            MessageEntry("network", "Disconnected from SkyHigh network", "warn")
        )

    async def send_text(self, target: str, message: str) -> None:
        if not message.strip():
            return
        callsign = self.store.state.session.callsign
        await self.bridge.send_text(target, message, callsign)
        self.store.append_message(
            MessageEntry("text", f"➜ {target}: {message}")
        )
