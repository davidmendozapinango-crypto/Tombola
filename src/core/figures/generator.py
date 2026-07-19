"""
Generador de matrices numeradas para familias de figuras.

Descripción:
  Este módulo exporta `generate_family_matrix` que, dado un módulo de
  familia (que implementa generadores de máscara/numerados), produce una
  matriz numerada según el orden solicitado (fila/columna/espiral).
"""

from .utils import fill_from_mask
import numpy as np


def generate_family_matrix(
    family_masks_module, n: int, which: str = "main", order: str = "row", start: int = 1
):
    """Generar la matriz numerada para una familia de figuras.

    Descripción:
        Usa el módulo de la familia (`family_masks_module`) para obtener una
        máscara o matriz numerada y luego la transforma en una matriz
        numerada siguiendo el `order` solicitado.

    Args:
        family_masks_module: Módulo que expone `generate_principal` y
            `generate_complementary` (u opcionalmente `mask_main`/`mask_complement`).
        n: Dimensión de la tarjeta (n x n).
        which: 'main' o 'complement' para elegir la figura.
        order: 'row' | 'col' | 'spiral' orden de numeración.
        start: Número inicial para la asignación.

    Returns:
        Tuple[np.ndarray, int]: Matriz numerada y siguiente número libre.
    """
    # Obtener la matriz entera numerada (con 0 en posiciones vacías) desde el módulo
    # de la familia. Algunos módulos exponen funciones históricas `mask_*` pero
    # la API preferida son `generate_principal` y `generate_complementary`.
    if which == "main":
        numbered = family_masks_module.generate_principal(n)
    else:
        numbered = family_masks_module.generate_complementary(n)

    # Convertir a máscara booleana: celdas con valor > 0 son ocupadas.
    mask = np.array(numbered) > 0

    # Delegar en la utilidad para rellenar números según el orden solicitado.
    (mat, next_start) = fill_from_mask(mask, order=order, start=start)
    return (mat, next_start)
