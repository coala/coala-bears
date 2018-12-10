#!/bin/sh

# Delete tests for bears that have been removed
set -e

bear_tests=$(find tests -type f -and -name '*Test.py')

for test in tests/generate_packageTest.py $bear_tests; do
  bear=${test/Test.py/.py}
  bear=${bear/tests/bears}
  dir=$(dirname $bear)
  if [[ ! -d $dir ]]; then
    echo Removing $test
    rm -f $test
  elif [[ ! -f $bear ]]; then
    echo Removing $test
    rm -f $test
  fi
done
