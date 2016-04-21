import os
import unittest
from queue import Queue

from clang.cindex import Index
from coalib.results.Result import Result
from coalib.results.SourceRange import SourceRange
from coalib.settings.Section import Section

from bears.c_languages.ClangComplexityBear import (
    ClangComplexityBear)
from tests.BearTestHelper import generate_skip_decorator
from tests.LocalBearTestHelper import execute_bear


@generate_skip_decorator(ClangComplexityBear)
class ClangComplexityBearTest(unittest.TestCase):

    def setUp(self):
        self.filename = os.path.abspath(os.path.join(os.path.dirname(__file__),
                                                     "codeclone_detection",
                                                     "conditions_samples.c"))
        self.file = "fake"
        self.queue = Queue()
        self.section = Section("test section")
        self.bear = ClangComplexityBear(self.section, self.queue)

    def test_calculation(self):
        """
        Testing that number of decision points and exit points are calculated
        correctly.
        """
        expected = [
            ('used(int, int)', 3),
            ('returned(int, int)', 1),
            ('loopy(int, int)', 5),
            ('in_condition(int, int)', 1),
            ('assignation(int, int)', 2),
            ('arithmetics(int, int)', 1),
            ('levels(int, int, int)', 10),
            ('structing(struct test_struct, struct test_struct *)', 1),
            ('switching(int, int)', 2)]

        root = Index.create().parse(self.filename).cursor
        complexities_gen = self.bear.complexities(root, self.filename)
        results = [(cursor.displayname, complexity)
                   for cursor, complexity in complexities_gen]
        self.assertSequenceEqual(results, expected)

    def test_output(self):
        """
        Validating that the yielded results are correct.
        """
        affected_code = (SourceRange.from_values(
            self.filename,
            start_line=111,
            start_column=1,
            end_line=143,
            end_column=2),)
        expected_result = Result(
            self.bear,
            "The function 'levels(int, int, int)' should be simplified. Its "
            "cyclomatic complexity is 10 which exceeds maximal recommended "
            "value of 8.",
            affected_code=affected_code)
        with execute_bear(self.bear, self.filename, self.file, 8) as out:
            self.assertEqual(len(out), 1)
        out[0].additional_info = ""  # Let's not test this, static and huge
        self.assertEqual(out[0], expected_result)

    def test_empty_declared_function(self):
        """
        Should not take into account and display empty function declarations.
        """
        self.filename = os.path.abspath(os.path.join(os.path.dirname(__file__),
                                                     "test_files",
                                                     "empty_declarations.c"))
        expected = [('with_body(int *)', 1)]

        root = Index.create().parse(self.filename).cursor
        complexities_gen = self.bear.complexities(root, self.filename)
        results = [(cursor.displayname, complexity)
                   for cursor, complexity in complexities_gen]
        self.assertSequenceEqual(results, expected)

    def test_file_does_not_exist(self):
        """
        Tests that bear throws TranslationUnitLoadError when file does not
        exist.
        """
        from clang.cindex import TranslationUnitLoadError

        generator = self.bear.execute("not_existing", self.file)
        self.assertNotEqual(generator, None)
        with self.assertRaises(TranslationUnitLoadError):
            yield generator
