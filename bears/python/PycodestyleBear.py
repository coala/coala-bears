from coalib.bearlib.abstractions.Linter import linter
from coalib.settings.Setting import typed_list

from dependency_management.requirements.PipRequirement import PipRequirement


@linter(executable='pycodestyle',
        output_format='regex',
        output_regex=r'(?P<line>\d+) (?P<column>\d+) '
                     r'(?P<message>(?P<origin>\S+).*)')
class PycodestyleBear:
    """
    A wrapper for the tool ``pycodestyle`` formerly known as ``pep8``.
    """
    LANGUAGES = {'Python', 'Python 2', 'Python 3'}
    REQUIREMENTS = {PipRequirement('pycodestyle', '2.2')}
    AUTHORS = {'The coala developers'}
    AUTHORS_EMAILS = {'coala-devel@googlegroups.com'}
    LICENSE = 'AGPL-3.0'
    CAN_DETECT = {'Formatting'}

    @staticmethod
    def create_arguments(
            filename, file, config_file,
            pycodestyle_ignore: typed_list(str)=(
                'E121', 'E123', 'E126', 'E133', 'E226',
                'E241', 'E242', 'E704', 'W503'
            ),
            pycodestyle_select: typed_list(str)=(),
            max_line_length: int=79):
        """
        :param pycodestyle_ignore:
            Comma separated list of errors to ignore.
            See ``pydocstyle`` documentation for a complete list of errors.
        :param pycodestyle_select:
            Comma separated list of errors to detect. If given only
            these errors are going to be detected.
            See ``pydocstyle`` documentation for a complete list of errors.
        :param max_line_length:
            Limit lines to this length.
        """
        arguments = [r'--format=%(row)d %(col)d %(code)s %(text)s']

        if pycodestyle_ignore:
            ignore = ','.join(part.strip() for part in pycodestyle_ignore)
            arguments.append('--ignore=' + ignore)

        if pycodestyle_select:
            select = ','.join(part.strip() for part in pycodestyle_select)
            arguments.append('--select=' + select)

        arguments.append('--max-line-length=' + str(max_line_length))

        arguments.append(filename)

        return arguments
