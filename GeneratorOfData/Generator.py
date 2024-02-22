import random
import pandas as pd
import random
import matplotlib.pyplot as plt
import statistics as st
import numpy as np
import collections as co
import math
from tabulate import tabulate



def crudos(filename):

    df = pd.read_csv(filename)
    df.dropna()
    l=df["data"].tolist()
    l=list(filter(lambda x: math.isnan(x) == False, l))
    l.sort()
    aux=[]
    for el in l:
        if el >= -57.37 and el <=238.54:
            aux.append(el)

    l=aux
    mean=np.mean(l)
    mediana=np.median(l)
    quantiles = np.quantile(l, [0.25,0.5,0.75,1])
    moda=st.mode(l)
    std=np.std(l)
    varianza=np.var(l)
    hea=["Media","Mediana","Moda", "Varianza","Desv Est"]
    datos=[[mean,mediana, moda, varianza,std]]
    crudos=tabulate(datos,headers=hea,tablefmt="fancy_grid")
    nums=[]
    for i in range(len(quantiles)):
        nums.append(("Cuantil"+ str(i+1)))
    quantiles=[quantiles]
    quantiles_crudos=tabulate(quantiles,headers=nums,tablefmt="fancy_grid")
    return l,crudos,quantiles_crudos

def clases_y_frecuencias_absolutas(diccionario,number_of_classes,mini,maxi):

    paso=(maxi-mini)/number_of_classes
    ex=paso-int(paso)
    lista_clases=[]
    pr=[]
    x=mini
    per=maxi+1-mini
    for i in range(1,number_of_classes+2):
        lista_clases.append(x)
        x+=paso
  #  lista_clases=[round(i+ex,4) for i in range(int(mini),int(v))]
    frecuencias={}
    for i in range(len(lista_clases)):
        suma=0
        x=lista_clases[i-1:i+1]
        if len(x)>0:
            for key,val in diccionario.items():
                if key <= x[1] and key >= x[0]:
                    suma+=val

                    clase=str(i)+" "
            frecuencias[str(str(round(x[0],3))+","+str(round(x[1],3))),sum(x)/2]=suma

    return frecuencias

def clases(diccionario,number_of_classes,mini, maxi):
    paso=(maxi-mini)/number_of_classes
    ex=paso-int(paso)
    lista_clases=[]
    x=mini
    for i in range(1,number_of_classes+2):
        lista_clases.append(x)
        x+=paso
    return lista_clases

def obtener_datos_longitud_menordato(filename):

    df = pd.read_csv(filename)
    l=df["data"].tolist()
    z=list(filter(lambda x: math.isnan(x) == False, l))

    z.sort()
    aux=[]
    for el in l:
        if el >= -57.37 and el <=238.54:
            aux.append(el)
    z=aux
    l=z
    mini=min(l)
    maxi=max(l)
    counter=co.Counter(l)
    x=dict(sorted(counter.items()))

    return x,len(l),mini,maxi

def crear_lista_frecuencias(diccionario):
    lfa=[]
    for key, val in diccionario.items():
        lfa.append(val)
    return lfa
def percentiles(lista_clases,suma,percentil,frecuencias,absolutas):
    alpha=suma*(percentil/100)
    lon=abs(lista_clases[0]-lista_clases[1])

    lfa=crear_lista_frecuencias(frecuencias)
    ind=0
    for i in range (len(lfa)):
        if alpha<lfa[i]:
            ind= i
            break

    li=lista_clases[ind]
    iu=ind-1
    inf=lfa[iu]
    j=alpha-inf
    ab=absolutas[ind]

    percen=li+(lon*(j/ab))
    #print("Percentil",percentil,"Valor",percen,"Li",li,"Lon",lon,"j",j,"ab",ab)
    return percen

def ultimo_elemento(dicti):
    return list(dicti)[-1]

def tabla(dicti, diccionario,l,n,maxi,mini):

    headerstabla=["Clase","Marca de clase","Frec abs","Frec abs acc","Frec Rev", "Frec Rev Acc"]
    print(" ")
    media=0
    maxm=0
    moda=0
    varianza=0
    suma=0
    sumarelativa=0
    frecuenciasacumuladas={}
    frecuenciasrelativas={}
    dif=[]
    absolutas=[]
    datosprint=[]
    for key, value in dicti.items():
        if value>maxm:
            maxm=value
            moda=key[1]
        suma+=value
        sumarelativa+=value/l
        datosprint.append([key[0],round(key[1],2), value,suma,round(value/l,4), round(sumarelativa,4)])
        dif.append(key[1])
        absolutas.append(value)
        frecuenciasacumuladas[key[1]]=suma
        frecuenciasrelativas[key[0]]=round(value/l,4)
        media+=key[1]*(value/l)
        ultimo=key[1]

    for key,value in dicti.items():
        varianza+=(((int(key[1])-media)**2)*value)
    varianza=varianza/suma
    key_list = list(dicti.keys())
    number_of_classes=len(dicti)

    lista_clases=clases(diccionario,number_of_classes,mini, maxi)
    quartil1= percentiles(lista_clases,suma,25,frecuenciasacumuladas,absolutas)
    quartil2= percentiles(lista_clases,suma,50,frecuenciasacumuladas,absolutas)
    quartil3= percentiles(lista_clases,suma,75,frecuenciasacumuladas,absolutas)
    quartil4=maxi
    tabla=tabulate(datosprint,headers=headerstabla,tablefmt="fancy_grid",showindex="always")
    print(" ")
    hea=["Media","Mediana","Moda", "Varianza","Desv Est"]
    datos=[[media,quartil2, moda, varianza,math.sqrt(varianza)]]
    tabulados=tabulate(datos,headers=hea,tablefmt="fancy_grid")
    print(" ")
    nums=[]
    quantiles=[quartil1,quartil2,quartil3,quartil4]
    for i in range(len(quantiles)):
        nums.append(("Cuantil"+ str(i+1)))
    quantiles=[quantiles]
    quantiles_tabulados=tabulate(quantiles,headers=nums,tablefmt="fancy_grid")
    return frecuenciasrelativas,tabla, tabulados,quantiles_tabulados



