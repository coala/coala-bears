set -e
set -x

source .ci/env_variables.sh

args=()

if [ "$system_os" == "LINUX" ]; then
  args+=('--cov' '--cov-fail-under=100' '--doctest-modules')
fi

if [[ "$(python3 --version)" != "Python 3.6"* ]]; then
  # This bear is impossible to cover as it requires Python 3.6+
  rm bears/python/BlackBear.py tests/python/BlackBearTest.py
fi

python3 -m pytest "${args[@]}"
