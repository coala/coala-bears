set -e
set -x

VERSION=0.4.1
BIN_PATH=~/.cabal/bin/shellcheck

function install_shellcheck {
  cabal update --verbose=0
  cabal install --verbose=0 --force-reinstalls shellcheck-$VERSION
}

function currently_installed_shellcheck_version {
  $BIN_PATH -V | grep version: | cut -d: -f2 | awk '{print $1}'
}

if [ ! -f $BIN_PATH ]; then
  install_shellcheck
else
  EXISTING_VERSION=$(currently_installed_shellcheck_version)
  if [ "$VERSION" != "$EXISTING_VERSION" ]; then
    rm -rf $BIN_PATH
    install_shellcheck
  else
    echo "Using cached ShellCheck $EXISTING_VERSION"
  fi
fi
