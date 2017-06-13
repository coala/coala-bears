from coalib.bearlib.languages.documentation.DocumentationComment import (
    DocumentationComment)
from coalib.bearlib.languages.documentation.DocstyleDefinition import (
    DocstyleDefinition)
from coalib.bearlib.languages.documentation.DocumentationExtraction import (
    extract_documentation)
from coalib.bears.LocalBear import LocalBear
from coalib.results.Diff import Diff
from coalib.results.Result import Result
from coalib.results.TextRange import TextRange


class DocumentationStyleBear(LocalBear):
    LANGUAGES = {language for docstyle, language in
                 DocstyleDefinition.get_available_definitions()}
    AUTHORS = {'The coala developers'}
    AUTHORS_EMAILS = {'coala-devel@googlegroups.com'}
    LICENSE = 'AGPL-3.0'
    ASCIINEMA_URL = 'https://asciinema.org/a/7sfk3i9oxs1ixg2ncsu3pym0u'
    CAN_DETECT = {'Documentation'}
    CAN_FIX = {'Documentation'}

    def run(self, filename, file, language: str,
            docstyle: str='default', allow_missing_func_desc: str=False,
            indent_size: int=4):
        """
        Checks for certain in-code documentation styles.

        It currently checks for the following style: ::

            The first line needs to have no indentation.
                - Following lines can have indentation

            :param x:
                4 space indent
            :return:
                also 4 space indent
                following lines are also 4 space indented

        :param language: The programming language of the file(s).
        :param docstyle: The docstyle to use. For example ``default`` or
                         ``doxygen``. Docstyles are language dependent, meaning
                         not every language is supported by a certain docstyle.
        :param allow_missing_func_desc: When set ``True`` this will allow
                         functions with missing descriptions, allowing
                         functions to start with params.
        :param indent_size: Number of spaces per indentation level.
        """
        for doc_comment in extract_documentation(file, language, docstyle):
            parsed = doc_comment.parse()
            metadata = iter(parsed)

            # Assuming that the first element is always the only main
            # description.
            main_description = next(metadata)

            if main_description.desc == '\n' and not allow_missing_func_desc:
                warning_desc = """
Missing function description.
Please set allow_missing_func_desc = True to ignore this warning.
"""
            else:
                warning_desc = 'Documentation does not have correct style.'

            # one empty line shall follow main description (except it's empty
            # or no annotations follow).
            if main_description.desc.strip() != '':
                main_description = main_description._replace(
                    desc='\n' + main_description.desc.strip() + '\n' *
                         (1 if len(parsed) == 1 else 2))

            new_metadata = [main_description]
            for m in metadata:
                # Split newlines and remove leading and trailing whitespaces.
                stripped_desc = list(map(str.strip, m.desc.splitlines()))

                if len(stripped_desc) == 0:
                    # Annotations should be on their own line, though no
                    # further description follows.
                    stripped_desc.append('')
                else:
                    # Wrap parameter description onto next line if it follows
                    # annotation directly.
                    if stripped_desc[0] != '':
                        stripped_desc.insert(0, '')

                # Indent with 4 spaces.
                stripped_desc = ('' if line == '' else ' ' * indent_size
                                 + line for line in stripped_desc)

                new_desc = '\n'.join(stripped_desc)

                # Strip away trailing whitespaces and obsolete newlines (except
                # one newline which is mandatory).
                new_desc = new_desc.rstrip() + '\n'

                new_metadata.append(m._replace(desc=new_desc.lstrip(' ')))

            new_comment = DocumentationComment.from_metadata(
                new_metadata, doc_comment.docstyle_definition,
                doc_comment.marker, doc_comment.indent, doc_comment.range)

            if new_comment != doc_comment:
                # Something changed, let's apply a result.
                diff = Diff(file)

                # We need to update old comment positions, as `assemble()`
                # prepends indentation for first line.
                old_range = TextRange.from_values(
                    doc_comment.range.start.line,
                    1,
                    doc_comment.range.end.line,
                    doc_comment.range.end.column)
                diff.replace(old_range, new_comment.assemble())

                yield Result(
                    origin=self,
                    message=warning_desc,
                    affected_code=(diff.range(filename),),
                    diffs={filename: diff})
