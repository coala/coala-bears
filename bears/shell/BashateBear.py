from coalib.bearlib.abstractions.Linter import linter
from dependency_management.requirements.PipRequirement import PipRequirement
from coalib.settings.Setting import typed_list


@linter(executable='bashate',
        output_format='regex',
        output_regex=r'\[.*?\] (?P<origin>E\d+): '
                     r'(?P<message>.+):.*\s.*: '
                     r'L(?P<line>\d+)')
class BashateBear:
    """
    Bashate is a style-checker for bash scripts.
    """
    LANGUAGES = {'bash'}
    REQUIREMENTS = {PipRequirement('bashate', '0.5.1')}
    AUTHORS = {'The coala developers'}
    AUTHORS_EMAILS = {'coala-devel@googlegroups.com'}
    LICENSE = 'AGPL-3.0'
    CAN_DETECT = {'Syntax', 'Style'}
    SEE_MORE = 'https://docs.openstack.org/bashate'

    def create_arguments(self, filename, file, config_file,
                         bashate_ignore: typed_list(str) = ()):
        """
        :param bashate_ignore: List of rules that should be ignored by bashate.
        """
        args = (filename,)
        if bashate_ignore:
            args += ('-i', ','.join(bashate_ignore))
        return args
