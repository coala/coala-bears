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

# apt-get commands
export DEBIAN_FRONTEND=noninteractive

deps="libclang1-3.4 indent mono-mcs chktex r-base julia golang-go luarocks verilator cppcheck flawfinder devscripts"
deps_infer="m4 opam"

case $CIRCLE_BUILD_IMAGE in
  "ubuntu-12.04")
    USE_PPAS="true"
    # The Circle provided Go is too old
    sudo mv /usr/local/go /usr/local/circleci-go
    ;;
  "ubuntu-14.04")
    # Use xenial, needed to replace outdated julia provided by Circle CI
    ADD_APT_UBUNTU_RELEASE=xenial
    # Work around lack of systemd on trusty, which xenial's lxc-common expects
    echo '#!/bin/sh' | sudo tee /usr/bin/systemd-detect-virt > /dev/null
    sudo chmod a+x /usr/bin/systemd-detect-virt

    # The non-apt go provided by Circle CI is acceptable
    deps=${deps/golang-go/}
    # Add packages which are already in the precise image
    deps="$deps g++-4.9 libxml2-utils php-cli php7.0-cli php-codesniffer"
    # gfortran on CircleCI precise is 4.6 and R irlba compiles ok,
    # but for reasons unknown it fails on trusty without gfortran-4.9
    deps="$deps gfortran-4.9"
    # Add extra infer deps
    deps_infer="$deps_infer ocaml camlp4"
    # opam install --deps-only --yes infer fails with
    #  Fatal error:
    #  Stack overflow
    # aspcud is an external dependency resolver, and is the recommended
    # solution: https://github.com/ocaml/opam/issues/2507
    deps_infer="$deps_infer aspcud"
    ;;
esac

if [ -n "$ADD_APT_UBUNTU_RELEASE" ]; then
  echo "deb http://archive.ubuntu.com/ubuntu/ $ADD_APT_UBUNTU_RELEASE main universe" | sudo tee -a /etc/apt/sources.list.d/$ADD_APT_UBUNTU_RELEASE.list > /dev/null
fi

if [ "$USE_PPAS" = "true" ]; then
  sudo add-apt-repository -y ppa:marutter/rdev
  sudo add-apt-repository -y ppa:staticfloat/juliareleases
  sudo add-apt-repository -y ppa:staticfloat/julia-deps
  sudo add-apt-repository -y ppa:ondrej/golang
  sudo add-apt-repository -y ppa:avsm/ppa
elif [ -n "$USE_PPAS" ]; then
  for ppa in $USE_PPAS; do
    sudo add-apt-repository -y ppa:$ppa
  done
fi

deps_perl="perl libperl-critic-perl"

sudo apt-get -y update
sudo apt-get -y --no-install-recommends install $deps $deps_perl $deps_infer

# On Trusty, g++ & gfortran 4.9 need activating for R lintr dependency irlba.
ls -al /usr/bin/gcc* /usr/bin/g++* /usr/bin/gfortran* || true
if [[ "$CIRCLE_BUILD_IMAGE" == "ubuntu-14.04" ]]; then
  sudo update-alternatives --install /usr/bin/gcc gcc /usr/bin/gcc-4.9 20
  sudo update-alternatives --install /usr/bin/g++ g++ /usr/bin/g++-4.9 20
  sudo update-alternatives --install /usr/bin/gfortran gfortran /usr/bin/gfortran-4.9 20
fi

# Change environment for flawfinder from python to python2
sudo sed -i '1s/.*/#!\/usr\/bin\/env python2/' /usr/bin/flawfinder

# NPM commands
ALEX=$(which alex || true)
# Delete 'alex' if it is not in a node_modules directory,
# which means it is ghc-alex.
if [[ -n "$ALEX" && "${ALEX/node_modules/}" == "${ALEX}" ]]; then
  echo "Removing $ALEX"
  sudo rm -rf $ALEX
fi
npm install

# R commands
echo '.libPaths( c( "'"$R_LIB_USER"'", .libPaths()) )' >> .Rprofile
echo 'options(repos=structure(c(CRAN="http://cran.rstudio.com")))' >> .Rprofile
R -q -e 'install.packages("lintr")'
R -q -e 'install.packages("formatR")'

# GO commands
go get -u github.com/golang/lint/golint
go get -u golang.org/x/tools/cmd/goimports
go get -u sourcegraph.com/sqs/goreturns
go get -u golang.org/x/tools/cmd/gotype
go get -u github.com/kisielk/errcheck
go get -u github.com/BurntSushi/toml/cmd/tomlv

# Ruby commands
bundle install --path=vendor/bundle --binstubs=vendor/bin --jobs=8 --retry=3

for dep_version in "${dep_versions[@]}" ; do
  pyenv install -ks $dep_version
  pyenv local $dep_version 2.7.10
  python --version
  source .ci/env_variables.sh

  pip install pip -U
  pip install -U setuptools
  pip install -r test-requirements.txt
  pip install -r requirements.txt
  pip install language_check==0.8.*
done

pip install -r docs-requirements.txt

python setup.py --help

# Dart Lint commands
if ! dartanalyzer -v &> /dev/null ; then
  wget -nc -O ~/dart-sdk.zip https://storage.googleapis.com/dart-archive/channels/stable/release/1.14.2/sdk/dartsdk-linux-x64-release.zip
  unzip -n ~/dart-sdk.zip -d ~/
fi

# VHDL Bakalint Installation
if [ ! -e ~/bakalint-0.4.0/bakalint.pl ]; then
  wget "http://downloads.sourceforge.net/project/fpgalibre/bakalint/0.4.0/bakalint-0.4.0.tar.gz?r=https%3A%2F%2Fsourceforge.net%2Fprojects%2Ffpgalibre%2Ffiles%2Fbakalint%2F0.4.0%2F&ts=1461844926&use_mirror=netcologne" -O ~/bl.tar.gz
  tar xf ~/bl.tar.gz -C ~/
fi

# elm-format Installation
if [ ! -e ~/elm-format-0.18/elm-format ]; then
  mkdir -p ~/elm-format-0.18
  curl -fsSL -o elm-format.tgz https://github.com/avh4/elm-format/releases/download/0.5.2-alpha/elm-format-0.17-0.5.2-alpha-linux-x64.tgz
  tar -xvzf elm-format.tgz -C ~/elm-format-0.18
fi

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
  opam pin add --yes --no-action atdgen 1.10.0
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
# Comment out the hardcoded PREFIX, so we can put it into ~/.local
if [ ! -e ~/.local/tailor/tailor-latest ]; then
  curl -fsSL -o install.sh https://tailor.sh/install.sh
  sed -i 's/read -r CONTINUE < \/dev\/tty/CONTINUE=y/;;s/^PREFIX.*/# PREFIX=""/;' install.sh
  PREFIX=$HOME/.local bash ./install.sh
  # Provide a constant path for the executable
  ln -s ~/.local/tailor/tailor-* ~/.local/tailor/tailor-latest
fi

# PHPMD installation
if [ ! -e ~/phpmd/phpmd ]; then
  mkdir -p ~/phpmd
  curl -fsSL -o phpmd.phar http://static.phpmd.org/php/latest/phpmd.phar
  sudo chmod +x phpmd.phar
  sudo mv phpmd.phar ~/phpmd/phpmd
fi
