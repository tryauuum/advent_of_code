#!/usr/bin/python3

# run it as
# ./8.py [ --one | --two ] < inputs/8

import sys
import math

def ingest():
    # don't you love python sometimes?
    return [[int(char) for char in line.strip()] for line in sys.stdin.readlines()]

def check_visible(direction_dict, mm):
    if direction_dict.get(mm, 0) == 9:
        return
    if direction_dict.get(mm) is None or direction_dict.get(mm, 0) < data[line][char]:
        visble.add((line, char))
    direction_dict[mm] = max(data[line][char], direction_dict.get(mm, 0))


if __name__ == '__main__':

    def display():
        winners = [sorted(rating.items(), key=lambda x: x[1])[-1][0]]
        for line in range(length):
            for char in range(length):
                if (line, char) in winners:
                    print('▇', end='')
                elif (line, char) in visble:
                    print('X', end='')
                else:
                    print(data[line][char], end='')
            print()

    data = ingest()
    assert len(data[0]) == len(data)
    length = len(data)
    visble = set()
    rating = {}

    if '--one' in sys.argv:
        # ok, will try to be smart here
        # check view from all 4 sides, this way I don't need to check some trees at all
        north, south, west, east = {}, {}, {}, {}
        for line in range(length):
            for char in range(length):
                check_visible(north, char)
        for line in reversed(range(length)):
            for char in range(length):
                check_visible(south, char)
        for char in range(length):
            for line in range(length):
                check_visible(west, line)
        for char in reversed(range(length)):
            for line in range(length):
                check_visible(east, line)
        print('visible:', len(visble))

    if '--two' in sys.argv:
        def calc(me, neighbors):
            value = 0
            if not neighbors:
                return value
            for n in neighbors:
                if n < me:
                    value += 1
                elif n == me:
                    value += 1
                    break
                else:
                    break
            return value

        # could be optimized by not copying every tree in each direction
        # but that's not fun anyway. It would be fun to avoid some groups of trees somehow entirely
        for line in range(length):
            for char in range(length):
                me = data[line][char]
                up = [data[_][char] for _ in reversed(range(0, line))]
                left = [data[line][_] for _ in reversed(range(0, char))]
                down = [data[_][char] for _ in range(line+1, length)]
                right = [data[line][_] for _ in range(char+1, length)]
                rating[(line, char)] = math.prod([calc(me, _) for _ in (up, left, down, right)])
        # display()
        winner_v = sorted(rating.items(), key=lambda x: x[1])[-1][1]
        print(winner_v)
