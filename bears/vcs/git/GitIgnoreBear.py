import shutil

from coalib.bears.GlobalBear import GlobalBear
from coalib.misc.Shell import run_shell_command


class GitIgnoreBear(GlobalBear):
    AUTHORS = {'The coala developers'}
    AUTHORS_EMAILS = {'coala-devel@googlegroups.com'}
    LICENSE = 'AGPL-3.0'
    CAN_DETECT = {'Formatting'}
    LANGUAGES = {'Git'}

    @classmethod
    def check_prerequisites(cls):
        if shutil.which('git') is None:
            return 'git is not installed.'
        else:
            return True

    @staticmethod
    def get_ignored_files():
        """
        This function checks for the files that are being tracked
        but are ignored in .gitignore file.
        Visit https://github.com/coala/coala-bears/issues/2610
        for more details.

        :return:
            A list of details of tracked files that are
            ignored in .gitignore file.
        """
        files, _ = run_shell_command('git ls-files')
        files = files.strip().split('\n')
        ignored = list(map(
            lambda file: run_shell_command(
                'git check-ignore --no-index -v {}'.format(file))[0].strip(),
            files
        ))
        return list(filter(lambda f: f != '', ignored))

    def run(self):
        for line in GitIgnoreBear.get_ignored_files():
            pattern, filename = line.split('\t')
            ignore_filename, line_number, ignore_regex = pattern.split(':')
            yield self.new_result(
                message='File {} is being tracked which was ignored in line '
                        'number {} in file {}.'.format(
                            filename, line_number, ignore_filename),
                file=filename)
