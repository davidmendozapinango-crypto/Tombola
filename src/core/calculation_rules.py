"""Reglas concretas de cálculo y ejecución de funciones de resultado.

Define varias reglas de cálculo (suma simple, suma por lote, cobertura de
tarjeta, puntuación de juego, contexto SDG) y un constructor de registro por
defecto que facilita el registro de rutas de cálculo.
"""

from typing import Any, Callable, Dict, List, Optional
from src.core.card import card_points
from src.core.game import check_winner, game_summary
from src.core.path_rules import make_registry, make_rule, register_rule
from src.ods.data import get_sdg_name, get_sdg_slogan


def _sum_single_entry(ctx: Dict[str, Any], payload: Dict[str, Any]) -> bool:
    return ctx.get("mode") == "single" and "a" in payload and ("b" in payload)


def _sum_batch_entry(ctx: Dict[str, Any], payload: Dict[str, Any]) -> bool:
    return ctx.get("mode") == "batch" and "items" in payload


def _sum_single_compute(payload: Dict[str, Any]) -> Dict[str, Any]:
    a = payload.get("a", 0)
    b = payload.get("b", 0)
    return {"sum": a + b, "operands": [a, b]}


def _sum_batch_compute(payload: Dict[str, Any]) -> Dict[str, Any]:
    items = payload.get("items", [])
    return {"sum": sum(items), "count": len(items), "items": items}


def _card_coverage_entry(ctx: Dict[str, Any], payload: Dict[str, Any]) -> bool:
    return (
        ctx.get("domain") == "tombola"
        and ctx.get("path") == "card_coverage"
        and ("card" in payload)
        and ("drawn_numbers" in payload)
    )


def _card_coverage_compute(payload: Dict[str, Any]) -> Dict[str, Any]:
    card = payload["card"]
    drawn = set(payload.get("drawn_numbers", []))
    total_cells = sum((len(row) for row in card))
    marked_cells = sum((1 for row in card for value in row if value in drawn))
    coverage = marked_cells / total_cells if total_cells else 0.0
    missing = [value for row in card for value in row if value not in drawn]
    return {
        "total_cells": total_cells,
        "marked_cells": marked_cells,
        "coverage_ratio": coverage,
        "coverage_percentage": round(coverage * 100, 2),
        "missing_numbers": missing,
    }


def _game_score_entry(ctx: Dict[str, Any], payload: Dict[str, Any]) -> bool:
    return (
        ctx.get("domain") == "tombola"
        and ctx.get("path") == "game_score"
        and ("main_card" in payload)
        and ("complement_card" in payload)
        and ("drawn_numbers" in payload)
    )


def _game_score_compute(payload: Dict[str, Any]) -> Dict[str, Any]:
    """
    Calcula la puntuación del juego a partir de las tarjetas y los números
    extraídos.

    Utiliza `game_summary` para obtener el ganador y los puntos; devuelve un
    diccionario con resumen y puntos totales.
    """
    main_card = payload["main_card"]
    complement_card = payload["complement_card"]
    drawn = set(payload.get("drawn_numbers", []))
    summary = game_summary(main_card, drawn, complement_card, drawn, card_type="A")
    winner = summary["winner"]
    total_points = summary["main_points"] + summary["complement_points"]
    return {
        "winner": winner,
        "main_points": summary["main_points"],
        "complement_points": summary["complement_points"],
        "total_points": total_points,
    }


def _sdg_context_entry(ctx: Dict[str, Any], payload: Dict[str, Any]) -> bool:
    return (
        ctx.get("domain") == "tombola"
        and ctx.get("path") == "sdg_context"
        and ("sdg_id" in payload)
    )


def _sdg_context_compute(payload: Dict[str, Any]) -> Dict[str, Any]:
    sdg_id = payload.get("sdg_id", 1)
    return {
        "sdg_id": sdg_id,
        "sdg_name": get_sdg_name(sdg_id),
        "sdg_slogan": get_sdg_slogan(sdg_id),
    }


def build_default_registry(dependencies: Optional[List[str]] = None) -> Dict[str, Any]:
    """
    Construye un `registry` con reglas de cálculo concretas ya registradas.

    Parámetros
    ----------
    dependencies : Optional[List[str]]
        Lista de dependencias bloqueantes que se aplican a todas las reglas.
    """
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
    register_rule(
        registry,
        make_rule(
            path_id="tombola:card_coverage",
            priority=20,
            entry_conditions=[_card_coverage_entry],
            output_definition={
                "impact_marker": "tombola_card_coverage",
                "compute": _card_coverage_compute,
            },
            blocking_dependencies=deps,
        ),
    )
    register_rule(
        registry,
        make_rule(
            path_id="tombola:game_score",
            priority=15,
            entry_conditions=[_game_score_entry],
            output_definition={
                "impact_marker": "tombola_game_score",
                "compute": _game_score_compute,
            },
            blocking_dependencies=deps,
        ),
    )
    register_rule(
        registry,
        make_rule(
            path_id="tombola:sdg_context",
            priority=8,
            entry_conditions=[_sdg_context_entry],
            output_definition={
                "impact_marker": "tombola_sdg_context",
                "compute": _sdg_context_compute,
            },
            blocking_dependencies=deps,
        ),
    )
    return registry


def compute_result(
    rule: Dict[str, Any], input_payload: Dict[str, Any]
) -> Dict[str, Any]:
    """
    Ejecuta la función `compute` definida en la regla de ruta.

    Si la regla no define una función `compute`, se devuelve el payload de
    entrada como fallback.
    """
    compute_fn = rule["output_definition"].get("compute")
    if compute_fn is None:
        return {"inputs": input_payload}
    return compute_fn(input_payload)
