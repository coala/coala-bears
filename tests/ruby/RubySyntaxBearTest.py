from bears.ruby.RubySyntaxBear import RubySyntaxBear
from coalib.testing.LocalBearTestHelper import verify_local_bear

good_file = """
class HelloWorld
    def initialize(name)
        @name = name.capitalize
    end
    def sayHi
        puts "Hello #{@name}!"
    end
end
"""


bad_file = """
class HelloWorld
    def initialize(name)
        @name = name.capitalize
    end
    def sayHi
        x = 1 # unused variables invoke a warning
        puts "Hello #{@name}!"
    end
"""


RubySyntaxBearTest = verify_local_bear(RubySyntaxBear,
                                       valid_files=(good_file,),
                                       invalid_files=(bad_file,))
