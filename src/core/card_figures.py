"""SDG card figure definitions and winner detection helpers (non-OOP).

The project provides 8 card figure families (A-H). Each family has a main
figure (type 1) and a complement figure (type 2). The shapes below were
interpreted from the provided PNG assets in assets/images/ods/.

Coordinates are zero-indexed (row, col) for a 5x5 reference grid. The figures
are applied as-is to any dimension >= 5; cells outside the reference grid do
not belong to the figure.
"""

from typing import Any, Container, Dict, List, Optional, Sequence, Set, Tuple

_FIGURES: Dict[str, Dict[str, Set[Tuple[int, int]]]] = {
    "A": {
        "main": {
            (0, 0),
            (0, 1),
            (0, 2),
            (0, 3),
            (0, 4),
            (1, 1),
            (1, 2),
            (1, 3),
            (2, 2),
            (3, 1),
            (3, 2),
            (3, 3),
            (4, 0),
            (4, 1),
            (4, 2),
            (4, 3),
            (4, 4),
        },
        "complement": {
            (0, 0),
            (0, 4),
            (1, 0),
            (1, 1),
            (1, 3),
            (1, 4),
            (2, 0),
            (2, 1),
            (2, 2),
            (2, 3),
            (2, 4),
            (3, 0),
            (3, 1),
            (3, 3),
            (3, 4),
            (4, 0),
            (4, 4),
        },
    },
    "B": {
        "main": {
            (0, 0),
            (0, 4),
            (1, 0),
            (1, 1),
            (1, 3),
            (1, 4),
            (2, 0),
            (2, 1),
            (2, 2),
            (2, 3),
            (2, 4),
            (3, 0),
            (3, 1),
            (3, 3),
            (3, 4),
            (4, 0),
            (4, 4),
        },
        "complement": {
            (0, 0),
            (0, 1),
            (0, 2),
            (0, 3),
            (0, 4),
            (1, 1),
            (1, 2),
            (1, 3),
            (2, 2),
            (3, 1),
            (3, 2),
            (3, 3),
            (4, 0),
            (4, 1),
            (4, 2),
            (4, 3),
            (4, 4),
        },
    },
    "C": {
        "main": {
            (0, 2),
            (1, 1),
            (1, 2),
            (1, 3),
            (2, 0),
            (2, 1),
            (2, 2),
            (2, 3),
            (2, 4),
            (3, 1),
            (3, 2),
            (3, 3),
            (4, 2),
        },
        "complement": {
            (0, 2),
            (1, 1),
            (1, 2),
            (1, 3),
            (2, 0),
            (2, 1),
            (2, 2),
            (2, 3),
            (2, 4),
            (3, 1),
            (3, 2),
            (3, 3),
            (4, 2),
        },
    },
    "D": {
        "main": {
            (0, 0),
            (0, 1),
            (0, 3),
            (0, 4),
            (1, 0),
            (1, 4),
            (3, 0),
            (3, 4),
            (4, 0),
            (4, 1),
            (4, 3),
            (4, 4),
        },
        "complement": {
            (0, 0),
            (0, 1),
            (0, 3),
            (0, 4),
            (1, 0),
            (1, 4),
            (3, 0),
            (3, 4),
            (4, 0),
            (4, 1),
            (4, 3),
            (4, 4),
        },
    },
    "E": {
        "main": {
            (0, 0),
            (0, 2),
            (0, 4),
            (1, 1),
            (1, 3),
            (2, 0),
            (2, 2),
            (2, 4),
            (3, 1),
            (3, 3),
            (4, 0),
            (4, 2),
            (4, 4),
        },
        "complement": {
            (0, 0),
            (0, 2),
            (0, 4),
            (1, 1),
            (1, 3),
            (2, 0),
            (2, 2),
            (2, 4),
            (3, 1),
            (3, 3),
            (4, 0),
            (4, 2),
            (4, 4),
        },
    },
    "F": {
        "main": {
            (0, 0),
            (0, 2),
            (0, 4),
            (1, 1),
            (1, 3),
            (2, 0),
            (2, 2),
            (2, 4),
            (3, 1),
            (3, 3),
            (4, 0),
            (4, 2),
            (4, 4),
        },
        "complement": {
            (0, 0),
            (0, 2),
            (0, 4),
            (1, 1),
            (1, 3),
            (2, 0),
            (2, 2),
            (2, 4),
            (3, 1),
            (3, 3),
            (4, 0),
            (4, 2),
            (4, 4),
        },
    },
    "G": {
        "main": {
            (0, 0),
            (0, 1),
            (0, 2),
            (0, 3),
            (0, 4),
            (1, 3),
            (2, 2),
            (3, 1),
            (4, 0),
            (4, 1),
            (4, 2),
            (4, 3),
            (4, 4),
        },
        "complement": {
            (0, 0),
            (0, 4),
            (1, 0),
            (1, 3),
            (1, 4),
            (2, 0),
            (2, 2),
            (2, 4),
            (3, 0),
            (3, 1),
            (3, 4),
            (4, 0),
            (4, 4),
        },
    },
    "H": {
        "main": {
            (0, 0),
            (0, 4),
            (1, 1),
            (1, 3),
            (3, 1),
            (3, 3),
            (4, 0),
            (4, 4),
        },
        "complement": {
            (0, 0),
            (0, 4),
            (1, 1),
            (1, 3),
            (3, 1),
            (3, 3),
            (4, 0),
            (4, 4),
        },
    },
    "I": {
        "main": {
            (0, 0),
            (0, 4),
            (1, 0),
            (1, 4),
            (2, 0),
            (2, 4),
            (3, 0),
            (3, 4),
            (4, 0),
            (4, 1),
            (4, 2),
            (4, 3),
            (4, 4),
        },
        "complement": {
            (0, 0),
            (0, 1),
            (0, 2),
            (0, 3),
            (0, 4),
            (1, 0),
            (1, 4),
            (2, 0),
            (2, 4),
            (3, 0),
            (3, 4),
            (4, 0),
            (4, 4),
        },
    },
    "J": {
        "main": {
            (0, 0),
            (0, 1),
            (0, 2),
            (0, 3),
            (0, 4),
            (1, 0),
            (2, 0),
            (3, 0),
            (4, 0),
            (4, 1),
            (4, 2),
            (4, 3),
            (4, 4),
        },
        "complement": {
            (0, 0),
            (0, 1),
            (0, 2),
            (0, 3),
            (0, 4),
            (1, 4),
            (2, 4),
            (3, 4),
            (4, 0),
            (4, 1),
            (4, 2),
            (4, 3),
            (4, 4),
        },
    },
}

