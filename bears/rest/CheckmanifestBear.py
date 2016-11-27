import os

from coalib.bearlib.abstractions.Linter import linter
from coalib.bears.requirements.PipRequirement import PipRequirement
from coalib.results.RESULT_SEVERITY import RESULT_SEVERITY


@linter(executable='check-manifest',
        output_format='corrected',)
class CheckmanifestBear:
    """
    Check MANIFEST.in in a Python source package for completeness

    Check <https://pypi.python.org/pypi/rstcheck> for more information.
    """

    LANGUAGES = {'MANIFEST.in'}
    REQUIREMENTS = {PipRequirement('check-manifest', '0.34')}
    AUTHORS = {'The coala developers'}
    AUTHORS_EMAILS = {'coala-devel@googlegroups.com'}
    LICENSE = 'AGPL-3.0'
    CAN_DETECT = {'Redundancy'}

    @staticmethod
    def create_arguments(filename, file, config_file,
                         create: bool=False, update: bool=False,
                         ignore: list=None):
        """
        :param create:
            create a MANIFEST.in if missing.
        :param update:
            append suggestions to MANIFEST.in (implies --create).
        :param ignore:
            ignore files/directories matching these comma-
            separated patterns
        """
        extra = ''
        if create:
            extra += '-c '
        if update:
            extra += '-u '
        args = ()
        if ignore:
          args = (extra + '--ignore=' +
                  ','.join(ignore),)
        return args + (os.path.dirname(filename),)
