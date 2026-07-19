"""
Pantalla de registro (no-OOP) con panel de datos y validador de clave.

Descripción:
  Permite crear un nuevo jugador con validaciones de datos y criterios de
  contraseña. El panel derecho explica los requisitos y sugiere una clave.
"""

from datetime import datetime
from typing import Any, Dict
import pygame
from src.auth.validator import check_password_criteria, validate_registration_data
from src.config import (
    COLOR_CHARCOAL,
    COLOR_MINT,
    COLOR_MOSS,
    COLOR_PINE,
    COLOR_SAGE_LIGHT,
    COLOR_WHITE,
    STATE_CODES,
    WINDOW_HEIGHT,
    WINDOW_WIDTH,
)
from src.persistence.players import (
    add_player,
    load_players,
    player_exists,
    save_players,
)
from src.ui.app_state import cycle_focus, get_focused, is_focused, set_error, set_info
from src.ui.common import (
    draw_button,
    draw_error_message,
    draw_input,
    draw_message_panel,
    draw_text,
    get_font,
    wrap_text,
)


def _layout() -> Dict[str, pygame.Rect]:
    """
    Devuelve los rectángulos (posiciones) usados por la pantalla de registro.
    """
    left_x = 70
    left_y = 115
    left_w = 460
    right_x = 550
    right_y = 115
    right_w = 400
    panel_h = 515
    return {
        "player_id": pygame.Rect(left_x + 20, left_y + 95, left_w - 40, 34),
        "full_name": pygame.Rect(left_x + 20, left_y + 160, left_w - 40, 34),
        "gender_m": pygame.Rect(left_x + 20, left_y + 225, 80, 30),
        "gender_f": pygame.Rect(left_x + 105, left_y + 225, 80, 30),
        "gender_o": pygame.Rect(left_x + 190, left_y + 225, 70, 30),
        "birthdate": pygame.Rect(left_x + 270, left_y + 225, left_w - 290, 30),
        "state_left": pygame.Rect(left_x + 20, left_y + 290, 32, 32),
        "state_value": pygame.Rect(left_x + 57, left_y + 290, left_w - 110, 32),
        "state_right": pygame.Rect(left_x + left_w - 52, left_y + 290, 32, 32),
        "access_key": pygame.Rect(left_x + 20, left_y + 355, left_w - 40, 34),
        "confirm_key": pygame.Rect(left_x + 20, left_y + 420, left_w - 40, 34),
        "login_link": pygame.Rect(left_x + 20, left_y + 545, 180, 28),
        "register": pygame.Rect(left_x + 210, left_y + 540, left_w - 230, 40),
    }


def _draw_person_icon(surface: pygame.Surface, rect: pygame.Rect) -> None:
    """Dibuja un icono simple de persona para el panel de datos."""
    (cx, cy) = rect.center
    pygame.draw.circle(surface, COLOR_PINE, (cx, cy - 5), 5, width=2)
    pygame.draw.arc(surface, COLOR_PINE, (cx - 8, cy - 2, 16, 12), 3.14, 6.28, 2)


def _draw_lock_icon(surface: pygame.Surface, rect: pygame.Rect) -> None:
    """Dibuja un icono de candado usado en el panel validador de clave."""
    (cx, cy) = rect.center
    pygame.draw.arc(surface, COLOR_MOSS, (cx - 6, cy - 10, 12, 12), 3.14, 6.28, 2)
    pygame.draw.rect(surface, COLOR_MOSS, (cx - 7, cy - 3, 14, 12), border_radius=2)
    pygame.draw.circle(surface, COLOR_PINE, (cx, cy + 2), 2)


def _draw_check_icon(surface: pygame.Surface, rect: pygame.Rect, met: bool) -> None:
    """Dibuja un marcador de check (cumplido) o cruz (no cumplido)."""
    (cx, cy) = rect.center
    color = COLOR_MOSS if met else COLOR_CHARCOAL
    if met:
        pygame.draw.circle(surface, COLOR_MOSS, (cx, cy), 8)
        pygame.draw.line(surface, COLOR_WHITE, (cx - 4, cy), (cx - 1, cy + 4), 2)
        pygame.draw.line(surface, COLOR_WHITE, (cx - 1, cy + 4), (cx + 4, cy - 3), 2)
    else:
        pygame.draw.circle(surface, COLOR_SAGE_LIGHT, (cx, cy), 8)
        pygame.draw.line(surface, COLOR_CHARCOAL, (cx - 3, cy - 3), (cx + 3, cy + 3), 2)
        pygame.draw.line(surface, COLOR_CHARCOAL, (cx + 3, cy - 3), (cx - 3, cy + 3), 2)


