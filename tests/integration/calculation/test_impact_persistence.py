from pathlib import Path

from src.core.application_impact import list_impact_records
from src.core.calculation_engine import execute_command, make_engine_context
from src.core.calculation_rules import build_default_registry
from src.core.command_contract import make_command
from src.core.dependencies import make_dependency_checker, register_dependency
from src.persistence.impact_records import (
    load_impact_records,
    make_impact_persistence,
)


def _make_engine(tmp_path: Path, with_persistence: bool = True):
    registry = build_default_registry(dependencies=["player_session"])
    checker = make_dependency_checker()
    register_dependency(checker, "player_session", lambda: True)
    persistence = make_impact_persistence(data_dir=str(tmp_path)) if with_persistence else None
    return make_engine_context(registry, [], checker, impact_persistence=persistence)


def test_success_persists_impact_record(tmp_path):
    engine_context = _make_engine(tmp_path)
    command = make_command(
        actor_id="player-001",
        operation_key="sum",
        path_context={"mode": "single"},
        input_payload={"a": 2, "b": 3},
        ui_origin="calculator_screen",
    )
    result = execute_command(command, engine_context)
    assert result["status"] == "success"

    persisted = load_impact_records(engine_context["impact_persistence"])
    assert len(persisted) == 1
    assert persisted[0]["interaction_point"] == "calculator_screen"
    assert "sum:single" in persisted[0]["after_behavior"]


def test_failure_persists_impact_record(tmp_path):
    engine_context = _make_engine(tmp_path)
    command = make_command(
        actor_id="",
        operation_key="sum",
        path_context={"mode": "single"},
        input_payload={"a": 2, "b": 3},
        ui_origin="calculator_screen",
    )
    result = execute_command(command, engine_context)
    assert result["status"] == "failure"

    persisted = load_impact_records(engine_context["impact_persistence"])
    assert len(persisted) == 1
    assert "rejected" in persisted[0]["after_behavior"].lower()


def test_multiple_executions_produce_valid_loadable_records(tmp_path):
    engine_context = _make_engine(tmp_path)
    for index in range(3):
        command = make_command(
            actor_id=f"player-{index:03d}",
            operation_key="sum",
            path_context={"mode": "single"},
            input_payload={"a": index, "b": index + 1},
            ui_origin="calculator_screen",
        )
        execute_command(command, engine_context)

    persisted = load_impact_records(engine_context["impact_persistence"])
    assert len(persisted) == 3


def test_malformed_persistence_lines_are_skipped(tmp_path):
    persistence = make_impact_persistence(data_dir=str(tmp_path))
    file_path = persistence["file_path"]
    file_path.write_text(
        '{"impact_id": "good-1", "interaction_point": "x", "before_behavior": "b", "after_behavior": "a", "validation_reference": "v"}\n'
        'this is not json\n'
        '{"impact_id": "good-2", "interaction_point": "x", "before_behavior": "b", "after_behavior": "a", "validation_reference": "v"}\n'
    )

    records = load_impact_records(persistence)
    assert len(records) == 2
    assert records[0]["impact_id"] == "good-1"
    assert records[1]["impact_id"] == "good-2"
