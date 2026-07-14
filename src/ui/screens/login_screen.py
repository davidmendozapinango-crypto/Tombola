"""Login screen (non-OOP)."""

from typing import Any, Dict

import pygame

from src.auth.session import login
from src.config import (
    COLOR_CHARCOAL,
    COLOR_MINT,
    COLOR_PINE,
    WINDOW_HEIGHT,
    WINDOW_WIDTH,
)
from src.persistence.players import ensure_default_players, find_player, load_players
from src.ui.app_state import cycle_focus, get_focused, is_focused, set_error, set_info
from src.ui.common import draw_button, draw_error_message, draw_input, draw_text


def _layout() -> Dict[str, pygame.Rect]:
    """Return the UI rectangles for the login screen."""
    center_x = WINDOW_WIDTH // 2
    y = 220
    return {
        "id": pygame.Rect(center_x - 150, y, 300, 40),
        "key": pygame.Rect(center_x - 150, y + 60, 300, 40),
        "login": pygame.Rect(center_x - 150, y + 130, 300, 45),
        "register": pygame.Rect(center_x - 150, y + 190, 145, 45),
        "exit": pygame.Rect(center_x + 5, y + 190, 145, 45),
    }


def init_login(state: Dict[str, Any]) -> None:
    """Initialize login screen state."""
    state["inputs"] = {"id": "", "key": ""}
    state["focusable"] = ["id", "key", "login", "register", "exit"]
    state["focus_index"] = 0
    state["rects"] = _layout()
    state["players"] = ensure_default_players()


def _try_login(state: Dict[str, Any]) -> str:
    """Validate credentials and return the next screen name."""
    player_id = state["inputs"].get("id", "").strip()
    access_key = state["inputs"].get("key", "").strip()

    if not player_id or not access_key:
        set_error(state, "Ingrese cedula y clave.")
        return "login"

    players = load_players()
    player = find_player(players, player_id)
    if player is None:
        set_error(state, "Jugador no registrado.")
        return "login"

    if player.get("access_key", "") != access_key:
        set_error(state, "Clave incorrecta.")
        return "login"

    login(state["session"], player)
    set_info(state, f"Bienvenido, {player['full_name']}")
    return "menu"


def handle_event(state: Dict[str, Any], event: pygame.event.Event) -> str:
    """Process a Pygame event and return the next screen name."""
    rects = state.get("rects") or _layout()
    state["rects"] = rects
    focused = get_focused(state)

    if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
        for name, rect in rects.items():
            if rect.collidepoint(event.pos):
                if name in state["focusable"]:
                    state["focus_index"] = state["focusable"].index(name)
                if name in ("login", "register", "exit"):
                    if name == "login":
                        return _try_login(state)
                    if name == "register":
                        return "register"
                    if name == "exit":
                        state["running"] = False
                        return "exit"
                return state["current_screen"]

    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_TAB:
            cycle_focus(state, 1)
            return state["current_screen"]
        if event.key == pygame.K_ESCAPE:
            state["running"] = False
            return "exit"
        if event.key in (pygame.K_RETURN, pygame.K_SPACE):
            if focused == "login":
                return _try_login(state)
            if focused == "register":
                return "register"
            if focused == "exit":
                state["running"] = False
                return "exit"
            return state["current_screen"]
        if focused in ("id", "key"):
            if event.key == pygame.K_BACKSPACE:
                state["inputs"][focused] = state["inputs"][focused][:-1]
            elif event.unicode.isprintable() and len(event.unicode) == 1:
                state["inputs"][focused] += event.unicode

    return state["current_screen"]


def draw(surface: pygame.Surface, state: Dict[str, Any]) -> None:
    """Render the login screen."""
    surface.fill(COLOR_MINT)
    rects = _layout()
    state["rects"] = rects

    draw_text(
        surface,
        "Tombola - ODS",
        (WINDOW_WIDTH // 2, 80),
        font_size=48,
        color=COLOR_PINE,
        center=True,
    )
    draw_text(
        surface,
        "Inicio de sesion",
        (WINDOW_WIDTH // 2, 150),
        font_size=32,
        color=COLOR_CHARCOAL,
        center=True,
    )

    mouse_pos = pygame.mouse.get_pos()

    draw_text(surface, "Cedula:", (rects["id"].x, rects["id"].y - 25), font_size=20)
    draw_input(
        surface,
        state["inputs"].get("id", ""),
        rects["id"],
        focused=is_focused(state, "id"),
    )

    draw_text(surface, "Clave:", (rects["key"].x, rects["key"].y - 25), font_size=20)
    draw_input(
        surface,
        state["inputs"].get("key", ""),
        rects["key"],
        focused=is_focused(state, "key"),
        mask=True,
    )

    hovered = {name: rect.collidepoint(mouse_pos) for name, rect in rects.items()}
    focused = get_focused(state)
    draw_button(
        surface,
        "Ingresar",
        rects["login"],
        hovered=hovered["login"],
        focused=focused == "login",
    )
    draw_button(
        surface,
        "Registrarse",
        rects["register"],
        hovered=hovered["register"],
        focused=focused == "register",
    )
    draw_button(
        surface,
        "Salir",
        rects["exit"],
        hovered=hovered["exit"],
        focused=focused == "exit",
    )

    if state.get("error_message"):
        draw_error_message(
            surface,
            state["error_message"],
            (WINDOW_WIDTH // 2, WINDOW_HEIGHT - 90),
            font_size=20,
        )
