"""Path rule registry helpers (non-OOP)."""

from typing import Any, Callable, Dict, List, Optional


def make_rule(
    path_id: str,
    priority: int,
    entry_conditions: Optional[List[Callable[..., bool]]] = None,
    output_definition: Optional[Dict[str, Any]] = None,
    blocking_dependencies: Optional[List[str]] = None,
) -> Dict[str, Any]:
    """Create a path rule dictionary."""
    return {
        "path_id": path_id,
        "priority": priority,
        "entry_conditions": entry_conditions or [],
        "output_definition": output_definition or {},
        "blocking_dependencies": blocking_dependencies or [],
    }


def rule_matches(
    rule: Dict[str, Any], path_context: Dict[str, Any], input_payload: Dict[str, Any]
) -> bool:
    """Evaluate all entry conditions of a rule against context and input."""
    for condition in rule["entry_conditions"]:
        if not condition(path_context, input_payload):
            return False
    return True


def make_registry() -> Dict[str, Any]:
    """Create an empty rule registry."""
    return {"rules": {}}


def register_rule(registry: Dict[str, Any], rule: Dict[str, Any]) -> None:
    """Register a rule in the registry."""
    if rule["path_id"] in registry["rules"]:
        raise ValueError(f"Duplicate path_id: {rule['path_id']}")
    registry["rules"][rule["path_id"]] = rule


def select_rule(
    registry: Dict[str, Any],
    operation_key: str,
    path_context: Dict[str, Any],
    input_payload: Dict[str, Any],
) -> Optional[Dict[str, Any]]:
    """Select the matching rule with highest priority for an operation."""
    candidates = [
        rule
        for rule in registry["rules"].values()
        if rule["path_id"].startswith(f"{operation_key}:")
        and rule_matches(rule, path_context, input_payload)
    ]
    if not candidates:
        return None
    return max(candidates, key=lambda r: r["priority"])


def get_rule(registry: Dict[str, Any], path_id: str) -> Optional[Dict[str, Any]]:
    """Get a rule by path_id."""
    return registry["rules"].get(path_id)
