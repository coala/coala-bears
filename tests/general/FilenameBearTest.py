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
                         'Invalid file-naming-convention provided: INVALID')
        self.assertEqual(log.log_level, LOG_LEVEL.ERROR)

    def test_snake_case(self):
        self.check_validity(self.uut, [''], filename='/Home/xyz/x_y.py')
        self.check_validity(self.uut, [''], filename='XYZ/__init__.py')

        self.section['file_naming_convention'] = 'snake'
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
        self.section['file_naming_convention'] = 'pascal'
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
        self.check_validity(self.uut, [''], filename='/LICENSE')

        self.section['ignore_uppercase_filenames'] = 'nope'

        self.check_validity(self.uut, [''], filename='/LICENSE', valid=False)

    def test_upper_case(self):
        self.section['file_naming_convention'] = 'Snake'
        self.check_validity(self.uut, [''], filename='/Home/xyz/x_y.py')
        self.check_validity(self.uut, [''], filename='XYZ/__init__.py')
        self.check_validity(self.uut, [''], filename='/a/pyCase', valid=False)
