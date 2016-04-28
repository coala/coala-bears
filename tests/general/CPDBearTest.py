import os
import unittest

from queue import Queue


from bears.general.CPDBear import CPDBear
from tests.BearTestHelper import generate_skip_decorator
from coalib.settings.Section import Section
from coalib.settings.Setting import Setting


@generate_skip_decorator(CPDBear)
class CPDBearTest(unittest.TestCase):

    def setUp(self):
        self.base_test_path = os.path.abspath(os.path.join(
            os.path.dirname(__file__),
            "code_duplication_samples"))

        self.section = Section("default")
        self.section.append(Setting("language", "java"))
        self.queue = Queue()

    def test_good_file(self):
        good_file = os.path.join(self.base_test_path, "good_code.java")

        with open(good_file) as file:
            good_filelines = file.readlines()

        self.uut = CPDBear({good_file: good_filelines},
                           self.section,
                           self.queue)

        result = list(self.uut.run_bear_from_section([], {}))

        self.assertEqual(result, [])

    def test_bad_file(self):

        bad_file = os.path.join(self.base_test_path, "bad_code.java")

        with open(bad_file) as file:
            bad_filelines = file.readlines()

        self.uut = CPDBear({bad_file: bad_filelines},
                           self.section,
                           self.queue)

        result = list(self.uut.run_bear_from_section([], {}))

        self.assertNotEqual(result, [])
