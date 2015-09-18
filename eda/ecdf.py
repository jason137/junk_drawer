#!/usr/bin/env python3
import sys
from statsmodels.distributions.empirical_distribution import ECDF

import numpy as np
import pandas as pd
from ggplot import *

pd.set_option('display.width', None)

PLOT = 'plot.png'
COLUMN = 'm_first_message_length'

def main(input_file):

    # load & preproc
    data = pd.read_csv(input_file, names=(COLUMN, ))
    print(data.describe())

    total_rows = data.shape[0]
    data = data.dropna(axis=0)
    good_rows = data.shape[0]
    print('na_rows = ', total_rows - good_rows)

    ecdf = ECDF(data[COLUMN])
    ecdf = pd.DataFrame({'x': ecdf.x, 'y': ecdf.y})

    plot = (ggplot(ecdf, aes(x='x', y='y')) + geom_line()
        # + scale_x_log()
        + ylab('ecdf'))

    print(plot)
    ggsave(plot, PLOT)

if __name__ == '__main__':
    input_file = sys.argv[1]
    main(input_file)
