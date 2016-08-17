from coalib.bears.LocalBear import LocalBear
from coalib.results.Diff import Diff
from coalib.results.Result import Result

from coalib.results.SourceRange import SourceRange
from coalib.results.SourcePosition import SourcePosition
from coalib.bearlib.languages.documentation.DocstyleDefinition import (
    DocstyleDefinition)
from coalib.bearlib.languages.documentation.DocumentationExtraction import (
    extract_documentation)
from coalib.bearlib.languages.documentation.DocumentationComment import (
    DocumentationComment)


class DocCapitalizeBear(LocalBear):
    LANGUAGES = "All"

    @staticmethod
    def capitalize_first_char(line):
        newline = ""

        for nr, char in enumerate(line):
            if char.isalpha():
                break

        newline += line[:nr] + line[nr].capitalize() + line[nr + 1:]
        return newline

    @staticmethod
    def capitalize_lines(lines):
        lines = lines.splitlines(keepends=True)

        newlines = []

        for nr, line in enumerate(lines):
            prevline = lines[nr - 1].strip()
            if not prevline == "":
                if not prevline.endswith(".") and nr != 0:
                    newlines.append(line)
                    continue
            newlines.append(DocCapitalizeBear.capitalize_first_char(line))

        return "".join(newlines)

    def run(self, filename, file,
            language: str, docstyle: str):
        """
        This bear capitalizes every description in every docstring.

        :param language: The language of the file
        :param docstyle: The docstyle (default, doxygen)
        """

        docs = extract_documentation(file, language, docstyle)
        docstyle_definition = DocstyleDefinition.load(language, docstyle)
        for doc in docs:
            bigdiff = Diff(file)
            docdata = doc.parse()
            for section_nr, section in enumerate(docdata):
                section_modified = section._replace(
                    desc=self.capitalize_lines(section.desc))
                docdata.pop(section_nr)
                docdata.insert(section_nr, section_modified)
            final = (DocumentationComment.from_metadata(docdata,
                                                        docstyle_definition,
                                                        doc.marker,
                                                        doc.indent,
                                                        doc.range))
            pos = doc.range.start.line
            for line in final.assemble().splitlines(True):
                bigdiff.change_line(pos, file[doc.range.start.line], line)
                pos += 1
            if bigdiff:
                yield Result(
                    origin=self,
                    message="Sentence not capitalized.",
                    affected_code=(bigdiff.range(filename),),
                    diffs={filename: bigdiff})
