"""GUI trigger adapter for calculation commands (non-OOP)."""
from typing import Any, Dict
from src.core.calculation_engine import execute_command
from src.core.command_normalizer import normalize_command_payload
from src.ui.state.calculation_state import state_set_error, state_set_success

def make_flow(engine_context: Dict[str, Any], state: Dict[str, Any]) -> Dict[str, Any]:
    """Create a calculation flow dictionary."""
    return {'engine_context': engine_context, 'state': state}

def trigger(flow: Dict[str, Any], raw_payload: Dict[str, Any]) -> Dict[str, Any]:
    """Trigger calculation from a GUI payload."""
    state = flow['state']
    state['is_loading'] = True
    try:
        command = normalize_command_payload(raw_payload)
        result = execute_command(command, flow['engine_context'])
        if result['status'] == 'success':
            state_set_success(state, result)
        else:
            state_set_error(state, result.get('error_message', 'Error desconocido.'))
        return result
    finally:
        state['is_loading'] = False