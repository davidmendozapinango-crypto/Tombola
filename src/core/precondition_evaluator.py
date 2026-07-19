"""Evaluación de precondiciones de negocio y utilidades relacionadas.

Descripción:
    Proporciona funciones para validar conjuntos de precondiciones y
    evaluar todas ellas respetando su orden de prioridad.
"""

from typing import Any, Dict, List, Optional, Tuple
from src.core.preconditions import evaluate_precondition


def validate_precondition_set(preconditions: List[Dict[str, Any]]) -> None:
    """Validar que los `priority_rank` son únicos en el conjunto.

    Se lanza `ValueError` si hay prioridades duplicadas, lo que evita
    ambigüedades cuando se selecciona la precondición fallida de mayor prioridad.
    """
    ranks = {}
    for precondition in preconditions:
        rank = precondition["priority_rank"]
        if rank in ranks:
            raise ValueError(
                f"Duplicate priority_rank {rank} in preconditions '{ranks[rank]['precondition_id']}' and '{precondition['precondition_id']}'"
            )
        ranks[rank] = precondition


def evaluate_preconditions(
    preconditions: List[Dict[str, Any]], payload: Dict[str, Any]
) -> Tuple[bool, Optional[Dict[str, Any]]]:
    """Evaluar todas las precondiciones y retornar el fallo de mayor prioridad.

    Flujo:
        1. Validar que no haya prioridades duplicadas.
        2. Evaluar cada precondición contra el `payload`.
        3. Si no hay fallos, devolver (True, None); de lo contrario devolver
           (False, failure) donde `failure` es la precondición con menor
           `priority_rank` (más prioritaria).

    Returns:
        Tuple[bool, Optional[Dict[str, Any]]]: (todas_pasaron, falla_mas_prioritaria)
    """
    validate_precondition_set(preconditions)
    failures = [
        precondition
        for precondition in preconditions
        if not evaluate_precondition(precondition, payload)
    ]
    if not failures:
        return (True, None)
    highest_priority_failure = min(failures, key=lambda p: p["priority_rank"])
    return (False, highest_priority_failure)
