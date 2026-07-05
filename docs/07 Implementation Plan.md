# Implementation Plan

## 1. Overview
Defines the phases, tasks, responsibilities, and schedule for developing the SDG-themed Tombola application while meeting the five academic challenges.

This plan MUST comply with the project constitution in
`.specify/memory/constitution.md`, with explicit checks for security,
maintainability, and code quality in each phase.

## 2. Project Phases

### Phase 1: Analysis and Planning
- Review the project statement and existing documentation.
- Define team roles.
- Complete the base documentation: goals, features, tech stack, UX, flow, backend, and plan.
- Establish coding conventions and project structure: modular, simple code without classes or object-oriented programming.

**Deliverable:** complete documentation in `docs/`.

### Phase 2: Environment Setup
- Create the project folder structure.
- Configure the Git repository.
- Create `requirements.txt` and `pyproject.toml`.
- Prepare the assets folder (images, fonts, sounds).

**Deliverable:** functional, versioned base project.

### Phase 3: Authentication Module (Challenge 1)
- Implement player registration.
- Implement recursive key validation.
- Implement login.
- Implement reading/writing of `JUGADORES.bin`.

**Deliverable:** players can register and log in.

### Phase 4: Card Module (Challenge 2)
- Implement NxN card generation.
- Implement SDG theme selection.
- Implement visualization of the filling sequence.
- Implement prior authentication for access.

**Deliverable:** player can create and view their cards.

### Phase 5: Game Module (Challenge 3)
- Implement random, non-repeating number draw.
- Implement automatic marking of numbers on cards.
- Detect winning card when the figure is completed.
- Calculate the sum of the winning card.
- Save each match in `JUEGOS.bin`.

**Deliverable:** fully functional game from start to finish.

### Phase 6: Reporting Module (Challenge 4)
- Implement listing of players and matches.
- Implement Gantt chart of frequencies.
- Implement game history.
- Implement TOP 5 players.
- Export reports to physical files.

**Deliverable:** reports generated correctly from the binary files.

### Phase 7: Environmental Integration (Challenge 5)
- Integrate images, colors, and slogans of the SDGs.
- Display educational messages during the game.
- Ensure the entire graphical interface is in Spanish.
- Polish animations and visual transitions.

**Deliverable:** complete graphical interface aligned with the SDGs.

### Phase 8: Frontend Integration with Pygame
- Develop screens in Pygame.
- Connect user events with game logic.
- Adapt the interface to different card dimensions.
- Conduct usability tests.

**Deliverable:** functional graphical application.

### Phase 9: Testing and Debugging
- Run test sessions with different dimensions.
- Verify correct data persistence.
- Review key validations and duplicate registrations.
- Fix detected errors.
- Execute deterministic verification for recursive password validation,
  non-repeating draw behavior, winner detection, and binary integrity handling.

**Deliverable:** stable version without critical errors.

### Phase 10: Final Delivery
- Write the written report.
- Prepare the user manual.
- Prepare the activity summary per team member.
- Package source code and documentation.

**Deliverable:** final product ready for defense and demonstration.

## 3. Responsibility Assignment

| Module | Suggested Owner |
|---|---|
| General documentation | Whole team |
| Authentication and persistence | Member 1 |
| Cards and SDG figures | Member 2 |
| Game logic and draw | Member 3 |
| Reports and statistics | Member 4 |
| Graphical interface with Pygame | Member 5 |
| Final testing and adjustments | Whole team |

## 4. Suggested Schedule

| Phase | Estimated Duration |
|---|---|
| Phase 1 | 3 days |
| Phase 2 | 2 days |
| Phase 3 | 4 days |
| Phase 4 | 4 days |
| Phase 5 | 5 days |
| Phase 6 | 4 days |
| Phase 7 | 4 days |
| Phase 8 | 5 days |
| Phase 9 | 4 days |
| Phase 10 | 4 days |

**Total estimated duration:** approximately 6 weeks.

## 5. Risks and Mitigation

| Risk | Mitigation |
|---|---|
| Loss of binary data | Make frequent backups |
| Difficulty with recursive validation | Design and test the algorithm in parts |
| Performance issues with large cards | Test with maximum dimensions from early stages |
| Late Pygame integration | Create visual prototypes from phase 3 |
| Documentation inconsistencies | Review docs at the end of each phase |

## 6. Completion Criteria
- The five challenges work correctly and independently.
- The graphical application is in Spanish and stable.
- Binary files store and retrieve information without errors.
- Documentation is complete, coherent, and up to date.
- The written report, user manual, and activity summary are ready.
- Constitution compliance evidence exists for each delivered module.
