from bears.shell.ShellCheckBear import ShellCheckBear
from tests.LocalBearTestHelper import verify_local_bear


valid_file = """
#!/usr/bin/env sh
echo "Path is $PATH"
echo "$P"
""".splitlines(keepends=True)

invalid_file = """
#!/usr/bin/env sh
echo 'Path is $PATH'
echo $P
X = 24
X+=2    # += operator is supported by bash and not by sh
echo $X
""".splitlines(keepends=True)


ShellCheckBearTest = verify_local_bear(ShellCheckBear,
                                       valid_files=(valid_file,),
                                       invalid_files=(invalid_file,))
