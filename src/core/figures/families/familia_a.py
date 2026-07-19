"""Familia A: banda por filas (principal) y banda por columnas (complemento).

Descripción:
    Implementa generadores de máscaras y matrices numeradas para la familia A.
    La figura principal es una banda centrada por filas (un "diamante" horizontal)
    y la complementaria es la versión por columnas.

API:
    - `generate_principal(n, seed=None)` / `generate_complementary(n, seed=None)`:
        Devuelven una matriz (n x n) con una permutación única de 1..k asignada
        a las posiciones ocupadas. Si se pasa `seed`, la asignación es
        determinista para reproducibilidad en tests.
    - Las funciones `mask_main` y `mask_complement` existen por compatibilidad
      y emiten `DeprecationWarning`. Preferir los generadores numerados.

Notas/Teoría:
    - n debe ser entero impar para preservar simetría.
    - El generador asigna números a las posiciones ocupadas en orden fila-major
      después de calcular la máscara.
"""

from __future__ import annotations
import random
import numpy as np


def _validate_n(n: int) -> None:
    """Validar que `n` es un entero positivo e impar.

    Lanza `TypeError` o `ValueError` si no se cumple la precondición.
    """
    if not isinstance(n, int):
        raise TypeError("n must be an integer")
    if n <= 0:
        raise ValueError("n must be positive")
    if n % 2 == 0:
        raise ValueError("n must be odd")


def _mask_main(n: int) -> "np.ndarray":
    """Calcular la máscara binaria de la figura principal (banda por filas).

    Esta función es privada; los consumidores deben preferir
    `generate_principal` que devuelve la matriz numerada.
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


def _mask_complement(n: int) -> "np.ndarray":
    """Calcular la máscara binaria complementaria (banda por columnas)."""
    _validate_n(n)
    mat = np.zeros((n, n), dtype=int)
    for j in range(n):
        left_col = min(j, n - 1 - j)
        right_col = n - 1 - left_col
        for i in range(n):
            if left_col <= i <= right_col:
                mat[i, j] = 1
    return mat


def mask_main(n: int) -> "np.ndarray":
    """Shim de compatibilidad (Deprecated).

    Emite `DeprecationWarning`. Mantener solo para migración de API.
    """
    import warnings

    warnings.warn(
        "mask_main is deprecated; use generate_principal and derive mask from its output",
        DeprecationWarning,
    )
    return (_assign_random_permutation_to_mask(_mask_main(n), seed=None) > 0).astype(
        int
    )


def mask_complement(n: int) -> "np.ndarray":
    import warnings

    warnings.warn(
        "mask_complement is deprecated; use generate_complementary and derive mask from its output",
        DeprecationWarning,
    )
    return (
        _assign_random_permutation_to_mask(_mask_complement(n), seed=None) > 0
    ).astype(int)


def _assign_random_permutation_to_mask(
    mask: "np.ndarray", seed: int | None = None
) -> "np.ndarray":
    """Dada una máscara binaria, asignar una permutación aleatoria 1..k.

    Args:
        mask: Matriz binaria con 1 en posiciones a numerar.
        seed: Semilla opcional para reproducibilidad.

    Returns:
        np.ndarray: Matriz entera donde las posiciones ocupadas contienen
        una permutación única de 1..k.
    """
    n = mask.shape[0]
    result = np.zeros_like(mask, dtype=int)
    positions = [(i, j) for i in range(n) for j in range(n) if mask[i, j] == 1]
    k = len(positions)
    nums = list(range(1, k + 1))
    rng = random.Random(seed)
    rng.shuffle(nums)
    for (i, j), num in zip(positions, nums):
        result[i, j] = num
    return result


def generate_principal(n: int, seed: int | None = None) -> "np.ndarray":
    """Generar figura principal numerada para la Familia A.

    Devuelve una matriz entera (n x n) con números únicos 1..k en las
    posiciones ocupadas. Si se suministra `seed`, la asignación es
    determinista para facilitar pruebas.
    """
    _validate_n(n)
    mask = _mask_main(n)
    return _assign_random_permutation_to_mask(mask, seed)


def generate_complementary(n: int, seed: int | None = None) -> "np.ndarray":
    """Generar figura complementaria numerada para la Familia A."""
    _validate_n(n)
    mask = _mask_complement(n)
    return _assign_random_permutation_to_mask(mask, seed)
