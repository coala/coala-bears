import os
from queue import Queue

from coalib.settings.Section import Section
from coalib.settings.Setting import Setting
from coalib.testing.LocalBearTestHelper import LocalBearTestHelper
from coalib.testing.BearTestHelper import generate_skip_decorator

from bears.css.CSSCombBear import CSSCombBear


@generate_skip_decorator(CSSCombBear)
class CSSCombBearTest(LocalBearTestHelper):

    def setUp(self):
        self.section = Section('name')
        self.uut = CSSCombBear(self.section, Queue())

    def test_enforce_semicolon(self):
        good_file = ['a { color: red; text-decoration: underline; }']
        self.check_validity(self.uut, good_file)

        bad_file = ['a { color: red; text-decoration: underline }']
        self.check_invalidity(self.uut, bad_file)

    def test_color_case(self):
        good_file = ['a { color: #FFF; }']
        self.check_validity(self.uut, good_file)

        bad_file = ['a { color: #fff; }']
        self.check_invalidity(self.uut, bad_file)

    def test_color_shorthand(self):
        self.section.append(Setting('allow_color_shorthand', False))
        good_file = ['b { color: #FFCC00; }']
        self.check_validity(self.uut, good_file)

        bad_file = ['b { color: #FC0; }']
        self.check_invalidity(self.uut, bad_file)

    def test_leading_zero_in_dimensions(self):
        good_file = ['p { padding: 0.5em; }']
        self.check_validity(self.uut, good_file)

        bad_file = ['p { padding: .5em; }']
        self.check_invalidity(self.uut, bad_file)

    def test_preferred_quotation(self):
        good_file = ["p[href^='https://']:before { content: 'secure'; }"]
        self.check_validity(self.uut, good_file)

        bad_file = ['p[href^="https://"]:before { content: "secure"; }']
        self.check_invalidity(self.uut, bad_file)

    def test_empty_rulesets(self):
        good_file = ['a { color: red; }\n',
                     '\n',
                     'p { /* hey */ }']
        self.check_validity(self.uut, good_file)

        bad_file = ['a { color: red; }\n\n',
                    'p { /* hey */ }\n\n',
                    'b { }']
        self.check_invalidity(self.uut, bad_file)

    def test_space_after_colon(self):
        good_file = ['a { top: 0; }']
        self.check_validity(self.uut, good_file)

        bad_file = ['a { top:0; }']
        self.check_invalidity(self.uut, bad_file)

    def test_space_before_combinator(self):
        good_file = ['p > a { color: panda; }']
        self.check_validity(self.uut, good_file)

        bad_file = ['p> a { color: panda; }']
        self.check_invalidity(self.uut, bad_file)

    def test_space_before_opening_brace(self):
        good_file = ['a { color: red; }']
        self.check_validity(self.uut, good_file)

        bad_file = ['a{ color: red; }']
        self.check_invalidity(self.uut, bad_file)

    def test_trailing_whitespace(self):
        good_file = ['a { color: red; }']
        self.check_validity(self.uut, good_file)

        bad_file = ['a { color: red; }\t']
        self.check_invalidity(self.uut, bad_file)

        bad_file = ['a { color: red; }  ']
        self.check_invalidity(self.uut, bad_file)

    def test_units_in_zero_valued_dimensions(self):
        good_file = ['img { border: 0; }']
        self.check_validity(self.uut, good_file)

        bad_file = ['img { border: 0px; }']
        self.check_invalidity(self.uut, bad_file)

    def test_config_file(self):
        self.section.append(Setting('csscomb_config', os.path.join(
            os.path.dirname(__file__), 'csscomb_test_files', '.csscomb.json')))
        good_file = ['a { color: red; }']
        self.check_validity(self.uut, good_file)

        bad_file = ['a {color: red;}']
        self.check_invalidity(self.uut, bad_file)
