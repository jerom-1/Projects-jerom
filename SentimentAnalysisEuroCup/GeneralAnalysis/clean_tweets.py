from alphabet_detector import AlphabetDetector
import preprocessor as tweet_processor
import re
from itertools import groupby

def clean_tweet(tweet):
    # Elimina caracteres especiales y puntuación
    tweet = re.sub(r'[^\w\s]', '', tweet)

    # Elimina URLs
    tweet = re.sub(r'http\S+', '', tweet)

    # Elimina menciones de usuario (@username)
    tweet = re.sub(r'@\w+', '', tweet)

    # Elimina hashtags (#hashtag)
    tweet = re.sub(r'#\w+', '', tweet)

    # Elimina caracteres repetidos
    tweet = re.sub(r'(.)\1+', r'\1\1', tweet)

    # Eliminar menciones a ciudades o estadios (nombre de ciudad o estadio)
    tweet = re.sub(r'\b[A-Z][a-z]+(\s[A-Z][a-z]+)?\b', '', tweet)
    
    # Convierttodo a minúsculas
    tweet = tweet.lower()

    return tweet



