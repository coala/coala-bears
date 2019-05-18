#!/bin/sh

set -e -x

# PMD commands
PMD_VERSION=5.4.1
if [ ! -e ~/.local/bin/pmd ]; then
  wget -nc -O ~/pmd.zip https://github.com/pmd/pmd/releases/download/pmd_releases%2F5.4.1/pmd-bin-5.4.1.zip
  unzip ~/pmd.zip -d ~/
  cp -r ~/pmd-bin-$PMD_VERSION/* ~/.local/
fi