# Map each SDG to a figure family. The mapping is cyclic across the 17 SDGs.
SDG_TO_CARD_TYPE = {
    1: "A",
    2: "B",
    3: "C",
    4: "D",
    5: "E",
    6: "F",
    7: "G",
    8: "H",
    9: "I",
    10: "J",
    11: "A",
    12: "B",
    13: "C",
    14: "D",
    15: "E",
    16: "F",
    17: "G",
}


def get_card_type(sdg_id: int) -> str:
    """Return the figure family letter for the given SDG id."""
    return SDG_TO_CARD_TYPE.get(sdg_id, "A")


def _scale_pattern(
    pattern: Set[Tuple[int, int]], dimension: int
) -> Set[Tuple[int, int]]:
    """Scale a 5x5 reference pattern to the requested card dimension."""
    if dimension <= 5:
        return pattern
    scaled: Set[Tuple[int, int]] = set()
    max_index = dimension - 1
    for row, col in pattern:
        new_row = round(row * max_index / 4)
        new_col = round(col * max_index / 4)
        scaled.add((new_row, new_col))
    return scaled


def get_figure_pattern(
    card_type: str, is_main: bool, dimension: int = 5
) -> Set[Tuple[int, int]]:
    """Return the set of (row, col) cells that form the figure."""
    key = "main" if is_main else "complement"
    base_pattern = _FIGURES.get(card_type, _FIGURES["A"])[key]
    return _scale_pattern(base_pattern, dimension)


def is_figure_complete(
    card: Sequence[Sequence[Optional[int]]],
    marked: Container[int],
    pattern: Set[Tuple[int, int]],
) -> bool:
    """Return True when every positional cell of the figure is marked."""
    for row, col in pattern:
        if row >= len(card) or col >= len(card[row]):
            continue
        value = card[row][col]
        if value is None or value not in marked:
            return False
    return True


def get_figure_value_positions(
    card: Sequence[Sequence[Optional[int]]], pattern: Set[Tuple[int, int]]
) -> List[int]:
    """Return the list of card values that occupy the figure cells."""
    values: List[int] = []
    for row, col in sorted(pattern):
        if row < len(card) and col < len(card[row]):
            value = card[row][col]
            if value is not None:
                values.append(value)
    return values


def make_figure_preview(
    dimension: int, pattern: Set[Tuple[int, int]]
) -> List[List[Any]]:
    """Return a dimension x dimension grid with figure cells highlighted."""
    grid: List[List[Any]] = []
    for row in range(dimension):
        grid_row: List[Any] = []
        for col in range(dimension):
            if (row, col) in pattern:
                grid_row.append("X")
            else:
                grid_row.append("")
        grid.append(grid_row)
    return grid
