# Tasks: Initial Calculation Feature Set

**Input**: Design documents from `specs/001-define-calculation-rules/`

**Prerequisites**: plan.md (required), spec.md (required for user stories), research.md, data-model.md, contracts/

**Tests**: Tests are REQUIRED for this feature because core validation, decision logic, dependency handling, and interface behavior change.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and test scaffolding for the calculation feature.

- [x] T001 Create feature module directories in `src/core/`, `src/ui/`, and `tests/`
- [x] T002 Add package markers in `src/core/__init__.py` and `src/ui/__init__.py`
- [x] T003 [P] Create calculation test folders in `tests/unit/calculation/`, `tests/integration/calculation/`, and `tests/contract/`
- [x] T004 [P] Add test data fixtures for calculation scenarios in `tests/fixtures/calculation_commands.json`

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core components required by all user stories.

**⚠️ CRITICAL**: No user story work can begin until this phase is complete.

- [x] T005 Implement internal command schema model in `src/core/command_contract.py`
- [x] T006 Implement path rule registry and selectors in `src/core/path_rules.py`
- [x] T007 Implement precondition definitions and priority ordering in `src/core/preconditions.py`
- [x] T008 Implement dependency status checker in `src/core/dependencies.py`
- [x] T009 Implement localized business error catalog in `src/core/error_messages.py`
- [x] T010 Implement calculation orchestrator shell in `src/core/calculation_engine.py`
- [x] T011 [P] Add shared binary safety helpers in `src/persistence/io_safety.py`
- [x] T012 [P] Add foundational unit tests for schema and rule loading in `tests/unit/calculation/test_contract_and_rules_bootstrap.py`

**Checkpoint**: Foundation ready - user story implementation can now begin.

---

## Phase 3: User Story 1 - Define and execute a valid calculation command (Priority: P1) 🎯 MVP

**Goal**: Enable successful GUI-triggered command validation and execution for valid inputs.

**Independent Test**: From the calculation GUI flow, submit a valid command and verify selected path plus successful output.

### Tests for User Story 1

- [x] T013 [P] [US1] Create contract success-shape tests in `tests/contract/test_internal_command_contract.py`
- [x] T014 [P] [US1] Create unit tests for path selection outcomes in `tests/unit/calculation/test_path_selection.py`
- [x] T015 [US1] Create integration test for GUI trigger to successful execution in `tests/integration/calculation/test_gui_trigger_success.py`

### Implementation for User Story 1

- [x] T016 [P] [US1] Implement command payload normalizer in `src/core/command_normalizer.py`
- [x] T017 [US1] Implement valid-command execution flow in `src/core/calculation_engine.py`
- [x] T018 [US1] Implement GUI trigger adapter in `src/ui/flows/calculation_flow.py`
- [x] T019 [US1] Implement calculation state updates for success in `src/ui/state/calculation_state.py`
- [x] T020 [US1] Wire calculation action on screen controls in `src/ui/screens/calculation_screen.py`

**Checkpoint**: User Story 1 is fully functional and independently testable.

---

## Phase 4: User Story 2 - Receive explicit business-precondition failures (Priority: P1)

**Goal**: Return deterministic, highest-priority, actionable Spanish errors for failed preconditions.

**Independent Test**: Submit invalid commands with multiple failed preconditions and verify only highest-priority mapped message is shown.

### Tests for User Story 2

- [x] T021 [P] [US2] Create contract failure-shape tests in `tests/contract/test_internal_command_failures.py`
- [x] T022 [P] [US2] Create unit tests for highest-priority precondition selection in `tests/unit/calculation/test_precondition_priority.py`
- [x] T023 [US2] Create integration test for multi-failure single-message behavior in `tests/integration/calculation/test_precondition_failure_flow.py`

### Implementation for User Story 2

- [x] T024 [US2] Implement precondition evaluator with rank ordering in `src/core/precondition_evaluator.py`
- [x] T025 [US2] Implement failure mapping to Spanish actionable messages in `src/core/error_messages.py`
- [x] T026 [US2] Integrate failure short-circuit behavior in `src/core/calculation_engine.py`
- [x] T027 [US2] Implement GUI error presentation state in `src/ui/state/calculation_state.py`
- [x] T028 [US2] Render business error messages in `src/ui/screens/calculation_screen.py`

