"""
coala-bears is a Python package containing all
the bears that are officially supported by coala.
"""


import os
import sys


VERSION_FILE = os.path.join(os.path.dirname(__file__), 'VERSION')
with open(VERSION_FILE, 'r') as ver:
    VERSION = ver.readline().strip()


__version__ = VERSION


def assert_supported_version():  # pragma: no cover
    if sys.version_info < (3, 4):
        print('coala supports only python 3.4 or later.')
        exit(4)
