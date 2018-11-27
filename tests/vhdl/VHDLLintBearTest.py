from unittest import TestCase, mock

from bears.vhdl.VHDLLintBear import VHDLLintBear
from coalib.testing.LocalBearTestHelper import verify_local_bear


class VHDLLintBearPrerequisiteTest(TestCase):
    def test_check_prerequisites(self):
        with mock.patch('bears.vhdl.VHDLLintBear.which') as mock_which:
            mock_which.side_effect = [None]
            self.assertEqual(VHDLLintBear.check_prerequisites(),
                             'perl is not installed.')

            mock_which.side_effect = ['path/to/perl', None]
            self.assertEqual(VHDLLintBear.check_prerequisites(),
                             'bakalint is missing. Download it from '
                             '<http://fpgalibre.sourceforge.net/'
                             'ingles.html#tp46> and put it into your PATH.')

            mock_which.side_effect = ['path/to/perl', 'path/to/bakalint']
            self.assertEqual(VHDLLintBear.check_prerequisites(), True)


VHDLLintBearTest = verify_local_bear(VHDLLintBear, ('test',), ('\t',))
