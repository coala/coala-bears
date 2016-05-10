#!/usr/bin/env python3

# Start ignoring PyImportSortBear as imports below may yield syntax errors
from bears import assert_supported_version
assert_supported_version()
# Stop ignoring

import locale
import sys
from os.path import exists
from shutil import copyfileobj
from subprocess import call
from urllib.request import urlopen

import setuptools.command.build_py
from bears import Constants
from setuptools import find_packages, setup
from setuptools.command.test import test as TestCommand

try:
    locale.getlocale()
except (ValueError, UnicodeError):
    locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')


def download(url, filename, overwrite=False):
    """
    Downloads the given URL to the given filename. If the file exists, it won't
    be downloaded.

    :param url:       A URL to download.
    :param filename:  The file to store the downloaded file to.
    :param overwrite: Set to True if the file should be downloaded even if it
                      already exists.
    :return:          The filename.
    """
    if not exists(filename) or overwrite:
        print("Downloading", filename + "...")
        with urlopen(url) as response, open(filename, 'wb') as out_file:
            copyfileobj(response, out_file)
        print("DONE.")

    return filename


class PyTestCommand(TestCommand):

    def run_tests(self):
        # import here, cause outside the eggs aren't loaded
        import pytest
        errno = pytest.main([])
        sys.exit(errno)


class BuildDocsCommand(setuptools.command.build_py.build_py):
    apidoc_command = ('sphinx-apidoc', '-f', '-o', 'docs/API',
                      'bears')
    make_command = ('make', '-C', 'docs', 'html', 'SPHINXOPTS=-W')

    def run(self):
        err_no = call(self.apidoc_command)
        if not err_no:
            err_no = call(self.make_command)
        sys.exit(err_no)


with open('requirements.txt') as requirements:
    required = requirements.read().splitlines()

with open('test-requirements.txt') as requirements:
    test_required = requirements.read().splitlines()

with open("README.rst") as readme:
    long_description = readme.read()


if __name__ == "__main__":
    download('http://sourceforge.net/projects/checkstyle/files/checkstyle/'
             '6.15/checkstyle-6.15-all.jar',
             'bears/java/checkstyle.jar')

    download('https://oss.sonatype.org/content/repositories/releases/org/'
             'scalastyle/scalastyle_2.10/0.8.0/scalastyle_2.10-0.8.0-batch.jar',
             'bears/scala/scalastyle.jar')

    setup(name='coala-bears',
          version=Constants.VERSION,
          description='Bears for coala (Code Analysis Application)',
          author="The coala developers",
          maintainer="Lasse Schuirmann, Fabian Neuschmidt, Mischa Kr\xfcger",
          maintainer_email=('lasse.schuirmann@gmail.com, '
                            'fabian@neuschmidt.de, '
                            'makman@alice.de'),
          url='http://coala.rtfd.org/',
          platforms='any',
          packages=find_packages(exclude=("build.*", "tests", "tests.*")),
          install_requires=required,
          tests_require=test_required,
          package_data={'bears': ["VERSION"],
                        'bears.java': ['checkstyle.jar', 'google_checks.xml'],
                        'bears.scala': ['scalastyle.jar',
                                        'scalastyle_config.xml']},
          license="AGPL-3.0",
          long_description=long_description,
          entry_points={"coalabears": ["coala_official_bears = bears"]},
          # from http://pypi.python.org/pypi?%3Aaction=list_classifiers
          classifiers=[
              'Development Status :: 4 - Beta',

              'Environment :: Console',
              'Environment :: MacOS X',
              'Environment :: Win32 (MS Windows)',
              'Environment :: X11 Applications :: Gnome',

              'Intended Audience :: Science/Research',
              'Intended Audience :: Developers',

              'License :: OSI Approved :: GNU Affero General Public License '
              'v3 or later (AGPLv3+)',

              'Operating System :: OS Independent',

              'Programming Language :: Python :: Implementation :: CPython',
              'Programming Language :: Python :: 3.3',
              'Programming Language :: Python :: 3.4',
              'Programming Language :: Python :: 3.5',
              'Programming Language :: Python :: 3 :: Only',

              'Topic :: Scientific/Engineering :: Information Analysis',
              'Topic :: Software Development :: Quality Assurance',
              'Topic :: Text Processing :: Linguistic'],
          cmdclass={'docs': BuildDocsCommand,
                    'test': PyTestCommand})
