#!/bin/sh

set -e -x

# TODO implement DISABLE_BEARS here
if [ -n "$BEARS" ]; then
  for item in $BEARS $BEAR_LIST; do
    if [ -f ".ci/deps.$item.sh" ]; then
      bash -e -x ".ci/deps.$item.sh"
    fi
  done
fi
