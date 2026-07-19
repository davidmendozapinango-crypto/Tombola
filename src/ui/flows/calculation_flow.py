"""Adaptador GUI para disparar comandos de cálculo.

Descripción:
    Convierte la carga recibida desde la UI en un comando interno y lo ejecuta
    mediante `execute_command`. Actualiza el `state` del flujo según el
    resultado (éxito o error) y gestiona el indicador `is_loading`.
"""

from typing import Any, Dict
from src.core.calculation_engine import execute_command
from src.core.command_normalizer import normalize_command_payload
from src.ui.state.calculation_state import state_set_error, state_set_success


def make_flow(engine_context: Dict[str, Any], state: Dict[str, Any]) -> Dict[str, Any]:
    """Crear la estructura `flow` que agrupa el contexto del motor y el estado GUI.

    El `flow` se utiliza como adaptador entre la UI y el `calculation_engine`.
    """
    return {"engine_context": engine_context, "state": state}


def trigger(flow: Dict[str, Any], raw_payload: Dict[str, Any]) -> Dict[str, Any]:
    """Disparar un cálculo a partir de un payload de la GUI.

    Args:
        flow: Estructura creada por `make_flow`.
        raw_payload: Diccionario recibido desde la interfaz.

    Returns:
        Dict[str, Any]: Resultado devuelto por `execute_command`.
    """
    state = flow["state"]
    state["is_loading"] = True
    try:
        command = normalize_command_payload(raw_payload)
        result = execute_command(command, flow["engine_context"])
        if result["status"] == "success":
            state_set_success(state, result)
        else:
            state_set_error(state, result.get("error_message", "Error desconocido."))
        return result
    finally:
        state["is_loading"] = False
