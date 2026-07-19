"""
Pantalla de reportes (estilo funcional, no-OOP) con seleccion de secciones y
exportacion de informes individuales en .txt.

Descripción:
  Contiene utilidades para filtrar partidas por fecha, construir diferentes
  secciones de informe (jugadores, top, frecuencia, historial) y exportarlas
  a archivos de texto. Las funciones de dibujo separan la logica de presentacion
  del armado del texto del informe.
"""

from collections import Counter
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple
import pygame
from src.config import (
    COLOR_CHARCOAL,
    COLOR_MINT,
    COLOR_MOSS,
    COLOR_PINE,
    COLOR_SAGE_LIGHT,
    COLOR_WHITE,
    WINDOW_HEIGHT,
    WINDOW_WIDTH,
)
from src.core.card import card_sum
from src.ods.data import get_sdg_name
from src.persistence.games import calculate_game_summary, load_games
from src.persistence.players import load_players
from src.ui.app_state import cycle_focus, get_focused, is_focused
from src.ui.common import (
    draw_button,
    draw_error_message,
    draw_input,
    draw_message_panel,
    draw_text,
    wrap_text,
)

_REPORT_SECTIONS = [
    ("players", "Jugadores y partidas"),
    ("top", "TOP 5 jugadores"),
    ("frequency", "Numeros mas frecuentes"),
    ("history", "Historial de partidas"),
]
_SECTION_LABELS = {
    "players": "Jugadores y partidas",
    "top": "TOP 5 jugadores por puntos",
    "frequency": "Numeros mas frecuentes",
    "history": "Historial de partidas",
}


def _layout() -> Dict[str, pygame.Rect]:
    """
    Devuelve los rectángulos (posiciones) usados por la pantalla de reportes.

    Devuelve:
        Dict[str, pygame.Rect]: Mapeo de nombres de control a rectángulos.
    """
    center_x = WINDOW_WIDTH // 2
    return {
        "date_start": pygame.Rect(center_x - 220, 90, 200, 32),
        "date_end": pygame.Rect(center_x + 20, 90, 200, 32),
        "apply": pygame.Rect(center_x - 100, 130, 90, 32),
        "clear": pygame.Rect(center_x + 10, 130, 90, 32),
        "players": pygame.Rect(60, 185, 190, 35),
        "top": pygame.Rect(60, 225, 190, 35),
        "frequency": pygame.Rect(60, 265, 190, 35),
        "history": pygame.Rect(60, 305, 190, 35),
        "back": pygame.Rect(WINDOW_WIDTH - 60 - 150, WINDOW_HEIGHT - 105, 150, 35),
        "export": pygame.Rect(
            WINDOW_WIDTH - 60 - 150 - 155, WINDOW_HEIGHT - 105, 150, 35
        ),
    }


def init_reports(state: Dict[str, Any]) -> None:
    """
    Inicializa el estado necesario para la pantalla de reportes.

    Args:
        state (Dict[str, Any]): Estado global de la aplicación (mutado in-place).

    Devuelve: None (mutación en `state`).
    """
    state["inputs"] = {"date_start": "", "date_end": ""}
    state["focusable"] = [
        "date_start",
        "date_end",
        "apply",
        "clear",
        "players",
        "top",
        "frequency",
        "history",
        "export",
        "back",
    ]
    state["focus_index"] = 4
    state["rects"] = _layout()
    state["selected_report"] = "players"
    state["players"] = load_players()
    state["all_games"] = load_games()
    state["filtered_games"] = state["all_games"]
    state["report_export_path"] = None


def _parse_date(text: str) -> Optional[datetime]:
    """
    Parsea una cadena en formato YYYY-MM-DD a un objeto datetime.

    Devuelve None si el texto no es un fech valido.
    """
    try:
        return datetime.strptime(text.strip(), "%Y-%m-%d")
    except ValueError:
        return None


def _filter_games_by_date(
    games: List[Dict[str, Any]], start_text: str, end_text: str
) -> Tuple[List[Dict[str, Any]], Optional[str]]:
    """
    Filtra la lista de partidas para incluir solo las jugadas dentro del rango
    especificado por `start_text` y `end_text`.

    Args:
        games (List[Dict[str, Any]]): Lista de partidas (diccionarios).
        start_text (str): Fecha de inicio en YYYY-MM-DD o cadena vacia.
        end_text (str): Fecha de fin en YYYY-MM-DD o cadena vacia.

    Returns:
        Tuple[List[Dict[str, Any]], Optional[str]]: (juegos_filtrados, error)
    """
    start_date = _parse_date(start_text)
    end_date = _parse_date(end_text)
    if start_text.strip() and start_date is None:
        return (games, "Fecha inicio invalida (YYYY-MM-DD).")
    if end_text.strip() and end_date is None:
        return (games, "Fecha fin invalida (YYYY-MM-DD).")
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
    return (filtered, None)


