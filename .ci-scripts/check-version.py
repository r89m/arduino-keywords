#! /usr/bin/env python

from __future__ import print_function

import os
import sys

os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

# get version information
exec(open('../arduinokeywords/version.py').read())

if len(sys.argv) < 2:
    print("Please provide a version string")
    sys.exit(1)

# Make sure given version matches the defined version, otherwise return an error
version = sys.argv[1]
if __version__ != version:
    print("Version mismatch - Expected: {expected}; Actual: {actual}".format(expected=__version__, actual=version))
    sys.exit(1)