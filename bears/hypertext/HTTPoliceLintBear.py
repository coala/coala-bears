from coalib.bearlib.abstractions.Linter import linter
from coalib.bears.requirements.PipRequirement import PipRequirement
from coalib.results.RESULT_SEVERITY import RESULT_SEVERITY
from coalib.settings.Setting import typed_list


@linter(executable='httpolice',
        output_format='regex',
        output_regex=r'-*\s*(?P<origin>(request|response).*)\n'
        r'(?P<severity>E|C|D)\s(?P<message>.*)')
class HTTPoliceLintBear:
    """
    HTTPolice is a lint for HTTP requests and responses. It checks them for
    conformance to standards and best practices.

    For more information on the analysis check
    <https://github.com/vfaronov/httpolice>.
    """
    LANGUAGES = {"HAR"}
    REQUIREMENTS = {PipRequirement('HttPolice', '0.2.0')}
    AUTHORS = {'The coala developers'}
    AUTHORS_EMAILS = {'coala-devel@googlegroups.com'}
    LICENSE = 'AGPL-3.0'
    CAN_DETECT = {'Formatting', 'Syntax'}
    severity_map = {'E': RESULT_SEVERITY.MAJOR,
                    'C': RESULT_SEVERITY.NORMAL,
                    'D': RESULT_SEVERITY.INFO}

    @staticmethod
    def create_arguments(filename, file, config_file,
                         silent: typed_list(str)=[]):
        silent = tuple('-s='+part for part in silent)
        args = ("-i", "har") + silent
        return args + (filename,)
