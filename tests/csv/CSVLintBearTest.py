import unittest

from queue import Queue
from bears.csv.CSVLintBear import CSVLintBear
from coalib.testing.BearTestHelper import generate_skip_decorator
from coalib.testing.LocalBearTestHelper import verify_local_bear, execute_bear
from coalib.results.RESULT_SEVERITY import RESULT_SEVERITY
from coalib.settings.Section import Section
from coala_utils.ContextManagers import prepare_file

good_file = """id,first_name,last_name,email,gender,ip_address
1,Cynthia,Rogers,crogers0@nasa.gov,Female,158.131.39.207
2,Lisa,Carroll,lcarroll1@elegantthemes.com,Female,157.69.195.53
3,Kevin,Baker,kbaker2@imageshack.us,Male,113.189.69.4
"""

major_file = """id,first_name,last_name,email,gender,ip_address
1,Cynthia,Rogers,crogers0@nasa.gov,Female,158.131.39.207
2,Lisa,Carroll,lcarroll1@elegantthemes.com,157.69.195.53
3,Kevin,Baker,kbaker2@imageshack.us,Male,113.189.69.4
"""

normal_file = """id,first_name,last_name,email,gender,ip_address,first_name
1,Cynthia,Rogers,crogers0@nasa.gov,Female,158.131.39.207,A
2,Lisa,Carroll,lcarroll1@elegantthemes.com,Female,157.69.195.53,A
3,Kevin,Baker,kbaker2@imageshack.us,Male,113.189.69.4,A
"""

CSVLintBearTest = verify_local_bear(CSVLintBear,
                                    valid_files=(good_file,),
                                    invalid_files=(major_file, normal_file))


@generate_skip_decorator(CSVLintBear)
class CSVLintBearSeverityTest(unittest.TestCase):

    def setUp(self):
        self.section = Section('')
        self.uut = CSVLintBear(self.section, Queue())

    def test_normal(self):
        content = normal_file.splitlines()
        with prepare_file(content, None) as (file, fname):
            with execute_bear(self.uut, fname, file) as results:
                self.assertEqual(results[0].severity, RESULT_SEVERITY.NORMAL)
                self.assertEqual(results[0].message,
                                 'A column in the CSV header'
                                 ' has a duplicate name. Column: 7')
                self.assertEqual(results[0].origin,
                                 'CSVLintBear (duplicate_column_name)')
                self.assertEqual(results[0].aspect, None)

    def test_errors(self):
        content = major_file.splitlines()
        with prepare_file(content, None) as (file, fname):
            with execute_bear(self.uut, fname, file) as results:
                self.assertEqual(results[0].severity, RESULT_SEVERITY.MAJOR)
                self.assertEqual(results[0].message,
                                 'Row has a different number of columns.'
                                 ' (than the first row in the file)')
                self.assertEqual(results[0].origin,
                                 'CSVLintBear (ragged_rows)')
                self.assertEqual(results[0].aspect, None)
