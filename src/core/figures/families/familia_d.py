"""Family D: outer two-layer frame generators

This family produces a two-layer outer border with the immediate
inner 1-layer hollowed out (for n=5 it matches the provided pattern).
Both mask and numbered generators are provided.
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
    for i in range(n):
        layer_i = min(i, n - 1 - i)
        for j in range(n):
            layer_j = min(j, n - 1 - j)
            if max(layer_i, layer_j) <= 1 and (not (layer_i == 1 and layer_j == 1)):
                mat[i, j] = 1
    return mat

def _mask_complement(n: int) -> 'np.ndarray':
    return _mask_main(n)

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
    return _assign_random_permutation_to_mask(_mask_complement(n), seed)

def mask_main(n: int) -> 'np.ndarray':
    import warnings
    warnings.warn('mask_main is deprecated; use generate_principal and derive mask from its output', DeprecationWarning)
    return (_assign_random_permutation_to_mask(_mask_main(n), seed=None) > 0).astype(int)

def mask_complement(n: int) -> 'np.ndarray':
    import warnings
    warnings.warn('mask_complement is deprecated; use generate_complementary and derive mask from its output', DeprecationWarning)
    return (_assign_random_permutation_to_mask(_mask_complement(n), seed=None) > 0).astype(int)