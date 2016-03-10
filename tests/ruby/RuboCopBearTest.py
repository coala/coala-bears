from bears.ruby.RuboCopBear import RuboCopBear
from tests.LocalBearTestHelper import verify_local_bear

good_file = """def bad_name
  test if something
end
""".splitlines(keepends=True)

bad_file = """def badName
  if something
    test
    end
end
""".splitlines(keepends=True)


RuboCopBearTest = verify_local_bear(RuboCopBear,
                                    invalid_files=(bad_file,),
                                    valid_files=(good_file,))
