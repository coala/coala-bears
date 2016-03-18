from shutil import which

from coalib.bearlib.abstractions.Linter import linter


@linter("bash", output_format="regex",
        output_regex=r'.+:(?P<line>.+):(?P<message>.*)')
class JavaPMDBear:
    """
    Check Java code for possible issues like potential bugs, dead code or too
    complicated expressions.

    More information is available at
    <http://pmd.github.io/pmd-5.4.1/pmd-java/rules/index.html>.
    """

    LANGUAGES = "Java"

    @classmethod
    def check_prerequisites(cls):  # pragma: no cover
        if which("bash") is None:
            return "bash is not installed."
        elif which("run.sh") is None:
            return ("PMD is missing. Make sure to install it from "
                    "<https://pmd.github.io/>")
        else:
            return True

    @staticmethod
    def create_arguments(filename, file, config_file,
                         check_best_practices: bool = True,
                         check_braces: bool = True,
                         check_clone_implementation: bool = True,
                         check_code_size: bool = True,
                         check_comments: bool = False,
                         check_controversial: bool = False,
                         check_design: bool = False,
                         check_imports: bool = True, check_naming: bool = True,
                         check_optimizations: bool = False,
                         check_strings: bool = False,
                         check_unnecessary: bool = True,
                         check_unused: bool = True):
        """
        :param check_best_practices:
            Activate to check for best practices.
        :param check_braces:
            Check for the right use of braces.
        :param check_clone_implementation:
            Check for the right implementation of the ``clone()`` function.
        :param check_code_size:
            Check for large or complicated code constructs.
        :param check_comments:
            Check comments for length, content and placement.
        :param check_controversial:
            Does various checks that are considered controversial.
        :param check_design:
            Check for optimal code implementations. Alternate approaches
            are suggested.
        :param check_imports:
            Check for duplicate and unused imports.
        :param check_naming:
            Check the names of identifiers against some rules.
        :param check_optimizations:
            Check for best pratices regarding optimization.
        :param check_strings:
            Check for String, StringBuffer and StringBuilder instances.
        :param check_unnecessary:
            Checks for unnecessary code.
        :param check_unused:
            Check for unused code.
        """
        options = {
            "java-basic": check_best_practices,
            "java-braces": check_braces,
            "java-clone": check_clone_implementation,
            "java-codesize": check_code_size,
            "java-comments": check_comments,
            "java-controversial": check_controversial,
            "java-design": check_design,
            "java-imports": check_imports,
            "java-naming": check_naming,
            "java-optimizations": check_optimizations,
            "java-strings": check_strings,
            "java-unnecessary": check_unnecessary,
            "java-unusedcode": check_unused}
        rules = ','.join(key for key in options if options[key])

        return which("run.sh"), "pmd", "-R", rules, "-d", filename
