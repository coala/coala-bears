from collections import namedtuple
import pkg_resources
import re

from safety import safety

from coalib.bears.LocalBear import LocalBear
from dependency_management.requirements.PipRequirement import PipRequirement
from coalib.results.Result import Result
from coalib.results.SourceRange import SourceRange
from coalib.settings.Setting import typed_list


# the safety module expects an object that looks like this
# (not importing it from there because it's in a private-ish location)
Package = namedtuple('Package', ('key', 'version'))


class PySafetyBear(LocalBear):
    """
    Checks if any of your Python dependencies have known security issues.

    Data is taken from pyup.io's vulnerability database hosted at
    https://github.com/pyupio/safety.
    """

    LANGUAGES = {
        'Python Requirements',
        'Python 2 Requirements',
        'Python 3 Requirements',
    }
    AUTHORS = {'Bence Nagy'}
    REQUIREMENTS = {PipRequirement('safety', '0.5.1')}
    AUTHORS_EMAILS = {'bence@underyx.me'}
    LICENSE = 'AGPL'
    CAN_DETECT = {'Security'}

    def run(self, filename, file):
        """
        Checks for vulnerable package versions in requirements files.
        """
        packages = list(
            Package(key=req.key, version=req.specs[0][1])
            for req in self.try_parse_requirements(file)
            if len(req.specs) == 1 and req.specs[0][0] == '=='
        )

        if not packages:
            return

        for vulnerability in safety.check(packages=packages):
            if vulnerability.is_cve:
                message_template = (
                    '{vuln.name}{vuln.spec} is vulnerable to {vuln.cve_id} '
                    'and your project is using {vuln.version}.'
                )
            else:
                message_template = (
                    '{vuln.name}{vuln.spec} is vulnerable and your project is '
                    'using {vuln.version}.'
                )

            # StopIteration should not ever happen so skipping its branch
            line_number, line = next(  # pragma: no branch
                (index, line) for index, line in enumerate(file, start=1)
                if vulnerability.name in line
            )
            version_spec_match = re.search(r'[=<>]+(\S+?)(?:$|\s|#)', line)
            source_range = SourceRange.from_values(
                filename,
                line_number,
                version_spec_match.start(1) + 1,
                line_number,
                version_spec_match.end(1) + 1,
            )

            yield Result(
                self,
                message_template.format(vuln=vulnerability),
                additional_info=vulnerability.description,
                affected_code=(source_range, ),
            )

    @staticmethod
    def try_parse_requirements(lines: typed_list(str)):
        """
        Yields all package requirements parseable from the given lines.

        :param lines: An iterable of lines from a requirements file.
        """
        for line in lines:
            try:
                yield from pkg_resources.parse_requirements(line)
            except pkg_resources.RequirementParseError:
                # unsupported requirement specification
                pass
