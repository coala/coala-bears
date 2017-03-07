from coalib.bearlib.abstractions.Linter import linter
from coalib.bearlib.spacing.SpacingHelper import SpacingHelper
from dependency_management.requirements.DistributionRequirement import (
    DistributionRequirement)


@linter(executable='astyle',
        output_format='corrected',
        use_stdin=True)
class AStyleLintBear:
    """
    Artistic Style is a source code indenter, formatter,
    and beautifier for the C, C++, C++/CLI, Objective‑C,
    C# and Java programming languages.

    For more information, consult <http://astyle.sourceforge.net/astyle.html>.
    """

    LANGUAGES = {'C', 'C++', 'Objective-C', 'C#', 'Java'}
    REQUIREMENTS = {DistributionRequirement(apt_get='astyle')}
    AUTHORS = {'The coala developers'}
    AUTHORS_EMAILS = {'coala-devel@googlegroups.com'}
    LICENSE = 'AGPL-3.0'
    CAN_FIX = {'Formatting'}

    @staticmethod
    def create_arguments(filename, file, config_file,
                         astyle_bracket_style: str='',
                         use_spaces: bool=None,
                         indent_size: int=0):
        """
        :param astyle_bracket_style:
            Defines the bracket style to use. If no bracket style is
            specified, the default 'allman' is used.
        :param use_spaces:
            If None, no indentation is specified and astyle uses a default.
            If True, astyle uses spaces or if explicitly set to False, astyle
            uses tabs for indentation.
        :param indent_size:
            Number of spaces per indentation level.
        """
        args = ['--dry-run', '--suffix=none']
        if astyle_bracket_style:
            args.append('--style=' + astyle_bracket_style)
        if use_spaces is None:
            indent = None
        elif use_spaces:
            indent = '--indent=spaces'
        else:
            indent = '--indent=tab'
        if indent:
            if indent_size:
                args.append(indent + '=' + str(indent_size))
            else:
                args.append(indent)
        return args
