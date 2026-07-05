import pytest

from src.core.calculation_engine import execute_command, make_engine_context
from src.core.calculation_rules import build_default_registry
from src.core.dependencies import make_dependency_checker, register_dependency
from src.core.preconditions import make_precondition
from src.ui.screens.calculation_screen import make_screen, on_calculate_action
from src.ui.state.calculation_state import make_state


def _make_screen():
    registry = build_default_registry(dependencies=["player_session"])
    checker = make_dependency_checker()
    register_dependency(checker, "player_session", lambda: True)
    preconditions = [
        make_precondition(
            precondition_id="actor_present",
            description="Actor present",
            priority_rank=1,
            check=lambda p: bool(p["command"]["actor_id"]),
            failure_message_id="missing_actor_id",
        ),
        make_precondition(
            precondition_id="operation_valid",
            description="Operation valid",
            priority_rank=2,
            check=lambda p: bool(p["command"]["operation_key"]),
            failure_message_id="missing_operation_key",
        ),
    ]
    engine_context = make_engine_context(registry, preconditions, checker)
    state = make_state()
    return make_screen(engine_context, state)


def test_multi_failure_returns_highest_priority():
    screen = _make_screen()
    raw_payload = {
        "actor_id": "",
        "operation_key": "",
        "path_context": {"mode": "single"},
        "input_payload": {"a": 5, "b": 3},
        "ui_origin": "calculator_screen",
    }
    result = on_calculate_action(screen, raw_payload)
    assert result["status"] == "failure"
    assert result["error_code"] == "missing_actor_id"
    assert screen["flow"]["state"]["result"] is None
