from bears.yaml.YAMLLintBear import YAMLLintBear
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
""".split("\n")

YAMLLintBear1Test = verify_local_bear(YAMLLintBear,
                                      valid_files=(),
                                      invalid_files=(test_file,))

YAMLLintBear2Test = verify_local_bear(YAMLLintBear,
                                      valid_files=(test_file,),
                                      invalid_files=(),
                                      settings={
                                          'yamllint_config': 'config.yml'})
