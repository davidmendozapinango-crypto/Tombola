"""Global application state helpers (non-OOP)."""
from typing import Any, Dict
from src.auth.session import make_session

def make_app_state() -> Dict[str, Any]:
    """Create the global application state dictionary."""
    return {'current_screen': 'login', 'running': True, 'session': make_session(), 'players': [], 'games': [], 'error_message': '', 'info_message': '', 'inputs': {}, 'focus_index': 0, 'focusable': []}

def set_screen(state: Dict[str, Any], screen_name: str) -> None:
    """Change the active screen and clear transient messages."""
    state['current_screen'] = screen_name
    state['error_message'] = ''
    state['info_message'] = ''
    state['inputs'] = {}
    state['focus_index'] = 0
    state['focusable'] = []

def set_error(state: Dict[str, Any], message: str) -> None:
    """Set an error message."""
    state['error_message'] = message

def set_info(state: Dict[str, Any], message: str) -> None:
    """Set an informational message."""
    state['info_message'] = message

def cycle_focus(state: Dict[str, Any], direction: int=1) -> None:
    """Move keyboard focus in the given direction."""
    focusable = state.get('focusable') or []
    if not focusable:
        return
    state['focus_index'] = (state['focus_index'] + direction) % len(focusable)

def get_focused(state: Dict[str, Any]) -> str:
    """Return the currently focused control name."""
    focusable = state.get('focusable') or []
    if not focusable:
        return ''
    return focusable[state['focus_index']]

def is_focused(state: Dict[str, Any], name: str) -> bool:
    """Return True if the named control is currently focused."""
    return get_focused(state) == name