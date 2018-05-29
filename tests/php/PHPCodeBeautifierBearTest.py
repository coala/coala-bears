from queue import Queue

from bears.php.PHPCodeBeautifierBear import PHPCodeBeautifierBear
from coalib.testing.LocalBearTestHelper import LocalBearTestHelper, \
    execute_bear

from coalib.settings.Section import Section
from coalib.settings.Setting import Setting
from coala_utils.ContextManagers import prepare_file


in_file1 = """<?php
$var = false;
echo $var;
>
"""

out_file1 = """<?php
$var = false;
echo $var;
>
"""

in_file1 = in_file1.replace(' ' * 4, '\t')
out_file1 = out_file1.replace(' ' * 4, '\t')


class PHPCodeBeautifierBearTest(LocalBearTestHelper):

    def setUp(self):
        self.section = Section('')
        self.uut = PHPCodeBeautifierBear(self.section, Queue())

    def test_without_simplify(self):
        content = in_file1.splitlines()
        with prepare_file(content, None) as (file, fname):
            with execute_bear(self.uut, fname, file
                              ) as results:
                fdict = {fname: file}
                self.assertEqual(''.join(fdict[fname]), out_file1)

    def test_with_simplify(self):
        self.section.append(Setting('fix_error_and_warning', 'true'))
        self.check_validity(self.uut, ['<?php',
                                       '$var = False;',
                                       'echo $var;',
                                       '>'], valid=False)
