# Project Title: Tombola Game
## Description
The **Sustainable Development Goals (SDG) Tombola** is a Python-based application developed for the Algorithms and Programming course at the Universidad Católica Andrés Bello. The project challenges students to build a functional bingo-style game that promotes the United Nations' Sustainable Development Goals through its mechanics, visual design, and informative content.

## Objectives 
### General Objective
**Social and Environmental Awareness:** The game is described as a "project with an ecological sense". Its core purpose is to **foster knowledge about the Sustainable Development Goals (SDGs)** by requiring students to creatively incorporate information, images, and slogans related to these goals into the application

### Specific Objectives
The project serves a dual purpose:
1. **Educational:** To develop professional competencies in software application development—specifically analysis, modular design, recursive algorithm implementation, and data persistence.
2. **Social:** To foster an "ecological sense" by immersing players in the themes and slogans of the 17 SDGs.
## Scope
The project scope is defined by **five specific challenges**:
1. **Player Registration:** Storing data in binary files with access key validation using recursive algorithms.
2. **Card Creation:** Generating game cards (main and complement) based on NxN dimensions (odd $\ge$ 5) and SDG themes.
3. **Tombola Gameplay:** Running the game with random numbers, marking cards, and determining a winner (bingo style).
4. **Report Generation:** Creating reports on players, Gantt charts for number frequency, and logs of completed games.
5. **Environmental Elements:** Creative integration of information, images, and slogans about the SDGs within the application.

## Key Functional Components

The game is structured around five primary "challenges":

1. **Secure Player Management:** A system to register players using binary files for permanent storage (`JUGADORES.bin`). It features a **recursive algorithm** to validate complex access keys, ensuring they meet specific security criteria.
2. **Dynamic Card Generation:** Players generate a pair of cards (Main and Complement) based on a chosen SDG theme. The cards are flexible in size, supporting N×N **dimensions** where N is any odd number between 5 and 15.
3. **Automated Gameplay:** The tombola draws random, non-repeating numbers from 1 to N×N. The system automatically marks matching numbers on the player's cards and identifies a **winner** when a specific pattern (figure) is completed.
4. **Data Persistence & Reporting:** Every match is recorded in a `JUEGOS.bin` file. The system generates detailed reports, including **TOP 5 player rankings**, game logs with accumulated points, and **Gantt charts** visualizing the frequency of drawn numbers.
5. **Ecological Integration:** The interface creatively incorporates colors, imagery, and inspirational slogans related to the SDGs to educate the player throughout the experience

## Delivery approach

The delivery is divided into **two parts**:
*   **Part One (5%):** Focused on planning, including the work methodology, modular decomposition, analysis of challenges 1 through 4, the approach for challenge 5, and the design of algorithms. This part is completed
*   **Part Two (20%):** Delivery of the built application and a detailed written report, including a user manual and a summary of activities performed by each team member.

## What "MVP working" means

A functional application ("MVP working") means the software must complete all development stages—analysis, design, construction, testing, and execution—and demonstrate that it provides a **correct response to the situations posed** in the five challenges.

## Extended-MVP (next phase)

The sources do not explicitly define an "Extended-MVP" phase, as the project concludes with the **defense and demonstration of the products obtained** during week 17 of the semester.

### Local development checklist

For the development and final submission, the following must be met:
Before testing the MVP, verify:

#### Challenge 1: Player Registration
- [ ] Storage: Is player data saved in a binary file (e.g., JUGADORES.bin)?
- [ ] Fields: Does it store ID (cédula), full name, sex (m/f), birthdate, 3-character state code (e.g., BOL, CCS), and access key?
- [ ] Uniqueness: Does the system prevent registering the same ID more than once?
- [ ] Access Key Rules:
    - [ ] Is it between 6 and 10 characters long?
    - [ ] Is it a mix of uppercase, lowercase, and numbers?
    - [ ] Does it contain at least one special character (*, =, %, or _)?
    - [ ] Does it block more than 3 consecutive identical characters (e.g., "1111" is invalid)?
    - [ ] Key Validation: Is the validation performed using a recursive algorithm?
    - [ ] User Interface: Does it show the key criteria and indicate which ones are not met during creation?

#### Challenge 2: Card Creation
- [ ] Authentication: Does it require a valid ID and access key to enter?
- [ ] Dimensions: Does it allow the user to define an NxN size where N is odd and ≥ 5 (e.g., 5, 7, 9... up to 15)?
- [ ] Themes: Are cards presented in pairs (Main and Complement) identified by SDG names?
- [ ] Visual Sequence: Before playing, does it show the cards with the filling sequence starting from 1?

#### Challenge 3: Gameplay & Persistence
- [ ] Random Filling: Are cards filled with unique random numbers (1 to N×N) according to the specific SDG pattern?
- [ ] Tombola Mechanics: Does the system draw random, non-repeating numbers (1 to N×N)?
- [ ] Auto-Marking: Are matching numbers automatically marked and visually distinguished (e.g., with a different color)?
- [ ] Winner Logic: Does the game stop exactly when a card completes its SDG figure (bingo style)?
- [ ] End-of-Game:
    - [ ] Is the winning card labeled "GANADOR"?
    - [ ] Does it display the sum of the winning card's cells?
    - [ ] Data Storage: Is each game saved in JUEGOS.bin with the ID, date/time, card sequences, and numbers drawn?
    - [ ] Constraint: Are you avoiding storing total points or the "winning" status in the binary file?

#### Challenge 4: Reporting
- [ ] Player Summary: Can it list all IDs and names from JUGADORES.bin along with their total games played?
- [ ] Gantt Chart: Does it generate a report showing the 10 most frequent numbers in a date range, sorted high-to-low?
- [ ] Game Logs: Does it report games in a date range including date, time, player, cards used, points per card, and the winner?
- [ ] TOP 5 Ranking: Does it show the top 5 players by accumulated points in a date range, including ID, name, and total points?
- [ ] File Output: Are reports (Gantt, Logs, and Top 5) saved to a physical file?

#### Challenge 5: Environmental Integration
- [ ] Creativity: Are images, colors, and slogans promoting the SDGs integrated into all previous challenges?
- [ ] Active Messaging: Do educational messages about the SDGs appear during the tombola (e.g., at the bottom of the screen)?

#### Final Submission Requirements
- [ ] Part 1 : Modular decomposition, problem analysis (I/O), Reto 5 approach, and algorithm designs.
- [ ] Part 2 (20%):
    - [ ] Full Python source code for backend logic.
    - [ ] Full Python source code + pygame for fontend.
    - [ ] Written report (Intro, Modular Chart, Algorithms, Code).
    - [ ] Summary of activities for each member.
    - [ ] User Manual (guide on how to use the app).


## Future enhancements (post-MVP)

**The provided sources do not contain information** regarding future improvements or post-MVP plans after the conclusion of the academic project.

## Technology selection note

The mandatory technological requirements include:
*   **Programming Language:** Python and pygame.
*   **Storage:** Binary files for data persistence (e.g., `JUGADORES.bin` and `JUEGOS.bin`).
*   **Graphical Language:** All text, labels, slogans, and UI messages displayed in the graphical interface must be in **Spanish**.

## How this document fits with the others

This document serves as the **main guide and requirements specification** for the Final Project of the Algorithms and Programming course for the 2022-15 semester at the Universidad Católica Andrés Bello. **No other documents are available** in the sources to establish further context, but this functions as the master roadmap for all delivery and evaluation phases.


