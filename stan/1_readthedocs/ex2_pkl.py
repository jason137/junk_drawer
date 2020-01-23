#!/usr/bin/env python3

# ex 2
# https://pystan.readthedocs.io/en/latest/avoiding_recompilation.html

import pickle
from pystan import StanModel

bernoulli_model = """
    data {
      int<lower=0> N;
      int<lower=0, upper=1> y[N];
    }

    parameters {
      real<lower=0, upper=1> theta;
    }

    model {
      theta ~ beta(0.5, 0.5);  // Jeffreys' prior
      for (n in 1:N)
        y[n] ~ bernoulli(theta);
    }
"""

def model1():

    sm = StanModel(model_code=bernoulli_model)

    data1 = dict(N=10, y=[0, 1, 0, 1, 0, 1, 0, 1, 1, 1])
    fit = sm.sampling(data=data1)

    with open('ex2.pkl', 'wb') as f:
        pickle.dump(sm, f)
    
    print(fit)

def model2():

    sm = pickle.load(open('ex2.pkl', 'rb'))

    data2 = dict(N=6, y=[0, 0, 0, 0, 0, 1])
    fit2 = sm.sampling(data=data2)
    print(fit2)

def main():

    model1()
    model2()

if __name__ == '__main__':
    main()
