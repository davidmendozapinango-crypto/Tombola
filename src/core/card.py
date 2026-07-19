import random
from typing import Any, Container, Dict, List, Optional, Sequence, Set, Tuple

from src.core.R2_galeria_matrices import (
    diags_sin_centro,
    diagonales_espaciadas,
    esquinas,
    relojes_arena_A,
    relojes_arena_B,
    rombos,
    tornados,
    zeta_ene,
)

#funcion adaptada
def generate_card(
    dimension: int, pattern: Optional[Set[Tuple[int, int]]] = None, card_type: str = "A", is_main: bool = True
) -> List[List[Optional[int]]]:
    """Genera una tarjeta NxN colocando los números aleatorios en el orden exacto de la secuencia."""
    grid: List[List[Optional[int]]] = [
        [None for _ in range(dimension)] for _ in range(dimension)
    ]
    numbers = list(range(1, dimension * dimension + 1))
    random.shuffle(numbers)

    if pattern is None:
        index = 0
        for r in range(dimension):
            for c in range(dimension):
                grid[r][c] = numbers[index]
                index += 1
        return grid

    dicc_funciones = {"A": relojes_arena_A, "B": relojes_arena_B, "C": rombos, "D": esquinas, "E": tornados, "F": diagonales_espaciadas, "G": zeta_ene, "H": diags_sin_centro}
    
    funcion_matriz = dicc_funciones.get(card_type, relojes_arena_A)
    p, c = funcion_matriz(dimension)
    matriz_secuencia = p if is_main else c

    #Creacion una lista de celdas y las se ordena según el número de secuencia programado
    pattern_cells = list(pattern)
    pattern_cells.sort(key=lambda celda: matriz_secuencia[celda[0]][celda[1]])
    #Se colocan los números aleatorios respetando el orden de la secuencia
    for index, (row, col) in enumerate(pattern_cells):
        if 0 <= row < dimension and 0 <= col < dimension:
            grid[row][col] = numbers[index]
    return grid


def make_cards(
    dimension: int,
    main_pattern: Optional[Set[Tuple[int, int]]] = None,
    complement_pattern: Optional[Set[Tuple[int, int]]] = None,
) -> Dict[str, Any]:
    """Create a main and complement card pair.

    When patterns are supplied, only the figure cells are numbered. Otherwise the
    full grid is filled for compatibility with demos and legacy callers.
    """
    return {
        "main": generate_card(dimension, main_pattern),
        "complement": generate_card(dimension, complement_pattern),
    }


def card_sum(card: Sequence[Sequence[Optional[int]]]) -> int:
    """Return the sum of all numbered cells in a card."""
    total = 0
    for row in card:
        for value in row:
            if value is not None:
                total += value
    return total


def mark_number(
    card: Sequence[Sequence[Optional[int]]], marked: Set[int], number: int
) -> bool:
    """Mark a number on a card if present. Return True if found."""
    found = False
    for row in card:
        if number in row:
            found = True
            break
    if found:
        marked.add(number)
    return found


def is_fully_marked(card: Sequence[Sequence[Optional[int]]], marked: Set[int]) -> bool:
    """Return True when every numbered cell on the card has been marked."""
    for row in card:
        for value in row:
            if value is not None and value not in marked:
                return False
    return True


def card_points(card: Sequence[Sequence[Optional[int]]], marked: Container[int]) -> int:
    """Return the sum of marked numbered cells on a card."""
    total = 0
    for row in card:
        for value in row:
            if value is not None and value in marked:
                total += value
    return total
