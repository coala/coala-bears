from tests.LocalBearTestHelper import verify_local_bear
from bears.general.IndentationBear import IndentationBear


IndentationBearTest = verify_local_bear(
    IndentationBear,
    valid_files=(
        ("{",
         "\tright indent",
         "}"),

        ('"indent withinstring{"',
         'No indent'),

        ('//indent within comments{',
         'remains unindented',),

        ('/*Indent within',
         'lines of multiline comment {',
         'doesnt have any effect{ */',
         'no affect on regular lines as well'),

        ('"strings can span ',
         'multiple lines as well{"'
         'but the bear works correctly'),

        ('branch indents{',
         '\tsecond branch{',
         '\t\twithin second branch',
         '\t}',
         '}',),

        ('/*this should indent*/{ /*hopefully*/',
         '\tand it does'),

        ("some_function(param1,",
         "              second_param,",
         "              third_one)",
         "indent back to normal"),

        ("branched_function(param1,"
         "                  param2_func(param3,"
         "                              param4)"
         "                  param5)",
         "indent back to original"),

        ("some_function(param1{"
         "              \tshould be here"
         "              }",
         "              param2)"),

        ("{{{\}{\}}",
         "\tone_indent",),

        ("some_function(param1",
         "              param2(param3,"
         "                     param4))",
         "right indent"),

        ("some_function(param1,",
         "                     ",
         "              param2)",
         "blank line test"),

        ("{ trying indent",
         "    ",
         "\tIndents even after blank line}"),

        ("a {",
         "\tindent1",
         "\tindent2",
         "}"),),

    invalid_files=(
        ("{",
         "wrong indent",
         "}"),

        ("some_function(param1,",
         "\twrongly_indented_param)"),

        ('"valid indent" { "between strings"',
         "unindent should give results",),

        ("some_function(param1,",
         "              param2)",
         "              wrong_indent"),

        ("some_function(param1{",
         "                     \tis this right?",
         "                     }",
         "              probably not)"),

        ("{ this shouldnt increase indent\}",
         "\tdoes it?"),

        ("some_function(",
         "         doesnt do hanging indents"
         "         so cant indent like this)"),

        ("some_function(param1",
         "              param2(param3,",
         "                     param4))",
         "              wrong indent"),

        ('"let us see if \\" this indents{"',
         "\thope it doesnt"),

        ("a {",
         "\tindentlevel1;",
         "\t\tsecondlinehere;",
         "}"),),

    settings={'language': 'C',
              'language_family': "C", })
