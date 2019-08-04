#!/usr/bin/env python3

import glob
import os
import os.path
import sys

from ruamel.yaml import YAML

yaml = YAML()
THIS_DIR = os.path.dirname(os.path.abspath(__file__))

PROJECT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

IS_WIN = os.name == 'nt'

# Clang DLLs x64 were nowadays installed, but the x64 version hangs, so we
# exclude according tests. See https://github.com/appveyor/ci/issues/495 and
# https://github.com/appveyor/ci/issues/688

WINDOWS_BROKEN = set((
    'bakalint',  # not installed
    'phpcs',  # https://github.com/coala/coala-bears/issues/2916
    'mcs',  # choco mono isnt providing this in the PATH
    'tailor',  # installer fails
    'shellcheck',  # https://github.com/coala/coala-bears/issues/2920
    # pip
    'apertium_lint',  # https://gitlab.com/jpsinghgoud/apertium-lint/issues/5
    'bandit',  # RuntimeError: Unable to output report using 'json' formatter
    'clang',  # see note above
    'cppclean',  # https://github.com/myint/cppclean/issues/120
    'scspell',  # https://github.com/coala/coala-bears/issues/2926
    'vint',  # https://github.com/Kuniwak/vint/issues/290
    # gem
    'csvlint',  # https://github.com/coala/coala-bears/issues/2909
    'sqlint',  # https://github.com/coala/coala-bears/issues/2923
    # npm ; try different version
    'alex',  # https://github.com/coala/coala-bears/issues/2922
    'coffeelint',  # Extra windows results
    'csscomb',   # Linter errors
    'dockerfile_lint',  # test case bug
    'elm-format',  # https://github.com/coala/coala-bears/issues/2925
    'gherkin',  # result json decode exception
    'jshint',  # test case bug
    'remark',  # remark result text difference due to unicode
    'postcss',  # https://github.com/coala/coala-bears/issues/2921
    'sass-lint',  # rule `!important not allowed` not trigger
    'textlint',  # Unexpected extra result in test
    # Also textlint plugin for asciidoc requires a compiler.
    # and should be replaced with plugin asciidoctor which does
    # not need a compiler

    # No information from linter bear
    'eslint',  # Two of tests fail
    'tslint',  # Half of tests fail
))


DISABLE_BEARS = set(os.environ.get('DISABLE_BEARS', '').split(' '))


def get_metadata():
    with open('bear-metadata.yaml') as f:
        metadata = yaml.load(f)

    return metadata['bear_metadata']


def get_bears(metadata, args, include_disabled=False):
    bears = []

    for arg in args:
        for bear in metadata.values():
            tags = set(bear['tags'])

            if tags.intersection(DISABLE_BEARS):
                tags.add('disabled')

            if IS_WIN and tags.intersection(WINDOWS_BROKEN):
                tags.add('disabled')

            if arg in tags and (include_disabled or 'disabled' not in tags):
                bears.append(bear)

    return bears


CLANG_EXTRA_TESTS = [
    'tests/c_languages/codeclone_detection/ClangCountingConditionsTest.py',
    'tests/c_languages/codeclone_detection/ClangCountVectorCreatorTest.py',
    'tests/c_languages/codeclone_detection/CountVectorTest.py',
    'tests/c_languages/codeclone_detection/CloneDetectionRoutinesTest.py',
]


def get_tests(bears):
    # Add 1 for the path separator after bears
    project_dir_prefix_len = len(PROJECT_DIR) + 1

    tests = set()
    for bear in bears:
        name = bear['name']
        if name.startswith('_'):
            continue
        subdir = bear['subdir']
        # A few test modules are FoobearSomethingTest.py, like
        # PySafetyBearWithoutMockTest.py
        testpath = os.path.join('tests', subdir, '{}*Test.py'.format(name))
        files = glob.glob(testpath)
        for filename in files:
            filename = filename.replace(os.path.sep, '/')
            if filename.startswith('/'):
                filename = filename[project_dir_prefix_len:]
            tests.add(filename)

        if subdir == 'c_languages/codeclone_detection':
            tests.update(CLANG_EXTRA_TESTS)

        elif subdir.startswith('vcs'):
            tests.add('tests/vcs/CommitBearTest.py')

    return tests


def get_pytest_deselected_tests(args, tests):
    not_list = []

    # language-check fails for different locale on windows
    if 'tests/documentation/DocGrammarBearTest.py' in tests:
        if 'win' in args:
            not_list.append('test_language_french')

    # async is not available on Python 3.4
    if 'tests/python/YapfBearTest.py' in tests:
        if 'py34' in args:
            not_list.append('test_valid_async')

    # https://github.com/coala/coala-bears/issues/2943
    if 'tests/php/PHPMessDetectorBearTest.py' in tests:
        not_list.append('test_cleancode_violation')

    return not_list


def main():
    args_orig = sys.argv[1:]
    metadata = get_metadata()

    include_disabled = False
    show_deselected = False
    if args_orig[0] == '--disabled':
        include_disabled = True
        args_orig = args_orig[1:]
    elif args_orig[0] == '--deselected':
        show_deselected = True
        args_orig = args_orig[1:]

    args = []
    for arg in args_orig:
        if arg in ['ghc-mod', 'default-jre']:
            args += [arg]
            continue
        args += arg.split('-')

    if 'java7' in args or 'java8' in args:
        args.append('java')

    if 'pip' in args:
        args.append('noreqs')

    # TODO: pass through any args which are literal test filenames

    bears = get_bears(metadata, args, include_disabled)
    tests = get_tests(bears)
    if show_deselected:
        not_list = get_pytest_deselected_tests(args, tests)
        deselect_list = [item for item in not_list if '::' in item]
        not_list = [item for item in not_list if item not in deselect_list]
        if len(not_list) > 1:
            not_list = '-k "not ({})"'.format(' or '.join(not_list))
        elif len(not_list) == 1:
            not_list = '-k "not {}"'.format(not_list[0])
        else:
            not_list = ''
        if deselect_list:
            deselect_list = ' --deselect={}'.format(
                ' --deselect='.join(deselect_list))
        else:
            deselect_list = ''
        print(not_list + deselect_list)
    else:
        print(' '.join(sorted(tests)))


if __name__ == '__main__':
    main()
