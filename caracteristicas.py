import pandas as pd
from nltk.corpus import stopwords
from funciones import ( combined_stopwords, contar_silabas, contar_morfemas, 
calcular_longitud_lema, count_stopwords, flesch_reading, calcular_flesch, 
calcular_gunning_fog, calcular_smog, calcular_rix, calcular_char_ngrams, 
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



# Normalizacion del resultado
df['normalized_morpheme_count'] = (df['morpheme_count'] - df['morpheme_count'].min()) / (df['morpheme_count'].max() - df['morpheme_count'].min())
df['normalized_lemma_length'] = (df['lemma_length'] - df['lemma_length'].min()) / (df['lemma_length'].max() - df['lemma_length'].min())
df['normalized_stopwords_count'] = (df['stopwords_count'] - df['stopwords_count'].min()) / (df['stopwords_count'].max() - df['stopwords_count'].min())
df['normalized_word_senses'] = (df['word_senses'] - df ['word_senses'].min()) / (df['word_senses'].max() - df['word_senses'].min())
df['normalized_flesch_score'] = (df['flesch_score'] - df['flesch_score'].min()) / (df['flesch_score'].max() - df['flesch_score'].min())
df['normalized_gunning_fog'] = (df['gunning_fog'] - df['gunning_fog'].min()) / (df['gunning_fog'].max() - df['gunning_fog'].min())
df['normalized_smog_index'] = (df['smog_index'] - df['smog_index'].min()) / (df['smog_index'].max() - df['smog_index'].min())
df['normalized_rix_score'] = (df['rix_score'] - df['rix_score'].min()) / (df['rix_score'].max() - df['rix_score'].min())
df['normalized_total_char_ngrams'] = (df['total_char_ngrams'] - df['total_char_ngrams'].min()) / (df['total_char_ngrams'].max() - df['total_char_ngrams'].min())



# Imprimir un mensaje
print("Se ha calculado la/s características.")

# Mantener las columnas originales y agregar las nuevas en el archivo Excel
with pd.ExcelWriter(file_path, engine='openpyxl', mode='a', if_sheet_exists='overlay') as writer:
    df.to_excel(writer, sheet_name=sheet_name, index=False)

# Guardar el archivo Excel las columnas con resultados sin nomrlaizar
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


#Guardar el archivo Excel las columnas con resultados normalizados
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