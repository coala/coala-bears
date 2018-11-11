from queue import Queue

from bears.python.PyStringConcatBear import PyStringConcatBear
from coalib.testing.LocalBearTestHelper import LocalBearTestHelper
from coalib.results.Result import Result
from coalib.settings.Section import Section


valid_string = """
string = 'foo'
         'bar'
"""

concat_non_string = """
list = [] +
       []
"""

invalid_single_quote_string = """
string = 'foo' +
         'bar'
"""

invalid_double_quote_string = """
string = "foo" +
         "bar"
"""

invalid_acute_string = """
string = `foo` +
         `bar`
"""


class PyStringConcatBearTest(LocalBearTestHelper):

    def setUp(self):
        self.uut = PyStringConcatBear(Section('name'), Queue())

    def test_valid(self):
        self.check_validity(self.uut, valid_string.splitlines())

    def test_non_string(self):
        self.check_validity(self.uut, concat_non_string.splitlines())

    def test_single_quote_string_invalid(self):
        self.check_results(
            self.uut,
            invalid_single_quote_string.splitlines(),
            [Result.from_values(
                'PyStringConcatBear',
                'Use of explicit string concatenation with `+` '
                'should be avoided.',
                line=2, column=16, end_line=3, end_column=17, file='default')
             ],
            filename='default'
            )

    def test_double_quote_string_invalid(self):
        self.check_results(
            self.uut,
            invalid_double_quote_string.splitlines(),
            [Result.from_values(
                'PyStringConcatBear',
                'Use of explicit string concatenation with `+` '
                'should be avoided.',
                line=2, column=16, end_line=3, end_column=17, file='default')
             ],
            filename='default'
            )

    def test_acute_string_invalid(self):
        self.check_results(
            self.uut,
            invalid_acute_string.splitlines(),
            [Result.from_values(
                'PyStringConcatBear',
                'Use of explicit string concatenation with `+` '
                'should be avoided.',
                line=2, column=16, end_line=3, end_column=17, file='default')
             ],
            filename='default'
            )
