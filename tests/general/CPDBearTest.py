import os
import unittest

from queue import Queue
import logging


from bears.general.CPDBear import CPDBear
from coalib.bearlib.languages import Language
from coalib.testing.BearTestHelper import generate_skip_decorator
from coalib.settings.Section import Section
from coalib.settings.Setting import Setting


@generate_skip_decorator(CPDBear)
class CPDBearTest(unittest.TestCase):

    def setUp(self):
        self.base_test_path = os.path.abspath(os.path.join(
            os.path.dirname(__file__),
            'code_duplication_samples'))

        self.section = Section('default')
        self.section.append(Setting('programming_language', 'Java'))
        self.section.language = Language['Java']
        self.queue = Queue()

    def test_good_file(self):
        good_file = os.path.join(self.base_test_path, 'good_code.java')

        with open(good_file) as file:
            good_filelines = file.readlines()

        self.uut = CPDBear({good_file: good_filelines},
                           self.section,
                           self.queue)

        result = list(self.uut.run_bear_from_section([], {}))

        self.assertEqual(result, [])

    def test_bad_file(self):
        bad_file = os.path.join(self.base_test_path, 'bad_code.java')

        with open(bad_file) as file:
            bad_filelines = file.readlines()

        self.uut = CPDBear({bad_file: bad_filelines},
                           self.section,
                           self.queue)

        result = list(self.uut.run_bear_from_section([], {}))

        self.assertNotEqual(result, [])

    def test_unsupported_language(self):
        self.section.update_setting(
            key='programming_language', new_value='html')
        self.section.language = Language['html']

        self.uut = CPDBear({'file_name': 'hello world  \n'},
                           self.section,
                           self.queue)

        list(self.uut.run_bear_from_section([], {}))
        self.assertEqual(
            self.uut.message_queue.queue[0].log_level, logging.WARNING)
        self.assertEqual('This bear has no support for html.',
                         self.uut.message_queue.queue[0].message)
