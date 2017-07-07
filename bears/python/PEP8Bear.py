import autopep8
import pycodestyle

from coalib.bearlib import deprecate_settings
from coalib.bearlib.spacing.SpacingHelper import SpacingHelper
from coalib.bears.LocalBear import LocalBear
from dependency_management.requirements.PipRequirement import PipRequirement
from coalib.results.Diff import Diff
from coalib.results.Result import Result
from coalib.settings.Setting import typed_list


class PEP8Bear(LocalBear):
    LANGUAGES = {'Python', 'Python 2', 'Python 3'}
    REQUIREMENTS = {PipRequirement('autopep8', '1.2')}
    AUTHORS = {'The coala developers'}
    AUTHORS_EMAILS = {'coala-devel@googlegroups.com'}
    LICENSE = 'AGPL-3.0'
    CAN_FIX = {'Formatting'}

    @deprecate_settings(indent_size='tab_width')
    def run(self, filename, file,
            max_line_length: int=79,
            indent_size: int=SpacingHelper.DEFAULT_TAB_WIDTH,
            pep_ignore: typed_list(str)=(),
            pep_select: typed_list(str)=(),
            local_pep8_config: bool=False):
        """
        Detects and fixes PEP8 incompliant code. This bear will not change
        functionality of the code in any way.

        :param max_line_length:   Maximum number of characters for a line.
        :param indent_size:       Number of spaces per indentation level.
        :param pep_ignore:        A list of errors/warnings to ignore.
        :param pep_select:        A list of errors/warnings to exclusively
                                  apply.
        :param local_pep8_config: Set to true if autopep8 should use a config
                                  file as if run normally from this directory.
        """
        options = {'ignore': pep_ignore,
                   'select': pep_select,
                   'max_line_length': max_line_length,
                   'indent_size': indent_size}

        errors = self.list_pep8_errors(source=file, options=options)

        corrected = autopep8.fix_code(''.join(file),
                                      apply_config=local_pep8_config,
                                      options=options).splitlines(True)

        diffs = enumerate(
            Diff.from_string_arrays(file, corrected).split_diff())

        for i, diff in diffs:
            yield Result(self,
                         'The code does not comply to PEP8.\n{}'
                         .format(errors[i]['info'] if i < len(errors) else ''),
                         affected_code=(diff.range(filename),),
                         diffs={filename: diff})

    def list_pep8_errors(self, source, options):
        """
        Generates and returns a list of PEP8 errors on source.

        :param source:  The source file to perform check upon.
        :param options: A dictionary of PEP8 options.
        :return:        A list of PEP8 errors.
        """
        checker = pycodestyle.Checker(
            '', lines=source, reporter=ListReport, **options)
        checker.check_all()
        return checker.report.get_error_list()


class ListReport(pycodestyle.BaseReport):
    """
    Custom pycodestyle report class.
    Original idea from autopep8's _execute_pep8 method.
    """

    def __init__(self, options):
        super(ListReport, self).__init__(options)
        self.__pep8_errors = []

    def error(self, line_number, offset, text, check):
        """
        Collects PEP8 errors in a list.
        Overrides pycodestyle.BaseReport.error method.

        :param line_number: Number of the current line.
        :param offset:      Offset of line from the original due to multiline
                            strings.
        :param text:        PEP8 error text.
        """
        code = super(ListReport, self).error(
            line_number, offset, text, check)
        if code:
            self.__pep8_errors.append(
                {'id': code,
                 'line': line_number,
                 'column': offset + 1,
                 'info': text})

    def get_error_list(self):
        """
        Getter.

        :return: A list of PEP8 errors
        """
        return self.__pep8_errors
