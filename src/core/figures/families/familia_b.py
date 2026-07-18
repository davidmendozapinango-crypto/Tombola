"""Family B: column-band (principal) and row-band (complement) masks

This module mirrors Family A but swaps the principal/complement
roles. It offers both binary mask functions and numbered generators
that assign a random permutation 1..k to filled positions.
"""
from __future__ import annotations
import random
import numpy as np

def _validate_n(n: int) -> None:
    if not isinstance(n, int):
        raise TypeError('n must be an integer')
    if n <= 0:
        raise ValueError('n must be positive')
    if n % 2 == 0:
        raise ValueError('n must be odd')

def _mask_main(n: int) -> 'np.ndarray':
    _validate_n(n)
    mat = np.zeros((n, n), dtype=int)
    for j in range(n):
        left_col = min(j, n - 1 - j)
        right_col = n - 1 - left_col
        for i in range(n):
            if left_col <= i <= right_col:
                mat[i, j] = 1
    return mat

def _mask_complement(n: int) -> 'np.ndarray':
    _validate_n(n)
    mat = np.zeros((n, n), dtype=int)
    for i in range(n):
        left = min(i, n - 1 - i)
        right = n - 1 - left
        for j in range(n):
            if left <= j <= right:
                mat[i, j] = 1
    return mat

def mask_main(n: int) -> 'np.ndarray':
    import warnings
    warnings.warn('mask_main is deprecated; use generate_principal and derive mask from its output', DeprecationWarning)
    return (_assign_random_permutation_to_mask(_mask_main(n), seed=None) > 0).astype(int)

def mask_complement(n: int) -> 'np.ndarray':
    import warnings
    warnings.warn('mask_complement is deprecated; use generate_complementary and derive mask from its output', DeprecationWarning)
    return (_assign_random_permutation_to_mask(_mask_complement(n), seed=None) > 0).astype(int)

def _assign_random_permutation_to_mask(mask: 'np.ndarray', seed: int | None=None) -> 'np.ndarray':
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
    _validate_n(n)
    mask = _mask_main(n)
    return _assign_random_permutation_to_mask(mask, seed)

def generate_complementary(n: int, seed: int | None=None) -> 'np.ndarray':
    _validate_n(n)
    mask = _mask_complement(n)
    return _assign_random_permutation_to_mask(mask, seed)