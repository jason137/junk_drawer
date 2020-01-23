#!/usr/bin/env python3

# ex 2
# https://pystan.readthedocs.io/en/latest/avoiding_recompilation.html

import hashlib
import pickle
    
import pystan

STAN_FILE = 'bernoulli.stan'

def StanCache(file=None, model_name=None, model_code=None, **kwargs):

    # get code from string or file
    try:
        assert model_code

    except AssertionError:

        try:
            assert file

        except AssertionError:
            raise

        else:
            with open(file, 'r') as f:
                model_code = f.read()

    code_hash = hashlib.md5(model_code.encode('ascii')).hexdigest()

    # locate cache
    try:
        assert model_name;

    except AssertionError:
        model_name = 'model'

    cache = 'cached-{}-{}.pkl'.format(model_name, code_hash)
        
    # hit cache & write on miss 
    try:
        stan_model = pickle.load(open(cache, 'rb'))

    except FileNotFoundError:

        stan_model = pystan.StanModel(model_code=model_code)

        with open(cache, 'wb') as f:
            pickle.dump(stan_model, f)

        log("caching StanModel instance:  {}".format(model_name))

    else:
        log("using cached StanModel instance")

    return stan_model

def log(k):

    j = "=" * 20
    print('\n', j, k, j)

def model1():

    sm = StanCache(file=STAN_FILE)

    data1 = dict(N=10, y=[0, 1, 0, 1, 0, 1, 0, 1, 1, 1])
    fit = sm.sampling(data=data1)

    print(fit)

def model2():

    sm = StanCache(file=STAN_FILE)

    data2 = dict(N=6, y=[0, 0, 0, 0, 0, 1])
    fit2 = sm.sampling(data=data2)
    print(fit2)

def test():

    model1()    # cache miss!
    model2()    # cache hit!

if __name__ == '__main__':
    main()
