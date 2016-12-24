from bears.yml.YAMLLintBear import YAMLLintBear
from coala_utils.ContextManagers import prepare_file
from coalib.testing.LocalBearTestHelper import verify_local_bear

test_file = """
---
receipt:     Oz-Ware Purchase Invoice
date:        2012-08-06
customer:
    first_name:   Dorothy
    family_name:  Gale

items:
    - part_no:   A4786
      descrip:   Water Bucket (Filled)
      price:     1.47
      quantity:  4
...
"""

no_start_yml_file = """receipt: Oz-Ware Purchase Invoice
date: 2012-08-06
customer:
    first_name: Dorothy
    family_name: Gale

items:
    - part_no: A4786
      descrip: Water Bucket (Filled)
      price: 1.47
      quantity: 4"""

with_start_yml_file = """---
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
                                      valid_files=(no_start_yml_file,),
                                      invalid_files=(with_start_yml_file,))

YAMLLintBear4Test = verify_local_bear(YAMLLintBear,
                                      valid_files=(with_start_yml_file,),
                                      invalid_files=(no_start_yml_file,),
                                      settings={
                                          'document_start': True})
