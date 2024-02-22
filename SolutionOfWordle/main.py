#importando los archivos
import matplotlib as plt 
import numpy as np
from numpy import loadtxt
import os
import random
import collections
import itertools 
import math
import pandas as pd
import statistics as st
from collections import OrderedDict
import time
#############################################################################################################
#############################################################################################################
#############################################################################################################


#archivos

RUTA_ABSOLUTA=os.getcwd()

#path en donde estan el archivo de las palabras
provLISTA_DE_PALABRAS = os.path.join(RUTA_ABSOLUTA, "provisionales.txt")

#path en donde quedan las imagenes

imagenes=os.path.join(RUTA_ABSOLUTA,"imagenes")


#hace un rastreo del archivo y lo convierte en una lista


#############################################################################################################
#############################################################################################################
#############################################################################################################

#hace un rastreo del archivo y lo convierte en una lista

def aLista(path):
    image = loadtxt(str(path),dtype=str, delimiter='","')
    provLISTA_VERTICAL=[] #Lista de las palabras verticales
    for element in image:
        provLISTA_VERTICAL.append(element)
    return provLISTA_VERTICAL






#############################################################################################################

LiSTA_TRABAJABLE=aLista(provLISTA_DE_PALABRAS) #lista de las palabras


palabra_del_dia=random.choice(LiSTA_TRABAJABLE) #palabra aleatoria dentro de la lista

#############################################################################################################







#METODOS UTILES


#############################################################################################################
#############################################################################################################
#############################################################################################################
#############################################################################################################
#metodo para ver las palabras dentro de la lista de manera ordenada, se puede imprimir tal cual pero aqui se ve una por una
def VER_PALABRAS(LiSTA_TRABAJABLE):

    for palabra in LiSTA_TRABAJABLE:

        print(palabra)


#############################################################################################################
#############################################################################################################
#############################################################################################################
#############################################################################################################

#Este metodo lo que hace es comparar palabra a palabra con la palabra del dia y obtener el tablero de colores 

def OBTENER_COLORES(palabra_del_dia,LiSTA_TRABAJABLE): 
    
    
    COMPENDIO_COLORES=[] #lista que tiene todos los tableros de colores

    for palabra in LiSTA_TRABAJABLE: 

        COLORES=list()  

        for letter in range(5): #para cada letra dentro de la palabra, va mirando lo que va generando

            if(palabra[letter]==palabra_del_dia[letter]):

                COLORES.append("v")            

            elif (palabra[letter] in palabra_del_dia):

                COLORES.append("a")

            else:

                COLORES.append("g")

        COMPENDIO_COLORES.append(COLORES) #para cada palabra devuelvo el tablero de colores 



    return COMPENDIO_COLORES #toda la lista con el comependio de colores



#############################################################################################################
#############################################################################################################
#############################################################################################################


def COLOR_SINGULAR(palabra_del_dia): #este metodo hace lo mismo que el anterior pero con una palabra que se mete por input, esto con el fin de
    #recortar probabilidades mas adelante

    palabra=input("INTRODUCE LA PALABRA: ")
    
    COLORES=[]

    LETRASVERDES=[] 

    NARANJAS=[]

    GRISES=[]

    for letter in range(len(palabra)):

        if(palabra[letter]==palabra_del_dia[letter]):

            COLORES.append("v")

            LETRASVERDES.append(palabra[letter])

        elif (palabra[letter] in palabra_del_dia):

            COLORES.append("n")

            NARANJAS.append(palabra[letter])
                
        else:

            COLORES.append("g")

            GRISES.append(palabra[letter])
            
    
    print(COLORES)

    return LETRASVERDES,NARANJAS,GRISES,COLORES
  


#############################################################################################################
#############################################################################################################
#############################################################################################################
#############################################################################################################

def VER_COMPENDIO(COMPENDIO_COLORES): #este metodo existe para ver cada tablero del compendio de colores

    for color in COMPENDIO_COLORES:


        print(color)



#############################################################################################################
#############################################################################################################
#############################################################################################################
#############################################################################################################


def _INDICE(tablero):# lo que hace es devolver el indice en donde estan las verdes, esto con el fin de poder recortar las palabras mas adelante

    INDICES=[]

    for i in range(len(tablero)):

        if tablero[i]=="v":

            INDICES.append(i)

    #print(INDICES)
    return INDICES


