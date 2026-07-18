"""Ayudantes para la lógica de juego de la tombola (funcional, sin OOP).

Contiene funciones para crear la pila de números, extraer el siguiente número,
y verificar el ganador basándose en las figuras definidas.
"""

import random
from typing import Any, Container, Dict, List, Optional, Sequence, Set

from src.core.card import card_points
from src.core.card_figures import get_figure_pattern, is_figure_complete


def make_number_pool(dimension: int, numbers: Optional[Set[int]] = None) -> List[int]:
    """Crea y devuelve una lista barajada de números válida para el juego.

    Si se proporciona `numbers`, la pila se crea a partir de ese conjunto; de
    lo contrario se generan los números del 1 al N*N (donde N es `dimension`).
    La lista resultante está mezclada aleatoriamente para simular el bombo.

    Parámetros
    ----------
    dimension : int
        Dimensión N de la tarjeta (define el rango 1..N*N cuando `numbers` es
        `None`).
    numbers : Optional[Set[int]]
        Conjunto opcional de números a incluir en la pila.

    Devuelve
    -------
    List[int]
        Lista de números mezclados; usar `pop()` para extraer el siguiente número.
    """
    if numbers is None:
        pool = list(range(1, dimension * dimension + 1))
    else:
        pool = list(numbers)
    random.shuffle(pool)
    return pool


def draw_next(pool: List[int]) -> Optional[int]:
    """
    Extrae y devuelve el siguiente número de la pila, o `None` si está vacía.

    Ejemplo
    -------
    >>> pool = make_number_pool(2)
    >>> n = draw_next(pool)
    """
    if not pool:
        return None
    return pool.pop()


def check_winner(
    main_card: Sequence[Sequence[Optional[int]]],
    marked_main: Container[int],
    complement_card: Sequence[Sequence[Optional[int]]],
    marked_complement: Container[int],
    card_type: str,
) -> Optional[str]:
    """
    Determina si hay un ganador ('main' o 'complement') según el tipo de figura.

    Descripción
    ----------
    Obtiene los patrones de figura para la tarjeta principal y la complementaria
    y verifica si alguna de las dos está completa usando `is_figure_complete`.

    Devuelve
    -------
    Optional[str]
        'main' si la tarjeta principal completa la figura, 'complement' si la
        complementaria lo hace, o `None` si aún no hay ganador.
    """
    dimension = len(main_card)
    main_pattern = get_figure_pattern(card_type, is_main=True, dimension=dimension)
    complement_pattern = get_figure_pattern(
        card_type, is_main=False, dimension=dimension
    )
    if is_figure_complete(main_card, marked_main, main_pattern):
        return "main"
    if is_figure_complete(complement_card, marked_complement, complement_pattern):
        return "complement"
    return None


def game_summary(
    main_card: Sequence[Sequence[Optional[int]]],
    marked_main: Container[int],
    complement_card: Sequence[Sequence[Optional[int]]],
    marked_complement: Container[int],
    card_type: str,
) -> Dict[str, Any]:
    """
    Devuelve un resumen del estado actual del juego.

    El resumen incluye el posible ganador y los puntos de cada tarjeta.
    """
    winner = check_winner(
        main_card, marked_main, complement_card, marked_complement, card_type
    )
    main_points = card_points(main_card, marked_main)
    complement_points = card_points(complement_card, marked_complement)
    return {
        "winner": winner,
        "main_points": main_points,
        "complement_points": complement_points,
    }
