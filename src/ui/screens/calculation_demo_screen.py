"""Calculation demo screen wrapper (non-OOP)."""

from typing import Any, Dict

import pygame

from src.config import (
    COLOR_CHARCOAL,
    COLOR_MINT,
    COLOR_PINE,
    WINDOW_HEIGHT,
    WINDOW_WIDTH,
)
from src.core.calculation_engine import make_engine_context
from src.core.calculation_rules import build_default_registry
from src.core.card import generate_card
from src.core.dependencies import make_dependency_checker, register_dependency
from src.persistence.impact_records import make_impact_persistence
from src.ui.common import draw_button, draw_error_message, draw_text
from src.ui.screens import calculation_screen


def _layout() -> Dict[str, pygame.Rect]:
    """Return the UI rectangles for the calculation demo screen."""
    center_x = WINDOW_WIDTH // 2
    return {
        "trigger": pygame.Rect(center_x - 120, 240, 240, 45),
        "back": pygame.Rect(center_x - 120, 310, 240, 45),
    }


def _build_engine_context() -> Dict[str, Any]:
    """Create a minimal engine context for the demo."""
    registry = build_default_registry(dependencies=["data_context"])
    dependency_checker = make_dependency_checker()
    register_dependency(dependency_checker, "data_context", lambda: True)
    return make_engine_context(
        registry=registry,
        preconditions=[],
        dependency_checker=dependency_checker,
        impact_persistence=make_impact_persistence(),
    )


def _build_sample_payload() -> Dict[str, Any]:
    """Return a sample GUI payload using a Tombola card coverage path."""
    dimension = 5
    card = generate_card(dimension)
    drawn_numbers = [cell for row in card for cell in row][:7]
    return {
        "actor_id": "player1",
        "operation_key": "tombola",
        "path_context": {"domain": "tombola", "path": "card_coverage"},
        "input_payload": {
            "card": card,
            "drawn_numbers": drawn_numbers,
        },
        "ui_origin": "calculation_demo",
    }


def init_calculation_demo(state: Dict[str, Any]) -> None:
    """Initialize the calculation demo screen."""
    engine_context = _build_engine_context()
    app_state = state.get("session") or {}
    demo_screen = calculation_screen.make_screen(engine_context, app_state)
    state["calculation_demo_screen"] = demo_screen
    state["calculation_result"] = None
    state["focusable"] = ["trigger", "back"]
    state["focus_index"] = 0
    state["rects"] = _layout()


_RECT_TO_CONTROL = {
    "trigger": "calculate_button",
    "back": "cancel_button",
}

_CONTROL_TO_RECT = {
    "calculate_button": "trigger",
    "cancel_button": "back",
}


def handle_event(state: Dict[str, Any], event: pygame.event.Event) -> str:
    """Process a Pygame event and return the next screen name."""
    rects = state.get("rects") or _layout()
    state["rects"] = rects
    demo_screen = state["calculation_demo_screen"]
    focused = demo_screen["focused_control"]

    if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
        for rect_name, rect in rects.items():
            if rect.collidepoint(event.pos):
                control_name = _RECT_TO_CONTROL[rect_name]
                demo_screen["focus_index"] = demo_screen["controls"].index(control_name)
                demo_screen["focused_control"] = control_name
                return _activate(state, rect_name)

    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_TAB:
            if event.mod & pygame.KMOD_SHIFT:
                calculation_screen.focus_previous(demo_screen)
            else:
                calculation_screen.focus_next(demo_screen)
            state["focus_index"] = demo_screen["focus_index"]
            return state["current_screen"]
        if event.key in (pygame.K_RETURN, pygame.K_SPACE):
            return _activate(state, _CONTROL_TO_RECT[focused])
        if event.key == pygame.K_ESCAPE:
            return "menu"

    return state["current_screen"]


def _activate(state: Dict[str, Any], rect_name: str) -> str:
    """Activate a control on this screen."""
    if rect_name == "trigger":
        demo_screen = state["calculation_demo_screen"]
        result = calculation_screen.on_calculate_action(
            demo_screen, _build_sample_payload()
        )
        state["calculation_result"] = result
        return state["current_screen"]
    if rect_name == "back":
        return "menu"
    return state["current_screen"]


def draw(surface: pygame.Surface, state: Dict[str, Any]) -> None:
    """Render the calculation demo screen."""
    surface.fill(COLOR_MINT)
    rects = _layout()
    state["rects"] = rects

    draw_text(
        surface,
        "Demo de calculo",
        (WINDOW_WIDTH // 2, 80),
        font_size=40,
        color=COLOR_PINE,
        center=True,
    )
    draw_text(
        surface,
        "Ejecuta un comando interno de suma de demostracion.",
        (WINDOW_WIDTH // 2, 140),
        font_size=22,
        color=COLOR_CHARCOAL,
        center=True,
    )

    mouse_pos = pygame.mouse.get_pos()
    hovered = {name: rect.collidepoint(mouse_pos) for name, rect in rects.items()}
    demo_screen = state["calculation_demo_screen"]
    focused_control = demo_screen.get("focused_control")
    draw_button(
        surface,
        "Ejecutar calculo",
        rects["trigger"],
        hovered=hovered["trigger"],
        focused=focused_control == "calculate_button",
    )
    draw_button(
        surface,
        "Volver",
        rects["back"],
        hovered=hovered["back"],
        focused=focused_control == "cancel_button",
    )

    result = state.get("calculation_result")
    if result:
        if result.get("status") == "success":
            text = f"Exito: {result.get('result_payload')}"
            color = COLOR_PINE
        else:
            text = f"Error: {result.get('error_message', 'Desconocido')}"
            color = (220, 80, 80)
        draw_text(
            surface,
            text,
            (WINDOW_WIDTH // 2, 420),
            font_size=22,
            color=color,
            center=True,
        )
    elif state.get("error_message"):
        draw_error_message(
            surface,
            state["error_message"],
            (WINDOW_WIDTH // 2, WINDOW_HEIGHT - 80),
            font_size=20,
        )
