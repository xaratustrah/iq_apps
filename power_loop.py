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
from pprint import pprint
from iqtools import *


def find_power(iq_object, file_offset):
    # read one second worth of data at the offset go through the file
    # corresponds to how many frames each 1024 points?
    nframes = int(iq_object.fs / 1024)
    iq_object.read(nframes=1,
                   lframes=int(iq_object.fs), sframes=file_offset)

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
    # results = []
    res_arr = np.array([])

    # Processing the first file
    first_ilename = sys.argv[1]
    print('Processing first file: ' + first_ilename)
    iq = get_iq_object(first_ilename)
    iq.read_samples(1)

    # Datetime is of the kind:
    # 2021 - 02 - 26T23: 22: 13.719023510 - 08: 00

    dt_first_file = datetime.datetime.strptime(
        iq.date_time[:-9], '%Y-%m-%dT%H:%M:%S.%f')
    ts_first_file = round(dt_first_file.timestamp())
    print('Time stamp of the first file:', ts_first_file)
    # make the total length round to one second
    length_total = int(iq.nsamples_total / iq.fs)

    # going inside the first file
    for file_offset in range(length_total):
        iq_pwr = find_power(iq, file_offset)
        # results.append([iq_pwr, file_offset, file_offset])
        res_arr = np.append(res_arr, [file_offset, round(
            dt_first_file.timestamp()) + file_offset, iq_pwr])

    if len(sys.argv) > 2:
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
                ts_current_file = round(dt_current_file.timestamp())
                iq_pwr = find_power(iq, file_offset)
                res_arr = np.append(res_arr, [
                    ts_current_file - ts_first_file + file_offset, ts_first_file + file_offset, iq_pwr])

    res_arr = np.reshape(res_arr, (int(len(res_arr) / 3), 3))
    np.savetxt('{}_results.csv'.format(first_ilename),
               res_arr, delimiter=',')
    write_spectrum_to_root(
        res_arr[:, 0], res_arr[:, 2], '{}_results.root'.format(first_ilename))
    plt.figure()
    plt.plot(res_arr[:, 0], res_arr[:, 2], 'r.')
    plt.grid()
    plt.savefig('{}_results.png'.format(first_ilename))
    plt.close()


# ------------------------
if __name__ == '__main__':
    main()
