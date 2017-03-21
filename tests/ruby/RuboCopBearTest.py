import os

from bears.ruby.RuboCopBear import RuboCopBear
from coalib.testing.LocalBearTestHelper import verify_local_bear

good_file = """def good_name
  test if something
end
"""

bad_file = """def badName
  test if something
end
"""


RuboCopBearTest = verify_local_bear(RuboCopBear,
                                    invalid_files=(bad_file,),
                                    valid_files=(good_file,))

# Testing Config
rubocop_config = os.path.join(os.path.dirname(__file__),
                              'test_files',
                              'rubocop_config.yaml')


# bad file becomes good and vice-versa
RuboCopBearConfigFileTest = verify_local_bear(
                                RuboCopBear,
                                valid_files=(bad_file,),
                                invalid_files=(good_file,),
                                settings={'rubocop_config': rubocop_config})

# Testing settings
another_good_file = """
def goodindent
 # 1 space indent
end
"""

another_bad_file = """
def badindent
  # 2 spaces indent
end
"""

RuboCopBearSettingsTest = verify_local_bear(
                              RuboCopBear,
                              valid_files=(another_good_file,),
                              invalid_files=(another_bad_file,),
                              settings={'indent_size': 1})

RuboCopBearSettingsTest = verify_local_bear(
                              RuboCopBear,
                              valid_files=(bad_file,),
                              invalid_files=(good_file,),
                              settings={'method_name_case': 'camel'})
