# Constitution Compliance Evidence

This document maps each delivered module to the principles defined in the project constitution (`.specify/memory/constitution.md`) and provides the evidence that demonstrates compliance.

## Constitution Principles Summary

- **I. Security by Design**: fail-safe auth, recursive key validation, no plain-text credential logging, append-safe binary writes.
- **II. Modular Maintainability**: focused modules, small public surface, centralized constants, no duplicated business logic.
- **III. Test-Backed Quality Gates**: automated tests for recursive validation, random draws, winner detection, binary integrity.
- **IV. Data Integrity and Traceability**: versioned/documented persistence formats, dedicated serialization functions, reports derived from source data.
- **V. UX Accessibility and Educational Fidelity**: Spanish UI text, actionable errors, SDG context, keyboard focus/visible states.

---

## 1. Authentication Module (`src/auth/`)

### Files
- `src/auth/validator.py`
- `src/auth/session.py`

### Compliance
| Principle | Evidence |
|-----------|----------|
| I. Security by Design | `validate_registration_data` enforces key length, character classes, and recursive `_no_long_run` / `_has_type` checks. Plain-text credentials are never logged. |
| II. Modular Maintainability | Auth rules are isolated from UI and persistence; public surface is `validate_registration_data`, `check_password_criteria`, `login`, `logout`. |
| III. Test-Backed Quality Gates | `tests/test_auth.py` covers valid/invalid keys, recursive long-run detection, and duplicate ID rejection. |
| V. UX Accessibility and Educational Fidelity | `check_password_criteria` returns per-criterion feedback rendered live on `register_screen.py`. All error messages are in Spanish. |

---

## 2. Core Gameplay Module (`src/core/`)

### Files
- `src/core/card.py`
- `src/core/card_figures.py`
- `src/core/game.py`
- `src/core/calculation_*.py`, `src/core/path_rules.py`, etc.

### Compliance
| Principle | Evidence |
|-----------|----------|
| I. Security by Design | Game logic does not read or write files directly; it receives cards and pools from callers and validates dimensions. |
| II. Modular Maintainability | Card generation, figure definitions, winner detection, and calculation engine are separated into focused files with documented inputs/outputs. |
| III. Test-Backed Quality Gates | `tests/test_card.py` verifies dimension, uniqueness, marking, points, and sums. `tests/test_game.py` verifies pool uniqueness, draw exhaustion, figure completion, and scaling. |
| IV. Data Integrity and Traceability | `game_summary` and `calculate_game_summary` derive points and winner status from raw stored data; no calculated fields are persisted in `JUEGOS.bin`. |
| V. UX Accessibility and Educational Fidelity | `card_figures.py` maps each SDG to a figure family, preserving educational SDG context during gameplay. |

---

## 3. SDG Data Module (`src/ods/`)

### Files
- `src/ods/data.py`

### Compliance
| Principle | Evidence |
|-----------|----------|
| II. Modular Maintainability | SDG names, colors, and slogans are centralized in one module to prevent drift across UI screens. |
| V. UX Accessibility and Educational Fidelity | The module provides Spanish SDG labels and slogans used by the configuration, card display, and gameplay screens. |

---

## 4. Persistence Module (`src/persistence/`)

### Files
- `src/persistence/players.py`
- `src/persistence/games.py`
- `src/persistence/io_safety.py`

### Compliance
| Principle | Evidence |
|-----------|----------|
| I. Security by Design | Both `save_players` and `save_games` use append-only binary writes (`"ab"` mode) to prevent silent overwrites. `io_safety.py` handles malformed/corrupted files gracefully. |
| II. Modular Maintainability | Read/write logic is isolated from UI code; public functions are `load_players`, `save_players`, `add_player`, `load_games`, `save_games`, etc. |
| III. Test-Backed Quality Gates | `tests/test_persistence.py` covers append behavior, duplicate rejection, corruption recovery, and calculated-field absence. |
| IV. Data Integrity and Traceability | Game records store only raw fields (player ID, date/time, cards, drawn numbers); `calculate_game_summary` computes totals and winner at read time. |

---

## 5. UI Module (`src/ui/`)

### Files
- `src/ui/common.py`
- `src/ui/app_state.py`
- `src/ui/screens/*.py`
- `src/main.py`

### Compliance
| Principle | Evidence |
|-----------|----------|
| II. Modular Maintainability | Shared rendering helpers live in `common.py`; screen modules expose `init_*`, `handle_event`, and `draw` functions. Constants are centralized in `src/config.py`. |
| III. Test-Backed Quality Gates | `tests/integration/calculation/test_keyboard_accessibility.py` and the card/game test suite exercise UI-triggered flows. |
| V. UX Accessibility and Educational Fidelity | All screen text is in Spanish. `draw_button` provides visible focus borders, hover color changes, and click offset feedback. `Esc` returns to the previous screen or exits from login, register, menu, config, reports, and result screens. SDG images and slogans appear in `config_screen.py`, `card_display_screen.py`, and `game_screen.py`. |

---

## 6. Reporting Module (`src/ui/screens/reports_screen.py`)

### Files
- `src/ui/screens/reports_screen.py`

### Compliance
| Principle | Evidence |
|-----------|----------|
| II. Modular Maintainability | Report generation logic is contained in the reporting screen and delegates aggregation to helper functions. |
| IV. Data Integrity and Traceability | Reports are derived from `load_games()` and `load_players()` source data; frequency, history, and ranking are recalculated on each request. `.txt` exports are saved to `reports/`. |
| V. UX Accessibility and Educational Fidelity | Reports are labeled in Spanish, support date-range filtering, and provide clear error messages for empty date ranges. |

---

## 7. Test Suite (`tests/`)

### Files
- `tests/test_auth.py`
- `tests/test_card.py`
- `tests/test_game.py`
- `tests/test_persistence.py`
- `tests/unit/calculation/*.py`
- `tests/integration/calculation/*.py`
- `tests/contract/*.py`

### Compliance
| Principle | Evidence |
|-----------|----------|
| III. Test-Backed Quality Gates | `pytest tests/` passes with all tests green. The suite covers unit, integration, contract, keyboard accessibility, and binary integrity concerns. |

---

## Verification Command

```bash
python -m pytest tests/
```

Expected result: all tests pass.

---

*Document generated as part of the final delivery checklist. Constitution version: 1.0.0.*
