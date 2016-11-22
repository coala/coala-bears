import json

from coalib.bearlib.abstractions.Linter import linter
from coalib.bears.requirements.PipRequirement import PipRequirement
from coalib.results.Result import Result
from coalib.results.RESULT_SEVERITY import RESULT_SEVERITY
from coalib.settings.Setting import typed_list


@linter(executable='bandit')
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
    def create_arguments(filename, file, config_file,
                         bandit_skipped_tests: typed_list(str)=
                         ('B105', 'B106', 'B107', 'B404', 'B603', 'B606',
                          'B607')):
        """
        :param bandit_skipped_tests:
            The IDs of the tests ``bandit`` shall not perform. You can get
            information about the available builtin codes at
            https://github.com/openstack/bandit#usage.
        """
        args = (filename, '-f', 'json')

        if bandit_skipped_tests:
            args += ('-s', ','.join(bandit_skipped_tests))

        return args

    severity_map = {'HIGH': RESULT_SEVERITY.MAJOR,
                    'MEDIUM': RESULT_SEVERITY.NORMAL,
                    'LOW': RESULT_SEVERITY.INFO}

    confidence_map = {'HIGH': 90,
                      'MEDIUM': 70,
                      'LOW': 50}

    def process_output(self, output, filename, file):
        output = json.loads(output)

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
