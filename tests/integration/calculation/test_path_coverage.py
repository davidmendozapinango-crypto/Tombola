import pytest

from src.core.calculation_engine import execute_command, make_engine_context
from src.core.calculation_rules import build_default_registry
from src.core.card import generate_card
from src.core.command_contract import make_command
from src.core.dependencies import make_dependency_checker, register_dependency
from src.core.preconditions import make_precondition


def _make_engine():
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
        )
    ]
    return make_engine_context(registry, preconditions, checker)


def test_single_path_coverage():
    engine_context = _make_engine()
    command = make_command(
        actor_id="player-001",
        operation_key="sum",
        path_context={"mode": "single"},
        input_payload={"a": 2, "b": 4},
        ui_origin="screen",
    )
    result = execute_command(command, engine_context)
    assert result["status"] == "success"
    assert result["path_id"] == "sum:single"


def test_batch_path_coverage():
    engine_context = _make_engine()
    command = make_command(
        actor_id="player-001",
        operation_key="sum",
        path_context={"mode": "batch"},
        input_payload={"items": [1, 2, 3]},
        ui_origin="screen",
    )
    result = execute_command(command, engine_context)
    assert result["status"] == "success"
    assert result["path_id"] == "sum:batch"


def test_tombola_card_coverage_path():
    engine_context = _make_engine()
    dimension = 5
    card = generate_card(dimension)
    drawn_numbers = [cell for row in card for cell in row][:7]
    command = make_command(
        actor_id="player-001",
        operation_key="tombola",
        path_context={"domain": "tombola", "path": "card_coverage"},
        input_payload={"card": card, "drawn_numbers": drawn_numbers},
        ui_origin="screen",
    )
    result = execute_command(command, engine_context)
    assert result["status"] == "success"
    assert result["path_id"] == "tombola:card_coverage"
    payload = result["result_payload"]
    assert payload["total_cells"] == dimension * dimension
    assert payload["marked_cells"] == 7
    assert payload["coverage_percentage"] == 28.0
    assert "missing_numbers" in payload


def test_tombola_game_score_path():
    engine_context = _make_engine()
    main_card = generate_card(5)
    complement_card = generate_card(5)
    drawn_numbers = [cell for row in main_card for cell in row][:10]
    command = make_command(
        actor_id="player-001",
        operation_key="tombola",
        path_context={"domain": "tombola", "path": "game_score"},
        input_payload={
            "main_card": main_card,
            "complement_card": complement_card,
            "drawn_numbers": drawn_numbers,
        },
        ui_origin="screen",
    )
    result = execute_command(command, engine_context)
    assert result["status"] == "success"
    assert result["path_id"] == "tombola:game_score"
    payload = result["result_payload"]
    assert "main_points" in payload
    assert "complement_points" in payload
    assert "total_points" in payload


def test_tombola_sdg_context_path():
    engine_context = _make_engine()
    command = make_command(
        actor_id="player-001",
        operation_key="tombola",
        path_context={"domain": "tombola", "path": "sdg_context"},
        input_payload={"sdg_id": 4},
        ui_origin="screen",
    )
    result = execute_command(command, engine_context)
    assert result["status"] == "success"
    assert result["path_id"] == "tombola:sdg_context"
    payload = result["result_payload"]
    assert payload["sdg_id"] == 4
    assert payload["sdg_name"]
    assert "sdg_slogan" in payload
