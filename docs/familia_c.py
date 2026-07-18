"""Family C: row-major diamond generators

This module provides two functions that generate the same diamond
figure for both principal and complementary roles. Both functions
traverse the grid row-by-row (row-major) and assign increasing
integers starting at 1 to the cells that belong to the diamond
centered on the matrix. Empty cells are left as 0.

Figure rule (diamond): let mid = n//2. A cell (i, j) belongs to the
figure when abs(i - mid) + abs(j - mid) <= mid.
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
    """Generate Family C principal diamond with row-major numbering.

    Traversal: row-by-row. The diamond is centered at (mid, mid) where
    mid = n // 2. A cell (i, j) belongs to the diamond if
    abs(i - mid) + abs(j - mid) <= mid. Numbers are assigned in
    row-major order starting at 1. Returns an (n,n) int NumPy array.
    """
    _validate_n(n)
    mat = np.zeros((n, n), dtype=int)
    mid = n // 2
    cont = 1
    for i in range(n):
        for j in range(n):
            if abs(i - mid) + abs(j - mid) <= mid:
                mat[i, j] = cont
                cont += 1
    return mat

def generate_complementary(n: int) -> np.ndarray:
    """Generate Family C complementary diamond with row-major numbering.

    This function produces the same diamond shape as the principal
    one; it is provided separately to keep API symmetry across families.
    """
    return generate_principal(n)
if __name__ == '__main__':
    import sys
    try:
        n = int(sys.argv[1]) if len(sys.argv) > 1 else 5
    except ValueError:
        n = 5
    print('Family C Principal ({}x{}):'.format(n, n))
    print(generate_principal(n))
    print()
    print('Family C Complementary ({}x{}):'.format(n, n))
    print(generate_complementary(n))