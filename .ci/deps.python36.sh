#!/bin/bash

set -e -x

source .ci/deps.pyenv.sh

PYTHON36_BIN="$(which python3.6 || true)"
if [ -n "$PYTHON36_BIN" ]; then
  if [ ! -d "$PYENV_ROOT/plugins/pyenv-register" ]; then
    # https://github.com/doloopwhile/pyenv-register/pull/3
    git clone https://github.com/garyp/pyenv-register.git \
      "$PYENV_ROOT/plugins/pyenv-register"
  fi

  pyenv register -f "$PYTHON36_BIN" || true
fi

PYTHON36_VERSION=$(pyenv versions --bare | fgrep '3.6' --max-count 1 || true)

if [ -z "$PYTHON36_VERSION" ]; then
  PYTHON36_VERSION=3.6.3

  pyenv install "$PYTHON36_VERSION";
fi

pyenv global "$PYTHON36_VERSION"

hash -r
