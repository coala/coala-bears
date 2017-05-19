from queue import Queue

from bears.go.GofmtBear import GofmtBear
from coalib.testing.LocalBearTestHelper import LocalBearTestHelper, \
    execute_bear

from coalib.settings.Section import Section
from coala_utils.ContextManagers import prepare_file


in_file1 = """package main
func main() {
    return 1
}"""

out_file1 = """package main

func main() {
    return 1
}
"""

simplify_in_file1 = """package main

func main() {
    array := []int{0, 2}
    array2 := array[1:len(array)]
    return 1
}
"""

simplify_out_file1 = """package main

func main() {
    array := []int{0, 2}
    array2 := array[1:]
    return 1
}
"""

in_file1 = in_file1.replace(' ' * 4, '\t')
out_file1 = out_file1.replace(' ' * 4, '\t')
simplify_in_file1 = simplify_in_file1.replace(' ' * 4, '\t')
simplify_out_file1 = simplify_out_file1.replace(' ' * 4, '\t')


class GofmtBearTest(LocalBearTestHelper):

    def setUp(self):
        self.section = Section('')
        self.uut = GofmtBear(self.section, Queue())

    def test_without_simplify(self):
        content = in_file1.splitlines()
        with prepare_file(content, None) as (file, fname):
            with execute_bear(self.uut, fname, file) as results:
                fdict = {fname: file}
                results[0].apply(fdict)
                self.assertEqual(''.join(fdict[fname]), out_file1)

<<<<<<< HEAD
GofmtBearTest = verify_local_bear(
    GofmtBear,
    ('package main\n\nfunc main() {\n\treturn 1\n}',),
    ('package main\nfunc main() {\n\treturn 1\n}',))
=======
    def test_with_simplify(self):
        content = simplify_in_file1.splitlines()
        with prepare_file(content, None) as (file, fname):
            with execute_bear(self.uut, fname, file, simplify='true'
                              ) as results:
                fdict = {fname: file}
                results[0].apply(fdict)
                self.assertEqual(''.join(fdict[fname]), simplify_out_file1)
>>>>>>> 2ce3fa3... PycodeStyleBear.py: Use 'typed_list(str)'
