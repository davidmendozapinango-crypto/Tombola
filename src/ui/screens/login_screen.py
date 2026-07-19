"""Login screen (non-OOP) with educational header and account panel."""

from typing import Any, Dict

import pygame

from src.auth.session import login
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
from src.persistence.players import ensure_default_players, find_player, load_players
from src.ui.app_state import cycle_focus, get_focused, is_focused, set_error, set_info
from src.ui.common import (
    draw_button,
    draw_error_message,
    draw_input,
    draw_message_panel,
    draw_text,
    get_font,
)


def _layout() -> Dict[str, pygame.Rect]:
    """Return the UI rectangles for the redesigned login screen."""
    panel_w = 430
    panel_h = 470
    left_x = (WINDOW_WIDTH - panel_w) // 2
    left_y = (WINDOW_HEIGHT - 70 - panel_h) // 2 + 40
    return {
        # Tabs
        "tab_login": pygame.Rect(WINDOW_WIDTH // 2 - 220, 95, 220, 40),
        "tab_register": pygame.Rect(WINDOW_WIDTH // 2, 95, 220, 40),
        # Left panel
        "panel": pygame.Rect(left_x, left_y, panel_w, panel_h),
        "selector_left": pygame.Rect(left_x + 20, left_y + 135, 32, 32),
        "selector_value": pygame.Rect(left_x + 57, left_y + 135, 316, 32),
        "selector_right": pygame.Rect(left_x + 378, left_y + 135, 32, 32),
        "key": pygame.Rect(left_x + 20, left_y + 225, 390, 38),
        "register_link": pygame.Rect(left_x + 20, left_y + 285, 390, 28),
        "login": pygame.Rect(left_x + 20, left_y + 335, 390, 45),
        "menu": pygame.Rect(left_x + 20, left_y + 390, 390, 45),
    }


def _draw_globe_icon(surface: pygame.Surface, rect: pygame.Rect) -> None:
    """Draw a small globe icon inside a badge."""
    cx, cy = rect.center
    radius = 10
    pygame.draw.circle(surface, COLOR_MOSS, (cx, cy), radius, width=2)
    pygame.draw.line(surface, COLOR_MOSS, (cx, cy - radius), (cx, cy + radius), 1)
    pygame.draw.line(surface, COLOR_MOSS, (cx - radius, cy), (cx + radius, cy), 1)
    pygame.draw.arc(surface, COLOR_MOSS, (cx - 6, cy - 12, 12, 24), 0, 3.14, 1)
    pygame.draw.arc(surface, COLOR_MOSS, (cx - 6, cy - 12, 12, 24), 3.14, 6.28, 1)


def _draw_key_icon(surface: pygame.Surface, rect: pygame.Rect) -> None:
    """Draw a simple key icon."""
    cx, cy = rect.center
    pygame.draw.circle(surface, COLOR_PINE, (cx - 6, cy), 5)
    pygame.draw.line(surface, COLOR_PINE, (cx - 6, cy), (cx + 8, cy), 3)
    pygame.draw.rect(surface, COLOR_PINE, (cx + 6, cy - 3, 6, 6))


def _draw_shield_icon(surface: pygame.Surface, rect: pygame.Rect) -> None:
    """Draw a simple shield icon."""
    cx, cy = rect.center
    pygame.draw.polygon(
        surface,
        COLOR_WHITE,
        [
            (cx, cy - 10),
            (cx + 9, cy - 4),
            (cx + 9, cy + 4),
            (cx, cy + 10),
            (cx - 9, cy + 4),
            (cx - 9, cy - 4),
        ],
    )
    pygame.draw.circle(surface, COLOR_PINE, (cx, cy), 3)


def _draw_header(surface: pygame.Surface, state: Dict[str, Any]) -> None:
    """Draw the top educational header."""
    header_rect = pygame.Rect(0, 0, WINDOW_WIDTH, 75)
    pygame.draw.rect(surface, COLOR_PINE, header_rect)

    icon_rect = pygame.Rect(25, 18, 38, 38)
    pygame.draw.circle(surface, COLOR_MOSS, icon_rect.center, 18)
    _draw_globe_icon(surface, icon_rect)

    draw_text(
        surface,
        "SIMULADOR EDUCATIVO",
        (75, 18),
        font_size=11,
        color=COLOR_MOSS,
        center=False,
    )
    draw_text(
        surface,
        "Tómbola ODS",
        (75, 34),
        font_size=22,
        color=COLOR_WHITE,
        center=False,
    )


def _draw_tabs(
    surface: pygame.Surface, rects: Dict[str, pygame.Rect], hovered: Dict[str, bool]
) -> None:
    """Draw the login/register tabs."""
    login_rect = rects["tab_login"]
    register_rect = rects["tab_register"]

    pygame.draw.rect(surface, COLOR_PINE, login_rect, border_radius=8)
    pygame.draw.rect(surface, COLOR_PINE, login_rect, width=2, border_radius=8)
    draw_text(
        surface,
        "Identidad Configuracion",
        (login_rect.centerx, login_rect.y + 12),
        font_size=13,
        color=COLOR_WHITE,
        center=True,
    )
    draw_text(
        surface,
        "(Login)",
        (login_rect.centerx, login_rect.y + 27),
        font_size=11,
        color=COLOR_MOSS,
        center=True,
    )

    bg = (107, 156, 95) if hovered["tab_register"] else COLOR_SAGE_LIGHT
    pygame.draw.rect(surface, bg, register_rect, border_radius=8)
    pygame.draw.rect(surface, COLOR_PINE, register_rect, width=2, border_radius=8)
    draw_text(
        surface,
        "Registrar Jugador (Nuevo)",
        register_rect.center,
        font_size=13,
        color=COLOR_PINE,
        center=True,
    )


def _draw_left_panel(
    surface: pygame.Surface,
    state: Dict[str, Any],
    rects: Dict[str, pygame.Rect],
    hovered: Dict[str, bool],
    focused: str,
) -> None:
    """Draw the left login panel."""
    panel_rect = rects["panel"]
    shadow_rect = panel_rect.copy()
    shadow_rect.x += 4
    shadow_rect.y += 4
    pygame.draw.rect(surface, COLOR_SAGE_LIGHT, shadow_rect, border_radius=16)
    pygame.draw.rect(surface, COLOR_WHITE, panel_rect, border_radius=16)
    pygame.draw.rect(surface, COLOR_SAGE_LIGHT, panel_rect, width=2, border_radius=16)

    # Title
    icon_rect = pygame.Rect(panel_rect.x + 20, panel_rect.y + 20, 28, 28)
    pygame.draw.circle(surface, COLOR_MINT, icon_rect.center, 14)
    _draw_key_icon(surface, icon_rect)
    draw_text(
        surface,
        "Ingreso Jugador",
        (panel_rect.x + 56, panel_rect.y + 24),
        font_size=22,
        color=COLOR_PINE,
        center=False,
    )
    italic_font = get_font(13)
    italic_font.set_italic(True)
    subtitle = italic_font.render("Acceso JUGADORES.bin", True, COLOR_CHARCOAL)
    surface.blit(subtitle, (panel_rect.x + 56, panel_rect.y + 48))

    # Separator
    pygame.draw.line(
        surface,
        COLOR_SAGE_LIGHT,
        (panel_rect.x + 20, panel_rect.y + 85),
        (panel_rect.right - 20, panel_rect.y + 85),
        1,
    )

    # Player selector
    draw_text(
        surface,
        "ELEGIR JUGADOR REGISTRADO",
        (panel_rect.x + 20, panel_rect.y + 105),
        font_size=12,
        color=COLOR_PINE,
        center=False,
    )
    players = state.get("players", [])
    index = state.get("selected_player_index", 0)
    label = "Sin jugadores"
    if players:
        label = f"{players[index]['full_name']} (V-{players[index]['player_id']})"
    draw_button(surface, "<", rects["selector_left"], hovered=hovered["selector_left"])
    pygame.draw.rect(surface, COLOR_MINT, rects["selector_value"])
    pygame.draw.rect(surface, COLOR_SAGE_LIGHT, rects["selector_value"], width=1)
    draw_text(
        surface,
        label,
        rects["selector_value"].center,
        font_size=14,
        color=COLOR_CHARCOAL,
        center=True,
    )
    draw_button(
        surface, ">", rects["selector_right"], hovered=hovered["selector_right"]
    )

    # Access key
    draw_text(
        surface,
        "CLAVE DE SEGURIDAD REGISTRADA",
        (panel_rect.x + 20, panel_rect.y + 195),
        font_size=12,
        color=COLOR_PINE,
        center=False,
    )
    draw_input(
        surface,
        state["inputs"].get("key", ""),
        rects["key"],
        focused=is_focused(state, "key"),
        mask=True,
        placeholder="Introduzca su clave de acceso",
    )

    # Register link
    link_color = COLOR_PINE if hovered["register_link"] else COLOR_CHARCOAL
    draw_text(
        surface,
        "¿Falta tu usuario?",
        (panel_rect.x + 20, panel_rect.y + 290),
        font_size=13,
        color=COLOR_CHARCOAL,
        center=False,
    )
    draw_text(
        surface,
        "Registrar Jugador",
        (panel_rect.x + 160, panel_rect.y + 290),
        font_size=13,
        color=link_color,
        center=False,
    )

    # Login button
    draw_button(
        surface,
        "Autenticar y Entrar",
        rects["login"],
        hovered=hovered["login"],
        focused=focused == "login",
    )
    shield_rect = pygame.Rect(
        rects["login"].x + 18, rects["login"].centery - 10, 20, 20
    )
    _draw_shield_icon(surface, shield_rect)

    draw_button(
        surface,
        "Volver al Menú",
        rects["menu"],
        hovered=hovered["menu"],
        focused=focused == "menu",
    )


def init_login(state: Dict[str, Any]) -> None:
    """Initialize login screen state."""
    state["inputs"] = {"key": ""}
    state["players"] = ensure_default_players()
    state["selected_player_index"] = 0
    state["focusable"] = [
        "selector_left",
        "selector_right",
        "key",
        "register_link",
        "login",
        "menu",
        "tab_register",
    ]
    state["focus_index"] = 0
    state["rects"] = _layout()
    state["session"]["bottom_sdg_id"] = None


def _selected_player(state: Dict[str, Any]) -> Dict[str, Any]:
    """Return the currently selected player."""
    players = state.get("players", [])
    index = state.get("selected_player_index", 0)
    if players and 0 <= index < len(players):
        return players[index]
    return {}


def _change_player(state: Dict[str, Any], direction: int) -> None:
    """Cycle through registered players."""
    players = state.get("players", [])
    if not players:
        return
    index = state.get("selected_player_index", 0)
    state["selected_player_index"] = (index + direction) % len(players)


def _select_player(state: Dict[str, Any], index: int) -> None:
    """Select a player by index."""
    players = state.get("players", [])
    if 0 <= index < len(players):
        state["selected_player_index"] = index


def _try_login(state: Dict[str, Any]) -> str:
    """Validate credentials and return the next screen name."""
    player = _selected_player(state)
    player_id = player.get("player_id", "").strip()
    access_key = state["inputs"].get("key", "").strip()

    if not player_id or not access_key:
        set_error(state, "Seleccione un jugador e ingrese la clave.")
        return "login"

    players = load_players()
    found = find_player(players, player_id)
    if found is None:
        set_error(state, "Jugador no registrado.")
        return "login"

    if found.get("access_key", "") != access_key:
        set_error(state, "Clave incorrecta.")
        return "login"

    login(state["session"], found)
    set_info(state, f"Bienvenido, {found['full_name']}")
    next_screen = state.get("pending_screen_after_login") or "menu"
    state["pending_screen_after_login"] = None
    return next_screen


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
                if name == "login":
                    return _try_login(state)
                if name == "menu":
                    return "menu"
                if name in ("register_link", "tab_register"):
                    return "register"
                if name == "selector_left":
                    _change_player(state, -1)
                    return state["current_screen"]
                if name == "selector_right":
                    _change_player(state, 1)
                    return state["current_screen"]

    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_TAB:
            cycle_focus(state, 1)
            return state["current_screen"]
        if event.key == pygame.K_ESCAPE:
            state["running"] = False
            return "exit"
        if event.key in (pygame.K_RETURN, pygame.K_SPACE):
            if focused == "login":
                return _try_login(state)
            if focused == "menu":
                return "menu"
            if focused in ("register_link", "tab_register"):
                return "register"
            if focused == "selector_left":
                _change_player(state, -1)
            elif focused == "selector_right":
                _change_player(state, 1)
            return state["current_screen"]
        if focused == "key":
            if event.key == pygame.K_BACKSPACE:
                state["inputs"]["key"] = state["inputs"]["key"][:-1]
            elif event.unicode.isprintable() and len(event.unicode) == 1:
                state["inputs"]["key"] += event.unicode

    return state["current_screen"]


def draw(surface: pygame.Surface, state: Dict[str, Any]) -> None:
    """Render the redesigned login screen."""
    surface.fill(COLOR_MINT)
    rects = _layout()
    state["rects"] = rects

    mouse_pos = pygame.mouse.get_pos()
    hovered = {name: rect.collidepoint(mouse_pos) for name, rect in rects.items()}
    focused = get_focused(state)

    _draw_header(surface, state)
    _draw_tabs(surface, rects, hovered)
    _draw_left_panel(surface, state, rects, hovered, focused)

    if state.get("error_message"):
        draw_error_message(
            surface,
            state["error_message"],
            (WINDOW_WIDTH // 2, WINDOW_HEIGHT - 70),
            font_size=18,
        )

    draw_message_panel(surface, state)
