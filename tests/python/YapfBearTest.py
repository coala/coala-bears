from queue import Queue

from bears.python.YapfBear import YapfBear
from tests.LocalBearTestHelper import LocalBearTestHelper
from tests.BearTestHelper import generate_skip_decorator
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
                             "y = 'hello ' 'world'\n"], valid=True)
        self.check_validity(self.uut,
                            ["x = {  'a':37,'b':42,\n", "'c':927}\n", '\n',
                             "y = 'hello ''world'\n"], valid=False)

    def test_blank_line_after_nested_class_or_def(self):
        self.section.append(Setting('blank_line_before_nested_class_or_def',
                                    True))
        self.check_validity(self.uut,
                            ["class foo(object):\n", "\n", "    def f(self):\n",
                             "        return 37 * -+2\n"],
                            valid=True)
        self.check_validity(self.uut,
                            ["class foo(object):\n", "    def f(self):\n",
                             "        return 37 * -+2\n"],
                            valid=False)

    def test_allow_multiline_lambdas(self):
        self.section.append(Setting('allow_multiline_lambdas', True))
        self.check_validity(self.uut,
                            ['func(a, lambda xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'
                             'xxxxxxxxxxxxxxxxx:\n', '     xxxxxxxxxxxxxxxxxxxx'
                             'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx + 222222222)\n'],
                            valid=True)
        self.section.append(Setting('allow_multiline_lambdas', False))
        self.check_validity(self.uut,
                            ['func(\n',
                             '    a,\n',
                             '    lambda xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'
                             'xxxxxxxxxxxxx: xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'
                             'xxxxxxxxxxxxxxxxx + 222222222)\n'],
                            valid=True)
