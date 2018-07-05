import os
import sys

from queue import Queue

from bears.c_languages.codeclone_detection.ClangCloneDetectionBear import (
    ClangCloneDetectionBear)
from bears.c_languages.codeclone_detection.ClangFunctionDifferenceBear import (
    ClangFunctionDifferenceBear)
from coalib.results.RESULT_SEVERITY import RESULT_SEVERITY
from coalib.results.Result import Result
from coalib.testing.BearTestHelper import generate_skip_decorator
from coalib.testing.LocalBearTestHelper import LocalBearTestHelper
from coalib.settings.Section import Section
from coalib.settings.Setting import Setting


@generate_skip_decorator(ClangCloneDetectionBear)
class ClangCloneDetectionBearTest(LocalBearTestHelper):

    def setUp(self):
        self.base_test_path = os.path.abspath(os.path.join(
            os.path.dirname(__file__),
            'clone_detection_samples'))
        self.section = Section('default')
        self.section.append(Setting('files', '', origin=self.base_test_path))
        self.section.append(Setting('max_clone_difference', '0.308'))
        self.clone_files = [os.listdir(os.path.join(self.base_test_path,
                                                    'clones'))]

    def test_dependencies(self):
        self.assertIn(ClangFunctionDifferenceBear,
                      ClangCloneDetectionBear.BEAR_DEPS)

    def test_configuration(self):
        self.section.append(Setting('average_calculation', 'true'))
        self.section.append(Setting('poly_postprocessing', 'false'))
        self.section.append(Setting('exp_postprocessing', 'true'))

        self.clone_files = [
            os.path.join(self.base_test_path, 'clones', 's4c.c')]

        # Ignore the results, it may be possible that it still passes :)
        self.check_clone_detection_bear(self.clone_files,
                                        lambda results, msg: True)

    def test_non_clones(self):
        self.non_clone_files = [
            os.path.join(self.base_test_path, 'non_clones', elem)
            for elem in os.listdir(os.path.join(self.base_test_path,
                                                'non_clones'))]

        self.check_clone_detection_bear(self.non_clone_files,
                                        lambda results, msg:
                                        self.assertEqual(results, [], msg))

    def test_clones(self):
        clone_files = ['python_casing.c',
                       'several_duplicates.c',
                       's3c.c',
                       'python_casing2.c',
                       's3a.c',
                       's1c.c',
                       's3b.c',
                       's2c.c',
                       's4a.c',
                       's4c.c',
                       's2b.c',
                       's4b.c',
                       'kernel_scrolling.c',
                       'one_big_one_small.c',
                       'bubblesort.c',
                       's3d.c',
                       's1b.c',
                       's1a.c',
                       'faculty.c',
                       's2a.c',
                       's4d.c',
                       's2d.c',
                       's3e.c']
        clone_files = [os.path.join(self.base_test_path, 'clones', name)
                       for name in clone_files]

        # Actual `Result` objects for each test files
        files_results = [self.get_results_clone_detection_bear(filepath) for
                         filepath in clone_files]

        result_msg_template = (
            'Code clone found. The other occurrence is at file '
            '{file}, line {line}, function {function}. The '
            'difference is {difference}%.')

        files_expected_results_py36 = [
            # python_casing.c
            [Result.from_values(
                origin='ClangCloneDetectionBear',
                message=result_msg_template.format(
                    file=clone_files[0],
                    line=30,
                    function=(
                        '_Py_bytes_capitalize(char *, char *, Py_ssize_t)'),
                    difference=0.3044843508457327),
                file=clone_files[0],
                severity=RESULT_SEVERITY.MAJOR,
                line=11,
                debug_msg=files_results[0][0].debug_msg)],

            # several_duplicates.c
            [Result.from_values(
                origin='ClangCloneDetectionBear',
                message=result_msg_template.format(
                    file=clone_files[1],
                    line=10,
                    function='something(int)',
                    difference=0.0),
                file=clone_files[1],
                severity=RESULT_SEVERITY.MAJOR,
                line=4,
                debug_msg=files_results[1][0].debug_msg),
             Result.from_values(
                origin='ClangCloneDetectionBear',
                message=result_msg_template.format(
                    file=clone_files[1],
                    line=16,
                    function='other(int)',
                    difference=0.0),
                file=clone_files[1],
                severity=RESULT_SEVERITY.MAJOR,
                line=4,
                debug_msg=files_results[1][1].debug_msg),
             Result.from_values(
                origin='ClangCloneDetectionBear',
                message=result_msg_template.format(
                    file=clone_files[1],
                    line=16,
                    function='other(int)',
                    difference=0.0),
                file=clone_files[1],
                severity=RESULT_SEVERITY.MAJOR,
                line=10,
                debug_msg=files_results[1][2].debug_msg)],

            # s3c.c
            [Result.from_values(
                origin='ClangCloneDetectionBear',
                message=result_msg_template.format(
                    file=clone_files[2],
                    line=15,
                    function='sumProd(int)',
                    difference=0.3033375935859079),
                file=clone_files[2],
                severity=RESULT_SEVERITY.MAJOR,
                line=7,
                debug_msg=files_results[2][0].debug_msg)],

            # python_casing2.c
            [Result.from_values(
                origin='ClangCloneDetectionBear',
                message=result_msg_template.format(
                    file=clone_files[3],
                    line=41,
                    function='_Py_bytes_isupper(const char *, Py_ssize_t)',
                    difference=0.0),
                file=clone_files[3],
                severity=RESULT_SEVERITY.MAJOR,
                line=14,
                debug_msg=files_results[3][0].debug_msg)],

            # s3a.c
            [Result.from_values(
                origin='ClangCloneDetectionBear',
                message=result_msg_template.format(
                    file=clone_files[4],
                    line=15,
                    function='sumProd(int)',
                    difference=0.12414801135904178),
                file=clone_files[4],
                severity=RESULT_SEVERITY.MAJOR,
                line=7,
                debug_msg=files_results[4][0].debug_msg)],

            # s1c.c
            [Result.from_values(
                origin='ClangCloneDetectionBear',
                message=result_msg_template.format(
                    file=clone_files[5],
                    line=15,
                    function='sumProd(int)',
                    difference=0.0),
                file=clone_files[5],
                severity=RESULT_SEVERITY.MAJOR,
                line=7,
                debug_msg=files_results[5][0].debug_msg)],

            # s3b.c
            [Result.from_values(
                origin='ClangCloneDetectionBear',
                message=result_msg_template.format(
                    file=clone_files[6],
                    line=15,
                    function='sumProd(int)',
                    difference=0.12414801135904178),
                file=clone_files[6],
                severity=RESULT_SEVERITY.MAJOR,
                line=7,
                debug_msg=files_results[6][0].debug_msg)],

            # s2c.c
            [Result.from_values(
                origin='ClangCloneDetectionBear',
                message=result_msg_template.format(
                    file=clone_files[7],
                    line=15,
                    function='sumProd(int)',
                    difference=0.0),
                file=clone_files[7],
                severity=RESULT_SEVERITY.MAJOR,
                line=7,
                debug_msg=files_results[7][0].debug_msg)],

            # s4a.c
            [Result.from_values(
                origin='ClangCloneDetectionBear',
                message=result_msg_template.format(
                    file=clone_files[8],
                    line=15,
                    function='sumProd(int)',
                    difference=0.0),
                file=clone_files[8],
                severity=RESULT_SEVERITY.MAJOR,
                line=7,
                debug_msg=files_results[8][0].debug_msg)],

            # s4c.c
            [Result.from_values(
                origin='ClangCloneDetectionBear',
                message=result_msg_template.format(
                    file=clone_files[9],
                    line=15,
                    function='sumProd(int)',
                    difference=0.0),
                file=clone_files[9],
                severity=RESULT_SEVERITY.MAJOR,
                line=7,
                debug_msg=files_results[9][0].debug_msg)],

            # s2b.c
            [Result.from_values(
                origin='ClangCloneDetectionBear',
                message=result_msg_template.format(
                    file=clone_files[10],
                    line=15,
                    function='sumProd(int)',
                    difference=0.0),
                file=clone_files[10],
                severity=RESULT_SEVERITY.MAJOR,
                line=7,
                debug_msg=files_results[10][0].debug_msg)],

            # s4b.c
            [Result.from_values(
                origin='ClangCloneDetectionBear',
                message=result_msg_template.format(
                    file=clone_files[11],
                    line=15,
                    function='sumProd(int)',
                    difference=0.0),
                file=clone_files[11],
                severity=RESULT_SEVERITY.MAJOR,
                line=7,
                debug_msg=files_results[11][0].debug_msg)],

            # kernel_scrolling.c
            [Result.from_values(
                origin='ClangCloneDetectionBear',
                message=result_msg_template.format(
                    file=clone_files[12],
                    line=17,
                    function='scrollUp()',
                    difference=0.3073388122494525),
                file=clone_files[12],
                severity=RESULT_SEVERITY.MAJOR,
                line=6,
                debug_msg=files_results[12][0].debug_msg)],

            # one_big_one_small.c
            [Result.from_values(
                origin='ClangCloneDetectionBear',
                message=result_msg_template.format(
                    file=clone_files[13],
                    line=21,
                    function='count_a_lot(int)',
                    difference=0.0),
                file=clone_files[13],
                severity=RESULT_SEVERITY.MAJOR,
                line=1,
                debug_msg=files_results[13][0].debug_msg)],

            # bubblesort.c
            [Result.from_values(
                origin='ClangCloneDetectionBear',
                message=result_msg_template.format(
                    file=clone_files[14],
                    line=21,
                    function='bubbleSort(int *, int)',
                    difference=0.15055637627789575),
                file=clone_files[14],
                severity=RESULT_SEVERITY.MAJOR,
                line=2,
                debug_msg=files_results[14][0].debug_msg)],

            # s3d.c
            [Result.from_values(
                origin='ClangCloneDetectionBear',
                message=result_msg_template.format(
                    file=clone_files[15],
                    line=15,
                    function='sumProd(int)',
                    difference=0.10641258116489294),
                file=clone_files[15],
                severity=RESULT_SEVERITY.MAJOR,
                line=7,
                debug_msg=files_results[15][0].debug_msg)],

            # s1b.c
            [Result.from_values(
                origin='ClangCloneDetectionBear',
                message=result_msg_template.format(
                    file=clone_files[16],
                    line=15,
                    function='sumProd(int)',
                    difference=0.0),
                file=clone_files[16],
                severity=RESULT_SEVERITY.MAJOR,
                line=7,
                debug_msg=files_results[16][0].debug_msg)],

            # s1a.c
            [Result.from_values(
                origin='ClangCloneDetectionBear',
                message=result_msg_template.format(
                    file=clone_files[17],
                    line=15,
                    function='sumProd(int)',
                    difference=0.0),
                file=clone_files[17],
                severity=RESULT_SEVERITY.MAJOR,
                line=7,
                debug_msg=files_results[17][0].debug_msg)],

            # faculty.c
            [Result.from_values(
                origin='ClangCloneDetectionBear',
                message=result_msg_template.format(
                    file=clone_files[18],
                    line=10,
                    function='faculty2(int)',
                    difference=0.2304748676745328),
                file=clone_files[18],
                severity=RESULT_SEVERITY.MAJOR,
                line=1,
                debug_msg=files_results[18][0].debug_msg)],

            # s2a.c
            [Result.from_values(
                origin='ClangCloneDetectionBear',
                message=result_msg_template.format(
                    file=clone_files[19],
                    line=15,
                    function='sumProd(int)',
                    difference=0.0),
                file=clone_files[19],
                severity=RESULT_SEVERITY.MAJOR,
                line=7,
                debug_msg=files_results[19][0].debug_msg)],

            # s4d.c
            [Result.from_values(
                origin='ClangCloneDetectionBear',
                message=result_msg_template.format(
                    file=clone_files[20],
                    line=15,
                    function='sumProd(int)',
                    difference=0.0),
                file=clone_files[20],
                severity=RESULT_SEVERITY.MAJOR,
                line=7,
                debug_msg=files_results[20][0].debug_msg)],

            # s2d.c
            [Result.from_values(
                origin='ClangCloneDetectionBear',
                message=result_msg_template.format(
                    file=clone_files[21],
                    line=15,
                    function='sumProd(int)',
                    difference=0.1625057057913528),
                file=clone_files[21],
                severity=RESULT_SEVERITY.MAJOR,
                line=7,
                debug_msg=files_results[21][0].debug_msg)],

            # s3e.c
            [Result.from_values(
                origin='ClangCloneDetectionBear',
                message=result_msg_template.format(
                    file=clone_files[22],
                    line=15,
                    function='sumProd(int)',
                    difference=0.22764169849191776),
                file=clone_files[22],
                severity=RESULT_SEVERITY.MAJOR,
                line=7,
                debug_msg=files_results[22][0].debug_msg)],
        ]

        # Due to different floating numbers implementation on Python version
        # 3.5 and 3.4, we just run this test on Python 3.6 or later
        if sys.version_info > (3, 6, 0):
            for files_result, files_expected_result in zip(
                    files_results, files_expected_results_py36):
                self.assertComparableObjectsEqual(files_result,
                                                  files_expected_result)

        self.check_clone_detection_bear(clone_files,
                                        lambda results, msg:
                                        self.assertNotEqual(results, [], msg))

    def get_results_clone_detection_bear(self, file):
        """
        Get the results of ClangCloneDetectionBear.

        :param file: A file path that will be checked.
        :return:     List of `Result`s object yielded by
                     ClangCloneDetectionBear.
        """
        difference_results = ClangFunctionDifferenceBear(
            {file: ''},
            self.section,
            Queue()).run_bear_from_section([], {})

        uut = ClangCloneDetectionBear(
            {file: ''},
            self.section,
            Queue())

        arg_dict = {'dependency_results':
                    {ClangFunctionDifferenceBear.__name__:
                        list(difference_results)}}

        return list(uut.run_bear_from_section([], arg_dict))

    def check_clone_detection_bear(self, files, result_check_function):
        """
        Checks the results of the CloneDetectionBear with the given function.

        :param files:                 The files to check. Each will be checked
                                      on its own.
        :param result_check_function: A function yielding an exception if the
                                      results are invalid.
        """
        for file in files:
            result_check_function(
                self.get_results_clone_detection_bear(file),
                'while analyzing '+file)
