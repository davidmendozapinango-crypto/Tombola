import pytest

from src.core.command_contract import make_command, validate_required_fields
from src.core.path_rules import make_registry, make_rule, register_rule


def test_command_required_fields():
    command = make_command(
        actor_id="player-001",
        operation_key="sum",
        path_context={"mode": "single"},
        input_payload={"a": 1, "b": 2},
        ui_origin="screen",
    )
    assert validate_required_fields(command) == []


def test_registry_duplicate_path_id():
    registry = make_registry()
    rule = make_rule(path_id="sum:single", priority=1)
    register_rule(registry, rule)
    with pytest.raises(ValueError):
        register_rule(registry, make_rule(path_id="sum:single", priority=2))
