from coalib.bearlib.abstractions.Linter import linter
from coalib.settings.Setting import typed_list
from coalib.results.RESULT_SEVERITY import RESULT_SEVERITY

from dependency_management.requirements.PipRequirement import PipRequirement


@linter(executable='httpolice',
        output_format='regex',
        output_regex=r'(?P<severity>E|C|D)\s(?P<message>.*)',
        severity_map={'E': RESULT_SEVERITY.MAJOR,
                      'C': RESULT_SEVERITY.NORMAL,
                      'D': RESULT_SEVERITY.INFO})
class HTTPoliceLintBear:
    """
    HTTPolice is a linter for HTTP requests and responses. It checks them for
    conformance to standards and best practices.
    """
    LANGUAGES = {'HAR'}
    REQUIREMENTS = {PipRequirement('HTTPolice', '0.5.2')}
    AUTHORS = {'The coala developers'}
    AUTHORS_EMAILS = {'coala-devel@googlegroups.com'}
    LICENSE = 'AGPL-3.0'
    CAN_DETECT = {'Formatting', 'Syntax'}
    SEE_MORE = 'https://github.com/vfaronov/httpolice'

    @staticmethod
    def create_arguments(filename, file, config_file,
                         httpolice_silence_ids: typed_list(str)=[]):
        """
        :param httpolice_silence_ids:
            Silences the given list of notice IDs. You can get more information
            about the available notices and their IDs at
            https://httpolice.readthedocs.io/en/stable/notices.html.
        """
        args = '-i', 'har', filename
        if httpolice_silence_ids:
            args += tuple('-s=' + part for part in httpolice_silence_ids)
        return args
