"""Ayudantes para la generación y manipulación de tarjetas (no orientado a objetos).

Descripción:
    Funciones para crear tarjetas NxN, marcar números, calcular puntos y
    obtener sumas. Están diseñadas para ser simples y fácilmente testeables.
"""

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
    """Generar una tarjeta NxN con o sin patrón.

    Descripción:
        Crea una matriz (lista de listas) de tamaño `dimension` x `dimension`.
        Si se proporciona `pattern`, sólo las celdas indicadas por el conjunto
        recibirán números; el resto quedará como `None`. Si `pattern` es None,
        se rellenan todas las celdas con números únicos entre 1 y dimension**2.

    Args:
        dimension (int): Tamaño N de la tarjeta (N x N).
        pattern (Optional[Set[Tuple[int, int]]]): Conjunto de coordenadas
            (fila, columna) que deben recibir números. Si es `None`, se
            rellenan todas las celdas.

    Returns:
        List[List[Optional[int]]]: Matriz de la tarjeta, con `None` en las
        celdas no numeradas.

    Notas/Teoría:
        - Se usan números únicos en la tarjeta generada cuando se rellena.
        - `random.shuffle` garantiza un orden aleatorio de los números.
        - No se valida que `pattern` esté dentro de los límites; se descartan
          coordenadas fuera del rango.

    Ejemplo:
        >>> generate_card(3)
        [[8, 1, 5], [3, 2, 9], [4, 6, 7]]  # ejemplo no determinista

    Complejidad:
        O(N) en tiempo y O(N) en espacio, con N = dimension**2.
    """
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
    """Crear un par de tarjetas: principal y complementaria.

    Descripción:
        Devuelve un diccionario con dos tarjetas generadas mediante
        `generate_card`. Si se proporcionan patrones, solo las celdas
        especificadas recibirán números.

    Args:
        dimension (int): Tamaño de las tarjetas.
        main_pattern (Optional[Set[Tuple[int, int]]]): Patrón para la tarjeta principal.
        complement_pattern (Optional[Set[Tuple[int, int]]]): Patrón para la tarjeta complementaria.

    Returns:
        Dict[str, Any]: Diccionario con claves "main" y "complement".
    """
    return {
        "main": generate_card(dimension, main_pattern),
        "complement": generate_card(dimension, complement_pattern),
    }


def card_sum(card: Sequence[Sequence[Optional[int]]]) -> int:
    """Calcular la suma de todos los valores numerados en una tarjeta.

    Args:
        card: Matriz de la tarjeta con enteros o `None` en celdas vacías.

    Devuelve:
        int: Suma de los valores presentes (ignora `None`).
    """
    total = 0
    for row in card:
        for value in row:
            if value is not None:
                total += value
    return total


def mark_number(
    card: Sequence[Sequence[Optional[int]]], marked: Set[int], number: int
) -> bool:
    """Marcar un número en la tarjeta si está presente.

    Descripción:
        Busca el `number` en la tarjeta; si se encuentra, lo añade al conjunto
        `marked` y devuelve True. Si no se encuentra, devuelve False.

    Args:
        card: Matriz de la tarjeta.
        marked: Conjunto mutable donde se almacenan los números ya marcados.
        number: Número a marcar.

    Returns:
        bool: True si el número estaba en la tarjeta y fue marcado; False si no.

    Notas:
        - La implementación evita el uso de `break` y, en su lugar, usa una
          bandera local `found` para indicar que el número fue hallado.
        - Complejidad: en el peor caso recorre todas las celdas -> O(N)
          con N = dimension**2. En promedio es O(N/2).
    """
    # Usar una bandera local para indicar si el número fue localizado en la
    # tarjeta. La implementación original usaba `break` para salir temprano;
    # aquí evitamos `break` comprobando `found` al inicio de cada iteración y
    # saltando trabajo adicional una vez que se descubre el número.
    found = False
    for row in card:
        if found:
            # Ya se encontró el número; saltar las filas restantes.
            continue
        if number in row:
            found = True

    if found:
        marked.add(number)
    return found


def is_fully_marked(card: Sequence[Sequence[Optional[int]]], marked: Set[int]) -> bool:
    """Comprobar si todas las celdas numeradas han sido marcadas.

    Devuelve:
        bool: True si no hay ninguna celda numerada que no esté en `marked`.
    """
    for row in card:
        for value in row:
            if value is not None and value not in marked:
                return False
    return True


def card_points(card: Sequence[Sequence[Optional[int]]], marked: Container[int]) -> int:
    """Calcular los puntos de la tarjeta sumando los números marcados.

    Args:
        card: Matriz de la tarjeta.
        marked: Contenedor (por ejemplo, set) con los números marcados.

    Devuelve:
        int: Suma de los valores que están presentes en `marked`.
    """
    total = 0
    for row in card:
        for value in row:
            if value is not None and value in marked:
                total += value
    return total
