from coalib.bearlib.abstractions.Linter import linter
from dependency_management.requirements.PipRequirement import PipRequirement
from coalib.settings.Setting import typed_list


@linter(executable='cppclean',
        output_format='regex',
        output_regex=r'.+:(?P<line>\d+):(?P<message>.*)')
class CPPCleanBear:
    """
    Find problems in C++ source code that slow down development in large code
    bases. This includes finding unused code, among other features.

    Read more about available routines at
    <https://github.com/myint/cppclean#features>.
    """

    LANGUAGES = {'CPP'}
    REQUIREMENTS = {PipRequirement('cppclean', '0.12.0')}
    AUTHORS = {'The coala developers'}
    AUTHORS_EMAILS = {'coala-devel@googlegroups.com'}
    LICENSE = 'AGPL-3.0'
    CAN_DETECT = {'Smell', 'Unused Code', 'Security'}

    @staticmethod
    def create_arguments(filename,
                         file,
                         config_file,
                         include_paths: typed_list(str) = (),
                         ):
        args = [filename]
        for include_path in include_paths:
            args.append('--include-path')
            args.append(include_path)

        return args
