"""Family A: row-band (principal) and column-band (complement) masks

This module provides two APIs:
- mask_main(n) / mask_complement(n): return a binary mask (1 for
  filled cells, 0 otherwise) produced by row-major conditional tests.
- generate_principal(n, seed=None) / generate_complementary(n, seed=None):
  traverse row-by-row and assign a random unique permutation of
  integers 1..k to the filled positions (deterministic if seed given).

Both kinds of functions validate that n is an odd positive integer and
work for scalable sizes such as 5,7,9,11.
"""
from __future__ import annotations

import random

import numpy as np


def _validate_n(n: int) -> None:
    """Validate that n is a positive odd integer."""
    if not isinstance(n, int):
        raise TypeError('n must be an integer')
    if n <= 0:
        raise ValueError('n must be positive')
    if n % 2 == 0:
        raise ValueError('n must be odd')

def _mask_main(n: int) -> 'np.ndarray':
    """Private: compute binary mask for Family A principal (row-based).

    This helper is intentionally private: the public mask functions
    were removed by design. Use the numbered generators instead.
    """
    _validate_n(n)
    mat = np.zeros((n, n), dtype=int)
    for i in range(n):
        left = min(i, n - 1 - i)
        right = n - 1 - left
        for j in range(n):
            if left <= j <= right:
                mat[i, j] = 1
    return mat

def _mask_complement(n: int) -> 'np.ndarray':
    """Private: compute binary mask for Family A complementary (column-based)."""
    _validate_n(n)
    mat = np.zeros((n, n), dtype=int)
    for j in range(n):
        left_col = min(j, n - 1 - j)
        right_col = n - 1 - left_col
        for i in range(n):
            if left_col <= i <= right_col:
                mat[i, j] = 1
    return mat

def mask_main(n: int) -> 'np.ndarray':
    """Deprecated compatibility shim.

    This function derives the binary mask from the numbered generator
    and emits a DeprecationWarning. It is provided to ease migration
    but will be removed in a future release. Use
    `generate_principal(n)` instead.
    """
    import warnings
    warnings.warn('mask_main is deprecated; use generate_principal and derive mask from its output', DeprecationWarning)
    return (_assign_random_permutation_to_mask(_mask_main(n), seed=None) > 0).astype(int)

def mask_complement(n: int) -> 'np.ndarray':
    import warnings
    warnings.warn('mask_complement is deprecated; use generate_complementary and derive mask from its output', DeprecationWarning)
    return (_assign_random_permutation_to_mask(_mask_complement(n), seed=None) > 0).astype(int)

def _assign_random_permutation_to_mask(mask: 'np.ndarray', seed: int | None=None) -> 'np.ndarray':
    """Given a binary mask, return an int matrix with a random unique
    permutation of 1..k assigned to the 1 positions in row-major order.

    If seed is provided, the permutation is reproducible.
    """
    n = mask.shape[0]
    result = np.zeros_like(mask, dtype=int)
    positions = [(i, j) for i in range(n) for j in range(n) if mask[i, j] == 1]
    k = len(positions)
    nums = list(range(1, k + 1))
    rng = random.Random(seed)
    rng.shuffle(nums)
    for ((i, j), num) in zip(positions, nums):
        result[i, j] = num
    return result

def generate_principal(n: int, seed: int | None=None) -> 'np.ndarray':
    """Generate numbered principal figure for Family A.

    Produces an (n,n) integer array where filled positions receive a
    random unique number from 1..k assigned in row-major order (k is
    the number of filled cells). If seed is provided, numbering is
    deterministic.
    """
    _validate_n(n)
    mask = _mask_main(n)
    return _assign_random_permutation_to_mask(mask, seed)

def generate_complementary(n: int, seed: int | None=None) -> 'np.ndarray':
    """Generate numbered complementary figure for Family A."""
    _validate_n(n)
    mask = _mask_complement(n)
    return _assign_random_permutation_to_mask(mask, seed)