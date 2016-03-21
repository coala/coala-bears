from bears.go.GoErrCheckBear import GoErrCheckBear
from tests.LocalBearTestHelper import verify_local_bear

good_file = """package main

import "fmt"

func main() {
    fmt.Println("Hello, Arch!")
}
""".splitlines(keepends=True)


bad_file = """package main

import "os"

func main() {
f, _ := os.Open("foo")
f.Write([]byte("Hello, world."))
f.Close()
}
""".splitlines(keepends=True)


GoErrCheckBearTest = verify_local_bear(GoErrCheckBear,
                                       valid_files=(good_file,),
                                       invalid_files=(bad_file,))
