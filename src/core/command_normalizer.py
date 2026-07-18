"""Normalize GUI payload into an internal command dictionary (non-OOP)."""
from datetime import datetime
from typing import Any, Dict

from src.core.command_contract import make_command


def normalize_command_payload(payload: Dict[str, Any]) -> Dict[str, Any]:
    """Convert a raw GUI payload into a command dictionary."""
    return make_command(actor_id=payload.get('actor_id', ''), operation_key=payload.get('operation_key', ''), path_context=payload.get('path_context', {}), input_payload=payload.get('input_payload', {}), ui_origin=payload.get('ui_origin', ''), command_id=payload.get('command_id'), trace_label=payload.get('trace_label'), requested_at=payload.get('requested_at', datetime.now()))