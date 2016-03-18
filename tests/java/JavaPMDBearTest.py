from bears.java.JavaPMDBear import JavaPMDBear
from tests.LocalBearTestHelper import verify_local_bear


good_file = """
package hello;
class Hello {
  public String myString;
  /* Default Hello constructor */
  public Hello(){
    myString = "Hello";
  }

  /* Print string length */
  public int test() {
    return myString.length();
  }
}
""".splitlines(keepends=True)

bad_file = """
// Hello.java
class Hello {
  int test() {
    String s = null;
    return s.length();
  }
}
""".splitlines(keepends=True)


JavaPMDBearTest = verify_local_bear(
    JavaPMDBear, valid_files=(good_file,), invalid_files=(bad_file,),
    tempfile_kwargs={"suffix": ".java"})
