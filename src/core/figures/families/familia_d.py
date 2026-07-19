"""Familia D: generadores de marco exterior de dos capas.

Descripción:
    Produce una banda exterior de dos capas dejando hueca la capa
    inmediatamente interior (para n=5 coincide con la plantilla provista).
    Se ofrecen tanto generadores de máscara como generadores numerados.

Notas:
    - `n` debe ser impar para mantener simetría.
    - La máscara incluye las celdas de las dos capas exteriores excepto
      la capa interna inmediata cuando corresponde.
"""

from __future__ import annotations
import random
import numpy as np


def _validate_n(n: int) -> None:
    """Validar que `n` es un entero positivo e impar.

    Lanza `TypeError` o `ValueError` si la condición no se cumple.
    """
    if not isinstance(n, int):
        raise TypeError("n must be an integer")
    if n <= 0:
        raise ValueError("n must be positive")
    if n % 2 == 0:
        raise ValueError("n must be odd")


def _mask_main(n: int) -> "np.ndarray":
    """Calcular la máscara principal (dos capas exteriores).

    Devuelve una matriz binaria (0/1) donde las posiciones pertenecientes al
    marco exterior de dos capas valen 1, excepto la capa interna inmediata
    en las intersecciones que quedan huecas según la regla.
    """
    _validate_n(n)
    mat = np.zeros((n, n), dtype=int)
    for i in range(n):
        layer_i = min(i, n - 1 - i)
        for j in range(n):
            layer_j = min(j, n - 1 - j)
            # Incluir celdas cuya capa máxima sea 0 o 1, pero excluir la
            # intersección de la capa 1 con sí misma para crear el hueco.
            if max(layer_i, layer_j) <= 1 and (not (layer_i == 1 and layer_j == 1)):
                mat[i, j] = 1
    return mat


def _mask_complement(n: int) -> "np.ndarray":
    # Para esta familia la máscara complementaria coincide con la principal
    return _mask_main(n)


def _assign_random_permutation_to_mask(
    mask: "np.ndarray", seed: int | None = None
) -> "np.ndarray":
    """Asignar una permutación aleatoria 1..k a las posiciones con 1 en la máscara.

    Args:
        mask: Matriz binaria con 1 en posiciones a numerar.
        seed: Semilla opcional para reproducibilidad.

    Returns:
        np.ndarray: Matriz entera con números únicos en las posiciones ocupadas.
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
    """Generar matriz numerada para la figura principal de la Familia D.

    Si se suministra `seed` la asignación es determinista.
    """
    _validate_n(n)
    mask = _mask_main(n)
    return _assign_random_permutation_to_mask(mask, seed)


def generate_complementary(n: int, seed: int | None = None) -> "np.ndarray":
    """Generar matriz numerada para la figura complementaria de la Familia D."""
    _validate_n(n)
    return _assign_random_permutation_to_mask(_mask_complement(n), seed)


def mask_main(n: int) -> "np.ndarray":
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
