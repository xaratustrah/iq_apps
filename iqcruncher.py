#!/usr/bin/env python
'''
crunches large number of huge IQ Files

xaratustrah 2022

'''

import argparse
import sys
import os
from iqtools import *

LFRAMES = 2**18
NFRAMES = 4096
AVG = 8
ZZMAX = 20000

# ------------ MAIN ----------------------------


def convert_to_raw(iq_obj, outfilename):
    iq_obj.read_samples(LFRAMES * NFRAMES)
    # iq_obj.read_complete_file()
    write_signal_to_bin(iq_obj.data_array, outfilename,
                        fs=0, center=0, write_header=False)


def make_spectra(iq_obj, outfilename):
    xx, yy, zz = iq_obj.get_spectrogram(lframes=LFRAMES, nframes=NFRAMES)
    xx, yy, zz = get_averaged_spectrogram(xx, yy, zz, every=AVG)
    plot_spectrogram(xx, yy, zz, filename=outfilename, zzmax=ZZMAX)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('filenames', nargs='+', type=str,
                        help='Name of the input files.')
    parser.add_argument('-o', '--outdir', type=str, default='.',
                        help='output directory.')

    args = parser.parse_args()

    if args.outdir:
        # handle trailing slash properly
        outfilepath = os.path.join(args.outdir, '')

    for file in args.filenames:
        iq_obj = get_iq_object(file)
        outfilename = outfilepath + iq_obj.file_basename
        convert_to_raw(iq_obj, outfilename)
        make_spectra(iq_obj, outfilename)

    # ----------------------------------------


if __name__ == '__main__':
    main()
