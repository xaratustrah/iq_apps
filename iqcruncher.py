#!/usr/bin/env python
'''
crunches large number of huge IQ Files

xaratustrah 2022

'''

import argparse
import sys
import os
import time
from datetime import datetime, timedelta
from pathlib import Path
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


def save_as_root(xx, yy, zz, filename, title):
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


def save_as_png(xx, yy, zz, filename, title):
    plot_spectrogram(xx, yy, zz, filename=filename, title=title)


def fake_process(filename):
    print('Sleeping for 30 secs...')
    time.sleep(30)
    with open(filename+'.txt', 'a') as f:
        f.write(filename + ' ' + title)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('filenames', nargs='+', type=str,
                        help='Name of the input files.')
    parser.add_argument('-o', '--outdir', type=str, default='.',
                        help='output directory.')
    parser.add_argument('-p', '--parent', type=str, default='',
                        help='Parent Directory Name, where usually time stamp is, e.g. IQ_2022-05-16_20-49-47')
    parser.add_argument('-d', '--delta', type=int, default=0,
                        help='Delta T between files in seconds')
    parser.add_argument('--fake', action='store_true')

    args = parser.parse_args()

    if args.outdir:
        # handle trailing slash properly
        outfilepath = os.path.join(args.outdir, '')

    for file in args.filenames:
        # create object
        iq_obj = get_iq_object(file)
        outfilename = outfilepath + iq_obj.file_basename
        
        # get file counter from file name
        filecounter = int(Path(file).stem.split('.')[0])
        title = datetime.strftime(datetime.strptime(args.parent, 'IQ_%Y-%m-%d_%H-%M-%S') + timedelta(seconds=args.delta * filecounter), '%Y-%m-%d_%H-%M-%S')
        
        iq_obj.read_complete_file()
        #iq_obj.read_samples(LFRAMES * NFRAMES)

        # convert_to_raw(iq_obj, outfilename)

        xx, yy, zz = make_spectra(iq_obj, outfilename)

        if args.fake:
            fake_process(outfilename, title)
            sys.exit()
        
        save_as_png(xx, yy, zz, outfilename, title)
        #save_as_root(xx, yy, zz, outfilename, title)
            

    # ----------------------------------------


if __name__ == '__main__':
    main()
