import shutil

from guess_language import guess_language

from coalib.bearlib import deprecate_settings
from coalib.bears.LocalBear import LocalBear
from coalib.bears.requirements.PipRequirement import PipRequirement
from coalib.results.Diff import Diff
from coalib.results.Result import Result
from coalib.results.SourceRange import SourceRange
from coalib.settings.Setting import typed_list


class LanguageToolBear(LocalBear):
    LANGUAGES = {'Natural Language'}
    REQUIREMENTS = {PipRequirement('guess-language-spirit', '0.5'),
                    PipRequirement('language-check', '0.8')}
    AUTHORS = {'The coala developers'}
    AUTHORS_EMAILS = {'coala-devel@googlegroups.com'}
    LICENSE = 'AGPL-3.0'
    CAN_DETECT = {'Spelling', 'Grammar'}

    @classmethod
    def check_prerequisites(cls):
        if shutil.which('java') is None:
            return 'java is not installed.'
        else:
            try:
                from language_check import LanguageTool, correct
                return True
            except ImportError:  # pragma: no cover
                return 'Please install the `language-check` pip package.'

    @deprecate_settings(language='locale')
    def run(self,
            filename,
            file,
            language: str='auto',
            languagetool_disable_rules: typed_list(str)=()):
        '''
        Checks the code with LanguageTool.

        :param language:                   A locale representing the language
                                           you want to have checked. If set to
                                           'auto' the language is guessed.
                                           If the language cannot be guessed,
                                           'en-US' is used.
        :param languagetool_disable_rules: List of rules to disable checks for.
        '''
        # Defer import so the check_prerequisites can be run without
        # language_check being there.
        from language_check import LanguageTool, correct

        joined_text = ''.join(file)
        language = (guess_language(joined_text)
                    if language == 'auto' else language)
        language = 'en-US' if not language else language

        tool = LanguageTool(language, motherTongue='en_US')
        tool.disabled.update(languagetool_disable_rules)

        matches = tool.check(joined_text)
        for match in matches:
            if not match.replacements:
                diffs = None
            else:
                replaced = correct(joined_text, [match]).splitlines(True)
                diffs = {filename:
                         Diff.from_string_arrays(file, replaced)}

            rule_id = match.ruleId
            if match.subId is not None:
                rule_id += '[{}]'.format(match.subId)

            message = match.msg + ' (' + rule_id + ')'
            source_range = SourceRange.from_values(filename,
                                                   match.fromy+1,
                                                   match.fromx+1,
                                                   match.toy+1,
                                                   match.tox+1)
            yield Result(self, message, diffs=diffs,
                         affected_code=(source_range,))
