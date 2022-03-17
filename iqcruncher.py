#!/usr/bin/env python
'''
crunches large number of huge IQ Files

xaratustrah 2022

'''

import argparse
import sys
import os
from iqtools import *
from ROOT import TCanvas, TFile


LFRAMES = 2**18
NFRAMES = 4096
AVG = 8
ZZMAX = 20000
ZZ_CUT = 27

# ------------ MAIN ----------------------------


def convert_to_raw(iq_obj, outfilename):
    #iq_obj.read_samples(LFRAMES * NFRAMES)
    # iq_obj.read_complete_file()
    write_signal_to_bin(iq_obj.data_array, outfilename,
                        fs=0, center=0, write_header=False)


def make_spectra(iq_obj, outfilename):
    xx, yy, zz = iq_obj.get_spectrogram(lframes=LFRAMES, nframes=NFRAMES)
    xx, yy, zz = get_averaged_spectrogram(xx, yy, zz, every=AVG)
    zz[zz > ZZ_CUT] = ZZ_CUT
    return xx, yy, zz


def save_as_root(xx, yy, zz, filename):
    h3 = get_root_th2d(xx, yy, zz)
    c = TCanvas('', '', 800, 600)
    c.Divide(1, 2)
    c.cd(1)
    h3.Draw('zcol')
    c.cd(2)
    h3.ProjectionX().DrawClone()
    c.Draw()
    ff = TFile(filename + '.root', 'RECREATE')
    h3.Write()
    h3.ProjectionX().Write()
    ff.Close()


def save_as_png(xx, yy, zz, filename):
    plot_spectrogram(xx, yy, zz, filename=filename, title='')


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
        # create object
        iq_obj = get_iq_object(file)
        outfilename = outfilepath + iq_obj.file_basename

        iq_obj.read_complete_file()
        #iq_obj.read_samples(LFRAMES * NFRAMES)

        # convert_to_raw(iq_obj, outfilename)

        xx, yy, zz = make_spectra(iq_obj, outfilename)

        save_as_png(xx, yy, zz, outfilename)

        save_as_root(xx, yy, zz, outfilename)

    # ----------------------------------------


if __name__ == '__main__':
    main()
