# Data Model: Initial Calculation Feature Set

## Entity: CalculationCommand

Represents the internal payload created from GUI interaction and submitted to calculation logic.

Fields:
- `command_id` (string): unique identifier for traceability in a session.
- `actor_id` (string): authenticated player identifier.
- `requested_operation` (string): selected calculation intent/path family.
- `context_snapshot` (object): validated operational context required for path selection.
- `input_fields` (object): required and optional values used by decision rules.
- `created_at` (datetime): local timestamp when command is formed.

Validation rules:
- `actor_id` MUST exist in player records and be active in current session.
- `requested_operation` MUST map to a defined CalculationPathRule.
- All required fields for the selected path MUST be present and valid before execution.

State transitions:
- `Draft` -> `Validated` -> `Executed` | `Rejected`

## Entity: CalculationPathRule

Defines path-specific entry conditions and expected outcomes.

Fields:
- `path_id` (string): unique path key.
- `priority` (integer): evaluation priority when more than one path could apply.
- `entry_conditions` (list): boolean conditions required for path selection.
- `output_definition` (object): expected result shape and business interpretation.
- `blocking_dependencies` (list): required dependency checks before execution.

Validation rules:
- `path_id` MUST be unique.
- `priority` MUST be unique per operation scope.
- `entry_conditions` MUST be testable and non-contradictory.

State transitions:
- `Defined` -> `Approved` -> `Deprecated`

## Entity: BusinessPrecondition

Represents a blocking rule evaluated before calculation execution.

Fields:
- `precondition_id` (string): unique rule id.
- `description` (string): business-readable rule definition.
- `priority_rank` (integer): order used to select highest-priority failure.
- `validation_expression` (string): deterministic check definition.
- `failure_message_id` (string): linked business error message.

Validation rules:
- `priority_rank` MUST be unique in the precondition set.
- Every precondition MUST map to exactly one failure message.

State transitions:
- `Configured` -> `Active` -> `Retired`

## Entity: BusinessErrorMessage

Stores localized user-facing messages for failed preconditions.

Fields:
- `message_id` (string): unique message key.
- `language` (string): message locale (`es-VE` default for GUI).
- `message_text` (string): actionable error text for user correction.
- `related_precondition_id` (string): parent precondition reference.

Validation rules:
- `message_text` MUST be clear and actionable in Spanish for GUI display.
- One-to-one relationship with `BusinessPrecondition` for blocking failures.

## Entity: DependencyStatus

Represents runtime availability checks required by calculation execution.

Fields:
- `dependency_id` (string): dependency identifier (player session, card state, file access).
- `status` (enum): `Available` | `Unavailable`.
- `checked_at` (datetime): timestamp of validation.
- `details` (string): optional operator-facing context.

Validation rules:
- Blocking dependencies marked `Unavailable` MUST prevent execution.

## Entity: ApplicationImpactRecord

Documents observable behavior changes for existing application consumers.

Fields:
- `impact_id` (string): unique change record identifier.
- `interaction_point` (string): screen or workflow point where behavior changes.
- `before_behavior` (string): previous observable behavior.
- `after_behavior` (string): new observable behavior.
- `validation_reference` (string): test/scenario that verifies expected behavior.

Validation rules:
- Every changed interaction point MUST include before/after descriptions.
- Every impact record MUST reference at least one validation scenario.

## Relationships

- `CalculationCommand` selects one `CalculationPathRule`.
- `CalculationPathRule` depends on many `BusinessPrecondition` and `DependencyStatus` checks.
- `BusinessPrecondition` maps one-to-one to `BusinessErrorMessage`.
- `ApplicationImpactRecord` links changed interaction points to validation evidence.
