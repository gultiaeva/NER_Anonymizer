import numpy as np
import pandas as pd
from joblib import load
#from processing.workers import Workers
from workers import Workers
import re


class DataPreprocessor():
    def __init__(self, input_data):
        self.input = input_data
        self.Worker = Workers()
        encoders = [load('processing/binaries/part_of_speech_encoder.joblib'),
                    load('processing/binaries/gender_encoder.joblib'),
                    load('processing/binaries/quantity_encoder.joblib'),
                    load('processing/binaries/case_encoder.joblib')]
        self.encoders = encoders

    def _to_df(self, string):
        lasts = np.array([0 if word[-1] in ['.', '!', '?'] else 1
                          for word in string.split()])
        lasts = (lasts == 0).astype('int64')
        words = pd.DataFrame(string.split(), columns=['word'])
        lasts = pd.DataFrame(lasts, columns=['last_in_sentence'])
        self.df_for_model = pd.concat([words, lasts], axis=1)
        self.words = df_words

    def _prepare_for_model(self, df):
        w2v_columns = [f'w2v_{i}' for i in range(1, 301)]

        df['first_in_sentence'] = self.Worker.is_first(df['word'].tolist())
        df['is_capital'] = df['word'].apply(self.Worker.is_capital)
        df['part_of_speech'] = df['word'].apply(self.Worker.get_pos)
        df['gender'] = df['word'].apply(self.Worker.get_gender)
        df['number'] = df['word'].apply(self.Worker.get_number)
        df['case'] = df['word'].apply(self.Worker.get_case)
        df['len'] = df['word'].apply(len)

        df['word'] = df['word'].apply(self.Worker.normalize_text)
        df = df.join(pd.DataFrame(df['word'].apply(self.Worker.vectorize).tolist(),
                                  columns=w2v_columns))
        df = df.drop(columns=['word'])

        new_columns = ['part_of_speech', 'gender',
                       'number', 'case']

        for encoder, name in zip(self.encoders, new_columns):
            df[name] = encoder.transform(df[name])

        df = self.Worker.create_neighbours(df.values)

    def prepare(self):
        if string[-1] != '.':
            string = string + '.'

        self._to_df(self.input)
        self._prepare_for_model(self.df_for_model)
        return self.df_for_model, self.df_words
