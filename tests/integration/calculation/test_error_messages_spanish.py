import pytest
from src.core.calculation_engine import execute_command, make_engine_context
from src.core.calculation_rules import build_default_registry
from src.core.command_contract import make_command
from src.core.dependencies import make_dependency_checker
from src.core.preconditions import make_precondition

def _always(ctx, payload):
    return True

def _make_engine():
    registry = build_default_registry()
    checker = make_dependency_checker()
    preconditions = [make_precondition(precondition_id='actor_present', description='Actor present', priority_rank=1, check=lambda p: bool(p['command']['actor_id']), failure_message_id='missing_actor_id')]
    return make_engine_context(registry, preconditions, checker)

def test_error_message_is_spanish():
    engine_context = _make_engine()
    command = make_command(actor_id='', operation_key='sum', path_context={}, input_payload={}, ui_origin='calculator_screen')
    result = execute_command(command, engine_context)
    assert result['status'] == 'failure'
    message = result['error_message']
    assert any((word in message.lower() for word in ['obligatorio', 'jugador', 'sesión', 'identificador']))