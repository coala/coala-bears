#!/bin/sh

set -e
set -x

.ci/deps.python27.sh

# Infer commands
if [ ! -e ~/infer-linux64-v1.1.0/infer/bin ]; then
  wget -nc -O ~/infer.tar.xz https://github.com/facebook/infer/releases/download/v1.1.0/infer-linux64-v1.1.0.tar.xz
  tar xf ~/infer.tar.xz -C ~/
  cd ~/infer-linux64-v1.1.0
  opam init --y
  opam update

  # See https://github.com/coala/coala-bears/issues/2059
  opam pin add --yes --no-action yojson 1.3.3
  opam pin add --yes --no-action biniou 1.0.6

  # See https://github.com/coala/coala-bears/issues/1763
  opam pin add --yes --no-action atdgen 1.10.0

  # See https://github.com/coala/coala-bears/issues/2059
  opam pin add --yes --no-action easy-format 1.2.0

  # See https://github.com/coala/coala-bears/issues/1763
  opam pin add --yes --no-action reason 1.13.5

  # See https://github.com/coala/coala-bears/issues/2664
  # for javalib and the disable-sandboxing below
  opam pin add --yes --no-action javalib 2.3.1

  opam pin add --yes --no-action infer .

  opam init -y --reinit --disable-sandboxing

  sed -i '/wrap-/d;/sandbox.sh/d' ~/.opam/config

  eval $(opam env)

  opam install --deps-only --yes infer
  ./build-infer.sh java
fi
