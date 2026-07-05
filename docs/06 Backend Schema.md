# Backend Schema

## 1. Overview
Defines the data structure, binary file formats, and validation rules used by the system to persist information.
## 2. Main Entities
### Player
Represents a person registered in the system.
- **ID Number:** Unique identifier of the player.
- **Full Name:** Player's first and last name.
- **Gender:** Character representing gender (m/f).
- **Date of Birth:** Date in a format recognized by the system.
- **State:** Three-character code of the originating state (e.g., BOL, CCS, ZLA).
- **Password:** Password validated using a recursive algorithm.
### Game
Represents a complete game session.
- **Player Identifier:** Participant's ID number.
- **Date and Time:** Time the game was played.
- **Main Card Sequence:** numbers and order of completion.
- **Supplementary Card Sequence:** numbers and order of completion.
- **Numbers Drawn:** list of numbers drawn during the lottery.
- **Winning Card:** indicates which card completed the pattern.
- **Points per Card:** score obtained on each card.
## 3. `PLAYERS.bin` Format
- Binary file with sequential or direct access.
- Each record corresponds to a player.
- The system must verify that there are no duplicate records before registering.
- Fields must have fixed lengths or an internal delimiter to facilitate reading.
## 4. `GAMES.bin` Format
- Binary file where each game played is saved.
- Each record represents a complete game.
- The total score and winner status should not be stored directly as separate fields; These are calculated from the saved data.
- The drawn numbers and card sequences must be reconstructible by reading the file.
## 5. Validation Rules
- The ID number must be unique.
- The name cannot be empty.
- The gender must be "m" or "f".
- The state must exist in the database of recognized codes.
- The password must comply with the security rules defined in challenge 1.
- It must be associated with an existing player.
- The date and time must be valid.
- The card dimensions must be odd, greater than or equal to 5 and less than or equal to 15.
- The card numbers must be in the range of 1 to N×N without repetition.
- The drawn numbers must be unique within the same game.
## 6. Read and Write Operations
### Writing
- Open the file in append mode to avoid overwriting existing records.
- Use `seek()` and `tell()` correctly when necessary.
- Close the file after each operation.
### Reading
- Traverse the file from beginning to end.
- Convert binary data into usable structures.
- Handle empty or corrupted files without stopping the application.
## 7. Data Integrity
- Perform regular backups of binary files.
- Validate data before writing.
- Prevent accidental overwriting of records.
## 8. Implementation Considerations
- Use dedicated functions for serializing and deserializing records.
- Keep persistence logic separate from the graphical interface.
- Document any changes to file formats for future versions.