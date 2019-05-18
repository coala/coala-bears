#!/bin/bash

set -e -x

source .ci/deps.pyenv.sh

PYTHON27_BIN="$(which python2.7 || true)"
if [ -n "$PYTHON27_BIN" ]; then
  if [ ! -d "$PYENV_ROOT/plugins/pyenv-register" ]; then
    # https://github.com/doloopwhile/pyenv-register/pull/3
    git clone https://github.com/garyp/pyenv-register.git \
      "$PYENV_ROOT/plugins/pyenv-register"
  fi

  pyenv register -f "$PYTHON27_BIN" || true
fi

PYTHON27_VERSION=$(pyenv versions --bare | fgrep '2.7' --max-count 1)
PYTHON36_VERSION=$(pyenv versions --bare | fgrep '3.6' --max-count 1 || true)

pyenv global "$PYTHON27_VERSION" "$PYTHON36_VERSION"
hash -r
