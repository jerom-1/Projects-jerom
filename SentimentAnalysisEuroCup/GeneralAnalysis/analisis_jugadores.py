import pandas as pd
import spacy
from spacytextblob.spacytextblob import SpacyTextBlob
import glob
import os


def analizar(nombres):
    # Crea un DataFrame llamado resultados con columnas nombre, negativo, positivo y neutral

    resultados = pd.DataFrame(columns=['nombre', 'negativo', 'positivo', 'neutral'])

    # Carga el modelo pre-entrenado de spacy en inglés

    nlp = spacy.load('en_core_web_md')

    nlp.add_pipe('spacytextblob')

    # Itera a través de cada jugador
    for nombre in nombres["jugador"]:
        print(nombre)
        # Si el nombre contiene el número 1, lo separa y utiliza solo la parte antes del guion
        # Inicializa los contadores para los resultados del análisis de sentimiento
        tweets_negativos = 0
        tweets_positivos = 0
        tweets_neutrales = 0
        # Obtiene la ruta de todos los archivos CSV que contienen los tweets
        files_paths = glob.glob(f"{os.getcwd()}/tweets/all_tweets_all_days/*")
        # Itera a través de los archivos CSV en la carpeta
        for f in files_paths:
            # Lee los tweets del archivo CSV
            tweets = pd.read_csv(f, lineterminator='\n', dtype=str)
            # Selecciona solo la columna 'rawContent' que contiene el texto del tweet
            tweets = tweets['rawContent']
            # Convierte la columna en un DataFrame y cambia el tipo de dato a string
            tweets = pd.DataFrame(tweets, columns=['rawContent'])
            tweets['rawContent'] = tweets['rawContent'].astype(str)
            # Itera a través de cada tweet
            for rawContent in tweets['rawContent']:
                # Obtiene el texto del tweet actual
                # Si el nombre del jugador actual está en el texto del tweet, realiza el análisis de sentimiento
                if nombre in rawContent:
                    # Realiza el análisis de sentimiento en el texto del tweet
                    doc = nlp(rawContent)
                    sentiment_score = doc._.polarity
                    # Clasifica el tweet como positivo, negativo o neutral
                    if sentiment_score > 0:
                        tweets_positivos += 1
                    elif sentiment_score < 0:
                        tweets_negativos += 1
                    else:
                        tweets_neutrales += 1
        # Si el jugador tiene al menos un tweet positivo, negativo o neutral, almacena los resultados en el
        # DataFrame resultados
        if tweets_negativos != 0 or tweets_neutrales != 0 or tweets_positivos != 0:
            resultados.loc[len(resultados)] = [nombre, tweets_negativos, tweets_positivos, tweets_neutrales] # type: ignore
            print(resultados)
            
    return resultados