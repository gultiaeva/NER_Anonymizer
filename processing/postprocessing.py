import pandas as pd
from processing.preprocessing import foo
import pickle
from joblib import load


with open('processing/binaries/LGBMClassifier.pkl', 'rb') as f:
    classifier = pickle.load(f)

cls_encoder = load("processing/binaries/class_encoder.joblib")

def form_answer(string): 
    df_4_boost, df_words = foo(string)
    predictions = predict(df_4_boost)
    

    return join_full_text(df_words, predictions)


def join_full_text(words, predictions, cls_encoder=cls_encoder):
    classes = cls_encoder.inverse_transform(predictions.astype('int64'))
    text = []
    for word, cls_ in zip(words.values, classes):
        if cls_ == 'other':
            text.append(word[0])
        elif cls_ == 'LOC':
            text.append('[LOC]')
        elif cls_ == 'PER':
            text.append('[PER]')
        elif cls_ == 'ORG':
            text.append('[ORG]')

    return (' '.join(text))


def predict(df):

    predictions = classifier.predict(df)

    return predictions

if __name__ == '__main__':
    form_answer('Владимир Путин')