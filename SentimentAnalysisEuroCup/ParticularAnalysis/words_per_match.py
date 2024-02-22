import re
import string
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import glob
import pandas as pd
import pandas as pd
from nltk.probability import FreqDist
nltk.download('stopwords')
nltk.download('punkt')


## DOCUMENTAR


def limpiar_tweet(tweet):
    # Eliminación de menciones y hashtags
    tweet = re.sub(r'@[A-Za-z0-9]+', '', tweet)
    tweet = re.sub(r'#', '', tweet)

    # Eliminación de URLs
    tweet = re.sub(r'https?:\/\/\S+', '', tweet)

    # Eliminación de signos de puntuación y caracteres especiales
    tweet = tweet.translate(str.maketrans('', '', string.punctuation))
    tweet = re.sub(r'[^\w\s]', '', tweet)

    # Conversión a minúsculas
    tweet = tweet.lower()

    # Eliminación de stopwords
    stop_words = set(stopwords.words('english')) 
    tokens = word_tokenize(tweet)
    tweet = ' '.join([word for word in tokens if word not in stop_words])

    # Normalización de palabras
    stemmer = nltk.stem.PorterStemmer()
    tokens = word_tokenize(tweet)
    tweet = ' '.join([stemmer.stem(word) for word in tokens])

    return tweet



# Función para obtener la fecha a partir de un texto de tweet
def obtener_fecha(texto):
    return texto.split()[0]




# Función principal que cuenta la frecuencia de palabras por jugador y fecha
def words_per_match():
    
    palabras_clave=['inmigrant',"..."] # lista de palabras clave
    
    resultados=pd.DataFrame(columns=['Pais','Jugador','Fecha','palabras']) # creamos un DataFrame vacío para almacenar los resultados
    cadena=""
    paises = glob.glob("matches/*") # lista de países (carpetas) donde están almacenados los tweets
    i=0 # contador de filas para el DataFrame
    for pais in paises:
        
        jugadores=glob.glob(f"{pais}/*") # lista de jugadores (archivos .csv) dentro de cada país
        
        for jugador in jugadores:
            tweets=pd.read_csv(jugador) # leemos el archivo de tweets
            del tweets['Unnamed: 0'] # eliminamos la columna 'Unnamed: 0' si existe
            tweets["rawContent"]=tweets["rawContent"].apply(limpiar_tweet) # limpiamos el texto de los tweets
            tweets["date"]=tweets["date"].apply(obtener_fecha) # extraemos la fecha del texto de cada tweet
            palabras_fechas=tweets.groupby('date')["rawContent"] # agrupamos los tweets por fecha
            
            for fecha in palabras_fechas:
                cadena=' '.join(fecha[1]) # unimos todos los tweets de la misma fecha en una cadena de texto

                tokens = word_tokenize(cadena) # convertimos la cadena de texto en una lista de tokens
                
                # Cálculo de la frecuencia de las palabras
                frecuencia = FreqDist(tokens) # usamos la clase FreqDist de NLTK para contar la frecuencia de cada palabra
                
                # guardamos los resultados en el DataFrame, pais-jugador-fecha-frecuencia
                resultados.loc[i] = [pais.split('\\')[-1],jugador.split('\\')[-1],fecha[0], frecuencia] # type: ignore 
                i+=1
        
    return resultados
    
    
    

# Mirar cuales palabras se repiten más en general.

def general_words():
    
    palabras_clave=['inmigrant']
    resultados=pd.DataFrame(columns=['Pais','palabras'])
    cadena=""
    paises = glob.glob("matches/*")
    i=0
    for pais in paises:
        jugadores=glob.glob(f"{pais}/*")
        for jugador in jugadores:
            tweets=(pd.read_csv(jugador))['rawContent'].apply(limpiar_tweet)
            cadena = cadena + (" ".join(tweets.values.tolist())) # type: ignore

    # Tokenización de palabras
    tokens = word_tokenize(cadena)
    
    # Cálculo de la frecuencia de las palabras
    frecuencia = FreqDist(tokens)

    # Obtención de las 10 palabras más frecuentes
    palabras_frecuentes = frecuencia.most_common(10)
    
    print(palabras_frecuentes)



def main():
    resultados=words_per_match()
    print(resultados)
    #general_words()
    
if __name__ == "__main__":
    main()
    



    



    