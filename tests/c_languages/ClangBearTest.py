from collections import namedtuple
import unittest
from unittest.mock import patch

from bears.c_languages.ClangBear import (
    ClangBear, diff_from_clang_fixit, sourcerange_from_clang_range)
from coalib.results.SourceRange import SourceRange
from coalib.settings.Section import Section
from coalib.testing.LocalBearTestHelper import verify_local_bear


class ClangBearUtilitiesTest(unittest.TestCase):
    @patch('bears.c_languages.ClangBear.get_distribution')
    def test_correct_clang_version_requirement(self, get_distribution):
        get_distribution.configure_mode(version='1.2')

        self.assertRaisesRegex(RuntimeError,
                               r'ClangBear requires clang 3\.4\.0',
                               ClangBear, Section('test-section'), None)

    def test_from_clang_fixit(self):
        try:
            from clang.cindex import Index, LibclangError
        except ImportError as err:
            raise unittest.case.SkipTest(str(err))

        joined_file = 'struct { int f0; }\nx = { f0 :1 };\n'
        file = joined_file.splitlines(True)
        fixed_file = ['struct { int f0; }\n', 'x = { .f0 = 1 };\n']
        try:
            tu = Index.create().parse('t.c', unsaved_files=[
                ('t.c', joined_file)])
        except LibclangError as err:
            raise unittest.case.SkipTest(str(err))

        fixit = tu.diagnostics[0].fixits[0]
        clang_fixed_file = diff_from_clang_fixit(fixit, file).modified
        self.assertEqual(fixed_file, clang_fixed_file)

    def test_from_clang_range(self):
        # Simulating a clang SourceRange is easier than setting one up without
        # actually parsing a complete C file.
        ClangRange = namedtuple('ClangRange', 'start end')
        ClangPosition = namedtuple('ClangPosition', 'file line column')
        ClangFile = namedtuple('ClangFile', 'name')
        file = ClangFile('t.c')
        start = ClangPosition(file, 1, 2)
        end = ClangPosition(file, 3, 4)

        uut = sourcerange_from_clang_range(ClangRange(start, end))
        compare = SourceRange.from_values('t.c', 1, 2, 3, 4)
        self.assertEqual(uut, compare)


ClangBearTest = verify_local_bear(
    ClangBear,
    ('int main() {}', ),
    ('bad things, this is no C code',  # Has no fixit
     # Has a fixit and no range
     'struct { int f0; } x = { f0 :1 };',
     'int main() {int *b; return b}'),  # Has a fixit and a range
    'test.c')


ClangBearIgnoreTest = verify_local_bear(
    ClangBear,
    # Should ignore the warning, valid!
    ('struct { int f0; } x = { f0 :1 };',),
    (),
    'test.c',
    settings={'clang_cli_options': '-w'})
