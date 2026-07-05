"""Dependency checker helpers (non-OOP)."""

from datetime import datetime
from typing import Any, Callable, Dict, List


def make_dependency_checker() -> Dict[str, Any]:
    """Create an empty dependency checker."""
    return {"checks": {}}


def register_dependency(
    checker: Dict[str, Any], dependency_id: str, check: Callable[[], bool]
) -> None:
    """Register an availability check for a dependency."""
    checker["checks"][dependency_id] = check


def make_dependency_status(
    dependency_id: str, status: str, checked_at: datetime, details: str = ""
) -> Dict[str, Any]:
    """Create a dependency status dictionary."""
    return {
        "dependency_id": dependency_id,
        "status": status,
        "checked_at": checked_at,
        "details": details,
    }


def check_dependency(
    checker: Dict[str, Any], dependency_id: str, details: str = ""
) -> Dict[str, Any]:
    """Check a single dependency and return its status."""
    check_fn = checker["checks"].get(dependency_id)
    if check_fn is None:
        return make_dependency_status(
            dependency_id,
            "Unavailable",
            datetime.now(),
            "No check registered",
        )
    try:
        available = bool(check_fn())
    except Exception as exc:
        return make_dependency_status(
            dependency_id, "Unavailable", datetime.now(), str(exc)
        )
    return make_dependency_status(
        dependency_id,
        "Available" if available else "Unavailable",
        datetime.now(),
        details,
    )


def check_all_dependencies(
    checker: Dict[str, Any], dependency_ids: List[str]
) -> Dict[str, Dict[str, Any]]:
    """Check multiple dependencies and return a status map."""
    return {dep_id: check_dependency(checker, dep_id) for dep_id in dependency_ids}
