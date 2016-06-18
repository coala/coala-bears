import re

from coalib.bearlib.abstractions.Lint import Lint
from coalib.bears.requirements.NpmRequirement import NpmRequirement
from coalib.bears.LocalBear import LocalBear


class AlexBear(LocalBear, Lint):
    executable = 'alex'
    output_regex = re.compile(
        r'\s+(?P<line>\d+):(?P<column>\d+)\-'
        r'(?P<end_line>\d+):(?P<end_column>\d+)'
        r'\s+(?:(?P<warning>warning))\s+(?P<message>.+)')
    arguments = "{filename}"
    LANGUAGES = {"Natural Language"}
    REQUIREMENTS = {NpmRequirement('alex', '2')}
    AUTHORS = {'The coala developers'}
    AUTHORS_EMAILS = {'coala-devel@googlegroups.com'}
    LICENSE = 'AGPL-3.0'

    def run(self, filename, file):
        '''
        Checks the markdown file with Alex - Catch insensitive,
        inconsiderate writing.
        '''
        return self.lint(filename)
