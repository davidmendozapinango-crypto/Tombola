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
    """Obtener la letra de la familia de figura para un ID SDG dado.

    Args:
        sdg_id (int): Identificador del SDG.

    Devuelve:
        str: Letra que identifica la familia de figura (por defecto 'A').
    """
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
