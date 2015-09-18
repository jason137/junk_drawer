#!/usr/bin/env python3
# author: Jason Dolatshahi

import argparse, sys
from collections import OrderedDict
from operator import attrgetter
import numpy as np

CHAR = '*'
SIG_FIGS = 5

parser = argparse.ArgumentParser(description='quick cmd-line histogram plotter')
parser.add_argument('-b', metavar='num_bins', type=int, nargs='?',
    help='number of bins', default=10)
parser.add_argument('-o', metavar='1/0', type=bool, nargs='?',
    help='omit header row', default=True)
parser.add_argument('-t', metavar='n/e', type=str, nargs='?',
    help='run in test mode (n = normal, e = exp)')
parser.add_argument('infile', nargs='?', type=argparse.FileType('r'),
     help='input file object', default=sys.stdin)
args = parser.parse_args()

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

def main(input_recs, n_bins):

    nonblank_recs = [k for k in input_recs if k != '']
    num_blanks = sum([1 for k in input_recs if k == ''])

    float_values = list(map(float, nonblank_recs))
    bins = get_bins(float_values, n_bins)
    histo = get_histo(bins, float_values)

    print('num_blanks =', num_blanks)
    display_histo(histo)

if __name__ == '__main__':

    n_bins, omit_header, test_mode = attrgetter('b', 'o', 't')(args)
    assert test_mode in ('n', 'e', None)

    # tests
    if test_mode == 'n':
        print('\ntest mode: normal RVs')
        input_recs = 10 * np.random.normal(size=200)

    elif test_mode == 'e':
        print('\ntest mode: exponential RVs')
        input_recs = 10 * np.random.exponential(size=200)

    # get input from stdin
    else:

        input_recs = [k.rstrip() for k in args.infile.readlines()]

        if omit_header:
            header = input_recs.pop(0)
            print(header)

    main(input_recs, n_bins)
