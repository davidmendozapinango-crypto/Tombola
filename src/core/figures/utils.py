import numpy as np
from typing import Tuple

def fill_from_mask(mask: np.ndarray, order: str='row', start: int=1) -> Tuple[np.ndarray, int]:
    """Rellena con numeros una matriz a partir de una máscara booleana.

    - mask: np.ndarray de tipo bool o 0/1 (n x n)
    - order: 'row' (por filas), 'col' (por columnas), o 'spiral' (recorrido en espiral)
    - start: numero inicial
    Devuelve (matriz_numerada, next_start)
    """
    n = mask.shape[0]
    mat = np.zeros((n, n), dtype=int)
    cont = start
    if order == 'row':
        for i in range(n):
            for j in range(n):
                if mask[i, j]:
                    mat[i, j] = cont
                    cont += 1
    elif order == 'col':
        for j in range(n):
            for i in range(n):
                if mask[i, j]:
                    mat[i, j] = cont
                    cont += 1
    elif order == 'spiral':
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