import numpy as np #Parte de: Albert
            
#Llenado & Patrones de las Parejas de Matrices
def relojes_arena_A(N):
    #---------------------------------- RELOJES DE ARENA (A) ----------------------------------
    #Llenado por filas de anajo a arriba de izq a der
    "A1 - Fin Pobreza"
    reloj_fil = np.zeros((N, N), dtype = "int")
    cont = 1
    centro = N//2
    for i in range(N-1,-1,-1):
        for j in range(N-1,-1,-1):
            if i <= centro and j >= i and j <= N-i-1:
                reloj_fil[i][j] = cont
                cont += 1
            elif i >= centro and j <= i and j >= N-i-1:
                reloj_fil[i][j] = cont
                cont += 1
    
    #Llenado de reloj por columnas inverso de abajo a arriba de der a izq
    "A2 - Hambre Cero"
    reloj_col_inv = np.zeros((N, N), dtype = "int")
    cont = 1
    for j in range(N-1,-1,-1):
        for i in range(N-1,-1,-1):
            if (j <= centro) and (i >= j) and (j <= N-1-i):
                reloj_col_inv[i, j] = cont
                cont += 1
            elif (j >= centro) and (j >= i) and (j >= N-i-1):
                reloj_col_inv[i, j] = cont
                cont += 1
    return reloj_fil, reloj_col_inv

def relojes_arena_B(N):
    #---------------------------------- RELOJES DE ARENA (B) ----------------------------------
    #Llenado de reloj por columnas inverso de abajo a arriba de der a izq
    "B1 - Salud y Bienestar"
    reloj_col_low = np.zeros((N, N), dtype = "int")
    cont = 1
    centro = N//2
    for i in range(0, N, 1):
        for j in range(0, N, 1):
            if (j <= centro) and (i >= j) and (j <= N-1-i):
                reloj_col_low[i, j] = cont
                cont += 1
            elif (j >= centro) and (j >= i) and (j >= N-i-1):
                reloj_col_low[i, j] = cont
                cont += 1
    
    #Llenado de reloj por columnas de arriba a abajo de izq a der
    "B2 - Educacion de Calidad"
    reloj_col_top = np.zeros((N, N), dtype = "int")
    cont = 1
    #Llenado por columnas
    for j in range(0, N, 1):
        for i in range(0, N, 1):
            if (i <= centro) and (j >= i) and (j <= N - 1 - i):
                reloj_col_top[i, j] = cont
                cont += 1
            elif (i > centro) and (j >= N - 1 - i) and (j <= i):
                reloj_col_top[i, j] = cont
                cont += 1
    return reloj_col_low, reloj_col_top

def rombos(N):
    #---------------------------------- ROMBOS (C) ----------------------------------
    #Llenado en rombo por filas de abajo a arriba y de der a izq
    "C1 - Igualdad de Genero"
    rombo_filas = np.zeros((N, N), dtype = "int")
    cont = 1
    med = N//2
    aux = 0
    for i in range(N-1, -1, -1):
        for j in range(N-1, -1, -1):
            if i >= med:
                if (j >= med - aux) and (j <= med + aux):
                    rombo_filas[i][j] = cont
                    cont += 1
            elif i < med:
                if (j >= med - i) and (j <= med + i):
                    rombo_filas[i][j] = cont
                    cont += 1
        if i > med:
            aux += 1
    
    #Llenado en rombo por columnas de izq a der y de abajo hacia arriba 
    "C2 - Agua Limpia y Saneamiento"
    rombo_cols = np.zeros((N, N), dtype = "int")
    cont = 1
    med = N//2
    aux = 0
    for j in range(N-1, -1, -1):
        for i in range(N-1, -1, -1):
            if j >= med:
                if (i >= j - med) and (i <= med + aux):
                    rombo_cols[i][j] = cont
                    cont += 1
            elif j < med:
                if (i >= med - j) and (i <= med + j):
                    rombo_cols[i][j] = cont
                    cont += 1
        if j > med:
            aux += 1
    return rombo_filas, rombo_cols

