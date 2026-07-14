"""Card display screen: shows SDG figure preview before playing (non-OOP)."""

from pathlib import Path
from typing import Any, Dict, Optional

import pygame

from src.config import (
    ASSETS_DIR,
    COLOR_CHARCOAL,
    COLOR_MINT,
    COLOR_PINE,
    COLOR_WHITE,
    WINDOW_HEIGHT,
    WINDOW_WIDTH,
)
from src.core.card_figures import get_card_type, get_figure_pattern
from src.ods.data import get_sdg_color, get_sdg_name
from src.ui.app_state import cycle_focus, get_focused
from src.ui.common import draw_button, draw_text


def _layout() -> Dict[str, pygame.Rect]:
    """Return the UI rectangles for the card display screen."""
    center_x = WINDOW_WIDTH // 2
    return {
        "play": pygame.Rect(center_x - 160, WINDOW_HEIGHT - 90, 150, 45),
        "back": pygame.Rect(center_x + 10, WINDOW_HEIGHT - 90, 150, 45),
    }


def _load_card_image(card_type: str, is_main: bool) -> Optional[pygame.Surface]:
    """Load the PNG figure image for the selected card type."""
    suffix = "1" if is_main else "2"
    filename = f"{card_type}{suffix}.png"
    image_path = ASSETS_DIR / "images" / "ods" / filename
    try:
        return pygame.image.load(str(image_path))
    except (FileNotFoundError, pygame.error):
        return None


def _draw_preview_card(
    surface: pygame.Surface,
    dimension: int,
    pattern: set,
    top_left: Any,
    cell_size: int,
    title: str,
    sdg_color: Any,
) -> None:
    """Draw a preview card showing the filling sequence and figure cells."""
    draw_text(surface, title, (top_left[0], top_left[1] - 30), font_size=20)
    sequence = 1
    for row in range(dimension):
        for col in range(dimension):
            rect = pygame.Rect(
                top_left[0] + col * cell_size,
                top_left[1] + row * cell_size,
                cell_size,
                cell_size,
            )
            is_figure = (row, col) in pattern
            fill_color = sdg_color if is_figure else COLOR_WHITE
            pygame.draw.rect(surface, fill_color, rect)
            pygame.draw.rect(surface, COLOR_CHARCOAL, rect, width=1)
            text_color = COLOR_WHITE if is_figure else COLOR_CHARCOAL
            draw_text(
                surface,
                str(sequence),
                rect.center,
                font_size=max(10, cell_size // 2),
                color=text_color,
                center=True,
            )
            sequence += 1


def init_card_display(state: Dict[str, Any]) -> None:
    """Initialize the card display screen."""
    state["inputs"] = {}
    state["focusable"] = ["play", "back"]
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
                if name == "play":
                    return "game"
                if name == "back":
                    return "config"

    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_TAB:
            cycle_focus(state, 1)
            return state["current_screen"]
        if event.key in (pygame.K_RETURN, pygame.K_SPACE):
            if focused == "play":
                return "game"
            if focused == "back":
                return "config"
        if event.key == pygame.K_ESCAPE:
            return "config"

    return state["current_screen"]


def draw(surface: pygame.Surface, state: Dict[str, Any]) -> None:
    """Render the card display screen."""
    surface.fill(COLOR_MINT)
    rects = _layout()
    state["rects"] = rects
    session = state["session"]

    sdg_id = session.get("sdg_id", 1)
    sdg_name = get_sdg_name(sdg_id)
    sdg_color = get_sdg_color(sdg_id)
    dimension = session.get("dimension", 5)
    card_type = get_card_type(sdg_id)

    draw_text(
        surface,
        f"Vista previa - {sdg_name}",
        (WINDOW_WIDTH // 2, 40),
        font_size=36,
        color=sdg_color,
        center=True,
    )
    draw_text(
        surface,
        f"Figura del carton: tipo {card_type}",
        (WINDOW_WIDTH // 2, 85),
        font_size=22,
        color=COLOR_CHARCOAL,
        center=True,
    )

    cell_size = max(20, min(40, 220 // dimension))
    main_pattern = get_figure_pattern(card_type, is_main=True, dimension=dimension)
    complement_pattern = get_figure_pattern(
        card_type, is_main=False, dimension=dimension
    )

    _draw_preview_card(
        surface,
        dimension,
        main_pattern,
        (80, 140),
        cell_size,
        "Principal (figura a completar)",
        sdg_color,
    )
    _draw_preview_card(
        surface,
        dimension,
        complement_pattern,
        (WINDOW_WIDTH - 80 - dimension * cell_size, 140),
        cell_size,
        "Complemento (figura a completar)",
        sdg_color,
    )

    image_y = 420
    main_image = _load_card_image(card_type, True)
    if main_image:
        scaled = pygame.transform.scale(main_image, (140, 140))
        surface.blit(scaled, (120, image_y))
    complement_image = _load_card_image(card_type, False)
    if complement_image:
        scaled = pygame.transform.scale(complement_image, (140, 140))
        surface.blit(scaled, (WINDOW_WIDTH - 260, image_y))

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
        "Volver",
        rects["back"],
        hovered=hovered["back"],
        focused=focused == "back",
    )
