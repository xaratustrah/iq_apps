#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Process wire measurement

'''

import os
import sys

from iqtools import *

n_samples = 6000000
result_file_name = 'result.csv'


def do_it(filename):
    iq = get_iq_object(filename)
    iq.read_samples(n_samples)
    ff, pp, _ = iq.get_fft()
    # change here for range, like ff[:] and pp[:]
    plot_spectrum(ff, pp)
    plt.plot(ff[pp.argmax()], pp[pp.argmax()], 'rv')
    plt.savefig(filename + '.png')
    write_spectrum_to_csv(ff, pp, filename='{}.csv'.format(filename))
    return ff[pp.argmax()], pp[pp.argmax()]


def main():
    for filename in sys.argv[1:]:
        print('Processing file: ' + filename)
        with open(result_file_name, 'a') as f:
            f.write('|'.join(map(str, do_it(filename))) + '\n')


# ------------------------

if __name__ == '__main__':
    main()
