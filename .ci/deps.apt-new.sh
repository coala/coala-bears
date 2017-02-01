#!/bin/sh

set -e -x

if [[ "$DIST" != "" && "$DIST" != "precise" && "$DIST" != "trusty" && "$DIST" != "debian-sid" ]]; then
  echo "deb http://archive.ubuntu.com/ubuntu/ $DIST main universe" | sudo tee -a /etc/apt/sources.list.d/$DIST.list > /dev/null
  echo "deb http://archive.ubuntu.com/ubuntu/ $DIST-updates main universe" | sudo tee -a /etc/apt/sources.list.d/$DIST.list > /dev/null
  echo "deb http://archive.ubuntu.com/ubuntu/ $DIST-backports main universe" | sudo tee -a /etc/apt/sources.list.d/$DIST.list > /dev/null
  sudo apt-get -y update
  sudo apt-get -y --no-install-recommends install chktex cppcheck default-jre flawfinder indent libperl-critic-perl libxml2-utils mono-mcs php7.0-cli php-codesniffer verilator
fi

# Change environment for flawfinder from python to python2
if [[ -n "$(which flawfinder)" ]]; then
  sed -e '1s/.*/#!\/usr\/bin\/env python2/' $(which flawfinder) > $HOME/bin/flawfinder;
  chmod a+x $HOME/bin/flawfinder;
fi
