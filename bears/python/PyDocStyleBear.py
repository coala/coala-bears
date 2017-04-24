from coalib.bearlib.abstractions.Linter import linter
from dependency_management.requirements.PipRequirement import PipRequirement
from coalib.settings.Setting import typed_list


@linter(executable='pydocstyle',
        use_stdout=True,
        use_stderr=True,
        output_format='regex',
        output_regex=r'.*:(?P<line>\d+) .+:\n\s+(?P<message>.*)')
class PyDocStyleBear:
    """
    Checks python docstrings.
    """
    LANGUAGES = {'Python', 'Python 2', 'Python 3'}
    REQUIREMENTS = {PipRequirement('pydocstyle', '2.0')}
    AUTHORS = {'The coala developers'}
    AUTHORS_EMAILS = {'coala-devel@googlegroups.com'}
    LICENSE = 'AGPL-3.0'
    CAN_DETECT = {'Formatting', 'Documentation'}

    def create_arguments(self, filename, file, config_file,
                         pydocstyle_select: typed_list(str)=(),
                         pydocstyle_ignore: typed_list(str)=(),
                         pydocstyle_add_ignore: typed_list(str)=(),
                         pydocstyle_add_select: typed_list(str)=()):
        """
        :param pydocstyle_select:
            List of checked errors by specifying which errors to check for.
            Can't be used together with ``pydocstyle_ignore``.
        :param pydocstyle_ignore:
            List of checked errors by specifying which errors to ignore. Can't
            be used together with ``pydocstyle_select``. It overrides
            default list of to-ignore error list.
        :param pydocstyle_add_ignore:
            List of checked errors to amend the list of default errors to
            check for by specifying more error codes to ignore.
        :param pydocstyle_add_select:
            List of checked errors to amend the list of default errors to
            check for by specifying more error codes to check.
        """
        args = (filename,)
        if pydocstyle_ignore and pydocstyle_select:
            self.err('The arguments pydocstyle_select and pydocstyle_ignore '
                     'are both given but mutually exclusive.')
            return
        elif pydocstyle_ignore:
            ignore = ','.join(part.strip() for part in pydocstyle_ignore)
            args += ('--ignore=' + ignore,)
        elif pydocstyle_select:
            select = ','.join(part.strip() for part in pydocstyle_select)
            args += ('--select=' + select,)
        elif pydocstyle_add_ignore:
            add_ignore = ','.join(part.strip()
                                  for part in pydocstyle_add_ignore)
            args += ('--add-ignore=' + add_ignore,)
        elif pydocstyle_add_select:
            add_select = ','.join(part.strip()
                                  for part in pydocstyle_add_select)
            args += ('--add-select=' + add_select,)

        return args
