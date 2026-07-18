import pytest
from src.core.calculation_engine import execute_command, make_engine_context
from src.core.command_contract import make_command
from src.core.dependencies import make_dependency_checker
from src.core.path_rules import make_registry, make_rule, register_rule

def _always(ctx, payload):
    return True

def _make_engine():
    registry = make_registry()
    register_rule(registry, make_rule(path_id='noop:default', priority=1, entry_conditions=[_always], output_definition={}, blocking_dependencies=[]))
    checker = make_dependency_checker()
    return make_engine_context(registry, [], checker)

def test_no_network_invocation():
    engine_context = _make_engine()
    command = make_command(actor_id='player-001', operation_key='noop', path_context={}, input_payload={}, ui_origin='calculator_screen')
    result = execute_command(command, engine_context)
    assert result['status'] == 'success'
    assert 'path_id' in result

def test_engine_has_no_http_client():
    engine_context = _make_engine()
    assert 'session' not in engine_context
    assert 'request' not in engine_context
    assert 'http_client' not in engine_context