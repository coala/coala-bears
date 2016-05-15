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
sudo add-apt-repository -y ppa:avsm/ppa
sudo apt-get -y update
deps="espeak libclang1-3.4 indent mono-mcs chktex hlint r-base julia luarocks verilator cppcheck flawfinder"
deps_python_dbus="libdbus-glib-1-dev libdbus-1-dev"
deps_python_gi="glib2.0-dev gobject-introspection libgirepository1.0-dev python3-cairo-dev"
deps_perl="perl libperl-critic-perl"
deps_infer="m4 opam"
sudo apt-get -y install $deps $deps_python_gi $deps_python_dbus $deps_perl $deps_infer

# Update hlint to latest version (not available in apt)
wget https://launchpad.net/ubuntu/+source/hlint/1.9.26-1/+build/8831318/+files/hlint_1.9.26-1_amd64.deb
sudo dpkg -i hlint_1.9.26-1_amd64.deb

# NPM commands
sudo rm -rf /opt/alex # Delete ghc-alex as it clashes with npm deps
npm install

# R commands
mkdir -p ~/.RLibrary
echo '.libPaths( c( "~/.RLibrary", .libPaths()) )' >> .Rprofile
echo 'options(repos=structure(c(CRAN="http://cran.rstudio.com")))' >> .Rprofile
R -e "install.packages('lintr', dependencies=TRUE, quiet=TRUE, verbose=FALSE)"

# GO commands
go get -u github.com/golang/lint/golint
go get -u golang.org/x/tools/cmd/goimports
go get -u sourcegraph.com/sqs/goreturns
go get -u golang.org/x/tools/cmd/gotype
go get -u github.com/kisielk/errcheck 

# Ruby commands
bundle install

for dep_version in "${dep_versions[@]}" ; do
  pyenv install -ks $dep_version
  pyenv local $dep_version 2.7.10
  python --version
  source .ci/env_variables.sh

  pip install -r test-requirements.txt
  pip install -r requirements.txt
done

pip install -r docs-requirements.txt

# Downloading nltk data that's required for nltk to run
bash .ci/deps.nltk.sh

python setup.py --help

# Dart Lint commands
if ! dartanalyzer -v &> /dev/null ; then
  wget -nc -O ~/dart-sdk.zip https://storage.googleapis.com/dart-archive/channels/stable/release/1.14.2/sdk/dartsdk-linux-x64-release.zip
  unzip -n ~/dart-sdk.zip -d ~/
fi

# VHDL Bakalint Installation
wget "http://downloads.sourceforge.net/project/fpgalibre/bakalint/0.4.0/bakalint-0.4.0.tar.gz?r=https%3A%2F%2Fsourceforge.net%2Fprojects%2Ffpgalibre%2Ffiles%2Fbakalint%2F0.4.0%2F&ts=1461844926&use_mirror=netcologne" -O ~/bl.tar.gz
tar xf ~/bl.tar.gz -C ~/

# Julia commands
julia -e "Pkg.add(\"Lint\")"

# Lua commands
sudo luarocks install luacheck --deps-mode=none

# Infer commands
if [ ! -e ~/infer-linux64-v0.7.0/infer/bin ]; then 
	wget -nc -O ~/infer.tar.xz https://github.com/facebook/infer/releases/download/v0.7.0/infer-linux64-v0.7.0.tar.xz
	tar xf ~/infer.tar.xz -C ~/
	cd ~/infer-linux64-v0.7.0
	opam init --y
	opam update
	opam pin add --yes --no-action infer .
	opam install --deps-only --yes infer
	./build-infer.sh java
fi

# PMD commands
if [ ! -e ~/pmd-bin-5.4.1/bin ]; then
	wget -nc -O ~/pmd.zip https://github.com/pmd/pmd/releases/download/pmd_releases%2F5.4.1/pmd-bin-5.4.1.zip
	unzip ~/pmd.zip -d ~/
fi

# Tailor (Swift) commands
curl -fsSL https://tailor.sh/install.sh | sed 's/read -r CONTINUE < \/dev\/tty/CONTINUE=y/' > install.sh
sudo bash install.sh
