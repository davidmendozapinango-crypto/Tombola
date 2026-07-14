"""Reports screen (non-OOP) with date filtering and txt export."""

from collections import Counter
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

import pygame

from src.config import (
    COLOR_CHARCOAL,
    COLOR_MINT,
    COLOR_PINE,
    COLOR_WHITE,
    WINDOW_HEIGHT,
    WINDOW_WIDTH,
)
from src.ods.data import get_sdg_name
from src.persistence.games import calculate_game_summary, load_games
from src.persistence.players import load_players
from src.ui.app_state import cycle_focus, get_focused, is_focused
from src.ui.common import (
    draw_button,
    draw_error_message,
    draw_input,
    draw_text,
    wrap_text,
)


def _layout() -> Dict[str, pygame.Rect]:
    """Return the UI rectangles for the reports screen."""
    center_x = WINDOW_WIDTH // 2
    return {
        "date_start": pygame.Rect(center_x - 220, 90, 200, 32),
        "date_end": pygame.Rect(center_x + 20, 90, 200, 32),
        "apply": pygame.Rect(center_x - 100, 130, 90, 32),
        "clear": pygame.Rect(center_x + 10, 130, 90, 32),
        "export": pygame.Rect(center_x - 160, WINDOW_HEIGHT - 80, 150, 45),
        "back": pygame.Rect(center_x + 10, WINDOW_HEIGHT - 80, 150, 45),
    }


def init_reports(state: Dict[str, Any]) -> None:
    """Initialize reports screen state."""
    state["inputs"] = {"date_start": "", "date_end": ""}
    state["focusable"] = [
        "date_start",
        "date_end",
        "apply",
        "clear",
        "export",
        "back",
    ]
    state["focus_index"] = 4
    state["rects"] = _layout()
    state["players"] = load_players()
    state["all_games"] = load_games()
    state["filtered_games"] = state["all_games"]
    state["report_export_path"] = None


def _parse_date(text: str) -> Optional[datetime]:
    """Parse a YYYY-MM-DD string into a datetime or return None."""
    try:
        return datetime.strptime(text.strip(), "%Y-%m-%d")
    except ValueError:
        return None


def _filter_games_by_date(
    games: List[Dict[str, Any]], start_text: str, end_text: str
) -> Tuple[List[Dict[str, Any]], Optional[str]]:
    """Return games within the requested date range and an optional error."""
    start_date = _parse_date(start_text)
    end_date = _parse_date(end_text)

    if start_text.strip() and start_date is None:
        return games, "Fecha inicio invalida (YYYY-MM-DD)."
    if end_text.strip() and end_date is None:
        return games, "Fecha fin invalida (YYYY-MM-DD)."

    filtered = []
    for game in games:
        played_at = game.get("played_at")
        if not isinstance(played_at, datetime):
            continue
        if start_date and played_at.date() < start_date.date():
            continue
        if end_date and played_at.date() > end_date.date():
            continue
        filtered.append(game)
    return filtered, None


def _player_game_counts(players, games):
    """Return a list of (player_id, full_name, count)."""
    counts = {player["player_id"]: 0 for player in players}
    for game in games:
        pid = game.get("player_id")
        if pid in counts:
            counts[pid] += 1
    return [
        (player["player_id"], player["full_name"], counts.get(player["player_id"], 0))
        for player in players
    ]


def _top_players(games, limit=5):
    """Return top players by accumulated total points (calculated from raw data)."""
    totals = Counter()
    names = {}
    for game in games:
        pid = game.get("player_id")
        summary = calculate_game_summary(game)
        totals[pid] += summary["total_points"]
        if pid not in names:
            names[pid] = pid
    sorted_totals = totals.most_common(limit)
    return [(pid, names.get(pid, pid), points) for pid, points in sorted_totals]


def _gantt_numbers(games, limit=10):
    """Return the most frequently drawn numbers across the filtered games."""
    counter = Counter()
    for game in games:
        for number in game.get("drawn_numbers", []):
            counter[number] += 1
    return counter.most_common(limit)


