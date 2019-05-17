import numpy as np
import pandas as pd
from joblib import load
from processing.workers import is_capital, is_first, get_case, get_gender, get_normal_form, get_number, get_pos, normalize_text, vectorise, create_neighbours
import pickle
import re


encoders = [load('processing/binaries/part_of_speech_encoder.joblib'),
            load('processing/binaries/gender_encoder.joblib'),
            load('processing/binaries/quantity_encoder.joblib'),
            load('processing/binaries/case_encoder.joblib'), 0]
            


def to_df(string):
    lasts = np.array([0 if word[-1] in ['.', '!', '?'] else 1 for word in string.split()])
    lasts = (lasts == 0).astype(int)
    words = pd.DataFrame(string.split(), columns=['word'])
    lasts = pd.DataFrame(lasts, columns=['last_in_sentence'])
    
    return pd.concat([words, lasts], axis=1), words


def prepare_for_boost(df, encoders=encoders[:-1]):

    w2v_columns = [f'w2v_{i}' for i in range(1, 301)]

    df['first_in_sentence'] = is_first(df.word.tolist())
    df['is_capital'] = df.word.apply(is_capital)
    df['part_of_speech'] = df.word.apply(get_pos)
    df['gender'] = df.word.apply(get_gender)
    df['number'] = df.word.apply(get_number)
    df['case'] = df.word.apply(get_case)
    df['len'] = df.word.apply(len)

    df.word = df.word.apply(normalize_text)
    df = df.join(pd.DataFrame(df.word.apply(vectorise).tolist(), columns=w2v_columns))
    df = df.drop(columns=['word'])

    new_columns = ['part_of_speech', 'gender',
                    'number', 'case']
    
    for encoder, name in zip(encoders, new_columns):
        df[name] = encoder.transform(df[name])
 

    df = create_neighbours(df.values)

    return df

def foo(string):
    if string[-1] != '.':
        string = string + '.'

    df_for_boost, df_words = to_df(string)

    df_for_boost = prepare_for_boost(df_for_boost)

    return df_for_boost, df_words
