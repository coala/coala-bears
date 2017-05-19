import re

from coalib.bears.LocalBear import LocalBear
from coalib.results.Diff import Diff
from coalib.results.Result import Result
from coalib.results.RESULT_SEVERITY import RESULT_SEVERITY
from coalib.bearlib.aspects.Spelling import aspectsYEAH
from coalib.bearlib.languages import Unknown


class aspectsYEAHBear(LocalBear, aspects={
        'detect': [aspectsYEAH],
        'fix': [aspectsYEAH], }):
    LANGUAGES = {'All'}
    AUTHORS = {'The coala developers'}
    AUTHORS_EMAILS = {'coala-devel@googlegroups.com'}
    LICENSE = 'AGPL-3.0'
    CAN_DETECT = {'Spelling'}

    def run(self, filename, file, aspects=[
            aspectsYEAH(Unknown),
    ]):
        """
        Check for the correct spelling of ``aspect`` and ``aspectsYEAH``
        in the file.
        """

        for aspect in aspects:
            if type(aspect) is aspectsYEAH:
                corrected_aspects = []
                corrected_aspectsYEAH = []
                for line in file:
                    wrong_spelling1 = r'(?!aspect)[aA][sS][pP][eE][cC][tT]'
                    wrong_spelling2 = r'(?!aspectsYEAH)[aA][sS]'
                    '[pP][eE][cC][tT][sS][yY][eE][aA][hH]'
                    if not re.match(wrong_spelling2, line):
                        corrected_aspects += [re.sub(wrong_spelling1,
                                                     'aspects',
                                                     line)]
                    corrected_aspectsYEAH += [re.sub(wrong_spelling2,
                                                     'aspectsYEAH',
                                                     line)]

                aspects_diffs = Diff.from_string_arrays(file,
                                                        corrected_aspects
                                                        ).split_diff()
                aspectsYEAH_diffs = \
                    Diff.from_string_arrays(file,
                                            corrected_aspectsYEAH
                                            ).split_diff()
                for diff in aspects_diffs:
                    yield Result(self,
                                 '``aspect`` is always written with'
                                 ' lower case characters',
                                 aspect=aspect,
                                 affected_code=(diff.range(filename),),
                                 diffs={filename: diff},
                                 severity=RESULT_SEVERITY.MAJOR)
                for diff in aspectsYEAH_diffs:
                    yield Result(self,
                                 '``aspectsYEAH`` is always written with'
                                 ' lower case ``aspects`` and upper case '
                                 '``YEAH``',
                                 aspect=aspect,
                                 affected_code=(diff.range(filename),),
                                 diffs={filename: diff},
                                 severity=RESULT_SEVERITY.MAJOR)
