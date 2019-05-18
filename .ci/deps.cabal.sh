#!/bin/sh

set -e -x

# cabal-install 1.22 is the minimum tested version
cabal --version

cabal update

cabal install happy

cabal install --only-dependencies --avoid-reinstalls

# Force ghc-mod to resolve its Cabal version
~/.cabal/bin/ghc-mod modules
