from queue import Queue
from bears.general.VariableCasingBear import VariableCasingBear
from tests.LocalBearTestHelper import LocalBearTestHelper
from coalib.settings.Section import Section
from coalib.settings.Setting import Setting


class VariableCasingBearTest(LocalBearTestHelper):

    def setUp(self):
        self.section = Section("test section")
        self.uut = VariableCasingBear(self.section, Queue())

    def test_defaults(self):
        self.section.append(Setting("casing", "snake_casing"))
        self.section.append(Setting("language", "CPP"))
        self.section.append(Setting("language_family", "C"))
        self.check_validity(self.uut, ["int abc_def;\n", "int ab_cd;\n"])
        self.check_validity(self.uut, ["int abc_def = xyz_abc;\n"])
        self.check_validity(self.uut, ["int abcEfg = 4;\n"], valid=False)
        self.check_validity(self.uut, ["int abCd = 4;\n"], valid=False)