#############################################################################################################
#############################################################################################################
#############################################################################################################
#############################################################################################################

#METODO PRINCIPAL PRACTICAMENTE


def REDUCIR_PROBABILIDADES(LiSTA_TRABAJABLE, INDICES, LETRASVERDES,NARANJAS,GRISES):

    #Este metodo lo que hace es recibir, un tablero de indices que es los indeices de las letras verdes, las letras verdes, las naranjas y las grises, y para cada palabra lo que voy haciendo es mirar si cumlpen con las condiciones de suficiencia para poder anexarla a las nuevas listas donde estan las palabras que cumplen con las condiciones del tablero de colores, 
    # Es decir, lo que esta haciendo es recortar la lista original en base al codigo de colores qeu recibe el metood

    NUEVAS_PALABRAS=[]   #palabras naranjas

    LiSTA_TRABAJABLE.pop() #por alguna razon queda un elemento vacio al final, por lo tanto lo quito

    preNUEVAS_PALABRAS=[]



#############################################################################################################

#PARTE NARANJAS

#aunque es algo de fuerza bruta funciona, basicamente lo que esta haciendo es ir mirando cuantas naranjas hay, es decir, cada vez que avanzo  =>
#lo que tengo que mirar es si hay una siguiente porque si no la hay no puedo comparar, por lo que mientras avanzo,  lo que hago, es por ser naranja, solo tengo que mirar si la letra esta en la palabra
#y si si esta y no hay siguiente, pues meto la palabra en la lista y ya acabo

    for word in LiSTA_TRABAJABLE:

        if len(NARANJAS)>=1:

            if NARANJAS[0] in word:

                if len(NARANJAS)>=2:

                    if NARANJAS[1] in word:

                        if len(NARANJAS)>=3:

                            if(NARANJAS[2]) in word:

                                if len(NARANJAS)>=4:

                                    if NARANJAS[3] in word:

                                        if len(NARANJAS)==5:

                                            if NARANJAS[4] in word:

                                                preNUEVAS_PALABRAS.append(word)

                                        else:
                                            preNUEVAS_PALABRAS.append(word)

                                else:
                                    preNUEVAS_PALABRAS.append(word)

                        else:
                            preNUEVAS_PALABRAS.append(word)
                else:
                    preNUEVAS_PALABRAS.append(word)



#############################################################################################################

#PARTE VERDES

#Aplicando la logica, al ser una letra verde lo que necesito es mirar en que indice esta la verde, y por lo tanto cual letra es =>
#por lo tanto lo que hago es mirar si la letra que hay en el indice que hay en indices de la palabra, es igual a la letra que hay en letras verdes
#Para esto debo seguir mirando si hay un elemento siguiente en los indices, y si no hay meto la palabra en la lista de verdes
    if len(INDICES)>=1:

        for palabra in LiSTA_TRABAJABLE:

            if len(palabra)>=1:

                if palabra[INDICES[0]]==LETRASVERDES[0]:

                    if len(INDICES) >= 2:

                        if palabra[INDICES[1]]==LETRASVERDES[1]:

                            if len(INDICES) >= 3:

                                if palabra[INDICES[2]]==LETRASVERDES[2]:

                                    if len(INDICES) >= 4:

                                        if palabra[INDICES[3]]==LETRASVERDES[3]:

                                            if len(INDICES) == 5:

                                                if palabra[INDICES[4]]==LETRASVERDES[4]:

                                                    NUEVAS_PALABRAS.append(palabra)

                                            else:
                                                NUEVAS_PALABRAS.append(palabra)
                                    else:
                                        NUEVAS_PALABRAS.append(palabra)                                                     
                            else:
                                NUEVAS_PALABRAS.append(palabra)
                    else:
                        NUEVAS_PALABRAS.append(palabra)
    else:
        print("Todas las palabras")
    
#############################################################################################################


#PARTE GRISES

# Lo que debo hacer aqui es en vez de mirar cuales tienen, al ser gris lo que debo de mirar es cuales no tienen estas letras
# Por lo que hago lo mismo que en naranjas pero con un "not in"
    lista_final=[]

    for word in LiSTA_TRABAJABLE:
        
        if len(GRISES)>=1:

            if GRISES[0] not in word:

                if len(GRISES)>=2:

                    if GRISES[1] not in word:

                        if len(GRISES)>=3:

                            if(GRISES[2]) not in word:

                                if len(GRISES)>=4:

                                    if GRISES[3] not in word:

                                        if len(GRISES)==5:

                                            if GRISES[4] not in word:

                                                lista_final.append(word)

                                        else:
                                            lista_final.append(word)

                                else:
                                    lista_final.append(word)

                        else:
                            lista_final.append(word)
                else:
                    lista_final.append(word)


