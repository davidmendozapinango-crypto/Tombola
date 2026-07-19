"""Main menu screen (image-based UI) with hotspot navigation."""

from typing import Any, Dict

import pygame

from src.auth.session import logout
from src.config import (
    ASSETS_DIR,
    COLOR_MINT,
    WINDOW_HEIGHT,
    WINDOW_WIDTH,
)
from src.core.card import make_cards
from src.core.card_figures import get_card_type, get_figure_pattern
from src.ui.app_state import cycle_focus, get_focused


MENU_HOTSPOTS = {
    "register": (0.645, 0.405, 0.290, 0.088),
    "play":     (0.560, 0.545, 0.290, 0.088),
    "reports":  (0.475, 0.685, 0.290, 0.088),
    "exit":     (0.390, 0.825, 0.290, 0.088),
}


def _layout() -> Dict[str, pygame.Rect]:
    """Return the interactive hotspots for the main menu image."""
    return {
        name: pygame.Rect(
            int(WINDOW_WIDTH * values[0]),
            int(WINDOW_HEIGHT * values[1]),
            int(WINDOW_WIDTH * values[2]),
            int(WINDOW_HEIGHT * values[3]),
        )
        for name, values in MENU_HOTSPOTS.items()
    }


def _regenerate_cards(state: Dict[str, Any]) -> None:
    """Regenerate the main and complement cards using default configuration."""
    dimension = 5
    sdg_id = 1

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


def init_menu(state: Dict[str, Any]) -> None:
    """Initialize menu screen state with the background image."""
    state["inputs"] = {}
    state["focusable"] = ["register", "play", "reports", "exit"]
    state["focus_index"] = -1
    state["rects"] = _layout()
    state["pending_screen_after_login"] = None

    _regenerate_cards(state)

    image_path = ASSETS_DIR / "images" / "screens" / "main_menu_img.png"
    try:
        fondo = pygame.image.load(str(image_path)).convert()
        state["fondo_menu"] = pygame.transform.scale(fondo, (WINDOW_WIDTH, WINDOW_HEIGHT))
    except (pygame.error, FileNotFoundError):
        print(f"Advertencia: No se pudo cargar '{image_path}'")
        state["fondo_menu"] = None


def _activate(state: Dict[str, Any], name: str) -> str:
    """Activate a menu option."""
    if name == "register":
        return "register"
    if name == "play":
        state["pending_screen_after_login"] = "config"
        return "login"
    if name == "reports":
        return "reports"
    if name == "exit":
        state["running"] = False
        return "exit"

    return state["current_screen"]


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
            logout(state["session"])
            return "login"
        if event.key in (pygame.K_RETURN, pygame.K_SPACE):
            return _activate(state, focused)

    return state["current_screen"]


def draw(surface: pygame.Surface, state: Dict[str, Any]) -> None:
    """Render the main menu screen using the background image."""
    if state.get("fondo_menu"):
        surface.blit(state["fondo_menu"], (0, 0))
    else:
        surface.fill(COLOR_MINT)
