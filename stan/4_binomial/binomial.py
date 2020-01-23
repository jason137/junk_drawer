#!/usr/bin/env python3

import pandas as pd

import pystan
import stan_utils

INPUT_FILE = 'EfronMorrisBB.txt'
USECOLS = ['FirstName', 'LastName', 'Hits', 'At-Bats', 'RemainingAt-Bats',
    'SeasonHits']

RANDOM_SEED = 194838
PROBS = (0.05, 0.1, 0.5, 0.9, 0.95)

FULL_POOLING_FILE = 'full_pooling.stan'
NO_POOLING_FILE = 'no_pooling.stan'
PARTIAL_POOLING_FILE = 'partial_pooling.stan'

LOG_ODDS_CP_FILE = 'log_odds_cp.stan'
LOG_ODDS_NCP_FILE = 'log_odds_ncp.stan'

def get_data(input_file=INPUT_FILE):

    k = pd.read_csv(input_file, sep='\t', usecols=USECOLS)
    k['RemainingHits'] = k.SeasonHits - k.Hits

    k_dict = {'N': len(k),
        'K': k['At-Bats'],                   # observed trials
        'y': k['Hits'],                      # observed successes
        'K_new': k['RemainingAt-Bats'],      # test trials
        'y_new': k['RemainingHits']}         # test successes

    # goal = estimate batting avg in remaining at bats 

    return k_dict

def run_stan(data, stan_file):

    # smaller stepsize, higher acceptance rate helps convergence
    # divergence <-> too much posterior curvature 

    model = stan_utils.StanCache(file=stan_file)

    fit = model.sampling(data=data, seed=RANDOM_SEED
        , control={'stepsize': 0.01, 'adapt_delta': 0.99}
    )

    print(stan_utils.stan_summary(fit, probs=PROBS), '\n')

    pystan.diagnostics.check_treedepth(fit, verbose=10, per_chain=True)
    pystan.diagnostics.check_energy(fit, verbose=10)
    pystan.diagnostics.check_div(fit, verbose=10, per_chain=True)

def main():

    data = get_data()

    # run_stan(data, FULL_POOLING_FILE)
    # run_stan(data, NO_POOLING_FILE)
    # run_stan(data, PARTIAL_POOLING_FILE)

    # run_stan(data, LOG_ODDS_CP_FILE)
    run_stan(data, LOG_ODDS_NCP_FILE)

if __name__ == '__main__':
    main()
