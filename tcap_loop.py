#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Process and plot tcap data in a loop

2017 Xaratustrah

"""
import sys
import numpy as np

import matplotlib
matplotlib.use('Agg')

from iqtools import *
from iqtools import TCAPData


def process(hdr_fiename, filename):
    iq_data = TCAPData(filename, hdr_fiename)
    file_counter = int(iq_data.filename_wo_ext[-3:])
    fs = 312500
    file_length_in_sec = 15625 * 32768 / fs
    time_passed_upto_now = (file_counter - 1) * file_length_in_sec

    # extract hour min sec
    hr, placeholder = divmod(time_passed_upto_now, 3600)
    mnt, sec = divmod(placeholder, 60)
    total_time = '{}h-{}m-{}s'.format(int(hr), int(mnt), int(sec))
    title = 'Time: {}:{}:{}'.format(int(hr), int(mnt), int(sec))

    zz = np.array([])
    for j in range(1, 780 * 2 * 10 + 1, 2 * 10):
        data = np.array([])
        # read 2*10 i.e. 20 blocks
        for i in range(j, j + 2 * 10):
            data = np.append(data, iq_data.read_block(i))
        data = np.reshape(data, (10, 32768 * 2))
        data_fft = np.fft.fft(data, axis=1)
        data_fft = np.average(data_fft, axis=0)
        data_fft = np.abs(np.fft.fftshift(data_fft))
        zz = np.append(zz, data_fft)

    zz = np.reshape(zz, (780, 32768 * 2))
    data_fft_freqs = np.fft.fftshift(
        np.fft.fftfreq(32768 * 2, d=1 / fs))  # in Hz
    xx, yy = np.meshgrid(data_fft_freqs, np.arange(780))
    yy = yy * 2.10  # in seconds
    plt_filename = '{}_{}'.format(iq_data.filename_wo_ext, total_time)
    print('Printing into file: ' + plt_filename)
    plot_spectrogram(xx, yy, zz, dbm=False, cmap=cm.jet,
                     filename=plt_filename, dpi=500, title=title)


def main():
    hdr = sys.argv[1]
    for arg in sys.argv[2:]:
        print('Processing file: ' + arg)
        print('Using header: ' + hdr)
        process(hdr, arg)

# ------------------------


if __name__ == '__main__':
    main()
