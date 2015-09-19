#!/usr/bin/env python3
# author: Jason Dolatshahi
# ref: Tukey, EDA (http://amzn.to/1QMSrWo)

import argparse, sys
from collections import OrderedDict
from operator import attrgetter

from numpy import log, random, sqrt

CHAR = '*'
SIG_FIGS = 5

parser = argparse.ArgumentParser(description='quick cmd-line histogram plotter')
parser.add_argument('infile', nargs='?', type=argparse.FileType('r'),
    help='input file object',
    default=sys.stdin)
parser.add_argument('-b', metavar='num_bins', type=int, nargs='?',
    help='number of bins',
    default=10)
parser.add_argument('-f', metavar='l/s/n', nargs='?', type=str,
    help='nonlinear transf to apply (l = log, s = sqrt, n = negative reciprocal)',
    default='i')
parser.add_argument('-o', metavar='1/0', type=bool, nargs='?',
    help='omit header row (ignored in demo mode)',
    default=True)
parser.add_argument('-x', metavar='n/e/u', type=str, nargs='?',
    help='run with demo data (n = normal, e = exp, u = unif)',
    default=False)

ARGS = ('infile', 'b', 'f', 'o', 'x')
EPS = 0.00001

DEMO_DISTRS = {'n': random.normal, 'e': random.exponential, 'u': random.uniform}
DEMO_NAMES = {'n': 'normal', 'e': 'exp', 'u': 'unif'}
DEMO_SAMPLE_SIZE = 200

TRANSFS = {'l': lambda k: log(k + EPS) if k == 0 else log(k),    # fat log
    's': sqrt,
    'n': lambda k: -1 / k,
    'i': lambda k: k}

TRANSF_NAMES = {'l': 'log', 's': 'sqrt', 'n': 'negative reciprocal',
    'i': 'identity'}


def get_bins(nums, n_bins):
    """create n_bins bins from nums"""

    max_num, min_num = max(nums), min(nums)

    bin_width = (max_num - min_num) / n_bins

    bins = list()
    for k in range(n_bins):

        # bin_lo = int(min_num + k * bin_width)
        # bin_hi = int(min_num + (1 + k) * bin_width)

        bin_lo = round(float(min_num + k * bin_width), 4)
        bin_hi = round(float(min_num + (1 + k) * bin_width), 4)

        bins.append((bin_lo, bin_hi))

    return bins

def get_histo(bins, values):
    """create histogram

    histogram stored as dict:
        key = tuple (corresponding to bin)
        value = string (graphical repn of bin frequency)
    """

    histo = OrderedDict()
    max_value = max(values)
    vals_range = max_value - min(values)

    for bn in bins:

        bn_lo, bn_hi = bn
        bin_size = sum([1 for v in values if bn_lo <= v and v < bn_hi])     # [lo, hi)

        # put max in last bin
        if bn_hi == max_value:
            bin_size += 1

        # TODO scale for large number of recs?
        # histo[bn] = CHAR * int(bin_size / vals_range)    # scaled
        histo[bn] = CHAR * bin_size

    return histo

def sig_figs(k):
    """return k with SIG_FIGS sig figs"""

    # return '%s' % float('%.{}g'.format(SIG_FIGS) % k)
    return float('%.{}g'.format(SIG_FIGS) % k)

def display_histo(histo):
    """format & display histogram"""

    for k, v in histo.items():

        disp_k = str(tuple(map(sig_figs, k)))
        disp_v = str(v)

        try:
            print("{:>25}    {:<}".format(disp_k, disp_v))

        except TypeError:
            print('problem:', disp_k)
            raise

def get_recs(infile, transf_key, omit_header, demo_key):

    transf = TRANSFS[transf_key]

    if demo_key:

        # use random data
        distr = DEMO_DISTRS[demo_key]
        input_recs = distr(size=DEMO_SAMPLE_SIZE)
        header = 'demo: distr = {}'.format(DEMO_NAMES[demo_key])

    else:

        # get input from stdin
        input_recs = [k.rstrip() for k in infile.readlines()]

        if omit_header:
            header = input_recs.pop(0)

    nonblank_recs = [k for k in input_recs if k != '']
    num_blanks = sum([1 for k in input_recs if k == ''])

    float_values = list(map(float, nonblank_recs))
    transf_values = list(map(transf, float_values))

    # side effects
    header += ', transf = {}'.format(TRANSF_NAMES[transf_key])
    print(header)
    print('num_blanks =', num_blanks)

    return transf_values

def main(infile, num_bins, transf_key, omit_header, demo_key):

    recs = get_recs(infile, transf_key, omit_header, demo_key)
    bins = get_bins(recs, num_bins)
    histo = get_histo(bins, recs)

    display_histo(histo)

if __name__ == '__main__':

    args_ns = parser.parse_args()
    args = attrgetter(*ARGS)(args_ns)
    main(*args)
