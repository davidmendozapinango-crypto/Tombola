"""Screen controller for GUI calculation actions with keyboard accessibility (non-OOP)."""
from typing import Any, Dict
from src.ui.flows.calculation_flow import make_flow, trigger
CONTROLS = ['calculate_button', 'cancel_button']

def make_screen(engine_context: Dict[str, Any], state: Dict[str, Any]) -> Dict[str, Any]:
    """Create a calculation screen dictionary."""
    screen = {'flow': make_flow(engine_context, state), 'controls': list(CONTROLS), 'focus_index': -1, 'focused_control': None}
    focus_next(screen)
    return screen

def on_calculate_action(screen: Dict[str, Any], raw_payload: Dict[str, Any]) -> Dict[str, Any]:
    """Handle a user-triggered calculation action."""
    return trigger(screen['flow'], raw_payload)

def focus_next(screen: Dict[str, Any]) -> None:
    """Move focus to the next control (keyboard navigation)."""
    screen['focus_index'] = (screen['focus_index'] + 1) % len(screen['controls'])
    screen['focused_control'] = screen['controls'][screen['focus_index']]

def focus_previous(screen: Dict[str, Any]) -> None:
    """Move focus to the previous control (keyboard navigation)."""
    screen['focus_index'] = (screen['focus_index'] - 1) % len(screen['controls'])
    screen['focused_control'] = screen['controls'][screen['focus_index']]