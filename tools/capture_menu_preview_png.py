"""Captura la renderización del panel de menú y la guarda como PNG.

Ejecutar desde la raíz del repo: `python tools/capture_menu_preview_png.py`
Genera `artifacts/menu_ui_preview_7.png` y `artifacts/menu_ui_preview_5.png`.
"""

import sys

sys.path.insert(0, "")
import pygame
from pathlib import Path
from src.ui.screens import menu_screen


def capture(dimension: int, out_path: Path):
    pygame.init()
    state = {"session": {}}
    menu_screen.init_menu(state)
    state["menu_config"]["dimension"] = dimension
    menu_screen._regenerate_cards(state)
    # create surface matching typical menu layout
    surface = pygame.Surface((800, 600))
    menu_screen.draw(surface, state)
    # save
    out_path.parent.mkdir(parents=True, exist_ok=True)
    pygame.image.save(surface, str(out_path))
    pygame.quit()


def main():
    out = Path("artifacts")
    capture(7, out / "menu_ui_preview_7.png")
    capture(5, out / "menu_ui_preview_5.png")
    print("Saved artifacts/menu_ui_preview_7.png and ..._5.png")


if __name__ == "__main__":
    main()
