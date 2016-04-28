import shutil

from guess_language import guess_language
from language_check import LanguageTool, correct

from coalib.bears.LocalBear import LocalBear
from coalib.results.Diff import Diff
from coalib.results.Result import Result
from coalib.results.SourceRange import SourceRange
from coalib.settings.Setting import typed_list


class LanguageToolBear(LocalBear):
    LANGUAGES = "Natural Language"

    @classmethod
    def check_prerequisites(cls):
        if shutil.which("java") is None:
            return "java is not installed."
        else:
            return True

    def run(self,
            filename,
            file,
            locale: str='auto',
            languagetool_disable_rules: typed_list(str)=()):
        '''
        Checks the code with LanguageTool.

        :param locale:                     A locale representing the language
                                           you want to have checked. If set to
                                           'auto' the language is guessed.
                                           If the language cannot be guessed,
                                           'en-US' is used.
        :param languagetool_disable_rules: List of rules to disable checks for.
        '''
        joined_text = "".join(file)
        locale = guess_language(joined_text) if locale == 'auto' else locale
        locale = 'en-US' if not locale else locale

        tool = LanguageTool(locale, motherTongue="en_US")
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
