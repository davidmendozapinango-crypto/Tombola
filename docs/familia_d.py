"""Family D: row-major outer-two-layer frame generators

Both principal and complementary figures are identical for Family D.
The shape is an outer two-layer frame where the second layer's inner
cells are removed (for n=5 this matches the provided pattern).

Rule used (scales to odd n): compute layer index for row/col as
layer = min(index, n-1-index). A cell (i,j) is filled when
max(layer_i, layer_j) <= 1 and not (layer_i == 1 and layer_j == 1).
This produces the 2-layer border with the inner 1-layer square empty.

Traversal is row-major; numbered cells increase in visit order starting
at 1. Empty cells are 0.
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
    """Generate Family D principal figure with row-major numbering.

    The figure is the same as the complementary one for Family D; it
    is implemented with the two-layer frame rule described in the
    module docstring.
    """
    _validate_n(n)
    mat = np.zeros((n, n), dtype=int)
    cont = 1
    for i in range(n):
        layer_i = min(i, n - 1 - i)
        for j in range(n):
            layer_j = min(j, n - 1 - j)
            if max(layer_i, layer_j) <= 1 and (not (layer_i == 1 and layer_j == 1)):
                mat[i, j] = cont
                cont += 1
    return mat

def generate_complementary(n: int) -> np.ndarray:
    """Generate Family D complementary figure (identical to principal).

    Kept separate for API symmetry; reuse the principal implementation.
    """
    return generate_principal(n)
if __name__ == '__main__':
    import sys
    try:
        n = int(sys.argv[1]) if len(sys.argv) > 1 else 5
    except ValueError:
        n = 5
    print('Family D Principal ({}x{}):'.format(n, n))
    print(generate_principal(n))
    print()
    print('Family D Complementary ({}x{}):'.format(n, n))
    print(generate_complementary(n))