def crear_rangos(diccionario):
    clases={}
    for key,val in diccionario.items():
        key=key.replace("[","")
        key=key.replace("]","")
        clases[tuple(key.split(","))]=val
    return clases
def generar_datos(rangos,lon,requeridos):
    l=[]
    aux=0
    k=requeridos
    if requeridos<=lon:
        print('ya los tienes')
        return 0
    for key,val in rangos.items():
        if k<=0:
            return l
        if len(l)>=requeridos:
            return l
        else:
            if type(key[0])==int():
                li=int(key[0])
            else:
                li=round(float(key[0]),2)
            if type(key[1])==int(): 
                ls=int(key[1])
            else:
                ls=float(key[1])
            l.append([random.uniform(li, ls) for i in range(int(requeridos*val))])

    return l


def aplanar(x):
    f=[]
    for el in x:
        for nums in el:
            f.append(nums)
    return f
def generados(l):

    mean=np.mean(l)
    mediana=np.median(l)
    quantiles = np.quantile(l, [0.25,0.5,0.75,1])
    moda=st.mode(l)
    std=np.std(l)
    varianza=np.var(l)
    hea=["Media","Mediana","Moda", "Varianza","Desv Est"]
    datos=[[mean,mediana, moda, varianza,std]]
    nums=[]
    generados=tabulate(datos,headers=hea,tablefmt="fancy_grid")
    for i in range(len(quantiles)):
        nums.append(("Cuantil"+ str(i+1)))
    quantiles=[quantiles]
    quantiles_generados = tabulate(quantiles,headers=nums,tablefmt="fancy_grid")
    return generados,quantiles_generados

def duel_hist(y1,y2):

    fig = plt.figure(figsize=(15,5))
    ax1 = fig.add_subplot(1, 2, 1)
    ax2 = fig.add_subplot(1, 2, 2)

    ax1.hist(y1)
    ax1.set_title('Crudos')

    ax2.hist(y2)
    ax2.set_title('Generados')
    plt.show()
    return fig
def duel_boxplot(y1,y2):

    fig = plt.figure(figsize=(15,5))
    ax1 = fig.add_subplot(1, 2, 1)
    ax2 = fig.add_subplot(1, 2, 2)

    ax1.boxplot(y1)
    ax1.set_title('Crudos')

    ax2.boxplot(y2)
    ax2.set_title('Generados')
    plt.show()
    return fig

def main():
    dataset=input("Dataset a usar: ")
    clases=int(input("Cuantas clases quieres generar: "))
    requeridos=int(input("Cuantos datos requieres: "))

    data1,crudos_tabla,quantiles_crudos=crudos(dataset)

    diccionario,l,mini,maxi=obtener_datos_longitud_menordato(dataset)

    frecuencias=clases_y_frecuencias_absolutas(diccionario,clases,mini,maxi)

    frencuencias_relativas,tabla_print,tabulados,quantiles_tabulados=tabla(frecuencias,diccionario,l,clases,maxi,mini)

    rangos=crear_rangos(frencuencias_relativas)

    nueva_data=generar_datos(rangos,l,requeridos)
    final_data=aplanar(nueva_data)
    data2=final_data

    generados_tabla,quantiles_generados=generados(final_data)

    
    print(" ------------- MEDIDAS DE TENDENCIA CENTRAL Y DE DISPERSION --------------- ")
    print("")
    print(crudos_tabla,"-------- CRUDOS")
    print(" ")
    print(tabulados,"-------- TABULADOS")
    print(" ")
    print(generados_tabla,"-------- GENERADOS")
    print(" ")
    print("---------------------------------------------------------------------------")
    print(" ")
    print("---------------------------------QUANTILES---------------------------------")
    print(" ")
    print(quantiles_crudos,"-------- QUANTILES CRUDOS")
    print(" ")
    print(quantiles_tabulados,"--------QUANTILES TABULADOS ")
    print(" ")
    print(quantiles_generados,"--------QUANTILES GENERADOS")
    print(" ")
    print("---------------------------------------------------------------------------")
    print(" ")
    print("---------------------------------- TABLA ----------------------------------")
    print(" ")
    print(tabla_print)
    duel_hist(data1,data2)
    duel_boxplot(data1,data2)
if __name__ == "__main__":
    main()




