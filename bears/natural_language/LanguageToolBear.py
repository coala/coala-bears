import shutil
import logging

from guess_language import guess_language

from coalib.bearlib import deprecate_settings
from coalib.bears.LocalBear import LocalBear
from dependency_management.requirements.PipRequirement import PipRequirement
from coalib.results.Diff import Diff
from coalib.results.Result import Result
from coalib.results.SourceRange import SourceRange
from coalib.settings.Setting import typed_list


class LanguageToolBear(LocalBear):
    LANGUAGES = {'Natural Language'}
    REQUIREMENTS = {PipRequirement('guess-language-spirit', '0.5.2'),
                    PipRequirement('language-tool-python', '2.5.4')}
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
                from language_tool_python import LanguageTool
                from language_tool_python.utils import correct
                LanguageTool
                correct
                return True
            except ImportError:
                return 'Please install the `language-tool-python` pip package.'

    @deprecate_settings(natural_language=('language', 'locale'))
    def run(self,
            filename,
            file,
            natural_language: str = 'auto',
            languagetool_disable_rules: typed_list(str) = (),
            ):
        """
        Checks the code with LanguageTool.

        :param natural_language:           A locale representing the language
                                           you want to have checked. If set to
                                           'auto' the language is guessed.
                                           If the language cannot be guessed or
                                           an unsupported language is guessed,
                                           'en-US' is used.
        :param languagetool_disable_rules: List of rules to disable checks for.
        """
        # Defer import so the check_prerequisites can be run without
        # language_tool_python being there.
        from language_tool_python import LanguageTool
        from language_tool_python.utils import correct

        joined_text = ''.join(file)
        natural_language = (guess_language(joined_text)
                            if natural_language == 'auto'
                            else natural_language)

        try:
            tool = LanguageTool(natural_language, motherTongue='en_US')
        except ValueError:
            # Using 'en-US' if guessed language is not supported
            logging.warn(
                "Changing the `natural_language` setting to 'en-US' as "
                '`language_tool_python` failed to guess a valid language.'
            )
            natural_language = 'en-US'
            tool = LanguageTool(natural_language, motherTongue='en_US')

        tool.disabled_rules.update(languagetool_disable_rules)
        matches = tool.check(joined_text)
        for match in matches:
            if not match.replacements:
                diffs = None
            else:
                replaced = correct(joined_text, [match]).splitlines(True)
                diffs = {filename:
                         Diff.from_string_arrays(file, replaced)}

            rule_id = match.ruleId

            message = match.message + ' (' + rule_id + ')'
            source_range = SourceRange.from_values(filename,
                                                   match.offset+1,
                                                   match.errorLength+1,
                                                   match.errorLength+match.offset+1,
                                                   len(match.replacements)+1)
            yield Result(self, message, diffs=diffs,
                         affected_code=(source_range,))
