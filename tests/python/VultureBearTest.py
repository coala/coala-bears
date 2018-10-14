import os
import unittest
from queue import Queue
from textwrap import dedent
from contextlib import ExitStack, contextmanager

from coala_utils.ContextManagers import prepare_file
from coalib.settings.Section import Section

from bears.python.VultureBear import VultureBear


def get_testfile_path(name):
    return os.path.join(os.path.dirname(__file__), 'vulture_test_files', name)


def load_testfile(name):
    with open(get_testfile_path(name)) as f:
        return f.read()


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

    def verify_results(self, test_file, expected):
        detected = dict((item.message, (item.affected_code[0].start.line,
                                        item.affected_code[0].end.line,
                                        item.confidence))
                        for item in self.get_results(load_testfile(test_file)))
        self.assertEqual(detected, expected)

    def test_used_variable(self):
        self.verify_results('used_variable.py', {})

    def test_unused_variable(self):
        self.verify_results('unused_variable.py', {
            "unused variable 'b'": (1, 1, 60)
        })

    def test_unused_arg(self):
        self.verify_results('unused_arg.py', {
            "unused variable 'a'": (1, 1, 100)
        })

    def test_import(self):
        self.verify_results('unused_import.py', {
            "unused import 'subprocess'": (2, 2, 90)
        })

    def test_class(self):
        self.verify_results('unused_class.py', {
            "unused class 'Name'": (1, 5, 60),
            "unused attribute 'name'": (4, 4, 60),
            "unused attribute 'surname'": (5, 5, 60)
        })

    def test_function(self):
        self.verify_results('unused_function.py', {
            "unused function 'hello'": (1, 2, 60)
        })

    def test_property(self):
        self.verify_results('unused_property.py', {
            "unused property 'prop'": (3, 5, 60)
        })

    def test_unsatisfiable_while(self):
        self.verify_results('unsatisfiable_while.py', {
            "unsatisfiable 'while' condition": (5, 7, 100)
        })

    def test_unsatisfiable_if(self):
        self.verify_results('unsatisfiable_if.py', {
            "unsatisfiable 'if' condition": (1, 2, 100)
        })

    def test_unreachable_else(self):
        self.verify_results('unreachable_else.py', {
            "unreachable 'else' block": (3, 6, 100)
        })
