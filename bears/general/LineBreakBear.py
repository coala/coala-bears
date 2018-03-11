from queue import Queue

from coalib.results.AbsolutePosition import AbsolutePosition
from coalib.results.Diff import Diff
from coalib.bearlib.languages.LanguageDefinition import LanguageDefinition
from coalib.bears.LocalBear import LocalBear
from coalib.results.Result import Result, RESULT_SEVERITY
from coalib.results.SourceRange import SourceRange
from coalib.bearlib.spacing.SpacingHelper import SpacingHelper

from bears.general.AnnotationBear import AnnotationBear
from bears.general.RangeHelpers import get_specified_block_range
from bears.general.LineLengthBear import LineLengthBear


class LineBreakBear(LocalBear):
    AUTHORS = {'The coala developers'}
    AUTHORS_EMAILS = {'coala-devel@googlegroups.com'}
    LICENSE = 'AGPL-3.0'
    CAN_FIX = {'Formatting'}

    def run(self,
            filename,
            file,
            language: str,
            dependency_results,
            use_spaces=True,
            indentation_width: int=SpacingHelper.DEFAULT_TAB_WIDTH,
            max_line_length: int=79,
            coalang_dir: str=None):
        """
        Runs the LineLengthBear and suggests alternate solutions where lines
        exceed the max_line_length.

        :param filename:
            Name of the file that needs to be checked.
        :param file:
            File that needs to be checked in the form of a list of strings.
        :param language:
            Language of the file it is running on.
        :param dependency_results:
            Results given by the AnnotationBear and the LineLengthBear.
        :param use_spaces:
            Inserts spaces instead of tabs for indentation.
        :param tab_width:
            No. of spaces to add before the newly created line.
        :param max_line_length:
            Maximum number of characters for a line, the newline character
            being excluded.
        :param dependency_results:
            Results given by the AnnotationBear.
        :param coalang_dir:
            Full path of external directory containing the coalang
            file for language.
        """
        encapsulators = dict(LanguageDefinition(
            language,
            coalang_dir=coalang_dir)['encapsulators'])

        # Get all lines which are over max_line_length
        line_length_bear = LineLengthBear(self.section, Queue())
        line_length_results = list(line_length_bear.execute(filename, file))

        affected_lines = [_range.start.line
                          for result in line_length_results
                          for _range in result.affected_code]
        annotation_dict = dependency_results[AnnotationBear.name][0].contents

        # Get all positions of encapsulators
        encaps_pos = sorted(tuple(_range
                                  for encapsulator in encapsulators
                                  for _range in get_specified_block_range(
                                      file,
                                      filename,
                                      encapsulator,
                                      encapsulators[encapsulator],
                                      annotation_dict)))
        print(encaps_pos)
        indent = indentation_width*' ' if use_spaces else '\t'

        suggested_positions = self._find_breakable_encapsulators(
            file,
            filename,
            affected_lines,
            max_line_length,
            encaps_pos)
        new_file = self._break_after_position(file,
                                              indent,
                                              suggested_positions)
        if new_file != list(file):
            wholediff = Diff.from_string_arrays(file, new_file)
            for diff in wholediff.split_diff():
                yield Result(
                    self,
                    'Following is a suggestion to break this long line',
                    severity=RESULT_SEVERITY.INFO,
                    affected_code=(diff.range(filename),),
                    diffs={filename: diff})

    def _break_after_position(self,
                              file,
                              indent,
                              suggested_positions):
        new_file = list(file)
        for position in suggested_positions:
            new_line = (indent +
                        file[position.line - 1][position.column:])
            new_file.insert(position.line, new_line)
            new_file[position.line - 1] = new_file[position.line - 1][
                :position.column] + '\n'
        return new_file

    def _find_breakable_encapsulators(self,
                                      file,
                                      filename,
                                      affected_lines,
                                      max_line_length,
                                      encapsulators):
        positions = []
        for line in affected_lines:
            last_encaps = None
            for encaps in encapsulators:
                if (encaps.start.line == line and
                        encaps.start.column < max_line_length):
                    last_encaps = encaps.start
            if last_encaps:
                positions.append(last_encaps)
        return tuple(positions)

    @staticmethod
    def get_dependencies():
        return [AnnotationBear]  # pragma: no cover
