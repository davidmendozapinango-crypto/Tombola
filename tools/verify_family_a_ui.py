"""Verifica que la máscara usada en UI (cartón generado) coincide con el patrón
definido por la familia A vía `get_figure_pattern`.

Ejecutar desde la raíz del repo: `python tools/verify_family_a_ui.py`
"""

import sys

sys.path.insert(0, "")
from src.core.figures.families import familia_a
from src.core.card_figures import get_figure_pattern, get_card_type
from src.core.card import generate_card, make_cards


def compare(dimension: int, sdg_id: int = 1):
    card_type = get_card_type(sdg_id)
    family_pattern = get_figure_pattern(card_type, is_main=True, dimension=dimension)
    # generate cards as the app does
    cards = make_cards(dimension, family_pattern, None)
    main = cards["main"]
    # infer pattern from card (what UI uses for preview)
    ui_pattern = {
        (r, c)
        for r, row in enumerate(main)
        for c, val in enumerate(row)
        if val is not None
    }
    only_in_family = sorted(family_pattern - ui_pattern)
    only_in_ui = sorted(ui_pattern - family_pattern)
    print(f"Dimension={dimension}, sdg_id={sdg_id}, card_type={card_type}")
    print(
        f"family_pattern size={len(family_pattern)}, ui_pattern size={len(ui_pattern)}"
    )
    if not only_in_family and not only_in_ui:
        print("Patterns match exactly.")
    else:
        print("Differences found:")
        if only_in_family:
            print("  In family pattern but not in UI card:")
            for r, c in only_in_family:
                print(f"   ({r + 1},{c + 1})")
        if only_in_ui:
            print("  In UI card but not in family pattern:")
            for r, c in only_in_ui:
                print(f"   ({r + 1},{c + 1})")


if __name__ == "__main__":
    for n in (5, 7, 9):
        compare(n, sdg_id=1)
