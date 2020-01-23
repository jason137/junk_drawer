#!/usr/bin/env python3

# ex 1
# https://pystan.readthedocs.io/en/latest/optimizing.html

import pystan
import numpy as np

ocode = """
data {
    int<lower=1> N;
    real y[N];
}
parameters {
    real mu;
}
model {
    y ~ normal(mu, 1);
}
"""

def main():

    sm = pystan.StanModel(model_code=ocode)
    y2 = np.random.normal(size=20)
    np.mean(y2)
    
    op = sm.optimizing(data=dict(y=y2, N=len(y2)))
    
    op

if __name__ == '__main__':
    main()
