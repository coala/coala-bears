from bears.ruby.RubyLinterBear import RubyLinterBear
from tests.LocalBearTestHelper import verify_local_bear

good_file = """
class HelloWorld
    def initialize(name)
        @name = name.capitalize
    end
    def sayHi
        puts "Hello #{@name}!"
    end
end
""".splitlines(keepends=True)


bad_file = """
class HelloWorld
    def initialize(name)
        @name = name.capitalize
    end
    def sayHi
        x = 1 # unused variables invoke a warning
        puts "Hello #{@name}!"
    end
""".splitlines(keepends=True)


RubyLinterBearTest = verify_local_bear(RubyLinterBear,
                                       valid_files=(good_file,),
                                       invalid_files=(bad_file,))
