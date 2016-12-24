from bears.go.GoReturnsBear import GoReturnsBear
from coalib.testing.LocalBearTestHelper import verify_local_bear

good_file1 = """import "errors"

func F() (*MyType, int, error) { return nil, 0, errors.New("foo") }"""

good_file2 = """package main

import "os"

func main() {
\tf, _ := os.Open("foo")
}"""

bad_file1 = """
func F() (*MyType, int, error) { return errors.New("foo") }
"""

bad_file2 = """
package main

func main() {
    f, _ := os.Open("foo")
    return nil, 0, errors.New("foo")
}

"""

GoReturnsBearTest = verify_local_bear(
    GoReturnsBear,
    (good_file1, good_file2,),
    (bad_file1, bad_file2,))
