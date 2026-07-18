"""Internal command payload helpers (non-OOP)."""
from datetime import datetime
from typing import Any, Dict, List, Optional


def make_command(actor_id: str, operation_key: str, path_context: Dict[str, Any], input_payload: Dict[str, Any], ui_origin: str, command_id: Optional[str]=None, trace_label: Optional[str]=None, requested_at: Optional[datetime]=None) -> Dict[str, Any]:
    """Create an internal command dictionary from GUI interaction."""
    return {'actor_id': actor_id, 'operation_key': operation_key, 'path_context': path_context, 'input_payload': input_payload, 'ui_origin': ui_origin, 'command_id': command_id or f"cmd-{datetime.now().strftime('%Y%m%d%H%M%S%f')}", 'trace_label': trace_label, 'requested_at': requested_at or datetime.now()}

def validate_required_fields(command: Dict[str, Any]) -> List[str]:
    """Return list of missing required field names."""
    missing = []
    for attr in ['actor_id', 'operation_key', 'ui_origin']:
        value = command.get(attr)
        if value is None or (isinstance(value, str) and value.strip() == ''):
            missing.append(attr)
    if command.get('path_context') is None:
        missing.append('path_context')
    if command.get('input_payload') is None:
        missing.append('input_payload')
    return missing