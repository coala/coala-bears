#!/bin/sh

set -e -x

luarocks install --local --deps-mode=none luacheck
