#!/bin/bash

set -e -x

# elm-format Installation
if [ ! -e ~/.local/bin/elm-format ]; then
  curl -fsSL -o elm-format.tgz https://github.com/avh4/elm-format/releases/download/0.5.2-alpha/elm-format-0.17-0.5.2-alpha-linux-x64.tgz
  tar -xvzf elm-format.tgz -C ~/.local/bin/
fi

if [ "$TRAVIS_ELM_VERSION" = "0.18.0" ]; then
  touch elm-package.json
else
  touch elm.json
fi
