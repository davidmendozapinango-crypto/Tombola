# App features

Here is a detailed and creative breakdown of the project stages based on the source material and the specific requirements of the SDG-themed Tombola.

## MVP scope (proof-of-concept version)

The following is a comprehensive list of features for the **SDG-themed Tombola** application, categorized by functional area:

### **1. Secure Player Management (Challenge 1)**
*   **Persistent Storage:** Player data is stored in a permanent binary file (`JUGADORES.bin`).
*   **Comprehensive Profiles:** Captures player ID (cédula), full name, sex (m/f), birthdate, state of origin, and access key.
*   **State Database:** Integrated library of 3-character state codes (e.g., BOL, CCS, ZLA) mapped to their full names.
*   **Recursive Security Validation:** An advanced **recursive algorithm** validates that access keys meet the following criteria:
    *   Length between 6 and 10 characters.
    *   Combination of uppercase, lowercase, numbers, and special characters (*, =, %, or _).
    *   Restriction against more than 3 consecutive identical characters.
*   **Real-time Registration Feedback:** The interface guides the user by highlighting which password criteria are not yet met during the registration process.

### **2. Dynamic Card Generation (Challenge 2)**
*   **Credentialed Access:** Secure login system using the player's ID and validated access key.
*   **Customizable Dimensions:** Supports square cards of **$N \times N$** dimensions, where $N$ is any odd number $\ge$ 5 (e.g., 5x5, 7x7, 9x9... up to 15x15).
*   **SDG Theming:** Menu-driven selection of card pairs (Main and Complement) named after and themed around **Sustainable Development Goals**.
*   **Pattern Visualization:** Displays the filling sequence (numerical order) of the chosen card figure before numbers are assigned.

### **3. Gameplay Mechanics (Challenge 3)**
*   **Unique Number Filling:** Cards are populated with non-repeating random numbers (1 to $N \times N$) following the specific pattern of the selected SDG theme.
*   **Automated Tombola Draw:** System draws random, non-repeating numbers until a winner is found.
*   **Visual Tracking:** 
    *   Real-time display of drawn numbers.
    *   Automatic "marking" of matching numbers on cards using **distinctive colors** for easy verification.
*   **Dynamic UI:** Displays the player's name, their state code, and the specific SDG names for each active card during the match.
*   **Multi-Round Support:** Ability to play multiple rounds consecutively without re-registering players.
*   **Winner Identification:** Automatically identifies and labels the winning card ("GANADOR") and calculates the **sum of all cells** on that card.
*   **Match History:** Every game is recorded in a binary file (`JUEGOS.bin`) including date, time, player ID, card sequences, and the drawn number sequence.

### **4. Advanced Reporting & Analytics (Challenge 4)**
*   **Participation Tracking:** Displays a list of all registered players and the total number of games each has played.
*   **Frequency Analysis (Gantt Chart):** Generates a report showing the **10 most frequent numbers** drawn within a specified date range, sorted from highest to lowest frequency.
*   **Detailed Game Logs:** Historical report of games within a date range, detailing time, player, cards used, points accumulated per card, and the winning card.
*   **TOP 5 Leaderboard:** Ranks the top 5 players based on total points accumulated over a specific period.
*   **File Export:** All reports are saved as physical files for record-keeping.

### **5. Environmental Integration (Challenge 5)**
*   **Educational Content:** Creative integration of images, colors, and slogans related to the SDGs throughout the entire user experience.
*   **Interactive Slogans:** Motivational and educational messages alusive to the chosen SDG theme appear dynamically at the bottom of the screen during gameplay.
*   **Spanish Graphical Language:** All on-screen text, menus, slogans, status messages, and winner announcements rendered in the graphical interface must be in **Spanish**.

To help you complete your project documentation, here is a detailed and creative breakdown of the project stages based on the source material and the specific requirements of the **SDG-themed Tombola**.

## **MVP behavior**
The **Minimum Viable Product (MVP)** is defined by the successful implementation of the five core challenges outlined in the sources. Its behavior includes:
*   **Secure Onboarding:** A user can register and log in only if their password passes a **recursive validation** check against complexity rules.
*   **Dynamic Card Setup:** The system generates a pair of $N \times N$ cards (Main and Complement) for any **odd $N \ge 5$**.
*   **Automated Game Loop:** The tombola draws random, non-repeating numbers, automatically marking them on the user's cards and declaring a winner when a specific SDG pattern is completed.
*   **Essential Persistence:** Every player and every match is saved to binary files (`JUGADORES.bin` and `JUEGOS.bin`).
*   **Stat Reporting:** Users can view participation counts, a **Gantt chart** of number frequencies, and a **TOP 5 ranking** of high-scoring players.

## **Extended-MVP features**
These features build upon the core requirements to enhance the user experience and educational impact:
*   **Expanded SDG Library:** Implementing unique patterns and specific educational content for **all 17 Sustainable Development Goals** beyond the initial examples.
*   **Interactive Slogan Engine:** A system that rotates motivational slogans in the footer during gameplay, tailored specifically to the SDG theme of the active cards.
*   **Session Management:** Allowing a player to play multiple consecutive rounds with different card dimensions without needing to re-authenticate.
*   **Enhanced Visualization:** Using advanced terminal coloring or character-based graphics to make the "marked" numbers and the "WINNER" (GANADOR) announcement more visually striking.

## **Post-MVP features**

### **Essential improvements**
*   **Graphical User Interface (GUI):** Transitioning from a text-based terminal interface to a windowed application (using libraries like Tkinter or Pygame) to better showcase the "images and colors" requested in Reto 5.
*   **Relational Database Migration:** Moving from flat binary files to a structured database (like SQLite) to ensure better data integrity and easier complex reporting for Challenge 4.
*   **Input Robustness:** Adding comprehensive "try-except" blocks to handle non-numeric inputs for dimensions or corrupted binary files.

### **Additional capabilities**
*   **Multiplayer Network Mode:** Evolving from a single-player experience to a local network setup where multiple students can compete on the same tombola draw in real-time.
*   **Exportable Reports:** Adding the ability to export the Gantt charts and TOP 5 rankings as PDF or Excel files for academic review.
*   **Sound Integration:** Adding audio feedback for drawn numbers and a celebratory anthem when a player wins.

### **Practical notes for developers**
*   **Recursion Depth:** When implementing the recursive password validator, ensure it is optimized for the 10-character limit to avoid unnecessary overhead.
*   **File Pointers:** Be meticulous with `seek()` and `tell()` when reading/writing to `JUEGOS.bin` to ensure that data is appended correctly without overwriting previous matches.
*   **Modular Decoupling:** Keep the "Environmental Integration" (Reto 5) as a separate module so that educational content can be updated without touching the core game logic.

## **Additional features (longer-term)**
*   **Gamified Learning Quizzes:** Before starting a round, players could answer a quick trivia question about an SDG to receive a "bonus" marked cell on their complement card.
*   **Mobile Companion App:** A version of the app that allows users to view their game history and global TOP 5 rankings from their phones.
*   **Global SDG Leaderboard:** An online component where students from different classes can compare their total accumulated points and participation in environmental awareness.
