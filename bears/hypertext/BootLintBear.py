from coalib.bearlib.abstractions.Linter import linter
from coalib.settings.Setting import typed_list


@linter(executable='bootlint',
        output_format='regex',
        output_regex=r'.+:(?P<line>\d*):(?P<column>\d*) (?P<severity>.)\d+ '
                     r'(?P<message>.+)')
class BootLintBear:
    """
    Raise several common HTML mistakes in html files that are using
    Bootstrap in a fairly "vanilla" way. Vanilla Bootstrap's components/widgets
    require their parts of the DOM to conform to certain structures that is
    checked. Also, raises issues about certain <meta> tags, HTML5 doctype
    declaration, etc. to use bootstrap properly.

    For more about the analysis, check Bootlint
    <https://github.com/twbs/bootlint#bootlint>.
    """
    LANGUAGES = "HTML"

    @staticmethod
    def create_arguments(filename, file, config_file,
                         bootlint_ignore: typed_list(str)=[]):
        """
        :param bootlint_ignore: List of checkers to ignore.
        """
        ignore = ','.join(part.strip() for part in bootlint_ignore)
        return '--disable=' + ignore, filename
