from bears.julia.JuliaLintBear import JuliaLintBear
from coalib.testing.LocalBearTestHelper import verify_local_bear

good_file = """
a = 2
println(2)
"""

bad_file = """
println(hello)
"""

JuliaLintBearTest = verify_local_bear(JuliaLintBear,
                                      valid_files=(good_file,),
                                      invalid_files=(bad_file,),
                                      tempfile_kwargs={'suffix': '.jl'},
                                      timeout=45)
