"""Localized business error catalog helpers (non-OOP)."""

from typing import Any, Dict, Optional

DEFAULT_LOCALE = "es-VE"

MESSAGES: Dict[str, Dict[str, str]] = {
    "missing_actor_id": {
        "es-VE": "El identificador del jugador es obligatorio. Inicie sesión nuevamente.",
    },
    "missing_operation_key": {
        "es-VE": "Debe seleccionar una operación de cálculo válida.",
    },
    "missing_path_context": {
        "es-VE": "El contexto operativo está incompleto. Verifique los datos ingresados.",
    },
    "missing_input_payload": {
        "es-VE": "Faltan datos necesarios para ejecutar el cálculo.",
    },
    "missing_ui_origin": {
        "es-VE": "No se pudo determinar la pantalla que inició la acción.",
    },
    "invalid_path_state": {
        "es-VE": "El estado actual no permite ejecutar esta operación.",
    },
    "dependency_unavailable": {
        "es-VE": "Un recurso requerido no está disponible en este momento. Intente más tarde.",
    },
}


def get_message(
    message_id: str,
    locale: str = DEFAULT_LOCALE,
    catalog: Optional[Dict[str, Dict[str, str]]] = None,
) -> str:
    """Look up a localized message by id."""
    catalog = catalog or MESSAGES
    message_catalog = catalog.get(message_id, {})
    return (
        message_catalog.get(locale) or message_catalog.get(DEFAULT_LOCALE) or message_id
    )


def register_message(
    message_id: str,
    text: str,
    locale: str = DEFAULT_LOCALE,
    catalog: Optional[Dict[str, Dict[str, str]]] = None,
) -> None:
    """Register a new localized message."""
    catalog = catalog or MESSAGES
    if message_id not in catalog:
        catalog[message_id] = {}
    catalog[message_id][locale] = text


def build_error_response(
    error_type: str,
    error_code: str,
    catalog: Optional[Dict[str, Dict[str, str]]] = None,
    locale: str = DEFAULT_LOCALE,
) -> Dict[str, str]:
    """Build a standardized failure response dictionary."""
    return {
        "status": "failure",
        "error_type": error_type,
        "error_code": error_code,
        "error_message": get_message(error_code, locale, catalog),
        "retry_hint": "Verifique los datos e intente nuevamente.",
    }