def _player_game_counts(players, games):
    """
    Devuelve una lista de tuplas (player_id, full_name, partidas_jugadas).
    """
    counts = {player["player_id"]: 0 for player in players}
    for game in games:
        pid = game.get("player_id")
        if pid in counts:
            counts[pid] += 1
    return [
        (player["player_id"], player["full_name"], counts.get(player["player_id"], 0))
        for player in players
    ]


def _player_lookup(players) -> Dict[str, Dict[str, Any]]:
    """
    Construye un mapeo rapido de player_id a registro de jugador.
    """
    return {player["player_id"]: player for player in players}


def _top_players(players, games, limit=5):
    """
    Calcula los jugadores con mayor puntaje acumulado.

    Cada entrada del resultado es una tupla:
    (player_id, full_name, state_code, game_count, points)
    """
    player_info = {
        player["player_id"]: (
            player.get("full_name", player["player_id"]),
            player.get("state_code", "?"),
        )
        for player in players
    }
    totals = Counter()
    game_counts = Counter()
    for game in games:
        pid = game.get("player_id")
        summary = calculate_game_summary(game)
        totals[pid] += summary["total_points"]
        game_counts[pid] += 1
    sorted_totals = totals.most_common(limit)
    return [
        (
            pid,
            player_info.get(pid, (pid, "?"))[0],
            player_info.get(pid, (pid, "?"))[1],
            game_counts.get(pid, 0),
            points,
        )
        for (pid, points) in sorted_totals
    ]


def _gantt_numbers(games, limit=10):
    """
    Devuelve los numeros mas frecuentes extraidos de las partidas filtradas.
    """
    counter = Counter()
    for game in games:
        for number in game.get("drawn_numbers", []):
            counter[number] += 1
    return counter.most_common(limit)


