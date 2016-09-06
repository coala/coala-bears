import json

from bears.js import JSONFormatBear
from tests.LocalBearTestHelper import verify_local_bear


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


JSONFormatBearTest = verify_local_bear(JSONFormatBear.JSONFormatBear,
                                       valid_files=(test_file1, test_file2),
                                       invalid_files=(test_file3,
                                                      unicode_file,
                                                      "",
                                                      "random stuff",
                                                      '{"a":5,"b":5}'))


JSONFormatBearSortTest = verify_local_bear(JSONFormatBear.JSONFormatBear,
                                           valid_files=(test_file1,),
                                           invalid_files=(test_file2,),
                                           settings={"json_sort": "true"})


JSONFormatBearTabWidthTest = verify_local_bear(JSONFormatBear.JSONFormatBear,
                                               valid_files=(test_file3,),
                                               invalid_files=(test_file2,),
                                               settings={
                                                   "indent_size": "3"})


JSONFormatBearUnicodeTest = verify_local_bear(JSONFormatBear.JSONFormatBear,
                                              valid_files=(unicode_file,),
                                              invalid_files=(),
                                              settings={'escape_unicode':
                                                        'false'})


def get_available_decodeerror_test(monkeypatch):
    class TestError(Exception):
        pass
    monkeypatch.setattr(
        json.decoder, 'JSONDecodeError', TestError, raising=False)
    result = JSONFormatBear.get_available_decodeerror()
    assert result == TestError


def get_available_decodeerror_py34_test(monkeypatch):
    monkeypatch.delattr('json.decoder.JSONDecodeError', raising=False)
    result = JSONFormatBear.get_available_decodeerror()
    assert result == ValueError
