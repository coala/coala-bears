import re

from coalib.bearlib.abstractions.Linter import linter
from coalib.bears.GlobalBear import GlobalBear
from coalib.results.Result import Result
from coalib.results.RESULT_SEVERITY import RESULT_SEVERITY
from dependency_management.requirements.DistributionRequirement import (
    DistributionRequirement)


@linter(executable='cloc')
class CLOCBear(GlobalBear):
    """
    Summarises a file or number of files in directory structure
    with total lines, number of comment lines, number of actual code lines
    using CLI tool cloc
    """
    LANGUAGES = {'All'}
    REQUIREMENTS = {DistributionRequirement('cloc')}
    AUTHORS = {'The coala developers'}
    AUTHORS_EMAILS = {'coala-devel@googlegroups.com'}
    LICENSE = 'AGPL-3.0'
    CAN_DETECT = {'Statistics'}
    SEE_MORE = 'https://github.com/AlDanial/cloc'

    @staticmethod
    def create_arguments(filename, file, config_file):
        return ('--csv', filename)

    def process_output(self, output, filename, file):
        lines = output.split('\n')
        regex = r'(\d+).*?\n\s+(\d+)'
        files, ignored_files = re.search(
            regex, '\n'.join(lines[1:3]), re.MULTILINE).group(1, 2)
        if files == ignored_files:
            msg = 'File does not belong to valid programming language.'
            yield Result.from_values(origin=self,
                                     message=msg,
                                     file=filename,
                                     severity=RESULT_SEVERITY.MAJOR)
        else:
            regex = re.compile(r'(\d+),(\S+),(\d+),(\d+),(\d+)')
            # cloc tool gives summary of files
            # starting from 5th(0-index) line up to second last line
            for row in lines[5:-1]:
                match = regex.match(row)

                nfiles, lang = match.group(1, 2)
                blank, comment, code = map(int, match.group(3, 4, 5))
                total = blank + comment + code

                report = '\n'.join(['Language: {0}'.format(lang),
                                    'Total files: {0}'.format(nfiles),
                                    'Total lines: {0}'.format(total),
                                    'Code lines: {0} ({1:.2f}%)'.format(
                                        code, code * 100.0 / total),
                                    'Comment lines: {0} ({1:.2f}%)'.format(
                                        comment, comment * 100.0 / total),
                                    'Blank lines: {0} ({1:.2f}%)'.format(
                                        blank, blank * 100.0 / total)
                                    ])
                yield Result.from_values(origin=self,
                                         message=report,
                                         file=filename,
                                         severity=RESULT_SEVERITY.INFO)
