import sys
from queue import Queue
from unittest.case import skipIf

from bears.python.YapfBear import YapfBear
from coalib.testing.LocalBearTestHelper import LocalBearTestHelper
from coalib.testing.BearTestHelper import generate_skip_decorator
from coalib.settings.Section import Section
from coalib.settings.Setting import Setting


@generate_skip_decorator(YapfBear)
class YapfBearTest(LocalBearTestHelper):

    def setUp(self):
        self.section = Section('name')
        self.uut = YapfBear(self.section, Queue())

    def test_valid(self):
        self.check_validity(self.uut,
                            ["x = {'a': 37, 'b': 42, 'c': 927}\n", '\n',
                             "y = 'hello ' 'world'\n"])
        self.check_invalidity(self.uut,
                              ["x = {  'a':37,'b':42,\n", "'c':927}\n", '\n',
                               "y = 'hello ''world'\n"])

    def test_eof_handling(self):
        self.check_validity(self.uut, [])
        self.check_validity(self.uut, [''])
        self.check_validity(self.uut, ['a = 2\n'])
        self.check_validity(self.uut, ['a = 2'])
        self.check_validity(self.uut, ['\n'])

    def test_invalid_python(self):
        results = self.check_invalidity(
            self.uut, ['def a():', ' b=1', '  bad indent'])
        self.assertEqual(len(results), 1, str(results))
        self.assertIn('unexpected indent', results[0].message)

        results = self.check_invalidity(
            self.uut, ['def a():', '    b=1', '\ttab error'])
        self.assertEqual(len(results), 1, str(results))
        self.assertIn('inconsistent use of tabs and spaces in indentation',
                      results[0].message)

        results = self.check_invalidity(
            self.uut, ['def a(:', '    b=1', '\ttab error'])
        self.assertEqual(len(results), 1, str(results))
        self.assertIn('syntax errors', results[0].message)

    def test_valid_python_2(self):
        self.check_validity(self.uut, ['print 1\n'])

    @skipIf(sys.version_info < (3, 5), "ast before 3.5 can't parse async def")
    def test_valid_async(self):
        self.check_validity(self.uut,
                            ['async def x():\n', '    pass\n'])

    def test_blank_line_after_nested_class_or_def(self):
        self.section.append(Setting('blank_line_before_nested_class_or_def',
                                    True))
        self.check_validity(self.uut,
                            ['class foo(object):\n', '\n',
                             '    def f(self):\n',
                             '        return 37 * -+2\n'])
        self.check_invalidity(self.uut,
                              ['class foo(object):\n', '    def f(self):\n',
                               '        return 37 * -+2\n'])

    def test_allow_multiline_lambdas(self):
        import pkg_resources
        YAPF_VERSION = tuple(
            map(int, pkg_resources.get_distribution('yapf').version.split('.')))
        self.section.append(Setting('allow_multiline_lambdas', True))

        if YAPF_VERSION > (0, 21, 0):
            self.check_validity(self.uut,
                                ['func(\n',
                                 '    a, lambda xxxxxxxxxxxxxxxxxxxxxxxxxxxxx'
                                 'xxxxxxxxxxxxxxxxxxxxxx:\n',
                                 '    xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'
                                 'xxxxxxxxxxxx + 222222222)'])
        else:
            self.check_validity(self.uut,
                                ['func(a, lambda xxxxxxxxxxxxxxxxxxxxxxxxxxxx'
                                 'xxxxxxxxxxxxxxxxxxxxxxx:\n',
                                 '     xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'
                                 'xxxxxxxxxxxxx + 222222222)\n'
                                 ])

        self.section.append(Setting('allow_multiline_lambdas', False))

        if YAPF_VERSION < (0, 26, 0):
            self.check_validity(self.uut,
                                ['func(\n',
                                 '    a,\n',
                                 '    lambda xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'
                                 'xxxxxxxxxxxxxxxxxxx: xxxxxxxxxxxxxxxxxxxxxx'
                                 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxx + 222222222\n',
                                 ')\n'])
        else:
            self.check_validity(self.uut,
                                ['func(\n',
                                 '    a, lambda xxxxxxxxxxxxxxxxxxxxxxxxxxxxx'
                                 'xxxxxxxxxxxxxxxxxxxxxx:\n', '    xxxxxxxxxx'
                                 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx +'
                                 ' 222222222)\n'])
