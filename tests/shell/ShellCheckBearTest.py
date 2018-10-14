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

trigger_sc2164 = """
#!/usr/bin/env sh
for dir in */
do
  cd "$dir"
  convert index.png index.jpg
done
"""

trigger_sc2060 = """
#!/usr/bin/env sh
tr -cd [:digit:]
"""

good_zero_byte = ''
good_only_eol = '\n'
good_only_eol_eol = '\n\n'
good_only_comment = '# this is a bash comment'

invalid_file_list = (invalid_file, trigger_sc2164, trigger_sc2060,)
ShellCheckBearTest = verify_local_bear(ShellCheckBear,
                                       valid_files=(valid_file,),
                                       invalid_files=invalid_file_list,
                                       )

small_files = (good_zero_byte, good_only_eol, good_only_eol_eol,
               good_only_comment,)
SmallFileTest = verify_local_bear(ShellCheckBear,
                                  valid_files=small_files,
                                  invalid_files=(),
                                  )

IgnoreSC2164Test = verify_local_bear(ShellCheckBear,
                                     valid_files=(trigger_sc2164,),
                                     invalid_files=(),
                                     settings={
                                         'shellcheck_ignore': ['SC2164']},
                                     )
IgnoreSC2060Test = verify_local_bear(ShellCheckBear,
                                     valid_files=(trigger_sc2060,),
                                     invalid_files=(),
                                     settings={
                                         'shellcheck_ignore': ['SC2060']},
                                     )
MultipleIgnoreTest = verify_local_bear(ShellCheckBear,
                                       valid_files=(trigger_sc2164,
                                                    trigger_sc2060,),
                                       invalid_files=(),
                                       settings={
                                           'shellcheck_ignore': ['SC2164',
                                                                 'SC2060']},
                                       )
