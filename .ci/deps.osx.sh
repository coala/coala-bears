VERSION=0.4.4
BIN_PATH=/usr/local/Cellar/shellcheck/

install_shellcheck() {
  brew update && brew install shellcheck
}

currently_installed_shellcheck_version() {
  ls /usr/local/Cellar/shellcheck/
}

if [ ! -d $BIN_PATH ]; then
  install_shellcheck
else
  EXISTING_VERSION=$(currently_installed_shellcheck_version)
  if [ "$VERSION" != "$EXISTING_VERSION" ]; then
    brew uninstall shellcheck
    install_shellcheck
  else
    echo "Using cached ShellCheck $EXISTING_VERSION"
  fi
fi
