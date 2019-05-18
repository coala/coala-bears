#!/bin/bash
# This file should be used with `source`

set -e -x

if [ -z "$(which pyenv)" ]; then
  export PYENV_ROOT="$HOME/.pyenv"
  export PATH="$PYENV_ROOT/bin:$PATH"
  if [ ! -f "$PYENV_ROOT/bin/pyenv" ]; then
    if [ -d "$PYENV_ROOT" ]; then
      rm -rf "$PYENV_ROOT"
    fi
    git clone https://github.com/pyenv/pyenv.git $PYENV_ROOT
    if [ -d ~/local/bin ]; then
      rm ~/local/bin/pyenv
      (cd ~/local/bin && ln -s $PYENV_ROOT/bin/pyenv .)
    fi
  fi
else
  export PYENV_ROOT="$(pyenv root)"
fi
