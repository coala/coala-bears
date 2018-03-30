import json
import re

from bears.python.ChecksSelector.ChecksSelector import set_checks

from coalib.bearlib import deprecate_settings
from coalib.bearlib.abstractions.Linter import linter
from dependency_management.requirements.PipRequirement import PipRequirement
from coalib.results.Result import Result
from coalib.results.RESULT_SEVERITY import RESULT_SEVERITY
from coalib.settings.Setting import typed_list


@linter(executable='bandit',
        use_stdout=True,
        use_stderr=True)
class BanditBear:
    """
    Performs security analysis on Python source code, utilizing the ``ast``
    module from the Python standard library.
    """
    LANGUAGES = {'Python', 'Python 2', 'Python 3'}
    REQUIREMENTS = {PipRequirement('bandit', '1.2')}
    AUTHORS = {'The coala developers'}
    AUTHORS_EMAILS = {'coala-devel@googlegroups.com'}
    LICENSE = 'AGPL-3.0'
    CAN_DETECT = {'Security'}

    @staticmethod
    @deprecate_settings(bandit_skip_tests='bandit_skipped_tests')
    def create_arguments(filename, file, config_file,
                         bandit_skip_tests: typed_list(str) = (
                             'B105', 'B106', 'B107', 'B404', 'B603', 'B606',
                             'B607'),
                         bandit_select_tests: typed_list(str) = ()):
        """
        :param bandit_skip_tests:
            The IDs of the tests ``bandit`` shall not perform.
        :param bandit_select_tests:
            The IDs of the tests ``bandit`` shall perform.
            You can get information about the available builtin codes at
            https://github.com/openstack/bandit#usage.
        """
        args = (filename, '-f', 'json')

        select = set_checks(ignore='--skip',
                            ignore_check=bandit_skip_tests,
                            select='--tests',
                            select_check=bandit_select_tests)
        if select:
            args += select

        return args

    severity_map = {'HIGH': RESULT_SEVERITY.MAJOR,
                    'MEDIUM': RESULT_SEVERITY.NORMAL,
                    'LOW': RESULT_SEVERITY.INFO}

    confidence_map = {'HIGH': 90,
                      'MEDIUM': 70,
                      'LOW': 50}

    def process_output(self, output, filename, file):
        def err_issue(message):
            self.err('While running {0}, some issues were found:'
                     .format(self.__class__.__name__))
            self.err(message)

        stdout, stderr = output
        # Taking output from stderr in case bandit shows errors
        # such as selected test ID and skipped test ID are same.
        err_pattern = re.compile(r'ERROR\s(?P<error>.*)')
        match = err_pattern.search(stderr)
        if match:
            err_issue(match.group('error'))

        if not stdout:
            return

        output = json.loads(stdout)

        for error in output['errors']:
            yield Result.from_values(
                origin=self,
                file=filename,
                severity=RESULT_SEVERITY.MAJOR,
                message=error['reason'])

        for issue in output['results']:
            yield Result.from_values(
                origin=issue['test_id'],
                file=filename,
                message=issue['issue_text'],
                severity=self.severity_map[issue['issue_severity']],
                confidence=self.confidence_map[issue['issue_confidence']],
                line=issue['line_range'][0],
                end_line=issue['line_range'][-1])
