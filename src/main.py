"""Tombola GUI entry point with full application flow (non-OOP)."""

from pathlib import Path
import sys
from typing import Any, Dict

# Allow `python src/main.py` to resolve `src.*` imports.
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import pygame  # noqa: E402

from src.config import FPS, WINDOW_HEIGHT, WINDOW_WIDTH  # noqa: E402
from src.ui.app_state import make_app_state, set_screen  # noqa: E402
from src.ui.screens.game_screen import (  # noqa: E402
    draw as draw_game,
    handle_event as handle_game,
    init_game,
)
from src.ui.screens.login_screen import (  # noqa: E402
    draw as draw_login,
    handle_event as handle_login,
    init_login,
)
from src.ui.screens.menu_screen import (  # noqa: E402
    draw as draw_menu,
    handle_event as handle_menu,
    init_menu,
)
from src.ui.screens.register_screen import (  # noqa: E402
    draw as draw_register,
    handle_event as handle_register,
    init_register,
)
from src.ui.screens.reports_screen import (  # noqa: E402
    draw as draw_reports,
    handle_event as handle_reports,
    init_reports,
)
from src.ui.screens.result_screen import (  # noqa: E402
    draw as draw_result,
    handle_event as handle_result,
    init_result,
)


SCREEN_HANDLERS = {
    "login": (init_login, handle_login, draw_login),
    "register": (init_register, handle_register, draw_register),
    "menu": (init_menu, handle_menu, draw_menu),
    "game": (init_game, handle_game, draw_game),
    "result": (init_result, handle_result, draw_result),
    "reports": (init_reports, handle_reports, draw_reports),
}


def main() -> None:
    """Run the Tombola application."""
    pygame.init()
    screen_surface = pygame.display.set_mode(
        (WINDOW_WIDTH, WINDOW_HEIGHT), pygame.DOUBLEBUF
    )
    pygame.display.set_caption("Tombola - ODS")
    clock = pygame.time.Clock()

    state = make_app_state()
    _init_screen(state, "login")

    while state["running"]:
        current = state["current_screen"]
        handler = SCREEN_HANDLERS.get(current)
        if handler is None:
            break
        _, handle_event, draw_screen = handler

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                state["running"] = False
                continue
            next_screen = handle_event(state, event)
            if next_screen != current and next_screen in SCREEN_HANDLERS:
                _switch_screen(state, next_screen)
                current = next_screen

        draw_screen = SCREEN_HANDLERS[state["current_screen"]][2]
        draw_screen(screen_surface, state)
        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()
    sys.exit(0)


def _init_screen(state: Dict[str, Any], name: str) -> None:
    """Initialize a screen without changing the current one during startup."""
    init_fn, _, _ = SCREEN_HANDLERS[name]
    init_fn(state)


def _switch_screen(state: Dict[str, Any], name: str) -> None:
    """Change to another screen and initialize it."""
    set_screen(state, name)
    init_fn, _, _ = SCREEN_HANDLERS[name]
    init_fn(state)


if __name__ == "__main__":
    main()
