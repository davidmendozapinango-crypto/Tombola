import pytest
from src.core.application_impact import list_impact_records
from src.core.calculation_engine import execute_command, make_engine_context
from src.core.calculation_rules import build_default_registry
from src.core.command_contract import make_command
from src.core.dependencies import make_dependency_checker, register_dependency
from src.core.preconditions import make_precondition

def _make_engine():
    registry = build_default_registry(dependencies=['player_session'])
    checker = make_dependency_checker()
    register_dependency(checker, 'player_session', lambda : True)
    preconditions = [make_precondition(precondition_id='actor_present', description='Actor present', priority_rank=1, check=lambda p: bool(p['command']['actor_id']), failure_message_id='missing_actor_id')]
    return make_engine_context(registry, preconditions, checker)

def test_success_creates_impact_record():
    engine_context = _make_engine()
    command = make_command(actor_id='player-001', operation_key='sum', path_context={'mode': 'single'}, input_payload={'a': 2, 'b': 3}, ui_origin='calculator_screen')
    result = execute_command(command, engine_context)
    assert result['status'] == 'success'
    records = list_impact_records(engine_context['impact_store'])
    assert len(records) == 1
    assert records[0]['interaction_point'] == 'calculator_screen'
    assert 'sum:single' in records[0]['after_behavior']

def test_failure_creates_impact_record():
    engine_context = _make_engine()
    command = make_command(actor_id='', operation_key='sum', path_context={'mode': 'single'}, input_payload={'a': 2, 'b': 3}, ui_origin='calculator_screen')
    result = execute_command(command, engine_context)
    assert result['status'] == 'failure'
    records = list_impact_records(engine_context['impact_store'])
    assert len(records) == 1
    assert 'rejected' in records[0]['after_behavior'].lower()