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

    See <https://github.com/btford/write-good> for more information.
    """
    LANGUAGES = {"Natural Language"}
    REQUIREMENTS = {NpmRequirement('write-good', '0.9.1')}
    AUTHORS = {'The coala developers'}
    AUTHORS_EMAILS = {'coala-devel@googlegroups.com'}
    LICENSE = 'AGPL-3.0'
    CAN_DETECT = {'Formatting', 'Grammar'}

    @staticmethod
    def create_arguments(filename, file, config_file,
                         check_passive_voice: bool=False,
                         check_so_beginning: bool=False,
                         check_adverbs: bool=False,
                         check_repeated_words: bool=False,
                         check_there_is: bool=False,
                         check_ambiguos_words: bool=False,
                         check_extra_words: bool=False,
                         check_cliche_exists: bool=False):
        """
        Using ``True`` will enable the check.

        :param check_passive_voice:     Checks for passive voice.
        :param check_so_beginning:      Checks for ``So`` at the beginning of
                                        the sentence.
        :param check_adverbs:           Checks for adverbs that can weaken the
                                        meaning, such as: ``really``, ``very``,
                                        ``extremely``, etc.
        :param check_repeated_words:    Checks for lexical illusions – cases
                                        where a word is repeated.
        :param check_there_is:          Checks for ``There is`` or ``There are``
                                        at the beginning of the sentence.
        :param check_ambiguos_words:    Checks for ``weasel words`` for example
                                        ``often``, ``probably``
        :param check_extra_words:       Checks for wordy phrases and
                                        unnecessary words.
        :param check_cliche_exists:     Checks for common cliche phrases in the
                                        sentence.
        """
        arg_map = {
            'check_passive_voice': '--passive',
            'check_so_beginning': '--so',
            'check_adverbs': '--adverb',
            'check_repeated_words': '--illusion',
            'check_there_is': '--thereIs',
            'check_ambiguos_words': '--weasel',
            'check_extra_words': '--tooWordy',
            'check_cliche_exists': '--cliches'
        }
        l = locals()
        args = tuple(arg for key, arg in arg_map.items()
                     if l[key])
        return args + (filename,)