#############################################################################################################

#CUALES SON CUALES
#lista_final(grises)
#preNUEVAS_PALABRAS(naranjas)
#NUEVAS_PALABRAS(verdes)

#CUALES SON CUALES
#############################################################################################################

#TODOS LOS POSIBLES CASOS DONDE NO EXISTEN ALGUNOS 

#Lo que hice aqui fue mirar las posibles combinaciones de la existencia de listas, es decir, evidentemente hay ocasiones en donde no hay verdes, o no hay naranjas o grises, o estan las 3, etc, entonces tenia que mirar cada una de las posibilidades para evitar errores
# Todo esto lo hago para poder devolver una lista final 

    prelista_final=[]

    if(len(NUEVAS_PALABRAS)>=1):

        if(len(preNUEVAS_PALABRAS)>=1):

            if(len(lista_final)>=1):

                for w1 in NUEVAS_PALABRAS:

                    for w2 in preNUEVAS_PALABRAS:

                        for w3 in lista_final:

                            if w1==w2==w3:

                                prelista_final.append(w1)  #VNG caso donde estan las 3 
            else:

                for w1 in NUEVAS_PALABRAS:

                    for w2  in preNUEVAS_PALABRAS:

                        if w1==w2:

                            prelista_final.append(w1) #VN caso donde estan solo verdes y naranjas

        elif(len(lista_final)>=1): 

            for w1 in NUEVAS_PALABRAS:

                for w2 in lista_final:

                    if w1==w2:

                        prelista_final.append(w1) #VG caso de verdes y grises
        else:
            print(" ") #V caso de solo verdes
    
    elif(len(preNUEVAS_PALABRAS)>=1):

        if(len(lista_final)>=1):

            for w1 in preNUEVAS_PALABRAS:

                for w2 in lista_final:

                    if w1==w2:

                        prelista_final.append(w1)   #NG caso de naranjas y grises

        else:
            prelista_final=preNUEVAS_PALABRAS  #N caso de naranjas

    else:
        prelista_final=lista_final  #G caso de grises 





#############################################################################################################
#############################################################################################################
#############################################################################################################

    if len(LiSTA_TRABAJABLE)>0:

        probabilidad=len(prelista_final)/len(LiSTA_TRABAJABLE) # esta es la probabilidad de la lista, que es la cantidad de palabras sobre la cantidad total de palabras


    else:

        probabilidad=1/1226

#############################################################################################################
#############################################################################################################
#############################################################################################################

#EJECUTABLE
    
    print ("\n".join([" ".join(prelista_final[i:i+15]) for i in range(0,len(prelista_final),15)]))  # aqui lo que hago es imprimir de a 15
    

#############################################################################################################
#############################################################################################################
#############################################################################################################


    if len(prelista_final)>=1:    

        bits=-(math.log2(probabilidad))  # los bits de informacion   

        print("Hay ",len(prelista_final), " palabras posibles, dando una probabilidad de: " ,probabilidad,"para este patron de colores dada la palabra original")

        #print("Ademas nos da",bits, "bits de informacion") #mejor dejar por afuera cuando se pone a jugar la maquina sola

        final_list=list(OrderedDict.fromkeys(prelista_final)) #eliminar palabras repetidas

        return final_list

    else:
        print("La probabilidad de tu palabra es: 1/", str(len(LiSTA_TRABAJABLE)))

    #return prelista_final


    

#############################################################################################################
#############################################################################################################
#############################################################################################################
#############################################################################################################






# Lo que hace este metood es permitir jugar al usuario, para probar nuestra version del juego 

def JUGAR_WORDLE(palabra_del_dia,LiSTA_TRABAJABLE):

    i=0

    GANASTE=['v','v','v','v','v']

    TABLERO=[]

    while TABLERO != GANASTE:

        if  i<6: #condiciones de ganar en menos de 6

            i+=1

            print(i)

            LETRASVERDES,NARANJAS,GRISES,TABLERO=COLOR_SINGULAR(palabra_del_dia)

            INDICES=_INDICE(TABLERO)    

            REDUCIR_PROBABILIDADES(LiSTA_TRABAJABLE,INDICES,LETRASVERDES,NARANJAS,GRISES)
            
        else:
            
            print('salimos')

            break

    print("Fin del juego")



