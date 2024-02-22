import matplotlib.pyplot as plt
import numpy as np
from openpyxl import Workbook
import time
import openpyxl


def crear_matriz(sol,m,n):
    R =  np.zeros((m, n),dtype=int)
    c = np.zeros(m,dtype=int)
    for p in sol: 
        maquina = p[0] - 1
        trabajo = p[1]
        
        R[maquina, c[maquina]] = trabajo + 1
        c[maquina]+=1
    return R

def makespan(sol,n,m):

    tm = np.zeros(m,dtype=int)
    l = np.zeros(n,dtype=int)
    
    for proceso in sol:
        j = proceso[1]
        m = proceso[0]
        t = proceso[2]
        ind = tm[m-1]
        if ind >= l[j]:

            tm[m-1] = ind + t 
            l[j] = ind+t 
        else:
            tm[m-1]= l[j]+t
            l[j] = l[j]+t 

    return max(tm)

def factible(l,n):
    
    ordenes = np.zeros(n)*-1
    for sub in l:
        if sub[3] != ordenes[sub[1]]:
            return False
        else:
            ordenes[sub[1]] += 1
    return True














def leer(path):
    """
    Leer la instancia y guardar las dimensiones de la matriz y crear las
    correspondientes matrices de tiempos, primeras n filas, y la matriz de orden
    las n filas restantes
    """
    with open(path, 'r') as archivo:
        n, m = map(int, archivo.readline().split())
    M = np.loadtxt(path,skiprows=1,dtype=int) # Matriz completa
    tiempos = M[:n,:].astype(int) # Matriz de tiempos, primeras n filas
    orden   = M[n:,:].astype(int) # Matriz de orden, n filas restantes
    return n,m,tiempos,orden


def guardar_excel(R,tiempo,mk,archivo,instancia):
    """
    Funcion para guardar la matriz de datos en un excel separado
    """

    # Crear un nuevo archivo de Excel
    wb = openpyxl.load_workbook(archivo)

    hoja = wb.create_sheet(title=instancia)

    for fila in R:
        hoja.append(list(fila))
    hoja.append([mk,tiempo])
    wb.save(archivo)













def obtener_numero(nombre):
    # Separa el nombre de archivo en partes utilizando el punto como separador
    partes = nombre.split('.')
    # Encuentra la última parte que debería ser el número
    ultimo_parte = partes[-2]
    # Extrae el número y lo convierte en entero
    numero = int(ultimo_parte.split('JSSP')[-1])
    return numero
