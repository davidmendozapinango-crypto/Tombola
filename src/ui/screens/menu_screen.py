"""Main menu screen (non-OOP) with card-style grid and active game config."""
from typing import Any, Callable, Dict, Set, Tuple
import pygame
from src.auth.session import get_player, logout
from src.config import COLOR_CHARCOAL, COLOR_MINT, COLOR_MOSS, COLOR_PINE, COLOR_SAGE_LIGHT, COLOR_WHITE, STATE_CODES, WINDOW_HEIGHT, WINDOW_WIDTH
from src.core.card import make_cards
from src.core.card_figures import get_card_type, get_figure_pattern
from src.ods.data import get_sdg_color, get_sdg_name, list_sdg_ids
from src.persistence.games import calculate_game_summary, load_games
from src.ui.app_state import cycle_focus, get_focused, set_error
from src.ui.common import draw_button, draw_error_message, draw_message_panel, draw_text
_MENU_CARDS: Dict[str, Tuple[str, str, Callable[[pygame.Surface, pygame.Rect], None]]] = {'play': ('Iniciar Partida de Tombola', 'Sortea los numeros del carton NxN alineado al ODS con el llenado seleccionado.', lambda surface, rect: _draw_play_icon(surface, rect)), 'reports': ('Estadisticas e Historicos', 'Analiza el grafico de barras horizontales, revisa el ranking general y el registro binario guardado de partidas.', lambda surface, rect: _draw_chart_icon(surface, rect)), 'logout': ('Cerrar Sesion Activa', 'Cierra tu sesion del bioma de simulacion de forma segura y vuelve a la pantalla de ingreso.', lambda surface, rect: _draw_logout_icon(surface, rect)), 'exit': ('Salir del Sistema', 'Finaliza la aplicacion y regresa al escritorio.', lambda surface, rect: _draw_exit_icon(surface, rect))}

