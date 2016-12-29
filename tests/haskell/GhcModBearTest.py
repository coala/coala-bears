from queue import Queue

from bears.haskell.GhcModBear import GhcModBear
from coalib.testing.LocalBearTestHelper import LocalBearTestHelper
from coalib.testing.LocalBearTestHelper import verify_local_bear
from coalib.testing.BearTestHelper import generate_skip_decorator
from coalib.settings.Section import Section
from coalib.settings.Setting import Setting


# A simple hello world program!
hello_world_file = """
main :: IO()
main = putStrLn "Hello World!"
""".splitlines()

# No instance for (Num String) in the first argument of ‘putStrLn’
not_string_3 = """
main :: IO()
main = putStrLn 3
""".splitlines()

# Takes a file and prints the number of lines
count_lines = """
main :: IO()
main = interact lineC
    where lineC input = show (length(lines input))
""".splitlines()

# Parse Error (mismatched brackets)
count_lines_bracket_missing = """
main :: IO()
main = interact lineC
    where lineC input = show (length(lines input)
""".splitlines()

# Prints "asd" which is the last but one element in the list
last_but_one_list = """
lastButOne :: [a] -> a
lastButOne xs | (length xs >= 2) = xs !! ((length xs) - 2)
              | otherwise = error "Not possible"

main :: IO()
main = do
    print(lastButOne(["asd", "ASd"]))
""".splitlines()

# Couldn't match expected type ‘[a]’ with actual type ‘a’
last_but_one_list_type_error = """
lastButOne :: a -> a
lastButOne xs | (length xs >= 2) = xs !! ((length xs) - 2)
              | otherwise = error "Not possible"

main :: IO()
main = do
    print(lastButOne(["asd", "ASd"]))
""".splitlines()


@generate_skip_decorator(GhcModBear)
class GhcModBearTest(LocalBearTestHelper):

    def setUp(self):
        self.section = Section('name')
        self.uut = GhcModBear(self.section, Queue())

    def test_valid(self):
        self.check_validity(self.uut, hello_world_file, valid=True,
                            tempfile_kwargs={'suffix': '.hs'})
        self.check_validity(self.uut, count_lines, valid=True,
                            tempfile_kwargs={'suffix': '.hs'})
        self.check_validity(self.uut, last_but_one_list,
                            valid=True,
                            tempfile_kwargs={'suffix': '.hs'})

    def test_invalid(self):
        results = self.check_validity(self.uut, not_string_3,
                                      valid=False,
                                      tempfile_kwargs={'suffix': '.hs'})
        self.assertEqual(len(results), 1, str(results))
        self.assertIn('No instance for (Num String) arising from the literal ',
                      results[0].message)
        results = self.check_validity(self.uut,
                                      count_lines_bracket_missing,
                                      valid=False,
                                      tempfile_kwargs={'suffix': '.hs'})
        self.assertEqual(len(results), 1, str(results))
        self.assertIn('parse error (possibly incorrect indentation '
                      'or mismatched brackets)', results[0].message)
        results = self.check_validity(self.uut,
                                      last_but_one_list_type_error,
                                      valid=False,
                                      tempfile_kwargs={'suffix': '.hs'})
        self.assertEqual(len(results), 1, str(results))
        self.assertIn("Couldn't match expected type",
                      results[0].message)
