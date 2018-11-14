import unittest
from unittest.mock import patch

from bears.natural_language.AlexBear import AlexBear
from coalib.testing.BearTestHelper import generate_skip_decorator
from coalib.testing.LocalBearTestHelper import verify_local_bear

good_file = 'Their network looks good.'

bad_file = 'His network looks good.'


AlexBearTest = verify_local_bear(AlexBear,
                                 valid_files=(good_file,),
                                 invalid_files=(bad_file,))


@generate_skip_decorator(AlexBear)
@patch('bears.natural_language.AlexBear.subprocess.check_output')
class AlexBearPrereqTest(unittest.TestCase):

    @patch('%s.super.check_prerequisites' % __name__, create=True)
    def test_alex_not_installed(self, check_output_mock):
        check_output_mock.side_effect = OSError
        self.assertIn('The `alex` package is not installed',
                      AlexBear.check_prerequisites())

    def test_unverified_alex_installed(self, check_output_mock):
        check_output_mock.side_effect = OSError
        self.assertIn('The `alex` package could not be verified',
                      AlexBear.check_prerequisites())

    def test_wrong_alex_installed(self, check_output_mock):
        check_output_mock.return_value = b'Unexpected output from package'
        self.assertIn("The `alex` package that's been installed seems to "
                      'be incorrect',
                      AlexBear.check_prerequisites())

    def test_right_alex_installed(self, check_output_mock):
        check_output_mock.return_value = (
            b'Some text here\n'
            b'  Catch insensitive, inconsiderate writing\n'
            b'Usage instructions and examples here ....')
        self.assertTrue(AlexBear.check_prerequisites())
