#!/bin/bash
# this script check for 'Circle' in the commit message

MESSAGE=$(git log -1 HEAD --pretty=format:%s)

if [[ "$MESSAGE" == *Circle* ]]; then
    exit 0
fi

exit 1
