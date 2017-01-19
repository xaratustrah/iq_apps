#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Determine and plot delta p over p from Schottky data


2015 Xaratustrah

"""
from iqtools import *
import sys, os

# GAMMA = 1.429845848445894  # 124-Xe-54+ @ 400 MeV/u
GAMMA = 1.1384857688249141  # 238-U-89+ @ 129 MeV/u
GAMMA_T = 2.44  # changed between 2.3 and 2.44

LFRAMES = 2 ** 12
NFRAMES = 100


def get_eta(gamma, gamma_t):
    eta = (1 / gamma ** 2) - (1 / gamma_t ** 2)
    return eta


def get_dpp(filename):
    iq_data = TIQData(filename)
    # iq_data.read(NFRAMES, LFRAMES, 1)
    iq_data.read_samples(NFRAMES * LFRAMES, offset=0)
    iq_data.window = 'hamming'

    filename_woe = os.path.splitext(filename)[0]

    xx, yy, zz = iq_data.get_spectrogram(NFRAMES, LFRAMES)
    plot_spectrogram_dbm(xx, yy, zz)
    plt.savefig('{}_spec.png'.format(filename_woe))

    plt.clf()
    plt.cla()
    plt.close()

    a, b = iq_data.get_time_average_vs_frequency(xx, yy, zz)
    fwhm, f_peak, freqs, powers = IQBase.get_fwhm(a, b, skip=20)

    plot_dbm_per_hz(a, b)
    plt.plot(freqs, IQBase.get_dbm(powers), 'ro')
    plt.savefig('{}_avg.png'.format(filename_woe))

    eta = get_eta(GAMMA, GAMMA_T)

    print('eta = {}'.format(eta))

    dpop = fwhm / (f_peak + iq_data.center) / eta
    print('∆p/p = {}'.format(dpop))


def main():
    get_dpp(sys.argv[1])


# ------------------------

if __name__ == '__main__':
    main()
