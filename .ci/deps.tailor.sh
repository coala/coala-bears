#!/bin/sh

set -e
set -x

# Tailor (Swift) commands
# Comment out the hardcoded PREFIX, so we can put it into ~/.local
if [ ! -e ~/.local/tailor/tailor-latest ]; then
  wget https://github.com/sleekbyte/tailor/releases/download/v0.1.0/tailor.tar -O /tmp/tailor.tar
  tar -xvf /tmp/tailor.tar
  # Provide a constant path for the executable
  mkdir ~/.local/tailor/tailor-latest -p
  ln -s tailor/bin ~/.local/tailor/tailor-latest
fi