def esquinas(N):
    #---------------------------------- ESQUINAS (D) ----------------------------------
    #Llenado en rombo por filas de abajo a rriba y de der a izq
    "D1 - Energia Asequible y No Contaminante"
    corners_filas = np.zeros((N, N), dtype = "int")
    cont = 1
    med = N//2
    aux = med
    for i in range(0, N, 1):
        for j in range(0, N, 1):
            if i < med:
                if (j < med - i) or (j >= med + i + 1):
                    corners_filas[i][j] = cont
                    cont += 1
            elif i > med:
                if (j <= med - aux) or (j >= med + aux):
                    corners_filas[i][j] = cont
                    cont += 1
        if i > med:
            aux = aux - 1
    
    #Llenado en rombo por columnas de arriba a abajo y de izq a der
    "D2 - Trabajo Decente y Crecimiento Economico"
    corners_cols = np.zeros((N, N), dtype = "int")
    cont = 1
    med = N//2
    aux = med-1
    for j in range(0, N, 1):
        for i in range(0, N, 1):
            if j < med:
                if (i < med - j) or (i > med + j):
                    corners_cols[i][j] = cont
                    cont += 1
            elif j > med:
                if (i < j - med) or (i > med + aux):
                    corners_cols[i][j] = cont
                    cont += 1
        if j > med:
            aux -= 1
    return corners_filas, corners_cols

def tornados(N):
    #---------------------------------- TORNADOS (E) ----------------------------------
    #Llenado en Tornado dejando espacios de recorrido Der->Abajo->Izq->Arriba
    "E1 - Industria, Innovacion e Infraestructura"
    m_tornado_1 = np.zeros((N, N), dtype=int)
    top = 0
    bottom = N - 1
    left = 0
    right = N - 1
    cont = 1
    while top <= bottom and left <= right:
        #Izquierda a Derecha
        for j in range(left, right + 1):
            if (top + j) % 2 == 0:
                m_tornado_1[top][j] = cont
                cont += 1
        top += 1
        
        #Arriba a Abajo
        for i in range(top, bottom + 1):
            if (i + right) % 2 == 0:
                m_tornado_1[i][right] = cont
                cont += 1
        right -= 1
        
        if top <= bottom:
            #Derecha a Izquierda
            for j in range(right, left - 1, -1):
                if (bottom + j) % 2 == 0:
                    m_tornado_1[bottom][j] = cont
                    cont += 1
            bottom -= 1
            
        if left <= right:
            #Abajo a Arriba
            for i in range(bottom, top - 1, -1):
                if (i + left) % 2 == 0:
                    m_tornado_1[i][left] = cont
                    cont += 1
            left += 1

    #Llenado en Tornado dejando espacios de recorrido Abajo->Der->Arriba->Izq
    "E2 - Reduccion de las Desigualdades"
    m_tornado_2 = np.zeros((N, N), dtype=int)
    top = 0
    bottom = N - 1
    left = 0
    right = N - 1
    cont = 1
    while top <= bottom and left <= right:
        #Arriba a Abajo
        for i in range(top, bottom + 1):
            if (i + left) % 2 == 0:
                m_tornado_2[i][left] = cont
                cont += 1
        left += 1
        
        #Izquierda a Derecha
        for j in range(left, right + 1):
            if (bottom + j) % 2 == 0:
                m_tornado_2[bottom][j] = cont
                cont += 1
        bottom -= 1
        
        #Abajo a Arriba
        if left <= right:
            for i in range(bottom, top - 1, -1):
                if (i + right) % 2 == 0:
                    m_tornado_2[i][right] = cont
                    cont += 1
            right -= 1
            
        #Derecha a Izquierda
        if top <= bottom:
            for j in range(right, left - 1, -1):
                if (top + j) % 2 == 0:
                    m_tornado_2[top][j] = cont
                    cont += 1
            top += 1       
    return m_tornado_1, m_tornado_2

def diagonales_espaciadas(N):
    #---------------------------------- DIAGONALES ESPACIADAS (F) ----------------------------------
    #Llenado de diagonales por columas de izq a der de arriba a abajo
    "F1 - Cudades y Comunidades Sostenibles"
    suma = 0
    diag_top = np.zeros((N, N), dtype=int)
    cont = 1
    for k in range(0, N, 1):
        for j in range(0, N, 1):
            for i in range(0, N, 1):
                if i + j == suma:
                    diag_top[i][j] = cont
                    cont += 1
        suma += 2
    
    #Llenado de diagonales por columas de izq a der de abajo a arriba
    "F2 - Produccion y Consumo Responsables"
    suma = N-1
    diag_low = np.zeros((N, N), dtype=int)
    cont = 1
    for k in range(0, N, 1):
        for j in range(0, N, 1):
            for i in range(N-1,-1,-1):
                if i - j == suma:
                    diag_low[i][j] = cont
                    cont += 1
        suma -= 2
    return diag_top, diag_low
    
