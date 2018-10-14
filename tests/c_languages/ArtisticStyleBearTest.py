from queue import Queue

from bears.c_languages.ArtisticStyleBear import ArtisticStyleBear
from coalib.settings.Section import Section
from coalib.settings.Setting import Setting
from coalib.testing.LocalBearTestHelper import LocalBearTestHelper
from coalib.testing.BearTestHelper import generate_skip_decorator


@generate_skip_decorator(ArtisticStyleBear)
class ArtisticStyleBearTest(LocalBearTestHelper):

    def setUp(self):
        self.section = Section('name')
        self.uut = ArtisticStyleBear(self.section, Queue())

    def test_attach_braces_to_namespace(self):
        good_file = ['namespace FooName {\n',
                     '}\n']
        self.check_validity(self.uut, good_file)

        bad_file = ['namespace FooName\n',
                    '{\n',
                    '}\n']
        self.check_invalidity(self.uut, bad_file)

    def test_attach_braces_to_class(self):
        good_file = ['class FooName {\n',
                     '}\n']
        self.check_validity(self.uut, good_file)

        bad_file = ['class FooName\n',
                    '{\n',
                    '}\n']
        self.check_invalidity(self.uut, bad_file)

    def test_indent_classes(self):
        self.section.append(Setting('require_braces_at_class', False))
        good_file = ['class Foo\n',
                     '{\n',
                     '    public:\n',
                     '        Foo();\n',
                     '        virtual ~Foo();\n',
                     '};\n']
        self.check_validity(self.uut, good_file)

        bad_file = ['class Foo\n',
                    '{\n',
                    'public:\n',
                    '    Foo();\n',
                    '    virtual ~Foo();\n',
                    '};\n']
        self.check_invalidity(self.uut, bad_file)

    def test_indent_cases(self):
        self.section.append(Setting('allow_indent_switches', False))
        self.section.append(Setting('allow_pad_header_blocks', False))
        good_file = ['switch (foo)\n',
                     '{\n',
                     'case 1:\n',
                     '    a += 1;\n',
                     '    break;\n',
                     '\n',
                     'case 2:\n',
                     '    {\n',
                     '        a += 2;\n',
                     '        break;\n',
                     '    }\n',
                     '}\n']
        self.check_validity(self.uut, good_file)

        bad_file = ['switch (foo)\n',
                    '{\n',
                    'case 1:\n',
                    '    a += 1;\n',
                    '    break;\n',
                    '\n',
                    'case 2:\n',
                    '{\n',
                    '    a += 2;\n',
                    '    break;\n',
                    '}\n',
                    '}\n']
        self.check_invalidity(self.uut, bad_file)

    def test_indent_namespaces(self):
        self.section.append(Setting('require_braces_at_class', False))
        self.section.append(Setting('require_braces_at_namespace', False))
        self.section.append(Setting('allow_indent_namespaces', True))
        good_file = ['namespace foospace\n',
                     '{\n',
                     '    class Foo\n',
                     '    {\n',
                     '        public:\n',
                     '            Foo();\n',
                     '            virtual ~Foo();\n',
                     '    };\n',
                     '}\n']
        self.check_validity(self.uut, good_file)

        bad_file = ['namespace foospace\n',
                    '{\n',
                    'class Foo\n',
                    '{\n',
                    '    public:\n',
                    '        Foo();\n',
                    '        virtual ~Foo();\n',
                    '};\n',
                    '}\n']
        self.check_invalidity(self.uut, bad_file)

    def test_indent_preproc_block(self):
        good_file = ['#ifdef _WIN32\n',
                     '    #include <windows.h>\n',
                     '    #ifndef NO_EXPORT\n',
                     '        #define EXPORT\n',
                     '    #endif\n',
                     '#endif\n']
        self.check_validity(self.uut, good_file)

        bad_file = ['#ifdef _WIN32\n',
                    '#include <windows.h>\n',
                    '#ifndef NO_EXPORT\n',
                    '#define EXPORT\n',
                    '#endif\n',
                    '#endif\n']
        self.check_invalidity(self.uut, bad_file)

    def test_pad_operators(self):
        self.section.append(Setting('allow_pad_header_blocks', False))
        good_file = ['if (foo == 2)\n',
                     '    a = bar((b - c) * a, d--);\n']
        self.check_validity(self.uut, good_file)

        bad_file = ['if (foo==2)\n',
                    '    a=bar((b-c)*a,d--);\n']
        self.check_invalidity(self.uut, bad_file)

    def test_pad_parenthesis(self):
        self.section.append(Setting('allow_pad_header_blocks', False))
        self.section.append(Setting('allow_pad_parenthesis', True))
        good_file = ['if ( isFoo ( ( a + 2 ), b ) )\n',
                     '    bar ( a, b );\n']
        self.check_validity(self.uut, good_file)

        bad_file = ['if (isFoo((a+2), b))\n',
                    '    bar(a, b);\n']
        self.check_invalidity(self.uut, bad_file)

    def test_delete_empty_lines_in_func(self):
        self.section.append(Setting('delete_empty_lines_in_func', True))
        good_file = ['void Foo()\n',
                     '{\n',
                     '    foo1 = 1;\n',
                     '    foo2 = 2;\n',
                     '}\n']
        self.check_validity(self.uut, good_file)

        bad_file = ['void Foo()\n',
                    '{\n',
                    '\n'
                    '    foo1 = 1;\n',
                    '\n'
                    '    foo2 = 2;\n',
                    '\n'
                    '}\n']
        self.check_invalidity(self.uut, bad_file)

    def test_require_braces_at_one_line_conditionals(self):
        self.section.append(Setting('require_braces_at_one_line_conditionals',
                                    True))
        self.section.append(Setting('allow_pad_header_blocks', False))
        good_file = ['if (isFoo) {\n',
                     '    isFoo = false;\n',
                     '}\n']
        self.check_validity(self.uut, good_file)

        bad_file = ['if (isFoo)\n',
                    '    isFoo = false;\n']
        self.check_invalidity(self.uut, bad_file)

    def test_bracket_style(self):
        self.section.append(Setting('bracket_style', 'google'))
        good_file = ['int Foo(bool isBar) {\n',
                     '    if (isBar) {\n',
                     '        bar();\n',
                     '        return 1;\n',
                     '    } else\n',
                     '        return 0;\n',
                     '}\n']
        self.check_validity(self.uut, good_file)

        bad_file = ['int Foo(bool isBar)\n'
                    '{\n',
                    '    if (isBar)\n'
                    '        {\n',
                    '            bar();\n',
                    '            return 1;\n',
                    '        }\n'
                    '    else\n',
                    '        return 0;\n',
                    '}\n']
        self.check_invalidity(self.uut, bad_file)

    def test_indentation_spaces(self):
        self.section.append(Setting('use_spaces', True))
        self.section.append(Setting('indent_size', 3))
        good_file = ['void Foo() {\n',
                     '   if (isBar1\n',
                     '         && isBar2)\n',
                     '      bar();\n']
        self.check_validity(self.uut, good_file)

        bad_file = ['void Foo() {\n',
                    '    if (isBar1\n',
                    '            && isBar2)\n',
                    '        bar();\n']
        self.check_invalidity(self.uut, bad_file)

    def test_indentation_tabs(self):
        self.section.append(Setting('use_spaces', False))
        bad_file = ['void Foo() {\n',
                    '    if (isBar1\n',
                    '            && isBar2)\n',
                    '        bar();\n']
        self.check_invalidity(self.uut, bad_file)
