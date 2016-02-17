set -e
set -x

# Choose the python versions to install deps for
case $CIRCLE_NODE_INDEX in
 0) dep_versions=( "3.3.6" "3.4.3" "3.5.1" ) ;;
 1) dep_versions=( "3.4.3" ) ;;
 2) dep_versions=( "3.3.6" ) ;;
 *) dep_versions=( "3.5.1" ) ;;
esac

# apt-get commands
sudo apt-get -qq update
deps="espeak libclang1-3.4 indent mono-mcs chktex perl libperl-critic-perl"
sudo apt-get -qq install $deps

# NPM commands
sudo rm -rf /opt/alex # Delete ghc-alex as it clashes with npm deps
npm install

# GO commands
go get -u github.com/karmakaze/goop
goop install

for dep_version in "${dep_versions[@]}" ; do
  pyenv install -ks $dep_version
  pyenv local $dep_version
  python --version
  source .misc/env_variables.sh

  pip install -q -r test-requirements.txt
  pip install -q -r requirements.txt

  # Use latest coala
  pip install coala -U --pre
done

# Calling setup.py will download checkstyle automatically so tests may succeed
python setup.py --help