def zeta_ene(N):
    #---------------------------------- Z y N (G) ----------------------------------
    #Llenado en Z por filas de abajo a arriba y de der a izq
    "G1 - Accion por el Clima" 
    zeta = np.zeros((N,N), dtype = "int")
    cont = 1
    for i in range(N-1,-1,-1):
        for j in range(N-1,-1,-1):
            if (i == N-1) or (i == 0) or (i+j == N-1):
                zeta[i][j] = cont
                cont += 1
    
    #Llenado en N por columnas de abajo a arriba y de der a izq
    "G2 - Vida Submarina"
    ene = np.zeros((N,N), dtype = "int")
    cont = 1
    for j in range(N-1,-1,-1):
        for i in range(N-1,-1,-1):
            if (j == N-1) or (j == 0) or (i+j == N-1):
                ene[i][j] = cont
                cont += 1
    return zeta, ene

def diags_sin_centro(N):
    #---------------------------------- DIAGONALES SIN CENTRO (H) ----------------------------------
    #Llenado de diagonales sin centro por filas de abajo a arriba en ambos sentidos
    "H1 - Vida de Ecosistemas Terrestres"
    diag = np.zeros((N,N), dtype = "int")
    cont = 1
    for j in range(0, N, 1):
        for i in range(N-1, -1, -1):
            if i + j == N-1 and i != j:
                diag[i][j] = cont
                cont += 1               
    for j in range(N-1, -1, -1):
        for i in range(N-1, -1, -1):
            if i == j and i != N//2:
                diag[i][j] = cont
                cont += 1
    
    #Llenado de diagonales sin centro por filas de abajo a arriba en ambos sentidos
    "H2 - Paz, Justicia e Instituciones Solidas"
    diag_inv = np.zeros((N,N), dtype = "int")
    cont = 1
    for j in range(N-1, -1, -1):
        for i in range(N-1, -1, -1):
            if i == j and i != N//2:
                diag_inv[i][j] = cont
                cont += 1
    for j in range(0, N, 1):
        for i in range(N-1, -1, -1):
            if i + j == N-1 and i != j:
                diag_inv[i][j] = cont
                cont += 1
    return diag, diag_inv

#Funcion de prueba para terminal   
def menu_cartones():
    #Validacion y Entrada de Datos
    N = int(input("Ingrese la cantidad de filas y columnas de la matriz: "))
    while (N%2 == 0) or (N < 5):
        if (N < 5):
            print("Error, el tamaño debe ser mayor o igual a 5")
        else:
            print("Error, el tamaño debe ser impar")
        N = int(input("Ingrese la cantidad de filas y columnas de la matriz: "))
    print()
    
    print("===================================================================")
    print("                CATÁLOGO DE MATRICES DISPONIBLES                   ")
    print("===================================================================\n")
    print("--- OPCIÓN A ---")
    relojes_arena_A(N)

    print("--- OPCIÓN B ---")
    relojes_arena_B(N)
    
    print("--- OPCIÓN C ---")
    rombos(N)
    
    print("--- OPCIÓN D ---")
    esquinas(N)
    
    print("--- OPCIÓN E ---")
    tornados(N)
    
    print("--- OPCIÓN F ---")
    diagonales_espaciadas(N)
    
    print("--- OPCIÓN G ---")
    zeta_ene(N)
    
    print("--- OPCIÓN H ---")
    diags_sin_centro(N)
    print("===================================================================\n")

    opcion = input("¿Qué letra o qué pareja deseas elegir? ")  
    opcion = opcion.upper()
    if opcion == "A":
        print("\n>> Tu elección ha sido la pareja A")
        relojes_arena_A(N)        
    elif opcion == "B":
        print("\n>> Tu elección ha sido la pareja B")
        relojes_arena_B(N)        
    elif opcion == "C":
        print("\n>> Tu elección ha sido la pareja C")
        rombos(N)        
    elif opcion == "D":
        print("\n>> Tu elección ha sido la pareja D")
        esquinas(N)        
    elif opcion == "E":
        print("\n>> Tu elección ha sido la pareja E")
        tornados(N)   
    elif opcion == "F":
        print("\n>> Tu elección ha sido la pareja F")
        diagonales_espaciadas(N)
    elif opcion == "G":
        print("\n>> Tu elección ha sido la pareja G")
        zeta_ene(N)        
    elif opcion == "H":
        print("\n>> Tu elección ha sido la pareja H")
        diags_sin_centro(N)        
    else:
        print("\n[!] Opción inválida. Por favor, selecciona una letra válida entre la A y la H.")
    
if __name__ == "__main__":      
    menu_cartones()