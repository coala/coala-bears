import os.path

from coalib.bears.LocalBear import LocalBear
from coalib.results.Diff import Diff
from coalib.results.Result import Result
from coalib.bearlib.naming_conventions import (
    to_camelcase, to_kebabcase, to_pascalcase, to_snakecase, to_spacecase)


class FilenameBear(LocalBear):
    LANGUAGES = {'All'}
    AUTHORS = {'The coala developers'}
    AUTHORS_EMAILS = {'coala-devel@googlegroups.com'}
    LICENSE = 'AGPL-3.0'

    _naming_convention = {'camel': to_camelcase,
                          'kebab': to_kebabcase,
                          'pascal': to_pascalcase,
                          'snake': to_snakecase,
                          'space': to_spacecase}

    _language_naming_convention = {
                                   '.java': 'pascal',
                                   '.js': 'kebab',
                                   '.py': 'snake',
                                  }

    def run(self, filename, file,
            file_naming_convention: str=None,
            ignore_uppercase_filenames: bool=True):
        """
        Checks whether the filename follows a certain naming-convention.

        :param file_naming_convention:
            The naming-convention. Supported values are:
            - ``auto`` to guess the correct convention. Defaults to ``snake``
            if the correct convention cannot be guessed.
            - ``camel`` (``thisIsCamelCase``)
            - ``kebab`` (``this-is-kebab-case``)
            - ``pascal`` (``ThisIsPascalCase``)
            - ``snake`` (``this_is_snake_case``)
            - ``space`` (``This Is Space Case``)
        :param ignore_uppercase_filenames:
            Whether or not to ignore fully uppercase filenames completely,
            e.g. COPYING, LICENSE etc.
        """
        head, tail = os.path.split(filename)
        filename_without_extension, extension = os.path.splitext(tail)

        if file_naming_convention is None:
            self.warn('Please specify a file naming convention explicitly'
                      ' or use "auto".')
            file_naming_convention = 'auto'
        else:
            file_naming_convention = file_naming_convention.lower()

        if file_naming_convention == 'auto':
            if extension in self._language_naming_convention:
                file_naming_convention = self._language_naming_convention[
                    extension]
            else:
                self.warn('The file naming convention could not be guessed. '
                          'Using the default "snake" naming convention.')
                file_naming_convention = 'snake'

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
