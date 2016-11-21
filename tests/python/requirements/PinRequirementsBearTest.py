from bears.python.requirements.PinRequirementsBear import PinRequirementsBear
from coalib.testing.LocalBearTestHelper import verify_local_bear


majors_given = """
# So this file contains majors, minors and patch versions
coala==0
coala-bears==0.8
coala-utils==0.5.0
"""

minors_given = """
# So this file contains majors, minors and patch versions
coala==0.8
coala-bears==0.8
coala-utils==0.5.0
"""

patches_given = """
# So this file contains majors, minors and patch versions
coala==0.8.2
coala-bears==0.8.1
coala-utils==0.5.0
"""


PinMinorTest = verify_local_bear(
    PinRequirementsBear,
    valid_files=(patches_given, minors_given),
    invalid_files=(majors_given,))

PinPatchTest = verify_local_bear(
    PinRequirementsBear,
    valid_files=(patches_given,),
    invalid_files=(majors_given, minors_given),
    settings={'require_patch': True})
