import os
import platform
import stat

from queue import Queue

from bears.general.FileModeBear import FileModeBear
from coalib.testing.LocalBearTestHelper import LocalBearTestHelper
from coalib.results.Result import RESULT_SEVERITY, Result
from coalib.settings.Section import Section
from coalib.settings.Setting import Setting


FILE_PATH = os.path.join(os.path.dirname(__file__),
                         'filemode_test_files', 'test_file.txt')


class FileModeBearTest(LocalBearTestHelper):

    def setUp(self):
        self.section = Section('')
        self.uut = FileModeBear(self.section, Queue())

    def test_r_to_r_permissions(self):
        os.chmod(FILE_PATH, stat.S_IRUSR)
        self.section.append(Setting('filemode', 'r'))
        self.check_results(
            self.uut,
            [],
            [],
            filename=FILE_PATH,
            )

    def test_w_to_w_permissions(self):
        os.chmod(FILE_PATH, stat.S_IWUSR)
        self.section.append(Setting('filemode', 'w'))
        self.check_results(
            self.uut,
            [],
            [],
            filename=FILE_PATH,
            )
        os.chmod(FILE_PATH, stat.S_IRUSR)

    def test_x_to_x_permissions(self):
        os.chmod(FILE_PATH, stat.S_IXUSR)
        if platform.system() != 'Windows':
            self.section.append(Setting('filemode', 'x'))
            self.check_results(
                self.uut,
                [],
                [],
                filename=FILE_PATH,
                )
        os.chmod(FILE_PATH, stat.S_IRUSR)

    def test_rw_to_rw_permissions(self):
        os.chmod(FILE_PATH, stat.S_IRUSR | stat.S_IWUSR)
        self.section.append(Setting('filemode', 'rw'))
        self.check_results(
            self.uut,
            [],
            [],
            filename=FILE_PATH,
            )
        os.chmod(FILE_PATH, stat.S_IRUSR)

    def test_wx_to_wx_permissions(self):
        os.chmod(FILE_PATH, stat.S_IWUSR | stat.S_IXUSR)
        if platform.system() != 'Windows':
            self.section.append(Setting('filemode', 'wx'))
            self.check_results(
                self.uut,
                [],
                [],
                filename=FILE_PATH,
                )
        os.chmod(FILE_PATH, stat.S_IRUSR)

    def test_rx_to_rx_permissions(self):
        os.chmod(FILE_PATH, stat.S_IRUSR | stat.S_IXUSR)
        if platform.system() != 'Windows':
            self.section.append(Setting('filemode', 'rx'))
            self.check_results(
                self.uut,
                [],
                [],
                filename=FILE_PATH,
                )
        os.chmod(FILE_PATH, stat.S_IRUSR)

    def test_rwx_to_rwx_permissions(self):
        os.chmod(FILE_PATH, stat.S_IRUSR | stat.S_IWUSR | stat.S_IXUSR)
        if platform.system() != 'Windows':
            self.section.append(Setting('filemode', 'rwx'))
            self.check_results(
                self.uut,
                [],
                [],
                filename=FILE_PATH,
                settings={'filemode': 'rwx'})
        os.chmod(FILE_PATH, stat.S_IRUSR)

    def test_r_to_rwx_permissions(self):
        os.chmod(FILE_PATH, stat.S_IRUSR)
        filemode = '-r--------'
        if platform.system() == 'Windows':
            filemode = '-r--r--r--'
        message = ('The file permissions are not adequate. The '
                   'permissions are set to {}'.format(filemode))
        self.section.append(Setting('filemode', 'rwx'))
        self.check_results(
            self.uut,
            [],
            [Result.from_values('FileModeBear',
                                message,
                                file=FILE_PATH,
                                severity=RESULT_SEVERITY.INFO)],
            filename=FILE_PATH,
            settings={'filemode': 'rwx'})

    def test_w_to_rwx_permissions(self):
        os.chmod(FILE_PATH, stat.S_IWUSR)
        filemode = '--w-------'
        if platform.system() == 'Windows':
            filemode = '-rw-rw-rw-'
        message = ('The file permissions are not adequate. The '
                   'permissions are set to {}'.format(filemode))
        self.section.append(Setting('filemode', 'rwx'))
        self.check_results(
            self.uut,
            [],
            [Result.from_values('FileModeBear',
                                message,
                                file=FILE_PATH,
                                severity=RESULT_SEVERITY.INFO)],
            filename=FILE_PATH,
            )
        os.chmod(FILE_PATH, stat.S_IRUSR)

    def test_x_to_rwx_permissions(self):
        os.chmod(FILE_PATH, stat.S_IXUSR)
        filemode = '---x------'
        if platform.system() != 'Windows':
            message = ('The file permissions are not adequate. The '
                       'permissions are set to {}'.format(filemode))
            self.section.append(Setting('filemode', 'rwx'))
            self.check_results(
                self.uut,
                [],
                [Result.from_values('FileModeBear',
                                    message,
                                    file=FILE_PATH,
                                    severity=RESULT_SEVERITY.INFO)],
                filename=FILE_PATH,
                )
        os.chmod(FILE_PATH, stat.S_IRUSR)

    def test_rx_to_rwx_permissions(self):
        os.chmod(FILE_PATH, stat.S_IRUSR | stat.S_IXUSR)
        filemode = '-r-x------'
        if platform.system() != 'Windows':
            message = ('The file permissions are not adequate. The '
                       'permissions are set to {}'.format(filemode))
            self.section.append(Setting('filemode', 'rwx'))
            self.check_results(
                self.uut,
                [],
                [Result.from_values('FileModeBear',
                                    message,
                                    file=FILE_PATH,
                                    severity=RESULT_SEVERITY.INFO)],
                filename=FILE_PATH,
                )
        os.chmod(FILE_PATH, stat.S_IRUSR)

    def test_wx_to_rwx_permissions(self):
        os.chmod(FILE_PATH, stat.S_IWUSR | stat.S_IXUSR)
        filemode = '--wx------'
        if platform.system() != 'Windows':
            message = ('The file permissions are not adequate. The '
                       'permissions are set to {}'.format(filemode))
            self.section.append(Setting('filemode', 'rwx'))
            self.check_results(
                self.uut,
                [],
                [Result.from_values('FileModeBear',
                                    message,
                                    file=FILE_PATH,
                                    severity=RESULT_SEVERITY.INFO)],
                filename=FILE_PATH,
                )
        os.chmod(FILE_PATH, stat.S_IRUSR)

    def test_rw_to_rwx_permissions(self):
        os.chmod(FILE_PATH, stat.S_IRUSR | stat.S_IWUSR)
        filemode = '-rw-------'
        if platform.system() == 'Windows':
            filemode = '-rw-rw-rw-'
        message = ('The file permissions are not adequate. The '
                   'permissions are set to {}'.format(filemode))
        self.section.append(Setting('filemode', 'rwx'))
        self.check_results(
            self.uut,
            [],
            [Result.from_values('FileModeBear',
                                message,
                                file=FILE_PATH,
                                severity=RESULT_SEVERITY.INFO)],
            filename=FILE_PATH,
            )
        os.chmod(FILE_PATH, stat.S_IRUSR)

    def test_invalid_char_in_filemode(self):
        self.section.append(Setting('filemode', 'rwmc'))
        error_msg = ('ValueError: Unable to recognize '
                     'character `mc` in filemode `rwmc`.')
        with self.assertRaisesRegex(AssertionError, error_msg):
            self.check_validity(self.uut, [], filename=FILE_PATH)