def _draw_play_icon(surface: pygame.Surface, rect: pygame.Rect) -> None:
    """Draw a simple play triangle icon."""
    center = rect.center
    size = 18
    points = [(center[0] - size // 2, center[1] - size), (center[0] - size // 2, center[1] + size), (center[0] + size, center[1])]
    pygame.draw.polygon(surface, COLOR_PINE, points)

def _draw_chart_icon(surface: pygame.Surface, rect: pygame.Rect) -> None:
    """Draw a simple bar chart icon."""
    (x, y) = (rect.x + 10, rect.y + 8)
    bar_width = 8
    bars = [(0, 22), (12, 14), (24, 28)]
    for (offset, height) in bars:
        bar_rect = pygame.Rect(x + offset, y + (32 - height), bar_width, height)
        pygame.draw.rect(surface, COLOR_PINE, bar_rect)

def _draw_logout_icon(surface: pygame.Surface, rect: pygame.Rect) -> None:
    """Draw a person icon with a logout arrow."""
    (cx, cy) = rect.center
    pygame.draw.circle(surface, COLOR_PINE, (cx - 2, cy - 6), 6)
    body_rect = pygame.Rect(cx - 12, cy + 1, 20, 14)
    pygame.draw.ellipse(surface, COLOR_PINE, body_rect)
    box_rect = pygame.Rect(cx + 6, cy - 8, 12, 10)
    pygame.draw.rect(surface, COLOR_PINE, box_rect, width=2, border_radius=1)
    arrow_start = (cx + 10, cy - 3)
    arrow_end = (cx + 18, cy - 3)
    pygame.draw.line(surface, COLOR_PINE, arrow_start, arrow_end, width=2)
    pygame.draw.polygon(surface, COLOR_PINE, [(cx + 18, cy - 6), (cx + 18, cy), (cx + 23, cy - 3)])

def _draw_exit_icon(surface: pygame.Surface, rect: pygame.Rect) -> None:
    """Draw a person icon with a door."""
    (cx, cy) = rect.center
    pygame.draw.circle(surface, COLOR_PINE, (cx - 8, cy - 5), 5)
    body_rect = pygame.Rect(cx - 15, cy + 2, 14, 11)
    pygame.draw.ellipse(surface, COLOR_PINE, body_rect)
    door_rect = pygame.Rect(cx + 2, cy - 12, 14, 24)
    pygame.draw.rect(surface, COLOR_PINE, door_rect, width=2, border_radius=1)
    pygame.draw.circle(surface, COLOR_PINE, (cx + 11, cy), 2)

def _draw_globe_icon(surface: pygame.Surface, rect: pygame.Rect) -> None:
    """Draw a small globe icon inside a badge."""
    (cx, cy) = rect.center
    radius = 8
    pygame.draw.circle(surface, COLOR_MOSS, (cx, cy), radius, width=2)
    pygame.draw.line(surface, COLOR_MOSS, (cx, cy - radius), (cx, cy + radius), 1)
    pygame.draw.line(surface, COLOR_MOSS, (cx - radius, cy), (cx + radius, cy), 1)
    pygame.draw.arc(surface, COLOR_MOSS, (cx - 5, cy - 10, 10, 20), 0, 3.14, 1)
    pygame.draw.arc(surface, COLOR_MOSS, (cx - 5, cy - 10, 10, 20), 3.14, 6.28, 1)

def _draw_medal_icon(surface: pygame.Surface, rect: pygame.Rect) -> None:
    """Draw a small ribbon medal icon."""
    (cx, cy) = rect.center
    pygame.draw.circle(surface, COLOR_PINE, (cx, cy - 2), 10)
    pygame.draw.polygon(surface, COLOR_PINE, [(cx - 8, cy + 8), (cx - 4, cy + 8), (cx - 6, cy + 18)])
    pygame.draw.polygon(surface, COLOR_PINE, [(cx + 4, cy + 8), (cx + 8, cy + 8), (cx + 6, cy + 18)])

def _player_total_points(player_id: str) -> int:
    """Return accumulated total points for the given player."""
    total = 0
    for game in load_games():
        if game.get('player_id') == player_id:
            total += calculate_game_summary(game).get('total_points', 0)
    return total

def _layout() -> Dict[str, pygame.Rect]:
    """Return the UI rectangles for the menu screen."""
    left_x = 60
    left_y = 198
    card_width = 420
    card_height = 110
    card_gap = 20
    right_x = 520
    right_y = 198
    right_w = 444
    right_h = 468
    return {'play': pygame.Rect(left_x, left_y, card_width, card_height), 'reports': pygame.Rect(left_x, left_y + card_height + card_gap, card_width, card_height), 'logout': pygame.Rect(left_x, left_y + 2 * (card_height + card_gap), card_width, card_height), 'exit': pygame.Rect(left_x, left_y + 3 * (card_height + card_gap), card_width, card_height), 'panel': pygame.Rect(right_x, right_y, right_w, right_h), 'dim_left': pygame.Rect(right_x + 20, right_y + 110, 40, 32), 'dim_value': pygame.Rect(right_x + 70, right_y + 110, 100, 32), 'dim_right': pygame.Rect(right_x + 180, right_y + 110, 40, 32), 'sdg_left': pygame.Rect(right_x + 20, right_y + 190, 40, 32), 'sdg_value': pygame.Rect(right_x + 70, right_y + 190, 300, 32), 'sdg_right': pygame.Rect(right_x + 380, right_y + 190, 40, 32)}

def _dimensions() -> list[int]:
    return [5, 7, 9, 11, 13, 15]

def _regenerate_cards(state: Dict[str, Any]) -> None:
    """Regenerate the main/complement cards based on current menu config."""
    config = state.get('menu_config', {})
    dimension = config.get('dimension', 5)
    sdg_id = config.get('sdg_id', 1)
    card_type = get_card_type(sdg_id)
    main_pattern = get_figure_pattern(card_type, is_main=True, dimension=dimension)
    complement_pattern = get_figure_pattern(card_type, is_main=False, dimension=dimension)
    cards = make_cards(dimension, main_pattern, complement_pattern)
    state['session']['dimension'] = dimension
    state['session']['sdg_id'] = sdg_id
    state['session']['main_card'] = cards['main']
    state['session']['complement_card'] = cards['complement']
    state['session']['drawn_numbers'] = []
    state['session']['marked_main'] = set()
    state['session']['marked_complement'] = set()
    state['session']['winning_card'] = None
    state['session']['game_over'] = False

def init_menu(state: Dict[str, Any]) -> None:
    """Initialize menu screen state."""
    state['inputs'] = {}
    state['menu_config'] = {'dimension': 5, 'sdg_id': 1}
    state['focusable'] = ['play', 'reports', 'logout', 'exit', 'dim_left', 'dim_right', 'sdg_left', 'sdg_right']
    state['focus_index'] = 0
    state['rects'] = _layout()
    player = get_player(state['session'])
    state['player_points'] = _player_total_points(player['player_id']) if player else 0
    _regenerate_cards(state)

def _change_dimension(state: Dict[str, Any], direction: int) -> None:
    dimensions = _dimensions()
    current = state['menu_config']['dimension']
    index = dimensions.index(current)
    new_index = max(0, min(len(dimensions) - 1, index + direction))
    state['menu_config']['dimension'] = dimensions[new_index]
    _regenerate_cards(state)

def _change_sdg(state: Dict[str, Any], direction: int) -> None:
    sdg_ids = list_sdg_ids()
    current = state['menu_config']['sdg_id']
    index = sdg_ids.index(current)
    new_index = (index + direction) % len(sdg_ids)
    state['menu_config']['sdg_id'] = sdg_ids[new_index]
    _regenerate_cards(state)

def _can_play(state: Dict[str, Any]) -> bool:
    """Return True when dimension and ODS are configured."""
    config = state.get('menu_config', {})
    return bool(config.get('dimension') and config.get('sdg_id'))

def _activate(state: Dict[str, Any], name: str) -> str:
    """Activate a menu option or config control."""
    if name == 'play':
        if not _can_play(state):
            set_error(state, 'Seleccione dimension y ODS antes de jugar.')
            return state['current_screen']
        return 'game'
    if name == 'reports':
        return 'reports'
    if name == 'logout':
        logout(state['session'])
        return 'login'
    if name == 'exit':
        state['running'] = False
        return 'exit'
    if name == 'dim_left':
        _change_dimension(state, -1)
    elif name == 'dim_right':
        _change_dimension(state, 1)
    elif name == 'sdg_left':
        _change_sdg(state, -1)
    elif name == 'sdg_right':
        _change_sdg(state, 1)
    return state['current_screen']

def handle_event(state: Dict[str, Any], event: pygame.event.Event) -> str:
    """Process a Pygame event and return the next screen name."""
    rects = state.get('rects') or _layout()
    state['rects'] = rects
    focused = get_focused(state)
    if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
        for (name, rect) in rects.items():
            if name == 'panel':
                continue
            if rect.collidepoint(event.pos):
                if name in state['focusable']:
                    state['focus_index'] = state['focusable'].index(name)
                return _activate(state, name)
    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_TAB:
            cycle_focus(state, 1)
            return state['current_screen']
        if event.key == pygame.K_ESCAPE:
            logout(state['session'])
            return 'login'
        if event.key in (pygame.K_RETURN, pygame.K_SPACE):
            return _activate(state, focused)
    return state['current_screen']

def _draw_badge(surface: pygame.Surface, rect: pygame.Rect, text: str, icon_drawer: Callable[[pygame.Surface, pygame.Rect], None]) -> None:
    """Draw a rounded pill badge with an icon and text."""
    pygame.draw.rect(surface, COLOR_PINE, rect, border_radius=16)
    pygame.draw.rect(surface, COLOR_MOSS, rect, width=2, border_radius=16)
    icon_rect = pygame.Rect(rect.x + 8, rect.y + 4, rect.height - 8, rect.height - 8)
    icon_drawer(surface, icon_rect)
    text_x = rect.x + rect.height + 2 + (rect.width - rect.height - 2) // 2
    draw_text(surface, text, (text_x, rect.centery), font_size=11, color=COLOR_MOSS, center=True)

def _draw_header(surface: pygame.Surface, state: Dict[str, Any]) -> None:
    """Draw the main menu header banner with player info and score."""
    header_rect = pygame.Rect(40, 20, WINDOW_WIDTH - 80, 160)
    pygame.draw.rect(surface, COLOR_PINE, header_rect, border_radius=16)
    player = get_player(state['session'])
    full_name = player['full_name'] if player else 'Jugador'
    state_code = player.get('state_code', 'CCS') if player else 'CCS'
    state_name = STATE_CODES.get(state_code, state_code)
    points = state.get('player_points', 0)
    globe_rect = pygame.Rect(header_rect.x + 25, header_rect.y + 20, 215, 28)
    state_rect = pygame.Rect(globe_rect.right + 12, header_rect.y + 20, 115, 28)
    _draw_badge(surface, globe_rect, 'SECTOR EDUCATIVO VENEZOLANO', _draw_globe_icon)
    _draw_badge(surface, state_rect, f'ESTADO {state_code}', _draw_globe_icon)
    draw_text(surface, f'Bienvenido, {full_name}', (header_rect.x + 25, header_rect.y + 62), font_size=34, color=COLOR_WHITE, center=False)
    subtitle_x = header_rect.x + 25
    subtitle_y = header_rect.y + 100
    line1_prefix = 'Usted representa la vanguardia del cambio. Su pertenencia al estado '
    line2 = 'impulsa la consciencia eco-social indispensable para el cumplimiento del Plan Patria Sostenible.'
    font = pygame.font.SysFont('Arial', 13)
    prefix_width = font.size(line1_prefix)[0]
    draw_text(surface, line1_prefix, (subtitle_x, subtitle_y), font_size=13, color=COLOR_WHITE, center=False)
    draw_text(surface, state_name, (subtitle_x + prefix_width, subtitle_y), font_size=13, color=COLOR_MOSS, center=False)
    draw_text(surface, line2, (subtitle_x, subtitle_y + 18), font_size=13, color=COLOR_WHITE, center=False)
    score_rect = pygame.Rect(header_rect.right - 175, header_rect.y + 25, 150, 110)
    pygame.draw.rect(surface, (76, 122, 79), score_rect, border_radius=12)
    icon_box = pygame.Rect(score_rect.x + 10, score_rect.centery - 20, 40, 40)
    pygame.draw.rect(surface, (107, 156, 95), icon_box, border_radius=10)
    _draw_medal_icon(surface, icon_box)
    text_x = icon_box.right + 10
    draw_text(surface, 'PUNTOS', (text_x, score_rect.y + 22), font_size=9, color=COLOR_WHITE, center=False)
    draw_text(surface, 'MUNDIALES', (text_x, score_rect.y + 35), font_size=9, color=COLOR_WHITE, center=False)
    draw_text(surface, f'{points} ODS', (text_x, score_rect.y + 58), font_size=18, color=COLOR_WHITE, center=False)

def _draw_card(surface: pygame.Surface, rect: pygame.Rect, title: str, description: str, icon_drawer: Callable[[pygame.Surface, pygame.Rect], None], hovered: bool, focused: bool) -> None:
    """Draw a single menu card."""
    bg_color = COLOR_WHITE
    border_color = COLOR_PINE if hovered or focused else COLOR_SAGE_LIGHT
    shadow_offset = 4 if hovered else 2
    shadow_rect = rect.copy()
    shadow_rect.x += shadow_offset
    shadow_rect.y += shadow_offset
    pygame.draw.rect(surface, COLOR_SAGE_LIGHT, shadow_rect, border_radius=12)
    pygame.draw.rect(surface, bg_color, rect, border_radius=12)
    pygame.draw.rect(surface, border_color, rect, width=2, border_radius=12)
    icon_rect = pygame.Rect(rect.x + 20, rect.y + 28, 48, 48)
    pygame.draw.circle(surface, COLOR_MINT, icon_rect.center, 24)
    icon_drawer(surface, icon_rect)
    draw_text(surface, title, (rect.x + 82, rect.y + 32), font_size=18, color=COLOR_PINE)
    max_width = rect.width - 100
    y_offset = 58
    for line in _wrap_description(description, max_width):
        draw_text(surface, line, (rect.x + 82, rect.y + y_offset), font_size=12, color=COLOR_CHARCOAL)
        y_offset += 16

def _wrap_description(text: str, max_width: int) -> list[str]:
    """Simple word wrap for card descriptions."""
    words = text.split()
    lines: list[str] = []
    current = ''
    for word in words:
        test = f'{current} {word}'.strip()
        if len(test) * 7 > max_width and current:
            lines.append(current)
            current = word
        else:
            current = test
    if current:
        lines.append(current)
    return lines[:3]

def _draw_preview_card(surface: pygame.Surface, card: Any, top_left: Tuple[int, int], cell_size: int, label: str) -> None:
    """Draw a small card preview for the menu config panel."""
    dimension = len(card)
    pattern: Set[Tuple[int, int]] = set()
    for (row_index, row) in enumerate(card):
        for (col_index, value) in enumerate(row):
            if value is not None:
                pattern.add((row_index, col_index))
    label_rect = draw_text(surface, label, (top_left[0], top_left[1] - 20), font_size=12, color=COLOR_CHARCOAL)
    for row in range(dimension):
        for col in range(dimension):
            rect = pygame.Rect(top_left[0] + col * cell_size, top_left[1] + row * cell_size, cell_size, cell_size)
            is_figure = (row, col) in pattern
            fill_color = COLOR_PINE if is_figure else COLOR_WHITE
            pygame.draw.rect(surface, fill_color, rect)
            pygame.draw.rect(surface, COLOR_CHARCOAL, rect, width=1)
            value = card[row][col]
            if value is not None:
                draw_text(surface, str(value), rect.center, font_size=max(8, cell_size // 2), color=COLOR_WHITE, center=True)

def _draw_config_panel(surface: pygame.Surface, state: Dict[str, Any], rects: Dict[str, pygame.Rect], hovered: Dict[str, bool], focused: str) -> None:
    """Draw the right-side active configuration panel."""
    panel = rects['panel']
    pygame.draw.rect(surface, COLOR_WHITE, panel, border_radius=12)
    pygame.draw.rect(surface, COLOR_SAGE_LIGHT, panel, width=2, border_radius=12)
    draw_text(surface, 'Configuracion Activa de la Tombola ODS', (panel.x + 20, panel.y + 20), font_size=20, color=COLOR_PINE)
    draw_text(surface, 'Alinea tu bioma educativo antes de iniciar el sorteo', (panel.x + 20, panel.y + 46), font_size=12, color=COLOR_CHARCOAL)
    config = state.get('menu_config', {})
    dimension = config.get('dimension', 5)
    sdg_id = config.get('sdg_id', 1)
    sdg_name = get_sdg_name(sdg_id)
    draw_text(surface, '1. DIMENSION DEL CARTON (N x N)', (panel.x + 20, panel.y + 80), font_size=14, color=COLOR_PINE)
    draw_button(surface, '<', rects['dim_left'], hovered=hovered['dim_left'], focused=focused == 'dim_left')
    pygame.draw.rect(surface, COLOR_MINT, rects['dim_value'])
    pygame.draw.rect(surface, COLOR_CHARCOAL, rects['dim_value'], width=1)
    draw_text(surface, f'{dimension} x {dimension}', rects['dim_value'].center, font_size=16, color=COLOR_CHARCOAL, center=True)
    draw_button(surface, '>', rects['dim_right'], hovered=hovered['dim_right'], focused=focused == 'dim_right')
    draw_text(surface, '2. SELECCION TEMATICA DE LOS ODS', (panel.x + 20, panel.y + 160), font_size=14, color=COLOR_PINE)
    draw_button(surface, '<', rects['sdg_left'], hovered=hovered['sdg_left'], focused=focused == 'sdg_left')
    sdg_color = get_sdg_color(sdg_id)
    pygame.draw.rect(surface, sdg_color, rects['sdg_value'])
    pygame.draw.rect(surface, COLOR_CHARCOAL, rects['sdg_value'], width=1)
    draw_text(surface, f'ODS {sdg_id}: {sdg_name}', rects['sdg_value'].center, font_size=14, color=COLOR_WHITE, center=True)
    draw_button(surface, '>', rects['sdg_right'], hovered=hovered['sdg_right'], focused=focused == 'sdg_right')
    draw_text(surface, '3. VISTA PREVIA DEL CARTON', (panel.x + 20, panel.y + 250), font_size=14, color=COLOR_PINE)
    main_card = state['session'].get('main_card')
    complement_card = state['session'].get('complement_card')
    if main_card and complement_card:
        cell_size = max(12, min(18, 140 // dimension))
        _draw_preview_card(surface, main_card, (panel.x + 30, panel.y + 280), cell_size, 'Principal')
        _draw_preview_card(surface, complement_card, (panel.x + 230, panel.y + 280), cell_size, 'Complemento')

def draw(surface: pygame.Surface, state: Dict[str, Any]) -> None:
    """Render the main menu screen with card-style grid and config panel."""
    surface.fill(COLOR_MINT)
    rects = _layout()
    state['rects'] = rects
    _draw_header(surface, state)
    mouse_pos = pygame.mouse.get_pos()
    hovered = {name: rect.collidepoint(mouse_pos) for (name, rect) in rects.items()}
    focused = get_focused(state)
    for (name, rect) in rects.items():
        if name not in _MENU_CARDS:
            continue
        (title, description, icon_drawer) = _MENU_CARDS[name]
        _draw_card(surface, rect, title, description, icon_drawer, hovered=hovered[name], focused=focused == name)
    _draw_config_panel(surface, state, rects, hovered, focused)
    if state.get('info_message'):
        _draw_info_message(surface, state['info_message'], (WINDOW_WIDTH // 2, WINDOW_HEIGHT - 105), font_size=20)
    if state.get('error_message'):
        draw_error_message(surface, state['error_message'], (WINDOW_WIDTH // 2, WINDOW_HEIGHT - 85), font_size=20)
    sdg_id = state.get('menu_config', {}).get('sdg_id', 1)
    draw_message_panel(surface, state, sdg_id=sdg_id)
from src.ui.common import draw_text as _draw_text

def _draw_info_message(surface, message, position, font_size=20):
    _draw_text(surface, message, position, font_size=font_size, color=COLOR_PINE)