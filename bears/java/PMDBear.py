import re

from coalib.bearlib.abstractions.Lint import Lint
from coalib.bears.LocalBear import LocalBear


class PMDBear(LocalBear, Lint):
    executable = 'run.sh'
    arguments = "pmd -R java-basic," + \
                "java-braces," + \
                "java-clone," + \
                "java-codesize," + \
                "java-controversial," + \
                "java-design," + \
                "java-imports," + \
                "java-naming," + \
                "java-optimizations," + \
                "java-strings," + \
                "java-unnecessary," + \
                "java-unusedcode" + \
                " -d {filename}"
    output_regex = re.compile(
        r'(?P<file_name>.+):'
        r'(?P<line>.+):'
        r'(?P<message>.*)')

    def run(self, filename, file):
        '''
        Checks Java source-code with ``PMD``.
        '''
        return self.lint(filename)
