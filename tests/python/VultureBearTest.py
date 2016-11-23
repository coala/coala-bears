import unittest
from queue import Queue
from textwrap import dedent
from contextlib import ExitStack, contextmanager

from coala_utils.ContextManagers import prepare_file
from coalib.settings.Section import Section

from bears.python.VultureBear import VultureBear


class VultureBearTest(unittest.TestCase):

    def setUp(self):
        self.section = Section('name')
        self.queue = Queue()
        self.file_dict = {}
        self.uut = VultureBear(self.file_dict, self.section, self.queue)

    def get_results(self, *files):
        """
        Runs the bears with the files given.

        :param files: A list of lists containing the file lines. File contents
                      will automatically be dedented and splitted.
        :return:      A list of the results of the uut!
        """
        with ExitStack() as stack:
            for file in files:
                @contextmanager
                def prep_file():
                    with prepare_file(
                        dedent(file).splitlines(True),
                        None,
                        tempfile_kwargs={'suffix': '.py'}
                    ) as lines_filename:
                        lines, filename = lines_filename
                        self.file_dict[filename] = file
                        yield

                stack.enter_context(prep_file())

            return list(self.uut.run())

    def test_used_variable(self):
        good_file = """
        x = 2
        print(x)
        """
        self.assertEqual(len(self.get_results(good_file)), 0)

    def test_unused_variable(self):
        bad_file = """
        b = 10
        a = 12
        print(a)
        """
        self.assertEqual(len(self.get_results(bad_file)), 1)

    def test_unused_parameter(self):
        bad_file = """
        def test(a):
            return 1

        test(1)
        """
        self.assertEqual(len(self.get_results(bad_file)), 1)

    def test_unused_function(self):
        bad_file = """
        def test(a):
            return a
        """
        self.assertEqual(len(self.get_results(bad_file)), 1)
