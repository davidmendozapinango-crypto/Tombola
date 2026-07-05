"""GUI state helpers for calculation flows (non-OOP)."""

from typing import Any, Dict, Optional


def make_state() -> Dict[str, Any]:
    """Create a calculation state dictionary."""
    return {
        "result": None,
        "error_message": "",
        "is_loading": False,
        "impact_validated": False,
    }


def state_set_success(state: Dict[str, Any], result: Dict[str, Any]) -> None:
    """Update state for a successful calculation."""
    state["result"] = result
    state["error_message"] = ""
    state["impact_validated"] = bool(result.get("impact_marker"))


def state_set_error(state: Dict[str, Any], message: str) -> None:
    """Update state for a failed calculation."""
    state["error_message"] = message
    state["result"] = None
    state["impact_validated"] = False


def state_clear(state: Dict[str, Any]) -> None:
    """Reset calculation state."""
    state["result"] = None
    state["error_message"] = ""
    state["is_loading"] = False
    state["impact_validated"] = False