def _state_names() -> list[str]:
    """Devuelve la lista ordenada de códigos de estado (regiones)."""
    return list(STATE_CODES.keys())


def _change_state(state: Dict[str, Any], direction: int) -> None:
    """Cicla entre los códigos de estado disponibles (regiones)."""
    codes = _state_names()
    current = state["inputs"].get("state_code", "").strip().upper()
    if current in codes:
        index = codes.index(current)
    else:
        index = -1
    new_index = (index + direction) % len(codes)
    state["inputs"]["state_code"] = codes[new_index]


def _suggest_password() -> str:
    """Devuelve una clave ejemplo que cumple todos los criterios del validador."""
    return "Aura*2026"


def init_register(state: Dict[str, Any]) -> None:
    """Inicializa el estado de la pantalla de registro con campos vacíos."""
    state["inputs"] = {
        "player_id": "",
        "full_name": "",
        "gender": "",
        "birthdate": "",
        "state_code": "",
        "access_key": "",
        "confirm_key": "",
    }
    state["focusable"] = [
        "player_id",
        "full_name",
        "gender_m",
        "gender_f",
        "gender_o",
        "birthdate",
        "state_left",
        "state_right",
        "access_key",
        "confirm_key",
        "login_link",
        "register",
    ]
    state["focus_index"] = 0
    state["rects"] = _layout()


def _try_register(state: Dict[str, Any]) -> str:
    """Valida y guarda un nuevo jugador; devuelve la pantalla siguiente.

    Verifica coincidencia de claves, validez de datos y si la cédula ya está
    registrada. En caso de éxito persiste el jugador y solicita login.
    """
    inputs = state["inputs"]
    access_key = inputs.get("access_key", "").strip()
    confirm_key = inputs.get("confirm_key", "").strip()
    if access_key != confirm_key:
        set_error(state, "Las claves no coinciden.")
        return "register"
    data = {
        "player_id": inputs.get("player_id", "").strip(),
        "full_name": inputs.get("full_name", "").strip(),
        "gender": inputs.get("gender", "").strip().lower(),
        "birthdate": inputs.get("birthdate", "").strip(),
        "state_code": inputs.get("state_code", "").strip().upper(),
        "access_key": access_key,
    }
    (valid, errors) = validate_registration_data(data)
    if not valid:
        set_error(state, errors[0])
        return "register"
    players = load_players()
    if player_exists(players, data["player_id"]):
        set_error(state, "Ya existe un jugador con esa cedula.")
        return "register"
    data["registered_at"] = datetime.now()
    players = add_player(players, data)
    save_players(players)
    set_info(state, "Registro exitoso. Inicie sesion.")
    return "login"


def handle_event(state: Dict[str, Any], event: pygame.event.Event) -> str:
    """Procesa eventos Pygame para la pantalla de registro y devuelve la
    pantalla siguiente.
    """
    rects = state.get("rects") or _layout()
    state["rects"] = rects
    focused = get_focused(state)
    if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
        for name, rect in rects.items():
            if rect.collidepoint(event.pos):
                if name in state["focusable"]:
                    state["focus_index"] = state["focusable"].index(name)
                if name == "register":
                    return _try_register(state)
                if name == "login_link":
                    return "login"
                if name in ("gender_m", "gender_f", "gender_o"):
                    state["inputs"]["gender"] = name.split("_")[1]
                    return state["current_screen"]
                if name == "state_left":
                    _change_state(state, -1)
                    return state["current_screen"]
                if name == "state_right":
                    _change_state(state, 1)
                    return state["current_screen"]
                return state["current_screen"]
    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_TAB:
            cycle_focus(state, 1)
            return state["current_screen"]
        if event.key == pygame.K_ESCAPE:
            return "login"
        if event.key in (pygame.K_RETURN, pygame.K_SPACE):
            if focused == "register":
                return _try_register(state)
            if focused == "login_link":
                return "login"
            if focused in ("gender_m", "gender_f", "gender_o"):
                state["inputs"]["gender"] = focused.split("_")[1]
            if focused == "state_left":
                _change_state(state, -1)
            elif focused == "state_right":
                _change_state(state, 1)
            elif focused in state["inputs"] and event.key == pygame.K_SPACE:
                state["inputs"][focused] += " "
            return state["current_screen"]
        if focused in state["inputs"]:
            if event.key == pygame.K_BACKSPACE:
                state["inputs"][focused] = state["inputs"][focused][:-1]
            elif event.unicode.isprintable() and len(event.unicode) == 1:
                state["inputs"][focused] += event.unicode
    return state["current_screen"]


