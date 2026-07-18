"""
1.Elabore un programa, en Python, que rellene una matriz NxN (con N impar) con una secuencia de números,
comenzando en 1, y haciendo el recorrido mostrado en la siguiente figura:
"""
import numpy as np


def main():
    n = int(input('Introduzca tamaño de la matriz: '))
    while n % 2 == 0:
        n = int(input('Tamaño debe ser impar: '))
    matriz = np.zeros([n, n], dtype='int')
    cont = 1
    for i in range(0, n, 1):
        if i <= n // 2:
            for j in range(i, n - i, 1):
                matriz[i, j] = cont
                cont += 1
        else:
            for j in range(n - i - 1, i + 1, 1):
                matriz[i, j] = cont
                cont += 1
    print(matriz)
if __name__ == '__main__':
    main()