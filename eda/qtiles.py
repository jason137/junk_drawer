#!/usr/bin/env python3
import fileinput
import numpy as np

QTILES = (0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100)

def _test():
    for line in fileinput.input():
        print(line.rstrip())

def main(header=True):

    input_stream = [line.rstrip() for line in fileinput.input()]

    recs = [k for k in input_stream if k != '']
    num_blanks = sum([1 for k in input_stream if k == ''])

    if header:
        values = recs[1: ]
    else:
        values = recs

    np_vals = np.array(values, dtype=float)

    for k in QTILES:
        print(k, '\t', np.percentile(np_vals, k))

    print('num blanks = ', num_blanks)

if __name__ == '__main__':

    main()
