import os
import unittest
from queue import Queue

from bears.non_free.MlintBear import MlintBear
from coalib.testing.LocalBearTestHelper import execute_bear
from coalib.testing.BearTestHelper import generate_skip_decorator
from coalib.settings.Section import Section
from coalib.settings.Setting import Setting


def get_absolute_test_path(file):
    return os.path.join(os.path.dirname(__file__),
                        'mlint_test_files', file)


@generate_skip_decorator(MlintBear)
class MlintBearTest(unittest.TestCase):

    def setUp(self):
        self.section = Section('')
        self.uut = MlintBear(self.section, Queue())
        self.good_file = 'lengthofline2.m'
        self.bad_file = 'lengthofline.m'

    def test_good_file(self):
        filename = get_absolute_test_path(self.good_file)
        with execute_bear(self.uut, filename) as result:
            self.assertEqual(result, [])

    def test_cli_options(self):
        filename = get_absolute_test_path(self.bad_file)
        self.section.append(Setting('mlint_cli_options', '-cyc -id'))
        expected_result = [
            'CABE: The McCabe complexity of \'lengthofline\' is 12.',
            'NASGU: The value assigned to variable \'nothandle\' ' +
            'might be unused.',
            'PSIZE: NUMEL(x) is usually faster than PROD(SIZE(x)).',
            'AGROW: The variable \'notline\' appears to change size ' +
            'on every loop iteration. Consider preallocating for speed.',
            'STCI: Use STRCMPI(str1,str2) instead of using UPPER/LOWER ' +
            'in a call to STRCMP.',
            'PSIZE: NUMEL(x) is usually faster than PROD(SIZE(x)).',
            'AGROW: The variable \'data\' appears to change size on ' +
            'every loop iteration. Consider preallocating for speed.',
            'GFLD: Use dynamic fieldnames with structures instead ' +
            'of GETFIELD.',
            'OR2: Use || instead of | as the OR operator in (scalar) ' +
            'conditional statements.',
            'OR2: Use || instead of | as the OR operator in (scalar) ' +
            'conditional statements.',
            'OR2: Use || instead of | as the OR operator in (scalar) ' +
            'conditional statements.',
            'AGROW: The variable \'dim\' appears to change size on ' +
            'every loop iteration. Consider preallocating for speed.',
            'AGROW: The variable \'dim\' appears to change size on ' +
            'every loop iteration. Consider preallocating for speed.',
            'NOPAR: Invalid syntax at \';\'. Possibly, a ), }, or ] ' +
            'is missing.',
            'NOPAR: Invalid syntax at \')\'. Possibly, a ), }, or ] ' +
            'is missing.',
            'SYNER: Parse error at \']\': usage might be invalid ' +
            'MATLAB syntax.',
            'NOPRT: Terminate statement with semicolon to suppress output ' +
            '(in functions).',
            'NBRAK: Use of brackets [] is unnecessary. Use parentheses ' +
            'to group, if needed.'
        ]
        with execute_bear(self.uut, filename) as result:
            for i in range(len(result)):
                self.assertEqual(result[i].message, expected_result[i])

    def test_bad_file(self):
        filename = get_absolute_test_path(self.bad_file)
        expected_result = [
            'The value assigned to variable \'nothandle\' might be unused.',
            'NUMEL(x) is usually faster than PROD(SIZE(x)).',
            'The variable \'notline\' appears to change size on every ' +
            'loop iteration. Consider preallocating for speed.',
            'Use STRCMPI(str1,str2) instead of using UPPER/LOWER in a call ' +
            'to STRCMP.',
            'NUMEL(x) is usually faster than PROD(SIZE(x)).',
            'The variable \'data\' appears to change size on every loop ' +
            'iteration. Consider preallocating for speed.',
            'Use dynamic fieldnames with structures instead of GETFIELD.',
            'Use || instead of | as the OR operator in (scalar) conditional ' +
            'statements.',
            'Use || instead of | as the OR operator in (scalar) conditional ' +
            'statements.',
            'Use || instead of | as the OR operator in (scalar) conditional ' +
            'statements.',
            'The variable \'dim\' appears to change size on every loop ' +
            'iteration. Consider preallocating for speed.',
            'The variable \'dim\' appears to change size on every loop ' +
            'iteration. Consider preallocating for speed.',
            'Invalid syntax at \';\'. Possibly, a ), }, or ] is missing.',
            'Invalid syntax at \')\'. Possibly, a ), }, or ] is missing.',
            'Parse error at \']\': usage might be invalid MATLAB syntax.',
            'Terminate statement with semicolon to suppress output ' +
            '(in functions).',
            'Use of brackets [] is unnecessary. Use parentheses to group, ' +
            'if needed.'
        ]
        with execute_bear(self.uut, filename) as result:
            for i in range(len(result)):
                self.assertEqual(result[i].message, expected_result[i])
