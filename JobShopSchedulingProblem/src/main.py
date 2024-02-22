from Constructivo import *
from Auxiliares import *
# from GRASP import GRASP
# from GRASP2 import GRASP2
import os
import glob
import random
import pandas as pd
from busquedalocal import *
from vecindarios import *
from GRASP import *


# Ruta de la carpeta que quieres explorar
carpeta = 'JSSP Instances'
archivos = glob.glob(os.path.join(carpeta, '*'))
archivos = sorted(archivos, key=obtener_numero)

dt = pd.read_excel('TimeLimit.xlsx')



random.seed(1414)

excel1 = 'resultados/JSSP_JEROM_VND.xlsx'
excel2 = 'resultados/JSSP_JEROM_MS_ELS_P(0.2).xlsx'
excel3 = 'resultados/JSSP_JEROM_MS_ELS_P(0.5).xlsx'
excel4 = 'resultados/JSSP_JEROM_MS_ELS_P(0.8).xlsx'
    
    
df = pd.DataFrame({'Instancia':[], 'MKGRASP':[], 'MKVND':[], 'MKMELS02':[], 'MKMELS05':[], 'MKMELS08':[], 
                    'tVND':[], 'tMELS02':[], 'tMELS05':[], 'tMELS08':[], 'itVND':[], 'itMELS02':[], 'itMELS05':[], 'itMELS08':[]})


for archivo in archivos:

    instancia=archivo.split('/')[1].split('.')[0]
    n,m,tiempos,orden = leer(archivo)
    sols, mkopt, tgraps = GRASP(n, m, tiempos, orden,0.2,20)

    tMAX = dt[dt['Instancia'] == instancia]['tMAX'].values[0]
    
    solMELSD,mkMELSD,tMELSD,itMELSD = MS_ELS_P(sols,n,m,tMAX, 0.2)
    
    solMELSC,mkMELSC,tMELSC,itMELSC = MS_ELS_P(sols,n,m,tMAX, 0.5)

    solMELSO,mkMELSO,tMELSO,itMELSO = MS_ELS_P(sols,n,m,tMAX, 0.8)
    
    
    
    solVND,mkVND,tVND,itVND = VND(sols[0][0],n,m,tMAX)
    
    df2= pd.DataFrame({'Instancia':[instancia], 'MKGRASP':[sols[0][1]], 'MKVND':[mkVND], 'MKMELS02':[mkMELSD], 'MKMELS05':[mkMELSC], 'MKMELS08':[mkMELSO], 
                      'tVND':[tVND], 'tMELS02':[tMELSD], 'tMELS05':[tMELSC], 'tMELS08':[tMELSO], 'itVND':[itVND], 'itMELS02':[itMELSD], 'itMELS05':[itMELSC], 'itMELS08':[itMELSO]})
                       
    
    df = pd.concat([df, df2], ignore_index=True)
    
    print(df)
    
    
    RVND = crear_matriz(solVND, m,n)
    
    RMELSC = crear_matriz(solMELSC, m, n)
    
    RMELSD = crear_matriz(solMELSD, m, n)
    
    RMELSO = crear_matriz(solMELSO, m, n)
    
    
    guardar_excel(RVND,tVND,mkVND,excel1,instancia)
    
    guardar_excel(RMELSD,tMELSD,mkMELSD,excel2,instancia)
    
    guardar_excel(RMELSC,tMELSC,mkMELSC,excel3,instancia)
    
    guardar_excel(RMELSO,tMELSO,mkMELSO,excel4,instancia)
    

    
df.to_csv('resultados_generales.csv', index=False)