def _report_header(title: str, date_start: str = "", date_end: str = "") -> List[str]:
    """
    Construye las lineas del encabezado estandar para un informe de texto.
    """
    lines: List[str] = []
    lines.append("=" * 60)
    lines.append(f"REPORTE TOMBOLA - ODS: {title.upper()}")
    lines.append(f"Generado: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    if date_start or date_end:
        lines.append(f"Rango de fechas: {date_start or 'inicio'} - {date_end or 'fin'}")
    lines.append("=" * 60)
    return lines


def _build_players_report(
    players, games, date_start: str = "", date_end: str = ""
) -> str:
    """
    Construye el informe de jugadores y partidas como un texto con columnas.
    """
    lines = _report_header("Jugadores y partidas", date_start, date_end)
    lines.append("")
    lines.append("JUGADORES Y PARTIDAS REGISTRADOS")
    lines.append("")
    lines.append(
        f"{'CEDULA':<15} {'JUGADOR':<28} {'ESTADO':<10} {'PARTIDAS JUGADAS':<20}"
    )
    lines.append("-" * 80)
    if players:
        for pid, name, count in _player_game_counts(players, games):
            partidas = "partida" if count == 1 else "partidas"
            player = _player_lookup(players).get(pid, {})
            state_code = player.get("state_code", "?")
            lines.append(f"{pid:<15} {name:<28} {state_code:<10} {count} {partidas}")
    else:
        lines.append("No hay jugadores registrados.")
    lines.append("")
    lines.append("=" * 60)
    return "\n".join(lines)


def _build_top_report(players, games, date_start: str = "", date_end: str = "") -> str:
    """
    Construye el informe TOP 5 de jugadores.
    """
    lines = _report_header("TOP 5 jugadores", date_start, date_end)
    lines.append("")
    lines.append("TOP 5: JUGADORES DESTACADOS")
    lines.append("Lideres acumulados registrados en JUGADORES.bin")
    lines.append("-" * 40)
    top = _top_players(players, games)
    if top:
        for rank, (pid, name, state_code, game_count, points) in enumerate(
            top, start=1
        ):
            partidas = "partida" if game_count == 1 else "partidas"
            lines.append(
                f"{rank}. {name} - Region: {state_code} - {game_count} {partidas} - {points} ODS puntos"
            )
    else:
        lines.append("No hay partidas registradas.")
    lines.append("")
    lines.append("=" * 60)
    return "\n".join(lines)


def _build_frequency_report(games, date_start: str = "", date_end: str = "") -> str:
    """
    Construye el informe de numeros mas frecuentes (TOP 10).
    """
    lines = _report_header("Frecuencia de numeros", date_start, date_end)
    lines.append("")
    lines.append("FRECUENCIA DE NUMEROS (TOP 10)")
    lines.append("-" * 40)
    gantt = _gantt_numbers(games)
    if gantt:
        for rank, (number, count) in enumerate(gantt, start=1):
            sorteos = "sorteo" if count == 1 else "sorteos"
            lines.append(f"#{rank:2} Numero {number:2}: {count} {sorteos}")
    else:
        lines.append("No hay sorteos registrados.")
    lines.append("")
    lines.append("Nota del Algoritmo:")
    lines.append(
        "La aleatoriedad de la tombola se aproxima a la campana estadistica en sesiones largas. Los datos se actualizan dinamicamente."
    )
    lines.append("")
    lines.append("=" * 60)
    return "\n".join(lines)


def _build_history_report(
    players, games, date_start: str = "", date_end: str = ""
) -> str:
    """
    Construye el informe de historial de partidas con una fila por partida.
    """
    player_map = _player_lookup(players)
    lines = _report_header("Historial historico de partidas", date_start, date_end)
    lines.append("")
    lines.append("HISTORIAL HISTORICO DE PARTIDAS (JUEGOS.BIN)")
    lines.append("Bitacora de auditoria Federal del juego educativo")
    lines.append("")
    lines.append(
        f"{'FECHA':<12} {'CODIGO':<10} {'JUGADOR':<25} {'EST':<6} {'BASE':<6} {'TEMA ODS SORTEADO':<28} {'SORTEOS':<12} {'CARTON GANADOR':<18} {'PUNTAJE':<10}"
    )
    lines.append("-" * 140)
    if games:
        for index, game in enumerate(games, start=1):
            played_at = game.get("played_at")
            date_text = played_at.strftime("%Y-%m-%d") if played_at else "?"
            log_code = f"g-{index:03d}"
            pid = game.get("player_id", "?")
            player = player_map.get(pid, {})
            player_name = player.get("full_name", pid)
            state_code = player.get("state_code", "?")
            dimension = game.get("dimension", 5)
            base = f"{dimension}x{dimension}"
            sdg_name = get_sdg_name(game.get("sdg_id", 1))
            drawn_count = len(game.get("drawn_numbers", []))
            sorteos_text = f"{drawn_count} bolos"
            summary = calculate_game_summary(game)
            winner = summary["winning_card"]
            if winner == "main":
                carton = "Tablero 1"
                winning_card = game.get("main_card", [])
            elif winner == "complement":
                carton = "Tablero 2"
                winning_card = game.get("complement_card", [])
            else:
                carton = "Ninguno"
                winning_card = []
            winning_sum = card_sum(winning_card)
            carton_text = f"{carton} ({winning_sum})"
            puntaje = f"+{summary['total_points']}"
            lines.append(
                f"{date_text:<12} {log_code:<10} {player_name:<25} {state_code:<6} {base:<6} {sdg_name:<28} {sorteos_text:<12} {carton_text:<18} {puntaje:<10}"
            )
    else:
        lines.append("No hay partidas registradas.")
    lines.append("")
    lines.append("=" * 60)
    return "\n".join(lines)


def _build_report_text(
    players, games, section: str, date_start: str = "", date_end: str = ""
) -> str:
    """
    Genera el texto del informe para la seccion seleccionada.
    """
    if section == "players":
        return _build_players_report(players, games, date_start, date_end)
    if section == "top":
        return _build_top_report(players, games, date_start, date_end)
    if section == "frequency":
        return _build_frequency_report(games, date_start, date_end)
    if section == "history":
        return _build_history_report(players, games, date_start, date_end)
    return _build_players_report(players, games, date_start, date_end)


def _export_reports(state: Dict[str, Any]) -> str:
    """
    Exporta la seccion seleccionada a un archivo .txt y devuelve la ruta.

    El directorio `reports/` se crea si no existe.
    """
    report_dir = Path("reports")
    report_dir.mkdir(exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    section = state.get("selected_report", "all")
    file_path = report_dir / f"reporte_{section}_{timestamp}.txt"
    text = _build_report_text(
        state["players"],
        state["filtered_games"],
        section,
        state["inputs"].get("date_start", ""),
        state["inputs"].get("date_end", ""),
    )
    file_path.write_text(text, encoding="utf-8")
    return str(file_path)


def _apply_date_filter(state: Dict[str, Any]) -> None:
    """
    Aplica el filtro de fechas almacenado en `state['inputs']` y actualiza
    `state['filtered_games']`. En caso de error define `state['error_message']`.
    """
    from src.ui.app_state import set_error

    (games, error) = _filter_games_by_date(
        state["all_games"],
        state["inputs"].get("date_start", ""),
        state["inputs"].get("date_end", ""),
    )
    if error:
        set_error(state, error)
        return
    state["filtered_games"] = games
    state["error_message"] = ""


def _select_report(state: Dict[str, Any], section: str) -> None:
    """
    Cambia la seccion de informe seleccionada y limpia la ruta de exportacion.
    """
    state["selected_report"] = section
    state["report_export_path"] = None


def handle_event(state: Dict[str, Any], event: pygame.event.Event) -> str:
    """Procesar un evento de Pygame y devolver el nombre de la pantalla siguiente.

    Maneja clics del ratón y teclas (TAB, ENTER, ESCAPE) y actualiza el
    estado de filtros/selección/exportación.
    """
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
                if name in dict(_REPORT_SECTIONS):
                    _select_report(state, name)
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
            if focused in dict(_REPORT_SECTIONS):
                _select_report(state, focused)
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


def _draw_section_button(
    surface: pygame.Surface,
    label: str,
    rect: pygame.Rect,
    hovered: bool,
    focused: bool,
    selected: bool,
) -> None:
    """Dibujar un botón para seleccionar la sección del informe.

    El estilo cambia según si está seleccionado, enfocado o si el ratón lo
    pasa por encima.
    """
    bg_color = COLOR_PINE if selected else COLOR_WHITE
    text_color = COLOR_WHITE if selected else COLOR_CHARCOAL
    border_color = COLOR_PINE if focused or selected else COLOR_CHARCOAL
    pygame.draw.rect(surface, bg_color, rect)
    pygame.draw.rect(surface, border_color, rect, width=2)
    draw_text(surface, label, rect.center, font_size=16, color=text_color, center=True)
    if hovered and (not selected):
        pygame.draw.rect(surface, COLOR_PINE, rect, width=2)


def _draw_first_wrapped_line(
    surface: pygame.Surface,
    text: str,
    x: int,
    y: int,
    max_width: int,
    font_size: int = 11,
    color: Any = COLOR_CHARCOAL,
) -> None:
    """Dibujar sólo la primera línea resultante de `wrap_text` para `text`.

    Este helper reemplaza el patrón anterior que usaba `break`. Usamos una
    bandera local `drawn` para ejecutar trabajo solo en la primera iteración,
    preservando la semántica sin usar `break`.
    """
    drawn = False  # local flag to indicate the first line has been drawn
    for line in wrap_text(text, max_width, font_size=font_size):
        if drawn:
            # Skip further iterations once we've drawn the first line.
            continue
        draw_text(surface, line, (x, y), font_size=font_size, color=color)
        drawn = True


def _draw_players_report(surface, players, games, content_x, content_y, content_w):
    """Dibujar el informe de jugadores y partidas como una tabla.

    Presenta columnas con cédula, nombre, estado y cantidad de partidas.
    """
    draw_text(
        surface,
        "JUGADORES Y PARTIDAS REGISTRADOS",
        (content_x, content_y),
        font_size=18,
        color=COLOR_PINE,
    )
    draw_text(
        surface,
        f"Registros totales: {len(players)}",
        (content_x + content_w - 140, content_y + 5),
        font_size=12,
        color=COLOR_CHARCOAL,
    )
    columns = [
        ("CEDULA", 140),
        ("JUGADOR", 250),
        ("ESTADO", 100),
        ("PARTIDAS JUGADAS", 140),
    ]
    col_x = [content_x]
    for _, width in columns[:-1]:
        col_x.append(col_x[-1] + width)
    table_y = content_y + 35
    row_height = 26
    header_height = 26
    header_rect = pygame.Rect(content_x, table_y, content_w, header_height)
    pygame.draw.rect(surface, COLOR_PINE, header_rect)
    for idx, (label, width) in enumerate(columns):
        x = col_x[idx] + 4
        draw_text(
            surface,
            label,
            (x, table_y + header_height // 2),
            font_size=11,
            color=COLOR_WHITE,
        )
    table_y += header_height
    if not players:
        draw_text(
            surface,
            "No hay jugadores registrados.",
            (content_x, table_y + 8),
            font_size=18,
        )
        return
    for pid, name, count in _player_game_counts(players, games):
        row_rect = pygame.Rect(content_x, table_y, content_w, row_height)
        pygame.draw.rect(surface, COLOR_WHITE, row_rect)
        pygame.draw.rect(surface, COLOR_CHARCOAL, row_rect, width=1)
        player = _player_lookup(players).get(pid, {})
        state_code = player.get("state_code", "?")
        partidas = "partida" if count == 1 else "partidas"
        partidas_text = f"{count} {partidas}"
        row_values = [pid, name, state_code, partidas_text]
        for idx, (value, width) in enumerate(zip(row_values, [c[1] for c in columns])):
            x = col_x[idx] + 4
            text_y = table_y + row_height // 2
            # Draw only the first wrapped line for this cell. Use the
            # helper to replace the previous `break` pattern.
            _draw_first_wrapped_line(
                surface, value, x, text_y, width - 8, font_size=11, color=COLOR_CHARCOAL
            )
        table_y += row_height


def _draw_top_report(surface, players, games, content_x, content_y, content_w):
    """Dibujar el informe TOP 5 de jugadores como tarjetas de ranking.

    Muestra el puesto, nombre, región, partidas y puntos.
    """
    draw_text(
        surface,
        "TOP 5: JUGADORES DESTACADOS",
        (content_x, content_y),
        font_size=22,
        color=COLOR_PINE,
    )
    draw_text(
        surface,
        "Lideres acumulados registrados en JUGADORES.bin",
        (content_x, content_y + 26),
        font_size=12,
        color=COLOR_CHARCOAL,
    )
    y = content_y + 55
    top = _top_players(players, games)
    if not top:
        draw_text(surface, "No hay partidas registradas.", (content_x, y), font_size=18)
        return
    rank_colors = {1: COLOR_PINE, 2: COLOR_MOSS, 3: COLOR_SAGE_LIGHT}
    card_height = 54
    card_gap = 10
    for rank, (pid, name, state_code, game_count, points) in enumerate(top, start=1):
        card_rect = pygame.Rect(content_x, y, content_w, card_height)
        pygame.draw.rect(surface, COLOR_WHITE, card_rect)
        pygame.draw.rect(surface, COLOR_CHARCOAL, card_rect, width=1)
        circle_color = rank_colors.get(rank, COLOR_SAGE_LIGHT)
        circle_center = (content_x + 26, y + card_height // 2)
        pygame.draw.circle(surface, circle_color, circle_center, 16)
        draw_text(
            surface,
            str(rank),
            circle_center,
            font_size=16,
            color=COLOR_CHARCOAL,
            center=True,
        )
        draw_text(
            surface, name, (content_x + 55, y + 10), font_size=18, color=COLOR_CHARCOAL
        )
        partidas = "partida" if game_count == 1 else "partidas"
        draw_text(
            surface,
            f"Region: {state_code} · {game_count} {partidas}",
            (content_x + 55, y + 32),
            font_size=13,
            color=COLOR_CHARCOAL,
        )
        draw_text(
            surface,
            str(points),
            (content_x + content_w - 70, y + 10),
            font_size=22,
            color=COLOR_PINE,
        )
        draw_text(
            surface,
            "ODS",
            (content_x + content_w - 35, y + 10),
            font_size=10,
            color=COLOR_CHARCOAL,
        )
        draw_text(
            surface,
            "PUNTOS",
            (content_x + content_w - 48, y + 32),
            font_size=10,
            color=COLOR_CHARCOAL,
        )
        y += card_height + card_gap


def _draw_frequency_report(surface, games, content_x, content_y, content_w):
    """Dibujar un gráfico tipo Gantt con los números más frecuentes extraídos.

    Muestra barras proporcionales a la frecuencia de aparición por número.
    """
    draw_text(
        surface,
        "Frecuencia de numeros (TOP 10)",
        (content_x, content_y),
        font_size=22,
        color=COLOR_PINE,
    )
    y = content_y + 35
    gantt = _gantt_numbers(games)
    if not gantt:
        draw_text(surface, "No hay sorteos registrados.", (content_x, y), font_size=18)
        return
    max_count = max((count for (_, count) in gantt))
    row_height = 28
    number_box_size = 24
    rank_width = 35
    number_offset = 45
    bar_x = content_x + number_offset + number_box_size + 12
    bar_max_width = content_w - (bar_x - content_x) - 100
    bar_height = 18
    track_color = COLOR_SAGE_LIGHT
    for rank, (number, count) in enumerate(gantt, start=1):
        draw_text(
            surface, f"#{rank}", (content_x, y + 2), font_size=14, color=COLOR_CHARCOAL
        )
        number_rect = pygame.Rect(
            content_x + number_offset, y, number_box_size, number_box_size
        )
        pygame.draw.rect(surface, COLOR_PINE, number_rect)
        draw_text(
            surface,
            str(number),
            number_rect.center,
            font_size=14,
            color=COLOR_WHITE,
            center=True,
        )
        track_rect = pygame.Rect(bar_x, y + 3, bar_max_width, bar_height)
        pygame.draw.rect(surface, track_color, track_rect)
        fill_width = int(bar_max_width * count / max_count) if max_count else 0
        fill_rect = pygame.Rect(bar_x, y + 3, fill_width, bar_height)
        pygame.draw.rect(surface, COLOR_PINE, fill_rect)
        sorteos_text = f"{count} sorteo" if count == 1 else f"{count} sorteos"
        draw_text(
            surface,
            sorteos_text,
            (bar_x + bar_max_width + 10, y + 3),
            font_size=14,
            color=COLOR_CHARCOAL,
        )
        y += row_height
    note_y = y + 10
    draw_text(
        surface,
        "Nota del Algoritmo:",
        (content_x, note_y),
        font_size=14,
        color=COLOR_PINE,
    )
    note_lines = wrap_text(
        "La aleatoriedad de la tombola se aproxima a la campana estadistica en sesiones largas. Los datos se actualizan dinamicamente.",
        content_w,
        font_size=12,
    )
    for line in note_lines:
        note_y += 18
        draw_text(
            surface, line, (content_x, note_y), font_size=12, color=COLOR_CHARCOAL
        )


def _draw_history_report(surface, players, games, content_x, content_y, content_w):
    """Dibujar el informe de historial de partidas como una tabla.

    Cada fila representa una partida con fecha, jugador, tema ODS y puntaje.
    """
    player_map = _player_lookup(players)
    draw_text(
        surface,
        "HISTORIAL HISTORICO DE PARTIDAS (JUEGOS.BIN)",
        (content_x, content_y),
        font_size=18,
        color=COLOR_PINE,
    )
    draw_text(
        surface,
        "Bitacora de auditoria Federal del juego educativo",
        (content_x, content_y + 22),
        font_size=12,
        color=COLOR_CHARCOAL,
    )
    total_text = f"Registros totales: {len(games)}"
    draw_text(
        surface,
        total_text,
        (content_x + content_w - 140, content_y + 5),
        font_size=12,
        color=COLOR_CHARCOAL,
    )
    columns = [
        ("FECHA", 65),
        ("CODIGO LOG", 60),
        ("JUGADOR", 125),
        ("ESTADO", 50),
        ("BASE N", 50),
        ("TEMA ODS SORTEADO", 125),
        ("SORTEOS REALIZADOS", 75),
        ("CARTON GANADOR", 85),
        ("PUNTAJE", 49),
    ]
    col_x = [content_x]
    for _, width in columns[:-1]:
        col_x.append(col_x[-1] + width)
    table_y = content_y + 55
    row_height = 26
    header_height = 26
    header_rect = pygame.Rect(content_x, table_y, content_w, header_height)
    pygame.draw.rect(surface, COLOR_PINE, header_rect)
    for idx, (label, width) in enumerate(columns):
        x = col_x[idx] + 4
        draw_text(
            surface,
            label,
            (x, table_y + header_height // 2),
            font_size=11,
            color=COLOR_WHITE,
        )
    table_y += header_height
    if not games:
        draw_text(
            surface,
            "No hay partidas registradas.",
            (content_x, table_y + 8),
            font_size=18,
        )
        return
    for index, game in enumerate(games, start=1):
        row_rect = pygame.Rect(content_x, table_y, content_w, row_height)
        pygame.draw.rect(surface, COLOR_WHITE, row_rect)
        pygame.draw.rect(surface, COLOR_CHARCOAL, row_rect, width=1)
        played_at = game.get("played_at")
        date_text = played_at.strftime("%Y-%m-%d") if played_at else "?"
        log_code = f"g-{index:03d}"
        pid = game.get("player_id", "?")
        player = player_map.get(pid, {})
        player_name = player.get("full_name", pid)
        state_code = player.get("state_code", "?")
        dimension = game.get("dimension", 5)
        base = f"{dimension}x{dimension}"
        sdg_name = get_sdg_name(game.get("sdg_id", 1))
        drawn_count = len(game.get("drawn_numbers", []))
        sorteos_text = f"{drawn_count} bolos"
        summary = calculate_game_summary(game)
        winner = summary["winning_card"]
        if winner == "main":
            carton = "Tablero 1"
            winning_card = game.get("main_card", [])
        elif winner == "complement":
            carton = "Tablero 2"
            winning_card = game.get("complement_card", [])
        else:
            carton = "Ninguno"
            winning_card = []
        winning_sum = card_sum(winning_card)
        carton_text = f"{carton} ({winning_sum})"
        puntaje = f"+{summary['total_points']}"
        row_values = [
            date_text,
            log_code,
            player_name,
            state_code,
            base,
            sdg_name,
            sorteos_text,
            carton_text,
            puntaje,
        ]
        for idx, (value, width) in enumerate(zip(row_values, [c[1] for c in columns])):
            x = col_x[idx] + 4
            text_y = table_y + row_height // 2
            # Draw only the first wrapped line for this cell. We call the
            # helper `_draw_first_wrapped_line` which uses a local boolean
            # flag to avoid `break` while preserving the original behavior.
            _draw_first_wrapped_line(
                surface, value, x, text_y, width - 8, font_size=11, color=COLOR_CHARCOAL
            )
        table_y += row_height


def _draw_report_content(
    surface: pygame.Surface,
    section: str,
    players,
    games,
    content_x: int,
    content_y: int,
    content_w: int,
) -> None:
    """Dibujar el área de contenido para la sección de informe seleccionada."""
    if section == "players":
        _draw_players_report(surface, players, games, content_x, content_y, content_w)
    elif section == "top":
        _draw_top_report(surface, players, games, content_x, content_y, content_w)
    elif section == "frequency":
        _draw_frequency_report(surface, games, content_x, content_y, content_w)
    elif section == "history":
        _draw_history_report(surface, players, games, content_x, content_y, content_w)
    else:
        _draw_players_report(surface, players, games, content_x, content_y, content_w)


def draw(surface: pygame.Surface, state: Dict[str, Any]) -> None:
    """Renderizar la pantalla de reportes.

    Dibuja controles de filtro, selección de sección y la tabla o gráfico
    correspondiente a la sección activa.
    """
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
    hovered = {name: rect.collidepoint(mouse_pos) for (name, rect) in rects.items()}
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
    selected = state.get("selected_report", "all")
    for section, label in _REPORT_SECTIONS:
        _draw_section_button(
            surface,
            label,
            rects[section],
            hovered=hovered.get(section, False),
            focused=focused == section,
            selected=selected == section,
        )
    content_x = 280
    content_y = 185
    content_w = WINDOW_WIDTH - content_x - 60
    content_h = WINDOW_HEIGHT - content_y - 120
    content_rect = pygame.Rect(content_x, content_y, content_w, content_h)
    pygame.draw.rect(surface, COLOR_WHITE, content_rect)
    pygame.draw.rect(surface, COLOR_CHARCOAL, content_rect, width=1)
    players = state.get("players", [])
    games = state.get("filtered_games", [])
    _draw_report_content(
        surface,
        selected,
        players,
        games,
        content_x + 15,
        content_y + 15,
        content_w - 30,
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
            (WINDOW_WIDTH // 2, 600),
            font_size=16,
            color=COLOR_PINE,
            center=True,
        )
    if state.get("error_message"):
        draw_error_message(
            surface, state["error_message"], (WINDOW_WIDTH // 2, 625), font_size=20
        )
    sdg_id = state.get("session", {}).get("sdg_id", 1)
    draw_message_panel(surface, state, sdg_id=sdg_id)
