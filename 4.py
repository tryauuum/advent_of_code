#!/usr/bin/python3

# run it as
# ./4.py [ --one | --two ] < inputs/4

import sys

total = 0
for line in sys.stdin:
    line = line.strip()
    pair = line.split(',')
    for index in range(len(pair)):
        pair[index] = [int(x) for x in pair[index].split('-')]
    x, y = pair
    # my first idea was just to use sets, as in previous task
    # my second idea was to use bitmap, do a logical OR operation
    #       and if result equals one of bitmaps then they intersect
    # but then I did a google search for "comparing ranges in python"...
    intersect = range(max(x[0], y[0]), min(x[1], y[1]) + 1)
    if '--one' in sys.argv:
        if len(intersect) == len(range(x[0], x[1]+1)) or len(intersect) == len(range(y[0], y[1]+1)):
            total += 1
    if '--two' in sys.argv:
        if len(intersect):
            total += 1
print(total)
