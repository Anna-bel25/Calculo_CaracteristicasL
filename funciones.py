import pandas as pd
import numpy as np
import spacy
import nltk
import re
import requests

nlp = spacy.load("es_core_news_sm")
nltk.download('punkt')
nltk.download('stopwords')
from nltk.util import ngrams
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
stop_words_nltk = set(stopwords.words('spanish'))
from nltk.tokenize import sent_tokenize, word_tokenize


# Leer el archivo Excel
morfemas_df = pd.read_excel('D:/XYZ/PHYTON/Calculo_CaracteristicasL/prefijos_sufijos.xlsx')

# Extraer prefijos y sufijos en listas
prefijos = morfemas_df['Prefijos'].dropna().tolist()
sufijos = morfemas_df['Sufijos'].dropna().tolist()

# Función para calcular el número de morfemas
def contar_morfemas(sentence):
    # Tokenizar la oración
    tokens = nlp(sentence)
    morfema_count = 0

    for token in tokens:
        # Contar la raíz
        morfema_count += 1  # La raíz cuenta como un morfema

        # Contar prefijos
        for prefijo in prefijos:
            if token.text.startswith(prefijo):
                morfema_count += 1  # Contar el prefijo como morfema
                break  # Solo contar una vez

        # Contar sufijos
        for sufijo in sufijos:
            if token.text.endswith(sufijo):
                morfema_count += 1  # Contar el sufijo como morfema
                break  # Solo contar una vez

    return morfema_count

# Función para calcular el número de morfemas
# def contar_morfemas(sentence):
#     doc = nlp(sentence)
#     return sum([len(token.morph) for token in doc])
    #return len(doc[0].morph)

# Función para calcular la longitud del lema
def lemma_length(text):
    doc = nlp(text)
    return sum(len(token.lemma_) for token in doc)

# Función para calcular la longitud del lema
def calcular_longitud_lema(palabra):
    doc = nlp(palabra)
    lema = doc[0].lemma_
    return len(lema)

# Obtener stopwords de SpaCy
stop_words_spacy = {token.text for token in nlp.vocab if token.is_stop}
combined_stopwords = stop_words_nltk.union(stop_words_spacy)
# Función para contar stopwords
def count_stopwords(sentence, stop_words):
    tokens = nltk.word_tokenize(sentence)
    stopwords_found = set(token for token in tokens if token in stop_words)
    return len(stopwords_found)


# Función para calcular el puntaje de Flesch
def flesch_reading(text):
    sentences = nltk.tokenize.sent_tokenize(text)
    total_sentences = len(sentences)

    words = nltk.tokenize.word_tokenize(text)
    total_words = len(words)
    
    total_syllables = sum(contar_silabas(word) for word in words)
    
    if total_words == 0 or total_sentences == 0:
        return 0
    
    flesch_score = 206.835 - 1.015 * (total_words / total_sentences) - 84.6 * (total_syllables / total_words)
    return flesch_score

# Función para contar sílabas en una palabra
def contar_silabas(palabra):
    palabra = palabra.lower()
    silabas = re.findall(r'[aeiouáéíóúü]+', palabra)
    return max(1, len(silabas))

# Función para contar palabras en una oración
def contar_palabras(oracion):
    palabras = oracion.split()
    return len(palabras)

# Función para contar oraciones
def contar_oraciones(oracion):
    oraciones = re.split(r'[.!?]+', oracion)
    oraciones = [o for o in oraciones if o.strip()]
    return max(1, len(oraciones))

# Función para calcular el puntaje de Flesch en español
def calcular_flesch(oracion):
    palabras = contar_palabras(oracion)
    oraciones = contar_oraciones(oracion)
    silabas = sum(contar_silabas(palabra) for palabra in oracion.split())
    
    palabras_por_oracion = palabras / oraciones
    silabas_por_palabra = silabas / palabras
    return 206.835 - (1.02 * palabras_por_oracion) - (60 * silabas_por_palabra)

# Función para contar palabras complejas (+3 sílabas)
def contar_palabras_complejas(sentence):
    palabras = word_tokenize(sentence)
    palabras_complejas = [palabra for palabra in palabras if contar_silabas(palabra) > 3]
    return len(palabras_complejas)

# Calcular el índice Gunning-Fog
def calcular_gunning_fog(sentence):
    palabras = word_tokenize(sentence)
    num_palabras = len(palabras)
    num_oraciones = len(sent_tokenize(sentence))
    palabras_complejas = contar_palabras_complejas(sentence)
    
    if num_oraciones > 0 and num_palabras > 0:
        gunning_fog = 0.4 * ((num_palabras / num_oraciones) + 100 * (palabras_complejas / num_palabras))
        return gunning_fog
    else:
        return 0

# Función para contar palabras polisilábicas (+1 sílabas)
def contar_palabras_polisilabicas(sentence):
    palabras = word_tokenize(sentence)
    palabras_polisilabicas = [palabra for palabra in palabras if contar_silabas(palabra) > 1]
    return len(palabras_polisilabicas)

# Calcular el índice SMOG para una oración
def calcular_smog(sentence):
    num_palabras_polisilabicas = contar_palabras_polisilabicas(sentence)
    num_oraciones = len(sent_tokenize(sentence))
    
    if num_oraciones > 0:
        smog = 1.0430 * (num_palabras_polisilabicas * (30 / num_oraciones))**0.5 + 3.1291
        return smog
    else:
        return 0

# Función para contar palabras largas (más de seis letras)
def contar_palabras_largas(sentence):
    palabras = word_tokenize(sentence)
    palabras_largas = [palabra for palabra in palabras if len(palabra) > 6]
    return len(palabras_largas)

# Calcular el índice RIX para una oración
def calcular_rix(sentence):
    num_palabras_largas = contar_palabras_largas(sentence)
    num_oraciones = len(sent_tokenize(sentence))
    
    if num_oraciones > 0:
        rix = num_palabras_largas / num_oraciones
        return rix
    else:
        return 0

# Función para calcular n-grams de caracteres
def calcular_char_ngrams(sentence, n=3):
    sentence = sentence.replace(" ", "").lower()
    ngrams_list = list(ngrams(sentence, n))
    ngrams_list = [''.join(gram) for gram in ngrams_list]
    return ngrams_list

# Función para calcular el número de n-grams de caracteres
def contar_char_ngrams(sentence, n=3):
    sentence = sentence.replace(" ", "").lower()
    ngrams_list = list(ngrams(sentence, n))
    return len(ngrams_list)