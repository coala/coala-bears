from coalib.bearlib import deprecate_settings
from coalib.bearlib.abstractions.Linter import linter
from coalib.bears.requirements.NpmRequirement import NpmRequirement
from coala_utils.param_convertion import negate


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
    @deprecate_settings(allow_passive_voice=('check_passive_voice', negate),
                        allow_so_beginning=('check_so_beginning', negate),
                        allow_adverbs=('check_adverbs', negate),
                        allow_repeated_words=('check_repeated_words', negate),
                        allow_there_is=('check_there_is', negate),
                        allow_ambiguous_words=('check_ambiguos_words', negate),
                        allow_extra_words=('check_extra_words', negate),
                        allow_cliche_phrases=('check_cliche_exists', negate))
    def create_arguments(filename, file, config_file,
                         allow_passive_voice: bool=True,
                         allow_so_beginning: bool=True,
                         allow_adverbs: bool=True,
                         allow_repeated_words: bool=True,
                         allow_there_is: bool=True,
                         allow_ambiguous_words: bool=True,
                         allow_extra_words: bool=True,
                         allow_cliche_phrases: bool=True):
        """
        Using ``False`` will enable the check.

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
                     if not l[key])
        return args + (filename,)
