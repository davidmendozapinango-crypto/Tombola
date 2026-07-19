#Bibliotecas y módulos del proyecto
import pygame
import struct
import os

#Gráficos

#Configuración inicial(pygame)
##pygame.init()
##icono = pygame.image.load("ruta de imagen")#<-LOGO EN LA VENTANA
##pygame.display.set_icon(icono)
##ventana = pygame.display.set_mode((1920,1080))#<-TAMAÑO VENTANA
##pygame.display.set_caption("Tombola: Registro de Jugadores")
##reloj = pygame.time.Clock()

#Funciones
#Verificación de cédula
def verificar_cedula(ced):
        #Preparamos la información para usar el archivo
        archivofis_jugadores = "JUGADORES.bin"
        formatojugador= "i30sc10s3s10s"
        tam_regjugadores = struct.calcsize(formatojugador)

        #Si no existe ninguna cédula todavia, cualquiera será válida
        if not os.path.exists(archivofis_jugadores):
            print("La cedula es valida (Primer registro).")
            return True

        archivo_jugadores = open(archivofis_jugadores, 'rb')
        eof = False 
        registro = archivo_jugadores.read(tam_regjugadores)
            
        while eof == False:
            if registro == b'':
                eof = True
            else:
                ced_reg, nom, sex, fecha, est, clav = struct.unpack(formatojugador, registro)
                    
                #Si se encuentra una cédula igual, retorna falso (la cédula está repetida, o sea que es inválida)
                if ced_reg == ced:
                    print("La cedula ya ha sido registrada. Intente ingresar otra.")
                    archivo_jugadores.close()
                    return False
                else:
                    registro = archivo_jugadores.read(tam_regjugadores)
        
        #Si acaba el archivo y no se ha encontrado una cédula igual, retorna verdadero (la cedula no está repetida, o sea que es válida)
        print("La cedula es valida.")
        archivo_jugadores.close()
        return True
        
def verificar_clave(clave, indice=0, mayus=False, minus=False, num=False, esp=False, consec=1, error_consec=False):
    #Caso base/ Verificar y salir al llegar al terminar de leer la clave
    if indice == len(clave):
        long_valida = (6 <= len(clave) <= 10)
        consec_valida = (not error_consec and consec <= 3)
        
        clave_valida = True
        
        # Evaluamos cada booleano individualmente
        if not long_valida:
            print("Error: La clave debe tener entre 6 y 10 caracteres")
            clave_valida = False
            
        if not mayus or not minus:
            print("Error: Debe combinar letras mayúsculas y minúsculas")
            clave_valida = False
            
        if not num:
            print("Error: Debe contener al menos un número")
            clave_valida = False
            
        if not esp:
            print("Error: Debe contener al menos un caracter especial (*, =, %, _)")
            clave_valida = False
            
        if not consec_valida:
            print("Error: No puede tener más de 3 caracteres iguales consecutivos")
            clave_valida = False
            
        return clave_valida
    
    #Caso recursivo/ Analizar el indice actual
    actual = clave[indice]
    
    #Verificación de condiciones booleanas
    if actual.isupper():
        mayus = True
    elif actual.islower():
        minus = True
    elif actual.isdigit():
        num = True
    elif actual == "*" or actual == "=" or actual == "%" or actual == "_":
        esp = True

    #Cantidad de caracteres consecutivos actual
    if indice>0:
        if actual == clave[indice-1]:
            consec = consec + 1
            if consec > 3:
                error_consec = True
        else:
            consec = 1

    #Llamada recursiva
    return verificar_clave(clave, indice+1, mayus, minus, num, esp, consec, error_consec)


#Proceso principal: ESTA es la funcion que se debe llamar desde el menu inicial del programa
def registrar_jugador():
    cedula_valida = False
    while cedula_valida == False:
        ced = int(input("Ingrese su cédula: "))
        cedula_valida = verificar_cedula(ced)

    #Revisamos que los datos tengan un contenido apropiado para el formato del binario
    valido = False
    while valido == False:
        name = input("Ingrese su nombre completo: ")
        if len(name) <= 30:
            valido = True
        else:
            print("Por favor, mantenga la respuesta por debajo de 31 caracteres.")

    valido = False
    while valido == False:
        gen = input("Sexo (m/f): ").lower()
        if gen == "m" or gen == "f":
            valido = True
        else:
            print("Ingrese una sola letra (m/f).")

    valido = False
    while valido == False:
        birth = input("Ingrese su fecha de nacimiento (numeros separados por guión): ")
        if len(birth) <= 10:
            valido = True
        else:
            print("Debe ingresar los numeros correspondientes a la fecha separados por guiones. Intente nuevamente.")

    valido = False
    while valido == False:
        est = input("Ingrese el codigo de su estado: ").upper()
        if len(est) == 3:
            valido = True
        else:
            print("El codigo debe ser de 3 caracteres, intente otra vez.")

    print("\n-Debe poseer entre 6 y 10 caracteres.")
    print("-Ser una combinación de letras en mayúscula y minúscula, números y caracteres especiales.")
    print("-Debe contener al menos uno de los siguientes caracteres: * = % _")
    print("-No debe contener un mismo caracter mas de 3 veces seguidas\n")

    clave_valida = False
    while clave_valida == False:
        clave = input("Ingrese su clave: ")
        clave_valida = verificar_clave(clave)
        
    #Para cuando se tengan todos los datos validados
    archivofis_jugadores = "JUGADORES.bin"
    archivo_jugadores = open(archivofis_jugadores, 'ab')

    name_bin = name.ljust(30).encode('utf-8')
    gen_bin = gen.ljust(1).encode('utf-8')
    birth_bin = birth.ljust(10).encode('utf-8')
    est_bin = est.ljust(3).encode('utf-8')
    clave_bin = clave.ljust(10).encode('utf-8')

    reg_binario = struct.pack(ced, name_bin, gen_bin, birth_bin, est_bin, clave_bin)
    archivo_jugadores.write(reg_binario)

    archivo_jugadores.close()

    
