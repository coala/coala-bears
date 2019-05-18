#!/usr/bin/env python3

import glob
import os
import os.path
import sys

THIS_DIR = os.path.dirname(os.path.abspath(__file__))

PROJECT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

PROJECT_BEAR_DIR = os.path.abspath(os.path.join(PROJECT_DIR, 'bears'))


def main():
    args = sys.argv[1:]
    do_missing = do_all = False
    if args[0] == '--all':
        do_all = True
        args = args[1:]
    elif args[0] == '--missing':
        do_missing = True
        args = args[1:]

    if do_all or do_missing:
        all_bears = glob.glob('{}/**/*.py'.format(PROJECT_BEAR_DIR))
        all_bears = [
            bear[len(PROJECT_DIR) + 1:].replace(os.path.sep, '/')
            for bear in all_bears
            if not bear.endswith('__init__.py')
        ]
        if do_all:
            print(' '.join(sorted(all_bears)))
            return

        all_bears = set(all_bears)

    bears = set()

    for arg in args:
        if arg.startswith('tests/'):
            bear = arg.replace('tests/', 'bears/')
            bear = bear[:bear.find('Test')] + '.py'
        else:
            bear = arg
        bears.add(bear)

    if do_missing:
        bears = all_bears - bears

    print(' '.join(sorted(bears)))


if __name__ == '__main__':
    main()
