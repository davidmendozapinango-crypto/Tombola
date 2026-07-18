"""Family A: row-major contour generators

This module provides two separate functions that generate numbered
contour matrices for odd-sized square grids. Both functions traverse
the grid row-by-row (row-major) and assign increasing integers starting
at 1 to the cells that belong to the figure. Empty cells are left as 0.

Functions
- generate_principal(n): Numbers the "principal" figure by filling
  columns j that satisfy min(i, n-1-i) <= j <= n-1-min(i, n-1-i).
- generate_complementary(n): Numbers the "complementary" figure by
  filling rows i that satisfy min(j, n-1-j) <= i <= n-1-min(j, n-1-j).

Both functions require odd n >= 1 and return a NumPy int array.
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
    """Generate the principal figure with row-major numbered cells.

    Traversal: row-by-row. For each row i compute the left/right band
    boundaries as left = min(i, n-1-i) and right = n-1-left. A cell
    (i, j) is part of the figure when left <= j <= right. Numbers are
    assigned in the order the cells are visited (row-major) starting
    at 1.

    Returns an (n,n) int NumPy array where figure cells contain
    consecutive integers and other cells are 0.
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

def generate_complementary(n: int) -> np.ndarray:
    """Generate the complementary figure with row-major numbering.

    Traversal: row-by-row. This figure is the transpose-like counterpart
    of the principal figure. For each column j compute left_col =
    min(j, n-1-j) and right_col = n-1-left_col. A cell (i, j) is part
    of the figure when left_col <= i <= right_col. Numbers are assigned
    in row-major order starting at 1.

    Returns an (n,n) int NumPy array where figure cells contain
    consecutive integers and other cells are 0.
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
if __name__ == '__main__':
    import sys
    try:
        n = int(sys.argv[1]) if len(sys.argv) > 1 else 5
    except ValueError:
        n = 5
    print('Principal ({}x{}):'.format(n, n))
    print(generate_principal(n))
    print()
    print('Complementary ({}x{}):'.format(n, n))
    print(generate_complementary(n))