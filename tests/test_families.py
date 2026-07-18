import numpy as np

import src.core.figures.families as families


def as_arr(list_of_lists):
    return np.array(list_of_lists, dtype=int)
EXPECTED_MASKS = {'a_main': as_arr([[1, 1, 1, 1, 1], [0, 1, 1, 1, 0], [0, 0, 1, 0, 0], [0, 1, 1, 1, 0], [1, 1, 1, 1, 1]]), 'a_complement': as_arr([[1, 0, 0, 0, 1], [1, 1, 0, 1, 1], [1, 1, 1, 1, 1], [1, 1, 0, 1, 1], [1, 0, 0, 0, 1]]), 'b_main': as_arr([[1, 0, 0, 0, 1], [1, 1, 0, 1, 1], [1, 1, 1, 1, 1], [1, 1, 0, 1, 1], [1, 0, 0, 0, 1]]), 'b_complement': as_arr([[1, 1, 1, 1, 1], [0, 1, 1, 1, 0], [0, 0, 1, 0, 0], [0, 1, 1, 1, 0], [1, 1, 1, 1, 1]]), 'c_main': as_arr([[0, 0, 1, 0, 0], [0, 1, 1, 1, 0], [1, 1, 1, 1, 1], [0, 1, 1, 1, 0], [0, 0, 1, 0, 0]]), 'd_main': as_arr([[1, 1, 0, 1, 1], [1, 0, 0, 0, 1], [0, 0, 0, 0, 0], [1, 0, 0, 0, 1], [1, 1, 0, 1, 1]]), 'e_main': as_arr([[1, 0, 1, 0, 1], [0, 1, 0, 1, 0], [1, 0, 1, 0, 1], [0, 1, 0, 1, 0], [1, 0, 1, 0, 1]]), 'f_main': as_arr([[1, 0, 1, 0, 1], [0, 1, 0, 1, 0], [1, 0, 1, 0, 1], [0, 1, 0, 1, 0], [1, 0, 1, 0, 1]]), 'g_main': as_arr([[1, 1, 1, 1, 1], [0, 0, 0, 1, 0], [0, 0, 1, 0, 0], [0, 1, 0, 0, 0], [1, 1, 1, 1, 1]]), 'g_complement': as_arr([[1, 0, 0, 0, 1], [1, 0, 0, 1, 1], [1, 0, 1, 0, 1], [1, 1, 0, 0, 1], [1, 0, 0, 0, 1]]), 'h_main': as_arr([[1, 0, 0, 0, 1], [0, 1, 0, 1, 0], [0, 0, 0, 0, 0], [0, 1, 0, 1, 0], [1, 0, 0, 0, 1]]), 'i_main': as_arr([[1, 0, 0, 0, 1], [1, 0, 0, 0, 1], [1, 0, 0, 0, 1], [1, 0, 0, 0, 1], [1, 1, 1, 1, 1]]), 'i_complement': as_arr([[1, 1, 1, 1, 1], [1, 0, 0, 0, 1], [1, 0, 0, 0, 1], [1, 0, 0, 0, 1], [1, 0, 0, 0, 1]]), 'j_main': as_arr([[1, 1, 1, 1, 1], [1, 0, 0, 0, 0], [1, 0, 0, 0, 0], [1, 0, 0, 0, 0], [1, 1, 1, 1, 1]]), 'j_complement': as_arr([[1, 1, 1, 1, 1], [0, 0, 0, 0, 1], [0, 0, 0, 0, 1], [0, 0, 0, 0, 1], [1, 1, 1, 1, 1]])}

def test_masks_n5():
    assert np.array_equal((families.familia_a_generate_principal(5) > 0).astype(int), EXPECTED_MASKS['a_main'])
    assert np.array_equal((families.familia_a_generate_complementary(5) > 0).astype(int), EXPECTED_MASKS['a_complement'])
    assert np.array_equal((families.familia_b_generate_principal(5) > 0).astype(int), EXPECTED_MASKS['b_main'])
    assert np.array_equal((families.familia_b_generate_complementary(5) > 0).astype(int), EXPECTED_MASKS['b_complement'])
    assert np.array_equal((families.familia_c_generate_principal(5) > 0).astype(int), EXPECTED_MASKS['c_main'])
    assert np.array_equal((families.familia_d_generate_principal(5) > 0).astype(int), EXPECTED_MASKS['d_main'])
    assert np.array_equal((families.familia_e_generate_principal(5) > 0).astype(int), EXPECTED_MASKS['e_main'])
    assert np.array_equal((families.familia_f_generate_principal(5) > 0).astype(int), EXPECTED_MASKS['f_main'])
    assert np.array_equal((families.familia_g_generate_principal(5) > 0).astype(int), EXPECTED_MASKS['g_main'])
    assert np.array_equal((families.familia_g_generate_complementary(5) > 0).astype(int), EXPECTED_MASKS['g_complement'])
    assert np.array_equal((families.familia_h_generate_principal(5) > 0).astype(int), EXPECTED_MASKS['h_main'])
    assert np.array_equal((families.familia_i_generate_principal(5) > 0).astype(int), EXPECTED_MASKS['i_main'])
    assert np.array_equal((families.familia_i_generate_complementary(5) > 0).astype(int), EXPECTED_MASKS['i_complement'])
    assert np.array_equal((families.familia_j_generate_principal(5) > 0).astype(int), EXPECTED_MASKS['j_main'])
    assert np.array_equal((families.familia_j_generate_complementary(5) > 0).astype(int), EXPECTED_MASKS['j_complement'])

def assert_is_permutation_of_1_to_k(arr, mask):
    vals = arr[mask == 1]
    k = mask.sum()
    assert len(vals) == k
    assert set(vals.tolist()) == set(range(1, k + 1))

def test_generate_returns_permutation_n5():
    seed = 12345
    for name in ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j']:
        gen_main = getattr(families, f'familia_{name}_generate_principal')
        gen_comp = getattr(families, f'familia_{name}_generate_complementary')
        mask_main = (gen_main(5, seed=0) > 0).astype(int)
        mask_comp = (gen_comp(5, seed=0) > 0).astype(int)
        arr_main = gen_main(5, seed=seed)
        arr_comp = gen_comp(5, seed=seed)
        assert_is_permutation_of_1_to_k(arr_main, mask_main)
        assert_is_permutation_of_1_to_k(arr_comp, mask_comp)