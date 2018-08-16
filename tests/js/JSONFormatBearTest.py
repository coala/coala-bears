from queue import Queue

from bears.js.JSONFormatBear import JSONFormatBear
from coalib.testing.LocalBearTestHelper import (verify_local_bear,
                                                LocalBearTestHelper)
from coalib.results.Result import Result
from coalib.settings.Section import Section

test_file = """{
}"""


test_file1 = """{
    "a": 5,
    "b": 5
}"""


test_file2 = """{
    "b": 5,
    "a": 5
}"""


test_file3 = """{
   "b": 5,
   "a": 5
}"""


unicode_file = """{
    "⌘": 5
}"""


test_file4 = """{
    a: 5
}"""


test_file5 = """{
    "expansion-coefficient": 23.4e-06,
    "length": 3.2e-3
}"""


test_file6 = """{
    "expansion-coefficient": 2.34e-05,
    "length": 0.0032
}"""


test_file7 = """[
    {
        "quantity": 261,
        "something": 23.4e-06,
    },
    {
        "quantity": 292,
        "something": 3.2e-3,
    },
    {
        "quantity": 211,
        "something": 23.4e-03,
    }
]"""


class JSONTest(LocalBearTestHelper):

    def setUp(self):
        self.section = Section('')
        self.uut = JSONFormatBear(self.section, Queue())

    def test_exception_result(self):
        self.check_results(
            self.uut,
            test_file4.split('\n'),
            [Result.from_values('JSONFormatBear',
                                'This file does not contain parsable JSON. '
                                'Expecting property name enclosed in '
                                'double quotes.',
                                file='default',
                                line=2,
                                column=5)],
            filename='default')

    def test_exception_empty_file(self):
        self.check_results(
            self.uut,
            [],
            [Result.from_values('JSONFormatBear',
                                'This file is empty.',
                                file='default')],
            filename='default')


JSONFormatBearTest = verify_local_bear(JSONFormatBear,
                                       valid_files=(test_file1, test_file2),
                                       invalid_files=(test_file3,
                                                      unicode_file,
                                                      '',
                                                      'random stuff',
                                                      '{"a":5,"b":5}'))


JSONFormatBearSortTest = verify_local_bear(JSONFormatBear,
                                           valid_files=(test_file1,),
                                           invalid_files=(test_file2,),
                                           settings={'json_sort': 'true'})


JSONFormatBearTabWidthTest = verify_local_bear(JSONFormatBear,
                                               valid_files=(test_file3,),
                                               invalid_files=(test_file2,),
                                               settings={
                                                   'indent_size': '3'})


JSONFormatBearUnicodeTest = verify_local_bear(JSONFormatBear,
                                              valid_files=(unicode_file,),
                                              invalid_files=(),
                                              settings={'escape_unicode':
                                                        'false'})

JSONFormatBearFloatsTest = verify_local_bear(JSONFormatBear,
                                             valid_files=(test_file5,
                                                          test_file6,
                                                          test_file7),
                                             invalid_files=(),
                                             settings={'escape_unicode':
                                                       'false'})
