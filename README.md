# Tombola Game

Academic SDG-themed Tombola project built with Python and Pygame.

## Overview

This desktop application implements a modular Tombola game with authenticated players,
binary persistence, and an internal calculation engine triggered directly from the GUI.
The project follows a project constitution that prioritizes security, test-backed
quality, data integrity, and Spanish-first user experience.

## Tech Stack

- Python 3
- Pygame (UI)
- pytest (testing)

## Setup

1. Clone the repository and switch to the `main` branch:

```bash
git checkout main
```

2. Create and activate a Python virtual environment:

On Windows:

```bash
python -m venv .venv
.venv\Scripts\activate
```

On Linux or macOS:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

## Running the Application

Launch the GUI entry point:

```bash
python src/main.py
```

The application starts at the login screen. Default credentials are created
automatically if `data/JUGADORES.bin` is empty:

- **Cedula:** `12345678`
- **Clave:** `Hola1=`

Use `Tab` to move focus between controls and `Enter` or `Space` to activate the
focused control. `Esc` returns to the previous screen or exits.

## Application Flow

1. **Login / Registro:** Authenticate with an existing player or register a new
   one. Access keys are validated recursively.
2. **Menu principal:** Choose *Jugar*, *Reportes*, *Demo calculadora*, *Cerrar sesion*,
   or *Salir*.
3. **Configuracion de cartones:** Select an odd dimension (5-15) and an SDG theme.
4. **Vista previa de cartones:** See the filling sequence and the SDG figure that
   must be completed to win. The figure images are loaded from `assets/images/ods/`.
5. **Partida:** Draw random numbers; matching cells are marked automatically. The
   game ends when a card completes its SDG figure and shows the winner's cell sum.
6. **Resultado:** Review the winning card and choose to play again or return to
   the menu.
7. **Reportes:** View players, game counts, TOP 5 rankings, frequent numbers,
   and recent game history. Reports can be exported to `reports/` as `.txt` files.

## Testing

Run the full automated test suite:

```bash
pytest
```

Run only the calculation tests:

```bash
pytest tests/
```

Run a specific test file:

```bash
pytest tests/integration/calculation/test_gui_trigger_success.py
```

Run a single test by name:

```bash
pytest tests/integration/calculation/test_gui_trigger_success.py::test_gui_trigger_success
```

Run with verbose output to see each test name:

```bash
pytest -v
```

Run quietly and stop on the first failure:

```bash
pytest -q -x
```

The suite includes contract, unit, and integration tests for the calculation feature.

## Project Structure

```text
src/
  auth/          # Session and recursive password validation
  core/          # Card generation, game logic, SDG figures, calculation engine
  ods/           # SDG data (names, colors, slogans)
  ui/            # GUI flows, state, and screens
  persistence/   # Binary persistence and impact record helpers
  main.py        # Pygame application entry point
tests/
  contract/      # Contract tests for commands and impact records
  unit/          # Unit tests for rules, preconditions, and dependencies
  integration/   # End-to-end flow and acceptance tests
  test_auth.py   # Authentication and registration validation tests
  test_persistence.py # Binary persistence edge case tests
specs/           # Feature specifications, plans, and task tracking
.specify/        # Project memory, constitution, and templates
docs/            # Project documentation and user manual
assets/          # SDG figure images, fonts, and sounds
data/            # Binary persistence files (JUGADORES.bin, JUEGOS.bin)
reports/         # Exported text reports
```

## Governance

Project governance is defined in `.specify/memory/constitution.md`.

Core non-negotiable principles:

- Security by design for authentication and binary persistence.
- Modular maintainability with clear module boundaries.
- Test-backed quality gates for core logic changes.
- Data integrity and traceability for `.bin` records and reports.
- Spanish-first UX with SDG educational fidelity.

## Current Feature

**Branch**: `main`

The application now implements the full Tombola flow: login/registration with
recursive password validation and live password-criteria feedback, binary
append-only player and game persistence, configurable SDG-themed cards with
figure previews, SDG figure-based winner detection, automated tombola draws,
results, and reports with `.txt` export. The original calculation feature
remains available as the *Demo calculadora* option in the main menu. See
`docs/ManualUsuario.md` for the complete user guide and
`specs/001-define-calculation-rules/quickstart.md` for calculation-specific
validation scenarios.
