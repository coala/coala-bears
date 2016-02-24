from bears.yaml.YAMLLintBear import YAMLLintBear
from coalib.misc.ContextManagers import prepare_file
from tests.LocalBearTestHelper import verify_local_bear

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
""".splitlines(keepends=True)

config_file = """
extends:
    default
rules:
    colons:
      max-spaces-after: -1
    indentation: disable
    empty-lines: disable
""".splitlines(keepends=True)


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
