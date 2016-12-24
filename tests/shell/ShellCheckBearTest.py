from bears.shell.ShellCheckBear import ShellCheckBear
from coalib.testing.LocalBearTestHelper import verify_local_bear


valid_file = """
#!/usr/bin/env sh
echo "Path is $PATH"
echo "$P"
"""

invalid_file = """
#!/usr/bin/env sh
echo 'Path is $PATH'
echo $P
X = 24
X+=2    # += operator is supported by bash and not by sh
echo $X
"""


ShellCheckBearTest = verify_local_bear(ShellCheckBear,
                                       valid_files=(valid_file,),
                                       invalid_files=(invalid_file,))
