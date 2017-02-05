from coalib.bearlib.abstractions.Linter import linter
from dependency_management.requirements.GoRequirement import GoRequirement


@linter(executable='tomlv',
        use_stderr=True,
        output_format='regex',
        output_regex=r"Error in '.*': "
                     r'Near line (?P<line>\d+) '
                     r"\(last key parsed '.*'\): (?P<message>.*)")
class TOMLBear:
    """
    Checks the code for formatting in ``TOML`` documents and prints
    each key's type. This is done using ``tomlv`` utility.
    """
    LANGUAGES = {'TOML'}
    REQUIREMENTS = {
        GoRequirement('github.com/BurntSushi/toml/cmd/tomlv'),
    }
    AUTHORS = {'The coala developers'}
    AUTHORS_EMAILS = {'coala-devel@googlegroups.com'}
    LICENSE = 'AGPL-3.0'
    CAN_DETECT = {'Formatting', 'Syntax'}
    SEE_MORE = 'https://github.com/BurntSushi/toml/tree/master/cmd/tomlv'

    @staticmethod
    def create_arguments(filename, file, config_file):
        return (filename, )
