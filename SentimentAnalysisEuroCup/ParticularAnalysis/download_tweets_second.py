# Importar las librerías necesarias
import os
import pandas as pd
import snscrape.modules.twitter as sntwitter
import datetime
import itertools
import warnings
import time 

# Definir función para obtener tweets de Twitter
def scrape_tweets(keyword,fechas):
    # Extraer las fechas de inicio y fin de búsqueda
    before=fechas[0]
    after=fechas[2]
    # Combinar la palabra clave y las fechas en un solo texto para realizar la búsqueda
    text=f"{keyword} since:{before} until:{after}"
    # Usar la API de snscrape para obtener los tweets y guardarlos en un DataFrame de pandas
    data = pd.DataFrame(itertools.islice(sntwitter.TwitterSearchScraper(
    text).get_items(),5000)) # type: ignore #
    # Devolver el DataFrame con los tweets
    return data

# Definir función para calcular el porcentaje
def percentage(part, whole):
    # Calcular el porcentaje y devolverlo
    percentage = 100 * float(part)/float(whole)
    return percentage

# Definir función para obtener las fechas de inicio, fin y centro de la búsqueda

def dates(since): #llamar esta función para cada día
    
     # Convertir la fecha en formato de string a un objeto datetime
     date_1 = datetime.datetime.strptime(since, '%Y-%m-%d').date()

     dia_1= date_1.strftime('%Y-%m-%d')
     # Calcular la fecha de inicio de búsqueda como 2 días antes de la fecha dada
     start_date = date_1 - datetime.timedelta(days=2)

     start = start_date.strftime('%Y-%m-%d')
     # Calcular la fecha de fin de búsqueda como 2 días después de la fecha dada
     end_date = date_1 + datetime.timedelta(days=2)

     final = end_date.strftime('%Y-%m-%d')
     
     # Crear una lista con las fechas de inicio, fin y centro de búsqueda
     fechas=[start,dia_1,final]

     return fechas

def descargar(partidos,n):
    
    for i in range(n):
        # Iteramos sobre los partidos
        
        fechas=dates(partidos["Date"][i]) # Obtenemos las fechas de los tweets que queremos descargar
        match=partidos["Country"][i] # Obtenemos el país del partido

        folder=f"matches/{match}" # Creamos la carpeta donde se guardarán los tweets del partido
        
        tweets = pd.DataFrame() # Inicializamos un dataframe vacío para guardar los tweets
        
        # Comprobamos si ya existe la carpeta del partido
        if os.path.exists(folder):

            num = [3, 6, 9, 12, 15, 18, 21, 24, 27, 30, 33, 36, 39, 42]
            
            for j in num:
                jugador = str(partidos.iloc[i, j]) # Obtenemos el nombre del jugador
                if jugador.lower() != "nan":
                    
                    # Si existe la carpeta del jugador, leemos el archivo csv con los tweets descargados anteriormente
                    
                    if os.path.exists(f"{folder}/{jugador}"):
                        
                        df_viejo = pd.read_csv(f"{folder}/{jugador}")
                        
                        try:
                            # Descargamos los nuevos tweets del jugador
                            
                            tweets = scrape_tweets(jugador, fechas)
                            
                            # Concatenamos los tweets nuevos con los que ya teníamos
                            tweets = pd.concat([df_viejo, tweets], ignore_index=True)
                            
                        except Exception as e:
                            # Si hay algún error, esperamos 10 minutos y continuamos con el siguiente jugador
                            time.sleep(600)
                            continue          
                    else:
                        # Si no existe la carpeta del jugador, descargamos los tweets
                        tweets = scrape_tweets(jugador, fechas)
                        
                    if len(tweets)>0:
                        # Si se descargaron tweets, los guardamos en un archivo csv
                        tweets.to_csv(f"{folder}/{jugador}.csv")
                        print(f'Aumentado los tweets de {match},{jugador}')
        else:
            # Si no existe la carpeta del partido, la creamos
            os.mkdir(folder)
            # Obtenemos la información de los jugadores que se jugaron en el partido
            num=[3, 6, 9, 12, 15, 18, 21, 24, 27, 30, 33, 36, 39, 42]
            
            for j in num:
                jugador= str(partidos.iloc[i,j]) # Obtenemos el nombre del jugador
                if jugador.lower() != "nan":
                    try:
                        # Descargamos los tweets del jugador
                        tweets = scrape_tweets(jugador, fechas)
                    except Exception as e:
                        # Si hay algún error, esperamos 10 minutos y continuamos con el siguiente jugador
                        time.sleep(600)
                        continue
                        
                    if len(tweets)>0:
                        # Si se descargaron tweets, los guardamos en un archivo csv
                        tweets.to_csv(f"{folder}/{jugador}.csv")
                        print(f'Descargados los tweets de {match},{jugador}')
                    else:
                        # Si no se descargaron tweets, mostramos un mensaje de que no se encontraron tweets del jugador
                        print(f"No se encontraron tweets de {match},{jugador}")
                        
def main():
    partidos=pd.read_csv("matches_players_clean.csv")
    n=int(input("Cuantos csv desea descargar: "))
    descargar(partidos,n)

if __name__ == "__main__":
    main()
    
    
