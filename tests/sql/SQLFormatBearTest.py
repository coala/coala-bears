from queue import Queue

from bears.sql.SQLFormatBear import SQLFormatBear
from coalib.testing.LocalBearTestHelper import LocalBearTestHelper
from coalib.settings.Section import Section
from coalib.settings.Setting import Setting


class SQLFormatBearTest(LocalBearTestHelper):

    def setUp(self):
        self.section = Section('name')
        self.uut = SQLFormatBear(self.section, Queue())

    def test_valid(self):
        self.check_validity(self.uut, ['SELECT *\n',
                                       'FROM tablename;\n',
                                       '\n'])

    def test_keyword_case(self):
        self.section.append(Setting('keyword_case', 'lower'))
        self.check_invalidity(self.uut, ['SELECT *\n',
                                         'FROM tablename;\n',
                                         '\n'])
        self.check_validity(self.uut, ['select *\n',
                                       'from tablename;\n',
                                       '\n'])

    def test_identifier_case(self):
        self.section.append(Setting('identifier_case', 'upper'))
        self.check_invalidity(self.uut, ['SELECT *\n',
                                         'FROM tablename;\n',
                                         '\n'])
        self.check_validity(self.uut, ['SELECT *\n',
                                       'FROM TABLE;\n',
                                       '\n'])

    def test_strip_comments(self):
        test_code = ['/* comment */\n',
                     'SELECT *\n',
                     'FROM tablename;\n',
                     '\n']
        self.check_validity(self.uut, test_code)
        self.section.append(Setting('strip_comments', 'True'))
        self.check_invalidity(self.uut, test_code)

    def test_reindent(self):
        test_code = ['SELECT * FROM tablename']
        self.check_invalidity(self.uut, test_code)

    def test_indent_tabs(self):
        test_code = ['SELECT *\n',
                     'FROM tablename\n',
                     'WHERE teacher IN\n',
                     '\t\t(SELECT *\n',
                     '\t\t\tFROM this);\n',
                     '\n']
        self.check_invalidity(self.uut, test_code)
        self.section.append(Setting('indent_tabs', 'True'))
        self.section.append(Setting('indent_width', '1'))
        self.check_validity(self.uut, test_code)

    def test_indent_width(self):
        test_code = ['SELECT *\n',
                     'FROM tablename\n',
                     'WHERE that IN\n',
                     '    (SELECT *\n',
                     '     FROM this);\n',
                     '\n']
        self.check_invalidity(self.uut, test_code)
        self.section.append(Setting('indent_width', '2'))
        self.check_validity(self.uut, test_code)
