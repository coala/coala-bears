from bears.js.JSONFormatBear import JSONFormatBear
from tests.LocalBearTestHelper import verify_local_bear


test_file1 = """{
    "a": 5,
    "b": 5
}""".splitlines(keepends=True)


test_file2 = """{
    "b": 5,
    "a": 5
}""".splitlines(keepends=True)


test_file3 = """{
   "b": 5,
   "a": 5
}""".splitlines(keepends=True)


unicode_file = """{
    "⌘": 5
}""".splitlines(keepends=True)


JSONFormatBearTest = verify_local_bear(JSONFormatBear,
                                       valid_files=(test_file1, test_file2),
                                       invalid_files=(test_file3,
                                                      unicode_file,
                                                      [""],
                                                      ["random stuff"],
                                                      ['{"a":5,"b":5}']))


JSONFormatBearSortTest = verify_local_bear(JSONFormatBear,
                                           valid_files=(test_file1,),
                                           invalid_files=(test_file2,),
                                           settings={"json_sort": "true"})


JSONFormatBearTabWidthTest = verify_local_bear(JSONFormatBear,
                                               valid_files=(test_file3,),
                                               invalid_files=(test_file2,),
                                               settings={"tab_width": "3"})


JSONFormatBearUnicodeTest = verify_local_bear(JSONFormatBear,
                                              valid_files=(unicode_file,),
                                              invalid_files=(),
                                              settings={'keep_unicode': 'true'})
