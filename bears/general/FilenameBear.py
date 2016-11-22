import os.path

from coalib.bears.LocalBear import LocalBear
from coalib.results.Diff import Diff
from coalib.results.Result import Result
from coalib.bearlib.naming_conventions import (
    to_camelcase, to_pascalcase, to_snakecase, to_spacecase)


class FilenameBear(LocalBear):
    LANGUAGES = {'All'}
    AUTHORS = {'The coala developers'}
    AUTHORS_EMAILS = {'coala-devel@googlegroups.com'}
    LICENSE = 'AGPL-3.0'

    _naming_convention = {'camel': to_camelcase,
                          'pascal': to_pascalcase,
                          'snake': to_snakecase,
                          'space': to_spacecase}

    def run(self, filename, file,
            file_naming_convention: str='snake',
            ignore_uppercase_filenames: bool=True):
        """
        Checks whether the filename follows a certain naming-convention.

        :param file_naming_convention:
            The naming-convention. Supported values are:
            - ``camel`` (``thisIsCamelCase``)
            - ``pascal`` (``ThisIsPascalCase``)
            - ``snake`` (``this_is_snake_case``)
            - ``space`` (``This Is Space Case``)
        :param ignore_uppercase_filenames:
            Whether or not to ignore fully uppercase filenames completely,
            e.g. COPYING, LICENSE etc.
        """
        head, tail = os.path.split(filename)
        filename_without_extension, extension = os.path.splitext(tail)
        try:
            new_name = self._naming_convention[file_naming_convention](
                filename_without_extension)
        except KeyError:
            self.err('Invalid file-naming-convention provided: ' +
                     file_naming_convention)
            return

        if ignore_uppercase_filenames and filename_without_extension.isupper():
            return

        if new_name != filename_without_extension:
            diff = Diff(file, rename=os.path.join(head, new_name + extension))

            yield Result(
                self,
                'Filename does not follow {} naming-convention.'.format(
                    file_naming_convention),
                diff.affected_code(filename),
                diffs={filename: diff})
