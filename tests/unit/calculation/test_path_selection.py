import pytest

from src.core.path_rules import make_registry, make_rule, register_rule, select_rule


def _mode_single(ctx, payload):
    return ctx.get("mode") == "single"


def _mode_batch(ctx, payload):
    return ctx.get("mode") == "batch"


@pytest.fixture
def registry():
    reg = make_registry()
    register_rule(
        reg,
        make_rule(
            path_id="sum:single",
            priority=10,
            entry_conditions=[_mode_single],
            output_definition={"impact_marker": "sum_single"},
        ),
    )
    register_rule(
        reg,
        make_rule(
            path_id="sum:batch",
            priority=5,
            entry_conditions=[_mode_batch],
            output_definition={"impact_marker": "sum_batch"},
        ),
    )
    return reg


def test_selects_matching_path(registry):
    rule = select_rule(registry, "sum", {"mode": "single"}, {"a": 1, "b": 2})
    assert rule is not None
    assert rule["path_id"] == "sum:single"


def test_no_match_returns_none(registry):
    rule = select_rule(registry, "sum", {"mode": "unknown"}, {"a": 1, "b": 2})
    assert rule is None


def test_highest_priority_wins(registry):
    rule = select_rule(registry, "sum", {"mode": "single"}, {"a": 1, "b": 2})
    assert rule["priority"] == 10
