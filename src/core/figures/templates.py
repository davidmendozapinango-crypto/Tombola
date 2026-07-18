"""Plantillas 5x5 para las familias (X = ocupado, . = vacio)"""
TEMPLATES = {'A': {'main': ['XXXXX', '.XXX.', '..X..', '.XXX.', 'XXXXX'], 'complement': ['X...X', 'XX.XX', 'XXXXX', 'XX.XX', 'X...X']}, 'B': {'main': ['X...X', 'XX.XX', 'XXXXX', 'XX.XX', 'X...X'], 'complement': ['XXXXX', '.XXX.', '..X..', '.XXX.', 'XXXXX']}, 'C': {'main': ['..X..', '.XXX.', 'XXXXX', '.XXX.', '..X..'], 'complement': ['..X..', '.XXX.', 'XXXXX', '.XXX.', '..X..']}, 'D': {'main': ['XX.XX', 'X...X', '.....', 'X...X', 'XX.XX'], 'complement': ['XX.XX', 'X...X', '.....', 'X...X', 'XX.XX']}, 'E': {'main': ['X.X.X', '.X.X.', 'X.X.X', '.X.X.', 'X.X.X'], 'complement': ['X.X.X', '.X.X.', 'X.X.X', '.X.X.', 'X.X.X']}, 'F': {'main': ['X.X.X', '.X.X.', 'X.X.X', '.X.X.', 'X.X.X'], 'complement': ['X.X.X', '.X.X.', 'X.X.X', '.X.X.', 'X.X.X']}, 'G': {'main': ['XXXXX', '...X.', '..X..', '.X...', 'XXXXX'], 'complement': ['X...X', 'X..XX', 'X.X.X', 'XX..X', 'X...X']}, 'H': {'main': ['X...X', '.X.X.', '.....', '.X.X.', 'X...X'], 'complement': ['X...X', '.X.X.', '.....', '.X.X.', 'X...X']}, 'I': {'main': ['X...X', 'X...X', 'X...X', 'X...X', 'XXXXX'], 'complement': ['XXXXX', 'X...X', 'X...X', 'X...X', 'X...X']}, 'J': {'main': ['XXXXX', 'X....', 'X....', 'X....', 'XXXXX'], 'complement': ['XXXXX', '....X', '....X', '....X', 'XXXXX']}}

def scale_template(template5, n):
    """Escala una plantilla 5x5 a tamaño n devolviendo máscara booleana n x n."""
    import numpy as np
    if n % 2 == 0:
        raise ValueError('n debe ser impar')
    if len(template5) != 5 or any((len(r) != 5 for r in template5)):
        raise ValueError('template5 debe ser 5x5')
    mask = np.zeros((n, n), dtype=bool)
    for i in range(n):
        i5 = i * 5 // n
        if i5 >= 5:
            i5 = 4
        for j in range(n):
            j5 = j * 5 // n
            if j5 >= 5:
                j5 = 4
            mask[i, j] = template5[i5][j5] == 'X'
    return mask