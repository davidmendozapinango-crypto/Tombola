import pytest

from src.core.calculation_engine import execute_command, make_engine_context
from src.core.calculation_rules import build_default_registry
from src.core.command_contract import make_command, validate_required_fields
from src.core.command_normalizer import normalize_command_payload
from src.core.dependencies import make_dependency_checker, register_dependency
from src.core.preconditions import make_precondition


def _sum_entry(ctx, payload):
    return ctx.get('mode') == 'single' and 'a' in payload and ('b' in payload)

def _make_engine():
    registry = build_default_registry(dependencies=['player_session'])
    checker = make_dependency_checker()
    register_dependency(checker, 'player_session', lambda : True)
    preconditions = [make_precondition(precondition_id='actor_present', description='Actor must be present', priority_rank=1, check=lambda p: bool(p['command']['actor_id']), failure_message_id='missing_actor_id')]
    return make_engine_context(registry, preconditions, checker)

def test_success_result_shape():
    context = _make_engine()
    command = make_command(actor_id='player-001', operation_key='sum', path_context={'mode': 'single'}, input_payload={'a': 5, 'b': 3}, ui_origin='calculator_screen')
    result = execute_command(command, context)
    assert result['status'] == 'success'
    assert result['path_id'] == 'sum:single'
    assert 'result_payload' in result
    assert result['impact_marker'] == 'sum_single'

def test_failure_result_shape():
    context = _make_engine()
    command = make_command(actor_id='', operation_key='sum', path_context={'mode': 'single'}, input_payload={'a': 5, 'b': 3}, ui_origin='calculator_screen')
    result = execute_command(command, context)
    assert result['status'] == 'failure'
    assert result['error_type'] == 'business_precondition_failed'
    assert 'error_code' in result
    assert 'error_message' in result
    assert 'retry_hint' in result

def test_required_fields_in_contract():
    payload = {'actor_id': 'player-001', 'operation_key': 'sum', 'path_context': {'mode': 'single'}, 'input_payload': {'a': 1, 'b': 2}, 'ui_origin': 'screen'}
    command = normalize_command_payload(payload)
    missing = validate_required_fields(command)
    assert missing == []

def test_missing_required_fields_in_contract():
    payload = {'actor_id': '', 'operation_key': '', 'path_context': {}, 'input_payload': {}, 'ui_origin': ''}
    command = normalize_command_payload(payload)
    missing = validate_required_fields(command)
    assert 'actor_id' in missing
    assert 'operation_key' in missing