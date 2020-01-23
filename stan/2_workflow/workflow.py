#!/usr/bin/env python3
# https://mc-stan.org/users/documentation/case-studies/pystan_workflow.html

import pystan
import matplotlib
import matplotlib.pyplot as plt
import numpy as np

import arviz as az

from stan_cache import StanCache

# STAN_FILE = 'eight_schools_cp.stan'

STAN_FILE = 'eight_schools_ncp.stan'
DATA_FILE = 'eight_schools.data.R'
RANDOM_SEED = 194838

DENSITY_PLOT = 'density.png'
PAIRS_PLOT = 'pairs.png'

def save_data():

    data = dict(J = 8, y = [28,  8, -3,  7, -1,  1, 18, 12], 
                sigma = [15, 10, 16, 11,  9, 11, 10, 18])

    pystan.stan_rdump(data, DATA_FILE)

def fit_model():

    save_data()

    model = StanCache(file=STAN_FILE)
    data = pystan.read_rdump(DATA_FILE)

    fit = model.sampling(data=data, seed=RANDOM_SEED,
        control={'adapt_delta': 0.9})

    return fit

def draw_plots(fit):

    az.plot_density(fit, var_names=['mu', 'tau']);
    print('saving fig:', DENSITY_PLOT)
    plt.savefig(DENSITY_PLOT)

    data = az.from_pystan(posterior=fit,
        posterior_predictive='y_hat',
        observed_data=['y'],
        log_likelihood='log_lik',
        coords={'school': np.array(['Choate', 'Deerfield', 'Phillips Andover',
            'Phillips Exeter', 'Hotchkiss', 'Lawrenceville', "St. Paul's",
            'Mt. Hermon'])},
        dims={'theta': ['school'], 'y': ['school'], 'log_lik': ['school'],
            'y_hat': ['school'], 'theta_tilde': ['school']}
    )

    az.plot_pair(data,
        coords={'school': ['Choate', 'Deerfield', 'Phillips Andover']},
        divergences=True
    )

    print('saving fig:', PAIRS_PLOT)
    plt.savefig(PAIRS_PLOT)

def run_diagnostics(fit):

    pystan.diagnostics.check_treedepth(fit, verbose=10, per_chain=True)
    pystan.diagnostics.check_energy(fit, verbose=10)
    pystan.diagnostics.check_div(fit, verbose=10, per_chain=True)

def main():

    fit = fit_model()
    print(fit, '\n')

    draw_plots(fit)

    run_diagnostics(fit)

if __name__ == '__main__':
    main()

# I feel like once you’ve done the 8-schools problem, the rest of Bayesian
# hierarchical modeling is just tinkering with the details.
# - Phil Price
# 
# https://statmodeling.stat.columbia.edu/2014/01/21/everything-need-know-bayesian-statistics-learned-eight-schools/
