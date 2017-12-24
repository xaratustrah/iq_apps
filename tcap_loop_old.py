#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Process and plot tcap data in a loop

2017 Xaratustrah

"""
import os
import sys
import numpy as np

from iqtools import *
from iqtools import TCAPData

hdr_fiename = './20060113hdr.txt'

nframes = 3000  # about ten seconds
lframes = 1024


def using_matplotlib(filename, cnt):

    iq_data = TCAPData(filename, hdr_fiename)
    # first read
    iq_data.read(nframes=nframes, lframes=lframes, sframes=cnt)

    file_counter = int(iq_data.filename_wo_ext[-3:])
    fs = 312500
    file_length_in_sec = iq_data.nsamples_total / fs
    time_passed_upto_now = (file_counter - 1) * file_length_in_sec

    xx, yy, zz = iq_data.get_spectrogram(nframes=nframes, lframes=lframes)
    delta_t = np.abs(np.abs(yy[1, 0]) - np.abs(yy[0, 0]))

    # extract hour min sec
    hr, placeholder = divmod(cnt * delta_t + time_passed_upto_now, 3600)
    mnt, sec = divmod(placeholder, 60)

    total_time = '{}h-{}m-{}s'.format(int(hr), int(mnt), int(sec))
    title = 'Time: {}:{}:{}'.format(int(hr), int(mnt), int(sec))
    plot_spectrogram(xx, yy, zz, dbm=False, cmap=cm.jet,
                     filename='{}_{}'.format(iq_data.filename_wo_ext, total_time), dpi=500, title=title)


def main():
    for arg in sys.argv[1:]:
        print('Processing file: ' + arg)
        for i in range(1, nframes * 10 * 26, nframes):  # read 6 * 10 sec * 26 = 26 min
            using_matplotlib(arg, i)

# ------------------------


if __name__ == '__main__':
    main()
