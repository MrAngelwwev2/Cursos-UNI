import matplotlib.pyplot as plt
import math
import numpy as np
import random
from timeit import default_timer

# El índice del punto con la ordenada más pequeña en puntos, si hay más de uno, se devolverá el punto con la abscisa más pequeña
def obtener_punto_inferior(puntos):
    min_indice = 0
    n = len(puntos)
    for i in range(0, n):
        if puntos[i][1] < puntos[min_indice][1] or (
                puntos[i][1] == puntos[min_indice][1] and puntos[i][0] < puntos[min_indice][0]):
            min_indice = i
    return min_indice

# Ordenar según el ángulo polar con el punto central, coseno, punto_central: punto central
def ordenar_angulo_polar_cos(puntos, punto_central):
    n = len(puntos)
    cos_valor = []
    rank = []
    norm_lista = []
    for i in range(0, n):
        punto_ = puntos[i]
        punto = [punto_[0] - punto_central[0], punto_[1] - punto_central[1]]
        rank.append(i)
        norm_valor = math.sqrt(punto[0] * punto[0] + punto[1] * punto[1])
        norm_lista.append(norm_valor)
        if norm_valor == 0:
            cos_valor.append(1)
        else:
            cos_valor.append(punto[0] / norm_valor)

    for i in range(0, n - 1):
        indice = i + 1
        while indice > 0:
            if cos_valor[indice] > cos_valor[indice - 1] or (
                    cos_valor[indice] == cos_valor[indice - 1]
                    and norm_lista[indice] > norm_lista[indice - 1]):
                temp = cos_valor[indice]
                temp_rank = rank[indice]
                temp_norm = norm_lista[indice]
                cos_valor[indice] = cos_valor[indice - 1]
                rank[indice] = rank[indice - 1]
                norm_lista[indice] = norm_lista[indice - 1]
                cos_valor[indice - 1] = temp
                rank[indice - 1] = temp_rank
                norm_lista[indice - 1] = temp_norm
                indice = indice - 1
            else:
                break
    puntos_ordenados = []
    for i in rank:
        puntos_ordenados.append(puntos[i])

    return puntos_ordenados


# Devuelve el ángulo entre el vector y el vector [1, 0] -cuántos grados girar en sentido antihorario desde [1, 0] para alcanzar este vector
def vector_angulo(vector):
    norm_ = math.sqrt(vector[0] * vector[0] + vector[1] * vector[1])
    if norm_ == 0:
        return 0

    angle = math.acos(vector[0] / norm_)
    if vector[1] >= 0:
        return angle
    else:
        return 2 * math.pi - angle


# Producto cruzado de dos vectores
def coss_multi(v1, v2):
    return v1[0] * v2[1] - v1[1] * v2[0]


def graham_scan(puntos):
    bottom_indice = obtener_punto_inferior(puntos)
    punto_inferior = puntos.pop(bottom_indice)
    puntos_ordenados = ordenar_angulo_polar_cos(puntos, punto_inferior)

    m = len(puntos_ordenados)
    if m < 2:
        print("El número de puntos es demasiado pequeño para formar un Convex Hull")
        return

    stack = []
    stack.append(punto_inferior)
    stack.append(puntos_ordenados[0])
    stack.append(puntos_ordenados[1])

    for i in range(2, m):
        longitud = len(stack)
        top = stack[longitud - 1]
        next_top = stack[longitud - 2]
        v1 = [puntos_ordenados[i][0] - next_top[0], puntos_ordenados[i][1] - next_top[1]]
        v2 = [top[0] - next_top[0], top[1] - next_top[1]]

        while coss_multi(v1, v2) >= 0:
            if longitud < 3:     # Después de agregar estas dos líneas de código, no se informará ningún error cuando la cantidad de datos sea grande
                break          # Después de agregar estas dos líneas de código, no se informará ningún error cuando la cantidad de datos sea grande
            stack.pop()
            longitud = len(stack)
            top = stack[longitud - 1]
            next_top = stack[longitud - 2]
            v1 = [puntos_ordenados[i][0] - next_top[0], puntos_ordenados[i][1] - next_top[1]]
            v2 = [top[0] - next_top[0], top[1] - next_top[1]]
        stack.append(puntos_ordenados[i])

    return stack


#Definimos el metodo Algoritmo_Graham_Scan
def Algoritmo_Graham_Scan():
    num_puntos = int(input("¿Cuantos puntos desea ingresar?: "))
    print("\n")
    for n in range(num_puntos,num_puntos+1):
        puntos = []
        for i in range(n):
            punto_x = random.randint(0,num_puntos)
            punto_y = random.randint(0,num_puntos)
            print("\n")
            temp = np.hstack((punto_x, punto_y))
            punto = temp.tolist()
            puntos.append(punto)

        resultado = graham_scan(puntos)

        
        for punto in puntos:
            plt.scatter(punto[0], punto[1], marker='o', c='y', s=8)
        longitud = len(resultado)
        for i in range(0, longitud - 1):
            plt.plot([resultado[i][0], resultado[i + 1][0]], [resultado[i][1], resultado[i + 1][1]], c='r')
        plt.plot([resultado[0][0], resultado[longitud - 1][0]], [resultado[0][1], resultado[longitud - 1][1]], c='r')
        plt.xlabel("EJE X",size = 18)
        plt.ylabel("EJE Y", size = 18)
        plt.title("CONVEX HULL",fontdict={'family':'monospace','color':'darkblue','weight':'bold','size':22})
        plt.show()

    inicio = default_timer()
    graham_scan(puntos)
    fin = default_timer()
    t_e = fin - inicio
    print("El tiempo de ejecución del Algoritmo con", num_puntos, "puntos es", t_e)


def menu():
    print("\t¡CONVEX HULL EN PYTHON!\n\t-----------------")
    print("1) Ejecutar el Algoritmo de Graham Scan")
    print("2) Salir")
    opcion = int(input("Elija una opción: "))
    return opcion

while True:
    opc = menu()
    if opc==1:
        Algoritmo_Graham_Scan()
    elif opc==2:
        break
    else:
        print("No has seleccionado una opción correcta.")
