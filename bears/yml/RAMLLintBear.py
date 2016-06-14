from coalib.bearlib.abstractions.Linter import linter


@linter(executable='ramllint',
        output_format='regex',
        output_regex=r'(?P<severity>error|warning|info).*\n  (?P<message>.+) '
                     r'\[(?P<origin>.+)\]')
class RAMLLintBear:
    """
    RAML Linter is a static analysis, linter-like, utility that will enforce
    rules on a given RAML document, ensuring consistency and quality.
    Note: Files should not have leading empty lines, else the bear fails to
    identify the problems correctly.
    """

    LANGUAGES = {"RAML"}
    AUTHORS = {'The coala developers'}
    AUTHORS_EMAILS = {'coala-devel@googlegroups.com'}
    LICENSE = 'AGPL-3.0'

    @staticmethod
    def create_arguments(filename, file, config_file):
        return filename,
