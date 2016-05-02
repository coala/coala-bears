import json
from collections import OrderedDict

from coalib.bearlib.spacing.SpacingHelper import SpacingHelper
from coalib.bears.LocalBear import LocalBear
from coalib.results.Diff import Diff
from coalib.results.Result import Result


class JSONFormatBear(LocalBear):
    try:
        DecodeError = json.decoder.JSONDecodeError
    except AttributeError:
        DecodeError = ValueError

    LANGUAGES = "JSON"

    def run(self, filename, file,
            json_sort: bool=False,
            tab_width: int=SpacingHelper.DEFAULT_TAB_WIDTH,
            keep_unicode: bool=False):
        """
        Raises issues for any deviations from the pretty-printed JSON.

        :param json_sort:    Whether or not keys should be sorted.
        :param tab_width:    Number of spaces to indent.
        :param keep_unicode: Wether or not to escape unicode values using ASCII.
        """
        try:
            json_content = json.loads(''.join(file),
                                      object_pairs_hook=OrderedDict)
        except self.DecodeError as err:
            return [Result.from_values(
                self,
                "This file does not contain parsable JSON. " + repr(str(err)),
                file=filename)]

        corrected = json.dumps(json_content,
                               sort_keys=json_sort,
                               indent=tab_width,
                               ensure_ascii=not keep_unicode).splitlines(True)
        # Because of a bug in several python versions we have to correct
        # whitespace here.
        corrected = [line.rstrip(" \n") + "\n" for line in corrected]

        diffs = Diff.from_string_arrays(file, corrected).split_diff()

        for diff in diffs:
            yield Result(self,
                         "This file can be reformatted by sorting keys and "
                         "following indentation.",
                         affected_code=(diff.range(filename),),
                         diffs={filename: diff})
