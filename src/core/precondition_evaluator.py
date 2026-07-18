"""Precondition evaluation helpers (non-OOP)."""
from typing import Any, Dict, List, Optional, Tuple
from src.core.preconditions import evaluate_precondition

def validate_precondition_set(preconditions: List[Dict[str, Any]]) -> None:
    """Validate that priority_rank values are unique across the precondition set."""
    ranks = {}
    for precondition in preconditions:
        rank = precondition['priority_rank']
        if rank in ranks:
            raise ValueError(f"Duplicate priority_rank {rank} in preconditions '{ranks[rank]['precondition_id']}' and '{precondition['precondition_id']}'")
        ranks[rank] = precondition

def evaluate_preconditions(preconditions: List[Dict[str, Any]], payload: Dict[str, Any]) -> Tuple[bool, Optional[Dict[str, Any]]]:
    """
    Evaluate preconditions in priority order.

    Returns (all_passed, highest_priority_failure).
    """
    validate_precondition_set(preconditions)
    failures = [precondition for precondition in preconditions if not evaluate_precondition(precondition, payload)]
    if not failures:
        return (True, None)
    highest_priority_failure = min(failures, key=lambda p: p['priority_rank'])
    return (False, highest_priority_failure)