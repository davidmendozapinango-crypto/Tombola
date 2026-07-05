import pytest

from src.core.calculation_engine import make_engine_context
from src.core.calculation_rules import build_default_registry
from src.core.dependencies import make_dependency_checker
from src.ui.screens.calculation_screen import focus_next, focus_previous, make_screen
from src.ui.state.calculation_state import make_state


@pytest.fixture
def screen():
    engine_context = make_engine_context(
        build_default_registry(),
        [],
        make_dependency_checker(),
    )
    return make_screen(engine_context, make_state())


def test_screen_supports_focus_navigation(screen):
    # Verify the screen exposes keyboard/focus primitives for accessibility.
    assert "focus_next" not in screen  # functions are module-level
    assert "focus_previous" not in screen
    assert "focused_control" in screen


def test_focus_next_cycles_through_controls(screen):
    assert screen["focused_control"] == "calculate_button"
    focus_next(screen)
    assert screen["focused_control"] == "cancel_button"
    focus_next(screen)
    assert screen["focused_control"] == "calculate_button"


def test_focus_previous_cycles(screen):
    focus_next(screen)
    focus_previous(screen)
    assert screen["focused_control"] == "calculate_button"
