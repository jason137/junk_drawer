#!/usr/bin/env python3
import pandas as pd
import pystan
import numpy as np

from random import gauss

from sklearn import linear_model
from sklearn.model_selection import cross_val_score as CV
from sklearn.metrics import mean_squared_error, r2_score

from stan_cache import StanCache

import matplotlib
from matplotlib import pyplot as plt

N = 100
ALPHA, BETA = 1.5, 10

OUTPUT_FILE = 'normals.data.R'
STAN_FILE = 'linreg_1d.stan'
RANDOM_SEED = 194838

INPUT_FILE = 'nyc_parks.tsv'

TRAIN_PCT = 0.8

def _get_synth_data(): 

    xs = range(1, 1 + N)
    ys = [ALPHA + BETA * k + gauss(0, 1) for k in xs]

    data_dict = {'x': xs, 'y': ys}
    return data_dict

def _get_parks_data(input_file=INPUT_FILE):
    k = pd.read_csv(input_file)
    return k

def run_LR(data):

    df = pd.DataFrame(data)
    LR = linear_model.LinearRegression()

    # df.plot.scatter('x', 'y')
    # plt.show()

    train_max = int(TRAIN_PCT * len(df))

    X_train = np.array(df.x[:train_max]).reshape(-1, 1)
    X_test = np.array(df.x[train_max:]).reshape(-1, 1)

    y_train = np.array(df.y[:train_max]).reshape(-1, 1)
    y_test = np.array(df.y[train_max:]).reshape(-1, 1)
    
    LR.fit(X_train, y_train)
    y_pred = LR.predict(X_test)
    
    print("coeffs:", LR.intercept_, LR.coef_)
    print("mse:", mean_squared_error(y_test, y_pred))
    print("r2:", r2_score(y_test, y_pred))

def run_stan(data):

    data['N'] = N

    model = StanCache(file=STAN_FILE)
    fit = model.sampling(data=data, seed=RANDOM_SEED)
    print(fit, '\n')

    pystan.diagnostics.check_treedepth(fit, verbose=10, per_chain=True)
    pystan.diagnostics.check_energy(fit, verbose=10)
    pystan.diagnostics.check_div(fit, verbose=10, per_chain=True)

def main():

    data = _get_synth_data()
    run_stan(data)
    run_LR(data)

if __name__ == '__main__':
    main()