**Checkpoint**: User Stories 1 and 2 work independently with deterministic failure behavior.

---

## Phase 5: User Story 3 - Validate decision paths and application impact (Priority: P2)

**Goal**: Validate all calculation paths and document/verify observable application-impact changes.

**Independent Test**: Execute one valid scenario per path and verify impact record evidence for changed interaction points.

### Tests for User Story 3

- [x] T029 [P] [US3] Create contract tests for impact marker behavior in `tests/contract/test_application_impact_contract.py`
- [x] T030 [P] [US3] Create unit tests for dependency unavailable outcomes in `tests/unit/calculation/test_dependency_failures.py`
- [x] T031 [US3] Create integration tests for full path coverage in `tests/integration/calculation/test_path_coverage.py`

### Implementation for User Story 3

- [x] T032 [US3] Implement application impact record model and writer in `src/core/application_impact.py`
- [x] T033 [US3] Persist impact records for changed behaviors in `src/persistence/impact_records.py`
- [x] T034 [US3] Add dependency-unavailable branch handling in `src/core/calculation_engine.py`
- [x] T035 [US3] Add GUI indicators for impact-validated outcomes in `src/ui/screens/calculation_screen.py`
- [x] T036 [US3] Add negative test ensuring no API/network endpoint invocation in `tests/integration/calculation/test_no_endpoint_invocation.py`
- [x] T037 [US3] Enforce internal-only trigger guard in `src/core/calculation_engine.py`

**Checkpoint**: All user stories are independently functional and validated.

---

## Phase 6: Polish & Cross-Cutting Concerns

**Purpose**: Final hardening, documentation, and end-to-end validation.

- [x] T038 [P] Update feature documentation references in `specs/001-define-calculation-rules/quickstart.md`
- [x] T039 Run full automated test suite via `pytest` and capture results in `specs/001-define-calculation-rules/quickstart.md`
- [x] T040 Validate binary integrity and corruption handling paths in `tests/integration/calculation/test_binary_integrity_guards.py`
- [x] T041 Confirm all new user-facing messages are Spanish and actionable in `src/core/error_messages.py`
- [x] T042 [P] Refactor duplicated calculation helpers in `src/core/`
- [x] T043 Define FR/SC-to-test traceability matrix in `specs/001-define-calculation-rules/quickstart.md`
- [x] T044 [P] Add acceptance-evidence checklist for FR-008 in `tests/integration/calculation/test_acceptance_traceability.py`
- [x] T045 Add FR-001 objective/context verification checklist in `specs/001-define-calculation-rules/quickstart.md`
- [x] T046 Add branch governance verification for FR-010 in `specs/001-define-calculation-rules/quickstart.md`

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately.
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories.
- **User Stories (Phase 3+)**: Depend on Foundational completion.
  - US1 (P1) should be completed first for MVP baseline.
  - US2 (P1) depends on shared engine from US1 but remains independently testable.
  - US3 (P2) depends on path and failure flow being in place.
- **Polish (Phase 6)**: Depends on all targeted stories being complete.

### User Story Dependencies

- **US1**: Starts after Phase 2; no dependency on other user stories.
- **US2**: Starts after Phase 2 and integrates with calculation engine introduced in US1.
- **US3**: Starts after Phase 2; uses core modules from US1/US2 for path and impact validation.

### Parallel Opportunities

- Setup tasks marked `[P]` can run in parallel.
- Foundational tasks T011 and T012 can run alongside T005-T010 after directories exist.
- In each story, contract and unit tests marked `[P]` can run in parallel.
- UI updates and persistence updates in US3 can proceed in parallel after core impact model exists.

---

## Parallel Example: User Story 1

```bash
# Parallel tests
Task: "T013 [US1] Contract success-shape tests in tests/contract/test_internal_command_contract.py"
Task: "T014 [US1] Unit path selection tests in tests/unit/calculation/test_path_selection.py"

# Parallel implementation
Task: "T016 [US1] Command payload normalizer in src/core/command_normalizer.py"
Task: "T020 [US1] Screen control wiring in src/ui/screens/calculation_screen.py"
```

