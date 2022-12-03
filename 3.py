#!/usr/bin/python3

# run it as
# ./3.py [ --one | --two ] < inputs/3

import sys


def value(value):
    return ord(value) - 96 if value.islower() else ord(value) - 38

if '--one' in sys.argv:
    total = 0
    for line in sys.stdin:
        half_length = len(line) // 2
        half1, half2 = line[:half_length], line[half_length:]
        # I guess the idea here was to utilize the fact that exactly one item is mismatched
        # So I could have used less computationally-intensive code than next line
        common = (set(half1) & set(half2)).pop()
        total += value(common)
    print(total)
elif '--two' in sys.argv:
    total = 0
    while True:
        three_packs = [sys.stdin.readline() for x in range(3)]
        if len(three_packs[0]) == 0:
            break
        sets = [set(line.strip()) for line in three_packs]
        total += value((sets[0] & sets[1] & sets[2]).pop())
    print(total)
