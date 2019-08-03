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
import logging
import os
import sys

from ruamel.yaml import YAML, RoundTripDumper
from ruamel.yaml.comments import CommentedMap

from coalib.bears.BEAR_KIND import BEAR_KIND
from coalib.collecting.Collectors import collect_bears

from dependency_management.requirements.AnyOneOfRequirements import (
    AnyOneOfRequirements,
)
from dependency_management.requirements.DistributionRequirement import (
    DistributionRequirement,
)
from dependency_management.requirements.ExecutableRequirement import (
    ExecutableRequirement,
)

DISABLED_BEARS = []

yaml = YAML(typ='rt')
yaml.default_flow_style = False
yaml.Dumper = RoundTripDumper

BEAR_METADATA_YAML = 'bear-metadata.yaml'
BEAR_REQUIREMENTS_YAML = 'bear-requirements.yaml'
BEAR_LANGUAGES_YAML = 'bear-languages.yaml'

_VERSION_OPERATORS = ('<', '>', '~', '=', '-', '!')

THIS_DIR = os.path.dirname(os.path.abspath(__file__))

PROJECT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

PROJECT_BEAR_DIR = os.path.abspath(os.path.join(PROJECT_DIR, 'bears'))


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

    parser.add_argument('--debug', action='store_true',
                        help='sets logging level to debug.')
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


INHERITED_PIP_REQUIREMENTS = get_inherited_requirements()

REQUIREMENT_TYPES = collections.OrderedDict({
    'PipRequirement': {
        'prefix': 'pip',
        'version_operator': '~=',
        'exclude': INHERITED_PIP_REQUIREMENTS,
    },
    'NpmRequirement': {
        'prefix': 'npm',
        'version_operator': '~',
    },
    'GemRequirement': {
        'prefix': 'gem',
        'version_operator': '~>',
    },
    'ComposerRequirement': {
        'prefix': 'composer',
        'version_operator': '~',
    },
    'CabalRequirement': {
        'prefix': 'cabal',
        'version_operator': '==',
    },
    'RscriptRequirement': {
        'prefix': 'r_script',
        'version_operator': '>=',
        'allow_missing_version': True,
    },
    'DistributionRequirement': {
        'prefix': 'distro',
        'version_operator': '>=',
        'allow_missing_version': True,
    },
    'ExecutableRequirement': {
        'prefix': 'exe',
        'version_operator': '>=',
        'allow_missing_version': True,
    },
    'JuliaRequirement': {
        'prefix': 'julia',
        'version_operator': '>=',
        'allow_missing_version': True,
    },
    'GoRequirement': {
        'prefix': 'go',
        'version_operator': '>=',
        'allow_missing_version': True,
    },
    'LuarocksRequirement': {
        'prefix': 'luarocks',
        'version_operator': '>=',
        'allow_missing_version': True,
    },
    'CondaRequirement': {
        'prefix': 'conda',
        'version_operator': '>=',
    },
})


def helper(requirements, instance_dict):
    for requirement in requirements:
        if isinstance(requirement, AnyOneOfRequirements):
            helper(requirement.requirements, instance_dict)
        elif requirement.__class__.__name__ not in REQUIREMENT_TYPES:
            raise RuntimeError(
                '{} not configured'.format(repr(requirement)))
        else:
            instance_dict[type(requirement).__name__].add(requirement)


def _clean_executable(executable):
    return executable.rpartition('/')[2].lower().replace('.exe', '')


def get_all_requirements(bears):
    bear_requirements = {}

    for bear in bears:
        instance_dict = collections.defaultdict(set)
        executable = None
        if hasattr(bear, 'get_executable'):
            executable = bear.get_executable()
        if executable:
            requirement = ExecutableRequirement(_clean_executable(executable))
            instance_dict['ExecutableRequirement'].add(requirement)
        helper(bear.REQUIREMENTS, instance_dict)
        bear_requirements[str(bear.name)] = instance_dict

    return bear_requirements


def _to_entry(requirement, default_operator):
    entry = {}

    if isinstance(requirement, DistributionRequirement):
        entry['packages'] = dict(sorted(requirement.packages.items()))

    if not requirement.version:
        requirement_type = requirement.__class__.__name__
        settings = REQUIREMENT_TYPES[requirement_type]
        if settings.get('allow_missing_version', False) is True:
            return entry or None
        else:
            raise RuntimeError(
                '{}({}) has no version'.format(requirement_type,
                                               requirement.package))

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


def _create_sorted_commented_map(input_dict):
    if not input_dict:
        return CommentedMap()
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


def get_bear_requirement_metadata(bear_requirement_sets, storage=None,
                                  old_labels=False):
    if not storage:
        storage = {}

    for requirement_type, settings in REQUIREMENT_TYPES.items():
        requirements = _get_requirements(
            bear_requirement_sets[requirement_type],
            settings['version_operator'],
            settings.get('exclude', [])
        )
        if not requirements:
            continue

        label = settings['prefix']
        if old_labels:
            label += '_requirements'

        storage[label] = requirements

    return storage


