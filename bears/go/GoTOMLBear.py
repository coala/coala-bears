from coalib.bearlib.abstractions.Linter import linter
from dependency_management.requirements.GoRequirement import GoRequirement


@linter(executable='gotoml',
        use_stdin=True,
        output_format='corrected')
class GoTOMLBear:
    """
    It is used to the know the type of every key used in a file.
    """
    LANGUAGES = {'Go'}
    REQUIREMENTS = {
               GoRequirement(package='github.com/BurntSushi/toml/cmd/tomlv',
                             version='0.1.0')}
    AUTHORS = {'The coala developers'}
    AUTHORS_EMAILS = {'coala-devel@googlegroups.com'}
    LICENSE = 'AGPL-3.0'
    CAN_DETECT = {'Data type'}

    @staticmethod
    def create_arguments(filename, file, config_file):
        return ()
