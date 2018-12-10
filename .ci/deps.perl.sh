#!/bin/bash

set -e -x

# VHDL Bakalint Installation
if [ ! -e ~/.local/bin/bakalint.pl ]; then
  BAKALINT_VERSION=0.4.0
  wget "http://downloads.sourceforge.net/project/fpgalibre/bakalint/0.4.0/bakalint-0.4.0.tar.gz?r=https%3A%2F%2Fsourceforge.net%2Fprojects%2Ffpgalibre%2Ffiles%2Fbakalint%2F0.4.0%2F&ts=1461844926&use_mirror=netcologne" -O ~/bl.tar.gz
  tar xf ~/bl.tar.gz -C ~/
  mv ~/bakalint-$BAKALINT_VERSION/bakalint.pl ~/.local/bin/
fi
