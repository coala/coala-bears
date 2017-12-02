import json
from collections import OrderedDict
from re import match

from coala_utils.param_conversion import negate
from coalib.bearlib import deprecate_settings
from coalib.bearlib.spacing.SpacingHelper import SpacingHelper
from coalib.bears.LocalBear import LocalBear
from coalib.misc.Compatibility import JSONDecodeError
from coalib.results.Diff import Diff
from coalib.results.Result import Result


class FloatWrapper():
    """
    Wrapper for floats, which allows you to keep float representation
    from initial file.
    """

    def __init__(self, s):
        self.s = s

    def __repr__(self):
        return self.s

    def get_s(self):
        return self.s


def create_float_wrapper(obj):
    """
    Wraps obj by FloatWrapper.

    :param obj:
        Float from initial json file.
    """
    return FloatWrapper(obj)


def default_floats(obj):
    """
    Handler for FloatWrapper objects, which return float from the initial file.

    :param obj:
        FloatWrapper object.
    """
    if isinstance(obj, FloatWrapper):
        return obj.get_s()


class JSONFormatBear(LocalBear):

    LANGUAGES = {'JSON'}
    AUTHORS = {'The coala developers'}
    AUTHORS_EMAILS = {'coala-devel@googlegroups.com'}
    ASCIINEMA_URL = 'https://asciinema.org/a/6vxc7076tnf996zanpdfwojwu'
    LICENSE = 'AGPL-3.0'
    CAN_DETECT = {'Formatting'}

    @deprecate_settings(indent_size='tab_width',
                        escape_unicode=('keep_unicode', negate))
    def run(self, filename, file,
            json_sort: bool=False,
            indent_size: int=SpacingHelper.DEFAULT_TAB_WIDTH,
            escape_unicode: bool=True):
        """
        Raises issues for any deviations from the pretty-printed JSON.

        :param json_sort:      Whether or not keys should be sorted.
        :param indent_size:    Number of spaces per indentation level.
        :param escape_unicode: Whether or not to escape unicode values using
                               ASCII.
        """
        # Output a meaningful message if empty file given as input
        if len(file) == 0:
            yield Result.from_values(self,
                                     'This file is empty.',
                                     file=filename)
            return

        try:
            json_content = json.loads(''.join(file),
                                      object_pairs_hook=OrderedDict,
                                      parse_float=create_float_wrapper)
        except JSONDecodeError as err:
            err_content = match(r'(.*): line (\d+) column (\d+)', str(err))
            yield Result.from_values(
                self,
                'This file does not contain parsable JSON. ' +
                err_content.group(1) + '.',
                file=filename,
                line=int(err_content.group(2)),
                column=int(err_content.group(3)))
            return

        corrected = json.dumps(json_content,
                               sort_keys=json_sort,
                               indent=indent_size,
                               ensure_ascii=escape_unicode,
                               default=default_floats
                               ).splitlines(True)
        # Because of a bug in several python versions we have to correct
        # whitespace here.
        corrected = tuple(line.rstrip(' \n') + '\n' for line in corrected)
        diff = Diff.from_string_arrays(file, corrected)

        if len(diff) > 0:
            yield Result(self,
                         'This file can be reformatted by sorting keys and '
                         'following indentation.',
                         affected_code=tuple(d.range(filename)
                                             for d in diff.split_diff()),
                         diffs={filename: diff})
