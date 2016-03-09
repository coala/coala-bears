from bears.ruby.RuboCopBear import RuboCopBear
from tests.LocalBearTestHelper import verify_local_bear

good_file = """arr = [1, 2, 3]
# good
arr.each { |elem| puts elem }""".splitlines(keepends=True)


bad_file = """arr = [1, 2, 3]
# bad
for elem in arr do
  puts elem
end""".splitlines(keepends=True)


RuboCopBearTest = verify_local_bear(RuboCopBear,
                                    valid_files=(good_file,),
                                    invalid_files=(bad_file,))
