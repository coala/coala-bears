import re

from coalib.bears.LocalBear import LocalBear
from coalib.bearlib.naming_conventions import (
    to_camelcase, to_pascalcase, to_snakecase)
from bears.general.AnnotationBear import AnnotationBear
from coalib.bearlib.languages.LanguageDefinition import LanguageDefinition
from coalib.results.SourceRange import SourceRange
from coalib.results.Diff import Diff
from coalib.results.Result import Result
from coalib.results.HiddenResult import HiddenResult


class CasingBear(LocalBear):

    def run(self,
            filename,
            file,
            dependency_results,
            casing: str,
            language: str,
            coalang_dir: str=None):
        """
        Checks whether all identifier names (variables, classes, objects)
        follow a certain naming convention.

        :param filename:           Name of the file that needs to be checked.
        :param file:               File that needs to be checked in the form
                                   of a list of strings.
        :param dependency_results: A dict of dependencies with bear name as
                                   key and results as value.
        :param casing:             "camel" for camelCasing or "snake" for
                                   snake_casing or "pascal" for PascalCasing.
        :param language:           The language of the file, which is used to
                                   determine the keywords to ignore.
        :param coalang_dir:        External directory for the coalang file.
        """
        casing_convention = {"camel": to_camelcase,
                             "pascal": to_pascalcase,
                             "snake": to_snakecase}
        if casing not in casing_convention:
            self.err("Invalid casing convention provided: " + casing)
            return
        convertor = casing_convention[casing]

        try:
            coalang = LanguageDefinition(language, coalang_dir=coalang_dir)
        except:
            content = ("coalang specification for " + language +
                       " not found.")
            yield HiddenResult(self, content)
            return

        # TODO: Adapt after coala/coala/issues/2200 is solved
        if "keywords" not in coalang or "special_chars" not in coalang:
            self.err("'keywords' and 'special_chars' are necessary fields "
                     "that are missing from the coalang definition "
                     "for {}.".format(language))
            return

        keywords = coalang["keywords"]

        # this prepares the list of special characters in the language for
        # regex by escaping the characters appropriately. This will later
        # be fed to a ``re.split``.
        delim = re.escape(str(coalang["special_chars"]) + " \t\n")

        annotations = dependency_results[AnnotationBear.name][0].contents
        string_results = annotations["strings"]
        source_ranges = []
        last_line = 1
        last_column = 1
        text = "".join(file)
        for string_range in string_results:
            source_ranges.append(SourceRange.from_values(
                text,
                start_line=last_line,
                start_column=last_column,
                end_line=string_range.start.line,
                end_column=string_range.start.column))
            last_line = string_range.end.line
            last_column = string_range.end.column
        source_ranges.append(SourceRange.from_values(
            text,
            start_line=last_line,
            start_column=last_column,
            end_line=len(file),
            end_column=len(file[-1])))

        changes = {}
        for result in source_ranges:
            line_number = result.start.line
            while line_number <= result.end.line:
                start = result.start.column if (
                        line_number == result.start.line) else 0
                end = result.end.column if (
                      line_number == result.end.line) else (
                      len(file[line_number - 1]))

                line_changes = self.generate_changes(
                    file[line_number - 1][start:end],
                    delim,
                    keywords,
                    convertor)
                for prev in line_changes:
                    changes[prev] = line_changes[prev]

                line_number += 1

        lines_changed = set()
        result_texts = []
        for prev in changes:
            change = changes[prev]
            diff = Diff(file)
            first_line = -1
            skip_var = False

            for line_number, line in enumerate(file, start=1):
                rep = re.sub("(?P<g1>[\\" + delim + "]*)" + prev +
                             "(?P<g2>[\\" + delim + "]*)",
                             "\g<g1>" + change + "\g<g2>", line)

                if rep != line:
                    if line_number in lines_changed:
                        skip_var = True
                    lines_changed.add(line_number)
                    diff.change_line(line_number, line, rep)
                    if first_line == -1:
                        first_line = line_number

            if skip_var:
                continue

            msg = "Change '" + prev + "' to '" + change + "'"
            result_texts.append(msg)
            name_changes = "The following name change is suggested:"
            name_changes += "".join("\n- " + string
                                    for string in result_texts)

            yield Result.from_values(
                self,
                name_changes,
                diffs={filename: diff},
                file=filename,
                line=first_line)
            result_texts = []

    def generate_changes(self, content, delim, keywords, convertor):
        """
        Processes the string by splitting it based on delimiters
        and then generate the casing changes.

        :param content:   The string to be processed.
        :param delim:     A string of characters that are to be used as
                          delimiters.
        :param keywords:  A ``Setting`` containing the keywords specific for
                          the language.
        :param convertor: A function that takes a string as input and
                          converts it to the appropriate casing.
        :return:          A dict with current casing as key and
                          proposed change as value.
        """
        splits = re.split("[" + delim + "]", content)
        results = {}
        for split in splits:
            if split not in keywords:
                converted = convertor(split)
                if split != converted:
                    results[split] = converted
        return results

    @staticmethod
    def get_dependencies():
        return [AnnotationBear]  # pragma: no cover
