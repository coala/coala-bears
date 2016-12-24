from bears.go.GoErrCheckBear import GoErrCheckBear
from coalib.testing.LocalBearTestHelper import verify_local_bear

good_file = """package main
import "fmt"
func main() {
    fmt.Println("Hello, Arch!")
}
"""


bad_file = """package main
import "os"
func main() {
f, _ := os.Open("foo")
f.Write([]byte("Hello, world."))
f.Close()
}
"""

assert_file = """package main

func main() {
// Type assertions
  var i interface{}
  s1 := i.(string)    // ASSERT
  s1 = i.(string)     // ASSERT
  s2, _ := i.(string) // ASSERT
  s2, _ = i.(string)  // ASSERT
  s3, ok := i.(string)
  s3, ok = i.(string)
  switch s4 := i.(type) {
  case string:
    _ = s4
  }
  _, _, _, _ = s1, s2, s3, ok

}
"""

blank_file = """package main
import "os"
import "fmt"

func main() {
f, _ := os.Open("random")
    fmt.Println(f)
}"""

ignorepkg_file = """package main
import (
  "io"
  "log"
  "os"
)
func main() {
  f, _ := os.Open("foo")
  log.Println("opened file")
  io.Copy(os.Stdout, f)
}"""

GoErrCheckBearTest = verify_local_bear(GoErrCheckBear,
                                       valid_files=(
                                           good_file, assert_file, blank_file),
                                       invalid_files=(bad_file,),
                                       tempfile_kwargs={'suffix': '.go'})

GoErrCheckBearWithIgnoreTest = verify_local_bear(GoErrCheckBear,
                                                 valid_files=(
                                                     good_file,
                                                     assert_file,
                                                     blank_file),
                                                 invalid_files=(bad_file,),
                                                 settings={
                                                     'ignore':
                                                     "'[rR]ead|[wW]rite'"},
                                                 tempfile_kwargs={'suffix':
                                                                  '.go'})
GoErrCheckBearWithIgnorePkgTest = verify_local_bear(GoErrCheckBear,
                                                    valid_files=(
                                                        good_file, assert_file,
                                                        blank_file),
                                                    invalid_files=(
                                                        ignorepkg_file,),
                                                    settings={
                                                        'ignorepkg':
                                                        "'io'"},
                                                    tempfile_kwargs={'suffix':
                                                                     '.go'})

GoErrCheckBearWithBlankTest = verify_local_bear(GoErrCheckBear,
                                                valid_files=(good_file,
                                                             assert_file),
                                                invalid_files=(blank_file,),
                                                settings={'blank': True},
                                                tempfile_kwargs={'suffix':
                                                                 '.go'})
GoErrCheckBearWithAssertsTest = verify_local_bear(GoErrCheckBear,
                                                  valid_files=(good_file,
                                                               blank_file),
                                                  invalid_files=(assert_file,),
                                                  settings={'asserts': True},
                                                  tempfile_kwargs={'suffix':
                                                                   '.go'})
