"""Generador rápido de vistas previas HTML para Familia A.

Este script crea archivos HTML con SVG que muestran la máscara y los
valores numerados para las dimensiones 5,7,9 usando la implementación
actual en `src.core.figures.families.familia_a`.

No requiere dependencias externas y puede abrirse en un navegador.
"""

from pathlib import Path
from html import escape
import sys

sys.path.insert(0, "")
from src.core.figures.families import familia_a


def render_svg(matrix, cell=30, show_numbers=True):
    n = matrix.shape[0]
    width = n * cell
    height = n * cell
    rects = []
    texts = []
    for i in range(n):
        for j in range(n):
            x = j * cell
            y = i * cell
            if int(matrix[i, j]) > 0:
                rects.append(
                    f'<rect x="{x}" y="{y}" width="{cell}" height="{cell}" fill="#333"/>'
                )
                if show_numbers:
                    texts.append(
                        f'<text x="{x + cell / 2}" y="{y + cell / 2 + 4}" font-size="{cell // 3}" text-anchor="middle" fill="#fff">{int(matrix[i, j])}</text>'
                    )
            else:
                rects.append(
                    f'<rect x="{x}" y="{y}" width="{cell}" height="{cell}" fill="#fff" stroke="#ccc"/>'
                )
    svg = f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">'
    svg += "".join(rects) + "".join(texts) + "</svg>"
    return svg


def make_html(title, svg):
    return f"""
<html>
  <head>
    <meta charset="utf-8">
    <title>{escape(title)}</title>
  </head>
  <body>
    <h2>{escape(title)}</h2>
    {svg}
  </body>
</html>
"""


def main():
    out = Path("artifacts")
    out.mkdir(exist_ok=True)
    for n in (5, 7, 9):
        main = familia_a.generate_principal(n, seed=0)
        comp = familia_a.generate_complementary(n, seed=0)
        svg_main = render_svg(main, cell=28, show_numbers=True)
        svg_comp = render_svg(comp, cell=28, show_numbers=True)
        (out / f"familia_a_main_{n}.html").write_text(
            make_html(f"Familia A principal {n}x{n}", svg_main), encoding="utf-8"
        )
        (out / f"familia_a_comp_{n}.html").write_text(
            make_html(f"Familia A complementario {n}x{n}", svg_comp), encoding="utf-8"
        )
    print("Previews written to artifacts/*.html")


if __name__ == "__main__":
    main()
