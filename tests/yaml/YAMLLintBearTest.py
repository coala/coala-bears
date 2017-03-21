import unittest
from queue import Queue

from bears.yaml.YAMLLintBear import YAMLLintBear
from coala_utils.ContextManagers import prepare_file
from coalib.testing.LocalBearTestHelper import verify_local_bear, execute_bear
from coalib.testing.BearTestHelper import generate_skip_decorator
from coalib.results.RESULT_SEVERITY import RESULT_SEVERITY
from coalib.settings.Section import Section

test_file = """
---
receipt:     Oz-Ware Purchase Invoice
date:        2012-08-06
customer:
    first_name:   Dorothy
    family_name:  Gale

items:
    - part_no:   A4786
#    - part_tag:  A5679
      descrip:   Water Bucket (Filled)
      price:     1.47
      quantity:  4
...
"""

no_start_yaml_file = """receipt: Oz-Ware Purchase Invoice
date: 2012-08-06
customer:
    first_name: Dorothy
    family_name: Gale

items:
    - part_no: A4786
      descrip: Water Bucket (Filled)
      price: 1.47
      quantity: 4"""

with_start_yaml_file = """---
receipt: Oz-Ware Purchase Invoice
date: 2012-08-06
customer:
    first_name: Dorothy
    family_name: Gale

items:
    - part_no: A4786
      descrip: Water Bucket (Filled)
      price: 1.47
      quantity: 4
..."""

config_file = """
extends:
    default
rules:
    colons:
      max-spaces-after: -1
    indentation: disable
    empty-lines: disable
"""


YAMLLintBear1Test = verify_local_bear(YAMLLintBear,
                                      valid_files=(),
                                      invalid_files=(test_file,))

with prepare_file(config_file,
                  filename=None,
                  force_linebreaks=True,
                  create_tempfile=True) as (conf_lines, conf_file):
    YAMLLintBear2Test = verify_local_bear(YAMLLintBear,
                                          valid_files=(test_file,),
                                          invalid_files=(),
                                          settings={
                                              'yamllint_config': conf_file})

YAMLLintBear3Test = verify_local_bear(YAMLLintBear,
                                      valid_files=(no_start_yaml_file,
                                                   with_start_yaml_file,),
                                      invalid_files=())

YAMLLintBear4Test = verify_local_bear(YAMLLintBear,
                                      valid_files=(no_start_yaml_file,),
                                      invalid_files=(with_start_yaml_file,),
                                      settings={'document_start': False})

YAMLLintBear5Test = verify_local_bear(YAMLLintBear,
                                      valid_files=(with_start_yaml_file,),
                                      invalid_files=(no_start_yaml_file,),
                                      settings={'document_start': True})


@generate_skip_decorator(YAMLLintBear)
class YAMLLintBearSeverityTest(unittest.TestCase):

    def setUp(self):
        self.section = Section('')
        self.uut = YAMLLintBear(self.section, Queue())

    def test_warning(self):
        content = test_file.splitlines()
        with prepare_file(content, None) as (file, fname):
            with execute_bear(self.uut, fname, file) as results:
                self.assertEqual(results[6].message, 'comment not indented'
                                 ' like content (comments-indentation)')
                self.assertEqual(results[6].affected_code[0].start.line, 11)
                self.assertEqual(results[6].affected_code[0].end.line, 11)
                self.assertEqual(results[6].severity, RESULT_SEVERITY.NORMAL)

    def test_error(self):
        content = test_file.splitlines()
        with prepare_file(content, None) as (file, fname):
            with execute_bear(self.uut, fname, file) as results:
                self.assertEqual(results[0].message, 'too many blank lines'
                                 ' (1 > 0) (empty-lines)')
                self.assertEqual(results[0].affected_code[0].start.line, 1)
                self.assertEqual(results[0].affected_code[0].end.line, 1)
                self.assertEqual(results[0].severity, RESULT_SEVERITY.MAJOR)
