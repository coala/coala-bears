from bears.configfiles.AnsibleLintBear import AnsibleLintBear
from coalib.testing.LocalBearTestHelper import verify_local_bear

good_file = """
"""

bad_file = """
"""

PuppetLintBearTest = verify_local_bear(AnsibleLintBear,
                                       valid_files=(good_file,),
                                       invalid_files=(bad_file,))
