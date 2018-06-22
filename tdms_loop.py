#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Process and create TDMS spectrogram in a loop from several files

2018 Xaratustrah

"""

import matplotlib
matplotlib.use('Agg')  # import before all others
import sys
import numpy as np
import iqtools
import matplotlib.pyplot as plt
import matplotlib.cm as cm
from matplotlib.colors import LogNorm

lframes = 2**21  # samples
zoom_window = 10000  # bins
vmin, vmax = 300, 3000  # contrast


def process(nframes, filenames):
    nfiles = len(filenames)
    print('Processing', nfiles, 'files in total')
    print('Number of frames from each:', nframes)

    iqdata = iqtools.TDMSData(filenames[0])

    # read one frame from the first file
    iqdata.read(nframes=1, lframes=lframes)

    # ff, pp, _ = iqdata.get_fft()
    pp = np.abs(np.fft.fftshift(np.fft.fft(iqdata.data_array)))
    ff = np.fft.fftshift(np.fft.fftfreq(lframes, 1 / iqdata.fs))

    zoom = slice(np.argmax(pp) - int(zoom_window / 2),
                 np.argmax(pp) + int(zoom_window / 2))

    peak = np.max(pp)

    plt.plot(ff / 1e6, pp / peak)
    plt.plot(ff[zoom] / 1e6, pp[zoom] / peak)
    plt.grid()
    plt.ylabel('Normalized power [a.u.]')
    plt.xlabel('Freq. [MHz]')
    plt.title(filenames[0])
    plt.savefig(filenames[0] + '_1d.png', dpi=300, bbox_inches='tight')
    plt.close()

    # background mesh. x is as long as the frame length
    # y is as long as number of frames * number of files + another dummy row
    # needed for concatenation

    xx, yy = np.meshgrid(ff, np.arange(nframes * nfiles + 1) *
                         lframes / iqdata.fs)

    # dummy row for concatenation
    zztotal = np.zeros((1, lframes))

    for ii in range(nfiles):
        iqdata = iqtools.TDMSData(filenames[ii])
        print('Current file: ', filenames[ii])

        # now read the rest: either only a part
        if nframes == 512:
            iqdata.read_complete_file()
        else:
            iqdata.read(nframes=nframes, lframes=lframes, sframes=1)

        dd = np.reshape(iqdata.data_array, (nframes, lframes))
        zz = np.fft.fft(dd, axis=1)
        #zz = (np.abs(np.fft.fftshift(zz, axes=1)) / np.sqrt(2))**2 / 50
        zz = np.abs(np.fft.fftshift(zz, axes=1))**2
        # concat on top of the previous one
        zztotal = np.concatenate((zz, zztotal))

    print('Shapes of xx, yy, zz and zztotal: ', np.shape(
        xx), np.shape(yy), np.shape(zz), np.shape(zztotal))
    print('Now plotting...')
    print('Plot shape:', np.shape(xx[:, zoom]))

    zztemp = zztotal[:, zoom]  # / np.max(zztotal)
    # zztemp[zztemp < 0.1] = 0
    sp = plt.pcolormesh(xx[:, zoom] / 1e3, yy[:, zoom], zztemp,
                        # norm=LogNorm(vmin=vmin,
                        #              vmax=vmax),
                        cmap=cm.PuBu)
    # cmap=cm.Greys)
    #cb = plt.colorbar(sp)
    #cb.set_label('Normalized power [a.u.]')
    plt.ylabel('Time [s]')
    plt.xlabel('Frequency [kHz]')
    plt.title('{} - {}'.format(filenames[0], filenames[-1]))
    plt.savefig('spec_{}_{}.png'.format(
        filenames[0], filenames[-1]), dpi=150, bbox_inches='tight')
    plt.close()


def main():
    process(int(sys.argv[1]), sys.argv[2:])

# ------------------------


if __name__ == '__main__':
    main()
