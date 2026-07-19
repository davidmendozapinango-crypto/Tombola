# Internal Command Contract: Calculation Execution

## Purpose

Define the internal GUI-triggered command schema used to execute calculation paths in the
desktop application.

## Trigger Source

- Source: GUI interaction only
- Public API endpoint: Not allowed
- External network invocation: Not allowed

## Command Schema

### Required fields

- `actor_id`: authenticated player identifier
- `operation_key`: selected calculation operation
- `path_context`: context object required to resolve decision path
- `input_payload`: business input values for selected path
- `ui_origin`: screen identifier that triggered command

### Optional fields

- `trace_label`: human-readable marker for debugging session runs
- `requested_at`: UI timestamp (if absent, system assigns current time)

## Validation Contract

1. Validate user/session and operation permissions.
2. Validate required fields and field-level business constraints.
3. Evaluate preconditions in configured priority order.
4. If any precondition fails, return the highest-priority failed precondition message.
5. If all checks pass, execute selected path and return result payload.

## Result Contract

### Success result

- `status`: `success`
- `path_id`: selected path identifier
- `result_payload`: output required by workflow
- `impact_marker`: reference to observable behavior impact scenario

### Failure result

- `status`: `failure`
- `error_type`: `business_precondition_failed` or `dependency_unavailable`
- `error_code`: mapped code for failed highest-priority precondition/dependency
- `error_message`: actionable Spanish message
- `retry_hint`: optional remediation hint

## Dependency Contract

Blocking dependencies checked before execution:
- Active player session
- Valid card/game context for requested operation
- Writable/readable binary persistence access where required

If a blocking dependency is unavailable, command execution is aborted and failure result is
returned with a deterministic message.

## Test Coverage Requirements

- Contract tests for required/optional field validation and result shapes.
- Rule-order tests verifying highest-priority failure selection.
- Dependency failure tests verifying blocked execution and deterministic errors.
- Integration tests validating GUI trigger -> command validation -> path outcome.
