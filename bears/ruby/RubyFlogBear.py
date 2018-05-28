import re

from coalib.bearlib.abstractions.Linter import linter
from dependency_management.requirements.GemRequirement import GemRequirement
from coalib.results.Result import Result
from coalib.results.SourceRange import SourceRange


@linter(executable='flog', use_stdin=True, use_stdout=True)
class RubyFlogBear:
    """
    Uses ``flog`` to perform complexity analysis on Ruby code, by assigning
    a score using an ABC (Assignments, Branches, Calls) metric, with
    particular attention placed on calls. Flog reports the most
    tortured or complex code in a pain report, with a higher
    score indicating higher complexity.
    """
    LANGUAGES = {'Ruby'}
    REQUIREMENTS = {GemRequirement('flog', '4.6.2')}
    AUTHORS = {'The coala developers'}
    AUTHORS_EMAILS = {'coala-devel@googlegroups.com'}
    LICENSE = 'AGPL-3.0'
    CAN_DETECT = {'Complexity'}
    SEE_MORE = 'https://github.com/seattlerb/flog'

    @staticmethod
    def create_arguments(filename, file, config_file):
        args = ('--all', '--continue', '--group', '--methods-only', filename)
        return args

    def process_output(self, output, filename, file):
        regex = re.compile(r'[\t\s]+(?P<flog_score>\d*\.?\d*)'
                           r':\s(?P<class>.*)'
                           r'#(?P<method>\S*)'
                           r'[\t\s]+(?P<filename>.*)'
                           r':(?P<start_line>\d+)'
                           r'-(?P<end_line>\d+)')

        output_lines = output.splitlines()
        results = [regex.match(line)
                   for line in output_lines if regex.match(line) is not None]
        for result in results:
            result_dict = result.groupdict()
            start_line = int(result_dict['start_line'])
            end_line = int(result_dict['end_line']) + 1
            flog_score = result_dict['flog_score']
            klass = result_dict['class']
            method = result_dict['method']

            yield Result.from_values(origin='{}'.format(self.__class__.__name__),
                                     message='{class}:{method} has a score of {score}',
                                     message_arguments={
                                         'class': klass, 'method': method, 'score': flog_score},
                                     file=filename,
                                     line=start_line,
                                     end_line=end_line)
