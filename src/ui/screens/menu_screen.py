"""Main menu screen (non-OOP)."""

from typing import Any, Dict

import pygame

from src.auth.session import get_player, logout
from src.config import (
    COLOR_CHARCOAL,
    COLOR_MINT,
    COLOR_PINE,
    WINDOW_HEIGHT,
    WINDOW_WIDTH,
)
from src.ui.app_state import cycle_focus, get_focused
from src.ui.common import draw_button, draw_error_message, draw_text


def _layout() -> Dict[str, pygame.Rect]:
    """Return the UI rectangles for the menu screen."""
    center_x = WINDOW_WIDTH // 2
    y = 260
    return {
        "play": pygame.Rect(center_x - 140, y, 280, 45),
        "reports": pygame.Rect(center_x - 140, y + 60, 280, 45),
        "calculator": pygame.Rect(center_x - 140, y + 120, 280, 45),
        "logout": pygame.Rect(center_x - 140, y + 180, 280, 45),
        "exit": pygame.Rect(center_x - 140, y + 240, 280, 45),
    }


# Placeholder until draw_info_message is defined in common.
from src.ui.common import draw_text as _draw_text


def _draw_info_message(surface, message, position, font_size=20):
    _draw_text(surface, message, position, font_size=font_size, color=COLOR_PINE)


def init_menu(state: Dict[str, Any]) -> None:
    """Initialize menu screen state."""
    state["inputs"] = {}
    state["focusable"] = ["play", "reports", "calculator", "logout", "exit"]
    state["focus_index"] = 0
    state["rects"] = _layout()


def handle_event(state: Dict[str, Any], event: pygame.event.Event) -> str:
    """Process a Pygame event and return the next screen name."""
    rects = state.get("rects") or _layout()
    state["rects"] = rects
    focused = get_focused(state)

    if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
        for name, rect in rects.items():
            if rect.collidepoint(event.pos):
                state["focus_index"] = state["focusable"].index(name)
                return _activate(state, name)

    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_TAB:
            cycle_focus(state, 1)
            return state["current_screen"]
        if event.key == pygame.K_ESCAPE:
            logout(state["session"])
            return "login"
        if event.key in (pygame.K_RETURN, pygame.K_SPACE):
            return _activate(state, focused)

    return state["current_screen"]


def _activate(state: Dict[str, Any], name: str) -> str:
    """Activate a menu option."""
    if name == "play":
        return "config"
    if name == "reports":
        return "reports"
    if name == "calculator":
        return "calculator"
    if name == "logout":
        logout(state["session"])
        return "login"
    if name == "exit":
        state["running"] = False
        return "exit"
    return state["current_screen"]


def draw(surface: pygame.Surface, state: Dict[str, Any]) -> None:
    """Render the main menu screen."""
    surface.fill(COLOR_MINT)
    rects = _layout()
    state["rects"] = rects

    player = get_player(state["session"])
    welcome = f"Bienvenido, {player['full_name']}" if player else "Bienvenido"
    draw_text(
        surface,
        welcome,
        (WINDOW_WIDTH // 2, 80),
        font_size=36,
        color=COLOR_PINE,
        center=True,
    )
    draw_text(
        surface,
        "Menu principal",
        (WINDOW_WIDTH // 2, 150),
        font_size=28,
        color=COLOR_CHARCOAL,
        center=True,
    )

    mouse_pos = pygame.mouse.get_pos()
    hovered = {name: rect.collidepoint(mouse_pos) for name, rect in rects.items()}
    focused = get_focused(state)

    draw_button(
        surface,
        "Jugar",
        rects["play"],
        hovered=hovered["play"],
        focused=focused == "play",
    )
    draw_button(
        surface,
        "Reportes",
        rects["reports"],
        hovered=hovered["reports"],
        focused=focused == "reports",
    )
    draw_button(
        surface,
        "Demo calculadora",
        rects["calculator"],
        hovered=hovered["calculator"],
        focused=focused == "calculator",
    )
    draw_button(
        surface,
        "Cerrar sesion",
        rects["logout"],
        hovered=hovered["logout"],
        focused=focused == "logout",
    )
    draw_button(
        surface,
        "Salir",
        rects["exit"],
        hovered=hovered["exit"],
        focused=focused == "exit",
    )

    if state.get("info_message"):
        _draw_info_message(
            surface,
            state["info_message"],
            (WINDOW_WIDTH // 2, WINDOW_HEIGHT - 90),
            font_size=20,
        )
    if state.get("error_message"):
        draw_error_message(
            surface,
            state["error_message"],
            (WINDOW_WIDTH // 2, WINDOW_HEIGHT - 60),
            font_size=20,
        )
