import time
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

def test_calculation_performance_within_target():
    engine_context = _make_engine()
    command = make_command(actor_id='player-001', operation_key='sum', path_context={'mode': 'single'}, input_payload={'a': 5, 'b': 10}, ui_origin='calculator_screen')
    start = time.perf_counter()
    result = execute_command(command, engine_context)
    elapsed_ms = (time.perf_counter() - start) * 1000
    assert result['status'] == 'success'
    assert elapsed_ms <= 500, f'Execution took {elapsed_ms:.2f} ms, exceeding 500 ms target'