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
import collections
import copy
import itertools
import os
import sys

from ruamel.yaml import YAML, RoundTripDumper
from ruamel.yaml.comments import CommentedMap

from coalib.bears.BEAR_KIND import BEAR_KIND
from coalib.collecting.Collectors import collect_bears

from dependency_management.requirements.AnyOneOfRequirements import (
    AnyOneOfRequirements)

yaml = YAML(typ='rt')
yaml.default_flow_style = False
yaml.Dumper = RoundTripDumper

BEAR_REQUIREMENTS_YAML = 'bear-requirements.yaml'
BEAR_LANGUAGES_YAML = 'bear-languages.yaml'

_VERSION_OPERATORS = ('<', '>', '~', '=', '-', '!')

THIS_DIR = os.path.dirname(os.path.abspath(__file__))

PROJECT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

PROJECT_BEAR_DIR = os.path.abspath(os.path.join(PROJECT_DIR, 'bears'))

SUPPORTED_INSTANCES = (
    'PipRequirement',
    'NpmRequirement',
    'GemRequirement',
    'ComposerRequirement',
    'CabalRequirement',
    'RscriptRequirement',
    'PerlRequirement',
)

INSTANCE_NAMES = (
    'pip_requirements',
    'npm_requirements',
    'gem_requirements',
    'composer_requirements',
    'cabal_requirements',
    'r_script_requirements',
    'perl_requirements'
)


def get_args():
    parser = argparse.ArgumentParser(
        description='This program generates a yaml requirement file for '
                    'installation of linters that are used by the bears.')
    parser.add_argument('--output', '-o',
                        help='name of file to generate, or - for stdout',
                        default=os.path.join(PROJECT_DIR,
                                             BEAR_REQUIREMENTS_YAML))
    parser.add_argument('--bear-dirs', '-d', nargs='+', metavar='DIR',
                        help='additional directories which may contain bears')

    parser.add_argument('--check', '-c', action='store_true',
                        help='performs a dry run, and reports differences.')
    parser.add_argument('--update', '-u', action='store_true',
                        help='updates "bear-requirements.yaml" '
                             'instead of overwriting')
    args = parser.parse_args()

    return args


def get_all_bears(bear_dirs):
    local_bears, global_bears = collect_bears(
        bear_dirs,
        ['**'],
        [BEAR_KIND.LOCAL, BEAR_KIND.GLOBAL],
        warn_if_unused_glob=False)
    return list(itertools.chain(local_bears, global_bears))


def get_inherited_requirements():
    inherited_requirements = set()

    in_inherited = False
    with open(os.path.join(PROJECT_DIR, 'requirements.txt'), 'r') as file:
        for line in file.read().splitlines():
            if 'inherited' in line:
                in_inherited = True
                continue
            if in_inherited:
                if line.startswith('# '):
                    requirement = line[2:]
                    inherited_requirements.add(requirement.replace('-', '_'))
                    inherited_requirements.add(requirement.replace('_', '-'))
                else:
                    in_inherited = False

    return inherited_requirements


def helper(requirements, instance_dict):
    for requirement in requirements:
        if isinstance(requirement, AnyOneOfRequirements):
            helper(requirement.requirements, instance_dict)
        elif any(type(requirement).__name__ == instance
                 for instance in SUPPORTED_INSTANCES):
            instance_dict[type(requirement).__name__].add(requirement)


def get_all_requirements(bears):
    instance_dict = collections.defaultdict(set)

    for bear in bears:
        helper(bear.REQUIREMENTS, instance_dict)

    return instance_dict


def _to_entry(requirement, default_operator):
    assert requirement.version, '%s has no version' % requirement.package
    entry = {}

    if requirement.version[0].isdigit():
        entry['version'] = default_operator + requirement.version
    else:
        assert requirement.version[0] in _VERSION_OPERATORS, \
               'Unknown version operator in %s' % requirement.version
        entry['version'] = requirement.version
    return entry


def _get_requirements(requirements, default_operator, exclude=[]):
    return dict(
        (requirement.package, _to_entry(requirement, default_operator))
        for requirement in requirements
        if requirement.package not in exclude
    )


def get_gem_requirements(requirements):
    return _get_requirements(requirements, '~>')

def get_r_requirements(requirements):
    return _get_requirements(requirements, '>=')

def get_npm_requirements(requirements):
    return _get_requirements(requirements, '~')


