from shutil import which
import xml.etree.ElementTree as ET

from coalib.bears.GlobalBear import GlobalBear
from coalib.misc.Shell import run_shell_command
from coalib.results.Result import Result
from coalib.results.SourceRange import SourceRange


class CPDBear(GlobalBear):

    LANGUAGES = ('C++', 'C#', 'Objective C', 'Java', 'JavaScript', 'Fortran',
                 'Go', 'JSP', 'Python 2', 'Python 3', 'Python', 'Ruby',
                 'PHP', 'Scala')

    @classmethod
    def check_prerequisites(cls):  # pragma: no cover
        if which("bash") is None:
            return "bash is not installed."
        elif which("run.sh") is None:
            return ("CPD is missing. Make sure to install it from "
                    "<https://pmd.github.io/>")
        else:
            return True

    def run(self, language: str, minimum_tokens: int=20,
            ignore_annotations: bool=False, ignore_identifiers: bool=True,
            ignore_literals: bool=False, ignore_usings: bool=False,
            skip_duplicate_files: bool=True):
        """
        Checks for similar code that looks as it could be replaced to reduce
        redundancy.

        For more details see:
        <https://pmd.github.io/pmd-5.4.1/usage/cpd-usage.html>

        :param language:
            One of "cpp", "cs", "js", "f", "go", "jsp", "m", "php", "py",
            "rb", "scala", "java" (i.e. the file ending of your language).
        :param minimum_tokens:
            The minimum token length which should be reported as a duplicate.
        :param ignore_annotations:
            Ignore language annotations when comparing text.
        :param ignore_identifiers:
            Ignore constant and variable names when comparing text.
        :param ignore_literals:
            Ignore number values and string contents when comparing text.
        :param ignore_usings:
            Ignore ``using`` directives in C#.
        :param skip_duplicate_files:
            Ignore multiple copies of files of the same name and length in
            omparison.
        """
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
            "java": "java"}

        if language not in language_args:  # pragma: no cover
            self.err("This bear does not support files with the extension "
                     "'{}'.".format(language))
            return

        options = {
            "--ignore-annotations": ignore_annotations,
            "--ignore-identifiers": ignore_identifiers,
            "--ignore-literals": ignore_literals,
            "--ignore-usings": ignore_usings,
            "--skip-duplicate-files": skip_duplicate_files}

        files = ",".join(self.file_dict.keys())
        arguments = ("bash", which("run.sh"), "cpd", "--skip-lexical-errors",
                     "--minimum-tokens", str(minimum_tokens),
                     "--language", language_args[language],
                     "--files", files,
                     "--format", "xml")

        arguments += tuple(option
                           for option, enable in options.items()
                           if enable is True)

        stdout_output, _ = run_shell_command(arguments)

        if stdout_output:
            root = ET.fromstring(stdout_output)

            for duplication in root.findall('duplication'):
                length = int(duplication.attrib['lines'])
                affected_code = list()

                for file in duplication.findall('file'):
                    filename = file.attrib['path']
                    start_line = int(file.attrib['line'])
                    end_line = min(start_line + length - 1, len(file))

                    affected_code.append(
                        SourceRange.from_values(filename,
                                                start_line=start_line,
                                                end_line=end_line))

                yield Result(
                    self, "Duplicate code found.", affected_code,
                    additional_info=(
                        "Duplicate code is an indicator "
                        "that you have more code than you need. Consider"
                        " refactor your code to remove one of the"
                        " occurrences. For more information go here:"
                        "http://tinyurl.com/coala-clone"))
