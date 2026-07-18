"""Definiciones de figuras de tarjetas SDG y ayudantes de detección de ganadores (no OOP).

El proyecto proporciona 8 familias de figuras de cartas (AH). Cada familia tiene una familia principal
figura (tipo 1) y figura complementaria (tipo 2). Las formas a continuación fueron
interpretado a partir de los activos PNG proporcionados en assets/images/ods/.

Las coordenadas tienen índice cero (fila, columna) para una cuadrícula de referencia de 5x5. Las cifras
se aplican tal cual a cualquier dimensión >= 5; las celdas fuera de la cuadrícula de referencia lo hacen
no pertenecen a la figura.
"""

from functools import lru_cache
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
        "main": {(0, 0), (0, 4), (1, 1), (1, 3), (3, 1), (3, 3), (4, 0), (4, 4)},
        "complement": {(0, 0), (0, 4), (1, 1), (1, 3), (3, 1), (3, 3), (4, 0), (4, 4)},
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
    """Devuelve la letra de la familia de figura para un `sdg_id` dado.

    Nota: Mantiene compatibilidad devolviendo 'A' si `sdg_id` no está mapeado.
    """
    return SDG_TO_CARD_TYPE.get(sdg_id, "A")


def _scale_pattern(
    pattern: Set[Tuple[int, int]], dimension: int
) -> Set[Tuple[int, int]]:
    """Escala un patrón de referencia 5x5 a la dimensión de tarjeta solicitada."""
    if dimension <= 5:
        return set(pattern)
    scaled: Set[Tuple[int, int]] = set()
    max_index = dimension - 1
    for t_row in range(dimension):
        src_row = round(t_row * 4 / max_index)
        for t_col in range(dimension):
            src_col = round(t_col * 4 / max_index)
            if (src_row, src_col) in pattern:
                scaled.add((t_row, t_col))
    return scaled


@lru_cache(maxsize=256)
def get_figure_pattern(card_type: str, is_main: bool, dimension: int = 5):
    """Devuelve las celdas (fila, columna) que forman la figura.

    El resultado se cachea y se devuelve como `frozenset` inmutable para
    evitar mutaciones accidentales del valor cacheado.
    """
    key = "main" if is_main else "complement"
    base_pattern = _FIGURES.get(card_type, _FIGURES["A"])[key]
    return frozenset(_scale_pattern(base_pattern, dimension))


def is_figure_complete(
    card: Sequence[Sequence[Optional[int]]],
    marked: Container[int],
    pattern: Set[Tuple[int, int]],
) -> bool:
    """Devuelve True cuando cada celda posicional de la figura está marcada."""
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
    """Devuelve la lista de valores de la tarjeta que ocupan las celdas de la figura."""
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
    """Devuelve una cuadrícula dimensión x dimensión con las celdas de la figura resaltadas."""
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
