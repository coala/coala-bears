#!/bin/sh

set -ex

go get -u github.com/alecthomas/gometalinter

gometalinter --install

go get -u sourcegraph.com/sqs/goreturns

go get -u github.com/BurntSushi/toml/cmd/tomlv