#############################################################################################################
#############################################################################################################
#############################################################################################################
#############################################################################################################

#

def frecuencias(COMPENDIO_COLORES,LiSTA_TRABAJABLE):

    #lo que hago en este metodo es mirar las frecuencias de los tableros, es decir, dada una palabra, al generar el compendio de colores lo que hago es mirar cuantas veces aperece un tabolero
    #esto lo hago con el fin de obetner la probabilidad de cada tablero
    NUEVO_COMPENDIO=[]

    for element in COMPENDIO_COLORES:

        nuevo_string=str(element).replace('"','')

        NUEVO_COMPENDIO.append(nuevo_string)


    counter=collections.Counter(NUEVO_COMPENDIO)

    diccionario2=dict(counter)

    diccionario=dict(sorted(diccionario2.items(), key=lambda item: item[1])) #Diccioario organiado de mayor a menor

    nueva_lista=[]

    for x in diccionario.keys():

        nueva_lista.append(diccionario[x]/len(LiSTA_TRABAJABLE)) #aqui meto a la lista de probababilidades

        #print(x , " => " , diccionario[x])
    
   # print(nueva_lista)
    return nueva_lista



#############################################################################################################
#############################################################################################################
#############################################################################################################
#############################################################################################################

def mejoresfrecuencias(COMPENDIO_COLORES,LiSTA_TRABAJABLE):
    #Es el mismo metodo que el anterior pero acotando la lista a las mejores
    NUEVO_COMPENDIO=[]
    for element in COMPENDIO_COLORES:
        nuevo_string=str(element).replace('"','')
        NUEVO_COMPENDIO.append(nuevo_string)

    counter=collections.Counter(NUEVO_COMPENDIO)
    diccionario2=dict(counter)
    diccionario=dict(sorted(diccionario2.items(), key=lambda item: item[1]))
    nueva_lista=[]
    for x in diccionario.keys():
        if ((int(list(diccionario.values())[-1]))-(int((list(diccionario.values())[-2]))))<5:
            #print(x , " => " , diccionario[x])
            nueva_lista.append(diccionario[x]/len(LiSTA_TRABAJABLE))
        else:
            #print("Muy poca entriopia")
            exit 
   # print(nueva_lista)
    return nueva_lista


#############################################################################################################
#############################################################################################################
#############################################################################################################
#############################################################################################################






#############################################################################################################
#############################################################################################################
#############################################################################################################
#############################################################################################################

# 

def auxiliarentropia(COMPENDIO_COLORES,LiSTA_TRABAJABLE):

#hace exactamente lo mismo que los dos anteriores pero devuelve dos listas, tanto probababilidades como tableros

    NUEVO_COMPENDIO=[]

    for element in COMPENDIO_COLORES:

        nuevo_string=str(element).replace('"','')

        NUEVO_COMPENDIO.append(nuevo_string)

    counter=collections.Counter(NUEVO_COMPENDIO)
    
    diccionario2=dict(counter)
    
    diccionario=dict(sorted(diccionario2.items(), key=lambda item: item[1]))
    
    nueva_lista=[]

    tableros=[]

    for x in diccionario2.keys():

        nueva_lista.append(diccionario[x]/len(LiSTA_TRABAJABLE))

    for key, value in diccionario2.items():

        tableros.append(key)



    
    return nueva_lista,tableros


#############################################################################################################
#############################################################################################################
#############################################################################################################
#############################################################################################################

#############################################################################################################
#############################################################################################################
#############################################################################################################
#############################################################################################################
#la frecuencia que tomo en el metodo son las frecuencias que vienen de un dataframe que contenia las ocurrencias de las palbras, es decir un data frame de las palabras mas usadas
 
#Este metodo lo que hace es tomar una lista, las frecuencias de las palabras, estas cosas vienen de un metodo dataframe, y una palabra, y a partir 
#de ello, lo que hace es crear el compendio de colores
#y en base a la lista creo el compendio y a partir de ese compendio aplicoel metodo auxiliar, con el fin de obtener las frecuencias de los tableros
#y por lo tanto calcular sus probabilidades tambien 
# para siguiente a ello  tomar las frecuencias que vienen del dataframe, que son la frecuencia de la palabra que estoy tomando en el for y
#por consiguiente, en base a lo que ya tengo calculo la entriopia del tablero y cuando ya tengo esto lo divido por la frecuencia de la palabra,
#esto con el fin de ponderar, ya que es mas preferble escoger una palabra con mayor frecuencia que una con menor frecuencia,
#ya que es masprobable que sea esa


