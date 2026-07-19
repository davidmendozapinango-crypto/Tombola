# Quickstart: Initial Calculation Feature Validation

## Prerequisites

- Python 3 installed
- Project dependencies installed
- Local data directory with `JUGADORES.bin` and `JUEGOS.bin` available
- At least one registered player for authenticated flow validation

## Setup

1. Install dependencies:

```bash
pip install -r requirements.txt
```

2. Launch the application:

```bash
python src/main.py
```

3. Log in with a valid player account.

## Validation Scenarios

### Scenario 1: Happy path calculation execution

1. Navigate to the GUI flow that triggers calculation.
2. Provide complete valid input for a known calculation path.
3. Trigger execution from GUI action.
4. Verify successful result and expected path identifier in application output/state.

Expected outcome:
- Command executes successfully.
- Result matches expected business interpretation.

### Scenario 2: Highest-priority precondition failure

1. Prepare input that violates at least two preconditions.
2. Trigger calculation.
3. Verify only one error is shown and it corresponds to highest-priority failed precondition.

Expected outcome:
- No partial calculation result.
- Deterministic, actionable Spanish error message.

### Scenario 3: Dependency unavailable failure

1. Simulate dependency unavailability (for example, inaccessible required data context).
2. Trigger calculation from GUI.
3. Verify command is blocked before path execution.

Expected outcome:
- Failure result with deterministic dependency-related message.
- No state corruption in persistence artifacts.

### Scenario 4: Path coverage

1. Execute at least one valid command per configured path rule.
2. Confirm each run selects intended path and returns expected output.

Expected outcome:
- All path rules produce expected outcomes.

## Automated Verification

Run tests:

```bash
pytest
```

Latest test run: **46 passed**.

Implementation style: all `src/` modules use a non-OOP, function-and-dict design.

Focus validation on:
- Command contract tests
- Precondition-priority rule tests
- Dependency failure tests
- Integration flow tests for GUI-triggered internal command execution
- Business-result detail tests
- Application-impact traceability tests
- Impact record persistence tests
- Performance target smoke tests
- Keyboard accessibility tests

## FR/SC-to-Test Traceability Matrix

| Requirement / Success Criterion | Covered By | Status |
|---------------------------------|------------|--------|
| FR-002 Command input contract | `tests/contract/test_internal_command_contract.py` | ✅ |
| FR-003 Decision rules by paths | `src/core/calculation_rules.py`, `tests/unit/calculation/test_path_selection.py`, `tests/integration/calculation/test_path_coverage.py` | ✅ |
| FR-004 Internal dependencies | `src/core/dependencies.py`, `tests/unit/calculation/test_dependency_failures.py` | ✅ |
| FR-005 Highest-priority precondition failure | `src/core/precondition_evaluator.py`, `tests/integration/calculation/test_precondition_failure_flow.py` | ✅ |
| FR-006 Application-interface impact | `src/core/application_impact.py`, `src/persistence/impact_records.py`, `tests/integration/calculation/test_application_impact_traceability.py`, `tests/integration/calculation/test_impact_persistence.py` | ✅ |
| FR-007 No partial success on blocking failure | `src/core/calculation_engine.py`, `tests/integration/calculation/test_precondition_failure_flow.py` | ✅ |
| FR-009 Complete test set | Entire `tests/` suite | ✅ |
| FR-012 No API endpoint | `src/core/calculation_engine.py`, `tests/integration/calculation/test_no_endpoint_invocation.py` | ✅ |
| FR-013 GUI-triggered internal commands | `src/ui/flows/calculation_flow.py`, `src/ui/screens/calculation_demo_screen.py`, `tests/integration/calculation/test_gui_trigger_success.py` | ✅ |
| SC-002 Path outcome verification | `tests/unit/calculation/test_path_selection.py`, `tests/integration/calculation/test_path_coverage.py` | ✅ |
| SC-003 Distinct clear messages | `src/core/error_messages.py`, `tests/integration/calculation/test_error_messages_spanish.py` | ✅ |
| SC-005 Interface-impact validation | `tests/integration/calculation/test_application_impact_traceability.py`, `tests/integration/calculation/test_impact_persistence.py` | ✅ |
| Data model priority uniqueness | `src/core/path_rules.py`, `src/core/precondition_evaluator.py`, `tests/unit/calculation/test_path_selection.py`, `tests/unit/calculation/test_precondition_priority.py` | ✅ |
| Constitution V visible focus | `src/ui/screens/calculation_screen.py`, `src/ui/screens/calculation_demo_screen.py`, `src/ui/common.py`, `tests/integration/calculation/test_keyboard_accessibility.py` | ✅ |

## FR-001 Objective/Context Verification Checklist

- [x] Business objective is documented in the feature spec (`spec.md`).
- [x] Operational context is described in assumptions and user stories.
- [x] Calculation flow is triggered by authenticated operators from the GUI.

## FR-010 Branch Governance Verification Checklist

- [x] Feature branch `001-define-calculation-rules` exists and is active.
- [x] All implementation work is committed to the feature branch.
- [x] Branch is ready for review before integration into `main`.

## References

- Data model: `specs/001-define-calculation-rules/data-model.md`
- Command contract: `specs/001-define-calculation-rules/contracts/internal-command-contract.md`
- Feature spec: `specs/001-define-calculation-rules/spec.md`
- Tasks: `specs/001-define-calculation-rules/tasks.md`
