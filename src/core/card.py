"""Funciones auxiliares para generación y evaluación de tarjetas.

Este módulo proporciona utilidades funcionales (sin programación orientada a
objetos) para crear tarjetas NxN, marcar números, y calcular sumas/puntos.
Las docstrings están en español y contienen explicaciones didácticas, ejemplos
y notas sobre complejidad para facilitar la comprensión a usuarios
principiantes.
"""

import random
from typing import Any, Container, Dict, List, Optional, Sequence, Set, Tuple


def generate_card(
    dimension: int, pattern: Optional[Set[Tuple[int, int]]] = None
) -> List[List[Optional[int]]]:
    """Genera una tarjeta de tamaño NxN.

    Si se proporciona `pattern` (conjunto de coordenadas (fila, columna)), sólo
    las celdas indicadas por el patrón recibirán números en el rango 1..N*N; las
    demás quedarán como `None`. Si `pattern` es `None` se rellena toda la
    cuadrícula con números aleatorios sin repetición (esto mantiene
    compatibilidad con demos y tests).

    Parámetros
    ----------
    dimension : int
        Tamaño N de la tarjeta (número de filas y columnas). Se asume N >= 1.
    pattern : Optional[Set[Tuple[int, int]]]
        Conjunto de coordenadas (fila, columna) que indican las celdas activas
        a numerar. Índices 0-based. Si es `None`, se numeran todas las celdas.

    Devuelve
    -------
    List[List[Optional[int]]]
        Grid NxN donde cada celda contiene un `int` si está numerada o `None`.

    Ejemplo
    -------
    >>> generate_card(2)
    [[2, 1], [4, 3]]

    Notas / Teoría
    ----------------
    - Se generan números del 1 al N*N y se barajan para asignarlos sin
      repetición.
    - Los patrones permiten construir "figuras" en la tarjeta dejando otras
      celdas vacías; son útiles para representar familias/plantillas.

    Complejidad
    ----------
    Tiempo: O(N^2)
    Espacio: O(N^2)
    """
    grid: List[List[Optional[int]]] = [
        [None for _ in range(dimension)] for _ in range(dimension)
    ]
    numbers = list(range(1, dimension * dimension + 1))
    random.shuffle(numbers)
    if pattern is None:
        index = 0
        for row in range(dimension):
            for col in range(dimension):
                grid[row][col] = numbers[index]
                index += 1
        return grid
    pattern_cells = list(pattern)
    for index, (row, col) in enumerate(pattern_cells):
        if 0 <= row < dimension and 0 <= col < dimension:
            grid[row][col] = numbers[index]
    return grid


def make_cards(
    dimension: int,
    main_pattern: Optional[Set[Tuple[int, int]]] = None,
    complement_pattern: Optional[Set[Tuple[int, int]]] = None,
) -> Dict[str, Any]:
    """
    Crea un par de tarjetas: 'main' y 'complement'.

    Descripción
    ----------
    Genera dos tarjetas aprovechando `generate_card`. Si se suministran
    patrones, solo las celdas del patrón serán numeradas; de lo contrario se
    rellenan todas las celdas.

    Devuelve
    -------
    Dict[str, Any]
        Diccionario con claves "main" y "complement" apuntando a las matrices
        correspondientes.
    """
    return {
        "main": generate_card(dimension, main_pattern),
        "complement": generate_card(dimension, complement_pattern),
    }


def card_sum(card: Sequence[Sequence[Optional[int]]]) -> int:
    """
    Calcula la suma de todas las celdas numeradas en una tarjeta.

    Ejemplo
    -------
    >>> card_sum([[1, None], [3, 4]])
    8

    Complejidad
    ----------
    Tiempo: O(N^2)
    Espacio: O(1)
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
    """
    Marca un número en la tarjeta si está presente; devuelve True si se encontró.

    Descripción
    ----------
    Recorre la tarjeta buscando `number`. Si existe, lo añade al conjunto
    `marked`. Devuelve un booleano indicando si la operación marcó algo.

    Parámetros
    ----------
    card : Sequence[Sequence[Optional[int]]]
        Tarjeta a revisar.
    marked : Set[int]
        Conjunto mutable donde se almacenan los números ya marcados.
    number : int
        Número a marcar.

    Devuelve
    -------
    bool
        True si el número estaba en la tarjeta y fue añadido a `marked`.

    Notas
    -----
    - `marked` se modifica in-place.
    - La búsqueda evita operaciones innecesarias tras encontrar el número.
    """
    found = False
    for row in card:
        if found:
            continue
        if number in row:
            found = True

    if found:
        marked.add(number)
    return found


def is_fully_marked(card: Sequence[Sequence[Optional[int]]], marked: Set[int]) -> bool:
    """
    Devuelve True si todas las celdas numeradas de la tarjeta están marcadas.

    Ejemplo
    -------
    >>> is_fully_marked([[1, None], [2, 3]], {1,2,3})
    True
    """
    for row in card:
        for value in row:
            if value is not None and value not in marked:
                return False
    return True


def card_points(card: Sequence[Sequence[Optional[int]]], marked: Container[int]) -> int:
    """
    Suma los valores de las celdas numeradas que están marcadas.

    Complejidad
    ----------
    Tiempo: O(N^2)
    """
    total = 0
    for row in card:
        for value in row:
            if value is not None and value in marked:
                total += value
    return total
