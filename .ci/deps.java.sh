set -e
set -x

# PMD commands
if [ ! -e ~/pmd-bin-5.6.1/bin ]; then
  wget -nc -O ~/pmd.zip https://github.com/pmd/pmd/releases/download/pmd_releases%2F5.6.1/pmd-bin-5.6.1.zip
  unzip ~/pmd.zip -d ~/
fi

# Tailor (Swift) commands
# Comment out the hardcoded PREFIX, so we can put it into ~/.local
if [ ! -e ~/.local/tailor/tailor-latest ]; then
  curl -fsSL -o install.sh https://tailor.sh/install.sh
  sed -i 's/read -r CONTINUE < \/dev\/tty/CONTINUE=y/;;s/^PREFIX.*/# PREFIX=""/;' install.sh
  PREFIX=$HOME/.local bash ./install.sh
  # Provide a constant path for the executable
  ln -s ~/.local/tailor/tailor-* ~/.local/tailor/tailor-latest
fi
