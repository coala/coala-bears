from bears.go.GoTypeBear import GoTypeBear
from tests.LocalBearTestHelper import verify_local_bear


good_file = """
package main
import "fmt"
func main() {
    fmt.Println("Hello World!")
}
""".splitlines(keepends=True)


bad_file = """
package main
import (
    "fmt"
    "math/rand"
    "time"
)
type A struct{}

func (A) String() string { return "A" }
func (B) String() string { return "B" }

func Print(s fmt.Stringer) {
    fmt.Println("Hello " + s.String())
}
func main() {
    rand.Seed(time.Now().UnixNano())
    if rand.Intn(2) == 1 {
        Print(A{})
    } else {
        Print(B{})
    }
}
""".splitlines(keepends=True)


GoTypeBearTest = verify_local_bear(GoTypeBear,
                                   valid_files=(good_file,),
                                   invalid_files=(bad_file,))
