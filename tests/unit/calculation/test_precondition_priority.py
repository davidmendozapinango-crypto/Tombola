import pytest

from src.core.precondition_evaluator import evaluate_preconditions
from src.core.preconditions import make_precondition


def test_duplicate_priority_rank_is_rejected():
    preconditions = [
        make_precondition(
            precondition_id="p1",
            description="Actor present",
            priority_rank=1,
            check=lambda p: bool(p.get("actor_id")),
            failure_message_id="missing_actor_id",
        ),
        make_precondition(
            precondition_id="p2",
            description="Operation present",
            priority_rank=1,
            check=lambda p: bool(p.get("operation_key")),
            failure_message_id="missing_operation_key",
        ),
    ]
    with pytest.raises(ValueError, match="Duplicate priority_rank"):
        evaluate_preconditions(preconditions, {"actor_id": "", "operation_key": ""})


def test_highest_priority_failure_returned():
    preconditions = [
        make_precondition(
            precondition_id="p1",
            description="Actor present",
            priority_rank=1,
            check=lambda p: bool(p.get("actor_id")),
            failure_message_id="missing_actor_id",
        ),
        make_precondition(
            precondition_id="p2",
            description="Operation present",
            priority_rank=2,
            check=lambda p: bool(p.get("operation_key")),
            failure_message_id="missing_operation_key",
        ),
    ]
    passed, failure = evaluate_preconditions(
        preconditions, {"actor_id": "", "operation_key": ""}
    )
    assert passed is False
    assert failure is not None
    assert failure["precondition_id"] == "p1"


def test_all_passed_returns_none():
    preconditions = [
        make_precondition(
            precondition_id="p1",
            description="Actor present",
            priority_rank=1,
            check=lambda p: bool(p.get("actor_id")),
            failure_message_id="missing_actor_id",
        ),
    ]
    passed, failure = evaluate_preconditions(preconditions, {"actor_id": "x"})
    assert passed is True
    assert failure is None
