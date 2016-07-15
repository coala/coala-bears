import unittest
from queue import Queue
import os

from bears.general.IndentationBear import IndentationBear
from bears.general.AnnotationBear import AnnotationBear
from coala_utils.string_processing.Core import escape
from coalib.settings.Section import Section
from coalib.settings.Setting import Setting


class IndentationBearTest(unittest.TestCase):

    def setUp(self):
        self.section = Section("")
        self.section.append(Setting('language', 'test'))
        self.section.append(Setting('use_spaces', False))
        self.section.append(Setting('coalang_dir', escape(os.path.join(
            os.path.dirname(__file__), "test_files"), '\\')))
        self.dep_uut = AnnotationBear(self.section, Queue())

    def get_results(self, file, section=None):
        if section is None:
            section = self.section
        dep_results_valid = self.dep_uut.execute("file", file)
        uut = IndentationBear(section, Queue())
        arg_dict = {'dependency_results':
                    {AnnotationBear.__name__:
                     list(dep_results_valid)},
                    'file': file}
        return list(uut.run_bear_from_section(["file"], arg_dict))

    def verify_bear(self,
                    valid_file=None,
                    invalid_file=None,
                    section=None):
        if valid_file:
            valid_results = self.get_results(valid_file, section)
            self.assertEqual(valid_results, [])

        if invalid_file:
            invalid_results = self.get_results(invalid_file, section)
            self.assertNotEqual(invalid_results, [])

    def test_basic_indent(self):
        valid_file =\
            ("{\n",
             "\tright indent\n",
             "}\n")
        invalid_file =\
            ("{\n",
             "wrong indent\n",
             "}\n")
        self.verify_bear(valid_file, invalid_file)

        valid_file2 =\
            ("a {\n",
             "\tindent1\n",
             "\tindent2\n",
             "}\n")

        invalid_file2 =\
            ("a {\n",
             "\tindentlevel1;\n",
             "\t\tsecondlinehere;\n",
             "}\n")
        self.verify_bear(valid_file2, invalid_file2)

    def test_within_strings(self):
        valid_file1 =\
            ('"indent specifier within string{"\n',
             'does not indent\n')
        self.verify_bear(valid_file1)

        valid_file2 =\
            ('R("strings can span\n',
             'multiple lines as well{")\n',
             'but the bear works correctly\n')
        self.verify_bear(valid_file2)

        valid_file3 =\
            ('"this should indent"{ "hopefully"\n',
             '\tand it does\n',
             '}\n')
        self.verify_bear(valid_file3)

    def test_within_comments(self):
        valid_file1 =\
            ('//indent specifier within comments{\n',
             'remains unindented\n')
        self.verify_bear(valid_file1)

        valid_file2 =\
            ('/*Indent specifier within\n',
             'lines of multiline comment {\n',
             'doesnt have any effect{ */\n',
             'no affect on regular lines as well\n')
        self.verify_bear(valid_file2)

        valid_file3 =\
            ('/*this should indent*/{ /*hopefully*/\n',
             '\tand it does\n',
             '}\n')
        self.verify_bear(valid_file3)

    def test_branch_indents(self):
        valid_file =\
            ('branch indents{\n',
             '\tsecond branch{\n',
             '\t\twithin second branch\n',
             '\t}\n',
             '}\n',)
        self.verify_bear(valid_file)

    def test_bracket_matching(self):
        valid_file = ("{{{}{}}",
                      "\tone_indent",
                      "}")
        invalid_file = ("{{{}{}}",
                        "did not give indent",
                        "}")
        self.verify_bear(valid_file, invalid_file)

        invalid_file = ('}}}{{{\n',)
        self.verify_bear(invalid_file=invalid_file)

    def test_blank_lines(self):
        valid_file = ("{ trying indent",
                      "\n",
                      "\tIndents even after blank line}")
        invalid_file = ("{ trying indent",
                        "\n",
                        "should have Indented after blank line}")
        self.verify_bear(valid_file, invalid_file)

        valid_file = ('def func(x):\n',
                      '\tlevel1\n',
                      '\n',
                      'level0\n')
        self.verify_bear(valid_file)

    def test_settings(self):
        section = Section("")
        section.append(Setting('language', 'c'))
        section.append(Setting('use_spaces', True))
        section.append(Setting('tab_width', 6))
        valid_file = ('{\n',
                      # Start ignoring SpaceConsistencyBear
                      '      6 spaces of indentation\n'
                      # Stop ignoring
                      '}\n')

        invalid_file = ('{\n',
                        # Start ignoring SpaceConsistencyBearW
                        '    4 spaces of indentation\n'
                        # Stop ignoring
                        '}\n')
        self.verify_bear(valid_file, invalid_file, section)

    def test_unmatched_indents(self):
        valid_file = ('{}\n',)
        invalid_file = ('{\n',)
        self.verify_bear(valid_file, invalid_file)

        invalid_file2 = ('{}}\n',)
        self.verify_bear(valid_file=None, invalid_file=invalid_file2)

    def test_multiple_indent_specifiers(self):
        valid_file = ('{<\n',
                      '\t\tdouble indents\n',
                      '\t>\n',
                      '\tother specifier closes\n',
                      '}\n')
        invalid_file = ('{\n',
                        '\t<\n',
                        '\t not giving indentation>}\n')
        self.verify_bear(valid_file, invalid_file)

    def test_unspecified_unindents(self):
        valid_file = ('switch(expression) {\n',
                      '\tcase constant-expression  :\n',
                      '\t\tstatement(s);\n',
                      '\t\tbreak;\n',
                      '\tcase constant-expression  :\n',
                      '\t\tstatement(s);\n',
                      '\t\tbreak;\n',
                      '\tdefault :\n',
                      '\t\tstatement(s);\n',
                      '}\n')
        invalid_file = ('switch(expression){\n',
                        '\tcase expr:\n',
                        '\tstatement(s);\n',
                        '}')
        self.verify_bear(valid_file, invalid_file)

        valid_file = ('def func(x,\n',
                      '         y,\n',
                      '         z):\n',
                      '\tsome line\n',
                      '\tsome line 2\n')
        invalid_file = ('def func(x):\n',
                        '\t\tsome line\n',
                        '\tsome line\n')
        self.verify_bear(valid_file, invalid_file)

        invalid_file = ('def func(x):\n',
                        '\tline 1\n',
                        '# A comment')
        self.verify_bear(invalid_file=invalid_file)

        invalid_file = ('def func(x):\n',
                        '\ta = [1, 2,\n',
                        '3, 4]\n')
        self.verify_bear(invalid_file=invalid_file)

        invalid_file = ('def func(x):\n',
                        '\t/* multiline comment\n',
                        'unindent*/')
        self.verify_bear(invalid_file=invalid_file)

    def test_absolute_indentation(self):
        valid_file =\
            ("some_function(param1,\n",
             "              second_param,\n",
             "              third_one)\n",
             "indent back to normal\n")

        invalid_file =\
            ("some_function(param1,\n",
             "              param2)\n",
             "              wrong_indent\n")

        self.verify_bear(valid_file=valid_file, invalid_file=invalid_file)

        valid_file = \
            ("branched_function(param1,\n",
             "                  param2_func(param3,\n",
             "                              param4)\n",
             "                  param5)\n",
             "indent back to original\n")

        invalid_file = \
            ("some_function(param1\n",
             "              param2(param3,\n",
             "                     param4))\n",
             "              wrong indent\n")

        self.verify_bear(valid_file=valid_file, invalid_file=invalid_file)

        valid_file =\
            ("some_function(param1{\n",
             "              \tshould be here\n",
             "              }\n",
             "              param2)\n")

        invalid_file =\
            ("some_function(param1{\n",
             "                     \tis this right?\n",
             "                     }\n",
             "              probably not)\n")

        self.verify_bear(valid_file=valid_file, invalid_file=invalid_file)

        valid_file =\
            ("some_function(\n",
             "         does hanging indents\n"
             "         so can indent like this)\n")

        self.verify_bear(valid_file)

    def test_invalid_specifiers(self):
        valid_file = ("not a valid : indent specifier\n",
                      "does not indent\n")
        invalid_file = ("not a valid : indent specifier\n",
                        "\tindents\n")
        self.verify_bear(valid_file, invalid_file)

        valid_file = ("[a specifier :\n",
                      " inside an encapsulator]\n",
                      "is not valid")
        self.verify_bear(valid_file)

        valid_file = ("This is a valid specifier: # A comment\n",
                      "\tand so it indents\n")
        self.verify_bear(valid_file)
