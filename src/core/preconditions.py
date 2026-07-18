"""Utilidades para precondiciones de negocio.

Permite construir objetos de precondición (como diccionarios) y evaluarlos de
forma segura contra un `payload`. Las precondiciones contienen una función
`check` que recibe el payload y devuelve booleano.
"""

from typing import Any, Callable, Dict


def make_precondition(
    precondition_id: str,
    description: str,
    priority_rank: int,
    check: Callable[[Dict[str, Any]], bool],
    failure_message_id: str,
) -> Dict[str, Any]:
    """
    Crea un diccionario que representa una precondición de negocio.

    Parámetros
    ----------
    precondition_id : str
        Identificador único de la precondición.
    description : str
        Descripción legible de la precondición.
    priority_rank : int
        Entero donde un valor menor indica mayor prioridad.
    check : Callable[[Dict[str, Any]], bool]
        Función que recibe el `payload` y devuelve `True` si la condición se
        cumple.
    failure_message_id : str
        Identificador del mensaje de error asociado a la falla.

    Devuelve
    -------
    Dict[str, Any]
        Diccionario listo para ser usado por el evaluador de precondiciones.
    """
    return {
        "precondition_id": precondition_id,
        "description": description,
        "priority_rank": priority_rank,
        "check": check,
        "failure_message_id": failure_message_id,
    }


def evaluate_precondition(
    precondition: Dict[str, Any], payload: Dict[str, Any]
) -> bool:
    """
    Evalúa una única precondición contra el `payload` de forma segura.

    Si la función `check` lanza una excepción, se captura y se considera que
    la precondición ha fallado (devuelve `False`).
    """
    try:
        return bool(precondition["check"](payload))
    except Exception:
        return False
