import shutil

from coalib.bearlib.languages.documentation.DocumentationComment import (
    DocumentationComment)
from coalib.bearlib.languages.documentation.DocstyleDefinition import (
    DocstyleDefinition)
from coalib.bearlib.languages.documentation.DocBaseClass import (
    DocBaseClass)
from dependency_management.requirements.PipRequirement import PipRequirement
from coalib.bears.LocalBear import LocalBear
from coalib.results.Result import Result
from coalib.settings.Setting import typed_list


class DocGrammarBear(DocBaseClass, LocalBear):
    LANGUAGES = {language for docstyle, language in
                 DocstyleDefinition.get_available_definitions()}
    REQUIREMENTS = {PipRequirement('language-check', '1.0')}
    AUTHORS = {'The coala developers'}
    AUTHORS_EMAILS = {'coala-devel@googlegroups.com'}
    LICENSE = 'AGPL-3.0'
    ASCIINEMA_URL = 'https://asciinema.org/a/132564'
    CAN_FIX = {'Documentation', 'Spelling', 'Grammar'}

    @classmethod
    def check_prerequisites(cls):
        if shutil.which('java') is None:
            return 'java is not installed.'
        else:
            try:
                from language_check import LanguageTool, correct
                LanguageTool
                correct
                return True
            except ImportError:  # pragma: no cover
                return 'Please install the `language-check` pip package.'

    def process_documentation(self,
                              parsed,
                              locale,
                              languagetool_disable_rules):
        """
        This fixes the parsed documentation comment by applying spell checking
        and grammatic rules via LanguageTool.

        :param parsed:
            Contains parsed documentation comment.
        :param locale:
            A locale representing the language you want to have checked.
            Default is set to 'en-US'.
        :param languagetool_disable_rules:
            List of rules to disable checks for.
        :return:
            A tuple of fixed parsed documentation comment and warning_desc.
        """
        # Defer import so the check_prerequisites can be run without
        # language_check being there.
        from language_check import LanguageTool, correct

        tool = LanguageTool(locale)
        tool.disabled.update(languagetool_disable_rules)

        metadata = iter(parsed)

        new_metadata = []
        for comment in metadata:
            matches = tool.check(comment.desc)
            new_desc = correct(comment.desc, matches)
            new_metadata.append(comment._replace(desc=new_desc))

        return (new_metadata,
                'Documentation has invalid Grammar/Spelling')

    def run(self, filename, file, language: str,
            docstyle: str='default', locale: str='en-US',
            languagetool_disable_rules: typed_list(str)=()):
        """
        Checks the main description and comments description of documentation
        with LanguageTool. LanguageTool finds many errors that a simple spell
        checker cannot detect and several grammar problems. A full list of
        rules for english language can be found here at:
        https://community.languagetool.org/rule/list?lang=en
        LanguageTool currently supports more than 25 languages. For further
        information, visit: https://www.languagetool.org/languages/

        :param language:
            The programming language of the file(s).
        :param docstyle:
            The docstyle to use. For example ``default`` or ``doxygen``.
            Docstyles are language dependent, meaning not every language is
            supported by a certain docstyle.
        :param locale:
            A locale representing the language you want to have checked.
            Default is set to 'en-US'.
        :param languagetool_disable_rules:
            List of rules to disable checks for.
        """
        for doc_comment in self.extract(file, language, docstyle):
            parsed = doc_comment.parse()

            (new_metadata, warning_desc) = self.process_documentation(
                parsed, locale, languagetool_disable_rules)

            new_comment = DocumentationComment.from_metadata(
                new_metadata, doc_comment.docstyle_definition,
                doc_comment.marker, doc_comment.indent, doc_comment.position)

            if new_comment != doc_comment:
                # Something changed, let's apply a result.
                diff = self.generate_diff(file, doc_comment, new_comment)

                yield Result(
                    origin=self,
                    message=warning_desc,
                    affected_code=(diff.range(filename),),
                    diffs={filename: diff})
