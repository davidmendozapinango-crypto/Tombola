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
#Eliminado scale_patters y variable FIGURES para reemplazar logica de generacion de matrices y patrones

def get_card_type(sdg_id: int) -> str:
    """Return the figure family letter for the given SDG id."""
    return SDG_TO_CARD_TYPE.get(sdg_id, "A")


def get_figure_pattern(
    card_type: str, is_main: bool, dimension: int = 5
) -> Set[Tuple[int, int]]:
    """Obtiene las coordenadas reales de la figura usando la lógica matemática de Albert."""
    #Llamamos a la función según la letra seleccionada
    if card_type == "A":
        p, c = relojes_arena_A(dimension)
    elif card_type == "B":
        p, c = relojes_arena_B(dimension)
    elif card_type == "C":
        p, c = rombos(dimension)
    elif card_type == "D":
        p, c = esquinas(dimension)
    elif card_type == "E":
        p, c = tornados(dimension)
    elif card_type == "F":
        p, c = diagonales_espaciadas(dimension)
    elif card_type == "G":
        p, c = zeta_ene(dimension)
    elif card_type == "H":
        p, c = diags_sin_centro(dimension)
    else:
        p, c = relojes_arena_A(dimension)
        
    # Seleccionamos la matriz principal y/o complmento
    matriz_elegida = p if is_main else c
    
    #Extraemos las coordenadas (fila, columna) donde el patrón no sea cero
    pattern: Set[Tuple[int, int]] = set()
    for r in range(dimension):
        for col in range(dimension):
            if matriz_elegida[r][col] != 0:
                pattern.add((r, col))       
    return pattern


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
