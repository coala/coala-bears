import argparse
import importlib
import re
import subprocess
import sys

from coala_utils.Question import ask_question
from coalib.collecting.Collectors import get_all_bears_names
from coalib.collecting.Importers import iimport_objects
from coalib.misc.Shell import call_without_output
from prompt_toolkit import prompt
from prompt_toolkit.contrib.completers import WordCompleter
from pygments.lexers import SqlLexer


def install_pip_package(package_name):
    """
    Uses call to install a PyPi package.

    :param package_name: The package to be installed.
    """
    subprocess.call(['sudo', 'pip3', 'install', package_name, '--upgrade'])


def get_output(command):
    """
    Runs the command and decodes the output and returns it.

    :param command: The command to be run.
    :return:        The output of the command, decoded.
    """
    function = subprocess.Popen(command, stdout=subprocess.PIPE)
    output, err = function.communicate()
    return output.decode("utf-8")


def create_installation_parser():
    """
    Creates a parser for command line arguments.

    :return: Parser arguments.
    """
    parser = argparse.ArgumentParser(
        description='Install bears requirements.')
    parser.add_argument('-i', '--install',
                        help='Install the requirements',
                        action='store_true')
    return parser


def main():
    args = create_installation_parser().parse_args()

    sql_completer = WordCompleter(['All', 'Some', 'None'], ignore_case=True)
    answer = prompt('What bears would you like to install?\n'
                    'All / Some / None\n', lexer=SqlLexer)

    if answer in ("All", "all"):
        print('Great idea, we are installing all the bears right now.')
        output = get_output(['pip', 'search', "coala.rtfd.org"])
        bear_name_list = re.findall(r'(.+) \(\d.*\n', output)

        for bear_name in sorted(bear_name_list):
            bears_failed_list = []
            try:
                install_pip_package(bear_name)
            except:
                bears_failed_list.append(bear_name)

            if args.install:
                bear_object = importlib.import_module(
                    bear_name + "." + bear_name)
                for requirement in getattr(bear_object, bear_name).REQUIREMENTS:
                    try:
                        subprocess.call([requirement.install_command()])
                    except:
                        bears_failed_list.append(bear_name)

            # check if any bear failed installing
            if bears_failed_list:
                print('Bears that failed installing:')
                for bear_failed in bears_failed_list:
                    print(bear_failed)

    elif answer in ("Some", "some"):
        print('This is a list of all the bears you can install:')

        output = get_output(['pip', 'search', "coala.rtfd.org"])
        bear_name_list = re.findall(r'(.+) \(\d.*\n', output)

        sql_completer = WordCompleter(bear_name_list, ignore_case=True)

        for bear_name in sorted(bear_name_list):
            print(bear_name)

        answer = prompt('Which ones? (You can add more, separated by commas)\n',
                        lexer=SqlLexer, completer=sql_completer).split(',')

        for bear_name in answer:
            bear_name = bear_name.replace(' ', '')
            bears_failed_list = []
            try:
                install_pip_package(bear_name)
            except:
                bears_failed_list.append(bear_name)

            if args.install:
                bear_object = importlib.import_module(
                    bear_name + "." + bear_name)
                for requirement in getattr(bear_object, bear_name).REQUIREMENTS:
                    try:
                        subprocess.call([requirement.install_command()])
                    except:
                        bears_failed_list.append(bear_name)

            # check if any bear failed installing
            if bears_failed_list:
                print('Bears that failed installing:')
                for bear_failed in bears_failed_list:
                    print(bear_failed)

    else:
        print('See ya!')
        return 0


if __name__ == '__main__':  # pragma: no cover
    sys.exit(main())