def _build_report_text(players, games, date_start: str = "", date_end: str = "") -> str:
    """Build a text report with all report sections."""
    lines: List[str] = []
    lines.append("=" * 60)
    lines.append("REPORTE TOMBOLA - ODS")
    lines.append(f"Generado: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    if date_start or date_end:
        lines.append(f"Rango de fechas: {date_start or 'inicio'} - {date_end or 'fin'}")
    lines.append("=" * 60)

    lines.append("")
    lines.append("JUGADORES Y PARTIDAS")
    lines.append("-" * 40)
    if players:
        for pid, name, count in _player_game_counts(players, games):
            lines.append(f"{pid} - {name}: {count} partidas")
    else:
        lines.append("No hay jugadores registrados.")

    lines.append("")
    lines.append("TOP 5 JUGADORES POR PUNTOS ACUMULADOS")
    lines.append("-" * 40)
    top = _top_players(games)
    if top:
        for rank, (pid, name, points) in enumerate(top, start=1):
            lines.append(f"{rank}. {name} - {points} pts")
    else:
        lines.append("No hay partidas registradas.")

    lines.append("")
    lines.append("NUMEROS MAS FRECUENTES")
    lines.append("-" * 40)
    gantt = _gantt_numbers(games)
    if gantt:
        for rank, (number, count) in enumerate(gantt, start=1):
            lines.append(f"{rank}. Numero {number}: {count} veces")
    else:
        lines.append("No hay sorteos registrados.")

    lines.append("")
    lines.append("HISTORIAL DE PARTIDAS")
    lines.append("-" * 40)
    if games:
        for game in games:
            played_at = game.get("played_at")
            date_text = played_at.strftime("%Y-%m-%d %H:%M") if played_at else "?"
            sdg_name = get_sdg_name(game.get("sdg_id", 1))
            summary = calculate_game_summary(game)
            lines.append(
                f"{date_text} - {game.get('player_id')} - {sdg_name} "
                f"- ganador: {summary['winning_card']} "
                f"- principal: {summary['main_points']} pts "
                f"- complemento: {summary['complement_points']} pts"
            )
    else:
        lines.append("No hay partidas registradas.")

    lines.append("")
    lines.append("=" * 60)
    return "\n".join(lines)


def _export_reports(state: Dict[str, Any]) -> str:
    """Export all reports to a physical text file and return the path."""
    report_dir = Path("reports")
    report_dir.mkdir(exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    file_path = report_dir / f"reporte_tombola_{timestamp}.txt"
    text = _build_report_text(
        state["players"],
        state["filtered_games"],
        state["inputs"].get("date_start", ""),
        state["inputs"].get("date_end", ""),
    )
    file_path.write_text(text, encoding="utf-8")
    return str(file_path)


def _apply_date_filter(state: Dict[str, Any]) -> None:
    """Apply the date filter and store the result or an error."""
    from src.ui.app_state import set_error

    games, error = _filter_games_by_date(
        state["all_games"],
        state["inputs"].get("date_start", ""),
        state["inputs"].get("date_end", ""),
    )
    if error:
        set_error(state, error)
        return
    state["filtered_games"] = games
    state["error_message"] = ""


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
                if name == "export":
                    path = _export_reports(state)
                    state["report_export_path"] = path
                    return state["current_screen"]
                if name == "apply":
                    _apply_date_filter(state)
                    return state["current_screen"]
                if name == "clear":
                    state["inputs"]["date_start"] = ""
                    state["inputs"]["date_end"] = ""
                    state["filtered_games"] = state["all_games"]
                    state["error_message"] = ""
                    return state["current_screen"]
                if name == "back":
                    return "menu"
                return state["current_screen"]

    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_TAB:
            cycle_focus(state, 1)
            return state["current_screen"]
        if event.key == pygame.K_ESCAPE:
            return "menu"
        if event.key in (pygame.K_RETURN, pygame.K_SPACE):
            if focused == "export":
                path = _export_reports(state)
                state["report_export_path"] = path
                return state["current_screen"]
            if focused == "apply":
                _apply_date_filter(state)
                return state["current_screen"]
            if focused == "clear":
                state["inputs"]["date_start"] = ""
                state["inputs"]["date_end"] = ""
                state["filtered_games"] = state["all_games"]
                state["error_message"] = ""
                return state["current_screen"]
            if focused == "back":
                return "menu"
            return state["current_screen"]
        if focused in ("date_start", "date_end"):
            if event.key == pygame.K_BACKSPACE:
                state["inputs"][focused] = state["inputs"][focused][:-1]
            elif event.unicode.isprintable() and len(event.unicode) == 1:
                state["inputs"][focused] += event.unicode

    return state["current_screen"]


def draw(surface: pygame.Surface, state: Dict[str, Any]) -> None:
    """Render the reports screen."""
    surface.fill(COLOR_MINT)
    rects = _layout()
    state["rects"] = rects

    draw_text(
        surface,
        "Reportes",
        (WINDOW_WIDTH // 2, 40),
        font_size=40,
        color=COLOR_PINE,
        center=True,
    )

    draw_text(
        surface,
        "Desde (YYYY-MM-DD):",
        (rects["date_start"].x, rects["date_start"].y - 20),
        font_size=16,
        color=COLOR_CHARCOAL,
    )
    draw_input(
        surface,
        state["inputs"].get("date_start", ""),
        rects["date_start"],
        focused=is_focused(state, "date_start"),
    )
    draw_text(
        surface,
        "Hasta (YYYY-MM-DD):",
        (rects["date_end"].x, rects["date_end"].y - 20),
        font_size=16,
        color=COLOR_CHARCOAL,
    )
    draw_input(
        surface,
        state["inputs"].get("date_end", ""),
        rects["date_end"],
        focused=is_focused(state, "date_end"),
    )

    mouse_pos = pygame.mouse.get_pos()
    hovered = {name: rect.collidepoint(mouse_pos) for name, rect in rects.items()}
    focused = get_focused(state)

    draw_button(
        surface,
        "Aplicar",
        rects["apply"],
        hovered=hovered["apply"],
        focused=focused == "apply",
    )
    draw_button(
        surface,
        "Limpiar",
        rects["clear"],
        hovered=hovered["clear"],
        focused=focused == "clear",
    )

    players = state.get("players", [])
    games = state.get("filtered_games", [])

    left_x = 60
    right_x = WINDOW_WIDTH // 2 + 40
    y_offset = 185

    draw_text(
        surface,
        "Jugadores y partidas",
        (left_x, y_offset),
        font_size=22,
        color=COLOR_PINE,
    )
    if players:
        for pid, name, count in _player_game_counts(players, games):
            draw_text(
                surface,
                f"{pid} - {name}: {count} partidas",
                (left_x, y_offset + 30),
                font_size=18,
            )
            y_offset += 24
    else:
        draw_text(
            surface,
            "No hay jugadores registrados.",
            (left_x, y_offset + 30),
            font_size=18,
        )
        y_offset += 30

    top_y = 185
    draw_text(
        surface, "TOP 5 jugadores", (right_x, top_y), font_size=22, color=COLOR_PINE
    )
    top = _top_players(games)
    if top:
        for rank, (pid, name, points) in enumerate(top, start=1):
            draw_text(
                surface,
                f"{rank}. {name} - {points} pts",
                (right_x, top_y + rank * 26),
                font_size=18,
            )
    else:
        draw_text(
            surface,
            "No hay partidas registradas.",
            (right_x, top_y + 30),
            font_size=18,
        )

    gantt_y = 405
    draw_text(
        surface,
        "Numeros mas frecuentes",
        (right_x, gantt_y),
        font_size=22,
        color=COLOR_PINE,
    )
    gantt = _gantt_numbers(games)
    if gantt:
        for rank, (number, count) in enumerate(gantt, start=1):
            draw_text(
                surface,
                f"{rank}. Numero {number}: {count} veces",
                (right_x, gantt_y + rank * 24),
                font_size=18,
            )
    else:
        draw_text(
            surface,
            "No hay sorteos registrados.",
            (right_x, gantt_y + 30),
            font_size=18,
        )

    history_y = 405
    draw_text(
        surface, "Ultimas partidas", (left_x, history_y), font_size=22, color=COLOR_PINE
    )
    recent = games[-5:][::-1]
    if recent:
        line_y = history_y + 30
        for game in recent:
            played_at = game.get("played_at")
            date_text = played_at.strftime("%Y-%m-%d %H:%M") if played_at else "?"
            sdg_name = get_sdg_name(game.get("sdg_id", 1))
            summary = calculate_game_summary(game)
            text = (
                f"{date_text} - {game.get('player_id')} - {sdg_name} "
                f"- ganador: {summary['winning_card']} "
                f"- P: {summary['main_points']} C: {summary['complement_points']}"
            )
            for line in wrap_text(text, WINDOW_WIDTH // 2 - 80, font_size=18):
                draw_text(surface, line, (left_x, line_y), font_size=18)
                line_y += 22
    else:
        draw_text(
            surface,
            "No hay partidas registradas.",
            (left_x, history_y + 30),
            font_size=18,
        )

    draw_button(
        surface,
        "Exportar .txt",
        rects["export"],
        hovered=hovered["export"],
        focused=focused == "export",
    )
    draw_button(
        surface,
        "Volver",
        rects["back"],
        hovered=hovered["back"],
        focused=focused == "back",
    )

    export_path = state.get("report_export_path")
    if export_path:
        draw_text(
            surface,
            f"Exportado: {Path(export_path).name}",
            (WINDOW_WIDTH // 2, WINDOW_HEIGHT - 130),
            font_size=16,
            color=COLOR_PINE,
            center=True,
        )

    if state.get("error_message"):
        draw_error_message(
            surface,
            state["error_message"],
            (WINDOW_WIDTH // 2, WINDOW_HEIGHT - 160),
            font_size=20,
        )
