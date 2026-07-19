"""Helpers de estado GUI para flujos de cálculo.

Descripción:
    Provee una estructura de estado simple y funciones para actualizarla en
    respuesta a resultados de cálculo (éxito o error) o para reiniciarla.
"""

from typing import Any, Dict, Optional


def make_state() -> Dict[str, Any]:
    """
    Crear el diccionario de estado inicial para el flujo de cálculo.

    Campos:
        result: Resultado del cálculo (o None si no existe).
        error_message: Mensaje de error si ocurrió alguno.
        is_loading: Indicador de carga en curso.
        impact_validated: Indica si el impacto del último resultado fue validado.
    """
    return {
        "result": None,
        "error_message": "",
        "is_loading": False,
        "impact_validated": False,
    }


def state_set_success(state: Dict[str, Any], result: Dict[str, Any]) -> None:
    """Actualizar el estado al recibir un resultado exitoso.

    Se borra cualquier mensaje de error y se marca `impact_validated` si el
    resultado incluye un `impact_marker`.
    """
    state["result"] = result
    state["error_message"] = ""
    state["impact_validated"] = bool(result.get("impact_marker"))


def state_set_error(state: Dict[str, Any], message: str) -> None:
    """Actualizar el estado cuando ocurre un error en el cálculo.

    Se registra el mensaje de error y se limpia cualquier resultado previo.
    """
    state["error_message"] = message
    state["result"] = None
    state["impact_validated"] = False


def state_clear(state: Dict[str, Any]) -> None:
    """Restablecer el estado del flujo de cálculo a sus valores iniciales."""
    state["result"] = None
    state["error_message"] = ""
    state["is_loading"] = False
    state["impact_validated"] = False
