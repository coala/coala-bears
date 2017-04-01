import unittest
from queue import Queue

from coalib.settings.Section import Section
from coalib.results.RESULT_SEVERITY import RESULT_SEVERITY
from coalib.bearlib.aspects.Spelling import aspectsYEAH
from bears.general.aspectsYEAHBear import aspectsYEAHBear


class aspectsYEAHBearTest(unittest.TestCase):

    def setUp(self):
        self.section = Section('name')
        self.queue = Queue()
        self.uut = aspectsYEAHBear(self.section, self.queue)

    def test_severity(self):
        bad_file = """
        AsPectYEAH
        """
        results = list(self.uut.run('bad_file', bad_file.split('\n')))
        self.assertEqual(results[0].severity,
                         RESULT_SEVERITY.MAJOR)

    def test_message(self):
        bad_file = """
        Aspects
        Aspectyeah"""
        results = list(self.uut.run('bad_file', bad_file.split('\n')))
        self.assertEqual(results[0].message,
                         '``aspect`` is always written'
                         ' with lower case characters')
        self.assertEqual(results[1].message,
                         '``aspectsYEAH`` is always written with '
                         'lower case ``aspects`` and upper case ``YEAH``')

    def test_aspect(self):
        bad_file = """
        Aspects
        """
        results = list(self.uut.run('bad_file', bad_file.split('\n')))
        self.assertEqual(type(results[0].aspect), aspectsYEAH)
