#!/usr/bin/python3

# run it as
# ./7.py [ --one | --two ] < inputs/7

import sys
import os

TOTAL_SPACE = 70000000
REQUIRED_FREE = 30000000

current_path = ''
dirdict = {}
for line in sys.stdin:
    line = line.strip()
    if line.startswith('$ cd'):
        current_path = os.path.normpath(current_path + '/' + line[5:])
        # some ugly stuff to remove double slash
        current_path = current_path.replace('//', '/')
    elif line.startswith('$ ls'):
        continue
    elif line.startswith('dir '):
        continue
    else:
        size = int(line.split()[0])
        tmp_path = current_path
        while True:
            if tmp_path in dirdict:
                dirdict[tmp_path] += size
            else:
                dirdict[tmp_path] = size
            if tmp_path == '/':
                break
            tmp_path = os.path.normpath(tmp_path + '/' + '..')
if '--one' in sys.argv:
    print(sum([x for x in dirdict.values() if x <= 100_000 ]))
elif'--two' in sys.argv:
    delta = REQUIRED_FREE - (TOTAL_SPACE - dirdict['/'])
    candidates = sorted([item for item in dirdict.items() if item[1] >= delta], key=lambda x: x[1])
    print(candidates[0][1])
