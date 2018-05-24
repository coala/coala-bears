import os
from queue import Queue

from bears.xml2.XCopBear import XCopBear
from coalib.testing.BearTestHelper import generate_skip_decorator
from coalib.testing.LocalBearTestHelper import LocalBearTestHelper
from coalib.settings.Section import Section


def get_testfile_path(filename):
    return os.path.join(os.path.dirname(__file__),
                        'test_files',
                        filename)


def load_testdata(filename):
    path = get_testfile_path(filename)
    with open(path) as f:
        return f.read()


valid_xml_file = load_testdata('concept-valid.xml').splitlines()
invalid_xml_file = load_testdata('concept-invalid.xml').splitlines()


@generate_skip_decorator(XCopBear)
class XCopBearTest(LocalBearTestHelper):

    def setUp(self):
        self.section = Section('')
        self.uut = XCopBear(self.section, Queue())

    def test_valid(self):
        self.check_validity(self.uut, valid_xml_file)

    def test_invalid(self):
        self.check_invalidity(self.uut, invalid_xml_file)
