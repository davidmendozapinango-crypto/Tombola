"""Ayudantes para verificación de dependencias externas.

Descripción:
    Provee un pequeño mecanismo para registrar verificaciones de
    disponibilidad de dependencias (por ejemplo, servicios externos) y
    consultar su estado actual.
"""

from datetime import datetime
from typing import Any, Callable, Dict, List


def make_dependency_checker() -> Dict[str, Any]:
    """Crear un comprobador de dependencias vacío.

    Devuelve una estructura que puede registrar funciones verificadoras por id.
    """
    return {"checks": {}}


def register_dependency(
    checker: Dict[str, Any], dependency_id: str, check: Callable[[], bool]
) -> None:
    """Registrar una función que verifica la disponibilidad de una dependencia.

    Args:
        checker: Estructura devuelta por `make_dependency_checker`.
        dependency_id: Identificador único de la dependencia.
        check: Función sin argumentos que devuelve True si la dependencia está disponible.
    """
    checker["checks"][dependency_id] = check


def make_dependency_status(
    dependency_id: str, status: str, checked_at: datetime, details: str = ""
) -> Dict[str, Any]:
    """Construir el diccionario que representa el estado de una dependencia.

    Args:
        dependency_id: Identificador de la dependencia.
        status: Cadena que indica estado; por convención 'Available' o 'Unavailable'.
        checked_at: Marca temporal de la verificación.
        details: Texto adicional con información de diagnóstico.

    Returns:
        Dict[str, Any]: Estructura con información de estado lista para serializar.
    """
    return {
        "dependency_id": dependency_id,
        "status": status,
        "checked_at": checked_at,
        "details": details,
    }


def check_dependency(
    checker: Dict[str, Any], dependency_id: str, details: str = ""
) -> Dict[str, Any]:
    """Comprobar una dependencia y devolver su estado.

    Si no existe una función registrada para la dependencia, se considera
    `Unavailable`. Las excepciones lanzadas por la función de comprobación se
    capturan y se reportan en `details`.
    """
    check_fn = checker["checks"].get(dependency_id)
    if check_fn is None:
        return make_dependency_status(
            dependency_id, "Unavailable", datetime.now(), "No check registered"
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
    """Comprobar múltiples dependencias y devolver un mapa de estados.

    Returns:
        Dict[str, Dict[str, Any]]: Mapa de dependency_id -> status dict.
    """
    return {dep_id: check_dependency(checker, dep_id) for dep_id in dependency_ids}
