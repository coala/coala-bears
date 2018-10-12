import logging

from coalib.bearlib.abstractions.Linter import linter
from dependency_management.requirements.DistributionRequirement import (
    DistributionRequirement)
from coalib.results.RESULT_SEVERITY import RESULT_SEVERITY
from coalib.settings.Setting import typed_list
from coalib.bearlib.languages.Language import Language


@linter(executable='cppcheck',
        use_stdout=False,
        use_stderr=True,
        global_bear=True,
        output_format='regex',
        output_regex=r'(?P<line>\d+):(?P<severity>[a-zA-Z]+):'
                     r'(?P<origin>[a-zA-Z]+):(?P<message>.*)',
        severity_map={'error': RESULT_SEVERITY.MAJOR,
                      'warning': RESULT_SEVERITY.NORMAL,
                      'style': RESULT_SEVERITY.INFO})
class CPPCheckBear:
    """
    Report possible security weaknesses for C/C++.
    For more information, consult <https://github.com/danmar/cppcheck>.
    """

    LANGUAGES = {'C', 'CPP'}
    REQUIREMENTS = {DistributionRequirement('cppcheck')}
    AUTHORS = {'The coala developers'}
    AUTHORS_EMAILS = {'coala-devel@googlegroups.com'}
    LICENSE = 'AGPL-3.0'
    CAN_DETECT = {'Security', 'Unused Code', 'Unreachable Code', 'Smell'}

    def create_arguments(self, config_file,
                         enable: typed_list(str) = [],
                         language: str = None,
                         ):
        """
        :param enable:
            Choose specific issues to report. Issues that can be
            reported are: all, warning, style, performance,
            portability, information, unusedFunction,
            missingInclude

        :param language:
            Choose specific language for linting. Language can be
            either c or c++
        """
        args = ('--template={line}:{severity}:{id}:{message}',)
        files = tuple(self.file_dict.keys())

        if enable:
            args += ('--enable=' + ','.join(enable),)

        if language is not None:
            try:
                lang = Language[language]
                if isinstance(lang, Language.CPP):
                    args += ('--language=c++',)
                elif isinstance(lang, Language.C):
                    args += ('--language=c',)
                else:
                    logging.error('Language can be either c or c++')
                    return
            except Exception:
                logging.error('Language can be either c or c++')
                return
        return args + files
