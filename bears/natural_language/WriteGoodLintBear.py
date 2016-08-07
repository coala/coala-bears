from coalib.bearlib.abstractions.Linter import linter
from coalib.bears.requirements.NpmRequirement import NpmRequirement


@linter(executable='write-good',
        output_format='regex',
        output_regex=r'(?P<message>.*)\s*on\s*line\s*(?P<line>\d+)\s*at\s'
                      'column\s*(?P<column>\d+)'
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
    ASCIINEMA_URL = 'https://asciinema.org/a/80761'
    CAN_DETECT = {'Formatting', 'Grammar'}

    @staticmethod
    def create_arguments(filename, file, config_file,
                         allow_passive_voice: bool=False,
                         allow_so_beginning: bool=False,
                         allow_adverbs: bool=False,
                         allow_repeated_words: bool=False,
                         allow_there_is: bool=False,
                         allow_ambiguous_words: bool=False,
                         allow_extra_words: bool=False,
                         allow_cliche_phrases: bool=False):
        """
        Using ``True`` will enable the check.

        :param allow_passive_voice:     Allows passive voice.
        :param allow_so_beginning:      Allows ``So`` at the beginning of
                                        the sentence.
        :param allow_adverbs:           Allows adverbs that can weaken the
                                        meaning, such as: ``really``,
                                        ``very``, ``extremely``, etc.
        :param allow_repeated_words:    Allows lexical illusions – cases
                                        where a word is repeated.
        :param allow_there_is:          Allows ``There is`` or ``There are``
                                        at the beginning of the sentence.
        :param allow_ambiguous_words:   Allows ``weasel words`` for example
                                        ``often``, ``probably``
        :param allow_extra_words:       Allows wordy phrases and unnecessary
                                        words.
        :param allow_cliche_phrases:    Allows common cliche phrases in the
                                        sentence.
        """
        arg_map = {
            'allow_passive_voice': '--passive',
            'allow_so_beginning': '--so',
            'allow_adverbs': '--adverb',
            'allow_repeated_words': '--illusion',
            'allow_there_is': '--thereIs',
            'allow_ambiguous_words': '--weasel',
            'allow_extra_words': '--tooWordy',
            'allow_cliche_phrases': '--cliches'
        }
        l = locals()
        args = tuple(arg for key, arg in arg_map.items()
                     if l[key])
        return args + (filename,)
