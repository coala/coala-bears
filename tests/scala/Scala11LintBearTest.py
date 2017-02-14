import os

from bears.scala.Scala11LintBear import Scala11LintBear
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
        var magicNumber = 10
    }
}
"""

conf_file_unable = os.path.join(os.path.dirname(__file__),
                                'test_files',
                                'scala_config_unable_magic_number_checker.xml')

Scala11LintBearMagicNumberUnabledTest = verify_local_bear(
    Scala11LintBear,
    valid_files=(good_file, bad_file),
    invalid_files=(),
    settings={'scalalint_config': conf_file_unable},
    tempfile_kwargs={'suffix': '.scala'}
)

Scala11LintBearMagicNumberEnabledTest = verify_local_bear(
    Scala11LintBear,
    valid_files=(good_file,),
    invalid_files=(bad_file,),
    tempfile_kwargs={'suffix': '.scala'}
)
