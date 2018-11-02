import unittest

from generate_bear_requirements import main


class RunTest(unittest.TestCase):

    def test_run(self):
        rv = main(['--update', '--check'])
        self.assertEqual(rv, None)
