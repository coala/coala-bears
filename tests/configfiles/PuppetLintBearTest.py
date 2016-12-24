from bears.configfiles.PuppetLintBear import PuppetLintBear
from coalib.testing.LocalBearTestHelper import verify_local_bear

good_file = """
file { '/some.conf':
  ensure => present,
}
"""

bad_file = """
# foo
class test::foo { }
"""

PuppetLintBearTest = verify_local_bear(PuppetLintBear,
                                       valid_files=(good_file,),
                                       invalid_files=(bad_file,))
