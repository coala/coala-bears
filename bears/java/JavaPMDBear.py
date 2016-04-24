import re

from coalib.bearlib.abstractions.Lint import Lint
from coalib.bears.LocalBear import LocalBear


class JavaPMDBear(LocalBear, Lint):
    executable = 'run.sh'
    output_regex = re.compile(
        r'(?P<file_name>.+):'
        r'(?P<line>.+):'
        r'(?P<message>.*)')

    def run(self, filename, file, check_best_practices: bool=True,
            check_braces: bool=True, check_clone_implementation: bool=True,
            check_code_size: bool=True, check_comments: bool=True,
            check_controversial: bool=False):
        """
        Checks Java source-code for various problems.

        (``PMD`` is used internally.)

        :param check_best_practices:
            Activate to check for best practices. See
            http://pmd.github.io/pmd-5.4.1/pmd-java/rules/index.html#Basic for
            more information on what this contains.
        :param check_braces:
            Check for the right use of braces. See
            http://pmd.github.io/pmd-5.4.1/pmd-java/rules/index.html#Braces
            for more information on this matter.
        :param check_clone_implementation:
            Check for the right implementation of the ``clone()`` function. See
            http://pmd.github.io/pmd-5.4.1/pmd-java/rules/index.html#Clone_Implementation
            for more information on this matter.
        :param check_code_size:
            Check for large or complicated code constructs. See
            http://pmd.github.io/pmd-5.4.1/pmd-java/rules/index.html#Code_Size
            for more information on this matter.
        :param check_comments:
            Check comments for length, content and placement. See
            http://pmd.github.io/pmd-5.4.1/pmd-java/rules/index.html#Comments
            for more information on this matter.
        :param check_controversial:
            Does various checks that are considered controversial. See
            http://pmd.github.io/pmd-5.4.1/pmd-java/rules/index.html#Controversial
            for more information on this matter.
        :param :
            Check for the right use of . See
            http://pmd.github.io/pmd-5.4.1/pmd-java/rules/index.html#
            for more information on this matter.
        """
        options = {
            "java-basic": check_best_practices,
            "java-braces": check_braces,
            "java-clone": check_clone_implementation,
            "java-codesize": check_code_size,
            "java-comments": check_comments,
            "java-controversial": check_controversial,
            "java-design"
            "java-imports"
            "java-naming"
            "java-optimizations"
            "java-strings"
            "java-unnecessary"
            "java-unusedcode"
        }
        rules = ','.join(key for key, value in options if value)

        self.arguments = "pmd -R " + rules + " -d {filename}"
        return self.lint(filename)
