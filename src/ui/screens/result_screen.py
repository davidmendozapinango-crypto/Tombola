"""Game result screen (non-OOP)."""

from typing import Any, Dict

import pygame

from src.config import (
    COLOR_CHARCOAL,
    COLOR_MINT,
    COLOR_PINE,
    WINDOW_HEIGHT,
    WINDOW_WIDTH,
)
from src.core.card import card_sum
from src.ods.data import get_sdg_color, get_sdg_name
from src.ui.app_state import cycle_focus, get_focused
from src.ui.common import draw_button, draw_text


def _layout() -> Dict[str, pygame.Rect]:
    """Return the UI rectangles for the result screen."""
    center_x = WINDOW_WIDTH // 2
    y = 520
    return {
        "play_again": pygame.Rect(center_x - 150, y, 145, 45),
        "menu": pygame.Rect(center_x + 5, y, 145, 45),
    }


def init_result(state: Dict[str, Any]) -> None:
    """Initialize result screen state."""
    state["inputs"] = {}
    state["focusable"] = ["play_again", "menu"]
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
            return "menu"
        if event.key in (pygame.K_RETURN, pygame.K_SPACE):
            return _activate(state, focused)

    return state["current_screen"]


def _activate(state: Dict[str, Any], name: str) -> str:
    """Activate a result screen option."""
    if name == "play_again":
        return "config"
    if name == "menu":
        return "menu"
    return state["current_screen"]


def draw(surface: pygame.Surface, state: Dict[str, Any]) -> None:
    """Render the result screen."""
    surface.fill(COLOR_MINT)
    rects = _layout()
    state["rects"] = rects
    session = state["session"]

    sdg_id = session.get("sdg_id", 1)
    sdg_color = get_sdg_color(sdg_id)
    winner = session.get("winning_card", "")
    winning_card = (
        session["main_card"] if winner == "main" else session["complement_card"]
    )
    winning_sum = card_sum(winning_card)

    draw_text(
        surface,
        "Resultado de la partida",
        (WINDOW_WIDTH // 2, 80),
        font_size=40,
        color=sdg_color,
        center=True,
    )
    draw_text(
        surface,
        "GANADOR",
        (WINDOW_WIDTH // 2, 160),
        font_size=48,
        color=COLOR_PINE,
        center=True,
    )
    draw_text(
        surface,
        f"Carton ganador: {winner.upper()}",
        (WINDOW_WIDTH // 2, 230),
        font_size=28,
        color=COLOR_CHARCOAL,
        center=True,
    )
    draw_text(
        surface,
        f"Suma de celdas del carton ganador: {winning_sum}",
        (WINDOW_WIDTH // 2, 290),
        font_size=24,
        color=COLOR_CHARCOAL,
        center=True,
    )
    draw_text(
        surface,
        f"Tema ODS: {get_sdg_name(sdg_id)}",
        (WINDOW_WIDTH // 2, 350),
        font_size=24,
        color=COLOR_CHARCOAL,
        center=True,
    )
    draw_text(
        surface,
        f"Numeros sorteados: {len(session.get('drawn_numbers', []))}",
        (WINDOW_WIDTH // 2, 410),
        font_size=22,
        color=COLOR_CHARCOAL,
        center=True,
    )

    mouse_pos = pygame.mouse.get_pos()
    hovered = {name: rect.collidepoint(mouse_pos) for name, rect in rects.items()}
    focused = get_focused(state)
    draw_button(
        surface,
        "Jugar de nuevo",
        rects["play_again"],
        hovered=hovered["play_again"],
        focused=focused == "play_again",
    )
    draw_button(
        surface,
        "Menu",
        rects["menu"],
        hovered=hovered["menu"],
        focused=focused == "menu",
    )
