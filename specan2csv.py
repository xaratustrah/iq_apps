#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
read specan files and convert them to CSV

2020 Xaratustrah

"""

import sys
import os
from iqtools import tools
import numpy as np


def process(filename):
    filename_base = os.path.basename(filename)
    filename_wo_ext = os.path.splitext(filename)[0]
    ff, pp, units = tools.read_trace_xml(filename)
    a = np.concatenate((ff, pp))
    b = np.reshape(a, (2, -1)).T
    np.savetxt(filename_wo_ext + '.csv', b, header='x [{}]|y [{}]|'.format(
        units[0], units[1]), delimiter='|')


def main():
    for file in sys.argv[1:]:
        process(file)


# ------------------------


if __name__ == '__main__':
    main()
