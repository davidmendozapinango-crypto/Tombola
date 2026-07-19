import pygame

from src.ui.app_state import make_app_state
from src.ui.screens.menu_screen import handle_event, init_menu


def test_app_starts_on_menu_screen() -> None:
    state = make_app_state()

    assert state["current_screen"] == "menu"


def test_play_button_routes_through_login_before_game() -> None:
    state = make_app_state()
    state["current_screen"] = "menu"
    init_menu(state)

    event = pygame.event.Event(
        pygame.MOUSEBUTTONDOWN,
        button=1,
        pos=state["rects"]["play"].center,
    )

    next_screen = handle_event(state, event)

    assert next_screen == "login"
    assert state["pending_screen_after_login"] == "game"
