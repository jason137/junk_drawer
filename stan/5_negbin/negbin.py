#!/usr/bin/env python3

import pandas as pd
from sklearn.preprocessing import OneHotEncoder as OH

import pystan
import stan_utils

INPUT_FILE = 'ceb.tsv'
USECOLS = ['dur', 'res', 'educ', 'y']
TARGET = 'y'


def load_data():
    return pd.read_csv(INPUT_FILE, sep='\t', usecols=USECOLS)


def preproc(X):

    OH_fit = OH(drop='first').fit(X)

    ks = OH_fit.get_feature_names()
    vs = OH_fit.transform(X)

    return pd.DataFrame(vs.toarray(), columns=ks).astype(int)


def main():

    data = load_data()
    print(data.head())

    _X, y = data.drop(TARGET, axis=1), data[TARGET]
    X = preproc(_X)
    print(X.head())
    
    pass


if __name__ == '__main__':
    pd.set_option('max.rows', None)
    pd.set_option('max.columns', None)
    main()

# https://data.princeton.edu/wws509/r/c4s1
