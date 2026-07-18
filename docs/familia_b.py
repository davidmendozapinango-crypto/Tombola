"""Family B: row-major contour generators

This module provides two separate functions that generate numbered
contour matrices for odd-sized square grids specific to Family B.
Both functions traverse the grid row-by-row (row-major) and assign
increasing integers starting at 1 to the cells that belong to the
figure. Empty cells are left as 0.

Design note: Family B principal figure corresponds to the column-based
pattern (the "complementary" figure from Family A). Family B
complementary corresponds to the row-based pattern (the "principal"
figure from Family A). Both are implemented independently and follow
the same validation and row-major traversal rules.
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
    """Generate Family B principal figure with row-major numbering.

    This principal figure fills vertical bands derived from column
    positions. For each column j compute left_col = min(j, n-1-j)
    and right_col = n-1-left_col. A cell (i, j) belongs to the figure
    when left_col <= i <= right_col. Numbers are assigned in
    row-major order starting at 1.
    """
    _validate_n(n)
    mat = np.zeros((n, n), dtype=int)
    cont = 1
    for i in range(n):
        for j in range(n):
            left_col = min(j, n - 1 - j)
            right_col = n - 1 - left_col
            if left_col <= i <= right_col:
                mat[i, j] = cont
                cont += 1
    return mat

def generate_complementary(n: int) -> np.ndarray:
    """Generate Family B complementary figure with row-major numbering.

    This complementary figure fills horizontal bands derived from row
    positions. For each row i compute left = min(i, n-1-i) and
    right = n-1-left. A cell (i, j) belongs to the figure when
    left <= j <= right. Numbers are assigned in row-major order
    starting at 1.
    """
    _validate_n(n)
    mat = np.zeros((n, n), dtype=int)
    cont = 1
    for i in range(n):
        left = min(i, n - 1 - i)
        right = n - 1 - left
        for j in range(n):
            if left <= j <= right:
                mat[i, j] = cont
                cont += 1
    return mat
if __name__ == '__main__':
    import sys
    try:
        n = int(sys.argv[1]) if len(sys.argv) > 1 else 5
    except ValueError:
        n = 5
    print('Family B Principal ({}x{}):'.format(n, n))
    print(generate_principal(n))
    print()
    print('Family B Complementary ({}x{}):'.format(n, n))
    print(generate_complementary(n))