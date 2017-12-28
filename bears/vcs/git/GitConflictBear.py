import shutil

from coalib.bears.LocalBear import LocalBear
from coalib.results.Result import Result
from coalib.results.Diff import Diff

# Run test at coala-bears/tests/vcs/git with
# coala --bears=GitConflictBear --files=
# conflict.txt,noconflict.txt
# -L DEBUG --flush-cache


class GitConflictBear(LocalBear):
    LANGUAGES = {'Git'}
    AUTHORS = {'The coala developers'}
    AUTHORS_EMAILS = {'coala-devel@googlegroups.com'}
    LICENSE = 'AGPL-3.0'

    @classmethod
    def check_prerequisites(cls):
        if shutil.which('git') is None:
            return 'git is not installed.'
        else:
            return True

    def run(self, filename, file):
        # Possible parameters : from line, to line
        '''
        Yield results for lines with potential git conflict s
        '''
        self.debug('Checking file', filename, '.')

        merge_conflict_from = -1  # search where the merge conflict begins from
        # this line differentiates merge conflict on local and remote
        split_merge_line = -1
        merge_conflict_to = -1
        remote_commit = ''
        local_commit = ''
        remote_code = ''
        local_changes = ''

        for line_number, line in enumerate(file):
            # check for `merge_conflict_from` only if not found already
            # there could be multiple conflicts in a file
            if merge_conflict_from == -1:
                if(line.startswith('<<<<<<< ')):
                    merge_conflict_from = line_number
                    # get the remote commit
                    if line.find(' ') != -1 and line.find(':') != -1:
                        remote_commit = line[line.find(' ')+1:line.find(':')]
                        # remote_code = ''
                else:
                    local_changes += line
                    remote_code += line

            elif split_merge_line == -1:
                if(line.startswith('=========')):
                    split_merge_line = line_number
                    # local_changes = ''
                else:
                    remote_code += line

            elif merge_conflict_to == -1:
                if(line.startswith('>>>>>>> ')):
                    merge_conflict_to = line_number
                    # get the local commit
                    if line.find(' ') != -1 and line.find(':') != -1:
                        local_commit = line[line.find(' ')+1:line.find(':')]
                        # reset merge variables
                        merge_conflict_from = -1
                        split_merge_line = -1
                        merge_conflict_to = -1
                else:
                    local_changes += line
            # no other condition remains

        if local_changes != remote_code:
            # Write local_changes to file, keep file contents safe
            shutil.copyfile(filename, filename+'.gitorig')

            diffs = Diff.from_string_arrays(file, remote_code).split_diff()
            difft = Diff.from_string_arrays(file, local_changes).split_diff()

            for diff in diffs:
                yield Result(self,
                             'Potential merge conflict found here.',
                             affected_code=(diff.range(remote_code),),
                             diffs={filename: diff})
