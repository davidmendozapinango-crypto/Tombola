"""Family E: row-major checkerboard generators

Both principal and complementary figures are identical: a checkerboard
pattern where cells with (i + j) % 2 == 0 are filled. Traversal is
row-by-row (row-major) and filled cells receive increasing integers
starting at 1; empty cells are 0.
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
    """Generate Family E principal checkerboard with row-major numbering.

    A cell (i, j) belongs to the figure when (i + j) % 2 == 0. Numbers
    are assigned in row-major order starting at 1.
    """
    _validate_n(n)
    mat = np.zeros((n, n), dtype=int)
    cont = 1
    for i in range(n):
        for j in range(n):
            if (i + j) % 2 == 0:
                mat[i, j] = cont
                cont += 1
    return mat

def generate_complementary(n: int) -> np.ndarray:
    """Generate Family E complementary figure (identical to principal).

    Kept separate for API symmetry.
    """
    return generate_principal(n)
if __name__ == '__main__':
    import sys
    try:
        n = int(sys.argv[1]) if len(sys.argv) > 1 else 5
    except ValueError:
        n = 5
    print('Family E Principal ({}x{}):'.format(n, n))
    print(generate_principal(n))
    print()
    print('Family E Complementary ({}x{}):'.format(n, n))
    print(generate_complementary(n))