import shutil
import tempfile
from os import path
import unittest

from bears.general.CheckmanifestBear import CheckmanifestBear
from tests.LocalBearTestHelper import verify_local_bear


class TestExample(unittest.TestCase):

    def setUp(self):
        self.test_dir = tempfile.mkdtemp()

    def tearDown(self):
        shutil.rmtree(self.test_dir)

    def test_something(self):
        with open(path.join(self.test_dir, 'setup.py'), 'w') as f:
            f.write("from setuptools import setup\n")
            f.write("setup(name='sample', py_modules=['sample'])\n")
        with open(path.join(self.test_dir, 'sample.py'), 'w') as f:
            f.write("# wow. such code. so amaze\n")
        f = open(path.join(self.test_dir, 'MANIFEST.in'), 'w')
        f = open(path.join(self.test_dir, 'unrelated.txt'), 'w')
        f.write('Hello from the other side')
        # Ignore LineLengthBear
        CheckmanifestBearTest_suggestion = verify_local_bear(
            CheckmanifestBear,
            invalid_files=(path.join(self.test_dir,
                                     'MANIFEST.in')))
        CheckmanifestBearTest_suggestion = verify_local_bear(CheckmanifestBear,
                                                             valid_files=(
                                                                 path.join(self.test_dir,
                                                                           'MANIFEST.in')),
                                                             settings={"ignore":
                                                                       "unrelated.txt"})

if __name__ == '__main__':
    unittest.main
