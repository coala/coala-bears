import os

from bears.ruby.RuboCopBear import RuboCopBear
from tests.LocalBearTestHelper import verify_local_bear

good_file = """def good_name
  test if something
end
""".splitlines(keepends=True)

bad_file = """def badName
  test if something
end
""".splitlines(keepends=True)


RuboCopBearTest = verify_local_bear(RuboCopBear,
                                    invalid_files=(bad_file,),
                                    valid_files=(good_file,))

# Testing Config
rubocop_config = os.path.join(os.path.dirname(__file__),
                              "test_files",
                              "rubocop_config.yml")


# bad file becomes good and vice-versa
RuboCopBearConfigFileTest = verify_local_bear(
                                RuboCopBear,
                                valid_files=(bad_file,),
                                invalid_files=(good_file,),
                                settings={"rubocop_config": rubocop_config})
