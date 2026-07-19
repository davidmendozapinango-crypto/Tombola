"""Utilidades para el contrato de comandos internos (payloads desde la GUI).

Descripción:
    Facilita la creación de comandos internos y la validación de campos
    requeridos antes de su procesamiento por el motor de cálculo.
"""

from datetime import datetime
from typing import Any, Dict, List, Optional


def make_command(
    actor_id: str,
    operation_key: str,
    path_context: Dict[str, Any],
    input_payload: Dict[str, Any],
    ui_origin: str,
    command_id: Optional[str] = None,
    trace_label: Optional[str] = None,
    requested_at: Optional[datetime] = None,
) -> Dict[str, Any]:
    """Crear un diccionario que representa un comando interno.

    Args:
        actor_id: Identificador del actor (usuario) que origina el comando.
        operation_key: Clave de la operación a ejecutar.
        path_context: Contexto de ruta/path asociado.
        input_payload: Datos de entrada para la operación.
        ui_origin: Punto de interacción UI que generó el comando.
        command_id: Identificador opcional del comando; si no se provee se genera uno.
        trace_label: Etiqueta opcional para traza/debug.
        requested_at: Marca temporal opcional; si no se provee se toma `datetime.now()`.

    Returns:
        Dict[str, Any]: Estructura lista para ser procesada por el motor.
    """
    return {
        "actor_id": actor_id,
        "operation_key": operation_key,
        "path_context": path_context,
        "input_payload": input_payload,
        "ui_origin": ui_origin,
        "command_id": command_id or f"cmd-{datetime.now().strftime('%Y%m%d%H%M%S%f')}",
        "trace_label": trace_label,
        "requested_at": requested_at or datetime.now(),
    }


def validate_required_fields(command: Dict[str, Any]) -> List[str]:
    """Devolver la lista de nombres de campos requeridos que faltan.

    Verifica que los campos esenciales estén presentes y no vacíos.
    """
    missing = []
    for attr in ["actor_id", "operation_key", "ui_origin"]:
        value = command.get(attr)
        if value is None or (isinstance(value, str) and value.strip() == ""):
            missing.append(attr)
    if command.get("path_context") is None:
        missing.append("path_context")
    if command.get("input_payload") is None:
        missing.append("input_payload")
    return missing
