"""Gestión del estado global de la aplicación (helpers no OOP).

Descripción:
    Mantiene una estructura de estado común usada por la UI: pantalla
    actual, sesión, mensajes transitorios, listas de jugadores/juegos y
    control de foco para navegación por teclado.
"""

from typing import Any, Dict
from src.auth.session import make_session


def make_app_state() -> Dict[str, Any]:
    """Crear el diccionario de estado global inicial de la aplicación.

    Campos clave:
        - current_screen: nombre de la pantalla activa.
        - running: indicador de ejecución principal.
        - session: sesión activa creada por `make_session`.
        - players/games: listas de entidades cargadas en memoria.
        - inputs/focusable/focus_index: estado para controles y foco de teclado.
    """
    return {
        "current_screen": "login",
        "running": True,
        "session": make_session(),
        "players": [],
        "games": [],
        "error_message": "",
        "info_message": "",
        "inputs": {},
        "focus_index": 0,
        "focusable": [],
    }


def set_screen(state: Dict[str, Any], screen_name: str) -> None:
    """Cambiar la pantalla activa y limpiar mensajes transitorios."""
    state["current_screen"] = screen_name
    state["error_message"] = ""
    state["info_message"] = ""
    state["inputs"] = {}
    state["focus_index"] = 0
    state["focusable"] = []


def set_error(state: Dict[str, Any], message: str) -> None:
    """Establecer un mensaje de error transitorio."""
    state["error_message"] = message


def set_info(state: Dict[str, Any], message: str) -> None:
    """Establecer un mensaje informativo transitorio."""
    state["info_message"] = message


def cycle_focus(state: Dict[str, Any], direction: int = 1) -> None:
    """Mover el foco de teclado en la dirección indicada (1 o -1)."""
    focusable = state.get("focusable") or []
    if not focusable:
        return
    state["focus_index"] = (state["focus_index"] + direction) % len(focusable)


def get_focused(state: Dict[str, Any]) -> str:
    """Devolver el nombre del control actualmente enfocado.

    Devuelve cadena vacía si no hay controles enfocables registrados.
    """
    focusable = state.get("focusable") or []
    if not focusable:
        return ""
    return focusable[state["focus_index"]]


def is_focused(state: Dict[str, Any], name: str) -> bool:
    """Indica si el control `name` es el actualmente enfocado."""
    return get_focused(state) == name
