#!/bin/sh

set -e
set -x

# PMD commands
PMD_VERSION=5.4.1
if [ ! -e ~/.local/bin/pmd ]; then
  wget -nc -O ~/pmd.zip https://github.com/pmd/pmd/releases/download/pmd_releases%2F5.4.1/pmd-bin-5.4.1.zip
  unzip ~/pmd.zip -d ~/
  cp -r ~/pmd-bin-$PMD_VERSION/* ~/.local/
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
