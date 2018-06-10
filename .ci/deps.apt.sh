set -e
set -x

TERM=dumb

# apt-get commands
export DEBIAN_FRONTEND=noninteractive

deps="libclang1-3.4 indent mono-mcs chktex r-base julia golang-go luarocks verilator cppcheck flawfinder devscripts mercurial"
deps_infer="m4 opam"

if [ $CIRCLECI ]; then
    USE_PPAS="true"
    deps=${deps/golang-go/}
    deps="$deps golang-1.9-go"
fi

if [ "$USE_PPAS" = "true" ]; then
  sudo add-apt-repository -y ppa:marutter/rdev
  sudo add-apt-repository -y ppa:staticfloat/juliareleases
  sudo add-apt-repository -y ppa:staticfloat/julia-deps
  sudo add-apt-repository -y ppa:gophers/archive
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

# Change environment for flawfinder from python to python2
sudo sed -i '1s/.*/#!\/usr\/bin\/env python2/' /usr/bin/flawfinder
