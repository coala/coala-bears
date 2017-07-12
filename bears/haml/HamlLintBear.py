from coalib.bearlib.abstractions.Linter import linter
from dependency_management.requirements.GemRequirement import GemRequirement
from coalib.results.RESULT_SEVERITY import RESULT_SEVERITY


@linter(executable='haml-lint',
        output_format='regex',
        output_regex=r'(?P<filename>\S+):(?P<line>\d+) \[(?P<severity>W|E)\] '
                     r'(?P<message>.*)',
        severity_map={'E': RESULT_SEVERITY.MAJOR,
                      'W': RESULT_SEVERITY.NORMAL},
        use_stdin=True)
class HamlLintBear:
    """
    Checks code using ``haml-lint``. To
    ensure clean and readable HAML code
    """
    LANGUAGES = {'Haml'}
    REQUIREMENTS = {GemRequirement('haml_lint', '0.26.0')}
    AUTHORS = {'The coala developers'}
    AUTHORS_EMAILS = {'coala-devel@googlegroups.com'}
    LICENSE = 'AGPL-3.0'
    SEE_MORE = 'https://github.com/brigade/haml-lint'

    def create_arguments(self, filename, file, config_file):
        args = ('--no-summary', filename)
        if config_file:
            args += ('-c', config_file)

        return args
