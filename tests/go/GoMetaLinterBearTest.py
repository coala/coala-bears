from bears.go.GoMetaLinterBear import GoMetaLinterBear
from coalib.testing.LocalBearTestHelper import verify_local_bear

good_file_errcheck = """package main
import "fmt"
func main() {
    fmt.Println("Hello, Arch!")
}
"""

bad_file_errcheck = """package main
import "os"
func main() {
f, _ := os.Open("foo")
f.Write([]byte("Hello, world."))
f.Close()
}
"""

good_file_imports = """package main

import "os"

func main() {
\tf, _ := os.Open("foo")
}"""

bad_file_imports = """package main


func main() {
\tf, _ := os.Open("foo")
}"""


GoMetaLinterBearTest = verify_local_bear(GoMetaLinterBear,
                                         valid_files=(good_file_errcheck,
                                                      bad_file_imports),
                                         invalid_files=(bad_file_errcheck,
                                                        good_file_imports))
