
import pandas as pd
import snscrape.modules.twitter as sntwitter
import datetime
import itertools
import warnings
import time


def scrape_tweets(keyword,since): #llamar esta función para cada día

    since = datetime.datetime.strptime(since, '%Y-%m-%d').date()
    ayer = since - datetime.timedelta(days=2) #dos dias menos
    ayer = ayer.strftime('%Y-%m-%d')
    manana = since + datetime.timedelta(days=2) #dos dias mas
    manana = manana.strftime('%Y-%m-%d')
    text=f"{keyword} since:{ayer} until:{manana}"

    data = pd.DataFrame(list(itertools.islice(sntwitter.TwitterSearchScraper(
    text).get_items(),5000))) 

    return data

def percentage(part, whole):

  percentage = 100 * float(part)/float(whole)
  return percentage

def count_values_in_column(data,feature):
 total=data.loc[:,feature].value_counts(dropna=False)
 percentage=round(data.loc[:,feature].value_counts(dropna=False,normalize=True)*100,2)
 return pd.concat([total,percentage],axis=1,keys=['Total','Percentage'])




def add_Keywords(partidos):
    partidos['kw1'] = partidos[['Equipo 1', 'Equipo 2']].agg(''.join, axis=1)
    partidos['kw2'] = partidos[['Equipo 1', 'Equipo 2']].agg('-'.join, axis=1)
    partidos['kw3'] = partidos[['Equipo 1', 'Equipo 2']].agg('_'.join, axis=1)
    partidos['kw4'] = partidos[['Equipo 1', 'Equipo 2']].agg('vs'.join, axis=1)
    partidos['kw5'] = partidos[['Equipo 1', 'Equipo 2']].agg(' vs '.join, axis=1)
    partidos['kw6'] = partidos[['Equipo 1', 'Equipo 2']].agg(' and '.join, axis=1)
    return partidos

def dates(since): #llamar esta función para cada día
     date_1 = datetime.datetime.strptime(since, '%Y-%m-%d').date()
     dia_1= date_1.strftime('%Y-%m-%d')
     start_date = date_1 - datetime.timedelta(days=1)
     start = start_date.strftime('%Y-%m-%d')
     end_date = date_1 + datetime.timedelta(days=1)
     final = end_date.strftime('%Y-%m-%d')
     fechas=[start,dia_1,final]

     return fechas

def limpiar(partidos):


    for s in partidos['Equipo 1']:
        s.replace('_x000D_','')

    partidos['Equipo 1'].replace({'Israel -':'Israel',
                                'Andorra -':'Andorra',
                                'Israel - Belgium':'Israel',
                                'Cyprus -':'Cyprus',
                                'Netherlands -':'Netherlands',
                                'Croatia -':'Croatia',
                                'Slovakia -':'Slovakia',
                                'Austria -':'Austria',
                                'North Macedonia -':'Macedonia',
                                'North Macedonia':'Macedonia',
                                'Kazakhstan -':'Kazakhstan',
                                'Belgium -':'Belgium',
                                'England -':'England',
                                'Luxembourg -':'Luxembourg',
                                'Portugal -':'Portugal',
                                'Albania -':'Albania',
                                'Moldova -':'Moldova',
                                'Wales -':'Wales',
                                'Georgia -':'Georgia',
                                'Gibraltar -':'Gibraltar',
                                'Sweden -':'Sweden',
                                'Italy -':'Italy',
                                'Hungary -':'Hungary',
                                'Poland -':'Poland',
                                'Slovenia -':'Slovenia',
                                'San Marino -':'San Marino',
                                'Kosovo -':'Kosovo',
                                'Montenegro -':'Montenegro',
                                'Turkey -':'Turkey',
                                'France -':'France',
                                'Ireland -':'Ireland',
                                'Switzerland -':'Switzerland',
                                'Norway -':'Norway',
                                'Romania -':'Romania',
                                'Armenia -':'Armenia',
                                'Estonia -':'Estonia',
                                'Belarus -':'Belarus',
                                'Azerbaijan -':'Azerbaijan',
                                'Iceland -':'Iceland',
                                'Scotland -':'Scotland',
                                'Finland -':'Finland',
                                'Bulgaria -':'Bulgaria',
                                'Serbia -':'Serbia',
                                'Ukraine -':'Ukraine',
                                'Denmark -':'Denmark',
                                'Malta -':'Malta',
                                'Latvia -':'Latvia',
                                'Germany -':'Germany',
                                'Russia -':'Russia',
                                'Greece -':'Greece',
                                'Lithuania -':'Lithuania',
                                'Spain -':'Spain',
                                'Bosnia-Herzegovina -':'Bosnia-Herzegovina',
                                'Czech':'Czech Republic',
                                'Northern':'Northern Ireland',
                                'Malta - Faroe':'Malta',
                                'Russia - San':'Russia',
                                'Israel - North':'Israel',
                                'Kosovo - Czech':'Kosovo',
                                'Spain - Faroe':'Spain',
                                'Belgium - San':'Belgium',
                                'Poland - North':'Poland',
                                'Scotland - San':'Scotland',
                                'Norway - Faroe':'Norway',
                                'Austria - North':'Austria',
                                'Sweden - Faroe':'Sweden',
                                'Georgia - North':'Georgia',
                                'North':'Macedonia',}, inplace=True)
    for i in partidos['Equipo 2']:
        i.replace('_x000D_','')
    partidos['Equipo 2'].replace({'BosniaHerzegovina':'Bosnia-Herzegovina',
                                'Republic  Netherlands':'Netherlands',
                                '01':'Belgium',
                                'Ireland  Faroe Islands':'Faroe Islands',
                                'Ireland  Finland':'Finland',
                                'Ireland  Romania':'Romania',
                                'Ireland  Hungary':'Hungary',
                                'Ireland  Greece':'Greece',
                                'Ireland  Estonia':'Estonia',
                                'Islands':'Faroe Islands',
                                'Ireland  Belarus':'Belarus',
                                'North Macedonia':'Macedonia',
                                'Marino':'San Marino',
                                'Macedonia  Austria':'Austria',
                                'Republic':'Czech Republic',
                                'Ireland  Germany':'Germany',
                                'Macedonia  Slovenia':'Slovenia',
                                'Macedonia  Israel':'Israel',
                                'Macedonia  Kosovo':'Kosovo',
                                'Ireland  Slovakia':'Slovakia',
                                'Ireland  Netherlands':'Netherlands'}, inplace=True)


    #Drop empty fields
    partidos.dropna()

    for i in range(len(partidos["Date"])):
        partidos["Date"][i]=datetime.datetime.strptime(partidos["Date"][i].replace('_x000D_',''), "%d-%m-%Y").strftime("%Y-%m-%d")


    return partidos


