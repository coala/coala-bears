from queue import Queue

from bears.general.FilenameBear import FilenameBear
from coalib.testing.LocalBearTestHelper import LocalBearTestHelper
from coalib.results.Result import RESULT_SEVERITY, Result
from coalib.output.printers.LOG_LEVEL import LOG_LEVEL
from coalib.settings.Section import Section


class FilenameBearTest(LocalBearTestHelper):

    def setUp(self):
        self.section = Section('test section')
        self.uut = FilenameBear(self.section, Queue())

    def test_invalid_naming_convention(self):
        self.section['file_naming_convention'] = 'INVALID'
        self.uut.execute('filename', [])

        # Automatic bear messages we want to ignore.
        self.uut.message_queue.get(timeout=1)

        log = self.uut.message_queue.get(timeout=1)
        self.assertEqual(log.message,
                         'Invalid file-naming-convention provided: invalid')
        self.assertEqual(log.log_level, LOG_LEVEL.ERROR)

    def test_snake_case(self):
        self.section['file_naming_convention'] = 'snake'
        self.check_validity(self.uut, [''], filename='/Home/xyz/x_y.py')
        self.check_validity(self.uut, [''], filename='XYZ/__init__.py')
        self.check_invalidity(self.uut, [''], filename='/a/camCase')

    def test_camel_case(self):
        self.section['file_naming_convention'] = 'camel'
        self.check_invalidity(self.uut, [''], filename='/Home/xyz/x_y.py')
        self.check_validity(self.uut, [''], filename='XYZ/__init__.py')
        self.check_validity(self.uut, [''], filename='/a/camCase')

    def test_kebab_case(self):
        self.section['file_naming_convention'] = 'kebab'
        self.check_invalidity(self.uut, [''], filename='/Home/xyz/x_y.py')
        self.check_validity(self.uut, [''], filename='XYZ/init.py')
        self.check_validity(self.uut, [''], filename='/a/kebab-case')

    def test_pascal_case(self):
        for convention in ('Pascal', 'pascal', 'PASCAL'):
            self.section['file_naming_convention'] = convention
            self.check_invalidity(self.uut, [''], filename='/Home/xyz/x_y.py')
            self.check_validity(self.uut, [''], filename='XYZ/__Init__.py')
            self.check_validity(self.uut, [''], filename='/a/PascalCase')

    def test_space_case(self):
        self.section['file_naming_convention'] = 'space'
        self.check_invalidity(self.uut, [''], filename='/Home/xyz/x_y.py')
        self.check_invalidity(self.uut, [''], filename='XYZ/__Init__.py')
        self.check_invalidity(self.uut, [''], filename='/a/camCase')
        self.check_validity(self.uut, [''], filename='/a/Space Case')

    def test_ignore_upper(self):
        self.section['file_naming_convention'] = 'auto'
        self.check_validity(self.uut, [''], filename='/LICENSE')

        self.section['ignore_uppercase_filenames'] = 'nope'

        self.check_invalidity(self.uut, [''], filename='/LICENSE')

    def test_default_naming_java(self):
        self.section['file_naming_convention'] = 'auto'
        self.check_invalidity(self.uut, [''], filename='/Home/xyz/x_y.java')
        self.check_invalidity(self.uut, [''], filename='/Home/xyz/x-y.java')
        self.check_invalidity(self.uut, [''], filename='/Home/xyz/x y.java')
        self.check_validity(self.uut, [''], filename='/Home/xyz/XY.java')

    def test_default_naming_javascript(self):
        self.section['file_naming_convention'] = 'auto'
        self.check_invalidity(self.uut, [''], filename='/Home/xyz/x_y.js')
        self.check_invalidity(self.uut, [''], filename='/Home/xyz/x y.js')
        self.check_validity(self.uut, [''], filename='/Home/xyz/XY.js')
        self.check_validity(self.uut, [''], filename='/Home/xyz/x-y.js')

    def test_default_file_naming_python(self):
        self.section['file_naming_convention'] = 'auto'
        self.check_validity(self.uut, [''], filename='/Home/xyz/x_y.py')
        self.check_validity(self.uut, [''], filename='XYZ/__init__.py')
        self.check_invalidity(self.uut, [''], filename='/a/x y.py')

    def test_none_file_naming_convention_warning(self):
        self.uut.execute('filename', [])

        # Automatic bear messages we want to ignore.
        self.uut.message_queue.get()

        log = self.uut.message_queue.get(timeout=1)
        self.assertEqual(log.message,
                         'Please specify a file naming convention explicitly'
                         ' or use "auto".')
        self.check_validity(self.uut, [''], filename='/Home/xyz/x_y.py')

    def test_auto_file_naming_convention_warning(self):
        self.section['file_naming_convention'] = 'auto'
        self.uut.execute('filename.xyz', [])

        # Automatic bear messages we want to ignore.
        self.uut.message_queue.get()

        log = self.uut.message_queue.get(timeout=1)
        self.assertEqual(log.message,
                         'The file naming convention could not be guessed. '
                         'Using the default "snake" naming convention.')

    def test_file_prefix(self):
        self.section['filename_prefix'] = 'pre'
        self.check_invalidity(
            self.uut, [''], filename='filename.xyz')
        self.check_validity(
            self.uut, [''], filename='prefilename.xyz')
        self.check_results(
            self.uut,
            [''],
            [Result.from_values('FilenameBear',
                                "Filename does not use the prefix 'pre'.",
                                severity=RESULT_SEVERITY.NORMAL,
                                file='filename.xyz')],
            filename='filename.xyz')

    def test_file_suffix(self):
        self.section['filename_suffix'] = 'fix'
        self.check_invalidity(
            self.uut, [''], filename='filename.xyz')
        self.check_validity(
            self.uut, [''], filename='filenamesuffix.xyz')
        self.check_results(
            self.uut,
            [''],
            [Result.from_values('FilenameBear',
                                "Filename does not use the suffix 'fix'.",
                                severity=RESULT_SEVERITY.NORMAL,
                                file='filename.xyz')],
            filename='filename.xyz')

    def test_file_prefix_suffix(self):
        self.section['filename_prefix'] = 'pre'
        self.section['filename_suffix'] = 'fix'
        self.check_results(
            self.uut,
            [''],
            [Result.from_values('FilenameBear',
                                "- Filename does not use the prefix 'pre'.\n"
                                "- Filename does not use the suffix 'fix'.",
                                severity=RESULT_SEVERITY.NORMAL,
                                file='filename.xyz')],
            filename='filename.xyz')

    def test_file_with_too_long_filename(self):
        msg = 'Filename is too long ({} > {}).'
        filename_test1 = '_filenamewhichistoolong'*15 + '.xyz'
        filename_test2 = '_filenamewhichistoolong'*10 + '.xyz'
        filename_test3 = '_validfilenamelength'*13
        max_filename_length = 260
        self.check_invalidity(
            self.uut, [''], filename=filename_test1)
        self.check_validity(
            self.uut, [''], filename=filename_test2)
        self.check_validity(
            self.uut, [''], filename=filename_test3)
        self.check_results(
            self.uut,
            [''],
            [Result.from_values('FilenameBear',
                                msg.format(len(filename_test1),
                                           max_filename_length),
                                severity=RESULT_SEVERITY.NORMAL,
                                file=filename_test1)],
            filename=filename_test1)

    def test_message_too_long_file_with_other_errors(self):
        self.section['filename_prefix'] = 'pre'
        filename_test1 = '_filenamewhichistoolong'*15 + '.xyz'
        max_filename_length = 260
        msg = ("- Filename does not use the prefix 'pre'.\n"
               '- Filename is too long ({} > {}).'
               )
        self.check_results(
            self.uut,
            [''],
            [Result.from_values('FilenameBear',
                                msg.format(len(filename_test1),
                                           max_filename_length),
                                severity=RESULT_SEVERITY.NORMAL,
                                file=filename_test1)],
            filename=filename_test1)
