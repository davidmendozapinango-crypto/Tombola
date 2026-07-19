import numpy as np
from typing import Tuple


def fill_from_mask(
    mask: np.ndarray, order: str = "row", start: int = 1
) -> Tuple[np.ndarray, int]:
    """Rellenar una matriz numerada a partir de una máscara booleana.

    Dada una máscara (n x n) con valores booleanos o 0/1, asigna números
    consecutivos a las posiciones `True` siguiendo el orden indicado:
    por filas ('row'), por columnas ('col') o en recorrido en espiral
    ('spiral'). Devuelve la matriz numerada y el siguiente número libre.

    Args:
        mask: Matriz booleana o 0/1 que indica posiciones a llenar.
        order: 'row' | 'col' | 'spiral' que indica el orden de llenado.
        start: Número inicial a asignar.

    Returns:
        (matriz_numerada, next_start)

    Notas:
        - Normaliza la entrada a `numpy.array` para aceptar listas anidadas.
        - Levanta `ValueError` si `order` no es uno de los valores esperados.
    """
    # Aceptamos máscaras booleanas o matriciales; normalizamos a numpy array
    mask = np.array(mask)
    n = mask.shape[0]
    mat = np.zeros((n, n), dtype=int)
    cont = start
    if order == "row":
        for i in range(n):
            for j in range(n):
                if mask[i, j]:
                    mat[i, j] = cont
                    cont += 1
    elif order == "col":
        for j in range(n):
            for i in range(n):
                if mask[i, j]:
                    mat[i, j] = cont
                    cont += 1
    elif order == "spiral":
        (top, left) = (0, 0)
        (bottom, right) = (n - 1, n - 1)
        while top <= bottom and left <= right:
            for j in range(left, right + 1):
                i = top
                if mask[i, j] and mat[i, j] == 0:
                    mat[i, j] = cont
                    cont += 1
            top += 1
            for i in range(top, bottom + 1):
                j = right
                if mask[i, j] and mat[i, j] == 0:
                    mat[i, j] = cont
                    cont += 1
            right -= 1
            if top <= bottom:
                for j in range(right, left - 1, -1):
                    i = bottom
                    if mask[i, j] and mat[i, j] == 0:
                        mat[i, j] = cont
                        cont += 1
                bottom -= 1
            if left <= right:
                for i in range(bottom, top - 1, -1):
                    j = left
                    if mask[i, j] and mat[i, j] == 0:
                        mat[i, j] = cont
                        cont += 1
                left += 1
    else:
        raise ValueError("order must be 'row', 'col', or 'spiral'")
    return (mat, cont)
