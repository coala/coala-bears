import os
from queue import Queue

from bears.php.PHPMessDetectorBear import PHPMessDetectorBear
from coalib.testing.LocalBearTestHelper import LocalBearTestHelper
from coalib.testing.BearTestHelper import generate_skip_decorator
from coalib.results.Result import Result
from coalib.settings.Section import Section
from coalib.settings.Setting import Setting


def get_testfile_path(name):
    return os.path.join(os.path.dirname(__file__),
                        'phpmessdetector_test_files',
                        name)


def load_testfile(name):
    with open(get_testfile_path(name)) as file:
        return file.readlines()


@generate_skip_decorator(PHPMessDetectorBear)
class PHPMessDetectorBearTest(LocalBearTestHelper):

    def setUp(self):
        self.section = Section('name')
        self.uut = PHPMessDetectorBear(self.section, Queue())

    def test_cleancode_violation(self):
        file_contents = load_testfile('cleancode_violation.php')
        self.section.append(Setting('phpmd_rulesets', 'cleancode'))
        self.check_results(
            self.uut,
            file_contents,
            [Result.from_values('PHPMessDetectorBear',
                                'The method bar uses an else expression. Else '
                                'is never necessary and you can simplify the '
                                'code to work without else.',
                                file=get_testfile_path(
                                    'cleancode_violation.php'),
                                line=8)],
            filename=get_testfile_path('cleancode_violation.php'))

    def test_codesize_violation(self):
        file_contents = load_testfile('codesize_violation.php')
        self.section.append(Setting('phpmd_rulesets', 'codesize'))
        self.check_results(
            self.uut,
            file_contents,
            [Result.from_values('PHPMessDetectorBear',
                                'The method example() has a Cyclomatic '
                                'Complexity of 11. The configured cyclomatic '
                                'complexity threshold is 10.',
                                file=get_testfile_path(
                                    'codesize_violation.php'),
                                line=4)],
            filename=get_testfile_path('codesize_violation.php'))

    def test_design_violation(self):
        file_contents = load_testfile('design_violation.php')
        self.section.append(Setting('phpmd_rulesets', 'design'))
        self.check_results(
            self.uut,
            file_contents,
            [Result.from_values('PHPMessDetectorBear',
                                'The method bar() contains an exit '
                                'expression.',
                                file=get_testfile_path(
                                    'design_violation.php'),
                                line=5),
             Result.from_values('PHPMessDetectorBear',
                                'The method foo() contains an eval '
                                'expression.',
                                file=get_testfile_path(
                                    'design_violation.php'),
                                line=12)],
            filename=get_testfile_path('design_violation.php'))

    def test_naming_violation(self):
        file_contents = load_testfile('naming_violation.php')
        self.section.append(Setting('phpmd_rulesets', 'naming'))
        self.check_results(
            self.uut,
            file_contents,
            [Result.from_values('PHPMessDetectorBear',
                                'Avoid variables with short names like $q. '
                                'Configured minimum length is 3.',
                                file=get_testfile_path(
                                    'naming_violation.php'),
                                line=3),
             Result.from_values('PHPMessDetectorBear',
                                'Avoid variables with short names like $as. '
                                'Configured minimum length is 3.',
                                file=get_testfile_path(
                                    'naming_violation.php'),
                                line=4),
             Result.from_values('PHPMessDetectorBear',
                                'Avoid variables with short names like $r. '
                                'Configured minimum length is 3.',
                                file=get_testfile_path(
                                    'naming_violation.php'),
                                line=5)],
            filename=get_testfile_path('naming_violation.php'))

    def test_unusedcode_violation(self):
        file_contents = load_testfile('unusedcode_violation.php')
        self.section.append(Setting('phpmd_rulesets', 'unusedcode'))
        self.check_results(
            self.uut,
            file_contents,
            [Result.from_values('PHPMessDetectorBear',
                                'Avoid unused local variables such as \'$i\'.',
                                file=get_testfile_path(
                                    'unusedcode_violation.php'),
                                line=5),
             Result.from_values('PHPMessDetectorBear',
                                'Avoid unused private methods such '
                                'as \'foo\'.',
                                file=get_testfile_path(
                                    'unusedcode_violation.php'),
                                line=9)],
            filename=get_testfile_path('unusedcode_violation.php'))
