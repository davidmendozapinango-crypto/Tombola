"""Normalizar el payload de la GUI a un diccionario de comando interno.

Descripción:
    Convierte la carga de datos cruda proveniente de la interfaz en la
    estructura interna esperada por el motor, aplicando valores por defecto
    cuando faltan campos.
"""

from datetime import datetime
from typing import Any, Dict
from src.core.command_contract import make_command


def normalize_command_payload(payload: Dict[str, Any]) -> Dict[str, Any]:
    """Convertir un payload crudo de GUI en un diccionario de comando.

    Args:
        payload: Diccionario recibido desde la interfaz de usuario.

    Returns:
        Dict[str, Any]: Comando interno normalizado con campos por defecto cuando proceda.

    Notas:
        - Esta función aplica valores por defecto mínimos para evitar que el
          motor falle por campos faltantes; no sustituye validaciones más
          específicas que hacen los precondiciones o las reglas de negocio.
        - `requested_at` se establece en `datetime.now()` si no se proporciona,
          por lo que para reproducibilidad en pruebas puede inyectarse un
          valor controlado.
    """
    return make_command(
        actor_id=payload.get("actor_id", ""),
        operation_key=payload.get("operation_key", ""),
        path_context=payload.get("path_context", {}),
        input_payload=payload.get("input_payload", {}),
        ui_origin=payload.get("ui_origin", ""),
        command_id=payload.get("command_id"),
        trace_label=payload.get("trace_label"),
        requested_at=payload.get("requested_at", datetime.now()),
    )
