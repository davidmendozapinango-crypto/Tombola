import pytest
from src.core.calculation_engine import execute_command, make_engine_context
from src.core.calculation_rules import build_default_registry
from src.core.dependencies import make_dependency_checker, register_dependency
from src.core.preconditions import make_precondition
from src.ui.screens.calculation_screen import make_screen, on_calculate_action
from src.ui.state.calculation_state import make_state

def _make_screen():
    registry = build_default_registry(dependencies=['player_session'])
    checker = make_dependency_checker()
    register_dependency(checker, 'player_session', lambda : True)
    preconditions = [make_precondition(precondition_id='actor_present', description='Actor present', priority_rank=1, check=lambda p: bool(p['command']['actor_id']), failure_message_id='missing_actor_id')]
    engine_context = make_engine_context(registry, preconditions, checker)
    state = make_state()
    return make_screen(engine_context, state)

def test_gui_trigger_success():
    screen = _make_screen()
    raw_payload = {'actor_id': 'player-001', 'operation_key': 'sum', 'path_context': {'mode': 'single'}, 'input_payload': {'a': 5, 'b': 3}, 'ui_origin': 'calculator_screen'}
    result = on_calculate_action(screen, raw_payload)
    assert result['status'] == 'success'
    assert result['path_id'] == 'sum:single'
    assert screen['flow']['state']['error_message'] == ''
    assert screen['flow']['state']['result'] is not None