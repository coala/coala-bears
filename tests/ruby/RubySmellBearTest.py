from bears.ruby.RubySmellBear import RubySmellBear
from tests.LocalBearTestHelper import verify_local_bear


good_file = """# Does something
class Something;
end
""".splitlines(True)

bad_file = ('class Something; end',)


RubySmellBearTest = verify_local_bear(RubySmellBear,
                                      valid_files=(good_file, ('',)),
                                      invalid_files=(bad_file,))

RubySmellBearConfigTest = verify_local_bear(
    RubySmellBear, valid_files=(good_file, bad_file), invalid_files=(),
    settings={'missing_module_description': "nope"})
