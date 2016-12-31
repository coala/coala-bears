from collections import namedtuple
import textwrap
import sys

from coalib.bearlib.abstractions.Linter import linter
from dependency_management.requirements.PipRequirement import PipRequirement


class FlagInfo(namedtuple('FlagInfo', 'arg doc inverse')):
    """
    Information about a command-line flag.

    :param arg:
        The argument to pass to enable the flag.
    :param doc:
        A help text for the flag.
    :param inverse:
        Set to ``True`` when the coala option is the inverse of
        the subprocess one, for example coala's ``allow_untyped_calls``
        is the inverse of mypy's ``--disallow-untyped-calls``.
    """

    def want_flag(self, value):
        """
        Check if the flag should be added to the argument list.

        :param value: The configuration value.
        :return:      The flag value, may be negated if the flag specifies so.
        """

        if self.inverse:
            value = not value
        return value


FLAG_MAP = {
    'allow_untyped_functions': FlagInfo(
        arg='--disallow-untyped-defs',
        doc='Allow defining functions without type annotations or with '
            'incomplete type annotations.',
        inverse=True),
    'allow_untyped_calls': FlagInfo(
        arg='--disallow-untyped-calls',
        doc='Allow calling functions without type annotations from '
            'typed functions.',
        inverse=True),
    'check_untyped_function_bodies': FlagInfo(
        arg='--check-untyped-defs',
        doc='Do not check the interior of functions without type annotations.',
        inverse=False),
    'strict_optional': FlagInfo(
        arg='--strict-optional',
        doc='Enable experimental strict checks related to Optional types. See '
            '<http://mypy-lang.blogspot.com.es/2016/07/mypy-043-released.html>'
            ' for an explanation.',
        inverse=False),
}


def add_param_docs(param_map):
    """
    Append documentation from FLAG_MAP to a function's docstring.

    :param param_map:
        A mapping of argument names (strings) to FlagInfo objects.
    :return:
        A decorator that appends flag information to a function's docstring.
    """
    def decorator(func):
        func.__doc__ = textwrap.dedent(func.__doc__) + '\n'.join(
            ':param {}:\n{}'.format(name, textwrap.indent(arg.doc, '    '))
            for name, arg in param_map.items())
        return func
    return decorator


# Mypy generates messages in the format:
#    blabla.py: note: In function "f":
#    blabla.py:2: error: Unsupported operand types for ...
# The "note" messages are only adding info coala should already know,
# so discard those. We're only capturing the errors.
@linter(executable=sys.executable,
        prerequisite_check_command=(sys.executable, '-m', 'mypy', '-V'),
        output_format='regex',
        output_regex=r'[^:]+:(?:(?P<line>\d+):)? '
                      '(?P<severity>error): (?P<message>.*)')
class MypyBear:
    """
    Type-checks your Python files!

    Checks optional static typing using the mypy tool.
    See <http://mypy.readthedocs.io/en/latest/basics.html> for info on how to
    add static typing.
    """

    LANGUAGES = {'Python', 'Python 2', 'Python 3'}
    AUTHORS = {'Petr Viktorin'}
    REQUIREMENTS = {PipRequirement('mypy-lang', '0.4.6')}
    AUTHORS_EMAILS = {'encukou@gmail.com'}
    LICENSE = 'AGPL-3.0'
    ASCIINEMA_URL = 'https://asciinema.org/a/90736'

    # This detects typing errors, which is pretty unique -- it doesn't
    # make sense to add a category for it.
    CAN_DETECT = set()

    @add_param_docs(FLAG_MAP)
    def create_arguments(self, filename, file, config_file,
                         language: str='Python 3',
                         python_version: str=None,
                         allow_untyped_functions: bool=True,
                         allow_untyped_calls: bool=True,
                         check_untyped_function_bodies: bool=False,
                         strict_optional: bool=False):
        """
        :param language:
            Set to ``Python`` or ``Python 3`` to check Python 3.x source.
            Use ``Python 2`` for Python 2.x.
        :param python_version:
            Set the specific Python version, e.g. ``3.5``.
        """
        args = ['-m', 'mypy']
        if language.lower() == 'python 2':
            args.append('--py2')
        elif language.lower() not in ('python 3', 'python'):
            # Ideally, this would fail the check, but there's no good
            # way to fail from create_arguments.
            # See https://github.com/coala-analyzer/coala/issues/2573
            self.err(
                'Language needs to be "Python", "Python 2" or "Python 3". '
                'Assuming Python 3.')
        if python_version:
            args.extend(['--python-version', python_version])
        loc = locals()
        args.extend(flag.arg for name, flag in FLAG_MAP.items()
                    if flag.want_flag(loc[name]))
        args.append(filename)
        return args
