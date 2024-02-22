import glob
from textblob import TextBlob
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import os
import nltk
from langdetect import detect
from nltk.stem import SnowballStemmer
from clean_tweets import *
#from wordcloud import WordCloud
from collections import Counter
from pprint import pprint

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '1'
from nltk.corpus import stopwords

# from nltk.sentiment import SentimentIntensityAnalyzer si quieres usar el
# analizer de mariana

# nueva libreria mas precisa
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

# funcion para contar las palabras en una columna de un dataframe
# retorna las 10 mas comunes, cambiar el 10 si se quieren mas

def contar_palabras(columna):
    contador = Counter(columna)
    return dict(contador.most_common(10))

def analizarglobal():
    os.system('cls')
    files_paths = glob.glob(f"{os.getcwd()}/tweets/all_tweets_all_days/*")
    cantidad_tweets_positivos = 0
    cantidad_tweets_negativos = 0
    cantidad_tweets_neutrales = 0
    data = {'positive_words': [], 'neutral_words': [], 'negative_words': []}
    dataframe_words = pd.DataFrame(data)
    stopwords = {'the', 'and', 'of', 'to', 'a', 'in', 'that', 'is', 'was', 'for', 'it', 'with', 'as', 'on', 'be', 'at',
                 'by', 'this', 'an', 'are', 'or', 'not', 'which', 'but', 'from', "albania", "andorra", "austria",
                 "belarus", "belgium", "bosnia and herzegovina", "bulgaria", "croatia", "cyprus", "czech republic",
                 "denmark", "estonia", "finland", "france", "germany", "greece", "hungary", "iceland", "ireland",
                 "italy", "kosovo", "latvia", "liechtenstein", "lithuania", "luxembourg", "malta", "moldova", "monaco",
                 "montenegro", "netherlands", "north macedonia", "norway", "poland", "portugal", "romania", "russia",
                 "san marino", "serbia", "slovakia", "slovenia", "spain", "sweden", "switzerland", "ukraine",
                 "united kingdom", "vatican city", "algeria", "egypt", "morocco", "tunisia", "western sahara",
                 "armenia", 'russia', '-', ',', '.', ':', ';', '?', 'vs', '!', '%', ')', '(', "v", "the", "and", "a",'=',
                 "to", "in", "that", "it", "with", "for", "is", "on", "was", "at", "by", "an", "be", "this", "which",
                 "or", "but", "not", "are", "from", "they", "we", "say", "her", "she", "will", "he", "his", "have",
                 "has", "had", "been", "one", "all", "there", "their", "what", "so", "up", "out", "if", "about", "who",
                 "get", "which", "go", "me", "when", "make", "can", "like", "time", "no", "just", "him", "know", "take",
                 "people", "into", "year", "your", "good", "some", "could", "them", "see", "other", "than", "then",
                 "now", "look", "only", "come", "its", "over", "think", "also", "back", "after", "use", "two", "how",
                 "our", "work", "first", "well", "way", "even", "new", "want", "because", "any", "these", "give", "day",
                 "most", "us"}

    for f in files_paths:    # Itera sobre los archivos que contienen los tweets
        print(f)
        tweets = pd.read_csv(f, lineterminator='\n',dtype="str")   # Carga el archivo como un dataframe
        tweets = tweets['rawContent']   # Selecciona solo la columna que contiene el texto de los tweets

        tweets = pd.DataFrame(tweets, columns=['rawContent'])   # Crea un nuevo dataframe solo con la columna de texto
        tweets['rawContent'] = tweets['rawContent'].astype(str)  # Convierte el tipo de datos de la columna de texto a string
        tweets['sentiment'] = None   # Crea una columna para el sentimiento de cada tweet y la inicializa con valores nulos

        # Inicializa el analizador de sentimientos
        sentiment_analyzer = SentimentIntensityAnalyzer()

        # Recorre cada tweet y clasifica su sentimiento como positivo, negativo o neutral
        for index, row in tweets.iterrows():
            rawContent = clean_tweet(row['rawContent'])
            sentiment_score = sentiment_analyzer.polarity_scores(rawContent)['compound']
            if sentiment_score >= 0.05:
                tweets.at[index, 'sentiment'] = 'positive'
            elif sentiment_score <= -0.05:
                tweets.at[index, 'sentiment'] = 'negative'
            else:
                tweets.at[index, 'sentiment'] = 'neutral'

        # Cuenta la cantidad de tweets negativos, positivos y neutrales
        negative_tweets = tweets[tweets['sentiment'] == 'negative'].shape[0]
        positive_tweets = tweets[tweets['sentiment'] == 'positive'].shape[0]
        neutral_tweets = tweets[tweets['sentiment'] == 'neutral'].shape[0]

        # Crea una lista con las cantidades
        sentiment_counts = [negative_tweets, positive_tweets, neutral_tweets]

        # Incrementa la cantidad total de tweets negativos, positivos y neutrales
        cantidad_tweets_negativos += sentiment_counts[0]
        cantidad_tweets_positivos += sentiment_counts[1]
        cantidad_tweets_neutrales += sentiment_counts[2]

        # Crea una lista con los textos para cada sentimiento
        positive_texts = tweets[tweets['sentiment'] == 'positive']['rawContent'].tolist()
        positive_text = " ".join(positive_texts)

        neutral_texts = tweets[tweets['sentiment'] == 'neutral']['rawContent'].tolist()
        neutral_text = " ".join(neutral_texts)

        negative_texts = tweets[tweets['sentiment'] == 'negative']['rawContent'].tolist()
        negative_text = " ".join(negative_texts)


        # Crear la nube de palabras y la lista de palabras más comunes para cada sentimiento
        # positive_wordcloud = WordCloud(stopwords=stopwords).generate(positive_text)
        
        # saca las palabras mas comunes  
        n=10
        
        positive_words = [word for word, freq in Counter(positive_text.split()).most_common(n) if word not in stopwords]

        # neutral_wordcloud = WordCloud(stopwords=stopwords).generate(neutral_text)
        neutral_words = [word for word, freq in Counter(neutral_text.split()).most_common(n) if word not in stopwords]

        # negative_wordcloud = WordCloud(stopwords=stopwords).generate(negative_text)
        negative_words = [word for word, freq in Counter(negative_text.split()).most_common(n) if word not in stopwords]

        # ngf = pd.DataFrame({'negative_words': negative_words})
        # npf = pd.DataFrame({'positive_words': positive_words})
        # nepf = pd.DataFrame({'neutral_words': neutral_words})
        # dataframe_words = pd.concat([ngf, npf, nepf, dataframe_words], axis=0)
        
        alcance=min(len(negative_words), len(positive_words),len(neutral_words))
        for i in range(alcance):
            dataframe_words.loc[len(dataframe_words)] = [negative_words[i],neutral_words[i],positive_words[i]] # type: ignore
    os.system('cls')

    # cuenta las palabras ignorando los '0' obviamente
    palabras_negativas = contar_palabras(dataframe_words['negative_words'].tolist())
    palabras_positivas = contar_palabras(dataframe_words['positive_words'].tolist())
    palabras_neutrales = contar_palabras(dataframe_words['neutral_words'].tolist())

    print('Las 5 palabras negativas mas comunes son:', palabras_negativas)
    print('Las 5 palabras positivas mas comunes son:', palabras_positivas)
    print('Las 5 palabras neutrales mas comunes son:', palabras_neutrales)
    suma = cantidad_tweets_negativos + cantidad_tweets_neutrales + cantidad_tweets_positivos

    print(
        f"La proporción de tweets son: positivos {cantidad_tweets_positivos / suma:.3f}, neutrales {cantidad_tweets_neutrales / suma:.3f} y negativos son {cantidad_tweets_negativos / suma:.3f}")

    # Crea un gráfico de torta con los resultados
    # labels = ['Negativos', 'Positivos', 'Neutrales']
    # sentiment_counts=[cantidad_tweets_neutrales,cantidad_tweets_negativos,cantidad_tweets_positivos]
    # plt.pie(sentiment_counts, labels=labels, startangle=90, autopct='%1.1f%%')
    # plt.axis('equal')
    # plt.savefig(os.getcwd())

























