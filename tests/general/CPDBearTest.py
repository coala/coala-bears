from bears.general.CPDBear import CPDBear
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
    int array_a[];
    int array_b[];

    int sum_a = 0;

    for (int i = 0; i < 4; i++)
      sum_a += array_a[i];

    int average_a = sum_a / 4;

    int sum_b = 0;

    for (int i = 0; i < 4; i++)
      sum_b += array_b[i];

    int average_b = sum_b / 4;
    return average_a;
  }
}

""".splitlines(keepends=True)


CPDBearTest = verify_local_bear(CPDBear,
                                valid_files=(good_file,),
                                invalid_files=(bad_file,),
                                tempfile_kwargs={"suffix": ".java"})
