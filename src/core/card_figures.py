"""Patrones de figuras de tarjetas y utilidades para extraer valores/ganadores.

Descripción:
    Este módulo centraliza las definiciones de las figuras (familias A..J) usadas
    por las tarjetas y ofrece ayudas para escalar patrones, obtener los valores
    que ocupan una figura en una tarjeta y comprobar si una figura está completa
    (todas sus celdas marcadas).

Notas/Teoría:
    - Las figuras se definen inicialmente en una rejilla de referencia 5x5 y
      luego se pueden escalar a dimensiones mayores mediante mapeo proporcional.
    - Para evitar mutaciones accidentales en patrones cacheados, `get_figure_pattern`
      devuelve un `frozenset` inmutable.

Formato:
    - Las coordenadas son tuplas (fila, columna) con índices base 0.
    - `SDG_TO_CARD_TYPE` mapea ids numéricos a letras de familia.
"""

from typing import (
    Any,
    Container,
    Dict,
    List,
    Optional,
    Sequence,
    Set,
    Tuple,
    AbstractSet,
)
from functools import lru_cache

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
    """Obtener la letra de la familia de figura para un ID SDG dado.

    Args:
        sdg_id (int): Identificador del SDG.

    Devuelve:
        str: Letra que identifica la familia de figura (por defecto 'A').
    """
    return SDG_TO_CARD_TYPE.get(sdg_id, "A")


def _scale_pattern(
    pattern: Set[Tuple[int, int]], dimension: int
) -> Set[Tuple[int, int]]:
    """Escalar un patrón de referencia 5x5 a la dimensión solicitada.

    Para tarjetas mayores que 5x5, cada celda destino se mapea a una celda
    fuente de la rejilla 5x5 mediante una proporción y redondeo. Si la celda
    fuente pertenece al patrón, la celda destino se incluye en el patrón
    escalado.
    """
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
    """Obtener el patrón de la figura escalada como un `frozenset` de coordenadas.

    Descripción:
        Calcula (y cachea) las celdas que componen la figura para la familia
        `card_type` y la variante `is_main` en una tarjeta de `dimension` x `dimension`.

    Args:
        card_type: Letra identificadora de la familia (por ejemplo, 'A').
        is_main: True para la figura principal, False para la complementaria.
        dimension: Tamaño de la tarjeta (por defecto 5).

    Devuelve:
        frozenset: Conjunto inmutable de tuplas (fila, columna) que forman la figura.

    Notas:
        - Se usa `frozenset` para garantizar que el patrón cacheado no sea
          modificado accidentalmente por el consumidor.
        - Para dimensiones mayores a 5, el patrón original se escala por
          mapeo proporcional; las celdas fuera de la tarjeta destino se ignoran.
    """
    key = "main" if is_main else "complement"
    base_pattern = _FIGURES.get(card_type, _FIGURES["A"])[key]
    return frozenset(_scale_pattern(base_pattern, dimension))


def is_figure_complete(
    card: Sequence[Sequence[Optional[int]]],
    marked: Container[int],
    pattern: AbstractSet[Tuple[int, int]],
) -> bool:
    """Verificar si todas las celdas posicionales de la figura están marcadas.

    Args:
        card: Tarjeta representada como matriz (lista de listas).
        marked: Contenedor de valores que han sido marcados.
        pattern: Conjunto (abstracto) de posiciones que definen la figura.

    Devuelve:
        bool: True si todas las posiciones del patrón apuntan a valores
              presentes en `marked`.
    """
    for row, col in pattern:
        if row >= len(card) or col >= len(card[row]):
            continue
        value = card[row][col]
        if value is None or value not in marked:
            return False
    return True


def get_figure_value_positions(
    card: Sequence[Sequence[Optional[int]]], pattern: AbstractSet[Tuple[int, int]]
) -> List[int]:
    """Obtener los valores numéricos de la tarjeta en las posiciones de la figura.

    Devuelve una lista de enteros que ocupan las celdas del `pattern`, ordenada
    por (fila, columna). Las celdas vacías (`None`) se omiten.

    Args:
        card: Matriz de la tarjeta con enteros o `None`.
        pattern: Conjunto de coordenadas que definen la figura.

    Devuelve:
        List[int]: Valores encontrados en las posiciones del patrón.
    """
    values: List[int] = []
    for row, col in sorted(pattern):
        if row < len(card) and col < len(card[row]):
            value = card[row][col]
            if value is not None:
                values.append(value)
    return values


def make_figure_preview(
    dimension: int, pattern: AbstractSet[Tuple[int, int]]
) -> List[List[Any]]:
    """Generar una vista previa de la figura en una cuadrícula de `dimension`.

    Las celdas pertenecientes al patrón se marcan con 'X' para facilitar la
    visualización en pruebas o herramientas de depuración.

    Args:
        dimension: Tamaño de la cuadrícula de salida.
        pattern: Conjunto de coordenadas de la figura.

    Devuelve:
        List[List[Any]]: Matriz donde 'X' indica celdas de la figura.
    """
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
