from queue import Queue
from textwrap import dedent
from unittest import mock
import sys
import unittest
import shutil
import platform

from coalib.results.Diff import Diff
from coalib.settings.Section import Section
from coalib.testing.LocalBearTestHelper import execute_bear
from coalib.testing.BearTestHelper import generate_skip_decorator

from bears.documentation.DocGrammarBear import DocGrammarBear


def make_docstring(main_desc: str = '',
                   param_desc: str = '',
                   return_desc: str = '',
                   ):
    """
    This assembles a simple docstring having a main description, a parameter
    description and a return description. This makes the tests readibilty
    clean.

    :param main_desc:
        Contains the main description of the docstring.
    :param param_desc:
        Contatins the parameter description of the docstring.
    :param return_desc:
        Contains the return description of the docstring.
    :return:
        Returns an assembled docstring.
    """
    docstring = dedent('"""\n'
                       '{}'
                       '\n'
                       ':param xyz:{}'
                       ':return:{}'
                       '"""\n')
    return docstring.format(main_desc,
                            param_desc,
                            return_desc).splitlines(True)


def gen_check(test_data, expected_data, optional_setting=None):
    def test_function(self):
        arguments = {'language': 'python', 'docstyle': 'default'}
        if optional_setting:
            arguments.update(optional_setting)
        section = Section('test-section')
        for key, value in arguments.items():
            section[key] = value

        with execute_bear(
                DocGrammarBear(section, Queue()),
                'dummy_filename',
                test_data,
                **arguments) as results:

            diff = Diff(test_data)
            for result in results:
                # Only the given test file should contain a patch.
                self.assertEqual(len(result.diffs), 1)

                diff += result.diffs['dummy_filename']

        self.assertEqual(expected_data, diff.modified)

    return test_function


@generate_skip_decorator(DocGrammarBear)
class DocGrammarBearTest(unittest.TestCase):

    def test_check_prerequisites(self):
        _shutil_which = shutil.which
        try:
            shutil.which = lambda *args, **kwargs: None
            self.assertEqual(DocGrammarBear.check_prerequisites(),
                             'java is not installed.')

            shutil.which = lambda *args, **kwargs: 'path/to/java'
            self.assertTrue(DocGrammarBear.check_prerequisites())
        finally:
            shutil.which = _shutil_which

        with mock.patch.dict(sys.modules, {'language_check': None}):
            assert DocGrammarBear.check_prerequisites() == ('Please '
                                                            'install the '
                                                            '`language-check` '
                                                            'pip package.')

    test_spelling = gen_check(
        make_docstring(main_desc='Thiss is main descrpton.\n'),
        make_docstring(main_desc='This is main description.\n'))

    test_capitalize_sentence_start = gen_check(
        make_docstring(main_desc='this sentence starts with small letter\n'),
        make_docstring(main_desc='This sentence starts with small letter\n'))

    test_extra_whitespace = gen_check(
        make_docstring(main_desc='This sentence    has extra  white spaces\n'),
        make_docstring(main_desc='This sentence has extra white spaces\n'))

    test_apostrophe_comma = gen_check(
        make_docstring(main_desc='This sentence doesnt have an apostrophe\n'),
        make_docstring(main_desc='This sentence doesn\'t have an '
                                 'apostrophe\n'))

    correct_docstring = make_docstring(
        main_desc='This documentation has correct grammar.\n',
        param_desc='Dummy description.\n',
        return_desc='Return Nothing.\n')

    test_correct_grammar = gen_check(correct_docstring, correct_docstring)

    test_disable_setting_UPPERCASE_SENTENCE_START = gen_check(
        make_docstring(main_desc='sentence starting with lowercase.\n',
                       param_desc='dummy description.\n',
                       return_desc='Nothing.\n'),
        make_docstring(main_desc='sentence starting with lowercase.\n',
                       param_desc='dummy description.\n',
                       return_desc='Nothing.\n'),
        {'languagetool_disable_rules': 'UPPERCASE_SENTENCE_START'})

    # FRENCH_WHITESPACE adds a unicode space if it finds empty strings.
    # which was breaking this test case.
    test_language_french = unittest.skipIf(
        platform.system() == 'Windows',
        'language-check fails for different locale on windows')(
            gen_check(
                make_docstring(main_desc='il monte en haut si il veut.\n'),
                make_docstring(main_desc='Il monte s’il veut.\n'),
                {'locale': 'fr',
                 'languagetool_disable_rules': 'FRENCH_WHITESPACE'}))

    # explicit language test cases to check the breakage of DocGrammarBear.
    test_java_explicit = gen_check([
        'class Square {\n',
        '    /**\n',
        '     * Returnss Area of a square.\n',
        '     *\n',
        '     *@param  side side of squaree\n',
        '     *@return  area of a square\n',
        '     */\n',
        '    public int Area(int side) {\n',
        '        return side * side;\n'
        '    }\n',
        '}'], [
        'class Square {\n',
        '    /**\n',
        '     * Returns Area of a square.\n',
        '     *\n',
        '     *@param  side Side of square\n',
        '     *@return  Area of a square\n',
        '     */\n',
        '    public int Area(int side) {\n',
        '        return side * side;\n'
        '    }\n',
        '}'],
        {'language': 'java'})

    test_python_explicit = gen_check([
        'def improper_grammar(param1):\n',
        '    """\n',
        '    Documntation contains gramatical mistakess.DocGrammarBear\n',
        '    doesnt check for style.\n',
        '    :param param1: Contains parameter descrption.\n',
        '    :return: returns nothing. first letter small.\n',
        '    """\n',
        '    return None'], [
        'def improper_grammar(param1):\n',
        '    """\n',
        '    Documentation contains grammatical mistakes. DocGrammarBear\n',
        '    doesn\'t check for style.\n',
        '    :param param1: Contains parameter description.\n',
        '    :return: Returns nothing. First letter small.\n',
        '    """\n',
        '    return None'])
