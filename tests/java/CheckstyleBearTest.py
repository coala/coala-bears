import os
import pathlib
from tempfile import NamedTemporaryFile
from queue import Queue

from bears.java import CheckstyleBear
from tests.BearTestHelper import generate_skip_decorator
from tests.LocalBearTestHelper import LocalBearTestHelper
from coalib.settings.Section import Section
from coalib.settings.Setting import path, Setting


@generate_skip_decorator(CheckstyleBear.CheckstyleBear)
class CheckstyleBearTest(LocalBearTestHelper):

    def setUp(self):
        self.section = Section("test section")
        self.uut = CheckstyleBear.CheckstyleBear(self.section, Queue())
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


def known_checkstyle_test(monkeypatch):
    monkeypatch.setattr(CheckstyleBear, 'known_checkstyles', {'such': 'style'})
    assert CheckstyleBear.known_checkstyle_or_path('such') == 'such'


def known_path_test(monkeypatch):
    monkeypatch.setattr(CheckstyleBear, 'known_checkstyles', {'such': 'style'})
    with NamedTemporaryFile() as coafile, NamedTemporaryFile() as style_file:
        coafile_path = pathlib.Path(coafile.name)
        style_path = pathlib.Path(style_file.name)
        setting = Setting(
            'style_path', style_path.name, origin=str(coafile_path))
        assert (
            CheckstyleBear.known_checkstyle_or_path(setting) == str(style_path)
        )
