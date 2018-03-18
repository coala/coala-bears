set -e
set -x

TERM=dumb

# Choose the python versions to install deps for
case $CIRCLE_NODE_INDEX in
 0) dep_versions=( "3.4.3" "3.5.1" ) ;;
 1) dep_versions=( "3.4.3" ) ;;
 -1) dep_versions=( ) ;;  # set by .travis.yml
 *) dep_versions=( "3.5.1" ) ;;
esac

for dep_version in "${dep_versions[@]}" ; do
  pyenv install -ks $dep_version
  pyenv local $dep_version 2.7.10
  python --version
  source .ci/env_variables.sh

  pip install pip==9.0.1
  pip install -U setuptools
  pip install -r test-requirements.txt
  pip install -r requirements.txt
done

pip install -r docs-requirements.txt
