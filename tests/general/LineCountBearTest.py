from queue import Queue

from bears.general.LineCountBear import LineCountBear
from tests.LocalBearTestHelper import LocalBearTestHelper
from coalib.results.Result import RESULT_SEVERITY, Result
from coalib.settings.Section import Section
from coalib.settings.Setting import Setting


class LineCountBearTest(LocalBearTestHelper):

    def setUp(self):
        self.section = Section("name")
        self.uut = LineCountBear(self.section, Queue())

    def test_run(self):
        self.section.append(Setting("max_lines_per_file", 1))
        self.check_results(
            self.uut, ["line 1", "line 2", "line 3"],
            [Result.from_values("LineCountBear",
                                "This file had 3 lines, which is 2 lines more "
                                "than the maximum limit specified.",
                                severity=RESULT_SEVERITY.NORMAL,
                                file="default")],
            filename="default")
        self.check_validity(self.uut, ["1 line"])
        self.check_validity(self.uut, [])  # Empty file
