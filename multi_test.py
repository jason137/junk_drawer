#!/usr/bin/env python
import os
import multiprocessing as mp

CONST = 10

# syntax for using mp module

def worker(file):
    print os.getpid(), file

def f(x):
    return x * x

def g(x, const):
    return x + const

def side_effects(x):
    print x + CONST

def pool_map():
    input = range(10)

    pool = mp.Pool()
    results = pool.map_async(f, input)
    print results.get()

def pool_apply():
    input = range(100)
    results = list()

    pool = mp.Pool()
    k = 10
    for x in input:
        result = pool.apply_async(g, args=(x, k))
        results.append(result.get())
    pool.close()
    pool.join()

    print results

def pool_apply_w_sideff():
    # NOTE order not preserved

    input = range(10)
    pool = mp.Pool()
    for x in input:
        pool.apply_async(side_effects, args=(x, ))  # NOTE still need comma for 1 arg
    pool.close()
    pool.join()

if __name__ == '__main__':
    mp.log_to_stderr(logging.INFO)
    pool_apply_w_sideff()
    # pool_map()

# NOTE seem to need apply_async when func takes args