# Función para descargar tweets de partidos de fútbol
def descargar(partidos, n):
    
    # Iterar n veces
    for i in range(n):
        
        # Obtener las palabras clave del partido actual
        keywords = [partidos['kw1'][i],partidos['kw2'][i],partidos['kw3'][i],partidos['kw4'][i],partidos['kw5'][i],partidos['kw6'][i]]
        
        # Obtener las fechas del partido actual
        fechas = dates(partidos["Date"][i])
        
        # Seleccionar la palabra clave principal
        match = keywords[3]
        
        # Seleccionar la fecha desde la cual se descargará tweets
        since = fechas[1]
        
        # Convertir la fecha en formato datetime.date
        since = datetime.datetime.strptime(since, '%Y-%m-%d').date()
        
        # Calcular la fecha de ayer (un día antes de la fecha de descarga)
        ayer = since - datetime.timedelta(days=1) 
        ayer = ayer.strftime('%Y-%m-%d')
        
        # Calcular la fecha de mañana (un día después de la fecha de descarga)
        manana = since + datetime.timedelta(days=1)
        manana = manana.strftime('%Y-%m-%d')

        # Inicializar un dataframe vacío para almacenar los tweets descargados
        tweets = pd.DataFrame()
        
        # Iterar sobre todas las fechas del partido actual
        for s in range(len(fechas)):
            # Inicializar un dataframe vacío para almacenar los tweets de cada fecha
            data = pd.DataFrame()
            # Iterar sobre todas las palabras clave del partido actual
            for j in range(len(keywords)):
                try:
                    # Descargar tweets con la palabra clave actual y la fecha actual
                    data = pd.concat([data, scrape_tweets(keywords[j],fechas[s])], ignore_index=True)
                except Exception as e:
                    # Si hay un error, esperar 10 minutos antes de volver a intentar
                    print("Hubo un error, volveremos a intentarlo en un momento")
                    time.sleep(600)
                    continue

            # Agregar los tweets descargados de cada palabra clave a tweets
            tweets = pd.concat([tweets, data], ignore_index=True)
        
        # Si se descargaron tweets, guardarlos en un archivo CSV
        if len(tweets) > 0:
            print(f'Descargados los tweets de {match} en {since}')
            tweets.to_csv(f"tweets/all_tweets_all_days/{ayer}_{keywords[3]}.csv")
            
def main():
    warnings.simplefilter(action = "ignore", category = RuntimeWarning) 
    partidos=add_Keywords(limpiar(pd.read_excel("Eurocupsf.xlsx")))   
    n=int(input("Cuantos csv desea descargar: "))
    descargar(partidos,n)

if __name__ == "__main__":
    main()