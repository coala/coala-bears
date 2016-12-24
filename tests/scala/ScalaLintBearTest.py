import os

from bears.scala.ScalaLintBear import ScalaLintBear
from coalib.testing.LocalBearTestHelper import verify_local_bear

good_file = """
object HelloWorld {
  def main(args: Array[String]): Unit = {
    println("Hello, world!")
  }
}
"""

bad_file = """
object HelloWorld {
  def main(args: Array[String]): Unit = {
    println("Hello, world!")
    var x = 10
  }
}
"""

conf_file = os.path.join(os.path.dirname(__file__),
                         'test_files',
                         'scala_config.xml')


ScalaLintBearTest = verify_local_bear(
                        ScalaLintBear,
                        valid_files=(good_file,),
                        invalid_files=(bad_file,),
                        tempfile_kwargs={'suffix': '.scala'}
                        )


ScalaLintBearConfigTest = verify_local_bear(
                              ScalaLintBear,
                              valid_files=(good_file, bad_file),
                              invalid_files=(),
                              settings={'scalalint_config': conf_file},
                              tempfile_kwargs={'suffix': '.scala'}
                              )
