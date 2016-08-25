import argparse
import glob
import os
import shutil
from string import Template
import subprocess
import sys
import time

from bears import VERSION
from coalib.bears.requirements.PipRequirement import PipRequirement
from coalib.collecting.Importers import iimport_objects
from coalib.parsing.Globbing import glob


def touch(file_name):
    """
    Creates an empty file. An existing file remains untouched.

    :param file_name: Name of the file.
    """
    open(file_name, 'a').close()


def create_file_from_template(template_file, output_file, substitution_dict):
    """
    Creates a file from a template file, using a substitution dict.

    :param template_file:     The template file.
    :param output_file:       The file to be written.
    :param substitution_dict: The dict from which the substitutions are taken.
    """
    with open(template_file) as fl:
        template = fl.read()
    template = Template(template).safe_substitute(**substitution_dict)

    with open(output_file, 'w') as output_handle:
        output_handle.write(template)


def create_file_structure_for_packages(root_folder, file_to_copy, object_name):
    """
    Creates a file structure for the packages to be uploaded. The structure
    will be ``root_folder/object_name/coalaobject_name/object_name.py``.
    Also holds a ``root_folder/object_name/coalaobject_name/__init__.py``
    to make the package importable.

    :param root_folder:  The folder in which the packages are going to be
                         generated.
    :param file_to_copy: The file that is going to be generated the package
                         for.
    :param object_name:  The name of the object that is inside the
                         file_to_copy.
    """
    upload_package_folder = os.path.join(
        root_folder, object_name, 'coala' + object_name)
    os.makedirs(upload_package_folder, exist_ok=True)
    touch(os.path.join(upload_package_folder, '__init__.py'))
    shutil.copyfile(file_to_copy, os.path.join(upload_package_folder,
                                               object_name + '.py'))


def perform_register(path, file_name):
    """
    Register the directory to PyPi, after creating a ``sdist`` and
    a ``bdist_wheel``.

    :param path: The file on which the register should be done.
    """
    subprocess.call(
        [sys.executable, 'setup.py', 'sdist', 'bdist_wheel'], cwd=path)
    subprocess.call(['twine', 'register', '-r', 'pypi', os.path.join(
        path, 'dist', file_name + '.tar.gz')])
    subprocess.call(['twine', 'register', '-r', 'pypi', os.path.join(
        path, 'dist', file_name + '-py3-none-any.whl')])


def perform_upload(path):
    """
    Uploads the directory to PyPi.

    :param path: The folder in which the upload should be done.
    """
    subprocess.call(
        ['twine', 'upload', path + '/dist/*'])


def create_upload_parser():
    """
    Creates a parser for command line arguments.

    :return: Parser arguments.
    """
    parser = argparse.ArgumentParser(
        description='Generates PyPi packages from bears.')
    parser.add_argument('-r', '--register',
                        help='Register the packages on PyPi',
                        action='store_true')
    parser.add_argument('-u', '--upload', help='Upload the packages on PyPi',
                        action='store_true')
    return parser


def main():
    args = create_upload_parser().parse_args()

    os.makedirs(os.path.join('bears', 'upload'), exist_ok=True)

    bear_version = VERSION
    if 'dev' in bear_version:
        bear_version = bear_version[:bear_version.find("dev")] + (
            str(int(time.time())))
    else:
        bear_version = repr(bear_version) + '.' + str(int(time.time()))

    for bear_file_name in sorted(set(glob('bears/**/*Bear.py'))):
        bear_object = next(iimport_objects(
            bear_file_name, attributes='kind', local=True),
            None)
        if bear_object:
            bear_name, _ = os.path.splitext(os.path.basename(bear_file_name))
            create_file_structure_for_packages(
                os.path.join('bears', 'upload'), bear_file_name, bear_name)
            if bear_object.REQUIREMENTS:
                for requirement in bear_object.REQUIREMENTS:
                    if isinstance(requirement, PipRequirement):
                        with open(os.path.join(
                                    'bears', 'upload',
                                    bear_name, 'requirements.txt'),
                                  'a') as reqtxt:
                            reqtxt.write(
                                requirement.package + '=='
                                + requirement.version + '\n')

                if os.path.exists(os.path.join('bears', 'upload',
                                               bear_name, 'requirements.txt')):
                    with open(os.path.join(
                                'bears', 'upload',
                                bear_name, 'MANIFEST.in'), 'w') as manifest:
                        manifest.write('include requirements.txt')

            substitution_dict = {'NAME': repr(bear_name),
                                 'VERSION': bear_version,
                                 'AUTHORS': str(bear_object.AUTHORS),
                                 'AUTHORS_EMAILS':
                                 str(bear_object.AUTHORS_EMAILS),
                                 'MAINTAINERS': str(bear_object.maintainers),
                                 'MAINTAINERS_EMAILS':
                                 str(bear_object.maintainers_emails),
                                 'PLATFORMS': str(bear_object.PLATFORMS),
                                 'LICENSE': str(bear_object.LICENSE),
                                 'LONG_DESCRIPTION': str(bear_object.__doc__),
                                 'BEAR_NAME': bear_name,
                                 'ENTRY': 'coala' + bear_name}

            create_file_from_template(os.path.join('bears', 'setup.py.in'),
                                      os.path.join('bears', 'upload',
                                                   bear_name, 'setup.py'),
                                      substitution_dict)

            bear_dist_name = bear_name + '-' + bear_version
            if args.register:
                perform_register(os.path.join('bears', 'upload', bear_name),
                                 bear_dist_name)
            if args.upload:
                perform_upload(os.path.join('bears', 'upload', bear_name))


if __name__ == '__main__':  # pragma: no cover
    sys.exit(main())
