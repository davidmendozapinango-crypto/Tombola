"""SDG (ODS) data helpers (non-OOP)."""

import random
from typing import List, Tuple

from src.config import COLOR_SDG, SDG_NAMES, SDG_SLOGANS


def list_sdg_ids() -> List[int]:
    """Return the list of available SDG identifiers."""
    return list(SDG_NAMES.keys())


def get_sdg_name(sdg_id: int) -> str:
    """Return the Spanish name for an SDG."""
    return SDG_NAMES.get(sdg_id, "ODS desconocido")


def get_sdg_color(sdg_id: int) -> Tuple[int, int, int]:
    """Return the brand color for an SDG."""
    return COLOR_SDG.get(sdg_id, (100, 100, 100))


def get_sdg_slogan(sdg_id: int) -> str:
    """Return the slogan for an SDG."""
    return SDG_SLOGANS.get(sdg_id, "")


def random_slogan(sdg_id: int) -> str:
    """Return the slogan for the selected SDG."""
    return get_sdg_slogan(sdg_id)
