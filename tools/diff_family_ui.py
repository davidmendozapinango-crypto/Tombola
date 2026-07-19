"""Generar imagen de comparación: patrón familiar vs patrón usado por la UI.

Guarda `artifacts/diff_family_ui_7.png` y escribe diferencias en consola.
"""

import sys

sys.path.insert(0, "")
import pygame
from pathlib import Path
from src.core.card import make_cards
from src.core.card_figures import get_figure_pattern, get_card_type
from src.core.figures.families import familia_a


def draw_grid(surface, top_left, n, cell_size, occupied, numbers=None, title=None):
    x0, y0 = top_left
    font = pygame.font.SysFont(None, max(12, cell_size // 2))
    if title:
        txt = font.render(title, True, (10, 10, 10))
        surface.blit(txt, (x0, y0 - 30))
    for i in range(n):
        for j in range(n):
            rect = pygame.Rect(
                x0 + j * cell_size, y0 + i * cell_size, cell_size, cell_size
            )
            fill = (255, 255, 255)
            if (i, j) in occupied:
                fill = (30, 120, 40)
            pygame.draw.rect(surface, fill, rect)
            pygame.draw.rect(surface, (0, 0, 0), rect, width=1)
            if numbers and numbers[i][j] is not None:
                text = font.render(str(numbers[i][j]), True, (255, 255, 255))
                trect = text.get_rect(center=rect.center)
                surface.blit(text, trect)


def main():
    pygame.init()
    n = 7
    cell = 40
    padding = 40
    width = (n * cell) * 2 + padding * 3
    height = n * cell + padding * 2 + 40
    surf = pygame.Surface((width, height))
    surf.fill((240, 240, 240))

    card_type = get_card_type(1)
    family_pattern = set(get_figure_pattern(card_type, is_main=True, dimension=n))
    cards = make_cards(n, family_pattern, None)
    main_card = cards["main"]
    ui_pattern = {
        (r, c)
        for r, row in enumerate(main_card)
        for c, val in enumerate(row)
        if val is not None
    }

    # draw expected on left, actual on right
    left_tl = (padding, padding + 30)
    right_tl = (padding * 2 + n * cell, padding + 30)
    draw_grid(surf, left_tl, n, cell, family_pattern, None, title="Expected (family)")
    draw_grid(surf, right_tl, n, cell, ui_pattern, main_card, title="Actual (UI)")

    # highlight differences
    diff1 = sorted(family_pattern - ui_pattern)
    diff2 = sorted(ui_pattern - family_pattern)
    font = pygame.font.SysFont(None, 20)
    y = padding
    info = font.render(
        f"diff expected-only: {len(diff1)} expected, actual-only: {len(diff2)}",
        True,
        (10, 10, 10),
    )
    surf.blit(info, (padding, 5))
    # draw red X on mismatches in both grids
    for r, c in diff1:
        rx = left_tl[0] + c * cell
        ry = left_tl[1] + r * cell
        pygame.draw.line(
            surf, (200, 20, 20), (rx + 4, ry + 4), (rx + cell - 4, ry + cell - 4), 4
        )
        pygame.draw.line(
            surf, (200, 20, 20), (rx + cell - 4, ry + 4), (rx + 4, ry + cell - 4), 4
        )
    for r, c in diff2:
        rx = right_tl[0] + c * cell
        ry = right_tl[1] + r * cell
        pygame.draw.line(
            surf, (200, 20, 20), (rx + 4, ry + 4), (rx + cell - 4, ry + cell - 4), 4
        )
        pygame.draw.line(
            surf, (200, 20, 20), (rx + cell - 4, ry + 4), (rx + 4, ry + cell - 4), 4
        )

    out = Path("artifacts")
    out.mkdir(exist_ok=True)
    path = out / "diff_family_ui_7.png"
    pygame.image.save(surf, str(path))
    print("Saved", path)
    print("Expected-only:", diff1)
    print("Actual-only:", diff2)
    pygame.quit()


if __name__ == "__main__":
    main()
