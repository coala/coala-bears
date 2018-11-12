import os
from collections import namedtuple
import pkg_resources
import re

from safety import safety

from coalib.bears.LocalBear import LocalBear
from dependency_management.requirements.PipRequirement import PipRequirement
from coalib.results.Result import Result
from coalib.settings.Setting import path
from coalib.results.SourceRange import SourceRange
from coalib.settings.Setting import typed_list


# It was for old versions of safety and those versions will be allow in future.
def cve_key_checker(vulnerability):
    if 'cve' in vulnerability.data:
        if vulnerability.data['cve'] is None:
            return None
        else:
            return True
    else:
        return None


# the safety module expects an object that looks like this
# (not importing it from there because it's in a private-ish location)
Package = namedtuple('Package', ('key', 'version'))

safety_get_vulnerabilities = safety.get_vulnerabilities
_insecure_full_json_url = ('https://raw.githubusercontent.com/pyupio/'
                           'safety-db/master/data/insecure_full.json')

_insecure_json_url = ('https://raw.githubusercontent.com/'
                      'pyupio/safety-db/master/data/insecure.json')


def _get_vulnerabilities(pkg, spec, db):
    for entry in safety_get_vulnerabilities(pkg, spec, db):
        entry['cve'] = entry['id'] if entry['cve'] is None else entry['cve']
        entry['id'] = entry['cve']
        yield entry


safety.get_vulnerabilities = _get_vulnerabilities


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
    REQUIREMENTS = {PipRequirement('safety', '1.8.2')}
    AUTHORS_EMAILS = {'bence@underyx.me'}
    LICENSE = 'AGPL'
    CAN_DETECT = {'Security'}

    def setup_dependencies(self):
        file = self.download_cached_file(_insecure_full_json_url,
                                         'insecure_full.json')
        self.download_cached_file(_insecure_json_url,
                                  'insecure.json')
        type(self).db_path = os.path.dirname(file)

    def run(self, filename, file,
            db_path: path = '',
            cve_ignore: typed_list(str) = []):
        """
        Checks for vulnerable package versions in requirements files.

        :param db_path:           Path to a local vulnerability database.
        :param cve_ignore:        A list of CVE number to be ignore.
        """
        db_path = self.db_path if not db_path else db_path
        packages = list(
            Package(key=req.key, version=req.specs[0][1])
            for req in self.try_parse_requirements(file)
            if len(req.specs) == 1 and req.specs[0][0] == '=='
        )

        if not packages:
            return

        for vulnerability in safety.check(packages, key=None,
                                          db_mirror=db_path, cached=False,
                                          ignore_ids=cve_ignore):
            if 'cve' in vulnerability.vuln_id.strip().lower():
                message_template = (
                    '{vuln.name}{vuln.spec} is vulnerable to {vuln.vuln_id} '
                    'and your project is using {vuln.version}.'
                )
            else:
                message_template = (
                    '{vuln.name}{vuln.spec} is vulnerable to '
                    'pyup.io-{vuln.vuln_id} and your project is using '
                    '{vuln.version}.'
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
                additional_info=vulnerability.advisory,
                affected_code=(source_range, ),
            )

    @staticmethod
    def try_parse_requirements(lines: typed_list(str)):
        """
        Yields all package requirements parsable from the given lines.

        :param lines: An iterable of lines from a requirements file.
        """
        for line in lines:
            try:
                yield from pkg_resources.parse_requirements(line)
            except pkg_resources.RequirementParseError:
                # unsupported requirement specification
                pass
