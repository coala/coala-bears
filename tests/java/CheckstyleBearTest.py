import os
from queue import Queue

from bears.java.CheckstyleBear import CheckstyleBear
from tests.BearTestHelper import generate_skip_decorator
from tests.LocalBearTestHelper import LocalBearTestHelper
from coalib.settings.Section import Section


@generate_skip_decorator(CheckstyleBear)
class CheckstyleBearTest(LocalBearTestHelper):

    def setUp(self):
        self.section = Section("test section")
        self.uut = CheckstyleBear(self.section, Queue())
        test_files = os.path.join(os.path.dirname(__file__), "test_files")
        self.good_file = os.path.join(test_files, "CheckstyleGood.java")
        self.bad_file = os.path.join(test_files, "CheckstyleBad.java")
        self.empty_config = os.path.join(test_files,
                                         "checkstyle_empty_config.xml")

    def test_run(self):
        self.check_validity(self.uut, [], self.good_file)
        self.check_validity(self.uut, [], self.bad_file, valid=False)

    def test_known_configs(self):
        self.section["checkstyle_configs"] = "google"
        self.check_validity(self.uut, [], self.good_file)

    def test_with_custom_configfile(self):
        self.section["checkstyle_configs"] = self.empty_config
        self.check_validity(self.uut, [], self.good_file)
        self.check_validity(self.uut, [], self.bad_file)
