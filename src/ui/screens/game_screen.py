"""Tombola gameplay screen (non-OOP)."""

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
from src.core.card import card_points, card_sum, mark_number
from src.core.card_figures import get_card_type
from src.core.game import check_winner, draw_next, make_number_pool
from src.ods.data import get_sdg_color, get_sdg_name, get_sdg_slogan
from src.persistence.games import add_game, load_games, make_game_record
from src.ui.app_state import cycle_focus, get_focused
from src.ui.common import draw_button, draw_error_message, draw_text


def _layout() -> Dict[str, pygame.Rect]:
    """Return the UI rectangles for the game screen."""
    return {
        "draw": pygame.Rect(WINDOW_WIDTH // 2 - 100, 120, 200, 45),
        "result": pygame.Rect(WINDOW_WIDTH // 2 - 100, 120, 200, 45),
        "menu": pygame.Rect(WINDOW_WIDTH // 2 - 100, 680, 200, 45),
    }


def init_game(state: Dict[str, Any]) -> None:
    """Initialize gameplay screen state."""
    session = state["session"]
    dimension = session.get("dimension", 5)
    if not session.get("number_pool"):
        session["number_pool"] = make_number_pool(dimension)
    state["inputs"] = {}
    state["focusable"] = ["draw", "menu"]
    state["focus_index"] = 0
    state["rects"] = _layout()
    state["games"] = load_games()


def _cell_size(dimension: int) -> int:
    """Choose a cell size that fits the available area."""
    max_side = 280
    return max(20, min(50, max_side // dimension))


def _draw_card(
    surface: pygame.Surface,
    card: Any,
    marked: Any,
    top_left: Any,
    cell_size: int,
    title: str,
    sdg_color: Any,
) -> None:
    """Draw a single NxN card grid."""
    draw_text(surface, title, (top_left[0], top_left[1] - 30), font_size=20)
    for row_index, row in enumerate(card):
        for col_index, value in enumerate(row):
            rect = pygame.Rect(
                top_left[0] + col_index * cell_size,
                top_left[1] + row_index * cell_size,
                cell_size,
                cell_size,
            )
            is_marked = value in marked
            fill_color = sdg_color if is_marked else COLOR_WHITE
            pygame.draw.rect(surface, fill_color, rect)
            pygame.draw.rect(surface, COLOR_CHARCOAL, rect, width=1)
            text_color = COLOR_WHITE if is_marked else COLOR_CHARCOAL
            draw_text(
                surface,
                str(value),
                rect.center,
                font_size=max(12, cell_size // 2),
                color=text_color,
                center=True,
            )


def _draw_number(state: Dict[str, Any]) -> str:
    """Draw the next tombola number and update game state."""
    session = state["session"]
    pool = session.get("number_pool", [])
    number = draw_next(pool)
    if number is None:
        return state["current_screen"]

    session["drawn_numbers"].append(number)
    main_card = session["main_card"]
    complement_card = session["complement_card"]
    mark_number(main_card, session["marked_main"], number)
    mark_number(complement_card, session["marked_complement"], number)

    card_type = get_card_type(session.get("sdg_id", 1))
    winner = check_winner(
        main_card,
        session["marked_main"],
        complement_card,
        session["marked_complement"],
        card_type,
    )
    if winner:
        session["winning_card"] = winner
        session["game_over"] = True
        _save_game(state)
        state["focusable"] = ["result", "menu"]
        state["focus_index"] = 0
    return state["current_screen"]


def _save_game(state: Dict[str, Any]) -> None:
    """Persist the completed game to the binary file with raw data only."""
    session = state["session"]
    player = session.get("player")
    if player is None:
        return
    game = make_game_record(
        player_id=player["player_id"],
        sdg_id=session.get("sdg_id", 1),
        dimension=session.get("dimension", 5),
        main_card=session["main_card"],
        complement_card=session["complement_card"],
        drawn_numbers=session["drawn_numbers"][:],
    )
    state["games"] = add_game(state["games"], game)


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
    """Activate a control on the game screen."""
    session = state["session"]
    if name == "draw" and not session.get("game_over"):
        return _draw_number(state)
    if name == "result" and session.get("game_over"):
        return "result"
    if name == "menu":
        return "menu"
    return state["current_screen"]


def draw(surface: pygame.Surface, state: Dict[str, Any]) -> None:
    """Render the gameplay screen."""
    surface.fill(COLOR_MINT)
    rects = _layout()
    state["rects"] = rects
    session = state["session"]

    sdg_id = session.get("sdg_id", 1)
    sdg_color = get_sdg_color(sdg_id)
    dimension = session.get("dimension", 5)
    cell_size = _cell_size(dimension)

    sdg_name = get_sdg_name(sdg_id)
    draw_text(
        surface,
        f"Partida - {sdg_name}",
        (WINDOW_WIDTH // 2, 30),
        font_size=32,
        color=sdg_color,
        center=True,
    )

    left_card_pos = (80, 180)
    _draw_card(
        surface,
        session["main_card"],
        session["marked_main"],
        left_card_pos,
        cell_size,
        f"Principal - {sdg_name}",
        sdg_color,
    )

    right_card_pos = (WINDOW_WIDTH - 80 - dimension * cell_size, 180)
    _draw_card(
        surface,
        session["complement_card"],
        session["marked_complement"],
        right_card_pos,
        cell_size,
        f"Complemento - {sdg_name}",
        sdg_color,
    )

    mouse_pos = pygame.mouse.get_pos()
    hovered = {name: rect.collidepoint(mouse_pos) for name, rect in rects.items()}
    focused = get_focused(state)

    if session.get("game_over"):
        draw_text(
            surface,
            f"GANADOR: {session['winning_card'].upper()}",
            (WINDOW_WIDTH // 2, 90),
            font_size=28,
            color=COLOR_PINE,
            center=True,
        )
        draw_button(
            surface,
            "Ver resultado",
            rects["result"],
            hovered=hovered["result"],
            focused=focused == "result",
        )
    else:
        last = session["drawn_numbers"][-1] if session["drawn_numbers"] else None
        last_text = (
            f"Ultimo numero: {last}" if last is not None else "Presione Sacar numero"
        )
        draw_text(
            surface,
            last_text,
            (WINDOW_WIDTH // 2, 90),
            font_size=24,
            color=COLOR_CHARCOAL,
            center=True,
        )
        draw_button(
            surface,
            "Sacar numero",
            rects["draw"],
            hovered=hovered["draw"],
            focused=focused == "draw",
        )

    draw_text(
        surface,
        f"Numeros sorteados: {len(session['drawn_numbers'])}",
        (WINDOW_WIDTH // 2, 620),
        font_size=20,
        color=COLOR_CHARCOAL,
        center=True,
    )

    slogan = get_sdg_slogan(sdg_id)
    draw_text(
        surface,
        slogan,
        (WINDOW_WIDTH // 2, WINDOW_HEIGHT - 40),
        font_size=18,
        color=COLOR_PINE,
        center=True,
    )

    draw_button(
        surface,
        "Menu",
        rects["menu"],
        hovered=hovered["menu"],
        focused=focused == "menu",
    )

    if state.get("error_message"):
        draw_error_message(
            surface,
            state["error_message"],
            (WINDOW_WIDTH // 2, WINDOW_HEIGHT - 120),
            font_size=20,
        )
