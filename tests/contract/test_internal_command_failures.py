import pytest
from src.core.calculation_engine import execute_command, make_engine_context
from src.core.calculation_rules import build_default_registry
from src.core.command_contract import make_command
from src.core.dependencies import make_dependency_checker, register_dependency
from src.core.preconditions import make_precondition

def _make_engine():
    registry = build_default_registry(dependencies=['player_session'])
    checker = make_dependency_checker()
    register_dependency(checker, 'player_session', lambda : True)
    preconditions = [make_precondition(precondition_id='actor_present', description='Actor present', priority_rank=1, check=lambda p: bool(p['command']['actor_id']), failure_message_id='missing_actor_id'), make_precondition(precondition_id='operation_valid', description='Operation valid', priority_rank=2, check=lambda p: bool(p['command']['operation_key']), failure_message_id='missing_operation_key')]
    return make_engine_context(registry, preconditions, checker)

def test_failure_shape_has_error_type():
    context = _make_engine()
    command = make_command(actor_id='', operation_key='sum', path_context={'mode': 'single'}, input_payload={'a': 5, 'b': 3}, ui_origin='calculator_screen')
    result = execute_command(command, context)
    assert result['status'] == 'failure'
    assert result['error_type'] == 'business_precondition_failed'

def test_failure_message_is_spanish():
    context = _make_engine()
    command = make_command(actor_id='', operation_key='sum', path_context={'mode': 'single'}, input_payload={'a': 5, 'b': 3}, ui_origin='calculator_screen')
    result = execute_command(command, context)
    message = result['error_message'].lower()
    assert 'obligatorio' in message or 'jugador' in message