"""Registration screen (non-OOP)."""

from datetime import datetime
from typing import Any, Dict

import pygame

from src.auth.validator import check_password_criteria, validate_registration_data
from src.config import (
    COLOR_CHARCOAL,
    COLOR_MINT,
    COLOR_PINE,
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
from src.ui.common import draw_button, draw_error_message, draw_input, draw_text


def _layout() -> Dict[str, pygame.Rect]:
    """Return the UI rectangles for the registration screen."""
    center_x = WINDOW_WIDTH // 2
    y = 140
    return {
        "player_id": pygame.Rect(center_x - 150, y, 300, 32),
        "full_name": pygame.Rect(center_x - 150, y + 50, 300, 32),
        "gender": pygame.Rect(center_x - 150, y + 100, 145, 32),
        "birthdate": pygame.Rect(center_x + 5, y + 100, 145, 32),
        "state_code": pygame.Rect(center_x - 150, y + 150, 300, 32),
        "access_key": pygame.Rect(center_x - 150, y + 200, 300, 32),
        "confirm_key": pygame.Rect(center_x - 150, y + 250, 300, 32),
        "register": pygame.Rect(center_x - 150, y + 400, 145, 40),
        "back": pygame.Rect(center_x + 5, y + 400, 145, 40),
    }


def init_register(state: Dict[str, Any]) -> None:
    """Initialize registration screen state."""
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
        "gender",
        "birthdate",
        "state_code",
        "access_key",
        "confirm_key",
        "register",
        "back",
    ]
    state["focus_index"] = 0
    state["rects"] = _layout()


def _try_register(state: Dict[str, Any]) -> str:
    """Validate and save a new player. Return next screen name."""
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

    valid, errors = validate_registration_data(data)
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
    """Process a Pygame event and return the next screen name."""
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
                if name == "back":
                    return "login"
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
            if focused == "back":
                return "login"
            return state["current_screen"]
        if focused in state["inputs"]:
            if event.key == pygame.K_BACKSPACE:
                state["inputs"][focused] = state["inputs"][focused][:-1]
            elif event.unicode.isprintable() and len(event.unicode) == 1:
                state["inputs"][focused] += event.unicode

    return state["current_screen"]


def draw(surface: pygame.Surface, state: Dict[str, Any]) -> None:
    """Render the registration screen."""
    surface.fill(COLOR_MINT)
    rects = _layout()
    state["rects"] = rects

    draw_text(
        surface,
        "Registro de jugador",
        (WINDOW_WIDTH // 2, 80),
        font_size=40,
        color=COLOR_PINE,
        center=True,
    )

    labels = {
        "player_id": "Cedula",
        "full_name": "Nombre completo",
        "gender": "Sexo (m/f)",
        "birthdate": "Fecha nacimiento (YYYY-MM-DD)",
        "state_code": "Codigo estado (3 letras)",
        "access_key": "Clave de acceso",
        "confirm_key": "Confirmar clave",
    }

    mouse_pos = pygame.mouse.get_pos()
    hovered = {name: rect.collidepoint(mouse_pos) for name, rect in rects.items()}

    for name, rect in rects.items():
        if name in labels:
            draw_text(
                surface,
                labels[name] + ":",
                (rect.x, rect.y - 22),
                font_size=18,
            )
            mask = name in ("access_key", "confirm_key")
            draw_input(
                surface,
                state["inputs"].get(name, ""),
                rect,
                focused=is_focused(state, name),
                mask=mask,
            )

    _draw_password_criteria(surface, state["inputs"].get("access_key", ""), rects)

    focused = get_focused(state)
    draw_button(
        surface,
        "Registrar",
        rects["register"],
        hovered=hovered["register"],
        focused=focused == "register",
    )
    draw_button(
        surface,
        "Volver",
        rects["back"],
        hovered=hovered["back"],
        focused=focused == "back",
    )

    if state.get("error_message"):
        draw_error_message(
            surface,
            state["error_message"],
            (WINDOW_WIDTH // 2, WINDOW_HEIGHT - 60),
            font_size=20,
        )


def _draw_password_criteria(
    surface: pygame.Surface, access_key: str, rects: Dict[str, pygame.Rect]
) -> None:
    """Draw a checklist of password criteria below the access key input."""
    criteria = check_password_criteria(access_key)
    items = [
        ("length_ok", "Entre 6 y 10 caracteres"),
        ("has_uppercase", "Al menos una mayuscula"),
        ("has_lowercase", "Al menos una minuscula"),
        ("has_digit", "Al menos un numero"),
        ("has_special", "Al menos un especial (* = % _)"),
        ("no_long_run", "Maximo 3 iguales seguidos"),
    ]
    start_y = rects["confirm_key"].bottom + 12
    x_left = rects["confirm_key"].x
    x_right = x_left + 160
    for index, (key, label) in enumerate(items):
        met = criteria[key]
        marker = "✓" if met else "✗"
        color = COLOR_PINE if met else (200, 60, 60)
        x = x_left if index < 3 else x_right
        y = start_y + (index % 3) * 22
        draw_text(
            surface,
            f"{marker} {label}",
            (x, y),
            font_size=16,
            color=color,
        )
