from queue import Queue

from coalib.results.Diff import Diff
from coalib.settings.Section import Section
from coalib.testing.BearTestHelper import generate_skip_decorator
from coalib.testing.LocalBearTestHelper import verify_local_bear
from coalib.testing.LocalBearTestHelper import LocalBearTestHelper
from bears.js.JSStandardBear import JSStandardBear

good_file = """
var foo = {
  bar: 1,
  baz: 2
}
var { bar, baz } = foo
var x = 1
function hello (arg) { return arg }

if (baz === 2 && x !== 1) {
  window.alert('hi')
  bar = bar === 1
    ? bar
    : 1
  if ((x === 33)) {
    console.log(bar + "hello 'world'")
  }
} else {
  (function myFunction (err) {
    if (err) throw err
    console.log('nothing')
  })()
  if (hello(bar)) console.log('bar')
}
"""

bad_file_indent = """
(function () {
    console.log('hello world')
})()
"""

bad_file_quote = """
console.log("hello world")
"""

bad_file_semicolon = """
console.log('hello world');
"""

bad_file_infix = """
var a = 'world'
console.log('hello'+a)
"""

bad_file_undef = """
console.log(a)
"""

bad_file_ifelse = """
var a = 1
if (a) {
  console.log(a)
}
else {
  console.log(0)
}
"""

bad_file_func_name = """
function my_function (a) {
  return a
}
"""

JSStandardBearTest = verify_local_bear(JSStandardBear,
                                       valid_files=(good_file,),
                                       invalid_files=(bad_file_indent,
                                                      bad_file_quote,
                                                      bad_file_semicolon,
                                                      bad_file_infix,
                                                      bad_file_undef,
                                                      bad_file_ifelse,
                                                      bad_file_func_name,))


@generate_skip_decorator(JSStandardBear)
class JSStandardBearTestClass(LocalBearTestHelper):
    bad_code = """
(function () {
    console.log('wrong indentation')
    console.log('wrong indentation and semicolon');
}())
""".splitlines(True)

    def setUp(self):
        section = Section('name')
        self.js_standard_bear = JSStandardBear(section, Queue())

    def _check_diff(self, result, line_number, corrected_code):
        self.assertEqual(1, len(result.affected_code))
        affected_code = result.affected_code[0]
        self.assertEqual(line_number, affected_code.start.line)
        self.assertEqual(line_number, affected_code.end.line)

        self.assertEqual(1, len(result.diffs))
        diff = list(result.diffs.values())[0]
        expected_diff = Diff(self.bad_code)
        expected_diff.modify_line(line_number, corrected_code)
        self.assertEqual(expected_diff, diff)

    def test_diffs(self):
        results = self.check_invalidity(
            self.js_standard_bear,
            self.bad_code)
        self.assertEqual(2, len(results))

        corrected_code = "  console.log('wrong indentation')"
        self._check_diff(results[0], 3, corrected_code)

        corrected_code = "  console.log('wrong indentation and semicolon')"
        self._check_diff(results[1], 4, corrected_code)

    def test_messages(self):
        results = self.check_invalidity(
            self.js_standard_bear,
            self.bad_code)
        self.assertEqual(2, len(results))
        self.assertIn('(indent)', results[0].message)

        # Check that messages for lines with multiple issues get merged.
        self.assertIn('(indent)', results[1].message)
        self.assertIn('(semi)', results[1].message)

    def test_corrected_code(self):
        """
        Check that the corrected code is valid.
        """
        corrected_code = self.js_standard_bear._get_corrected_code(
            self.bad_code)
        self.check_validity(
            self.js_standard_bear,
            corrected_code)

    def test_get_issues_from_output(self):
        output = """
coala-bears/test.js:2:5: Expected indentation of 2 spaces but found 4. (indent)
coala-bears/test.js:3:5: Expected indentation of 2 spaces but found 4. (indent)
coala-bears/test.js:3:51: Extra semicolon. (semi)
"""
        issues = list(self.js_standard_bear._get_issues(output))
        line_numbers = [line_number for line_number, _ in issues]
        self.assertEqual(line_numbers, [2, 3])
        messages = [message for _, message in issues]
        expected_messages = [
            'Expected indentation of 2 spaces but found 4. (indent)',
            ('Expected indentation of 2 spaces but found 4. (indent)\n'
             'Extra semicolon. (semi)')]
        self.assertEqual(messages, expected_messages)

    def test_different_number_of_lines(self):
        """
        Check a case where the number of lines of the invalid and the
        corrected code differs.
        """
        bad_code_with_empty_lines = ['\n', '\n'] + self.bad_code
        results = self.check_invalidity(
            self.js_standard_bear,
            bad_code_with_empty_lines)
        self.assertEqual(3, len(results))
        self.assertIn('(no-multiple-empty-lines)', results[0].message)

        # When there the number of lines differ, the diff is `None`.
        self.assertEqual(1, len(results[0].diffs))
        diff = list(results[0].diffs.values())[0]
        self.assertEqual(None, diff)
