from bears.coffee_script.CoffeeLintBear import CoffeeLintBear
from coalib.testing.LocalBearTestHelper import verify_local_bear

good_file = """
# Lint your CoffeeScript!

class Gangster

  wasItAGoodDay : () ->
    yes
"""


good_file_use_english_operator = """
1 or 1
1 and 1
1 isnt 1
1 is 1
"""


bad_file_use_english_operator = """
1 || 1
1 && 1
1 != 1
1 == 1
x = !y
"""


good_file_no_duplicate_keys = """
class SomeThing
  getConfig: ->
    @config =
      foo: 1
  @getConfig: ->
    config =
      foo: 1
"""


bad_file_no_duplicate_keys = """
class SomeThing
  getConfig: ->
    one = 1
    one = 5
    @config =
      keyA: one
      keyB: one
      keyA: 2
  getConfig: ->
    @config =
      foo: 1
  @getConfig: ->
    config =
      foo: 1"""


good_file_tab_width = """
# Lint your CoffeeScript!

class Gangster

    wasItAGoodDay : () ->
        yes
"""


good_file_allow_trailing_white_spaces = """
x = 1234
y = 1
"""


bad_file_allow_trailing_white_spaces = """
x = 1234      \ny = 1
"""


good_file_arrow_spacing = """
x(-> 3)
x( -> 3)
"""


bad_file_arrow_spacing = """
{x((a,b)-> 3)
"""


good_file_no_backticks = """
myFunction(a, b, c)
"""


bad_file_no_backticks = """
`myFunction a,b,c
"""


good_file_allow_trailing_semiColon = """
x = '1234'; console.log(x)
{spacing:true}
"""


bad_file_allow_trailing_semiColon = """
alert('end of line');
"""


good_file_no_empyty_functions_and_parameter_list = """
foo = (empty = (-> undefined)) -> undefined
{  a, b  }
{  }
foo = 'bar'
{  spacing : true  }
"""


bad_file_no_empyty_functions_and_parameter_list = """
-> =>
blah = () ->
y++
--x
{a, b}
{}
foo = "bar"
{spacing:true}
"""


good_file_disable_throwing_strings = """
x++;
x+=1
doSomething(foo = ',',bar)
myFunction a, b, {1:2, 3:4}
`with(document) alert(height);`
foo = "#{inter}foo#{polation}"
@::
"""


bad_file_disable_throwing_strings = """
throw 'my error'
throw "#{1234}"
throw '''
  long string
'''
foo = '#{inter}foo#{polation}'
myFunction a, b, 1:2, 3:4
"""


good_file_no_stand_alone_at_sign = """
@[ok]
@ok()
doSomething(foo = ',', bar)\nfooBar()
c = new Foo 1, 2
throw 'my error'
throw "#{1234}"
"""


bad_file_no_stand_alone_at_sign = """
@ notok
not(@).ok
@::
doSomething(foo = ',',bar)\nfooBar()
"""


good_file_no_this = """
class Y extends X
  constructor: ->
    @.hello
"""


bad_file_no_this = """
class Y extends X
  constructor: ->
    this.hello
"""


good_file_enforce_parentheses_on_constructors = """
g = new Foo(1, 2)
h = new Foo(
  config: 'parameter'
)
i = new bar.foo.Foo(1, 2)
j = new bar.foo.Foo(
  config: 'parameter'
)
myFunction a, b, 1:2, 3:4
foo = '#{bar}'
"""


bad_file_enforce_parentheses_on_constructors = """
c = new Foo 1, 2
d = new Foo
  config: 'parameter'
e = new bar.foo.Foo 1, 2
f = new bar.foo.Foo
  config: 'parameter'
"""


good_file_new_lines_after_classes = """
class Foo
  constructor: () ->
    bla()
  a: "b"
  c: "d"

class Bar extends Foo
  constructor: () ->
    bla()
"""


bad_file_new_lines_after_classes = """
class Foo
  constructor: () ->
      bla()
  a: "b"
  c: "d"
class Bar extends Foo
  constructor: () ->
    bla()
"""


bad_file_cyclomatic_complexity = """
x = () ->
  a = () ->
    1 or 2
"""


good_file_cyclomatic_complexity = """
x = () -> 1234
"""


warning_file = """
# Nested string interpolation
str = "Book by #{"#{firstName} #{lastName}".toUpperCase()}"
"""


error_file = """
# Wrong capitalization
class theGangster

  wasItAGoodDay : () ->
    yes
"""


invalid_file = """
# Coffeelint is buggy here and will generate an error with invalid CSV on this
var test
"""

infinite_line_length_file = """# File to check long line length support
""" + 'number   = 42; ' * 1000 + """number   = 42
console.log number
"""

CoffeeLintBearTest = verify_local_bear(CoffeeLintBear,
                                       valid_files=(good_file,),
                                       invalid_files=(warning_file,
                                                      error_file,
                                                      invalid_file))


CoffeeLintBearUseEnglishOperatorTest = verify_local_bear(
    CoffeeLintBear,
    valid_files=(good_file_use_english_operator,),
    invalid_files=(bad_file_use_english_operator,),
    settings={'allow_bitwise_operators': 'false',
              'consistent_line_endings_style': 'unix'})


CoffeeLintBearTabWidthTest = verify_local_bear(
    CoffeeLintBear,
    valid_files=(good_file_tab_width,),
    invalid_files=(good_file,),
    settings={'use_spaces': 'false', 'indent_size': 4})


