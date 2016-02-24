from bears.coffee_script.CoffeeLintBear import CoffeeLintBear
from tests.LocalBearTestHelper import verify_local_bear

good_file = """
# Lint your CoffeeScript!

class Gangster

  wasItAGoodDay : () ->
    yes
""".splitlines(keepends=True)


warning_file = """
# Nested string interpolation
str = "Book by #{"#{firstName} #{lastName}".toUpperCase()}"
""".splitlines(keepends=True)


error_file = """
# Wrong capitalization
class theGangster

  wasItAGoodDay : () ->
    yes
""".splitlines(keepends=True)


invalid_file = """
# Coffeelint is buggy here and will generate an error with invalid CSV on this
var test
""".splitlines(keepends=True)


CoffeeLintBearTest = verify_local_bear(CoffeeLintBear,
                                       valid_files=(good_file,),
                                       invalid_files=(warning_file,
                                                      error_file,
                                                      invalid_file))
