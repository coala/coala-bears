from bears.vhdl.VHDLLintBear import VHDLLintBear
from tests.LocalBearTestHelper import verify_local_bear


VHDLLintBearTest = verify_local_bear(VHDLLintBear,
                                     (('test',),),
                                     (('\t',),))
