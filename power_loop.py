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


def find_power(data):
    return 42


def main():
    results = []

    # Processing the first file
    filename = sys.argv[1]
    print('Processing file: ' + filename)
    if filename.lower().endswith('tiq'):
        iq = TIQData(filename)
        iq.read_samples(1)

    if filename.lower().endswith('iqt'):
        iq = IQTData(filename)
        iq.read_samples(1)

    # Datetime is of the kind:
    # 2021 - 02 - 26T23: 22: 13.719023510 - 08: 00

    dt_first_file = datetime.datetime.strptime(
        iq.date_time[:-9], '%Y-%m-%dT%H:%M:%S.%f')

    # make the total length round to one second
    length_total = int(iq.nsamples_total / iq.fs)

    # going inside the file
    for file_offset in range(length_total):

        # read one second worth of data at the offset go through the file
        iq.read_samples(int(iq.fs))

        # do something with those data
        iq_pwr = find_power(iq.data_array)

        # save results in an array
        results.append([iq_pwr, file_offset, int(file_offset)])

    if (sys.argv) == 2:
        exit()
    # now if more files are there
    # looping through all remaining files
    for filename in sys.argv[2:]:
        print('Processing file: ' + filename)
        if filename.lower().endswith('tiq'):
            iq = TIQData(filename)
            iq.read_samples(1)

        if filename.lower().endswith('iqt'):
            iq = IQTData(filename)
            iq.read_samples(1)

        # Datetime is of the kind:
        # 2021 - 02 - 26T23: 22: 13.719023510 - 08: 00

        dt = datetime.datetime.strptime(
            iq.date_time[:-9], '%Y-%m-%dT%H:%M:%S.%f')

        # make the total length round to one second
        length_total = int(iq.nsamples_total / iq.fs)

        # going through each file
        for file_offset in range(length_total):

            # read one second worth of data at the offset go through the file
            iq.read_samples(int(iq.fs))

            # do something with those data
            iq_pwr = find_power(iq.data_array)

            # save results in an array
            # print(iq_pwr, file_offset, int(file_offset + (dt - dt_first_file).total_seconds()),
            #       dt_first_file, dt, dt + datetime.timedelta(seconds=file_offset))
            results.append([iq_pwr, file_offset, int(file_offset +
                                                     (dt - dt_first_file).total_seconds())])
    from pprint import pprint
    pprint(results)


# ------------------------
if __name__ == '__main__':
    main()