def get_bear_tags(bear, metadata):
    tags = set()

    requirements = metadata['requirements'] or {}
    for requirement_type, requirement_items in requirements.items():
        if requirement_type == 'distro':
            for name, settings in requirement_items.items():
                tags.add(name)
                tags.update(settings['packages'])
        elif 'default-jre' in requirement_items:
            tags.add('java')

        tags.add(requirement_type)

    # Extra pip dependencies does not make the bear a pip bear
    # Allow for 'exe' dependency
    if 'pip' in tags and tags not in (set(['pip']), set(['pip', 'exe'])):
        tags.remove('pip')

    if not requirements:
        tags.add('noreqs')

    tags.add(metadata['subdir'].replace('_', '-').replace('/', '-'))

    if bear.name == 'VHDLLintBear':
        tags.add('perl')

    if 'exe' in requirements:
        tags.update(requirements['exe'].keys())

    if requirements.get('pip', {}).get('libclang-py3'):
        tags.add('clang')

    if 'swift' in tags:
        tags.add('java')

    # Special cases
    if bear.name == 'InferBear':
        # Processes java, but not written in Java
        if 'java' in tags:
            tags.remove('java')
        tags.add('opam')

    elif bear.name == 'CPDBear':
        # Has no requirements defined yet
        tags.remove('noreqs')
        tags.add('java')

    elif bear.name == 'LanguageToolBear':
        # Has no requirements defined yet
        tags.add('java')
        tags.add('languagetool')

    elif bear.name == 'JavaPMDBear':
        # Has no executable defined
        tags.add('pmd')

    elif bear.name == 'CPDBear':
        # Has no executable defined
        tags.add('cpd')

    elif bear.name == 'VHDLLintBear':
        # Has no executable defined
        tags.add('bakalint')

    if bear.name in DISABLED_BEARS:
        tags.add('disabled')

    return tags


def get_metadata(bears, bear_requirements, bear_languages):
    # Add 1 for the path separator after bears
    bear_dir_prefix_len = len(PROJECT_BEAR_DIR) + 1
    metadata = {}
    for bear in bears:
        name = str(bear.name)
        requirements = bear_requirements[name]
        requirement_metadata = get_bear_requirement_metadata(requirements)
        if requirement_metadata:
            requirement_metadata = _create_sorted_commented_map(
                requirement_metadata)
        else:
            requirement_metadata = None
        directory, filename = os.path.split(bear.source_location)
        bears_subdirs = directory[bear_dir_prefix_len:].split(os.path.sep)
        language_metadata = bear_languages[name]
        if language_metadata:
            assert sorted(language_metadata) == language_metadata
        metadata[name] = {
            'name': name,
            'subdir': '/'.join(bears_subdirs),
            'filename': filename,
            'requirements': requirement_metadata,
            'languages': bear_languages[name],
        }
        tags = get_bear_tags(bear, metadata[name])
        metadata[name]['tags'] = sorted(tags)

    return metadata


def deep_update(target, src):
    for key, value in src.items():
        if target.get(key) is None:
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


def merge_requirements(bear_requirements, exclude=['ExecutableRequirement']):
    merged_requirements = collections.defaultdict(set)

    for bear, bear_requirement_sets in bear_requirements.items():
        for requirement_type, requirements in bear_requirement_sets.items():
            if requirement_type not in exclude:
                for requirement in requirements:
                    merged_requirements[requirement_type].add(requirement)

    return merged_requirements


def sort_requirements(req_dict):
    for _type, settings in REQUIREMENT_TYPES.items():
        key = settings['prefix'] + '_requirements'
        req_dict[key] = _create_sorted_commented_map(req_dict.get(key))


YAML_MISSING = (
    'bear-requirements.yaml not found or is empty. '
    'Please fetch it from the repository.'
)


if __name__ == '__main__':
    args = get_args()

    logging.basicConfig(
        level=logging.DEBUG if args.debug else logging.WARNING,
    )

    bear_dirs = [PROJECT_BEAR_DIR]

    if args.bear_dirs is not None:
        bear_dirs.extend(args.bear_dirs)

    all_bears = get_all_bears(bear_dirs)

    bear_requirements = get_all_requirements(all_bears)
    instance_dict = merge_requirements(bear_requirements)

    requirements = CommentedMap()
    requirements.yaml_set_start_comment(
        'This is an automatically generated file.\n'
        'And should not be edited by hand.')

    requirements['overrides'] = 'pm-requirements.yaml'
    get_bear_requirement_metadata(bear_requirement_sets=instance_dict,
                                  storage=requirements, old_labels=True)

    if args.update or args.check:
        input_file_path = os.path.join(PROJECT_DIR, BEAR_REQUIREMENTS_YAML)

        try:
            input_file = open(input_file_path, 'r')
        except FileNotFoundError:
            print(YAML_MISSING)
            exit(1)

        input_requirments = yaml.load(input_file)

        if not input_requirments:
            print(YAML_MISSING)
            exit(1)

        new_requirments = copy.deepcopy(input_requirments)
        deep_update(new_requirments, requirements)

        if args.update:
            requirements = new_requirments

        if args.check:
            changed = deep_diff(input_requirments, new_requirments)
            if changed:
                yaml.dump(changed, sys.stdout)
                exit(1)

    sort_requirements(requirements)

    if args.output == '-':
        output = sys.stdout
    else:
        output = open(args.output, 'w')

    yaml.dump(requirements, output)
    output.close()

    language_requirements = get_languages(all_bears)
    bear_languages = language_requirements
    language_requirements = _create_sorted_commented_map(language_requirements)
    file_path = os.path.join(PROJECT_DIR, BEAR_LANGUAGES_YAML)
    with open(file_path, 'w') as outfile:
        yaml.indent(mapping=2, sequence=4, offset=2)
        yaml.dump(language_requirements, outfile)

    metadata = get_metadata(all_bears, bear_requirements, bear_languages)
    metadata = _create_sorted_commented_map(metadata)
    metadata = {'bear_metadata': metadata}
    file_path = os.path.join(PROJECT_DIR, BEAR_METADATA_YAML)
    with open(file_path, 'w') as outfile:
        yaml.indent(mapping=2, sequence=4, offset=2)
        yaml.dump(metadata, outfile)
