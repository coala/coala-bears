#!/bin/sh

set -e -x
# This file causes ghc-mod to try to install them all
# which fails https://github.com/coala/coala-bears/issues/1384
rm coala-bears.cabal
