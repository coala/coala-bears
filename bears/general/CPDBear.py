import re
import os

from coalib.bearlib.abstractions.Lint import Lint
from coalib.bears.LocalBear import LocalBear


class CPDBear(LocalBear, Lint):
    executable = 'run.sh'
    arguments = "cpd --minimum-tokens 10 --files {filename}"
    output_regex = re.compile(
        r'(?P<message>.*) in .*\n'
        r'[A-Za-z ]*(?P<line>[0-9]+).*\n')

    def run(self, filename, file):
        '''
        Checks duplicate code with ``CPD``.
        CPD offers support for:
        - C++, C#, Objective C
        - Java, JavaScript, JSP
        - Python, Ruby, Go, PHP, Scala, Fortran
        '''
        language_args = {
            "cpp": "cpp",
            "cs": "cs",
            "js": "ecmascript",
            "f": "fortran",
            "go": "go",
            "jsp": "jsp",
            "m": "objectivec",
            "php": "php",
            "py": "python",
            "rb": "ruby",
            "scala": "scala",
            "java": "java"
        }
        _, extension = os.path.splitext(filename)
        extension = extension[1:]  # remove period
        self.arguments += " --language {}".format(language_args.get(extension,
                                                                    extension))
        return self.lint(filename)
