"""Family I: row-major left-right border with full bottom/top row

Principal rule: fill the first and last columns (j == 0 or j == n-1)
and also fill the entire last row (i == n-1). This matches the
provided principal pattern where the bottom row is full and other rows
have only the two outer columns filled.

Complementary rule: fill the first row (i == 0) and the two outer
columns (j == 0 or j == n-1). This mirrors the principal figure with
the full row at the top instead of the bottom.

Both functions traverse the grid row-by-row (row-major) and assign
increasing integers starting at 1 to filled cells; empty cells are 0.
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
    """Generate Family I principal figure with row-major numbering.

    Condition: fill when j == 0 or j == n-1 or i == n-1.
    """
    _validate_n(n)
    mat = np.zeros((n, n), dtype=int)
    cont = 1
    for i in range(n):
        for j in range(n):
            if j == 0 or j == n - 1 or i == n - 1:
                mat[i, j] = cont
                cont += 1
    return mat

def generate_complementary(n: int) -> np.ndarray:
    """Generate Family I complementary figure with row-major numbering.

    Condition: fill when i == 0 or j == 0 or j == n-1.
    """
    _validate_n(n)
    mat = np.zeros((n, n), dtype=int)
    cont = 1
    for i in range(n):
        for j in range(n):
            if i == 0 or j == 0 or j == n - 1:
                mat[i, j] = cont
                cont += 1
    return mat
if __name__ == '__main__':
    import sys
    try:
        n = int(sys.argv[1]) if len(sys.argv) > 1 else 5
    except ValueError:
        n = 5
    print('Family I Principal ({}x{}):'.format(n, n))
    print(generate_principal(n))
    print()
    print('Family I Complementary ({}x{}):'.format(n, n))
    print(generate_complementary(n))