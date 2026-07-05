# Title: Tombola Game - UI/UX Pygame Desktop Application
## Summary

>[!Abstract]
>
>
>.

---
## 1. Version Control and Window Configuration

Since Pygame renders in a native operating system window, it is essential to define the initial canvas.

* **Initial Screen Configuration:**
* **Base Resolution:** e.g. `1280 x 720` pixels (16:9 aspect ratio).
* **Mode:** Fixed window, resizable (`pygame.RESIZABLE`), or fullscreen (`pygame.FULLSCREEN`)?
* **Resize Behavior:** If the user stretches the window, does the content scale proportionally (letterboxing/pillarboxing) or does the visible area expand?

* **Key Links:** Links to visual mockups, shared folder with audio/graphic assets, and code repository.

---

## 2. Application State Flow (State Machine)

The logical control flow in Pygame must be implemented through an event loop that updates and invokes drawing modules according to the `current_state` variable:

```
               +---------------+
               |     LOGIN     |<---------------+
               +---------------+                | (Logout)
                       | (Authentication)        |
                       v                        |
               +---------------+                |
               |   DASHBOARD   |----------------+
               +---------------+
                 |           |
    (Configure)  |           | (View Reports)
                 v           v
          +-----------+ +-----------+
          | GAMEPLAY  | |  METRICS  |
          +-----------+ +-----------+
```

### Behavior Specification per State:

1. **LOGIN (Access):** Menu to select the player's ID (loaded from `JUGADORES.bin`) and a 55x55 pixel on-screen numeric keypad to securely enter the 4-digit key.
2. **REGISTER (New Player):** Form to enter ID, Full Name, Age, Gender, and Venezuelan State, synchronously serializing the registration into the database file.
3. **DASHBOARD (Control Center):** Adjustment of card dimensions (Matrix: 5, 7, 9, or 11), selection of the filling algorithm, and choice of the SDG theme to solve.
4. **GAMEPLAY (Tombola):** Animation of the ball drum on the left side. When the spin stops, a numbered physical ball is ejected. On the right, the interactive card is rendered for user click detection.
5. **METRICS (Historical Symbiosis):** Displays the national ranking through bar charts and prints the decoded log in real time from `JUEGOS.bin`.

---

## 3. Visual Style Guide and Asset Management
### Window Configuration and Graphics Engine
To ensure a perfectly symmetrical replica of the web prototype in a native desktop application, Pygame must be initialized with the following hardware physical specifications:
- Fixed Base Resolution: 1024 x 768 pixels (Standard 4:3 aspect ratio for school-use screens).
- Window Mode: Fixed with double buffer (`pygame.DOUBLEBUF`) to avoid visual flickering (tearing) during tombola animations.
- Refresh Rate: Strictly limited to 60 FPS using a system clock to stabilize hardware processor update cycles:

```Python
clock = pygame.time.Clock()
dt = clock.tick(60) / 1000.0  # Delta time for smooth, time-based animations
```

### Interface Color Palette (RGB Format)
 Everything is defined through RGB color tuples and rectangle coordinates (`pygame.Rect`).

