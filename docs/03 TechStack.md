This tech stack proposal integrates the mandatory academic requirements with **Pygame** to create a visually engaging and educational "SDG-themed Tombola" application.

# **Tech Stack: SDG-themed Tombola**

## **Why Python + Pygame?**
*   **Mandatory Foundation:** The project specifically requires the application to be built using **Python**.
*   **Creative Freedom:** Challenge 5 (Reto 5) explicitly asks for creativity, using images, colors, and slogans to promote the Sustainable Development Goals (SDGs). Pygame provides a robust framework to transition from a basic text interface to a **rich graphical environment** where these visual elements can be displayed dynamically.
*   **Game Mechanics:** Pygame is ideal for the "bingo-style" requirements, such as drawing random numbers and **visually marking cells** with different colors in real-time.

## **Responsibilities**
*   **Frontend (Pygame):**
    *   **Visual Interface:** Rendering the $N \times N$ game cards and highlighting marked numbers.
    *   **Animation:** Managing the tombola draw and the "GANADOR" (WINNER) announcement.
    *   **Educational Overlay:** Displaying SDG images and rotating environmental slogans at the bottom of the screen.
    *   **Language:** All graphical text, labels, slogans, and messages shown in the Pygame interface must be in **Spanish**.
*   **Backend (Python Core):**
    *   **Recursive Logic:** Handling the mandatory **recursive algorithm** for access key validation.
    *   **Game Engine:** Managing random, non-repeating number generation and determining the winner based on the SDG patterns.
    *   **Data Processing:** Sorting algorithms for the "TOP 5" ranking and frequency reports.
*   **Data Layer (Binary Files):**
    *   **Persistence:** Direct reading and writing of player profiles to `JUGADORES.bin` and match history to `JUEGOS.bin`.

## **MVP-first Implementation Approach**
1.  **Phase 1: Core Logic (CLI):** Develop the modular structure and ensure the **binary file storage** and **recursive validation** work perfectly in a terminal environment.
2.  **Phase 2: Pygame Integration:** Implement the visual game loop for Challenges 2 and 3, replacing text inputs with graphical menus for selecting SDG card themes.
3.  **Phase 3: Environmental Polish:** Integrate the "Challenge 5" elements by adding textures, icons for each ODS, and a dynamic messaging system.
4.  **Phase 4: Reporting Module:** Build the file-based reporting system (Gantt charts and Logs) that pulls data from the binary files.

## **Local Development**
*   **Modular Decomposition:** The project must be organized into clear modules (e.g., `auth.py`, `game_logic.py`, `ui_render.py`, `reporting.py`).
*   **Simple, Non-OOP Code Style:** All code must be written without classes or object-oriented patterns. Use plain functions and simple data structures (lists, dictionaries, tuples) to keep the codebase modular yet easy to understand.
*   **Asset Management:** A dedicated folder for SDG images and fonts to ensure the "creative sense" is consistent across the app.
*   **Testing:** Conduct "runs" (corridas) to verify that the random number generation correctly marks cards and stops exactly when a figure is completed.

```text
JuegoODS/
├── src/
│   ├── __init__.py
│   ├── main.py
│   ├── config.py
│   ├── auth/
│   │   ├── __init__.py
│   │   ├── registration.py
│   │   ├── login.py
│   │   └── validator.py
│   ├── core/
│   │   ├── __init__.py
│   │   ├── card.py
│   │   ├── game.py
│   │   └── points.py
│   ├── persistence/
│   │   ├── __init__.py
│   │   ├── players.py
│   │   └── games.py
│   ├── reports/
│   │   ├── __init__.py
│   │   ├── ranking.py
│   │   ├── gantt.py
│   │   └── logs.py
│   ├── ui/
│   │   ├── __init__.py
│   │   ├── app.py
│   │   ├── screens.py
│   │   ├── renderer.py
│   │   └── assets.py
│   └── ods/
│       ├── __init__.py
│       ├── data.py
│       └── messages.py
├── assets/
│   ├── images/ods/
│   ├── fonts/
│   └── sounds/
├── data/
│   ├── JUGADORES.bin
│   └── JUEGOS.bin
├── tests/
│   ├── test_auth.py
│   ├── test_card.py
│   ├── test_game.py
│   └── test_persistence.py
├── docs/
├── README.md
├── requirements.txt
├── pyproject.toml
└── .gitignore
```

## **Future Enhancements**
*   **Soundscapes:** Adding audio clips that explain each SDG when a card is selected.
*   **Scalable UI:** Ensuring the Pygame window adjusts perfectly whether the user chooses a **5x5 or a 15x15** card dimension.
*   **Database Integration:** Transitioning from `.bin` files to a more scalable storage solution for long-term use.

## **Summary**
By combining **Python’s** logical power with **Pygame’s** visual capabilities, this stack fulfills all academic "challenges"—from **recursive security** to **binary persistence**—while creating a high-quality, professional application that effectively promotes the **Sustainable Development Goals**.