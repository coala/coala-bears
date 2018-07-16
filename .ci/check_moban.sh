#!/bin/bash

set -ex

: "${MOBAN_BRANCH:=master}"

if [ ! -d ../coala-mobans ]; then
  git clone https://gitlab.com/coala/mobans \
          --branch=${MOBAN_BRANCH} ../coala-mobans
fi

date

moban
git diff --exit-code
