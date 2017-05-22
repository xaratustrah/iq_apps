#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Determine and plot delta p over p from Schottky data


2017 Xaratustrah

"""
from iqtools import *
import matplotlib.pyplot as plt

GAMMA = 1.429845848445894  # 124-Xe-54+ @ 400 MeV/u
# GAMMA = 1.1384857688249141  # 238-U-89+ @ 129 MeV/u
GAMMA_T = 2.37  # changed between 2.3 and 2.44


def get_eta(gamma, gamma_t):
    eta = (1 / gamma ** 2) - (1 / gamma_t ** 2)
    return eta


def get_dpp(filename):
    # make a new object
    iq_data = TIQData(filename)

    # read some samples
    iq_data.read_samples(100 * 2 ** 12)

    # make FFT over whole data points
    f, p, _ = iq_data.get_fft()

    # get an estimate of the half power points
    _, delta_idx_fwhm, idx_mhm, idx_phm = IQBase.get_sigma_estimate(f, p)

    # Due to some noise, make in between
    idx_peak = int((idx_mhm + idx_phm) / 2)

    # Clear previous plots
    plt.clf()
    plt.cla()
    plt.close()

    # plot stuff
    plt.plot(f, IQBase.get_dbm(p))
    plt.plot(f[idx_mhm], IQBase.get_dbm(p[idx_mhm]), 'rv')
    plt.plot(f[idx_phm], IQBase.get_dbm(p[idx_phm]), 'kv')
    plt.plot(f[idx_peak], IQBase.get_dbm(p[idx_peak]), 'go')
    plt.xlabel('Freq. [Hz]')
    plt.ylabel('Signal power [dBm]')
    plt.grid()
    filename_woe = os.path.splitext(filename)[0]
    plt.savefig('{}.png'.format(filename_woe))
    fwhm = abs(f[idx_mhm] - f[idx_phm])
    f_peak = f[idx_peak]
    dpop = fwhm / (f_peak + iq_data.center) / get_eta(GAMMA, GAMMA_T)
    print('∆p/p = {}'.format(dpop))


def main():
    for arg in sys.argv[1:]:
        print('Processing file: ' + arg)
        get_dpp(arg)


# ------------------------

if __name__ == '__main__':
    main()
