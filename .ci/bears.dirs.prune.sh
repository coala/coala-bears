#!/bin/sh

# Delete empty bear directories
set -e

dirs=$(find bears -depth -type d -and -not -name '__pycache__')

for dir in $dirs; do
  bears=$(ls $dir/*Bear.py 2>/dev/null || true)
  subdirs=$(ls -d $dir/*/ 2>/dev/null || true)
  if [[ -z "$bears""$subdirs" ]]; then
    echo Removing $dir
    rm -rf $dir
  fi
done
