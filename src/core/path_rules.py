"""Ayudantes para el registro y selección de reglas de ruta (path rules).

Un `registry` es un contenedor simple que almacena reglas identificadas por
`path_id`. Cada regla contiene condiciones de entrada, definición de salida y
lista de dependencias que pueden bloquear su ejecución.
"""

from typing import Any, Callable, Dict, List, Optional


def make_rule(
    path_id: str,
    priority: int,
    entry_conditions: Optional[List[Callable[..., bool]]] = None,
    output_definition: Optional[Dict[str, Any]] = None,
    blocking_dependencies: Optional[List[str]] = None,
) -> Dict[str, Any]:
    """
    Construye un diccionario que representa una regla de ruta.

    Parámetros
    ----------
    path_id : str
        Identificador único de la regla, normalmente con formato
        `<operacion>:<subpath>`.
    priority : int
        Prioridad de la regla; valores mayores indican mayor prioridad.
    entry_conditions : Optional[List[Callable[..., bool]]]
        Lista de llamadas que determinan si la regla aplica para un contexto
        y payload dados.
    output_definition : Optional[Dict[str, Any]]
        Definición de salida que puede incluir la función `compute`.
    blocking_dependencies : Optional[List[str]]
        Lista de ids de dependencias que bloquean la ejecución de la regla.
    """
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
    """Evalúa todas las condiciones de entrada de una regla contra el contexto y el payload."""
    for condition in rule["entry_conditions"]:
        if not condition(path_context, input_payload):
            return False
    return True


def make_registry() -> Dict[str, Any]:
    """Crea un registro vacío para almacenar reglas."""
    return {"rules": {}}


def _operation_key(path_id: str) -> str:
    """Devuelve la clave de operación (prefijo) de un `path_id`."""
    return path_id.split(":", 1)[0]


def register_rule(registry: Dict[str, Any], rule: Dict[str, Any]) -> None:
    """Registra una regla en el `registry`.

    Valida que no exista otra regla con el mismo `path_id` y que no haya
    conflicto de prioridad entre reglas de la misma operación.
    """
    if rule["path_id"] in registry["rules"]:
        raise ValueError(f"Duplicate path_id: {rule['path_id']}")
    operation = _operation_key(rule["path_id"])
    for existing in registry["rules"].values():
        if (
            _operation_key(existing["path_id"]) == operation
            and existing["priority"] == rule["priority"]
        ):
            raise ValueError(
                f"Duplicate priority {rule['priority']} for operation '{operation}' between '{existing['path_id']}' and '{rule['path_id']}'"
            )
    registry["rules"][rule["path_id"]] = rule


def select_rule(
    registry: Dict[str, Any],
    operation_key: str,
    path_context: Dict[str, Any],
    input_payload: Dict[str, Any],
) -> Optional[Dict[str, Any]]:
    """Selecciona la regla aplicable con mayor prioridad para una operación dada."""
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
    """Obtiene una regla por su `path_id` si existe, o `None` en otro caso."""
    return registry["rules"].get(path_id)