## Parallel Example: User Story 2

```bash
# Parallel tests
Task: "T021 [US2] Contract failure-shape tests in tests/contract/test_internal_command_failures.py"
Task: "T022 [US2] Priority selection tests in tests/unit/calculation/test_precondition_priority.py"

# Parallel implementation after evaluator exists
Task: "T027 [US2] GUI error state in src/ui/state/calculation_state.py"
Task: "T028 [US2] Error rendering in src/ui/screens/calculation_screen.py"
```

## Parallel Example: User Story 3

```bash
# Parallel tests
Task: "T029 [US3] Impact marker contract tests in tests/contract/test_application_impact_contract.py"
Task: "T030 [US3] Dependency failure unit tests in tests/unit/calculation/test_dependency_failures.py"

# Parallel implementation after impact model exists
Task: "T033 [US3] Impact persistence in src/persistence/impact_records.py"
Task: "T035 [US3] GUI impact indicators in src/ui/screens/calculation_screen.py"
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1 and Phase 2.
2. Complete Phase 3 (US1).
3. Validate happy-path execution via T013-T015.
4. Demo GUI-triggered successful calculation flow.

### Incremental Delivery

1. Deliver US1 for baseline successful command execution.
2. Deliver US2 for deterministic error handling and fail-safe behavior.
3. Deliver US3 for path coverage and application-impact validation.
4. Finish with Phase 6 hardening and regression checks.

### Parallel Team Strategy

1. Developer A: Core engine and precondition flow (`src/core/`).
2. Developer B: GUI flow/state (`src/ui/`).
3. Developer C: Tests and persistence/impact records (`tests/`, `src/persistence/`).

---

## Phase 7: Convergence

**Purpose**: Close remaining gaps between the feature spec/plan and the current implementation.

- [x] T047 Define concrete calculation path rules and real result computation per FR-003 (partial)
- [x] T048 Add integration test verifying business-meaningful result detail per SC-002 / US1/AC2 (missing)
- [x] T049 Create and link ApplicationImpactRecord instances to calculation outcomes per FR-006 / SC-005 (partial)
- [x] T050 Add performance smoke test for <= 500 ms / <= 1.5 s targets per plan Performance Goals (partial)
- [x] T051 Append FR/SC-to-test traceability matrix and FR-001/FR-010 checklists to quickstart.md per plan (missing)
- [x] T052 Add keyboard navigation and visible focus handling to CalculationScreen per Constitution V (partial)

---

## Phase 8: Convergence - Remove OOP from Implementation

**Purpose**: Refactor all implementation modules to use a non-OOP, function-and-dict style per project direction.

- [x] T053 Rewrite all `src/core/` modules to remove classes/dataclasses and use functions with plain dicts per FR-002/FR-003 (contradicts)
- [x] T054 Rewrite all `src/ui/` modules to remove classes and use module-level state/functions per FR-013 (contradicts)
- [x] T055 Rewrite all `src/persistence/` modules to remove classes and use functions per Constitution IV (contradicts)
- [x] T056 Update all `tests/` to use the new functional APIs and keep full coverage per FR-009 (contradicts)
- [x] T057 Run `pytest` and verify all tests pass after OOP removal per Constitution III (contradicts)

---

## Phase 9: Convergence

**Purpose**: Close remaining gaps identified between the feature spec/plan and the current implementation.

- [x] T058 CRITICAL: Fix impact record append serialization bug and add load validation per Constitution IV (contradicts)
- [x] T059 Wire impact record persistence into calculation flow and engine per T033 / FR-006 / SC-005 (missing)
- [x] T060 Implement Tombola-domain calculation paths with card/game/SDG context per FR-001 / FR-003 / US3/AC1 (partial)
- [x] T061 Integrate `calculation_screen` focus helpers with Pygame event flow per T052 / Constitution V (partial)
- [x] T062 Enforce precondition `priority_rank` uniqueness in precondition evaluator per data-model (partial)
- [x] T063 Enforce path rule priority uniqueness per operation scope in path registry per data-model (partial)
