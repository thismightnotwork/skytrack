"""Radio service: manages COM1/COM2 state and drives FGCom bridge updates."""
from __future__ import annotations

from dataclasses import replace

from loguru import logger

from skytrack.core.models import AppState, RadioState
from skytrack.core.state import AppStateStore
from skytrack.services.radio.fgcom_bridge import FgcomBridge
from skytrack.services.radio.radio_model import FrequencyValidator, NormalizedRadioPacket


class RadioService:
    """Domain service for all radio stack operations.

    Deliberately has no Qt dependency — testable without QApplication.
    """

    def __init__(self, store: AppStateStore, bridge: FgcomBridge) -> None:
        self.store = store
        self.bridge = bridge

    # --- Frequency management ---

    def set_frequency(self, radio_name: str, field: str, value: str) -> None:
        """Validate and apply a frequency change to active or standby."""
        normalized = FrequencyValidator.normalize(value)
        radio = self._get_radio(radio_name)
        updated = replace(radio, **{field: normalized})
        self._set_radio(updated)
        logger.info(f"{radio_name} {field} set to {normalized}")

    def swap(self, radio_name: str) -> None:
        """Swap active and standby frequencies for *radio_name*."""
        radio = self._get_radio(radio_name)
        updated = replace(radio, active=radio.standby, standby=radio.active)
        self._set_radio(updated)
        logger.info(f"{radio_name} swapped: active={updated.active} standby={updated.standby}")

    # --- Toggle controls ---

    def set_toggle(self, radio_name: str, attr: str, value: bool) -> None:
        """Set a boolean attribute (power, monitor, transmitting, receiving)."""
        radio = self._get_radio(radio_name)
        self._set_radio(replace(radio, **{attr: value}))

    def set_volume(self, radio_name: str, volume: int) -> None:
        """Set volume (0–100) for *radio_name*."""
        volume = max(0, min(100, volume))
        radio = self._get_radio(radio_name)
        self._set_radio(replace(radio, volume=volume))

    # --- FGCom bridge publish ---

    async def publish_snapshot(self, app_state: AppState) -> None:
        """Emit current radio + position state to the FGCom bridge."""
        for radio in [app_state.com1, app_state.com2]:
            packet = NormalizedRadioPacket(
                callsign=app_state.session.callsign,
                radio=radio.name,
                active_freq=radio.active,
                standby_freq=radio.standby,
                tx=radio.transmitting,
                rx=radio.receiving,
                monitoring=radio.monitor,
                lat=app_state.position.lat,
                lon=app_state.position.lon,
                altitude_ft=app_state.position.altitude_ft,
                source=app_state.position.source,
            )
            await self.bridge.push_radio_state(packet)

    # --- Helpers ---

    def _get_radio(self, name: str) -> RadioState:
        return self.store.state.com1 if name == "COM1" else self.store.state.com2

    def _set_radio(self, radio: RadioState) -> None:
        if radio.name == "COM1":
            self.store.update(com1=radio)
        else:
            self.store.update(com2=radio)
