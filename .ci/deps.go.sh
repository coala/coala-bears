#!/bin/sh

set -ex

go get -u github.com/alecthomas/gometalinter

gometalinter --install

go get -u github.com/BurntSushi/toml/cmd/tomlv

go get -u sourcegraph.com/sqs/goreturns
