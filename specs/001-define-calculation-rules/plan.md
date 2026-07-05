# Implementation Plan: Initial Calculation Feature Set

**Branch**: `001-define-calculation-rules` | **Date**: 2026-07-04 | **Spec**: `specs/001-define-calculation-rules/spec.md`

**Input**: Feature specification from `specs/001-define-calculation-rules/spec.md`

## Summary

Implement a GUI-triggered internal calculation command flow for the Tombola desktop app that
defines command input contracts, deterministic decision paths, precondition-priority error handling,
dependency handling, and measurable validation outcomes without introducing API endpoints.

## Technical Context

**Language/Version**: Python 3.x

**Primary Dependencies**: Pygame (desktop GUI), Python standard library modules for binary I/O

**Storage**: Binary files (`JUGADORES.bin`, `JUEGOS.bin`) with append-safe writes

**Testing**: pytest for automated logic validation plus deterministic manual GUI validation scenarios

**Target Platform**: Desktop environments used in coursework labs (Windows-first)

**Project Type**: Desktop application (GUI-triggered internal command flow, no API endpoint)

**Performance Goals**: Maintain smooth 60 FPS GUI loop; 95% of GUI-triggered calculation
validation/execution cycles complete in <= 500 ms and 100% complete in <= 1.5 s on baseline lab
hardware

**Constraints**: Spanish-first UI messaging, odd card sizes 5..15, recursive security validation,
no API endpoint introduction, fail-safe binary write behavior

**Scale/Scope**: Single application instance per user session, classroom-scale data and gameplay
history persisted in local binary files

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

- **Security by Design**: Identify authentication, validation, and file-write risks; define
  fail-safe behavior and logging limits (no plain-text credentials).
- **Modular Maintainability**: Map module boundaries (auth, gameplay, persistence, reporting, UI)
  and list any shared constants/data contracts.
- **Test-Backed Quality Gates**: Define automated tests or deterministic run checks for all core
  logic impacted by this feature.
- **Data Integrity and Traceability**: Document binary schema impacts, serialization strategy, and
  corruption/partial-read handling.
- **UX Accessibility and Educational Fidelity**: Confirm Spanish UI content, actionable errors, and
  SDG educational context on affected screens.

**Initial Gate Assessment**: PASS

- Security by design is enforced via precondition checks, deterministic highest-priority errors,
  and no plaintext credential exposure in messages.
- Modularity is preserved by separating input contract, decision rules, dependency validation,
  and error mapping.
- Test-backed quality is scoped with happy path, path coverage, failure coverage, and integration
  behavior validation.
- Data integrity constraints align with binary append-safe and reconstructible records.
- UX requirements enforce actionable Spanish messages and GUI-triggered interaction.

## Project Structure

### Documentation (this feature)

```text
specs/001-define-calculation-rules/
├── plan.md              # This file (/speckit.plan command output)
├── research.md          # Phase 0 output (/speckit.plan command)
├── data-model.md        # Phase 1 output (/speckit.plan command)
├── quickstart.md        # Phase 1 output (/speckit.plan command)
├── contracts/           # Phase 1 output (/speckit.plan command)
└── tasks.md             # Phase 2 output (/speckit.tasks command - NOT created by /speckit.plan)
```

### Source Code (repository root)

```text
src/
├── auth/
├── core/
├── persistence/
├── reports/
├── ui/
└── ods/

assets/
├── images/
├── fonts/
└── sounds/

data/
├── JUGADORES.bin
└── JUEGOS.bin

tests/
├── unit/
├── integration/
└── contract/
```

**Structure Decision**: Single desktop application structure aligned with existing Tombola
module boundaries; no backend/api split will be introduced for this feature.

## Complexity Tracking

No constitution violations identified that require justification.

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| None | N/A | N/A |

## Phase 0: Research Output

Research decisions are documented in `specs/001-define-calculation-rules/research.md`.
All prior clarification gaps from planning context were resolved without introducing API scope.

## Phase 1: Design Output

- Data model: `specs/001-define-calculation-rules/data-model.md`
- Contracts: `specs/001-define-calculation-rules/contracts/internal-command-contract.md`
- Validation guide: `specs/001-define-calculation-rules/quickstart.md`

## Post-Design Constitution Re-check

**Post-Design Gate Assessment**: PASS

- Security rules are directly reflected in command validation and deterministic failure handling.
- Modular boundaries are captured in design artifacts with clear ownership by concern.
- Test requirements are explicit in contract and quickstart validation scenarios.
- Data traceability is maintained through explicit records and dependency impact definitions.
- Spanish-first GUI behavior is preserved and no API surface was added.
