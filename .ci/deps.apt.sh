set -e
set -x

TERM=dumb

# apt-get commands
export DEBIAN_FRONTEND=noninteractive

deps="libclang1-3.4 indent mono-mcs chktex r-base julia golang-go luarocks verilator cppcheck flawfinder devscripts mercurial"
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
