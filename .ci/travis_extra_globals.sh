#!/bin/bash
# This must be `source`d, and kept very basic to avoid breaking travis shell

# Uses tox.ini selectors so that multiple languages can be handled in one job
if [ -z "$TOX_TEST_SELECTORS" ] && [ "$TRAVIS_LANGUAGE" ]; then
  if [ "$TRAVIS_LANGUAGE" = "ruby" ]; then
    TOX_TEST_SELECTORS=gem
  elif [ "$TRAVIS_LANGUAGE" = "node_js" ]; then
    TOX_TEST_SELECTORS=npm
  elif [ "${BEARS/lua/}" != "$BEARS" ]; then
    TOX_TEST_SELECTORS="$BEARS"
  else
    TOX_TEST_SELECTORS="$TRAVIS_LANGUAGE"
  fi
  export TOX_TEST_SELECTORS
fi

if [ "${TOX_TEST_SELECTORS/gem/}" != "$TOX_TEST_SELECTORS" ]; then
  # https://travis-ci.community/t/bundle-path-disappears/4260
  export BUNDLE_PATH="$TRAVIS_BUILD_DIR/vendor/bundle"
  export BUNDLE_BIN="$BUNDLE_PATH/bin"
  EXTRA_PATH="$EXTRA_PATH:$BUNDLE_BIN"
fi

if [ "${TOX_TEST_SELECTORS/java/}" != "$TOX_TEST_SELECTORS" ]; then
  EXTRA_PATH="$EXTRA_PATH:$HOME/.local/tailor/tailor-latest/bin"
fi

if [ "${TOX_TEST_SELECTORS/php/}" != "$TOX_TEST_SELECTORS" ]; then
  EXTRA_PATH="$EXTRA_PATH:$TRAVIS_BUILD_DIR/vendor/bin"
fi

if [ "${TOX_TEST_SELECTORS/npm/}" != "$TOX_TEST_SELECTORS" ]; then
  # Travis adds relative ./node_modules/.bin , but some tests change directory
  EXTRA_PATH="$EXTRA_PATH:$TRAVIS_BUILD_DIR/node_modules/.bin"
fi

if [ "${TOX_TEST_SELECTORS/lua/}" != "$TOX_TEST_SELECTORS" ]; then
  EXTRA_PATH="$EXTRA_PATH:$HOME/.luarocks/bin"
fi

# Remove leading colons
EXTRA_PATH="${EXTRA_PATH##:}"

if [ "$EXTRA_PATH" != "" ]; then
  echo "EXTRA_PATH=$EXTRA_PATH"
  export PATH="$PATH:$EXTRA_PATH"
fi
