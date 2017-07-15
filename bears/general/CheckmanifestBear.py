import os

from coalib.bearlib.abstractions.Linter import linter
from dependency_management.requirements.PipRequirement import PipRequirement
from coalib.results.RESULT_SEVERITY import RESULT_SEVERITY
from coalib.bears.GlobalBear import GlobalBear
from coalib.results.Result import Result
from coalib.misc.Shell import run_shell_command
from coalib.results.Diff import Diff


class CheckmanifestBear(GlobalBear):
    """
    Check MANIFEST.in in a Python source package for completeness

    Check https://pypi.python.org/pypi/rstcheck for more information.
    """

    LANGUAGES = {'Python MANIFEST.in'}
    REQUIREMENTS = {PipRequirement('check-manifest', '0.34')}
    AUTHORS = {'The coala developers'}
    AUTHORS_EMAILS = {'coala-devel@googlegroups.com'}
    LICENSE = 'AGPL-3.0'
    CAN_DETECT = {'Redundancy'}
    EXECUTABLE = 'check-manifest'

    def run(self, ignore: list=[]):
        """
        Check MANIFEST.in in a Python source package for completeness

        Check https://pypi.python.org/pypi/rstcheck for more information.

        :param ignore:
            ignore files/directories matching these comma-
            separated patterns
        """
        args = ''
        if ignore:
            args = ('--ignore=' +
                    ','.join(ignore),)

        output_message = 'suggested MANIFEST.in rules:'
        output, _ = run_shell_command(
            (self.EXECUTABLE,) + tuple(args) +
            tuple(os.path.dirname(filename)
                  for filename in self.file_dict.keys()))
        to_search = output_message+'\n'

        temp_output = output.splitlines(1)
        if to_search in temp_output:
            index = temp_output.index(to_search)
            new_output = temp_output[index+1:]
            final_output = [x.strip(' ') for x in new_output]
        else:
            final_output = ''
            # Ignore LineLengthBear
            output_message = 'lists of files in version control and sdist match!'

        a = Diff(list(self.file_dict.values())[0])
        a.add_lines(len(list(self.file_dict.values())[0]), final_output)

        yield Result(self, output_message,
                     diffs={list(self.file_dict.keys())[0]: a})
