import argparse
import glob
import os
import shutil
from string import Template
import subprocess
import sys
import time
import re

from bears import VERSION
from coalib.collecting.Importers import iimport_objects
from coalib.parsing.Globbing import glob

from coala_utils.Question import ask_question
from coala_utils.ContextManagers import open_files


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


def create_file_structure_for_packages(root_folder, file_to_copy,
                                       object_name, package_type):
    """
    Creates a file structure for the packages to be uploaded. The structure
    will be ``root_folder/object_name/object_name/file_to_copy`` for PyPI
    packages and ``root_folder/object_name/file_to_copy`` for conda packages.

    :param root_folder:   The folder in which the packages are going to be
                          generated.
    :param file_to_copy:  The file that is going to be generated the package
                          for.
    :param object_name:   The name of the object that is inside the
                          file_to_copy.
    :param package_type:  The type of package: conda or PyPI.
    """
    upload_package_folder = (os.path.join(root_folder,
                                          object_name,
                                          object_name)
                             if package_type.lower() == "pypi"
                             else os.path.join(root_folder, object_name))
    os.makedirs(upload_package_folder, exist_ok=True)
    shutil.copyfile(file_to_copy, os.path.join(upload_package_folder,
                                               '__init__.py'))


def perform_register(path, file_name):
    """
    Register the directory to PyPI, after creating a ``sdist`` and
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
    Uploads the directory to PyPI.

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
        description='Generates PyPI packages from bears.')
    parser.add_argument('-r', '--register',
                        help='Register the packages on PyPI',
                        action='store_true')
    parser.add_argument('-u', '--upload', help='Upload the packages on PyPI',
                        action='store_true')
    parser.add_argument('-c', '--conda', help='Create a conda package',
                        metavar='dir')
    return parser


def get_bear_glob(path):
    """
    Returns a list of filenames depending on the type of package that is to be
    created.

    :param path: Path from which to fetch the Bear if a conda package is to be
                 created.
    :return:     Returns a list with one filename for a conda package or a
                 list with multiple filenames for the PyPI packages.
    """
    return (list(glob(os.path.join(path, '*Bear.py')))
            if path else sorted(set(glob('bears/**/*Bear.py'))))


def fetch_url(path):
    """
    Checks the ``.git`` directory in ``path`` and fetches the URL of the repo.

    :param path: Path in which to look for a ``.git`` directory.
    :return:     Returns the url fetched or ``False`` if the URL could not be
                 fetched.
    """
    config = os.path.join(path, '.git', 'config')
    try:
        with open(config, 'r') as f:
            match = re.search(r'\s*url = (?P<url>.+)', f.read())
            return match.group('url') if match.group('url') else None
    except FileNotFoundError:
        return None


def main():
    args = create_upload_parser().parse_args()

    os.makedirs(os.path.join('bears', 'upload'), exist_ok=True)

    bear_version = VERSION
    if 'dev' in bear_version:  # pragma: no cover
        bear_version = bear_version[:bear_version.find("dev")] + (
            str(int(time.time())))
    else:  # pragma: no cover
        bear_version = repr(bear_version) + '.' + str(int(time.time()))

    for bear_file_name in get_bear_glob(args.conda):
        bear_object = next(iimport_objects(
            bear_file_name, attributes='kind', local=True),
            None)
        if bear_object:
            bear_name, _ = os.path.splitext(os.path.basename(bear_file_name))
            (create_file_structure_for_packages(
                os.path.join('bears', 'upload'),
                bear_file_name,
                bear_name, 'pypi') if not args.conda else
                create_file_structure_for_packages(
                args.conda,
                bear_file_name,
                bear_name, 'conda'))
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
                                 'BEAR_NAME': bear_name}
            template_dir = os.path.join('bears', 'templates')
            create_file_from_template(os.path.join(template_dir,
                                                   'setup.py.in'),
                                      os.path.join('bears',
                                                   'upload',
                                                   bear_name,
                                                   'setup.py')
                                      if not args.conda else
                                      os.path.join(args.conda,
                                                   'setup.py'),
                                      substitution_dict)

            bear_dist_name = bear_name + '-' + bear_version
            if args.register:
                perform_register(os.path.join('bears', 'upload', bear_name),
                                 bear_dist_name)
            if args.upload:
                perform_upload(os.path.join('bears', 'upload', bear_name))

            if args.conda:
                substitution_dict['URL'] = (fetch_url(args.conda) or
                                            ask_question("""
                                                Repository URL was not found.
                                                Please submit it manually.
                                                """))
                # conda accepts only lowercase package names
                substitution_dict['NAME'] = substitution_dict['NAME'].lower()
                create_file_from_template(os.path.join(template_dir,
                                                       'meta.yaml.in'),
                                          os.path.join(
                                              args.conda, 'meta.yaml'),
                                          substitution_dict)
                with open_files(
                    (os.path.join(template_dir, 'build.sh'), 'r'),
                    (os.path.join(args.conda, 'build.sh'), 'w')) as (f_in,
                                                                     f_out):
                    f_out.write(f_in.read())
                    f_out.close()
                with open_files(
                    (os.path.join(template_dir, 'bld.bat'), 'r'),
                    (os.path.join(args.conda, 'bld.bat'), 'w')) as (f_in,
                                                                    f_out):
                    f_out.write(f_in.read())
                    f_out.close()


if __name__ == '__main__':  # pragma: no cover
    sys.exit(main())
