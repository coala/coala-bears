import os
import unittest

from generate_bear_requirements import main


class RunTest(unittest.TestCase):

    def setUp(self):
        self.orig_dir = os.getcwd()

    def test_dependency_yaml_check(self):
        rv = main(['--update', '--check'])
        self.assertEqual(rv, None)

    def tearDown(self):
        shutil.rmtree(os.path.join(self.BEARS_UPLOAD_PATH))

        os.chdir(self.orig_dir)