CoffeeLintBearNoDuplicateKeysTest = verify_local_bear(
    CoffeeLintBear,
    valid_files=(good_file_no_duplicate_keys,),
    invalid_files=(bad_file_no_duplicate_keys,),
    settings={'prevent_duplicate_keys': 'true',
              'enforce_newline_at_EOF': 'true'})


CoffeeLintBearCamelCaseTest = verify_local_bear(
    CoffeeLintBear,
    valid_files=(good_file,),
    invalid_files=(error_file,),
    settings={'class_naming_camelCase': 'true'})


CoffeeLintBearAllowTrailingWhiteSpacesTest = verify_local_bear(
    CoffeeLintBear,
    valid_files=(good_file_allow_trailing_white_spaces,),
    invalid_files=(bad_file_allow_trailing_white_spaces,),
    settings={'allow_trailing_whitespaces': 'false',
              'allow_bitwise_operators': 'false',
              'spaces_around_operators': 'true'})


CoffeLintBearArrowSpacingTest = verify_local_bear(
    CoffeeLintBear,
    valid_files=(good_file_arrow_spacing,),
    invalid_files=(bad_file_arrow_spacing,),
    settings={'space_before_and_after_arrow': 'true'})


CoffeeLintBearNoBackticksTest = verify_local_bear(
    CoffeeLintBear,
    valid_files=(good_file_no_backticks,),
    invalid_files=(bad_file_no_backticks,),
    settings={'prohibit_embedding_javascript_snippet': 'true',
              'space_after_comma': 'true',
              'no_function_call_without_parentheses': 'true'})


CoffeeLintBearAllowTrailingSemiColonTest = verify_local_bear(
    CoffeeLintBear,
    valid_files=(good_file_allow_trailing_semiColon,),
    invalid_files=(bad_file_allow_trailing_semiColon,),
    settings={'allow_trailing_semicolons': 'false'})


CoffeeLintBearNoEmpytyFunctionsAndParameterListTest = verify_local_bear(
    CoffeeLintBear,
    valid_files=(good_file_no_empyty_functions_and_parameter_list,),
    invalid_files=(bad_file_no_empyty_functions_and_parameter_list,),
    settings={'allow_empty_functions': 'true',
              'allow_no_parameters': 'true',
              'allow_increment': 'false',
              'check_braces_spacing': 'true',
              'braces_spacing_width': 2,
              'spacing_in_empty_braces': 2,
              'allow_unnecessary_double_quotes': 'false',
              'spaces_before_and_after_colon': 'true',
              'spaces_before_colon': 1,
              'allow_implicit_parentheses': 'false'})


CoffeeLintBearDisableThrowingStringsTest = verify_local_bear(
    CoffeeLintBear,
    valid_files=(good_file_disable_throwing_strings,),
    invalid_files=(bad_file_disable_throwing_strings,),
    settings={'allow_throwing_strings': 'false',
              'allow_trailing_semicolons': 'true',
              'allow_trailing_whitespaces': 'true',
              'spaces_around_operators': 'false',
              'space_after_comma': 'false',
              'force_braces': 'true',
              'allow_implicit_parentheses': 'true',
              'prohibit_embedding_javascript_snippet': 'false',
              'allow_interpolation_in_single_quotes': 'false',
              'allow_stand_alone_at_sign': 'true'})


CoffeeLintBearNoStandAloneAtTest = verify_local_bear(
    CoffeeLintBear,
    valid_files=(good_file_no_stand_alone_at_sign, bad_file_no_duplicate_keys),
    invalid_files=(bad_file_no_stand_alone_at_sign,),
    settings={'allow_stand_alone_at_sign': 'false',
              'space_after_comma': 'true',
              'enforce_parentheses_on_non_empty_constructors': 'false',
              'prevent_duplicate_keys': 'false',
              'allow_throwing_strings': 'true'})


CoffeeLintBearNoThisTest = verify_local_bear(
    CoffeeLintBear,
    valid_files=(good_file_no_this,),
    invalid_files=(bad_file_no_this,),
    settings={'allow_this_statements': 'false',
              'class_naming_camelCase': 'false'})


CoffeeLintBearEnforceParenthesesOnConstructorsTest = verify_local_bear(
    CoffeeLintBear,
    valid_files=(good_file_enforce_parentheses_on_constructors,),
    invalid_files=(bad_file_enforce_parentheses_on_constructors,),
    settings={'enforce_parentheses_on_non_empty_constructors': 'true',
              'no_function_call_without_parentheses': 'false',
              'allow_interpolation_in_single_quotes': 'true'})


CoffeeLintBearNewLinesAfterClassesTest = verify_local_bear(
    CoffeeLintBear,
    valid_files=(good_file_new_lines_after_classes,),
    invalid_files=(bad_file_new_lines_after_classes,),
    settings={'number_of_newlines_after_classes': 1})


CoffeeLintBearCyclomaticComplexityTest = verify_local_bear(
    CoffeeLintBear,
    valid_files=(good_file_cyclomatic_complexity,),
    invalid_files=(bad_file_cyclomatic_complexity,),
    settings={'cyclomatic_complexity': 1})


CoffeeLintBearInfiniteLineLengthTest = verify_local_bear(
    CoffeeLintBear,
    valid_files=(infinite_line_length_file,),
    invalid_files=(),
    settings={'max_line_length': 0})
