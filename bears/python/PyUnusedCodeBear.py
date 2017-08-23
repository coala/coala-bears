import autoflake

from coalib.bears.LocalBear import LocalBear
from dependency_management.requirements.PipRequirement import PipRequirement
from coalib.results.Diff import Diff
from coalib.results.Result import Result
from coalib.bearlib.aspects import map_setting_to_aspect
from coalib.bearlib.aspects.Redundancy import (
    Redundancy,
    UnusedImport,
    UnusedLocalVariable,
)


class PyUnusedCodeBear(
        LocalBear,
        aspects={
            'fix': [
                UnusedImport,
                UnusedLocalVariable,
            ]},
        languages=['Python'],
        ):
    LANGUAGES = {'Python', 'Python 2', 'Python 3'}
    REQUIREMENTS = {PipRequirement('autoflake', '0.7')}
    AUTHORS = {'The coala developers'}
    AUTHORS_EMAILS = {'coala-devel@googlegroups.com'}
    LICENSE = 'AGPL-3.0'
    CAN_DETECT = {'Unused Code'}

    @map_setting_to_aspect(
        remove_all_unused_imports=UnusedImport.remove_non_standard_import,
        remove_unused_variables=UnusedLocalVariable)
    def run(self, filename, file,
            remove_all_unused_imports: bool=True,
            remove_unused_variables: bool=True):
        """
        Detects unused code. By default this functionality is limited to:

        - Unneeded pass statements.
        - All unused imports - might have side effects
        - Unused variables - might have side effects

        :param remove_all_unused_imports:
            ``False`` removes only unused builtin imports
        :param remove_unused_variables:
            ``False`` keeps unused variables
        """
        corrected = autoflake.fix_code(
                       ''.join(file),
                       additional_imports=None,
                       remove_all_unused_imports=remove_all_unused_imports,
                       remove_unused_variables=remove_unused_variables
                       ).splitlines(True)

        for diff in Diff.from_string_arrays(file, corrected).split_diff():
            yield Result(self,
                         'This file contains unused source code.',
                         affected_code=(diff.range(filename),),
                         diffs={filename: diff},
                         aspect=Redundancy('py'))
