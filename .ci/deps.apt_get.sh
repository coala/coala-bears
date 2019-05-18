#!/bin/sh

set -e -x

if [ -f /usr/bin/flawfinder ]; then
    sh .ci/deps.flawfinder.sh
fi
