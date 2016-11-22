from coalib.bearlib.abstractions.Linter import linter


@linter(executable='infer',
        output_format='regex',
        output_regex=r'.+:(?P<line>\d+): (?P<severity>error|warning): '
                     r'(?P<message>.*)')
class InferBear:
    """
    Checks the code with ``infer``.
    """
    LANGUAGES = {"Java", "Objective-C", "C"}
    AUTHORS = {'The coala developers'}
    AUTHORS_EMAILS = {'coala-devel@googlegroups.com'}
    LICENSE = 'AGPL-3.0'
    ASCIINEMA_URL = 'https://asciinema.org/a/1g2k0la7xo5az9t8f1v5zy66q'
    CAN_DETECT = {'Security'}

    def create_arguments(self, filename, file, config_file, language: str):
        """
        :param language: The language to analyze (Java, Objective-C or C).
        """
        language_args = {
            'java': ('javac',),
            'objective-c': ('clang', '-c'),
            'c': ('gcc', '-c')
        }
        if language not in language_args:
            self.err("Invalid language given! Falling back to Java.")
            language = 'java'

        return ('-npb', '--') + language_args[language.lower()] + (filename,)
