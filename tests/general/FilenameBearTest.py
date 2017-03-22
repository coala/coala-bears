from queue import Queue

from bears.general.FilenameBear import FilenameBear
from coalib.testing.LocalBearTestHelper import LocalBearTestHelper
from coalib.output.printers.LOG_LEVEL import LOG_LEVEL
from coalib.settings.Section import Section


class SpaceConsistencyBearTest(LocalBearTestHelper):

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
        self.check_validity(self.uut, [''], filename='/a/camCase', valid=False)

    def test_camel_case(self):
        self.section['file_naming_convention'] = 'camel'
        self.check_validity(self.uut, [''], filename='/Home/xyz/x_y.py',
                            valid=False)
        self.check_validity(self.uut, [''], filename='XYZ/__init__.py')
        self.check_validity(self.uut, [''], filename='/a/camCase')

    def test_kebab_case(self):
        self.section['file_naming_convention'] = 'kebab'
        self.check_validity(self.uut, [''], filename='/Home/xyz/x_y.py',
                            valid=False)
        self.check_validity(self.uut, [''], filename='XYZ/init.py')
        self.check_validity(self.uut, [''], filename='/a/kebab-case')

    def test_pascal_case(self):
        for convention in ('Pascal', 'pascal', 'PASCAL'):
            self.section['file_naming_convention'] = convention
            self.check_validity(self.uut, [''], filename='/Home/xyz/x_y.py',
                                valid=False)
            self.check_validity(self.uut, [''], filename='XYZ/__Init__.py')
            self.check_validity(self.uut, [''], filename='/a/PascalCase')

    def test_space_case(self):
        self.section['file_naming_convention'] = 'space'
        self.check_validity(self.uut, [''], filename='/Home/xyz/x_y.py',
                            valid=False)
        self.check_validity(self.uut, [''], filename='XYZ/__Init__.py',
                            valid=False)
        self.check_validity(self.uut, [''], filename='/a/camCase',
                            valid=False)
        self.check_validity(self.uut, [''], filename='/a/Space Case')

    def test_ignore_upper(self):
        self.section['file_naming_convention'] = 'auto'
        self.check_validity(self.uut, [''], filename='/LICENSE')

        self.section['ignore_uppercase_filenames'] = 'nope'

        self.check_validity(self.uut, [''], filename='/LICENSE', valid=False)

    def test_default_naming_java(self):
        self.section['file_naming_convention'] = 'auto'
        self.check_validity(self.uut, [''], filename='/Home/xyz/x_y.java',
                            valid=False)
        self.check_validity(self.uut, [''], filename='/Home/xyz/x-y.java',
                            valid=False)
        self.check_validity(self.uut, [''], filename='/Home/xyz/x y.java',
                            valid=False)
        self.check_validity(self.uut, [''], filename='/Home/xyz/XY.java')

    def test_default_naming_javascript(self):
        self.section['file_naming_convention'] = 'auto'
        self.check_validity(self.uut, [''], filename='/Home/xyz/x_y.js',
                            valid=False)
        self.check_validity(self.uut, [''], filename='/Home/xyz/x y.js',
                            valid=False)
        self.check_validity(self.uut, [''], filename='/Home/xyz/XY.js')
        self.check_validity(self.uut, [''], filename='/Home/xyz/x-y.js')

    def test_default_file_naming_python(self):
        self.section['file_naming_convention'] = 'auto'
        self.check_validity(self.uut, [''], filename='/Home/xyz/x_y.py')
        self.check_validity(self.uut, [''], filename='XYZ/__init__.py')
        self.check_validity(self.uut, [''], filename='/a/x y.py', valid=False)

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
