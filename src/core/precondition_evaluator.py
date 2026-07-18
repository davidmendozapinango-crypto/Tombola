"""Funciones para evaluación de precondiciones en orden de prioridad.

Estas utilidades permiten validar conjuntos de precondiciones y evaluar el
resultado agregado devolviendo la primera precondición fallida de mayor
prioridad (el menor `priority_rank`).
"""

from typing import Any, Dict, List, Optional, Tuple

from src.core.preconditions import evaluate_precondition


def validate_precondition_set(preconditions: List[Dict[str, Any]]) -> None:
    """
    Valida que no existan `priority_rank` duplicados en el conjunto de
    precondiciones.

    Lanza `ValueError` si detecta dos precondiciones con el mismo `priority_rank`.
    """
    ranks: Dict[int, Dict[str, Any]] = {}
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
    """
    Evalúa todas las precondiciones y devuelve si todas pasan y la falla más
    prioritaria en caso contrario.

    Retorna una tupla `(all_passed, highest_priority_failure)` donde
    `highest_priority_failure` es `None` si todas pasan.
    """
    validate_precondition_set(preconditions)
    failures = [p for p in preconditions if not evaluate_precondition(p, payload)]
    if not failures:
        return (True, None)
    highest_priority_failure = min(failures, key=lambda p: p["priority_rank"])
    return (False, highest_priority_failure)
