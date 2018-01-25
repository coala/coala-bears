from itertools import compress

from coalib.bearlib.abstractions.Linter import linter
from dependency_management.requirements.GoRequirement import GoRequirement


@linter(executable='go',
        use_stdout=False,
        use_stderr=True,
        output_format='regex',
        output_regex=r'.+:(?P<line>\d+): (?P<message>.*)')
class GoVetBear:
    """
    Analyze Go code and raise suspicious constructs, such as printf calls
    whose arguments do not correctly match the format string, useless
    assignments, common mistakes about boolean operations, unreachable code,
    etc.

    This is done using the ``vet`` command. For more information visit
    <https://golang.org/cmd/vet/>.
    """
    LANGUAGES = {'Go'}
    REQUIREMENTS = {GoRequirement(package='golang.org/cmd/vet', flag='-u')}
    AUTHORS = {'The coala developers'}
    AUTHORS_EMAILS = {'coala-devel@googlegroups.com'}
    LICENSE = 'AGPL-3.0'
    CAN_DETECT = {'Unused Code', 'Smell', 'Unreachable Code'}

    @staticmethod
    def create_arguments(filename, file, config_file,
                         disallow_assembly_go_mismatches: bool=False,
                         check_useless_assignments: bool=False,
                         check_sync_package_mistakes: bool=False,
                         check_boolean_operator_mistakes: bool=False,
                         disallow_bad_build_tags: bool=False,
                         disallow_cgo_pointer_violations: bool=False,
                         disallow_unkeyed_composites: bool=False,
                         disallow_copying_locks: bool=False,
                         check_method_signatures: bool=False,
                         disallow_nil_function_comparisons: bool=False,
                         check_printf_calls: bool=False,
                         check_range_loop_variables: bool=False,
                         check_shadow_variables: bool=False,
                         check_shifts: bool=False,
                         check_struct_tag_format: bool=False,
                         disallow_unreachable_code: bool=False,
                         disallow_unsafe_pointers: bool=False,
                         disallow_unused_results: bool=False):
        """
        :param disallow_assembly_go_mismatches:
            Mismatches between assembly files and Go function declarations.
        :param check_useless_assignments:
            Check for useless assignments.
        :param check_sync_package_mistakes:
            Common mistaken usages of the sync/atomic package.
        :param check_boolean_operator_mistakes:
            Mistakes involving boolean operators.
        :param disallow_bad_build_tags:
            Badly formed or misplaced +build tags.
        :param disallow_cgo_pointer_violations:
            Detect some violations of the cgo pointer passing rules.
        :param disallow_unkeyed_composites:
            Composite struct literals that do not use the field-keyed syntax.
        :param disallow_copying_locks:
            Locks that are erroneously passed by value.
        :param check_method_signatures:
            Non-standard signatures for methods with familiar names, including:
            Format, GobEncode, GobDecode, MarshalJSON, MarshalXML, Peek,
            ReadByte,ReadFrom, ReadRune, Scan, Seek, UnmarshalJSON, UnreadByte,
            UnreadRune, WriteByte, WriteTo
        :param disallow_nil_function_comparisons:
            Comparisons between functions and nil.
        :param check_printf_calls:
            Suspicious calls to functions in the ``Printf`` family.
        :param check_range_loop_variables:
            Incorrect uses of range loop variables in closures.
        :param check_shadow_variables:
            Variables that may have been unintentionally shadowed.
        :param check_shifts:
            Shifts equal to or longer than the variable's length.
        :param check_struct_tag_format:
            Struct tags that do not follow the format understood by
            ``reflect.StructTag.Get``. Well-known encoding struct tags
            (json, xml) used with unexported fields.
        :param disallow_unreachable_code:
            Unreachable code.
        :param disallow_unsafe_pointers:
            Likely incorrect uses of ``unsafe.Pointer`` to convert integers to
            pointers.
        :param disallow_unused_results:
            Calls to well-known functions and methods that return a value that
            is discarded.
        """
        # Every check in Vet is true by default.
        # Adding a flag set to True enables that check and disables all other
        # checks.
        # Adding a flag set to False disables that check and runs all
        # other checks.
        # Multiple checks can be enabled and/or disabled at once.
        options = {'-asmdecl': disallow_assembly_go_mismatches,
                   '-assign': check_useless_assignments,
                   '-atomic': check_sync_package_mistakes,
                   '-bool': check_boolean_operator_mistakes,
                   '-buildtags': disallow_bad_build_tags,
                   '-cgocall': disallow_cgo_pointer_violations,
                   '-composites': disallow_unkeyed_composites,
                   '-copylocks': disallow_copying_locks,
                   '-methods': check_method_signatures,
                   '-nilfunc': disallow_nil_function_comparisons,
                   '-printf': check_printf_calls,
                   '-rangeloops': check_range_loop_variables,
                   '-shadow': check_shadow_variables,
                   '-shift': check_shifts,
                   '-structtags': check_struct_tag_format,
                   '-unreachable': disallow_unreachable_code,
                   '-unsafeptr': disallow_unsafe_pointers,
                   '-unusedresult': disallow_unused_results}
        args = ['{}=true'.format(op) for op in compress(options.keys(),
                                                        options.values())]
        return ['tool', 'vet'] + args + [filename]
