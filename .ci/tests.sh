set -e
set -x

source .ci/env_variables.sh

args=()

if [ "$system_os" == "LINUX" ] ; then
  args+=('--cov' '--cov-fail-under=100' '--doctest-modules')
fi

mv bears/vimscript/VintBear.py bears/vimscript/VintBear._py
mv tests/vimscript/VintBearTest.py tests/vimscript/VintBearTest._py

python3 -m pytest "${args[@]}"

mv bears/vimscript/VintBear._py bears/vimscript/VintBear.py
mv tests/vimscript/VintBearTest._py tests/vimscript/VintBearTest.py
