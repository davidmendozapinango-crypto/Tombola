"""Family G: row-major principal and complementary figures

Principal rule (scales to odd n): fill the entire first and last
rows, and additionally fill the anti-diagonal (j == n-1-i).

Complementary rule: fill the entire first and last columns (j == 0
or j == n-1) and also fill the anti-diagonal (j == n-1-i).

Both functions traverse row-by-row (row-major) and assign increasing
integers starting at 1 to filled cells; empty cells are 0.
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
    """Generate Family G principal figure with row-major numbering.

    Condition: fill when i == 0 or i == n-1 or j == n-1-i.
    """
    _validate_n(n)
    mat = np.zeros((n, n), dtype=int)
    cont = 1
    for i in range(n):
        for j in range(n):
            if i == 0 or i == n - 1 or j == n - 1 - i:
                mat[i, j] = cont
                cont += 1
    return mat

def generate_complementary(n: int) -> np.ndarray:
    """Generate Family G complementary figure with row-major numbering.

    Condition: fill when j == 0 or j == n-1 or j == n-1-i.
    """
    _validate_n(n)
    mat = np.zeros((n, n), dtype=int)
    cont = 1
    for i in range(n):
        for j in range(n):
            if j == 0 or j == n - 1 or j == n - 1 - i:
                mat[i, j] = cont
                cont += 1
    return mat
if __name__ == '__main__':
    import sys
    try:
        n = int(sys.argv[1]) if len(sys.argv) > 1 else 5
    except ValueError:
        n = 5
    print('Family G Principal ({}x{}):'.format(n, n))
    print(generate_principal(n))
    print()
    print('Family G Complementary ({}x{}):'.format(n, n))
    print(generate_complementary(n))