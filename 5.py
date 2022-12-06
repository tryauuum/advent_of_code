#!/usr/bin/python3

# run it as
# ./5.py [ --one | --two ] < inputs/5

import sys
import re

def read_crates():
    crates = []
    while True:
        line = input()
        if line == '':
            break
        crates.append(line)
    crates.pop() # remove " 1   2   3" line
    crates_new = list([] for _ in range(len(crates[0])))
    for line in crates:
        for i in range(len(line)):
            crates_new[i].append(line[i])
    return [list(line.strip()[::-1]) for line in ["".join(line) for line in crates_new] if line.strip().isalpha()]


crates = read_crates()
for line in sys.stdin:
    how_many, source, dest = [int(x) for x in re.findall(r'[0-9]+', line)]
    # we have zero-indexed crates
    source = source - 1
    dest = dest - 1
    if '--one' in sys.argv:
        for x in range(how_many):
            crates[dest].append(crates[source].pop())
    if '--two' in sys.argv:
        tmp = []
        for x in range(how_many):
            tmp.insert(0, crates[source].pop())
        crates[dest] += tmp

print("".join([x[-1] for x in crates]))
