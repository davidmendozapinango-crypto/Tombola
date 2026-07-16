# Tombola Game - Project Completion Checklist

## Documentation

- [x] Project goals documented in `docs/01 ProjectGoals.md`
- [x] Application features documented in `docs/02 AppFeatures.md`
- [x] Tech stack documented in `docs/03 TechStack.md`
- [x] UX design documented in `docs/04 UXDesing.md`
- [x] Frontend flow documented in `docs/05 FrontEnd Flow.md`
- [x] Backend schema documented in `docs/06 Backend Schema.md`
- [x] Implementation plan documented in `docs/07 Implementation Plan.md`
- [x] This checklist kept up to date in `docs/checklist.md`

## Environment Setup

- [x] Python 3 installed
- [x] Virtual environment created and activated
- [x] Dependencies installed from `requirements.txt`
- [x] `data/` directory exists with `JUGADORES.bin` and `JUEGOS.bin`
- [x] `assets/` directory created for images, fonts, and sounds
- [x] Project runs with `python src/main.py`
- [x] Full test suite passes with `pytest`

## Architecture & Code Style

- [x] Project follows modular decomposition
- [x] Code uses functions and dictionaries (no classes or OOP)
- [x] Graphical interface text rendered in Spanish
- [x] Constitution compliance evidence exists for each module
- [x] Sensitive data (keys, credentials) not logged or exposed

## Challenge 1: Secure Player Management

- [x] Player data persisted to `data/JUGADORES.bin`
- [x] Each player record contains: ID (cédula), full name, sex (m/f), birthdate, 3-character state code, access key
- [x] Duplicate player IDs are rejected
- [x] Access key length enforced between 6 and 10 characters
- [x] Access key contains at least one uppercase letter
- [x] Access key contains at least one lowercase letter
- [x] Access key contains at least one digit
- [x] Access key contains at least one special character (`*`, `=`, `%`, `_`)
- [x] Access key blocks more than 3 consecutive identical characters
- [x] Key validation implemented with a recursive algorithm
- [x] Registration UI shows password criteria and indicates unmet rules
- [x] Player login verifies ID and access key against `JUGADORES.bin`

## Challenge 2: Dynamic Card Creation

- [x] Card creation requires valid ID and access key
- [x] Player can choose an odd dimension N where 5 <= N <= 15
- [x] Card pair generated: Main and Complement
- [x] Each card themed with one of the 17 SDGs
- [x] Main and Complement cards identified by SDG names
- [x] Cards display the filling sequence before numbers are assigned
- [x] Each card filled with unique random numbers from 1 to N×N

## Challenge 3: Gameplay & Persistence

- [x] Tombola draws random, non-repeating numbers from 1 to N×N
- [x] Matching numbers are marked automatically on both cards
- [x] Marked cells are visually distinguished
- [x] Game detects when a card completes the SDG figure
- [x] Winning card labeled "GANADOR"
- [x] Sum of all cells on the winning card displayed
- [x] Player can play multiple consecutive rounds without re-authenticating
- [x] Each game saved to `data/JUEGOS.bin`
- [x] Game record contains: player ID, date/time, main card, complement card, drawn numbers
- [x] Total points and "winning" status are calculated, not stored as separate fields

## Challenge 4: Reporting

- [x] Report screen lists all players with total games played
- [x] Gantt-style frequency report shows the 10 most drawn numbers in a date range
- [x] Frequency report sorted from highest to lowest
- [x] Game history report shows date, time, player, cards, points per card, and winner
- [x] TOP 5 ranking shows the highest-scoring players by accumulated points
- [x] Reports are saved to physical files

## Challenge 5: Environmental Integration

- [x] SDG colors used throughout the interface
- [x] SDG images integrated where available
- [x] SDG slogans displayed on relevant screens
- [x] Educational SDG messages appear during gameplay
- [x] Rotating SDG educational message panel shown on every screen
- [x] Visual design promotes the Sustainable Development Goals

## Frontend / Pygame UI

- [x] Window configured at 1024×768 with double buffering
- [x] Application runs at a stable 60 FPS
- [x] Login screen implemented
- [x] Registration screen implemented
- [x] Main menu screen implemented
- [x] Card configuration screen implemented
- [x] Card display screen implemented
- [x] Gameplay screen implemented
- [x] Results screen implemented
- [x] Reports screen implemented
- [x] Navigation works with mouse and keyboard
- [x] Visible focus indicator for keyboard navigation
- [x] Buttons show hover and click feedback
- [x] Text inputs support focus, typing, and backspace
- [x] Error messages displayed in Spanish
- [x] `Esc` key returns or exits appropriately

## Backend / Persistence

- [x] `JUGADORES.bin` uses binary serialization
- [x] `JUEGOS.bin` uses binary serialization
- [x] Records appended without overwriting existing data
- [x] Empty or corrupted binary files handled gracefully
- [x] Read/write logic isolated from UI code
- [x] State code validation uses the built-in state catalog

## Testing & Quality

- [x] Contract tests exist for command and impact records
- [x] Unit tests exist for path rules, preconditions, and dependencies
- [x] Integration tests exist for GUI-triggered flows
- [x] Login and registration validation covered by tests
- [x] Card generation and game logic covered by tests
- [x] Binary persistence edge cases covered by tests
- [x] All tests pass before delivery

## Final Delivery

- [x] Complete Python source code in `src/`
- [x] Full Pygame frontend implemented
- [x] Written report with introduction, modular chart, algorithms, and code
- [x] User manual explaining how to run and use the application
- [x] Summary of activities performed by each team member
- [x] README.md updated with setup, run, and test instructions
