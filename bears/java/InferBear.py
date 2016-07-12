import re

from coalib.bearlib.abstractions.Lint import Lint
from coalib.bears.LocalBear import LocalBear
from coalib.results.RESULT_SEVERITY import RESULT_SEVERITY


class InferBear(LocalBear, Lint):
    executable = 'infer'
    arguments = '-npb -- javac {filename}'
    output_regex = re.compile(
        r'(.+):'
        r'(?P<line>.+): '
        r'(?P<severity>error|warning): '
        r'(?P<message>.*)')
    severity_map = {
        "error": RESULT_SEVERITY.MAJOR,
        "warning": RESULT_SEVERITY.NORMAL}
    LANGUAGES = {"Java"}
    AUTHORS = {'The coala developers'}
    AUTHORS_EMAILS = {'coala-devel@googlegroups.com'}
    LICENSE = 'AGPL-3.0'
    CAN_DETECT = {'Security'}

    def run(self, filename, file):
        '''
        Checks the code with ``infer``.
        '''
        return self.lint(filename)
