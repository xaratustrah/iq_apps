#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Extract values from DCCT / frequency input from NTCAP systme

2021 Xaratustrah

"""
from iqtools import *
import numpy as np
import pandas as pd
import sys
import datetime


def process(filename):
    with open(filename) as f:
        firstline = f.readline()
    first_ts = datetime.datetime.strptime(
        firstline.split('\t')[0], '%Y-%m-%d %H:%M:%S').timestamp()

    with open(filename) as f:
        content = f.readlines()
    dcct = np.array([])
    for line in content:
        ts = datetime.datetime.strptime(line.split(
            '\t')[0], '%Y-%m-%d %H:%M:%S').timestamp()
        val = float(line.split('\t')[1].split()[0])
        dcct = np.append(dcct, [ts - first_ts, ts, val])

    dcct = np.reshape(dcct, (int(len(dcct) / 3), 3))

    df = pd.DataFrame(dcct, columns=list('abc'))

    reduced = df.groupby('a').mean().reset_index().values
    with open('{}.npy'.format(filename), 'wb') as f:
        np.save(f, reduced)
    np.savetxt('{}.csv'.format(filename),
               reduced, delimiter=',')
    write_spectrum_to_root(
        reduced[:, 0], reduced[:, 2], '{}.root'.format(filename))


def main():
    process(sys.argv[1])


# ------------------------
if __name__ == '__main__':
    main()
