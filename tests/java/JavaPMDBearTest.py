from unittest import mock, TestCase

from bears.java.JavaPMDBear import JavaPMDBear
from coalib.testing.LocalBearTestHelper import verify_local_bear


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
"""

bad_file = """
// Hello.java
class Hello {
  int test() {
    String s = null;
    return s.length();
  }
}
"""


class JavaPMDBearPrerequisiteTest(TestCase):
    def test_check_prerequisites(self):
        with mock.patch('bears.java.JavaPMDBear.which') as mock_which:
            mock_which.side_effect = [None, None, None]
            self.assertEqual(JavaPMDBear.check_prerequisites(),
                             'bash is not installed.')

            mock_which.side_effect = ['path/to/bash', None, None]
            self.assertEqual(JavaPMDBear.check_prerequisites(),
                             ('PMD is missing. Make sure to install it from '
                              '<https://pmd.github.io/>'))

            mock_which.side_effect = ['path/to/bash',
                                      'path/to/pmd',
                                      'path/to/run']
            self.assertEqual(JavaPMDBear.check_prerequisites(), True)


JavaPMDBearTest = verify_local_bear(
    JavaPMDBear, valid_files=(good_file,), invalid_files=(bad_file,),
    tempfile_kwargs={'suffix': '.java'})
