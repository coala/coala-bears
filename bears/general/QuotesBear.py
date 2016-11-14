from coalib.bears.LocalBear import LocalBear
from bears.general.AnnotationBear import AnnotationBear
from coalib.results.Diff import Diff
from coalib.results.HiddenResult import HiddenResult
from coalib.results.Result import Result


class QuotesBear(LocalBear):

    BEAR_DEPS = {AnnotationBear}
    AUTHORS = {'The coala developers'}
    AUTHORS_EMAILS = {'coala-devel@googlegroups.com'}
    LICENSE = 'AGPL-3.0'
    CAN_DETECT = {'Formatting'}

    def correct_single_line_str(self, filename, file, sourcerange,
                                preferred_quotation):
        """
        Corrects a given single line string assuming it does not use the
        preferred quotation. If the preferred quotation mark is used inside the
        string, no correction will be made.

        This function will yield one or no Result objects.

        :param filename:
            The filename of the file to correct the line in.
        :param file:
            The file contents as list of lines.
        :param sourcerange:
            The sourcerange indicating where to find the string.
        :param preferred_quotation:
            ``'`` or ``"`` respectively.
        """
        str_contents = file[sourcerange.start.line - 1][
                       sourcerange.start.column:sourcerange.end.column-1]

        if preferred_quotation in str_contents:
            return

        before = file[sourcerange.start.line - 1][:sourcerange.start.column-1]
        after = file[sourcerange.end.line - 1][sourcerange.end.column:]

        replacement = (before + preferred_quotation + str_contents +
                       preferred_quotation + after)

        diff = Diff(file)
        diff.change_line(sourcerange.start.line,
                         file[sourcerange.start.line - 1],
                         replacement)
        yield Result(self, 'You do not use the preferred quotation marks.',
                     diff.affected_code(filename), diffs={filename: diff})

    def run(self, filename, file, dependency_results,
            preferred_quotation: str='"'):
        """
        Checks and corrects your quotation style.

        For all single line strings, this bear will correct the quotation to
        your preferred quotation style if that kind of quote is not included
        within the string. Multi line strings are not supported.

        :param preferred_quotation: Your preferred quotation character, e.g.
                                    ``"`` or ``'``.
        """
        if not isinstance(dependency_results[AnnotationBear.name][0],
                          HiddenResult):
            return
        if isinstance(dependency_results[AnnotationBear.name][0].contents,
                      str):
            self.err(dependency_results[AnnotationBear.name][0].contents)
            return

        ranges = dependency_results[AnnotationBear.name][0].contents['strings']

        for string_range in ranges:
            if (file[string_range.start.line-1][string_range.start.column-1] ==
                    preferred_quotation):
                continue

            if string_range.start.line == string_range.end.line:
                yield from self.correct_single_line_str(
                    filename, file, string_range, preferred_quotation)
