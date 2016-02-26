from bears.CheckPrerequisites import check_linter_prerequisites_builder


class Dummy:
    pass


def check_linter_prerequisites_builder_invalid_executable_test():
    executable = 'invalid_executable'
    executable_fail_message = executable + ' is not installed.'
    check_linter_prerequisites = check_linter_prerequisites_builder(
                               executable,
                               [],
                               ""
                               )
    assert check_linter_prerequisites(Dummy) == executable_fail_message


def check_linter_prerequisites_builder_valid_executable_test():
    executable = 'java'
    check_linter_prerequisites = check_linter_prerequisites_builder(
                               executable,
                               ['java', '-version'],
                               ''
                               )
    assert check_linter_prerequisites(Dummy) == True


def check_linter_prerequisites_builder_invalid_options_test():
    executable = 'java'
    options_fail_msg = 'invalid option'
    check_linter_prerequisites = check_linter_prerequisites_builder(
                               executable,
                               ['java', '-v'],
                               options_fail_msg
                               )
    assert check_linter_prerequisites(Dummy) == options_fail_msg
