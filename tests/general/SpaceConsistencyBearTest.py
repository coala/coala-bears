from queue import Queue

import coalib.bearlib.aspects as coala_aspects
from bears.general.SpaceConsistencyBear import (
    SpaceConsistencyBear, SpacingHelper)
from coalib.bearlib.aspects.collections import AspectList
from coalib.testing.LocalBearTestHelper import LocalBearTestHelper
from coalib.settings.Section import Section
from coalib.settings.Setting import Setting


class SpaceConsistencyBearTest(LocalBearTestHelper):

    def setUp(self):
        self.section = Section('test section')
        self.section.language = 'Python'
        self.uut = SpaceConsistencyBear(self.section, Queue())

    def test_defaults(self):
        # use_spaces is no default, need to set it explicitly.
        self.section.append(Setting('use_spaces', 'true'))

        self.check_validity(self.uut, ['    t'])
        self.check_invalidity(self.uut, ['\tt'])
        self.check_invalidity(self.uut, ['t \n'])
        self.check_invalidity(self.uut, ['t'],
                              force_linebreaks=False)

    def test_data_sets_spaces(self):
        self.section.append(Setting('use_spaces', 'true'))
        self.section.append(Setting('allow_trailing_whitespace', 'false'))
        self.section.append(Setting('enforce_newline_at_EOF', 'false'))

        self.check_validity(self.uut, ['    t'])
        self.check_invalidity(self.uut, ['t \n'])
        self.check_invalidity(self.uut, ['\tt\n'])

    def test_data_sets_tabs(self):
        self.section.append(Setting('use_spaces', 'false'))
        self.section.append(Setting('allow_trailing_whitespace', 'true'))
        self.section.append(Setting('enforce_newline_at_EOF', 'false'))

        self.check_invalidity(self.uut, ['    t'])
        self.check_validity(self.uut, ['t \n'])
        self.check_validity(self.uut, ['\tt\n'])

    def test_enforce_newline_at_eof(self):
        self.section.append(Setting('use_spaces', 'true'))
        self.section.append(Setting('allow_trailing_whitespace', 'true'))
        self.section.append(Setting('enforce_newline_at_EOF', 'true'))

        self.check_validity(self.uut,
                            ['hello world  \n'],
                            force_linebreaks=False)
        self.check_validity(self.uut,
                            ['def somecode():\n',
                             "    print('funny')\n",
                             "    print('funny end.')\n"],
                            force_linebreaks=False)
        self.check_invalidity(self.uut,
                              [' no hello world'],
                              force_linebreaks=False)
        self.check_invalidity(self.uut,
                              ['def unfunny_code():\n',
                               "    print('funny')\n",
                               "    print('the result is not funny...')"],
                              force_linebreaks=False)

    def test_aspects_space(self):
        self.section.aspects = AspectList([
            coala_aspects['Indentation']('Python', indent_type='space')
        ])

        self.check_validity(self.uut, ['    t'])
        self.check_invalidity(self.uut, ['\tt\n'])

    def test_aspects_tabs(self):
        self.section.aspects = AspectList([
            coala_aspects['Indentation']('Python', indent_type='tab')
        ])

        self.check_invalidity(self.uut, ['   t'])
        self.check_validity(self.uut, ['\tt\n'])

    def test_aspects_tab_size(self):
        self.section.aspects = AspectList([
            coala_aspects['Indentation']('Python',
                                         indent_size=2, indent_type='space')
        ])

        self.check_validity(self.uut,
                            ['def validghost():\n',
                             "  print('boo!')\n"],
                            force_linebreaks=False)
        self.check_invalidity(self.uut,
                              ['def invalidghost():\n',
                               "   print('boo.')\n"],
                              force_linebreaks=False)

    def test_aspects_nondefault(self):
        self.section.aspects = AspectList([
            coala_aspects['NewlineAtEOF']('Python', newline_at_EOF='false')
        ])

        self.check_validity(self.uut, ['t\n'])
        self.check_validity(self.uut, ['t'])
