from queue import Queue
from bears.general.CasingBear import CasingBear
from bears.general.AnnotationBear import AnnotationBear
from tests.LocalBearTestHelper import LocalBearTestHelper
from coalib.settings.Section import Section
from coalib.settings.Setting import Setting
from coalib.bears.LocalBear import LocalBear
from coalib.results.HiddenResult import HiddenResult


class CasingBearTest(LocalBearTestHelper):

    def setUp(self):
        self.section = Section("test section")

    def get_results(self, file, section=None):
        self.dep_uut = AnnotationBear(section, Queue())
        dep_results_valid = self.dep_uut.execute("file", file)
        uut = CasingBear(section, Queue())

        arg_dict = {'dependency_results':
                    {AnnotationBear.__name__:
                     list(dep_results_valid)},
                    'file': file}
        reply = uut.run_bear_from_section(["file"], arg_dict)
        return list(reply)

    def verify_bear(self,
                    file=None,
                    valid=True,
                    exception=False):
        results = self.get_results(file, self.section)
        if valid:
            self.assertEqual(results, [])
        else:
            self.assertNotEqual(results, [])

    def test_defaults(self):
        self.section.append(Setting("casing", "snake"))
        self.section.append(Setting("language", "CPP"))
        self.verify_bear(["int abc_def;\n", "int ab_cd;\n"])
        self.verify_bear(["int abc_def = xyz_abc;\n"])
        self.verify_bear(["int abcEfg = 4;\n"], valid=False)
        self.verify_bear(["int abCd = 4;\n"], valid=False)
        self.verify_bear(
            ["int abc_def;\n", "int abCd;\n"],
            valid=False)
        self.verify_bear(
            ["char wrongStr=\"test\";\n", "int correct_var = 42;\n"],
            valid=False)
        self.verify_bear(
            ["char correct_str=\"test\";\n", "int correct_var = 42;\n"],
            valid=True)
        self.verify_bear(
            ["testVar = 42;\n", "testVar = 0;\n", "testVar += 1;\n"],
            valid=False)
        self.verify_bear(
            ["int incorrectVar = 32, anotherInt = 22\n"],
            valid=False)
        self.verify_bear(
            ["int correct_var = 32, anotherInt = 22\n"],
            valid=False)
        self.verify_bear(
            ["int correct_var = 32, another_int = 22\n"],
            valid=True)

    def test_invalid_settings(self):
        self.section = Section("test_section_2")
        self.section.append(Setting("casing", "snake"))
        self.section.append(Setting("language", "InvalidLang"))

        results = self.get_results(
            ["int testVar = 42;\n", "int correct_var = 32;\n"],
            self.section)
        self.assertEqual(len(results), 1)
        self.assertEqual(HiddenResult, type(results[0]))
        self.assertTrue("coalang specification for " in results[0].contents)

        self.section = Section("test_section_3")
        self.section.append(Setting("casing", "invalid"))
        self.section.append(Setting("language", "C"))

        # This should return no results since the given casing is invalid.
        self.verify_bear(
            ["int testVar = 42;\n"],
            valid=True)

        self.section = Section("test_section_4")
        self.section.append(Setting("casing", "snake"))
        self.section.append(Setting("language", "python3"))

        # No results will be returned since python3 doesn't have
        # complete coalang support with keywords yet.
        self.verify_bear(
            ["testVar = 42\n"],
            valid=True)
