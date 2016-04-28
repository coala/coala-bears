from coalib.bearlib.abstractions.Lint import Lint
from coalib.bears.LocalBear import LocalBear
from coalib.settings.Setting import typed_list


class PyDocStyleBear(LocalBear, Lint):
    executable = 'pydocstyle'
    output_regex = r'(.*\.py):(?P<line>\d+) (.+):\n\s+(?P<message>.*)'
    use_stderr = True
    LANGUAGES = ("Python", "Python 2", "Python 3")

    def run(self,
            filename,
            file,
            pydocstyle_select: typed_list(str)=(),
            pydocstyle_ignore: typed_list(str)=()):
        '''
        Checks python docstrings.

        :param pydocstyle_select:      List of checked errors by specifying
                                       which errors to check for.
        :param pydocstyle_ignore:      List of checked errors by specifying
                                       which errors to ignore.

        Note: pydocstyle_select and pydocstyle_ignore are mutually exclusive.
              They cannot be used together.

        '''
        self.arguments = '{filename}'
        if pydocstyle_ignore and pydocstyle_select:
            self.err("The arguments pydocstyle_select and pydocstyle_ignore "
                     "are both given but mutually exclusive.")
            return
        elif pydocstyle_ignore:
            ignore = ','.join(part.strip() for part in pydocstyle_ignore)
            self.arguments += " --ignore={}".format(ignore)
        elif pydocstyle_select:
            select = ','.join(part.strip() for part in pydocstyle_select)
            self.arguments += " --select={} ".format(select)
        return self.lint(filename, file)
