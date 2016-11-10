#!/bin/bash

source ../rultor_secrets.sh

set -x
set -e

cd ~
rm -rf bear-docs

git clone "https://$GITHUB_TOKEN@github.com/coala/bear-docs.git"

cd bear-docs
git checkout pre

python3 ./generate local

if [[ -z $(git status -s) ]]; then
    git add -A
    git commit -m "Docs Update"
    git push --set-upstream origin pre
fi
