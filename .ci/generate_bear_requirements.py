#!/usr/bin/env python3

# This program is free software: you can redistribute it and/or modify it
# under the terms of the GNU Affero General Public License as published by the
# Free Software Foundation, either version 3 of the License, or (at your
# option) any later version.
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
# FITNESS FOR A PARTICULAR PURPOSE.  See the GNU Affero General Public License
# for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import argparse
import itertools
import os
import sys

from pyprint.NullPrinter import NullPrinter

from coalib.bears.BEAR_KIND import BEAR_KIND
from coalib.collecting.Collectors import collect_bears

from dependency_management.requirements.PipRequirement import PipRequirement

PROJECT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

PROJECT_BEAR_DIR = os.path.abspath(os.path.join(PROJECT_DIR, 'bears'))

PINNED_PACKAGES = (
   'radon',
   'click',
)


def get_args():
    parser = argparse.ArgumentParser(
        description='This program generates a pip requirement file for '
                    'installation of linters that are used by the bears.')
    parser.add_argument('--output', '-o',
                        help='name of file to generate, or - for stdout',
                        default=os.path.join(PROJECT_DIR,
                                             'bear-requirements.txt'))
    parser.add_argument('--bear-dirs', '-d', nargs='+', metavar='DIR',
                        help='additional directories which may contain bears')

    args = parser.parse_args()

    return args


def get_all_bears(bear_dirs):
    local_bears, global_bears = collect_bears(
        bear_dirs,
        ['**'],
        [BEAR_KIND.LOCAL, BEAR_KIND.GLOBAL],
        NullPrinter(),
        warn_if_unused_glob=False)
    return list(itertools.chain(local_bears, global_bears))


def get_all_pip_requirements(bears):
    requirements = []

    for bear in bears:
        for requirement in bear.REQUIREMENTS:
            if isinstance(requirement, PipRequirement) and \
               requirement not in requirements:
                requirements.append(requirement)

    return sorted(requirements, key=lambda requirement: requirement.package)


def write_requirements(requirements, output):
    for requirement in requirements:
        if requirement.version:
            marker = '==' if requirement.package in PINNED_PACKAGES else '~='
            output.write('{0}{1}{2}\n'.format(requirement.package,
                                              marker,
                                              requirement.version))
        else:
            output.write(requirement.package + '\n')


if __name__ == '__main__':
    args = get_args()

    bear_dirs = [PROJECT_BEAR_DIR]

    if args.bear_dirs is not None:
        bear_dirs.extend(args.bear_dirs)

    reqs = get_all_pip_requirements(get_all_bears(bear_dirs))

    output = None

    if args.output == '-':
        output = sys.stdout
    else:
        output = open(args.output, 'w')

    write_requirements(reqs, output)
    output.close()
