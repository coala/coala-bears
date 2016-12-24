import unittest
from unittest.mock import patch

from bears.natural_language.AlexBear import AlexBear
from tests.BearTestHelper import generate_skip_decorator
from coalib.testing.LocalBearTestHelper import verify_local_bear

good_file = 'Their network looks good.'

bad_file = 'His network looks good.'


AlexBearTest = verify_local_bear(AlexBear,
                                 valid_files=(good_file,),
                                 invalid_files=(bad_file,))


@generate_skip_decorator(AlexBear)
@patch('bears.natural_language.AlexBear.subprocess.check_output')
class AlexBearPrereqTest(unittest.TestCase):

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
