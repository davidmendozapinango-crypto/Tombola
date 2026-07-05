<!--
Sync Impact Report
- Version change: template -> 1.0.0
- Modified principles:
  - PRINCIPLE_1_NAME -> I. Security by Design
  - PRINCIPLE_2_NAME -> II. Modular Maintainability
  - PRINCIPLE_3_NAME -> III. Test-Backed Quality Gates
  - PRINCIPLE_4_NAME -> IV. Data Integrity and Traceability
  - PRINCIPLE_5_NAME -> V. UX Accessibility and Educational Fidelity
- Added sections:
  - Technical Standards and Constraints
  - Delivery Workflow and Review Gates
- Removed sections: none
- Templates requiring updates:
  - .specify/templates/plan-template.md: ✅ updated
  - .specify/templates/spec-template.md: ✅ updated
  - .specify/templates/tasks-template.md: ✅ updated
  - .specify/templates/commands/*.md: ⚠ pending (no command templates found)
  - README.md: ✅ updated
  - docs/07 Implementation Plan.md: ✅ updated
- Deferred follow-ups: none
-->

# Tombola Game Constitution

## Core Principles

### I. Security by Design
All player authentication and persistence flows MUST be designed to fail safely.
Access keys MUST be validated with the required recursive algorithm before storage,
credentials MUST never be logged in plain text, and binary file writes MUST use append-safe
flows that prevent silent overwrite. Any feature that reads or writes `JUGADORES.bin` or
`JUEGOS.bin` MUST define input validation and explicit error-handling behavior.
Rationale: the project handles identity and gameplay history records, so predictable and
auditable security controls are mandatory.

### II. Modular Maintainability
Code MUST be organized into focused modules with clear function-level boundaries for
authentication, gameplay, persistence, reporting, and UI rendering. Each module MUST expose a
small public surface, avoid duplicated business logic, and include concise documentation for
inputs, outputs, and side effects. Shared constants (for example, SDG metadata and UI labels)
MUST be centralized to prevent drift.
Rationale: modular decomposition is a graded academic requirement and is essential for team
delivery velocity.

### III. Test-Backed Quality Gates
Every change to core logic MUST include automated tests or documented deterministic run checks
that prove correctness. At minimum, the team MUST verify recursive key validation, random
draw uniqueness, winner detection, and binary read/write integrity before merge. A task is not
complete until corresponding verification evidence is captured in the plan, tasks, or PR notes.
Rationale: code quality is measured by repeatable correctness, not by implementation effort.

### IV. Data Integrity and Traceability
Persistence formats for player and game records MUST be versioned and documented before any
format change is implemented. Serialization and deserialization MUST be implemented in dedicated
functions and validated against malformed or partial records. Reports MUST be derived from stored
source data, not manually edited aggregates.
Rationale: the project depends on reproducible game history and ranking outputs.

### V. UX Accessibility and Educational Fidelity
All user-facing interface text in the graphical experience MUST be in Spanish, and error
messages MUST be actionable and understandable for non-technical users. The UI MUST preserve
educational SDG context during onboarding, gameplay, and results through consistent visual and
message integration. Keyboard interaction and visible focus states SHOULD be implemented for
core screens to improve accessibility.
Rationale: the project has explicit educational and language requirements, not only gameplay
requirements.

## Technical Standards and Constraints

- The implementation stack MUST remain Python with Pygame for UI and binary files for required
  persistence artifacts.
- Card dimensions MUST support odd values from 5 to 15 inclusive, with deterministic validation
  and user feedback for invalid inputs.
- Gameplay draws MUST be non-repeating within a game session and bounded to the active card range
  `1..N*N`.
- Core persistence files MUST be treated as authoritative records; backup and corruption-recovery
  procedures MUST be documented in project docs before release.

## Delivery Workflow and Review Gates

- Work MUST be planned against documented phases and tracked by module ownership.
- Each feature spec MUST include explicit security, maintainability, and quality requirements.
- Implementation plans MUST pass a constitution check before coding and again before final review.
- Task lists MUST include verification tasks for testing, data integrity checks, and documentation
  updates.
- Reviewers MUST reject changes that do not provide evidence for affected constitution principles.

## Governance

This constitution overrides conflicting informal practices for planning, implementation, and
review in this repository.

Amendment process:
- Any amendment MUST include: proposed change, impacted principles or sections, migration impact,
  and updates to dependent templates/docs.
- Amendments require approval by project maintainers and must be recorded in this file.

Versioning policy:
- MAJOR version increments for removed or redefined principles that change compliance expectations.
- MINOR version increments for new principles, new mandatory sections, or materially expanded
  governance requirements.
- PATCH version increments for clarifications, wording improvements, and non-semantic edits.

Compliance review expectations:
- Every implementation plan and review MUST include a constitution compliance check.
- Non-compliant items MUST be resolved before merge or explicitly documented in a temporary
  exception record with owner and expiration date.
- This constitution MUST be reviewed for relevance whenever project scope or required stack changes.

**Version**: 1.0.0 | **Ratified**: 2026-07-04 | **Last Amended**: 2026-07-04
