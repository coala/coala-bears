import os
import stat

from coalib.bears.LocalBear import LocalBear
from coalib.results.Result import Result
from coalib.results.RESULT_SEVERITY import RESULT_SEVERITY


class FileModeBear(LocalBear):
    LANGUAGES = {'All'}
    AUTHORS = {'The coala developers'}
    AUTHORS_EMAILS = {'coala-devel@googlegroups.com'}
    LICENSE = 'AGPL-3.0'

    def run(self,
            filename,
            file,
            filemode: str,
            ):
        """
        The bear will check if the file has required permissions provided by
        the user.

        :param filemode:
            Filemode to check, e.g. `rw`, `rwx`, etc.
        """
        st = os.stat(filename)
        permissions = {'r': stat.S_IRUSR,
                       'w': stat.S_IWUSR,
                       'x': stat.S_IXUSR,
                       }

        invalid_chars = [ch for ch in filemode if ch not in permissions]

        if invalid_chars:
            raise ValueError('Unable to recognize character `{}` in filemode '
                             '`{}`.'.format(''.join(invalid_chars), filemode))

        mode = st.st_mode
        for char in filemode:
            if not mode & permissions[char]:
                message = ('The file permissions are not adequate. '
                           'The permissions are set to {}'
                           .format(stat.filemode(mode)))
                return [Result.from_values(origin=self,
                                           message=message,
                                           severity=RESULT_SEVERITY.INFO,
                                           file=filename)]
