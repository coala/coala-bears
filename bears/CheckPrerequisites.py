import shutil
import subprocess


def check_linter_prerequisites_builder(executable,
                                       prerequisites_args_list,
                                       prerequisites_fail_msg):
    '''
    Checks whether prerequisites are installed for a linter and valid flags
    are given with the command.

    :executable:              A valid executable binary
    :prerequisites_args_list: List of arguments for executable
    :prerequisites_fail_msg:  Message returned in case of invalid arguments
    '''
    def check_linter_prerequisites(cls):
        if shutil.which(executable) is None:
            return executable + " is not installed."
        else:
            exitcode = subprocess.call(prerequisites_args_list)
            if exitcode != 0:
                return (prerequisites_fail_msg)
            else:
                return True
    return check_linter_prerequisites
