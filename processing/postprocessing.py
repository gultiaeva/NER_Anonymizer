import pandas as pd
from processing.preprocessing import DataPreprocessor
import pickle
from joblib import load
from lightgbm import LGBMClassifier


class Predictor():
    def __init__(self, estimator):
        self.data = ''
        self.Preprocessor = DataPreprocessor(self.data)
        self.clf = estimator
        self.encoder = load("processing/binaries/class_encoder.joblib")

    def provide_data(self, data):
        self.data = data
        self.Preprocessor.input = self.data

    def form_answer(self):
        if self.data == '':
            return "No text provided"
        df_4_model, df_words = self.Preprocessor.prepare()
        predictions = self.predict(df_4_model)

        return self.join_full_text(df_words, predictions)

    def join_full_text(self, words, predictions):
        classes = self.encoder.inverse_transform(predictions.astype('int64'))
        out_text = self.data
        for word, cls_ in zip(words.values, classes):
            if word[0] in self.Preprocessor.Worker.stopwords:
                continue
            if cls_ == 'LOC':
                out_text = out_text.replace(word[0], '[LOC]', 1)
            elif cls_ == 'PER':
                out_text = out_text.replace(word[0], '[PER]', 1)
            elif cls_ == 'ORG':
                out_text = out_text.replace(word[0], '[ORG]', 1)

        return out_text

    def predict(self, df):
        predictions = self.clf.predict(df)
        return predictions


if __name__ == '__main__':
    with open('processing/binaries/LGBMClassifier.pkl', 'rb') as f:
        classifier = pickle.load(f)
    text = 'Владимир Путин - молодец'
    pred = Predictor(classifier, text)

    print(pred.form_answer())
