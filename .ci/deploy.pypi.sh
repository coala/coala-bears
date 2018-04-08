#!/bin/bash

# Do not use `set -x` here as then it displays the PYPIPW in logs
set -e

# Ship it!
echo "Uploading coala to pypi"
pip3 install twine wheel
python3 setup.py sdist bdist_wheel
# Upload packages one by one to avoid timeout, allow erroring out.
# Don't block merging because pypi is in error 500 mood again
set +e
twine upload dist/*.whl -u "$PYPIUSER" -p "$PYPIPW"
twine upload dist/*.tar.gz -u "$PYPIUSER" -p "$PYPIPW"
