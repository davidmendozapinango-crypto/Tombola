"""Ayudantes para la jugabilidad de la Tómbola (no orientado a objetos).

Descripción:
    Funciones utilitarias para crear y manipular la bolsa de números,
    comprobar ganadores y obtener un resumen del estado del juego.

Notas:
    - Estas funciones están diseñadas para ser sencillas y fáciles de probar.
    - No se altera la lógica del juego; sólo se añaden docstrings y
      comentarios explicativos en español.
"""

import random
from typing import Any, Container, Dict, List, Optional, Sequence, Set
from src.core.card import card_points
from src.core.card_figures import get_figure_pattern, is_figure_complete


def make_number_pool(dimension: int, numbers: Optional[Set[int]] = None) -> List[int]:
    """Crear una bolsa (lista) de números mezclada (aleatoria).

    Descripción:
        Genera y devuelve una lista de enteros que representa la bolsa de
        números que se sacarán en la tómbola. Si se proporciona `numbers`,
        únicamente se usará ese conjunto; en caso contrario se genera la
        secuencia completa desde 1 hasta dimension*dimension.

    Args:
        dimension (int): Tamaño de la tarjeta (por ejemplo 3 para 3x3).
        numbers (Optional[Set[int]]): Conjunto opcional de números a incluir.
            Si es `None`, se usan todos los números del rango 1..dimension**2.

    Returns:
        List[int]: Lista de números mezclada aleatoriamente. Se utiliza
        `random.shuffle`, por lo que el orden será impredecible.

    Notas/Teoría:
        - Complejidad temporal: O(N) para crear la lista (N=dimension**2),
          y O(N) en promedio para mezclar.
        - No se valida que `numbers` esté dentro del rango esperado;
          se asume que quien llama provee valores válidos.
    """
    if numbers is None:
        pool = list(range(1, dimension * dimension + 1))
    else:
        pool = list(numbers)
    random.shuffle(pool)
    return pool


def draw_next(pool: List[int]) -> Optional[int]:
    """Extrae y devuelve el siguiente número de la bolsa.

    Descripción:
        Pop del final de la lista `pool` para simular sacar un número.
        Si la bolsa está vacía devuelve `None`.

    Args:
        pool (List[int]): La bolsa de números (lista). Se modifica in-place
            (se extrae el último elemento).

    Returns:
        Optional[int]: El número extraído, o `None` si la bolsa estaba vacía.

    Notas:
        - Esta función modifica `pool` (efecto colateral intencional); si
          necesitas preservar la bolsa original, pásale una copia.
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
    """Comprueba si el patrón (figura) ganador está completo en alguna tarjeta.

    Descripción:
        Usa las funciones de `card_figures` para obtener el patrón esperado
        para el tipo de carta (`card_type`) y verifica si la figura está
        completa en la tarjeta principal o en la complementaria.

    Args:
        main_card: Matriz (secuencia de secuencias) con los números de la tarjeta principal.
        marked_main: Conjunto o contenedor de números ya marcados en la principal.
        complement_card: Tarjeta complementaria con la misma estructura.
        marked_complement: Conjunto de números marcados en la complementaria.
        card_type (str): Identificador del tipo de figura/partida a comprobar.

    Returns:
        Optional[str]: `'main'` si gana la tarjeta principal, `'complement'` si
        gana la complementaria, o `None` si no hay ganador aún.

    Notas/Teoría:
        - Dependencia: `get_figure_pattern` y `is_figure_complete`.
        - Se asume que `marked_main` y `marked_complement` contienen los números
          actualmente marcados (no índices). La verificación es set-based y rápida.
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
    """Devuelve un resumen del estado actual del juego.

    Descripción:
        Calcula si hay ganador y los puntos de cada tarjeta usando `card_points`.

    Args:
        main_card: Tarjeta principal (matriz de números).
        marked_main: Números marcados en la tarjeta principal.
        complement_card: Tarjeta complementaria.
        marked_complement: Números marcados en la complementaria.
        card_type: Tipo de carta para comprobar figuras.

    Returns:
        Dict[str, Any]: Diccionario con claves: 'winner', 'main_points', 'complement_points'.
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
