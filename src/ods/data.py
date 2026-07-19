"""Utilidades para acceder a datos relacionados con ODS (SDG)."""

import random
from typing import List, Tuple
from src.config import COLOR_SDG, SDG_MESSAGES, SDG_NAMES, SDG_SLOGANS


def list_sdg_ids() -> List[int]:
    """Devolver la lista de identificadores SDG disponibles."""
    return list(SDG_NAMES.keys())


def get_sdg_name(sdg_id: int) -> str:
    """Obtener el nombre (en español) de un SDG por su id."""
    return SDG_NAMES.get(sdg_id, "ODS desconocido")


def get_sdg_color(sdg_id: int) -> Tuple[int, int, int]:
    """Obtener el color de marca asociado a un SDG.

    Devuelve un color RGB por defecto si no existe el id.
    """
    return COLOR_SDG.get(sdg_id, (100, 100, 100))


def get_sdg_slogan(sdg_id: int) -> str:
    """Obtener el lema asociado a un SDG."""
    return SDG_SLOGANS.get(sdg_id, "")


def random_slogan(sdg_id: int) -> str:
    """Alias: obtener el lema (slogan) del SDG seleccionado."""
    return get_sdg_slogan(sdg_id)


def get_sdg_message(sdg_id: int) -> str:
    """Obtener un mensaje aleatorio alusivo al SDG."""
    messages = SDG_MESSAGES.get(sdg_id, [""])
    return random.choice(messages)


def get_sdg_messages(sdg_id: int) -> list[str]:
    """Devolver todos los mensajes alusivos asociados a un SDG."""
    return SDG_MESSAGES.get(sdg_id, [""])
