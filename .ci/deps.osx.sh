set -e
set -x

# Prerequisites for Go
mkdir $HOME/Go
export GOPATH=$HOME/Go
export GOROOT=/usr/local/opt/go/libexec
export PATH=$PATH:$GOPATH/bin
export PATH=$PATH:$GOROOT/bin

# Install packages with brew
brew update >/dev/null
brew outdated pyenv || brew upgrade pyenv
brew upgrade go
brew install libffi && brew link libffi --force
brew install sqlite && brew link sqlite --force
brew install openssl && brew link openssl --force
brew install gnu-indent
brew install go
brew tap staticfloat/julia
brew install julia

# Install required go libraries
go get -u github.com/golang/lint/golint
go get -u golang.org/x/tools/cmd/goimports
go get -u sourcegraph.com/sqs/goreturns

# Install required python version for this build
pyenv install -ks $PYTHON_VERSION
pyenv global $PYTHON_VERSION
python --version

# Install packages with pip
pip install -r test-requirements.txt
pip install -r requirements.txt

# Calling setup.py will download checkstyle automatically so tests may succeed
python setup.py --help

# julia
julia -e "Pkg.add(\"Lint\")"
