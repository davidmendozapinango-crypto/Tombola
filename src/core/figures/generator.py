from .utils import fill_from_mask


def generate_family_matrix(family_masks_module, n: int, which: str='main', order='row', start=1):
    """Genera la matriz numerada para una familia.

    - family_masks_module: módulo que expone `mask_main` y `mask_complement`.
    - which: 'main' o 'complement'
    - order: 'row'|'col'|'spiral'
    - start: número inicial
    """
    if which == 'main':
        if hasattr(family_masks_module, 'mask_main'):
            mask = (family_masks_module.generate_principal(n) > 0).astype(int)
        else:
            numbered = family_masks_module.generate_principal(n)
            mask = (numbered > 0).astype(int)
    elif hasattr(family_masks_module, 'mask_complement'):
        mask = (family_masks_module.generate_complementary(n) > 0).astype(int)
    else:
        numbered = family_masks_module.generate_complementary(n)
        mask = (numbered > 0).astype(int)
    (mat, next_start) = fill_from_mask(mask, order=order, start=start)
    return (mat, next_start)