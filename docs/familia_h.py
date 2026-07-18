"""Family H: row-major symmetric-diagonals-without-center generators

Both principal and complementary figures are identical for Family H.
The figure fills the two diagonals except the central row (the center
cell is left empty). Traversal is row-by-row (row-major) and filled
cells receive consecutive integers starting at 1; empty cells are 0.
"""
from __future__ import annotations

import numpy as np


def _validate_n(n: int) -> None:
    if not isinstance(n, int):
        raise TypeError('n must be an integer')
    if n <= 0:
        raise ValueError('n must be positive')
    if n % 2 == 0:
        raise ValueError('n must be odd')

def generate_principal(n: int) -> np.ndarray:
    """Generate Family H principal figure with row-major numbering.

    Condition: fill when (j == i or j == n-1-i) and i != mid, where
    mid = n // 2. This produces the two diagonals but leaves the
    central row empty.
    """
    _validate_n(n)
    mat = np.zeros((n, n), dtype=int)
    mid = n // 2
    cont = 1
    for i in range(n):
        for j in range(n):
            if i != mid and (j == i or j == n - 1 - i):
                mat[i, j] = cont
                cont += 1
    return mat

def generate_complementary(n: int) -> np.ndarray:
    """Generate Family H complementary figure (identical to principal).

    Provided separately for API symmetry.
    """
    return generate_principal(n)
if __name__ == '__main__':
    import sys
    try:
        n = int(sys.argv[1]) if len(sys.argv) > 1 else 5
    except ValueError:
        n = 5
    print('Family H Principal ({}x{}):'.format(n, n))
    print(generate_principal(n))
    print()
    print('Family H Complementary ({}x{}):'.format(n, n))
    print(generate_complementary(n))