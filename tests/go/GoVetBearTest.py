import os
from queue import Queue
from shutil import which
from unittest.case import skipIf

from bears.go.GoVetBear import GoVetBear
from coalib.testing.LocalBearTestHelper import LocalBearTestHelper
from coalib.settings.Section import Section
from coalib.settings.Setting import Setting


@skipIf(which('go') is None, 'go is not installed')
class GoVetBearTest(LocalBearTestHelper):

    def setUp(self):
        self.section = Section('test section')
        self.uut = GoVetBear(self.section, Queue())
        self.good_file = os.path.join(os.path.dirname(__file__),
                                      'test_files',
                                      'vet_good.go')
        self.bad_file = os.path.join(os.path.dirname(__file__),
                                     'test_files',
                                     'vet_bad.go')

    def test_run(self):
        self.check_validity(self.uut, [], self.good_file)
        self.check_invalidity(self.uut, [], self.bad_file)

    def test_args(self):
        self.section.append(Setting('disallow_assembly_go_mismatches', True))
        self.section.append(Setting('check_useless_assignments', True))
        self.section.append(Setting('check_sync_package_mistakes', True))
        self.section.append(Setting('check_boolean_operator_mistakes', True))
        self.section.append(Setting('disallow_bad_build_tags', True))
        self.section.append(Setting('disallow_cgo_pointer_violations', True))
        self.section.append(Setting('disallow_unkeyed_composites', True))
        self.section.append(Setting('disallow_copying_locks', True))
        self.section.append(Setting('check_method_signatures', True))
        self.section.append(Setting('disallow_nil_function_comparisons', True))
        self.section.append(Setting('check_printf_calls', True))
        self.section.append(Setting('check_range_loop_variables', True))
        self.section.append(Setting('check_shadow_variables', True))
        self.section.append(Setting('check_shifts', True))
        self.section.append(Setting('check_struct_tag_format', True))
        self.section.append(Setting('disallow_unreachable_code', True))
        self.section.append(Setting('disallow_unsafe_pointers', True))
        self.section.append(Setting('disallow_unused_results', True))
        self.check_validity(self.uut, [], self.good_file)
        self.check_invalidity(self.uut, [], self.bad_file)
