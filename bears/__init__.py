"""
coala-bears is a Python package containing all
the bears that are officially supported by coala.
"""


from distutils.version import StrictVersion
import logging
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


def check_coala_version():
    """
    Check the installed coala and coala-bears version.
    """
    try:
        import coalib
        # check only MAJOR.MINOR version
        coalib_version = '.'.join(coalib.__version__.split('.')[:2])
        bears_version = '.'.join(__version__.split('.')[:2])
        if StrictVersion(coalib_version) > StrictVersion(bears_version):
            logging.warning('Version mismatch between coala ({}) and '
                            'coala-bears ({}). This may or may not cause '
                            'errors. If you encounter a problem, try to '
                            'update coala and coala-bears to latest version '
                            "with 'pip3 install -U coala coala-bears'."
                            .format(coalib.__version__, __version__))
    except ImportError:  # pragma: no cover
        logging.error('Module coalib is not found. Cannot do version '
                      'checking.')


check_coala_version()
