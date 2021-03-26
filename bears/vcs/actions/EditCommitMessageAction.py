import subprocess
from coalib.results.result_actions.ResultAction import ResultAction


class EditCommitMessageAction(ResultAction):
    """
    Opens an editor to edit the commit message of the HEAD commit.
    """

    SUCCESS_MESSAGE = 'Commit message edited successfully.'

    def apply(self, result, original_file_dict, file_diff_dict):
        """
        Edit (C)ommit Message [Note: This may rewrite your commit history]
        """
        subprocess.check_call(['git', 'commit', '-o', '--amend'])
        return file_diff_dict
