from coalib.misc.Shell import run_shell_command
from coalib.results.result_actions.ResultAction import ResultAction


class AddNewlineAction(ResultAction):
    """
    Adds a newline between shortlog and body of the commit message
    of the HEAD commit.
    """

    SUCCESS_MESSAGE = 'New Line added successfully.'

    def is_applicable(self,
                      result,
                      original_file_dict,
                      file_diff_dict,
                      applied_actions=()):
        new_message, _ = run_shell_command('git log -1 --pretty=%B')
        new_message = new_message.rstrip('\n')
        pos = new_message.find('\n')
        self.shortlog = new_message[:pos] if pos != -1 else new_message
        self.body = new_message[pos+1:] if pos != -1 else ''
        if self.body[0] != '\n':
            return True
        else:
            return False

    def apply(self, result, original_file_dict, file_diff_dict):
        """
        Add New(L)ine [Note: This may rewrite your commit history]
        """
        new_commit_message = '{}\n\n{}'.format(self.shortlog, self.body)
        command = 'git commit -o --amend -m "{}"'.format(new_commit_message)
        stdout, err = run_shell_command(command)
        return file_diff_dict
