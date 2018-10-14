import unittest
import os

from queue import Queue

from coalib.settings.Section import Section

from bears.python.PythonPackageInitBear import PythonPackageInitBear


class PythonPackageInitBearTest(unittest.TestCase):

    def setUp(self):

        self.queue = Queue()
        self.file_dict = {}
        self.section = Section('PythonPackageInit')
        self.uut = PythonPackageInitBear(self.file_dict, self.section,
                                         self.queue)

    def run_uut(self, *args, **kwargs):
        return list(result.message for result in self.uut.run(*args, **kwargs))

    def test_missing_init(self):
        path = os.path.abspath('not-ignored-no-init/test-file.py')
        self.uut.file_dict = {path: ''}
        self.assertEqual(self.run_uut(),
                         ['Directory "{}" does not contain __init__.py file'
                          .format(os.path.relpath(os.path.split(path)[0],
                                                  self.uut.get_config_dir()))])

    def test_init_exists(self):
        path = os.path.abspath('with-init/__init__.py')
        self.uut.file_dict = {path: ''}
        self.assertEqual(self.run_uut(), [])
