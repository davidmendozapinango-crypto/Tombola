"""Renderiza una vista HTML que simula exactamente `_draw_preview_card` del menu.

Genera archivos en `artifacts/menu_preview_{n}.html` replicando colores
y tamaño de celda usado en la UI para facilitar inspección local.
"""

import sys

sys.path.insert(0, "")
from pathlib import Path
from html import escape
from src.core.card import make_cards
from src.core.card_figures import get_card_type

COL_FILL = "#2e7d32"  # approximated COLOR_PINE
COL_WHITE = "#ffffff"
COL_BORDER = "#2b2b2b"  # COLOR_CHARCOAL


def render_html(card, cell_size=18, title="Preview"):
    n = len(card)
    w = n * cell_size
    h = n * cell_size
    cells = []
    for i, row in enumerate(card):
        for j, val in enumerate(row):
            x = j * cell_size
            y = i * cell_size
            if val is not None:
                fill = COL_FILL
                text = str(val)
                text_color = COL_WHITE
            else:
                fill = COL_WHITE
                text = ""
                text_color = COL_BORDER
            cells.append((x, y, fill, text, text_color))
    svg_items = []
    for x, y, fill, text, text_color in cells:
        svg_items.append(
            f'<rect x="{x}" y="{y}" width="{cell_size}" height="{cell_size}" fill="{fill}" stroke="{COL_BORDER}"/>'
        )
        if text:
            svg_items.append(
                f'<text x="{x + cell_size / 2}" y="{y + cell_size / 2 + 4}" font-size="{cell_size // 2}" text-anchor="middle" fill="{text_color}">{text}</text>'
            )
    svg = f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}">'
    svg += "\n".join(svg_items) + "</svg>"
    return f'<html><head><meta charset="utf-8"><title>{escape(title)}</title></head><body><h3>{escape(title)}</h3>{svg}</body></html>'


def main():
    out = Path("artifacts")
    out.mkdir(exist_ok=True)
    for n in (5, 7, 9):
        # simulate menu: take family pattern and generate cards
        cards = make_cards(
            n, None, None
        )  # make_cards will fill all cells when pattern None
        # but menu uses patterns from get_figure_pattern via _regenerate_cards -> make_cards
        # instead, replicate: get pattern via card type A
        from src.core.card_figures import get_figure_pattern, get_card_type

        pattern = get_figure_pattern(get_card_type(1), is_main=True, dimension=n)
        cards = make_cards(n, pattern, None)
        main_card = cards["main"]
        cell_size = max(12, min(18, 140 // n))
        html = render_html(
            main_card, cell_size=cell_size, title=f"Menu preview main {n}x{n}"
        )
        (out / f"menu_preview_main_{n}.html").write_text(html, encoding="utf-8")
    print("Wrote artifacts/menu_preview_main_{n}.html for n=5,7,9")


if __name__ == "__main__":
    main()
