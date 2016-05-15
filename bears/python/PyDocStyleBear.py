from coalib.bearlib.abstractions.Linter import linter
from coalib.settings.Setting import typed_list


@linter(executable='pydocstyle',
        use_stdout=False,
        use_stderr=True,
        output_format='regex',
        output_regex=r'.*:(?P<line>\d+) .+:\n\s+(?P<message>.*)')
class PyDocStyleBear:
    """
    Checks python docstrings.
    """
    LANGUAGES = ("Python", "Python 2", "Python 3")

    @staticmethod
    def create_arguments(filename, file, config_file,
                         pydocstyle_select: typed_list(str)=(),
                         pydocstyle_ignore: typed_list(str)=()):
        """
        :param pydocstyle_select:
            List of checked errors by specifying which errors to check for.
            Can't be used together with ``pydocstyle_ignore``.
        :param pydocstyle_ignore:
            List of checked errors by specifying which errors to ignore. Can't
            be used together with ``pydocstyle_select``.
        """
        args = (filename,)
        if pydocstyle_ignore and pydocstyle_select:
            # TODO there's no self...
            self.err("The arguments pydocstyle_select and pydocstyle_ignore "
                     "are both given but mutually exclusive.")
            return
        elif pydocstyle_ignore:
            ignore = ','.join(part.strip() for part in pydocstyle_ignore)
            args += ("--ignore=" + ignore,)
        elif pydocstyle_select:
            select = ','.join(part.strip() for part in pydocstyle_select)
            args += ("--select=" + select,)

        return args
