import numpy as np
import pandas as pd


def div_sentence(word):
    if word[-1] in '.!?;':
        return 1
    else:
        return 0


def get_raw_df(text):
    df = pd.DataFrame({'word': text.strip().split()})
    df['last_in_sentence'] = df1['word'].apply(div_sentence)
    return df