def get_composer_requirements(requirements):
    return _get_requirements(requirements, '~')


def get_pip_requirements(requirements):
    inherited_requirements = get_inherited_requirements()
    return _get_requirements(requirements, '~=', inherited_requirements)


def get_cabal_requirements(requirements):
    return _get_requirements(requirements, '==')

def get_perl_requirements(requirements):
    return _get_requirements(requirements, '==')

def _create_sorted_commented_map(input_dict):
    return CommentedMap(sorted(input_dict.items(),
                               key=lambda t: t[0]))


def get_languages(bears):
    language_dict = {}
    for bear in bears:
        language_dict[str(bear.name)] = list(sorted(bear.LANGUAGES))
    for key, value in language_dict.items():
        if 'All' in value:
            value.remove('All')
        if 'default' in value:
            value.remove('default')
        if not value:
            language_dict[key] = None

    return language_dict


def deep_update(target, src):
    for key, value in src.items():
        if key not in target:
            target[key] = copy.deepcopy(value)
        else:
            if isinstance(value, list):
                target[key].extend(value)
            elif isinstance(value, dict):
                deep_update(target[key], value)
            elif isinstance(value, set):
                target[key].update(value.copy())
            else:
                target[key] = copy.copy(value)


def deep_diff(target, src):
    errors = []
    for key, value in src.items():
        if key not in target:
            errors.append((key, 'Missing'))
        elif target[key] != value:
            if isinstance(value, list):
                if [x for x in value if x not in target[key]]:
                    errors.append(key)
            elif isinstance(value, dict):
                if target[key] != value:
                    errors.append((key, deep_diff(target[key], value)))
            elif isinstance(value, set):
                if set(target[key]).symmetric_difference(value):
                    errors.append(key)
            else:
                errors.append((key, target[key]))
    return errors



def sort_requirements(req_dict):
    for key in INSTANCE_NAMES:
        req_dict[key] = _create_sorted_commented_map(req_dict[key])


if __name__ == '__main__':
    args = get_args()

    bear_dirs = [PROJECT_BEAR_DIR]

    if args.bear_dirs is not None:
        bear_dirs.extend(args.bear_dirs)

    all_bears = get_all_bears(bear_dirs)

    instance_dict = get_all_requirements(all_bears)

    requirements = CommentedMap()
    requirements.yaml_set_start_comment(
        'This is an automatically generated file.\n'
        'And should not be edited by hand.')

    requirements['overrides'] = 'coala-build.yaml'
    requirements['gem_requirements'] = get_gem_requirements(
                                            instance_dict['GemRequirement'])
    requirements['r_script_requirements'] = get_r_requirements(
                                            instance_dict['RscriptRequirement'])
    requirements['npm_requirements'] = get_npm_requirements(
                                            instance_dict['NpmRequirement'])
    requirements['pip_requirements'] = get_pip_requirements(
                                            instance_dict['PipRequirement'])
    requirements['composer_requirements'] = get_composer_requirements(
                                            instance_dict['ComposerRequirement'])
    requirements['cabal_requirements'] = get_cabal_requirements(
                                            instance_dict['CabalRequirement'])
    requirements['perl_requirements'] = get_perl_requirements(
                                            instance_dict['PerlRequirement'])

    if args.update or args.check:
        input_file_path = os.path.join(PROJECT_DIR, BEAR_REQUIREMENTS_YAML)

        try:
            input_file = open(input_file_path, 'r')
        except FileNotFoundError:
            print('bear-requirements.yaml not found. '
                  'Run without flags to generate it.')
            exit(1)

        input_requirments = yaml.load(input_file)

        new_requirments = copy.deepcopy(input_requirments)
        deep_update(new_requirments, requirements)

        if args.update:
            requirements = new_requirments

        if args.check:
            changed = deep_diff(input_requirments, new_requirments)
            if changed:
                yaml.dump(changed, sys.stdout)
                exit(1)

    if args.output == '-':
        output = sys.stdout
    else:
        output = open(args.output, 'w')

    language_requirements = get_languages(all_bears)
    language_requirements = _create_sorted_commented_map(language_requirements)
    file_path = os.path.join(PROJECT_DIR, BEAR_LANGUAGES_YAML)
    with open(file_path, 'w') as outfile:
        yaml.indent(mapping=2, sequence=4, offset=2)
        yaml.dump(language_requirements, outfile)

    sort_requirements(requirements)
    yaml.dump(requirements, output)
    output.close()
