import pandas as pd


def join_full_text(df, df_predicted):
    text = []
    for i, word in df.itertuples():
        w, cls = df_predicted.iloc[0, :].values
        if w == word:
            if cls == 'other':
                text.append(word)
            elif cls == 'LOC':
                text.append('[LOC]')
            elif cls == 'PER':
                text.append('[PER]')
            elif cls == 'ORG':
                text.append('[ORG]')
            df_predicted = df_predicted[1:]
        else:
            text.append(word)

    return ' '.join(text)
