from coalib.bearlib.abstractions.Linter import linter
from coalib.bears.requirements.NpmRequirement import NpmRequirement


@linter(executable='write-good',
        output_format='regex',
        output_regex=r'(?P<message>.*)\s*on\s*line\s*(?P<line>\d+)\s*at\scolumn'
                      '\s*(?P<column>\d+)'
        )
class WriteGoodLintBear:
    """
    Lints the text files using ``write-good`` for improving proses.
    For more information on this tool, visit
    https://github.com/btford/write-good
    """
    LANGUAGES = {"Natural Language"}
    REQUIREMENTS = {NpmRequirement('write-good', '0.9.1')}
    AUTHORS = {'The coala developers'}
    AUTHORS_EMAILS = {'coala-devel@googlegroups.com'}
    LICENSE = 'AGPL-3.0'
    CAN_DETECT = {'Formatting', 'Grammar'}

    @staticmethod
    def create_arguments(filename, file, config_file,
                         passive: bool=False,
                         illusion: bool=False,
                         adverb: bool=False,
                         so: bool=False,
                         thereIs: bool=False,
                         weasel: bool=False,
                         tooWordy: bool=False,
                         cliches: bool=False):
        """
        Bear configuration arguments.
        Using ``False`` will disable the check.

        :param passive:        Checks for passive voice
        :param so:             Checks for ``So`` at the beginning of the
                               sentence.
        :param adverb:         Checks for adverbs that can weaken meaning, such
                               as: ``really``, ``very``, ``extremely``, etc.
        :param illusion:       Checks for lexical illusions – cases where a word
                               is repeated.
        :param thereIs:        Checks for ``There is`` or ``There are`` at the
                               beginning of the sentence.
        :param weasel:         Checks for ``weasel words``.
        :param tooWordy:       Checks for wordy phrases and unnecessary words.
        :param cliches:        Checks for common cliches.
        """
        args = ()
        if passive:
            args += ("--passive",)
        if so:
            args += ("--so",)
        if adverb:
            args += ("--adverb",)
        if illusion:
            args += ("--illusion",)
        if thereIs:
            args += ("--thereIs",)
        if weasel:
            args += ("--weasel",)
        if tooWordy:
            args += ("--tooWordy",)
        if cliches:
            args += ("--cliches",)
        return args + (filename,)