For Pygame colors to exactly match the "eye-safe" aesthetic (designed for students' visual rest) of the web prototype, the following constants must be declared in the Python file:

#### A. Base Theme Colors (Corporate)

| Python Constant | RGB Value (8-bit Integers) | Hexadecimal | Use in Pygame Interface                                         |
| --------------- | -------------------------- | ----------- | --------------------------------------------------------------- |
| COLOR_PINE      | (56, 102, 65)              | #386641     | Main titles, active button backgrounds, and table headers.      |
| COLOR_MOSS      | (167, 201, 87)             | #a7c957     | Card borders, hit indicator, and confirmation buttons.          |
| COLOR_MINT      | (242, 247, 244)            | #f2f7f4     | Main screen background (eye-rest canvas).                       |
| COLOR_CHARCOAL  | (27, 46, 30)               | #1b2e1e     | Primary texts, SDG captions, and card outlines.                 |
| COLOR_WHITE     | (255, 255, 255)            | #ffffff     | Background of numeric cells in the game tombola.                |
| COLOR_SAGE_LIGHT| (215, 225, 210)            | #d7e1d2     | Panel borders, divider lines, and disabled states.              |
| COLOR_RED_ALERT | (220, 80, 80)              | #dc5050     | Error messages, log deletion button, and reading LED.           |
| COLOR_AMBER_LED | (245, 180, 50)             | #f5b432     | LED indicator of synchronous writing to binary storage.         |


* **Typography:** Fonts in `.ttf` or `.otf` format that will be bundled with the app (e.g. `Ubuntu-Regular.ttf`).
* Sizes defined in points for `pygame.font.Font` objects (e.g. Titles: 32pt, Buttons: 24pt, Body: 16pt).


* **Sprites and Graphic Elements:** Mandatory `.png` format with alpha channel (transparency). Specify the exact pixel size to avoid Pygame consuming CPU scaling images in real time through `pygame.transform.scale`.
#### B. Identity Colors for the Sustainable Development Goals (SDGs)

Each card will dynamically change its brand color when the player selects a specific SDG in the control panel. The programmer must map the hit matrix with these constants:

```python
COLOR_SDG = {
    1:  (229, 36, 59),   # SDG 1: No Poverty (Red)
    2:  (221, 166, 58),  # SDG 2: Zero Hunger (Mustard)
    3:  (76, 159, 56),   # SDG 3: Good Health and Well-being (SDG Green)
    4:  (199, 33, 47),   # SDG 4: Quality Education (Dark Red)
    5:  (239, 64, 43),   # SDG 5: Gender Equality (Orange)
    6:  (38, 189, 226),  # SDG 6: Clean Water and Sanitation (Light Blue)
    7:  (252, 195, 11),  # SDG 7: Affordable and Clean Energy (SDG Yellow)
    8:  (162, 25, 66),   # SDG 8: Decent Work and Economic Growth (Burgundy)
    9:  (243, 111, 33),  # SDG 9: Industry, Innovation and Infrastructure (Bright Orange)
    10: (221, 19, 103),  # SDG 10: Reduced Inequalities (Fuchsia)
    11: (249, 157, 37),  # SDG 11: Sustainable Cities and Communities (Warm Orange)
    12: (207, 141, 42),  # SDG 12: Responsible Consumption and Production (Ochre)
    13: (63, 126, 68),   # SDG 13: Climate Action (Dark Green)
    14: (10, 151, 217),  # SDG 14: Life Below Water (SDG Blue)
    15: (86, 192, 43),   # SDG 15: Life on Land (Light Green)
    16: (19, 106, 124),  # SDG 16: Peace, Justice and Strong Institutions (Petroleum Blue)
    17: (24, 72, 116),   # SDG 17: Partnerships for the Goals (Navy Blue)
}
```

---

## 4. Custom UI Component Specifications

Since Pygame does not include native buttons or inputs, they must be programmed from scratch by analyzing collisions with `rect.collidepoint(event.pos)`. Their design and behavior must be specified:

* **Buttons:**
* *Normal:* Flat rectangle or base sprite.
* *Hover:* Background color change or highlighted border when the mouse pointer collides with the area.
* *Click:* Text offset 2 pixels down/right to simulate physical depth.


* **Text Fields (Inputs):**
* *Inactive:* Gray border.
* *Active (Focus):* Primary color border and a blinking cursor (`|`). Specify character limit and behavior if prohibited keys are pressed.


* **Scroll Bars / Sliders (e.g. Volume Control):**
* Rail design, handle design, and calculation of the float value between `0.0` and `1.0` according to the mouse `X` position while dragging.



---

## 5. Control Map (Inputs)

It is vital to map how the user interacts with the desktop application at the hardware level.

| UI Action | Mouse Event | Alternative Key (Keyboard) |
| --- | --- | --- |
| Select / Click | `pygame.MOUSEBUTTONDOWN` (Left) | `K_RETURN` (Enter) or `K_SPACE` |
| Navigate between elements | Move cursor over elements | `K_UP` / `K_DOWN` / `K_TAB` |
| Go back / Cancel | Click "Back" button | `K_ESCAPE` |
| Scroll | Mouse wheel (`BUTTON_WHEELUP/DOWN`) | `K_PAGEUP` / `K_PAGEDOWN` |

---

## 6. Performance and Refresh Rates (FPS)

UI fluidity depends on the system clock (`pygame.time.Clock`).

* **Target FPS:** Fixed at stable `60 FPS` (`clock.tick(60)`).
* **Time-Based Animations:** If there are screen transitions (fades) or interface element movements, specify whether time deltas (`dt`) will be used to ensure the UI moves at the same speed regardless of the user's processor power.

---

## 7. Texts, Contents, and System Messages

Each text string must be stored in a centralized dictionary or JSON file to facilitate rendering and future translations.

* **Menu Texts:** "Start", "Settings", "Exit".
* **Alert Messages:** What happens if the app does not detect a save file or the resolution is not supported? Design the internal dialog box that will be drawn over the current screen.

---

## 8. Accessibility Criteria in Graphical Environments

Because it is a free canvas, accessibility must be explicitly programmed:

* **Visual Focus Indicator:** If the user chooses to navigate the interface with the keyboard arrows, the currently selected element must have a very visible outer border or an indicator icon next to it (e.g. an arrow or asterisk).
* **Blinking Frequency:** Ensure that cursors or blinking elements do not exceed 3 Hz to avoid photosensitivity issues.

---

## 9. Hand-off Protocol for Pygame Developers

How to deliver the screens to the Python programmer.

* **Suggested Asset Folder Structure:**
```text
assets/
├── fonts/      # .ttf files
├── graphics/   # UI sprites, backgrounds, icons (.png)
└── sfx/        # Sound effects for clicks or transitions (.wav)

```


* **Absolute Coordinates:** Provide the `(X, Y)` position of the top-left corner of each important element relative to the base resolution (`1280x720`).

---
