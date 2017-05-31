#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Determine and plot delta p over p from Schottky data


2015 Xaratustrah

"""
import os
import sys

from iqtools import *

GAMMA = 1.429845848445894  # 124-Xe-54+ @ 400 MeV/u
# GAMMA = 1.1384857688249141  # 238-U-89+ @ 129 MeV/u
GAMMA_T = 2.37  # changed between 2.3 and 2.44
LFRAMES = 2 ** 10
NFRAMES = 100


def get_eta(gamma, gamma_t):
    eta = (1 / gamma ** 2) - (1 / gamma_t ** 2)
    return eta


def get_dpp(filename):
    filename_woe = os.path.splitext(filename)[0]
    eta = get_eta(GAMMA, GAMMA_T)
    iq_data = TIQData(filename)
    iq_data.read_samples(1)
    iq_data.window = 'hamming'
    fs = iq_data.fs
    ts = 1 / fs  # in sekunden
    nsamples_total = iq_data.nsamples_total
    zeit = 0
    n_complete_frames = int(nsamples_total / NFRAMES / LFRAMES)

    for ii in range(0, n_complete_frames * NFRAMES * LFRAMES, NFRAMES * LFRAMES):
        iq_data.read_samples(NFRAMES * LFRAMES, offset=ii)

        xx, yy, zz = iq_data.get_spectrogram(NFRAMES, LFRAMES)
        # plot_spectrogram_dbm(xx, yy, zz)
        # plt.savefig('{}_spec.png'.format(filename_woe))

        # plt.clf()
        # plt.cla()
        # plt.close()

        a, b = iq_data.get_time_average_vs_frequency(xx, yy, zz)
        fwhm, f_peak, freqs, powers = IQBase.get_fwhm(a, b, skip=20)

        # plot_dbm_per_hz(a, b)
        # plt.plot(freqs, IQBase.get_dbm(powers), 'ro')
        # plt.savefig('{}_avg.png'.format(filename_woe))

        # print('\neta = {}'.format(eta))
        dpop = fwhm / (f_peak + iq_data.center) / eta
        # print('delta_p/p = {}\n'.format(dpop))

        # Ausgabe in Datei: Zeitpunkt und dpop
        zeit += NFRAMES * LFRAMES * ts
        print(zeit)
        with open('{}.txt'.format(filename_woe), 'a') as outfile:
            outfile.write('{}\t {}\n'.format(zeit, dpop))


def main():
    for arg in sys.argv[1:]:
        print('Processing file: ' + arg)
        get_dpp(arg)


# ------------------------

if __name__ == '__main__':
    main()