def entriopia(lista,frecuencias,palabra_del_dia):


    promedios=[]

    mayor=0

    palabrafinal=''

    index=0

    diccionario={}
    
    if lista is None:

        lista=[]

        lista.append(palabra_del_dia)

    for palabra in lista:

        if len(lista)==1:

            break

        promedio=[]

        COMPENDIO_COLORES=OBTENER_COLORES(palabra,lista)

        index2=0 

        probababilidades,tableros=auxiliarentropia(COMPENDIO_COLORES,lista)
            #probabilidad 
        for element in probababilidades:

            frecuenciapalabra=frecuencias[index] 

            bits=-(math.log2(element)) #probababilidad del tablero

            suma=len(probababilidades)/243 #suma de probababilidades entre el total de tableros, esto con el fin de obtener la suma total

            entriopia=bits*suma #formula de entriopia

            promedio.append(entriopia/frecuenciapalabra) #medida de frecuencia, ya explicada al inicio del metodo

            index2+=1
        
        index+=1

        relacion=sum(promedio)/len(promedio) # la relacion vendria siendo una medida de cuan valiosa es la palabra, esto lo meto en un diccionario, y ese diccionario lo organizo
        #lo organizo porque cuanto automatizo todo, lo que ahgo es escoger la ultima palabra, porque es evidente que es mejor escoger la palabra con la relacion de menor valor

        diccionario[palabra]=relacion
            
    diccionario=dict(sorted(diccionario.items(), key=lambda item: item[1]))

    return diccionario #nueva lista para elegir la siguiente palabra por decirlo de alguna manera



#este metodo lo que hace es obtener el dataframe para retornar las listas que necesito
def DATA_FRAME():

    RUTA_ABSOLUTA=os.getcwd()
    rutaarchivo = os.path.join(RUTA_ABSOLUTA, "2frecuencia.csv")
    df = pd.read_csv(rutaarchivo,sep=";",on_bad_lines='skip')
    df.dropna()
    df['Word'] = df['Word'].astype('str')
    mask = (df['Word'].str.len() == 5)
    df = df.loc[mask]
    
    palabras=df['Word'].tolist()
    
    frecuencias=df['Freq'].tolist()
    
    for palabra in palabras:
        palabra=str(palabra)
        if len(palabra) != 5:
            indexpalabra=palabras.index(palabra)
            del palabras[indexpalabra]
    
    return palabras,frecuencias


#############################################################################################################
#############################################################################################################

#MAQUINA(Automatizacion)

#En esta parte del codigo, son los mismos metodos con las mismas funciones, pero hechos de tal forma que se ejecuten solos, sin intervencion del usuario
#############################################################################################################
#############################################################################################################

def MAQUINA_COLOR_SINGULAR(palabra,palabra_del_dia): #la diferencia entre este metodo y el de arriba, es que este ya recibe la palabra y no la mete por input

    COLORES=[]

    LETRASVERDES=[]

    NARANJAS=[]

    GRISES=[]

    for letter in range(len(str(palabra))):

        if(palabra[letter]==palabra_del_dia[letter]):

            COLORES.append("v")

            LETRASVERDES.append(palabra[letter])

        elif (palabra[letter] in palabra_del_dia):

            COLORES.append("n")

            NARANJAS.append(palabra[letter])
                
        else:
            COLORES.append("g")

            GRISES.append(palabra[letter])
            
    
    print(COLORES)

    return LETRASVERDES,NARANJAS,GRISES,COLORES


def MEJOR_PALABRA(diccionario,palabra_del_dia):
    #Este metodo lo que hace es devolverme en base el diccionario que devuelve entriopia
    #lo que hace es elegir la palabra mas optima, que seria la ultima 

    if len(list(diccionario.keys()))>=1:

        first_value = list(diccionario.keys())[-1]

        palabra=str(first_value)

        print(palabra)

        return palabra
    else:
        return palabra_del_dia
    #quiero hacer un metodo que me coja una lista que contenga las palabras ordenadas 
    #por mayor probabilidad y que escoja la primera

