import re
import textwrap

from coalib.bearlib.languages.documentation.DocumentationComment import (
    DocumentationComment)
from coalib.bearlib.languages.documentation.DocstyleDefinition import (
    DocstyleDefinition)
from coalib.bearlib.languages.documentation.DocumentationExtraction import (
    extract_documentation)
from coalib.bears.LocalBear import LocalBear
from coalib.results.Diff import Diff
from coalib.results.Result import Result


class coalaBear(LocalBear):
    LANGUAGES = {language for docstyle, language in
                 DocstyleDefinition.get_available_definitions()}
    AUTHORS = {'The coala developers'}
    AUTHORS_EMAILS = {'coala-devel@googlegroups.com'}
    LICENSE = 'AGPL-3.0'
    # TODO: maybe later
    ASCIINEMA_URL = 'https://asciinema.org/a/4p1i873ebi9qdfmczn2tvxrm0'
    CAN_DETECT = {'TODO'}  # TODO

    def run(self, filename, file, docstyle, language):
        """
        Checks for certain in-code documentation styles.
        """
        # TODO This checks only for one certain style (and really roughly):
        """
        my style as this one is easier

        :param x:
            4 space indent
        :return:
            also 4 space indent
            following lines are also 4 space indented
        """

        for doc_comment in extract_documentation(file, language, docstyle):
            doc_comment.indent
            doc_comment.marker
            doc_comment.range

            metadata = iter(doc_comment.parse())

            # Assuming that the first element is always the only description.
            description = next(metadata)

            # TODO Don't use `m`, I'm just lazy :3
            new_items = [description] + [
                m._replace(desc=textwrap.indent(m.desc.lstrip(), " " * 4))
                for m in metadata]

            new_comment = DocumentationComment.from_metadata(
                new_items, doc_comment.docstyle_definition, doc_comment.marker,
                doc_comment.indent, doc_comment.range)

            if new_comment != doc_comment:
                # Something changed, let's apply a result.
                diff = Diff()

                # Delete the old comment
                for i in range(doc_comment.range.start_line,
                               doc_comment.range.end_line + 1):
                    diff.delete_line(i)

                # Apply the new comment
                diff.add_lines(new_comment.range.start_line,
                               new_comment.assemble().splitlines()) # <-- Not sure, maybe you need to use "keepends=True"

                self.new_result("Documentation comment does not have correct style.",
                                affected_code=(diff.range(filename),),
                                diffs={filename: diff})
