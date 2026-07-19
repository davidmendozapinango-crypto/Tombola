"""Helpers para definir y evaluar precondiciones de negocio.

Descripción:
    Las precondiciones representan reglas simples que deben cumplirse antes
    de ejecutar una operación de negocio. Estas funciones ayudan a crear la
    estructura de una precondición y a evaluarla de forma segura.

Notas/Teoría:
    - Una precondición es una estructura ligera (diccionario) que contiene
      un `check`, una función que recibe el `payload` y devuelve True/False.
    - Se mantienen como datos y funciones en lugar de clases para facilitar
      la composición dinámica y las pruebas unitarias.

Ejemplo:
    >>> p = make_precondition('has_money', 'El actor debe tener saldo', 10, lambda pl: pl.get('balance',0) > 0, 'no_balance')
    >>> evaluate_precondition(p, {'balance': 5})
    True
"""

from typing import Any, Callable, Dict


def make_precondition(
    precondition_id: str,
    description: str,
    priority_rank: int,
    check: Callable[[Dict[str, Any]], bool],
    failure_message_id: str,
) -> Dict[str, Any]:
    """Crear un diccionario que representa una precondición.

    Args:
        precondition_id: Identificador único de la precondición.
        description: Texto descriptivo de la precondición.
        priority_rank: Prioridad numérica (menor = más prioritaria).
        check: Función que recibe el `payload` y devuelve True si pasa.
        failure_message_id: Identificador del mensaje de fallo asociado.

    Returns:
        Dict[str, Any]: Diccionario con la definición completa de la precondición.

    Notas:
        La función `check` puede lanzar excepciones. Se recomienda que las
        funciones `check` sean pequeñas y robustas; las excepciones se
        consideran fallos de precondición al evaluarlas con
        `evaluate_precondition`.
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
    """Evaluar una precondición de forma segura frente a excepciones.

    Descripción:
        Invoca la función `check` definida en la precondición con el payload
        proporcionado. Si la función lanza una excepción, se captura y se
        considera que la precondición no pasa (devuelve False).

    Notas:
        - Esta función encapsula la evaluación para evitar que una excepción
          en una precondición interrumpa el flujo del motor; por tanto, el
          comportamiento es seguro frente a errores en `check`.
        - Si se desea diferenciar errores de precondición de errores internos,
          adaptar `check` para devolver un objeto detallado en lugar de bool.

    Args:
        precondition: Diccionario que contiene la clave `check` con la función.
        payload: Datos sobre los que evaluar la precondición.

    Returns:
        bool: True si la precondición se cumple; False en caso contrario o si
            se produce una excepción durante la evaluación.
    """
    try:
        return bool(precondition["check"](payload))
    except Exception:
        return False
