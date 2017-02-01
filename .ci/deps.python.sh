#!/bin/sh

set -e -x

echo pip3.4 is $(which pip3.4)
echo python3.4 is $(which python3.4)
if [[ -n "$(which pip3.4)" ]]; then
  ln -sf $(which pip3.4) $HOME/bin/pip3
fi
if [[ -n "$(which python3.4)" ]]; then
  ln -sf $(which python3.4) $HOME/bin/python3
fi

echo pip3.5 is $(which pip3.5)
echo python3.5 is $(which python3.5)
if [[ -n "$(which pip3.5)" ]]; then
  ln -sf $(which pip3.5) $HOME/bin/pip3
fi
if [[ -n "$(which python3.5)" ]]; then
  ln -sf $(which python3.5) $HOME/bin/python3
fi

echo pip3 is $(which pip3)
echo python3 is $(which python3)
if [[ -n "$(which python3)" ]]; then
  ln -sf $(which python3) $HOME/bin/python
fi

python --version
# Needed as some hosts may be providing python 3.2
wget https://bootstrap.pypa.io/get-pip.py
python get-pip.py --user
rm get-pip.py
cp $HOME/.local/bin/pip $HOME/.local/bin/pip3
cp $HOME/.local/bin/pip $HOME/bin/pip
cp $HOME/.local/bin/pip $HOME/bin/pip3
pip --version
