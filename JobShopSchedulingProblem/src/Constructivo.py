import numpy as np
from itertools import groupby
import time



def menesteres(tiempos, orden, n, m):
    """
    Función para crear las matrices necesarias para el procesamiento del codigo,
    esta matriz crea el vector que contenerá los procesos, así como la matriz de ordenes.
    """
    M = []
    O = []
    for i in range(n): # Por cada trabajo
        for j in range(m): # Por cada maquina
            M.append([orden[i,j], i, tiempos[i, j],j]) # [Maquina, trabajo, tiempo, prioridad]
        O.append(orden[i,:]) # Orden del trabajo i

    O = np.array(O)

    M = np.array(sorted(M, key=lambda x: x[2])) # Sorteo los procesos por tiempo

    # Estas tres lineas me agrupan los trabajos por priodidad, conservando el orden pre establecido
    # de tiempos

    Mo = sorted(M, key=lambda x: x[3]) # Sorteo por prioridad
    grupos = {key: list(group) for key, group in groupby(Mo, key=lambda x: x[3])}
    M = [list(grupo) for key in sorted(grupos.keys()) for grupo in grupos[key]]

    # Finalmente M es una lista de todos los trabajos ordenados por prioridad y por tiempo
    return M, O




def constructivo(n,m,tiempos,orden):

    """
    Esta es la función principal del codigo encargada de realizar el algoritmo como tal.
    Su funcionamiento es el siguiente: dado un vector ordenado de procesos "Mf", quiero crear una lista de
    candidatos reales Mf2, a entrar en esta iteración. Despues de tener esa lista de candidatos reales,
    procedo a preguntar si en verdad puedo ingresar ese trabajo en la matriz de procesos sintentica,
    en caso positivo, lo hago y finalmente calculo a cual proceso le corresponde el makespan minimo, entendiendo
    este makespan como el makespan despues de ingresar el proceso i en la matriz de procesamiento sintentica,
    finalmente conservo el proceso cuyo makespan sea minimo, e ingreso realmente ese proceso
    en la matriz de procesamientos real. Esto lo repito hasta que no queden mas trabajos por agendar.
    """
    ti = time.time()
    lista=[]
    l = np.zeros((1,n),dtype=int) # Tiempos acumulados para cada trabajo
    tm = np.zeros(m,dtype=int) # Tiempo de finalizacion en las maquinas


    Mf, O = menesteres(tiempos,orden,n,m) # Vector de procesos ordenados, matriz de ordenes, en donde cada fila i es
    # el orden del trabajo i

    while len(Mf) > 0: # El ciclo va hasta que ya no hayan mas trabajos
        minmk = float("inf") # Cota superior para el makespan minimo

        aux = [] # Lista auxiliar que contiene los trabajos que ya han ingresado en la lista de candidados reales
        h = [] # Candidato final, aquel que tiene menor makespan
        Mf2=[] # Candidatos reales
        # "Mf2" contiene los candidatos reales para esta iteración, el criterio de descarte 
        # de esta lista, es que si ya tengo un trabajo 'i', con una prioridad mas 
        # urgente, es evidente que sus otros trabajos no van a entrar en esta iteración, esto 
        # es evidente cuando se piensa que un trabajo debe seguir un orden por lo que 
        # un mismo trabajo no puede ingresar en la misma iteracion

        for p in Mf:
            if p[1] not in aux:
                aux.append(p[1])
                Mf2.append(p)

        # Itero sobre cada candidato real 
        for p in Mf2:
            tmi = np.array(tm).copy()
            li = np.array(l).copy() # Matriz de tiempos artificial para el proceso i
            Oi = np.array(O).copy() # Matriz de orden principal para el proceso i

            m = p[0] # maquina del candidato i
            j = p[1] # trabajo del candidato i
            t = p[2] # tiempo del candidato i

            # Como cada que finalizo una maquina actualizo la maquina que acabo de procesar por 0,
            # entonces para obtener la maquina que debo procesar miro el primer elemento diferente 
            # de 0 de la fila

            nz1=np.nonzero(Oi[j])[0] # non-zero del vector de ordenes del trabajo j
            if len(nz1)>0:
                nz2=nz1[0]
            else:
                nz2=0 # si no hay ninguno es porque ese indice es el primero, es decir, todavia no he ingresado a
                # ninguna maquina


            if Oi[j][nz2] == m: # Si el orden del trabajo j se corresponde con la maquina del proceso, entonces
                # puedo procesar el trabajo

                # Como cada fila de la matriz de procesos corresponde a una maquina, quiero mirar cual 
                # es el ultimo elemento diferente de 0 de esa fila, y asi obtengo el tiempo de finalización 
                # del ultimo proceso que llevé a cabo en esa maquina

                ind = tmi[m-1]
                if ind >= li[0,j]:
                    pos = (ind,ind+t)
                    tmi[m-1] = ind + t # Meto el trabajo en la matriz de procesamientos
                    li[0,j] = ind+t # Actualizo el tiempo acumulado del trabajo
                else:
                    pos=(li[0,j],li[0,j]+t)

                    #Si el trabajo termina despues
                    tmi[m-1]= li[0,j]+t
                    li[0,j] = li[0,j]+t # Actualizo el tiempo acumulado del trabajo

                Oi[j][nz2] = 0 # Actualizo el orden a 0, porque ya lo realicé

                if max(tmi) < minmk:
                    minmk = max(tmi)
                    h = [p,tmi,Oi,li,pos]

        if len(h)>0: # condicional auxiliar

            # Actualizo las variables reales con los datos del proceso optimo
            pmin = h[0]
            tm = h[1]  # elimino todas las columnas donde todo es 0
            O = h[2]
            l = h[3]
            Mf.pop(Mf.index(pmin)) #elimino el trabajo que acabo de ingresar
            lista.append(pmin)
    tf =time.time()

    t  = tf-ti
    return lista, max(tm), t






