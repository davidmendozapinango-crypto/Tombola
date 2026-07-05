"""Precondition evaluation helpers (non-OOP)."""

from typing import Any, Dict, List, Optional, Tuple

from src.core.preconditions import evaluate_precondition


def evaluate_preconditions(
    preconditions: List[Dict[str, Any]],
    payload: Dict[str, Any],
) -> Tuple[bool, Optional[Dict[str, Any]]]:
    """
    Evaluate preconditions in priority order.

    Returns (all_passed, highest_priority_failure).
    """
    failures = [
        precondition
        for precondition in preconditions
        if not evaluate_precondition(precondition, payload)
    ]
    if not failures:
        return True, None
    highest_priority_failure = min(failures, key=lambda p: p["priority_rank"])
    return False, highest_priority_failure
