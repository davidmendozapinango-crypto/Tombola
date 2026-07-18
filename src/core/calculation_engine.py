"""Calculation orchestrator with deterministic failure handling (non-OOP)."""
from typing import Any, Dict, List, Optional
from src.core.application_impact import add_impact_record, make_impact_record, make_impact_store
from src.core.calculation_rules import compute_result
from src.core.command_contract import validate_required_fields
from src.core.dependencies import check_dependency
from src.core.error_messages import MESSAGES, build_error_response
from src.core.path_rules import select_rule
from src.core.precondition_evaluator import evaluate_preconditions
from src.persistence.impact_records import save_impact_records

def make_engine_context(registry: Dict[str, Any], preconditions: List[Dict[str, Any]], dependency_checker: Dict[str, Any], error_catalog: Optional[Dict[str, Dict[str, str]]]=None, impact_store: Optional[List[Dict[str, Any]]]=None, impact_persistence: Optional[Dict[str, Any]]=None) -> Dict[str, Any]:
    """Create an engine context dictionary holding all collaborators."""
    return {'registry': registry, 'preconditions': preconditions, 'dependency_checker': dependency_checker, 'error_catalog': error_catalog or MESSAGES, 'impact_store': impact_store if impact_store is not None else make_impact_store(), 'impact_persistence': impact_persistence}

def execute_command(command: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
    """Execute a GUI-triggered internal calculation command."""
    error_catalog = context['error_catalog']
    if not command.get('ui_origin'):
        _record_impact(command, None, False, context)
        return build_error_response('business_precondition_failed', 'missing_ui_origin', error_catalog)
    missing = validate_required_fields(command)
    if missing:
        _record_impact(command, None, False, context)
        return build_error_response('business_precondition_failed', f'missing_{missing[0]}', error_catalog)
    rule = select_rule(context['registry'], command['operation_key'], command['path_context'], command['input_payload'])
    if rule is None:
        _record_impact(command, None, False, context)
        return build_error_response('business_precondition_failed', 'invalid_path_state', error_catalog)
    for dep_id in rule['blocking_dependencies']:
        status = check_dependency(context['dependency_checker'], dep_id)
        if status['status'] == 'Unavailable':
            _record_impact(command, rule, False, context)
            return build_error_response('dependency_unavailable', 'dependency_unavailable', error_catalog)
    payload = {'command': command, 'path_context': command['path_context'], 'input_payload': command['input_payload']}
    (passed, failure) = evaluate_preconditions(context['preconditions'], payload)
    if not passed and failure is not None:
        _record_impact(command, rule, False, context, failure=failure)
        return build_error_response('business_precondition_failed', failure['failure_message_id'], error_catalog)
    result_payload = compute_result(rule, command['input_payload'])
    _record_impact(command, rule, True, context)
    return {'status': 'success', 'path_id': rule['path_id'], 'result_payload': result_payload, 'impact_marker': rule['output_definition'].get('impact_marker')}

def _record_impact(command: Dict[str, Any], rule: Optional[Dict[str, Any]], success: bool, context: Dict[str, Any], failure: Optional[Dict[str, Any]]=None) -> None:
    """Record observable application impact for auditability."""
    impact_id = f"IMP-{command['command_id']}"
    interaction_point = command.get('ui_origin') or 'unknown'
    if success:
        before_behavior = 'No calculation result available'
        after_behavior = f"Calculation succeeded via {(rule['path_id'] if rule else 'unknown')}"
    else:
        before_behavior = 'No calculation error recorded'
        after_behavior = f"Calculation rejected: {(failure['precondition_id'] if failure else 'precondition_failed')}"
    validation_reference = f"command:{command['command_id']}"
    record = make_impact_record(impact_id=impact_id, interaction_point=interaction_point, before_behavior=before_behavior, after_behavior=after_behavior, validation_reference=validation_reference)
    add_impact_record(context['impact_store'], record)
    persistence = context.get('impact_persistence')
    if persistence is not None:
        save_impact_records(persistence, [record])