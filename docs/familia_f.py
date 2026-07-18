"""Family F: same as Family E (checkerboard)

Family F uses the same checkerboard rule as Family E. Both principal
and complementary functions are provided for API symmetry and both
use row-major numbering with filled cells numbered consecutively and
empty cells set to 0.
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
    return generate_principal(n)
if __name__ == '__main__':
    import sys
    try:
        n = int(sys.argv[1]) if len(sys.argv) > 1 else 5
    except ValueError:
        n = 5
    print('Family F Principal ({}x{}):'.format(n, n))
    print(generate_principal(n))
    print()
    print('Family F Complementary ({}x{}):'.format(n, n))
    print(generate_complementary(n))