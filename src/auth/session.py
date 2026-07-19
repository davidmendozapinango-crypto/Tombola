"""
Helpers para el estado de sesión (no-OOP).

Descripción:
  Provee funciones simples para crear y manipular un diccionario `session`
  que almacena el jugador autenticado, cartones, estado de juego y marcaciones.
"""

from typing import Any, Dict, Optional


def make_session() -> Dict[str, Any]:
    """Crear el diccionario de sesión inicial con campos por defecto.

    Returns:
        Dict[str, Any]: Estructura de sesión vacía lista para usarse.
    """
    return {
        "player": None,
        "main_card": None,
        "complement_card": None,
        "dimension": None,
        "sdg_id": None,
        "drawn_numbers": [],
        "marked_main": set(),
        "marked_complement": set(),
        "winning_card": None,
        "game_over": False,
    }


def login(session: Dict[str, Any], player: Dict[str, Any]) -> Dict[str, Any]:
    """Almacena el registro del jugador autenticado en la sesión.

    Args:
        session: Diccionario de sesión (mutado in-place).
        player: Registro del jugador autenticado.

    Returns:
        Dict[str, Any]: La misma sesión actualizada.
    """
    session["player"] = player
    return session


def logout(session: Dict[str, Any]) -> Dict[str, Any]:
    """Limpia la sesión y devuelve una sesión nueva por defecto."""
    session.clear()
    return make_session()


def get_player(session: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    """Return the current player or None."""
    return session.get("player")


def is_authenticated(session: Dict[str, Any]) -> bool:
    """Return True if a player is logged in."""
    return session.get("player") is not None
