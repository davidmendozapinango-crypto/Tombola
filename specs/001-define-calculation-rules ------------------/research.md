# Research: Initial Calculation Feature Set

## Decision 1: Calculation execution channel

- Decision: Execute calculations only through GUI-triggered internal commands.
- Rationale: The project is a desktop Pygame application and explicitly excludes API endpoints.
  Keeping execution internal avoids unnecessary surface area and aligns with current architecture.
- Alternatives considered:
  - Public API endpoint: rejected due to direct conflict with clarified scope.
  - Public CLI entrypoint: rejected because primary user flow is GUI-driven.

## Decision 2: Precondition failure policy

- Decision: Return only the highest-priority failed precondition message.
- Rationale: Deterministic single-error responses reduce ambiguity, simplify user correction,
  and make acceptance testing consistent.
- Alternatives considered:
  - Return all failed preconditions at once: rejected due to additional ordering complexity.
  - Generic error message only: rejected due to poor operator guidance.

## Decision 3: Input contract representation

- Decision: Define one canonical internal command schema with required fields, optional fields,
  validation rules, and per-rule failure messages.
- Rationale: A single source of truth reduces drift between UI, core logic, and tests.
- Alternatives considered:
  - Per-screen ad hoc payloads: rejected for maintainability risk.
  - Implicit field assumptions in code only: rejected due to traceability and review gaps.

## Decision 4: Internal dependency handling

- Decision: Treat player state, card state, and binary persistence availability as explicit
  pre-execution dependencies; block execution when a blocking dependency fails.
- Rationale: The constitution requires fail-safe behavior and no partial success on blocking errors.
- Alternatives considered:
  - Best-effort continuation on missing dependencies: rejected due to integrity risk.
  - Silent fallback defaults: rejected due to hidden incorrect behavior.

## Decision 5: Validation and quality evidence

- Decision: Use layered validation with unit tests (rule logic), integration tests (flow and file
  interactions), contract tests (input/error mapping), and manual GUI run checks.
- Rationale: This provides evidence for both logic correctness and user-observable behavior.
- Alternatives considered:
  - Manual testing only: rejected due to low repeatability.
  - Unit tests only: rejected due to missing end-to-end confidence.
