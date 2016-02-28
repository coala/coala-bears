from bears.julia.JuliaLintBear import JuliaLintBear
from tests.LocalBearTestHelper import verify_local_bear

good_file = """
a = 2
println(2)
""".splitlines(keepends=True)

bad_file = """
println(hello)
""".splitlines(keepends=True)

JuliaLintBearTest = verify_local_bear(JuliaLintBear,
                                      valid_files=(good_file,),
                                      invalid_files=(bad_file,),
                                      tempfile_kwargs={"suffix": ".jl"},
                                      timeout=45)