#este metodo lo qe hace es jugar solo, la magia esta en que en este caso, la lista se va terminando, hasta que solo queda la lista ocn la palabra final
def MAQUINA_JUGAR_WORDLE(LiSTA_TRABAJABLE,frecuencias):

    palabra_del_dia=random.choice(LiSTA_TRABAJABLE)

    i=0

    GANASTE=['v','v','v','v','v']

    TABLERO=[]

    palabra='crane' #esta palabra puede ser la que queramos
    count=0
    medidor=0
    start_time=time.time() #tomando el tiempo que tarda el metodo
    while TABLERO != GANASTE:
        if  i<6:
            count+=1
            i+=1
                     
            LETRASVERDES,NARANJAS,GRISES,TABLERO=MAQUINA_COLOR_SINGULAR(palabra,palabra_del_dia) #creo las letras, y el tablero con todo

            if TABLERO==GANASTE:
                break

            INDICES=_INDICE(TABLERO)    #indices para las verdes
            if medidor==0: 
                #este medidor se usa para mirar que sea en el primer intento, se hace esto porque si no pues no habria lista inicial, ya que para poder recortarla tengo que usar su version anterior
                lista = REDUCIR_PROBABILIDADES(LiSTA_TRABAJABLE,INDICES,LETRASVERDES,NARANJAS,GRISES)

            else:
                
                lista = REDUCIR_PROBABILIDADES(lista,INDICES,LETRASVERDES,NARANJAS,GRISES) # hago el metodo con la lista previa para ir acortando

            medidor+=1

            
            if lista==True: 

                if len(lista)==1:

                    break

            diccionario=entriopia(lista,listafrecuencias,palabra_del_dia) #creo el diccionario en base a la lista que tengo con el fin de elegir la mejor palabra para seguir jugando

            
            if palabra_del_dia==palabra:

                break
            
            palabra = MEJOR_PALABRA(diccionario,palabra_del_dia)
            
        else:
            print('No vale')
            break
    tiempo_final=time.time()
    print("Fin del juego",'Con '+str(count)+" intentos")
    tiempo_total=tiempo_final-start_time
    return count, tiempo_total





#creo las listas para jugar
listapalabras,listafrecuencias=DATA_FRAME()

#MAQUINA JUEGA SOLA

contadorpromedios=[]
tiempos=[]
for i in range(500):
    contador,tiempo= MAQUINA_JUGAR_WORDLE(listapalabras,listafrecuencias)
    contadorpromedios.append(contador)


#entriopia(lista)


#JUGAR NOSOTROS


#MAQUINA_JUGAR_WORDLE(listapalabras,listafrecuencias)


#METODO DE UN SOLO USO

def histograma(mydict,palabra_del_dia):
    numeros=[]
    
    for x in range(len(mydict)):
        numeros.append(x)
    fig, ax = plt.subplots()
    ax.bar(numeros,mydict)
    plt.title(palabra_del_dia)

    imagenes=str(palabra_del_dia)
    plt.savefig('imagenes2/'+palabra_del_dia)

    plt.xlabel('Patron')
    plt.ylabel('frecuencias')

    plt.show()


def guardarimagenes(LiSTA_TRABAJABLE):
    for palabra in LiSTA_TRABAJABLE:
        COMPENDIO_COLORES=OBTENER_COLORES(palabra,LiSTA_TRABAJABLE)
        lista=mejoresfrecuencias(COMPENDIO_COLORES,LiSTA_TRABAJABLE)
        if len(lista)>1:
            #print(lista)
            histograma(lista,palabra)


path_tiempos=os.path.join(RUTA_ABSOLUTA,'tiemposnosotros.txt')


print(sum(contadorpromedios)/len(contadorpromedios))
#print(tiempos)
#tiempos.append(tiempo)

#Atxt(path_tiempos,tiempos)
def Atxt(path,lista):

    textfile = open(path, "w")

    for element in lista:

        textfile.write(str(element) + "\n")

    textfile.close()







#histograma(lista,palabra_del_dia)


#METODOS INUTILES
def enumerar_colores():
    cont=0
    colores="vag"
    estados=itertools.product(colores,colores,colores,colores,colores)
    PATRONES=[]
    for i in estados:
        PATRONES.append(i)
   
    for element in PATRONES:
        print(element)


    return PATRONES












