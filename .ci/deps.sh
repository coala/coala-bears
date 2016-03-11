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
sudo add-apt-repository -y ppa:marutter/rdev
sudo add-apt-repository -y ppa:staticfloat/juliareleases
sudo add-apt-repository -y ppa:staticfloat/julia-deps
sudo apt-get -qq update
deps="espeak libclang1-3.4 indent mono-mcs chktex hlint r-base julia luarocks"
deps_python_dbus="libdbus-glib-1-dev libdbus-1-dev"
deps_python_gi="glib2.0-dev gobject-introspection libgirepository1.0-dev python3-cairo-dev"
deps_perl="perl libperl-critic-perl"
sudo apt-get -qq install $deps $deps_python_gi $deps_python_dbus $deps_perl > /dev/null

# Update hlint to latest version (not available in apt)
wget -q https://launchpad.net/ubuntu/+source/hlint/1.9.26-1/+build/8831318/+files/hlint_1.9.26-1_amd64.deb
sudo dpkg -i hlint_1.9.26-1_amd64.deb

# NPM commands
sudo rm -rf /opt/alex # Delete ghc-alex as it clashes with npm deps
npm install

# R commands
mkdir -p ~/.RLibrary
echo '.libPaths( c( "~/.RLibrary", .libPaths()) )' >> .Rprofile
echo 'options(repos=structure(c(CRAN="http://cran.rstudio.com")))' >> .Rprofile
R -q -e "install.packages('lintr', dependencies=TRUE, quiet=TRUE, verbose=FALSE)"

# GO commands
go get -u github.com/golang/lint/golint
go get -u golang.org/x/tools/cmd/goimports
go get -u sourcegraph.com/sqs/goreturns

# Ruby commands
bundle install

for dep_version in "${dep_versions[@]}" ; do
  pyenv install -ks $dep_version
  pyenv local $dep_version
  python --version
  source .ci/env_variables.sh

  pip install -q -r test-requirements.txt
  pip install -q -r requirements.txt
done

pip install -r docs-requirements.txt

python setup.py --help

# Dart Lint commands
if ! dartanalyzer -v &> /dev/null ; then
  wget -nc -O ~/dart-sdk.zip https://storage.googleapis.com/dart-archive/channels/stable/release/1.14.2/sdk/dartsdk-linux-x64-release.zip
  unzip -n ~/dart-sdk.zip -d ~/
fi

# Julia commands
julia -e "Pkg.add(\"Lint\")"

# Lua commands
sudo luarocks install luacheck --deps-mode=none
