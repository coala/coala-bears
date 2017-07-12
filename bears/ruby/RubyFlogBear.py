import re

from coalib.bearlib.abstractions.Linter import linter
from dependency_management.requirements.GemRequirement import GemRequirement
from coalib.results.Result import Result
from coalib.results.SourceRange import SourceRange


@linter(executable='flog', use_stdin=True)
class RubyFlogBear:
    """
    Check Ruby files for tortured code and reports in an easy to read
    pain report.
    """
    LANGUAGES = {'Ruby'}
    REQUIREMENTS = {GemRequirement('flog', '4.6.1')}
    AUTHORS = {'The coala developers'}
    AUTHORS_EMAILS = {'coala-devel@googlegroups.com'}
    LICENSE = 'AGPL-3.0'
    SEE_MORE = 'https://github.com/seattlerb/flog'

    def create_arguments(self, filename, file, config_file, threshold: int=1):

        args = ('', filename)  # ('-t', str(threshold), filename)
        self.log(20, args)
        return args

    def process_output(self, output, filename, file):
        # TODO : HOW TO PROCEED WITH ERRORS
        regex = r
        '[t]+(?P < flog_score >\d +\.\d+):'
        ' (?P < class_with_method > .*)[t]+'
        '(?P < file_with_path >\S+): '
        '(?P < start_line >\d+)-(?P < end_line >\d+)'
        regex_object = re.compile(regex)
        output_lines = output.splitlines()
        results = [regex_object.match(
            line) for line in output_lines if regex_object.match(
            line) is not None]
        for result in results:
            result_dict = result.groupdict()

            start_line = int(result_dict['start_line'])
            end_line = int(result_dict['end_line']) + 1
            flog_score = result_dict['flog_score']

            sourceranges = [SourceRange.from_values(
                    file=filename, start_line=line) for line in range(
                    start_line, end_line)]
            # TODO: GIVE MORE INFORMATIVE MESSAGES
            yield Result(
                origin='{} ({})'.format(self.__class__.__name__,
                                        result_dict['file_with_path']),
                message='Flog Score: {}'.format(flog_score),
                affected_code=sourceranges,
                additional_info=result_dict['class_with_method'])
