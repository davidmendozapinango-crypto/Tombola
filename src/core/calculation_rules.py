"""Concrete calculation path rules and result computation (non-OOP)."""

from typing import Any, Callable, Dict, List, Optional

from src.core.path_rules import make_registry, make_rule, register_rule


def _sum_single_entry(ctx: Dict[str, Any], payload: Dict[str, Any]) -> bool:
    return ctx.get("mode") == "single" and "a" in payload and "b" in payload


def _sum_batch_entry(ctx: Dict[str, Any], payload: Dict[str, Any]) -> bool:
    return ctx.get("mode") == "batch" and "items" in payload


def _sum_single_compute(payload: Dict[str, Any]) -> Dict[str, Any]:
    a = payload.get("a", 0)
    b = payload.get("b", 0)
    return {"sum": a + b, "operands": [a, b]}


def _sum_batch_compute(payload: Dict[str, Any]) -> Dict[str, Any]:
    items = payload.get("items", [])
    return {"sum": sum(items), "count": len(items), "items": items}


def build_default_registry(
    dependencies: Optional[List[str]] = None,
) -> Dict[str, Any]:
    """Build a registry with concrete calculation path rules."""
    registry = make_registry()
    deps = dependencies or []
    register_rule(
        registry,
        make_rule(
            path_id="sum:single",
            priority=10,
            entry_conditions=[_sum_single_entry],
            output_definition={
                "impact_marker": "sum_single",
                "compute": _sum_single_compute,
            },
            blocking_dependencies=deps,
        ),
    )
    register_rule(
        registry,
        make_rule(
            path_id="sum:batch",
            priority=5,
            entry_conditions=[_sum_batch_entry],
            output_definition={
                "impact_marker": "sum_batch",
                "compute": _sum_batch_compute,
            },
            blocking_dependencies=deps,
        ),
    )
    return registry


def compute_result(
    rule: Dict[str, Any], input_payload: Dict[str, Any]
) -> Dict[str, Any]:
    """Execute the compute function defined by the path rule."""
    compute_fn = rule["output_definition"].get("compute")
    if compute_fn is None:
        return {"inputs": input_payload}
    return compute_fn(input_payload)
