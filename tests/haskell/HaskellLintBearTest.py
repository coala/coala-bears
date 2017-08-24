from queue import Queue

from bears.haskell.HaskellLintBear import HaskellLintBear
from coalib.testing.LocalBearTestHelper import LocalBearTestHelper
from coalib.testing.BearTestHelper import generate_skip_decorator
from coalib.settings.Section import Section


good_single_line_file = """
myconcat = (++)
""".splitlines()

bad_single_line_file = """
myconcat a b = ((++) a b)
""".splitlines()

good_multiple_line_file = """
import qualified Data.ByteString.Char8 as BS


main :: IO()
main =
    return $ BS.concat
        [ BS.pack "I am being tested by hlint!"
        , "String dummy"
        , "Another String dummy"
        ]
""".splitlines()

bad_multiple_line_file = """
import qualified Data.ByteString.Char8 as BS


main :: IO()
main =
    return $ BS.concat $
        [ BS.pack $ "I am being tested by hlint!"
        , "String dummy"
        , "Another String dummy"
        ]
""".splitlines()


@generate_skip_decorator(HaskellLintBear)
class HaskellLintBearTest(LocalBearTestHelper):

    def setUp(self):
        self.section = Section('name')
        self.uut = HaskellLintBear(self.section, Queue())

    def test_valid(self):
        self.check_validity(self.uut, good_single_line_file,
                            tempfile_kwargs={'suffix': '.hs'})
        self.check_validity(self.uut, good_multiple_line_file,
                            tempfile_kwargs={'suffix': '.hs'})

    def test_invalid(self):
        results = self.check_invalidity(self.uut, bad_single_line_file,
                                        tempfile_kwargs={'suffix': '.hs'})
        self.assertEqual(len(results), 1, str(results))
        self.assertIn('Redundant bracket',
                      results[0].message)

        results = self.check_invalidity(self.uut, bad_multiple_line_file,
                                        tempfile_kwargs={'suffix': '.hs'})
        self.assertEqual(len(results), 2, str(results))
        self.assertIn('Redundant $',
                      results[0].message)
