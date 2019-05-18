#!/usr/bin/env python3

import sys

# Tags like list, check and collectonly shouldnt appear on codecov
# but they also shouldnt be submitted to codecov, so they are not
# removed here as that would hide a bug in tox.ini
REJECT_TAGS = set(['codecov', 'skip', 'noskip'])


def main():
    env_factors = set(sys.argv[1].split('-'))

    print(','.join(sorted(env_factors - REJECT_TAGS)))


if __name__ == '__main__':
    main()
