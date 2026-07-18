"""Tombola gameplay screen (non-OOP)."""

from typing import Any, Dict, List, Set

import pygame

from src.config import (COLOR_CHARCOAL, COLOR_MINT, COLOR_MOSS, COLOR_PINE,
                        COLOR_SAGE_LIGHT, COLOR_WHITE, WINDOW_HEIGHT,
                        WINDOW_WIDTH)
from src.core.card import card_points, card_sum, mark_number
from src.core.card_figures import get_card_type
from src.core.game import check_winner, draw_next, make_number_pool
from src.ods.data import get_sdg_color, get_sdg_messages, get_sdg_name
from src.persistence.games import add_game, load_games, make_game_record
from src.ui.app_state import cycle_focus, get_focused
from src.ui.common import (draw_button, draw_error_message, draw_message_panel,
                           draw_text, get_font)


def _layout() -> Dict[str, pygame.Rect]:
    """Return the UI rectangles for the game screen."""
    return {
        "draw": pygame.Rect(WINDOW_WIDTH // 2 - 100, 120, 200, 45),
        "simulate": pygame.Rect(WINDOW_WIDTH // 2 - 100, 175, 200, 45),
        "result": pygame.Rect(WINDOW_WIDTH // 2 - 100, 120, 200, 45),
        "menu": pygame.Rect(WINDOW_WIDTH // 2 - 100, 640, 200, 45),
        "victory": pygame.Rect(WINDOW_WIDTH // 2 - 150, 540, 300, 45),
    }


def _card_numbers(*cards: Any) -> Set[int]:
    """Return the union of all numbered cells across the given cards."""
    numbers: Set[int] = set()
    for card in cards:
        for row in card:
            for value in row:
                if value is not None:
                    numbers.add(value)
    return numbers


def init_game(state: Dict[str, Any]) -> None:
    """Initialize gameplay screen state."""
    session = state["session"]
    dimension = session.get("dimension", 5)
    if not session.get("number_pool"):
        main_card = session.get("main_card")
        complement_card = session.get("complement_card")
        if main_card is not None and complement_card is not None:
            numbers = _card_numbers(main_card, complement_card)
            session["number_pool"] = make_number_pool(dimension, numbers)
        else:
            session["number_pool"] = make_number_pool(dimension)
    state["inputs"] = {}
    state["focusable"] = ["draw", "simulate", "menu"]
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
            if value is None:
                pygame.draw.rect(surface, COLOR_WHITE, rect)
                pygame.draw.rect(surface, COLOR_CHARCOAL, rect, width=1)
                continue
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
        state["focusable"] = ["victory", "menu"]
        state["focus_index"] = 0
    return state["current_screen"]


def _simulate_game(state: Dict[str, Any]) -> str:
    """Run the full tombola draw simulation until a winner is found."""
    max_draws = len(state["session"].get("number_pool", []))
    # Use the `game_over` flag to skip further draws once a winner is
    # found. The original code used `break` to exit the loop early; here we
    # avoid `break` by checking the flag and simply continuing iterations
    # without work once the game is over. This preserves semantics while
    # complying with the requirement to remove `break` usage.
    for _ in range(max_draws):
        if state["session"].get("game_over"):
            # Skip drawing further numbers; loop continues but does no work.
            continue
        _draw_number(state)
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
    if name == "draw" and (not session.get("game_over")):
        return _draw_number(state)
    if name == "simulate" and (not session.get("game_over")):
        return _simulate_game(state)
    if name in ("result", "victory") and session.get("game_over"):
        return "menu"
    if name == "menu":
        return "menu"
    return state["current_screen"]


def _draw_trophy_icon(surface: pygame.Surface, rect: pygame.Rect) -> None:
    """Draw a simple trophy icon."""
    (cx, cy) = rect.center
    pygame.draw.polygon(
        surface,
        COLOR_PINE,
        [
            (cx, cy - 14),
            (cx + 10, cy - 6),
            (cx + 8, cy + 4),
            (cx - 8, cy + 4),
            (cx - 10, cy - 6),
        ],
    )
    pygame.draw.rect(surface, COLOR_PINE, (cx - 3, cy + 4, 6, 8))
    pygame.draw.rect(surface, COLOR_PINE, (cx - 6, cy + 11, 12, 3))


def _draw_victory_modal(
    surface: pygame.Surface,
    state: Dict[str, Any],
    rects: Dict[str, pygame.Rect],
    hovered: Dict[str, bool],
    focused: str,
) -> None:
    """Draw a centered modal declaring the winner."""
    session = state["session"]
    sdg_id = session.get("sdg_id", 1)
    dimension = session.get("dimension", 5)
    sdg_name = get_sdg_name(sdg_id)
    sdg_color = get_sdg_color(sdg_id)
    winning_card = session.get("winning_card", "main")
    if winning_card == "main":
        card = session["main_card"]
        marked = session["marked_main"]
        card_label = "Cartón 1"
    else:
        card = session["complement_card"]
        marked = session["marked_complement"]
        card_label = "Cartón 2"
    total_sum = card_sum(card)
    points = card_points(card, marked)
    messages = get_sdg_messages(sdg_id)
    sdg_message = messages[0] if messages else ""
    overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.SRCALPHA)
    overlay.fill((242, 247, 244, 200))
    surface.blit(overlay, (0, 0))
    modal_w = 520
    modal_h = 520
    modal_rect = pygame.Rect(
        (WINDOW_WIDTH - modal_w) // 2, (WINDOW_HEIGHT - modal_h) // 2, modal_w, modal_h
    )
    pygame.draw.rect(surface, COLOR_WHITE, modal_rect, border_radius=20)
    pygame.draw.rect(surface, COLOR_MOSS, modal_rect, width=4, border_radius=20)
    trophy_rect = pygame.Rect(modal_rect.centerx - 25, modal_rect.y + 30, 50, 50)
    pygame.draw.circle(surface, COLOR_MINT, trophy_rect.center, 28)
    _draw_trophy_icon(surface, trophy_rect)
    draw_text(
        surface,
        "¡RESULTADO GLOBAL DE LA PARTIDA!",
        (modal_rect.centerx, modal_rect.y + 95),
        font_size=13,
        color=COLOR_PINE,
        center=True,
    )
    draw_text(
        surface,
        "¡GANADOR!",
        (modal_rect.centerx, modal_rect.y + 125),
        font_size=42,
        color=COLOR_PINE,
        center=True,
    )
    italic_font = get_font(14)
    italic_font.set_italic(True)
    description = f"Este cartón ha cubierto todas sus celdas biológicas en base a la tómbola {dimension}x{dimension} del {sdg_name}."
    desc_lines = []
    words = description.split()
    line = ""
    max_width = modal_w - 80
    for word in words:
        test = f"{line} {word}".strip()
        if italic_font.size(test)[0] <= max_width:
            line = test
        else:
            desc_lines.append(line)
            line = word
    if line:
        desc_lines.append(line)
    desc_y = modal_rect.y + 170
    for desc_line in desc_lines[:3]:
        rendered = italic_font.render(desc_line, True, COLOR_CHARCOAL)
        rect = rendered.get_rect(center=(modal_rect.centerx, desc_y))
        surface.blit(rendered, rect)
        desc_y += 20
    table_y = desc_y + 20
    table_rect = pygame.Rect(modal_rect.x + 40, table_y, modal_w - 80, 70)
    pygame.draw.rect(surface, COLOR_MINT, table_rect, border_radius=12)
    pygame.draw.rect(surface, COLOR_SAGE_LIGHT, table_rect, width=1, border_radius=12)
    stats = [
        ("IDENTIDAD", card_label),
        ("SUMA DE CELDAS", str(total_sum)),
        ("PUNTAJE ODS", f"+{points} pts"),
    ]
    col_width = (modal_w - 80) // 3
    for index, (label, value) in enumerate(stats):
        x = table_rect.x + index * col_width + col_width // 2
        draw_text(
            surface,
            label,
            (x, table_rect.y + 12),
            font_size=10,
            color=COLOR_CHARCOAL,
            center=True,
        )
        draw_text(
            surface,
            value,
            (x, table_rect.y + 36),
            font_size=16,
            color=COLOR_PINE,
            center=True,
        )
        if index < 2:
            pygame.draw.line(
                surface,
                COLOR_SAGE_LIGHT,
                (table_rect.x + (index + 1) * col_width, table_rect.y + 10),
                (table_rect.x + (index + 1) * col_width, table_rect.bottom - 10),
                1,
            )
    quote_y = table_rect.bottom + 25
    quote_rect = pygame.Rect(modal_rect.x + 40, quote_y, modal_w - 80, 45)
    pygame.draw.rect(surface, sdg_color, quote_rect, border_radius=12)
    quote_font = get_font(12)
    quote_font.set_italic(True)
    quote_lines = []
    words = sdg_message.split()
    line = ""
    for word in words:
        test = f"{line} {word}".strip()
        if quote_font.size(test)[0] <= modal_w - 120:
            line = test
        else:
            quote_lines.append(line)
            line = word
    if line:
        quote_lines.append(line)
    quote_line_y = quote_rect.centery - (len(quote_lines[:2]) - 1) * 14 // 2
    for quote_line in quote_lines[:2]:
        rendered = quote_font.render(f'"{quote_line}"', True, COLOR_WHITE)
        rect = rendered.get_rect(center=(quote_rect.centerx, quote_line_y))
        surface.blit(rendered, rect)
        quote_line_y += 14
    draw_text(
        surface,
        "Autorespaldo consolidado exitosamente en JUEGOS.bin e historial del jugador.",
        (modal_rect.centerx, quote_rect.bottom + 25),
        font_size=10,
        color=COLOR_CHARCOAL,
        center=True,
    )
    draw_button(
        surface,
        "IR A MENÚ",
        rects["victory"],
        hovered=hovered["victory"],
        focused=focused == "victory",
    )


def draw(surface: pygame.Surface, state: Dict[str, Any]) -> None:
    """Render the gameplay screen."""
    surface.fill(COLOR_MINT)
    rects = _layout()
    state["rects"] = rects
    session = state["session"]
    sdg_id = session.get("sdg_id", 1)
    dimension = session.get("dimension", 5)
    cell_size = _cell_size(dimension)
    sdg_name = get_sdg_name(sdg_id)
    draw_text(
        surface,
        f"Partida - {sdg_name}",
        (WINDOW_WIDTH // 2, 30),
        font_size=32,
        color=COLOR_PINE,
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
        COLOR_PINE,
    )
    right_card_pos = (WINDOW_WIDTH - 80 - dimension * cell_size, 180)
    _draw_card(
        surface,
        session["complement_card"],
        session["marked_complement"],
        right_card_pos,
        cell_size,
        f"Complemento - {sdg_name}",
        COLOR_PINE,
    )
    mouse_pos = pygame.mouse.get_pos()
    hovered = {name: rect.collidepoint(mouse_pos) for (name, rect) in rects.items()}
    focused = get_focused(state)
    if session.get("game_over"):
        _draw_victory_modal(surface, state, rects, hovered, focused)
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
        draw_button(
            surface,
            "Simular completo",
            rects["simulate"],
            hovered=hovered["simulate"],
            focused=focused == "simulate",
        )
    draw_text(
        surface,
        f"Numeros sorteados: {len(session['drawn_numbers'])}",
        (WINDOW_WIDTH // 2, 620),
        font_size=20,
        color=COLOR_CHARCOAL,
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
            (WINDOW_WIDTH // 2, WINDOW_HEIGHT - 100),
            font_size=20,
        )
    draw_message_panel(surface, state, sdg_id=sdg_id)
