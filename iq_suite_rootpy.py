#!/usr/bin/env python
"""
Using iq_suite together with rootpy (based on CERN ROOT Package)

type:
    source `which thisroot.sh`
before running this code.

For more information please refer to:

https://gist.github.com/xaratustrah/4efc5001f1bbcce47e02e2343ba29b87
http://www.rootpy.org/
https://root.cern.ch/
https://root.cern.ch/pyroot


Xaratustrah

2016

Tested with:

Python 3.4.5 +readline and root v. 6.06/08 +python34 from Macports on OSX 10.11.6 El Capitan
Latest ndawe/rootpy from GitHUB

"""

print(__doc__)

# note that currently matplotlib import freezes the output of rootpy. matplotlib import
# is included in Spectrum package which is in turn imported in iqbase. So we only import tiqdata

import argparse
from iqtools import *
from rootpy.plotting import Hist, Canvas, Legend
from rootpy.interactive import wait
import numpy as np


def do_stuff(file_name, plot=True):
    tiq_data = TIQData(file_name)
    NFRAMES = 100
    LFRAMES = 1024

    tiq_data.read(nframes=NFRAMES, lframes=LFRAMES, sframes=1)
    center = tiq_data.center

    # do fft
    ff, pp, _ = tiq_data.get_fft()

    freq_lower = center + ff[0] / 1e6
    freq_upper = center + ff[-1] / 1e6

    # create hist
    h1 = Hist(NFRAMES * LFRAMES, freq_lower, freq_upper, name='h1', title='Frequency Spectrum',
              drawstyle='hist',
              legendstyle='F',
              fillstyle='/',
              linecolor='green')

    for i in range(len(pp)):
        h1.set_bin_content(i, pp[i])

    # set visual attributes
    h1.GetXaxis().SetTitle('Freuqency [MHz]')
    h1.linecolor = 'green'
    # h1.fillcolor = 'green'
    # h1.fillstyle = '/'

    if plot:
        # plot
        c = Canvas(name='c1', width=700, height=500)
        c.set_left_margin(0.15)
        c.set_bottom_margin(0.15)
        c.set_top_margin(0.10)
        c.set_right_margin(0.05)
        c.toggle_editor()
        c.toggle_event_status()
        c.toggle_tool_bar()
        # c.set_crosshair()

        h1.Draw()

        # create the legend
        legend = Legend([h1], pad=c,
                        header='Header',
                        leftmargin=0.05,
                        rightmargin=0.5)
        legend.Draw()

        # wait for key press
        wait()


# ------------------
if __name__ == '__main__':
    parser = argparse.ArgumentParser(prog='analysis')
    parser.add_argument('infile', nargs=1, type=str, help='Input file')
    parser.add_argument('--plot', action='store_true', help='Start server')
    parser.set_defaults(plot=False)

    args = parser.parse_args()

    file_name = args.infile[0]

    if args.plot:
        do_stuff(file_name)

    else:
        do_stuff(file_name, False)
