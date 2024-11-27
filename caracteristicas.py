import pandas as pd
from nltk.corpus import stopwords
from funciones import ( 
    normalize_column,
    combined_stopwords, 
    contar_silabas, 
    contar_morfemas, 
    calcular_longitud_lema, 
    count_stopwords, 
    flesch_reading, 
    calcular_flesch, 
    calcular_gunning_fog, 
    calcular_smog, 
    calcular_rix, 
    calcular_char_ngrams, 
    contar_char_ngrams, lemma_length
)

# Leer el archivo Excel
file_path = 'D:/XYZ/PHYTON/Calculo_CaracteristicasL/Adminlex_single_train_normalizacion.xlsx' #archivo original
#file_path = 'D:/XYZ/PHYTON/Calculo_CaracteristicasL/Adminlex_single_train_si_normalizacion.xlsx'
#file_path = 'D:/XYZ/PHYTON/Calculo_CaracteristicasL/Adminlex_single_train_no_normalizacion.xlsx'
sheet_name = 'Nivel de Complejidad'
df = pd.read_excel(file_path)
n = 3


# Calculo de las características
df['morpheme_count'] = df['token'].apply(contar_morfemas)
df['lemma_length'] = df['token'].apply(lemma_length)
df['stopwords_count'] = df['sentence'].apply(lambda x: count_stopwords(x, combined_stopwords))
df['word_senses'] = df.groupby('token')['sentence'].transform('nunique')
df['flesch_score'] = df['sentence'].apply(calcular_flesch)
df['gunning_fog'] = df['sentence'].apply(calcular_gunning_fog)
df['smog_index'] = df['sentence'].apply(calcular_smog)
df['rix_score'] = df['sentence'].apply(calcular_rix)
df['total_char_ngrams'] = df['sentence'].apply(lambda x: contar_char_ngrams(x, n))


# Aplicar normalización
df['normalized_morpheme_count'] = normalize_column(df['morpheme_count'])
df['normalized_lemma_length'] = normalize_column(df['lemma_length'])
df['normalized_stopwords_count'] = normalize_column(df['stopwords_count'])
df['normalized_word_senses'] = normalize_column(df['word_senses'])
df['normalized_flesch_score'] = normalize_column(df['flesch_score'])
df['normalized_gunning_fog'] = normalize_column(df['gunning_fog'])
df['normalized_smog_index'] = normalize_column(df['smog_index'])
df['normalized_rix_score'] = normalize_column(df['rix_score'])
df['normalized_total_char_ngrams'] = normalize_column(df['total_char_ngrams'])



# Imprimir un mensaje
print("Se ha calculado la/s características.")

# Definir las columnas originales y las normalizadas
original_columns = [
    'id', 'corpus', 'sentence', 'token', 'complexity',
    'abs_frecuency', 'rel_frecuency', 'length', 'number_syllables',
    'token_possition', 'number_token_sentences', 'number_synonyms',
    'number_hyponyms', 'number_hypernyms', 'Part_of_speech',
    'freq_relative_word_before', 'freq_relative_word_after',
    'len_word_before', 'len_word_after', 'mtld_diversity',
    'propn', 'aux', 'verb', 'adp', 'noun', 'nn', 'sym', 'num'
]

normalized_columns = [
    'normalized_morpheme_count',
    'normalized_lemma_length',
    'normalized_stopwords_count',
    'normalized_word_senses',
    'normalized_flesch_score',
    'normalized_gunning_fog',
    'normalized_smog_index',
    'normalized_rix_score',
    'normalized_total_char_ngrams'
]

new_column_order = original_columns + normalized_columns

# Mantener las columnas originales y agregar las nuevas en el archivo Excel - Normalizadas
with pd.ExcelWriter(file_path, engine='openpyxl', mode='a', if_sheet_exists='overlay') as writer:
    df[new_column_order].to_excel(writer, sheet_name=sheet_name, index=False)


# Mantener las columnas originales y agregar las nuevas en el archivo Excel - Sin Normalizar
# with pd.ExcelWriter(file_path, engine='openpyxl', mode='a', if_sheet_exists='overlay') as writer:
#     df.to_excel(writer, sheet_name=sheet_name, index=False)


# Guardar el archivo Excel las columnas con resultados sin nomrlaizar - Adminlex_single_train_no_normalizacion.xlsx
# df[['id', 'corpus', 'sentence', 'token', 'complexity', 
#     'morpheme_count',
#     'lemma_length',
#     'stopwords_count',
#     'word_senses',
#     'flesch_score',
#     'gunning_fog',
#     'smog_index',
#     'rix_score',
#     'total_char_ngrams',
#     ]].to_excel(file_path, index=False)


#Guardar el archivo Excel las columnas con resultados normalizados - Adminlex_single_train_si_normalizacion.xlsx
# df[['id', 'corpus', 'sentence', 'token', 'complexity', 
#     'normalized_morpheme_count',
#     'normalized_lemma_length',
#     'normalized_stopwords_count',
#     'normalized_word_senses',
#     'normalized_flesch_score',
#     'normalized_gunning_fog',
#     'normalized_smog_index',
#     'normalized_rix_score',
#     'normalized_total_char_ngrams',
#     ]].to_excel(file_path, index=False)