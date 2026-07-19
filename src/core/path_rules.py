"""Registro y evaluación de reglas de ruta (sin OOP).

Descripción:
    Este módulo proporciona utilidades ligeras para definir reglas de "paths"
    (identificadas por `path_id`) que determinan cuál salida/flujo debe
    ejecutarse en función del contexto (`path_context`) y los datos de entrada
    (`input_payload`). Las reglas incluyen condiciones de entrada, prioridad y
    dependencias bloqueantes. El diseño evita objetos complejos y usa
    diccionarios simples para facilitar las pruebas y la serialización.

Notas/Teoría:
    - Cada `path_id` suele tener la forma "operacion:detalle"; la parte antes
      de ':' se usa para agrupar reglas por operación.
    - La prioridad (campo `priority`) se usa para seleccionar la regla más
      relevante entre candidatos coincidentes; mayor valor = mayor prioridad.

"""

from typing import Any, Callable, Dict, List, Optional


def make_rule(
    path_id: str,
    priority: int,
    entry_conditions: Optional[List[Callable[..., bool]]] = None,
    output_definition: Optional[Dict[str, Any]] = None,
    blocking_dependencies: Optional[List[str]] = None,
) -> Dict[str, Any]:
    """Construir una definición de regla de ruta.

    Args:
        path_id: Identificador único de la regla (ej. "draw:early").
        priority: Prioridad numérica (mayor = preferida cuando hay empate).
        entry_conditions: Lista de funciones que reciben (path_context, input_payload)
            y devuelven True si la condición se cumple.
        output_definition: Diccionario que describe la salida esperada si la regla
            coincide (metadatos usados por el motor).
        blocking_dependencies: Lista de ids de dependencias que deben estar
            disponibles para que la regla sea válida.

    Returns:
        Dict[str, Any]: Estructura de regla lista para registrar.

    Notas:
        Las `entry_conditions` pueden ser funciones sencillas que consultan el
        contexto o el payload; se evalúan todas y la regla coincide solo si
        todas devuelven True.
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
    """Evaluar las condiciones de entrada de una regla.

    Itera sobre `entry_conditions` y llama cada función con `(path_context, input_payload)`.
    Si alguna condición devuelve False, la regla no coincide.

    Args:
        rule: Definición de regla creada por `make_rule`.
        path_context: Contexto del path donde se evalúa la regla.
        input_payload: Datos de entrada de la operación.

    Returns:
        bool: True si todas las condiciones se cumplen; False en caso contrario.
    """
    for condition in rule["entry_conditions"]:
        if not condition(path_context, input_payload):
            return False
    return True


def make_registry() -> Dict[str, Any]:
    """Crear un registro vacío de reglas.

    El registro es un diccionario con clave `rules` que mapea `path_id` a la
    definición de la regla. Se mantiene simple para facilitar pruebas y
    manipulación en memoria.
    """
    return {"rules": {}}


def _operation_key(path_id: str) -> str:
    """Extraer la clave de operación desde un `path_id`.

    Por convención `path_id` puede contener ':'; esta función devuelve la
    parte anterior a ':' que se utiliza para agrupar reglas de la misma
    operación.
    """
    return path_id.split(":", 1)[0]


def register_rule(registry: Dict[str, Any], rule: Dict[str, Any]) -> None:
    """Registrar una regla en el registro.

    Comprueba duplicados por `path_id` y evita duplicación de prioridad dentro
    de la misma operación (misma clave antes de ':').

    Args:
        registry: Estructura devuelta por `make_registry`.
        rule: Diccionario creado por `make_rule`.

    Raises:
        ValueError: Si existe `path_id` duplicado o una prioridad duplicada para
            la misma operación.
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
    """Seleccionar la regla aplicable de mayor prioridad para una operación.

    Busca reglas cuyo `path_id` comience con `operation_key + ':'` y que
    además cumplan sus condiciones de entrada. Si hay varias candidatas,
    devuelve la de mayor campo `priority`.

    Args:
        registry: Registro de reglas.
        operation_key: Llave de operación (parte antes de ':').
        path_context: Contexto para evaluar condiciones.
        input_payload: Payload de entrada.

    Returns:
        Optional[Dict[str, Any]]: Regla seleccionada o None si no hay coincidencias.
    """
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
    """Obtener una regla por su `path_id`.

    Args:
        registry: Registro de reglas.
        path_id: Identificador de la regla.

    Returns:
        Optional[Dict[str, Any]]: La regla si existe, o None.
    """
    return registry["rules"].get(path_id)
