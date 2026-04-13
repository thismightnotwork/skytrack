"""FGCom-mumble bridge boundary.

This module translates NormalizedRadioPackets from RadioService into
FGCom-mumble-compatible messages and delivers them to the plugin.

TODO (blocked — see GitHub issue #3):
  - Implement UDP socket send to fgcom-mumble plugin listener (default port 16661)
  - Translate NormalizedRadioPacket fields to FGCom UDP packet format:
      CALLSIGN=SKY123,COM1_FRQ=118.000,COM1_TX=1,COM1_RX=1,LAT=51.47,LON=-0.46,ALT=0
  - Handle send failures gracefully; log and continue — never crash voice state
  - Consider helper-process approach if direct UDP is insufficient for plugin integration

References:
  https://github.com/hbeni/fgcom-mumble
  integrations/fgcom/README.md
"""
from __future__ import annotations

from loguru import logger

from skytrack.services.radio.radio_model import NormalizedRadioPacket


class FgcomBridge:
    """[STUB] FGCom-mumble bridge. Replace push_radio_state with real UDP send."""

    async def push_radio_state(self, packet: NormalizedRadioPacket) -> None:
        """Emit radio state to the FGCom-mumble plugin.

        Currently a no-op stub. When implemented:
          1. Format packet as FGCom UDP string
          2. Send to 127.0.0.1:16661 via asyncio UDP socket
          3. Log send failures at WARNING level
        """
        logger.debug(
            f"[STUB] FGCom push: {packet.radio} active={packet.active_freq} "
            f"tx={packet.tx} rx={packet.rx} lat={packet.lat:.4f} lon={packet.lon:.4f}"
        )
