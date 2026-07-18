"""Business precondition helpers (non-OOP)."""
from typing import Any, Callable, Dict

def make_precondition(precondition_id: str, description: str, priority_rank: int, check: Callable[[Dict[str, Any]], bool], failure_message_id: str) -> Dict[str, Any]:
    """Create a business precondition dictionary."""
    return {'precondition_id': precondition_id, 'description': description, 'priority_rank': priority_rank, 'check': check, 'failure_message_id': failure_message_id}

def evaluate_precondition(precondition: Dict[str, Any], payload: Dict[str, Any]) -> bool:
    """Evaluate a single precondition against a payload."""
    try:
        return bool(precondition['check'](payload))
    except Exception:
        return False