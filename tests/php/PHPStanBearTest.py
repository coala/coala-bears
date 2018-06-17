import os
from queue import Queue
from shutil import which
from unittest.case import skipIf

from bears.php.PHPStanBear import PHPStanBear
from coalib.testing.LocalBearTestHelper import LocalBearTestHelper
from coalib.settings.Section import Section
from coalib.results.Result import RESULT_SEVERITY, Result
from coalib.settings.Setting import Setting


@skipIf(which('phpstan') is None, 'PHPStan is not installed')
class PHPStanTest(LocalBearTestHelper):

    def setUp(self):
        self.section = Section('test section')
        self.uut = PHPStanBear(self.section, Queue())
        self.test_file1 = os.path.join(os.path.dirname(__file__),
                                       'test_files',
                                       'phplint_test1.php')
        self.test_file2 = os.path.join(os.path.dirname(__file__),
                                       'test_files',
                                       'phplint_test2.php')
        self.config_file = os.path.join(os.path.dirname(__file__),
                                        'test_files',
                                        'phpstan.neon')

    def test_run(self):
        # Test for a particular output
        self.check_results(
            self.uut,
            [],
            [Result.from_values(self.uut,
                                "Syntax error, unexpected ';' on line 3",
                                line=3,
                                severity=RESULT_SEVERITY.NORMAL,
                                file=self.test_file1)],
            filename=self.test_file1)

        # Test a file with errors and warnings
        self.check_validity(
            self.uut,
            [],
            self.test_file1,
            valid=False)
        self.section.append(Setting('phpstan_config', 'phpstan.neon'))
        # Test a file without any issues with a config file
        self.check_validity(
            self.uut,
            [],
            self.test_file2)
        self.section.append(Setting('phpstan_level', '3'))
        self.section.append(Setting('phpstan_config', 'phpstan.neon'))
        # Test a file without any issues with level set and a config file
        self.check_validity(
            self.uut,
            [],
            self.test_file2)
