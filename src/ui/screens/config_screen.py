"""Card configuration screen (non-OOP)."""

from typing import Any, Dict

import pygame

from src.config import (
    COLOR_CHARCOAL,
    COLOR_MINT,
    COLOR_PINE,
    COLOR_WHITE,
    WINDOW_HEIGHT,
    WINDOW_WIDTH,
)
from src.core.card import make_cards
from src.core.card_figures import get_card_type, get_figure_pattern
from src.ods.data import get_sdg_color, get_sdg_name, list_sdg_ids
from src.ui.app_state import cycle_focus, get_focused
from src.ui.common import draw_button, draw_error_message, draw_text


def _layout() -> Dict[str, pygame.Rect]:
    """Return the UI rectangles for the configuration screen."""
    center_x = WINDOW_WIDTH // 2
    y = 240
    return {
        "dim_left": pygame.Rect(center_x - 170, y, 60, 40),
        "dim_value": pygame.Rect(center_x - 100, y, 200, 40),
        "dim_right": pygame.Rect(center_x + 110, y, 60, 40),
        "sdg_left": pygame.Rect(center_x - 170, y + 80, 60, 40),
        "sdg_value": pygame.Rect(center_x - 100, y + 80, 200, 40),
        "sdg_right": pygame.Rect(center_x + 110, y + 80, 60, 40),
        "continue": pygame.Rect(center_x - 150, y + 180, 145, 45),
        "back": pygame.Rect(center_x + 5, y + 180, 145, 45),
    }


def _dimensions() -> list[int]:
    return [5, 7, 9, 11, 13, 15]


def init_config(state: Dict[str, Any]) -> None:
    """Initialize configuration screen state."""
    state["inputs"] = {
        "dimension": 5,
        "sdg_id": 1,
    }
    state["focusable"] = [
        "dim_left",
        "dim_right",
        "sdg_left",
        "sdg_right",
        "continue",
        "back",
    ]
    state["focus_index"] = 4
    state["rects"] = _layout()


def _change_dimension(state: Dict[str, Any], direction: int) -> None:
    dimensions = _dimensions()
    current = state["inputs"]["dimension"]
    index = dimensions.index(current)
    new_index = max(0, min(len(dimensions) - 1, index + direction))
    state["inputs"]["dimension"] = dimensions[new_index]


def _change_sdg(state: Dict[str, Any], direction: int) -> None:
    sdg_ids = list_sdg_ids()
    current = state["inputs"]["sdg_id"]
    index = sdg_ids.index(current)
    new_index = (index + direction) % len(sdg_ids)
    state["inputs"]["sdg_id"] = sdg_ids[new_index]


def _start_game(state: Dict[str, Any]) -> str:
    """Generate cards and move to the card display preview screen."""
    dimension = state["inputs"]["dimension"]
    sdg_id = state["inputs"]["sdg_id"]
    card_type = get_card_type(sdg_id)
    main_pattern = get_figure_pattern(card_type, is_main=True, dimension=dimension)
    complement_pattern = get_figure_pattern(
        card_type, is_main=False, dimension=dimension
    )
    cards = make_cards(dimension, main_pattern, complement_pattern)
    state["session"]["dimension"] = dimension
    state["session"]["sdg_id"] = sdg_id
    state["session"]["main_card"] = cards["main"]
    state["session"]["complement_card"] = cards["complement"]
    state["session"]["drawn_numbers"] = []
    state["session"]["marked_main"] = set()
    state["session"]["marked_complement"] = set()
    state["session"]["winning_card"] = None
    state["session"]["game_over"] = False
    return "card_display"


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
    """Activate a control on this screen."""
    if name == "dim_left":
        _change_dimension(state, -1)
    elif name == "dim_right":
        _change_dimension(state, 1)
    elif name == "sdg_left":
        _change_sdg(state, -1)
    elif name == "sdg_right":
        _change_sdg(state, 1)
    elif name == "continue":
        return _start_game(state)
    elif name == "back":
        return "menu"
    return state["current_screen"]


def draw(surface: pygame.Surface, state: Dict[str, Any]) -> None:
    """Render the card configuration screen."""
    surface.fill(COLOR_MINT)
    rects = _layout()
    state["rects"] = rects

    draw_text(
        surface,
        "Configuracion de cartones",
        (WINDOW_WIDTH // 2, 80),
        font_size=40,
        color=COLOR_PINE,
        center=True,
    )

    mouse_pos = pygame.mouse.get_pos()
    hovered = {name: rect.collidepoint(mouse_pos) for name, rect in rects.items()}
    focused = get_focused(state)

    draw_text(
        surface,
        "Dimension del carton:",
        (rects["dim_value"].centerx, rects["dim_value"].y - 30),
        font_size=22,
        color=COLOR_CHARCOAL,
        center=True,
    )
    draw_button(
        surface,
        "<",
        rects["dim_left"],
        hovered=hovered["dim_left"],
        focused=focused == "dim_left",
    )
    draw_text(
        surface,
        f"{state['inputs']['dimension']} x {state['inputs']['dimension']}",
        rects["dim_value"].center,
        font_size=24,
        color=COLOR_CHARCOAL,
        center=True,
    )
    draw_button(
        surface,
        ">",
        rects["dim_right"],
        hovered=hovered["dim_right"],
        focused=focused == "dim_right",
    )

    sdg_id = state["inputs"]["sdg_id"]
    sdg_name = get_sdg_name(sdg_id)
    draw_text(
        surface,
        "Tema ODS:",
        (rects["sdg_value"].centerx, rects["sdg_value"].y - 30),
        font_size=22,
        color=COLOR_CHARCOAL,
        center=True,
    )
    draw_button(
        surface,
        "<",
        rects["sdg_left"],
        hovered=hovered["sdg_left"],
        focused=focused == "sdg_left",
    )
    pygame.draw.rect(surface, get_sdg_color(sdg_id), rects["sdg_value"])
    pygame.draw.rect(surface, COLOR_CHARCOAL, rects["sdg_value"], width=2)
    draw_text(
        surface,
        f"ODS {sdg_id}: {sdg_name}",
        rects["sdg_value"].center,
        font_size=18,
        color=COLOR_WHITE,
        center=True,
    )
    draw_button(
        surface,
        ">",
        rects["sdg_right"],
        hovered=hovered["sdg_right"],
        focused=focused == "sdg_right",
    )

    draw_button(
        surface,
        "Continuar",
        rects["continue"],
        hovered=hovered["continue"],
        focused=focused == "continue",
    )
    draw_button(
        surface,
        "Volver",
        rects["back"],
        hovered=hovered["back"],
        focused=focused == "back",
    )

    if state.get("error_message"):
        draw_error_message(
            surface,
            state["error_message"],
            (WINDOW_WIDTH // 2, WINDOW_HEIGHT - 80),
            font_size=20,
        )
