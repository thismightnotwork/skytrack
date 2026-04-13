"""Radio state models and frequency validation.

This module is isolated from Qt and I/O so it is fully unit-testable.
"""
from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True)
class NormalizedRadioPacket:
    """Canonical radio state snapshot emitted towards FGCom bridge or network."""

    callsign: str
    radio: str           # 'COM1' | 'COM2'
    active_freq: str     # '118.000'
    standby_freq: str
    tx: bool
    rx: bool
    monitoring: bool
    lat: float
    lon: float
    altitude_ft: int
    source: str = "manual"  # sim source identifier


class FrequencyValidator:
    """VHF COM frequency validation and normalisation."""

    VHF_MIN = 118.0
    VHF_MAX = 136.9917

    # 8.33 kHz channel spacing valid channel spacing values (last 3 digits)
    # A simplified check — expand for strict 8.33 validation
    _833_VALID_LAST3 = {
        "000", "005", "010", "015", "025", "030", "035", "040",
        "050", "055", "060", "065", "075", "080", "085", "090",
        "100", "105", "110", "115", "125", "130", "135", "140",
        "150", "155", "160", "165", "175", "180", "185", "190",
        "200", "205", "210", "215", "225", "230", "235", "240",
        "250", "255", "260", "265", "275", "280", "285", "290",
        "300", "305", "310", "315", "325", "330", "335", "340",
        "350", "355", "360", "365", "375", "380", "385", "390",
        "400", "405", "410", "415", "425", "430", "435", "440",
        "450", "455", "460", "465", "475", "480", "485", "490",
        "500", "505", "510", "515", "525", "530", "535", "540",
        "550", "555", "560", "565", "575", "580", "585", "590",
        "600", "605", "610", "615", "625", "630", "635", "640",
        "650", "655", "660", "665", "675", "680", "685", "690",
        "700", "705", "710", "715", "725", "730", "735", "740",
        "750", "755", "760", "765", "775", "780", "785", "790",
        "800", "805", "810", "815", "825", "830", "835", "840",
        "850", "855", "860", "865", "875", "880", "885", "890",
        "900", "905", "910", "915", "925", "930", "935", "940",
        "950", "955", "960", "965", "975", "980", "985", "990",
    }

    @classmethod
    def normalize(cls, value: str, strict_833: bool = False) -> str:
        """Return a normalised frequency string 'NNN.NNN' or raise ValueError."""
        raw = value.strip()
        if not raw:
            raise ValueError("Frequency cannot be empty")
        try:
            numeric = float(raw)
        except ValueError:
            raise ValueError(f"Invalid frequency value: {raw!r}")
        if not (cls.VHF_MIN <= numeric <= cls.VHF_MAX):
            raise ValueError(
                f"Frequency {numeric:.3f} outside VHF COM band "
                f"({cls.VHF_MIN}–{cls.VHF_MAX} MHz)"
            )
        formatted = f"{numeric:.3f}"
        if strict_833:
            last3 = formatted.split(".")[1]
            if last3 not in cls._833_VALID_LAST3:
                raise ValueError(f"Frequency {formatted} is not a valid 8.33 kHz channel")
        return formatted
