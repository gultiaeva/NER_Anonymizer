import os
import re
import numpy as np
import pandas as pd
import pymorphy2
from gensim.models import Word2Vec, KeyedVectors
from functools import lru_cache
import nltk
from joblib import dump, load
from sklearn.preprocessing import LabelEncoder

ru_stopwords = nltk.corpus.stopwords.words('russian')
morph = pymorphy2.MorphAnalyzer()
w2v = KeyedVectors.load('model/my_model')

@lru_cache(maxsize=1000000) # с кешом!
def get_normal_form(i):
    return morph.normal_forms(i)[0]

def normalize_text(x):
    return ' '.join([get_normal_form(i) for i in re.findall('\w+', x) if i not in ru_stopwords])

def vectorise(phrase):
    try:
        return w2v[phrase]
    except KeyError:
        return np.random.normal(0, 1, 300)


def is_capital(word):
    return int(word[0].isupper())


def get_pos(word):
    findall = re.findall(r'[-\w]+', word)
    match = findall[0] if findall else ''
    return str(morph.parse(match)[0].tag.POS) or 'other' 


def get_gender(word):
    findall = re.findall(r'[-\w]+', word)
    match = findall[0] if findall else ''
    return str(morph.parse(match)[0].tag.gender) or 'other' 


def get_number(word):
    findall = re.findall(r'[-\w]+', word)
    match = findall[0] if findall else ''
    return str(morph.parse(match)[0].tag.number) or 'other' 


def get_case(word):
    findall = re.findall(r'[-\w]+', word)
    match = findall[0] if findall else ''
    return str(morph.parse(match)[0].tag.case) or 'other' 

def my_gen(words):
    i = 0
    for word in words:
        if word[-1] not in ['.', '!', '?']:
            yield i
            i += 1
        else:
            yield i
            i = 0
            
def is_first(words):
    positions = np.array([i for i in my_gen(words)])
    return (positions == 0).astype(int)

def create_neighbours(df):
    
    zeros_ = np.zeros(df.shape[1])
    
    left = []
   
    
    right = []
    
    
    for idx, row in enumerate(df):
        
        if row[0] == 1 and row[1] == 1:
            left.append(zeros_)
            right.append(zeros_)

        elif row[1] == 1:
            left.append(zeros_)
            right.append(df[idx + 1])
            
        elif row[0] == 1:
            left.append(df[idx - 1])
            right.append(zeros_)
            
        else: 
            left.append(df[idx - 1])
            right.append(df[idx + 1])
    
    """left.columns = [f'prev_{col}' for col in left.columns]
    right.columns = [f'next_{col}' for col in right.columns]
    
    left = left.reset_index().drop('index', axis=1)
    df = df.reset_index().drop('index', axis=1)
    right = right.reset_index().drop('index', axis=1)"""
    
    left = pd.DataFrame(np.array(left))
    df = pd.DataFrame(np.array(df))
    right = pd.DataFrame(np.array(right))
    
    #return left, df, right
    #return np.hstack([np.hstack([left, df]), right])
    return pd.concat([pd.concat([left, df], axis=1), right], axis=1)
    