def _draw_title(surface: pygame.Surface) -> None:
    """Dibuja el título y subtítulo de la pantalla de registro."""
    draw_text(
        surface,
        "Registro de Jugador Acreditado",
        (WINDOW_WIDTH // 2, 55),
        font_size=32,
        color=COLOR_PINE,
        center=True,
    )
    italic_font = get_font(14)
    italic_font.set_italic(True)
    subtitle = italic_font.render(
        "Uniendo voluntades para alcanzar los Objetivos de Desarrollo Sostenible.",
        True,
        COLOR_CHARCOAL,
    )
    rect = subtitle.get_rect(center=(WINDOW_WIDTH // 2, 85))
    surface.blit(subtitle, rect)


def _draw_data_panel(
    surface: pygame.Surface,
    state: Dict[str, Any],
    rects: Dict[str, pygame.Rect],
    hovered: Dict[str, bool],
    focused: str,
) -> None:
    """Dibuja el panel izquierdo con los campos de datos del jugador."""
    left_x = 70
    left_y = 115
    left_w = 460
    panel_rect = pygame.Rect(left_x, left_y, left_w, 515)
    shadow_rect = panel_rect.copy()
    shadow_rect.x += 4
    shadow_rect.y += 4
    pygame.draw.rect(surface, COLOR_SAGE_LIGHT, shadow_rect, border_radius=16)
    pygame.draw.rect(surface, COLOR_WHITE, panel_rect, border_radius=16)
    pygame.draw.rect(surface, COLOR_SAGE_LIGHT, panel_rect, width=2, border_radius=16)
    icon_rect = pygame.Rect(panel_rect.x + 18, panel_rect.y + 18, 28, 28)
    pygame.draw.circle(surface, COLOR_MINT, icon_rect.center, 14)
    _draw_person_icon(surface, icon_rect)
    draw_text(
        surface,
        "Datos de Jugador",
        (panel_rect.x + 54, panel_rect.y + 22),
        font_size=18,
        color=COLOR_PINE,
        center=False,
    )
    pygame.draw.line(
        surface,
        COLOR_SAGE_LIGHT,
        (panel_rect.x + 18, panel_rect.y + 60),
        (panel_rect.right - 18, panel_rect.y + 60),
        1,
    )
    draw_text(
        surface,
        "CÉDULA DE IDENTIDAD (V- ...)",
        (rects["player_id"].x, rects["player_id"].y - 20),
        font_size=11,
        color=COLOR_CHARCOAL,
        center=False,
    )
    draw_input(
        surface,
        state["inputs"].get("player_id", ""),
        rects["player_id"],
        focused=is_focused(state, "player_id"),
        placeholder="Ej: 12345678",
    )
    draw_text(
        surface,
        "NOMBRE COMPLETO",
        (rects["full_name"].x, rects["full_name"].y - 20),
        font_size=11,
        color=COLOR_CHARCOAL,
        center=False,
    )
    draw_input(
        surface,
        state["inputs"].get("full_name", ""),
        rects["full_name"],
        focused=is_focused(state, "full_name"),
        placeholder="Ej: Camila Valentina Silva",
    )
    draw_text(
        surface,
        "GÉNERO / SEXO",
        (rects["gender_m"].x, rects["gender_m"].y - 20),
        font_size=11,
        color=COLOR_CHARCOAL,
        center=False,
    )
    current_gender = state["inputs"].get("gender", "").lower()
    for key, label in (("m", "Masculino"), ("f", "Femenino"), ("o", "Otro")):
        rect = rects[f"gender_{key}"]
        selected = current_gender == key
        bg = (
            COLOR_PINE
            if selected
            else COLOR_MOSS
            if hovered[f"gender_{key}"]
            else COLOR_WHITE
        )
        pygame.draw.rect(surface, bg, rect, border_radius=15)
        border_color = (
            COLOR_PINE if selected or hovered[f"gender_{key}"] else COLOR_SAGE_LIGHT
        )
        pygame.draw.rect(surface, border_color, rect, width=1, border_radius=15)
        draw_text(
            surface,
            label,
            rect.center,
            font_size=11,
            color=COLOR_WHITE if selected else COLOR_CHARCOAL,
            center=True,
        )
    draw_text(
        surface,
        "FECHA DE NACIMIENTO",
        (rects["birthdate"].x, rects["birthdate"].y - 20),
        font_size=11,
        color=COLOR_CHARCOAL,
        center=False,
    )
    draw_input(
        surface,
        state["inputs"].get("birthdate", ""),
        rects["birthdate"],
        focused=is_focused(state, "birthdate"),
        placeholder="01/01/2000",
    )
    draw_text(
        surface,
        "ESTADO DE PROCEDENCIA (REGIÓN ORIGEN)",
        (rects["state_value"].x, rects["state_value"].y - 20),
        font_size=11,
        color=COLOR_CHARCOAL,
        center=False,
    )
    draw_button(surface, "<", rects["state_left"], hovered=hovered["state_left"])
    pygame.draw.rect(surface, COLOR_MINT, rects["state_value"])
    pygame.draw.rect(surface, COLOR_SAGE_LIGHT, rects["state_value"], width=1)
    state_code = state["inputs"].get("state_code", "").upper()
    state_label = STATE_CODES.get(state_code, "Seleccione...")
    draw_text(
        surface,
        f"{state_label} ({state_code})" if state_code else state_label,
        rects["state_value"].center,
        font_size=13,
        color=COLOR_CHARCOAL,
        center=True,
    )
    draw_button(surface, ">", rects["state_right"], hovered=hovered["state_right"])
    draw_text(
        surface,
        "CLAVE DE ACCESO (CRITERIO ODS)",
        (rects["access_key"].x, rects["access_key"].y - 20),
        font_size=11,
        color=COLOR_CHARCOAL,
        center=False,
    )
    draw_input(
        surface,
        state["inputs"].get("access_key", ""),
        rects["access_key"],
        focused=is_focused(state, "access_key"),
        mask=True,
        placeholder="Ej: Clave*25",
    )
    draw_text(
        surface,
        "CONFIRMAR CLAVE",
        (rects["confirm_key"].x, rects["confirm_key"].y - 20),
        font_size=11,
        color=COLOR_CHARCOAL,
        center=False,
    )
    draw_input(
        surface,
        state["inputs"].get("confirm_key", ""),
        rects["confirm_key"],
        focused=is_focused(state, "confirm_key"),
        mask=True,
        placeholder="Repita su clave",
    )


def _draw_bottom_actions(
    surface: pygame.Surface,
    rects: Dict[str, pygame.Rect],
    hovered: Dict[str, bool],
    focused: str,
) -> None:
    """Dibuja el enlace a login y el botón de registro debajo del panel."""
    link_color = COLOR_PINE if hovered["login_link"] else COLOR_CHARCOAL
    draw_text(
        surface,
        "¿Ya estás registrado? Inicia Sesión",
        (rects["login_link"].x, rects["login_link"].y + 6),
        font_size=13,
        color=link_color,
        center=False,
    )
    draw_button(
        surface,
        "Generar Ciudadanía  →",
        rects["register"],
        hovered=hovered["register"],
        focused=focused == "register",
    )


def _draw_validator_panel(surface: pygame.Surface, state: Dict[str, Any]) -> None:
    """Dibuja el panel derecho que muestra las reglas de la contraseña y
    evalúa en tiempo real si la clave cumple los criterios.
    """
    right_x = 550
    right_y = 115
    right_w = 400
    panel_rect = pygame.Rect(right_x, right_y, right_w, 515)
    pygame.draw.rect(surface, COLOR_PINE, panel_rect, border_radius=16)
    icon_rect = pygame.Rect(panel_rect.x + 18, panel_rect.y + 18, 28, 28)
    _draw_lock_icon(surface, icon_rect)
    draw_text(
        surface,
        "VALIDADOR DE CLAVE",
        (panel_rect.x + 54, panel_rect.y + 20),
        font_size=18,
        color=COLOR_WHITE,
        center=False,
    )
    draw_text(
        surface,
        "Criterios Algorítmicos Recursivos",
        (panel_rect.x + 54, panel_rect.y + 40),
        font_size=12,
        color=COLOR_MOSS,
        center=False,
    )
    pygame.draw.line(
        surface,
        (76, 122, 79),
        (panel_rect.x + 18, panel_rect.y + 75),
        (panel_rect.right - 18, panel_rect.y + 75),
        1,
    )
    intro_text = "El juego requiere claves de acceso robustas conforme con los estándares gubernamentales para proteger la bitácora JUGADORES.bin contra intrusiones:"
    intro_lines = wrap_text(intro_text, right_w - 40, font_size=12)
    italic_font = get_font(12)
    italic_font.set_italic(True)
    line_y = panel_rect.y + 90
    for line in intro_lines[:3]:
        rendered = italic_font.render(line, True, COLOR_MOSS)
        surface.blit(rendered, (panel_rect.x + 18, line_y))
        line_y += 16
    access_key = state["inputs"].get("access_key", "")
    confirm_key = state["inputs"].get("confirm_key", "")
    criteria = check_password_criteria(access_key)
    keys_match = bool(access_key) and access_key == confirm_key
    items = [
        (
            "length_ok",
            "Longitud Permitida",
            "Debe tener exactamente de 6 a 10 caracteres.",
        ),
        (
            "has_uppercase",
            "Mezcla de Caracteres",
            "Debe contener al menos una Mayúscula, una minúscula y un número.",
        ),
        (
            "has_special",
            "Carácter Especial Exclusivo",
            "Debe incluir al menos uno de estos símbolos: * = % _",
        ),
        (
            "no_long_run",
            "Sin Repetitividad Secuencial",
            "No se admiten más de 3 caracteres idénticos consecutivos.",
        ),
        (
            "keys_match",
            "Confirmacion de Clave",
            "Ambas claves deben coincidir.",
            keys_match,
        ),
    ]
    y = line_y + 10
    for index, item in enumerate(items):
        if len(item) == 4:
            (key, title, description, met) = item
        else:
            (key, title, description) = item
            met = criteria[key]
        _draw_check_icon(surface, pygame.Rect(panel_rect.x + 30, y + 6, 20, 20), met)
        draw_text(
            surface,
            f"{index + 1}. {title}",
            (panel_rect.x + 58, y),
            font_size=13,
            color=COLOR_WHITE,
            center=False,
        )
        words = description.split()
        line = ""
        line_y = y + 18
        font = get_font(11)
        max_width = right_w - 80
        for word in words:
            test = f"{line} {word}".strip()
            if font.size(test)[0] <= max_width:
                line = test
            else:
                draw_text(
                    surface,
                    line,
                    (panel_rect.x + 58, line_y),
                    font_size=11,
                    color=COLOR_MOSS,
                    center=False,
                )
                line = word
                line_y += 16
        if line:
            draw_text(
                surface,
                line,
                (panel_rect.x + 58, line_y),
                font_size=11,
                color=COLOR_MOSS,
                center=False,
            )
        y += 56
    suggestion = _suggest_password()
    draw_text(
        surface,
        "Sugerencia de Clave Válida:",
        (panel_rect.x + 18, panel_rect.bottom - 65),
        font_size=12,
        color=COLOR_WHITE,
        center=False,
    )
    suggestion_text = f"{suggestion}, que cumple con las restricciones y se encriptará de forma simétrica antes de empaquetarse."
    suggestion_lines = wrap_text(suggestion_text, right_w - 40, font_size=11)
    line_y = panel_rect.bottom - 47
    for line in suggestion_lines[:3]:
        draw_text(
            surface,
            line,
            (panel_rect.x + 18, line_y),
            font_size=11,
            color=COLOR_MOSS,
            center=False,
        )
        line_y += 16


def draw(surface: pygame.Surface, state: Dict[str, Any]) -> None:
    """Renderiza la pantalla de registro completa con validación visual."""
    surface.fill(COLOR_MINT)
    rects = _layout()
    state["rects"] = rects
    mouse_pos = pygame.mouse.get_pos()
    hovered = {name: rect.collidepoint(mouse_pos) for (name, rect) in rects.items()}
    focused = get_focused(state)
    _draw_title(surface)
    _draw_data_panel(surface, state, rects, hovered, focused)
    _draw_bottom_actions(surface, rects, hovered, focused)
    _draw_validator_panel(surface, state)
    if state.get("error_message"):
        draw_error_message(
            surface,
            state["error_message"],
            (WINDOW_WIDTH // 2, WINDOW_HEIGHT - 75),
            font_size=18,
        )
    draw_message_panel(surface, state)
