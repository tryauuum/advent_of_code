#!/usr/bin/python3

# run it as
# ./9.py inputs/9 [--one | --two] [--debug]

import sys
import math
import time

def get_commands():
    with open(sys.argv[1]) as f:
        return [(line.strip().split()[0], int(line.strip().split()[1])) for line in f.readlines()]


def adjust_tail():
    global tail
    if tail == head:
        return
    if (head[0] - 1 <= tail[0] <= head[0] + 1 and
        head[1] -1 <= tail[1] <= head[1] + 1):
        return
    else:
        # I'm to lazy to operate numbers here, I assume tail will just take place
        # of previous head position
        tail = head_previous.copy()

def adjust_rope():
    for c in range(1, len(rope)):
        if rope[c-1] == rope[c]:
            continue
        if (rope[c-1][0] - 1 <= rope[c][0] <= rope[c-1][0] + 1 and
            rope[c-1][1] -1 <= rope[c][1] <= rope[c-1][1] + 1):
            continue
        else:
            # I have to count numbers here unfortunatelly
            candidates = [rope[c-1].copy() for _ in range(4)]
            candidates[0][0] += 1
            candidates[1][1] += 1
            candidates[2][0] -= 1
            candidates[3][1] -= 1
            candidates = sorted([(candidate, math.dist(rope[c], candidate))
                for candidate in candidates], key=lambda x: x[1])
            if candidates[0][1] == candidates[1][1]:
                # we are positioned diagonally, so let's try again with more options
                # diagonal motion is only allowed in this case
                candidates = [rope[c-1].copy() for _ in range(4)]
                candidates[0][0] += 1; candidates[0][1] += 1
                candidates[1][0] -= 1; candidates[1][1] += 1
                candidates[2][0] -= 1; candidates[2][1] -= 1
                candidates[3][0] += 1; candidates[3][1] -= 1
                candidates = sorted([(candidate, math.dist(rope[c], candidate))
                    for candidate in candidates], key=lambda x: x[1])
            rope[c] = candidates[0][0]


def print_field(whole_field=False):
    def p(*args):
        print(*args, end='')
    if whole_field:
        range_lines = range(min([x[1] for x in list(tail_places)]),
            max([x[1] for x in list(tail_places)]) + 1)
        range_colums = range(min([x[0] for x in list(tail_places)]),
            max([x[0] for x in list(tail_places)]) + 1)
    else:
        range_lines = range_colums = range(-10, 10)
    for line in range_lines:
        p(str(line).zfill(5), '-> ')
        for char in range_colums:
            for chain in range(len(rope)):
                if rope[chain][0] == char and rope[chain][1] == line:
                    letter = str(chain)
                    if chain == 0: letter = 'H'
                    if chain == len(rope) - 1: letter = 'T'
                    p(letter)
                    break
            else:
                if (char, line) in tail_places:
                    p('#')
                else:
                    p('.')
        print()


if __name__ == '__main__':
    data = get_commands()
    if '--one' in sys.argv:
        tail = [0, 0]
        head = [0, 0]
        tail_places = set()
        tail_places.add(tuple(tail))
        for action, count in data:
            for _ in range(count):
                head_previous = head.copy()
                if action == 'L':
                    head[0] -= 1
                if action == 'R':
                    head[0] += 1
                if action == 'U':
                    head[1] += 1
                if action == 'D':
                    head[1] -= 1
                adjust_tail()
                tail_places.add(tuple(tail))
    if '--two' in sys.argv:
        rope = [[0, 0] for _ in range(10)]
        tail_places = set()
        # rope's head is leftmost
        tail_places.add(tuple(rope[-1]))
        for action, count in data:
            for _ in range(count):
                if action == 'L':
                    rope[0][0] -= 1
                if action == 'R':
                    rope[0][0] += 1
                if action == 'U':
                    rope[0][1] += 1
                if action == 'D':
                    rope[0][1] -= 1
                adjust_rope()
                tail_places.add(tuple(rope[-1]))
        if '--debug' in sys.argv:
            print_field(True)
    print(len(tail_places))
