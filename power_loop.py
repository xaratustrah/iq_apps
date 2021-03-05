#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Determine Schottky power vs time and plot
if several files are provided, then they are aligned correctly in time axis according to their time stamp so that the overall result can be plotted on one plot. This can be the case, if you record the lifetime of a very long living beam in the storage ring by doing several short timed measurements. The starting time of the overall measurement is taken from the timestamp of the first file provided in the command line.


2021 Xaratustrah

"""
import os
import sys
import datetime
from iqtools import *


def find_power(iq_object, file_offset):
    # read one second worth of data at the offset go through the file
    iq_object.read_samples(
        int(iq_object.fs), offset=file_offset)

    window = 50000  # Hz
    # lf = 2048
    # nf = int(len(iq_object.data_array) / lf)
    # ff, pp, _ = iq_object.get_fft(
    #     x=iq_object.data_array[0:nf * lf], nframes=nf, lframes=lf)

    ff, pp, _ = iq_object.get_fft()
    # plt.figure()
    # plot_spectrum(ff, pp)
    # plt.plot(ff[pp.argmax() - window], pp[pp.argmax() - window], 'r|')
    # plt.plot(ff[pp.argmax() + window], pp[pp.argmax() + window], 'r|')
    # plt.plot(ff[pp.argmax()], pp[pp.argmax()], 'rv')
    # plt.savefig('plot_{}'.format(file_offset))
    # plt.close()
    return pp[pp.argmax() - window:pp.argmax() + window].sum()


def main():
    results = []

    # Processing the first file
    first_ilename = sys.argv[1]
    print('Processing first file: ' + first_ilename)
    iq = get_iq_object(first_ilename)
    iq.read_samples(1)

    # Datetime is of the kind:
    # 2021 - 02 - 26T23: 22: 13.719023510 - 08: 00

    dt_first_file = datetime.datetime.strptime(
        iq.date_time[:-9], '%Y-%m-%dT%H:%M:%S.%f')

    # make the total length round to one second
    length_total = int(iq.nsamples_total / iq.fs)

    # going inside the first file
    for file_offset in range(length_total):
        iq_pwr = find_power(iq, file_offset)
        results.append([iq_pwr, file_offset, file_offset])

    if (sys.argv) == 2:
        exit()
    # now if more files are there loop through all of them

    for filename in sys.argv[2:]:
        print('Processing file: ' + filename)
        iq = get_iq_object(filename)
        iq.read_samples(1)

        # Datetime is of the kind:
        # 2021 - 02 - 26T23: 22: 13.719023510 - 08: 00

        dt_current_file = datetime.datetime.strptime(
            iq.date_time[:-9], '%Y-%m-%dT%H:%M:%S.%f')

        # make the total length round to one second
        length_total = int(iq.nsamples_total / iq.fs)

        # going through each file
        for file_offset in range(length_total):
            iq_pwr = find_power(iq, file_offset)
            results.append([iq_pwr, int(
                file_offset + (dt_current_file - dt_first_file).total_seconds()), file_offset])

    res_arr = np.array(results)
    # from pprint import pprint
    # pprint(res_arr)
    # plot_spectrum(res_arr[:, 1], res_arr[:, 0], filename='plot')
    np.savetxt('{}_results.csv'.format(first_ilename),
               res_arr[:, 0:2], delimiter=',')
    write_spectrum_to_root(
        res_arr[:, 1], res_arr[:, 0], '{}_results.root'.format(first_ilename))
    plt.figure()
    plt.plot(res_arr[:, 1], res_arr[:, 0], 'ro')
    plt.savefig('{}_results.png'.format(first_ilename))
    plt.close()


# ------------------------
if __name__ == '__main__':
    main()
