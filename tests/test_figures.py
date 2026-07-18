import unittest
import numpy as np
from src.core.figures import fill_from_mask
from src.core.figures.families import familia_a, familia_b

class TestFigures(unittest.TestCase):

    def test_familia_a_5(self):
        mask = (familia_a.generate_principal(5, seed=0) > 0).astype(int)
        (mat, _) = fill_from_mask(mask, order='row', start=1)
        self.assertEqual(mat[2, 2], 9)

    def test_familia_b_5_col_order(self):
        mask = (familia_b.generate_principal(5, seed=0) > 0).astype(int)
        (mat, _) = fill_from_mask(mask, order='col', start=1)
        self.assertTrue(mat[0, 0] == 1 or mat[0, 0] == 0)
if __name__ == '__main__':
    unittest.main()