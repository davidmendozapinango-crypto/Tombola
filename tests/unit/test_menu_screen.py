import pygame

from src.config import WINDOW_HEIGHT, WINDOW_WIDTH
from src.ui.screens.menu_screen import draw


def test_draw_menu_renders_without_name_error():
    pygame.init()
    surface = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
    state = {
        "running": True,
        "session": {},
        "error_message": "",
        "info_message": "",
        "focus_index": 0,
        "focusable": [],
        "rects": {},
        "menu_config": {"dimension": 5, "sdg_id": 1},
        "player_points": 0,
    }

    draw(surface, state)

    assert state["rects"]
