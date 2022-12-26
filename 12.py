#!/usr/bin/python3

# run it as
# ./12.py inputs/12 [--one | --two]

import sys
import math

with open(sys.argv[1]) as f:
    # reversed because I want to have (0, 0) in lower left corner
    MAP = [line.strip() for line in reversed(f.readlines())]
    MAP_MAX_X = len(MAP[0])
    MAP_MAX_Y = len(MAP)

class Coordinates:

    def __init__(self, x, y):
        assert x in range(MAP_MAX_X)
        assert y in range(MAP_MAX_Y)
        self.x = x
        self.y = y

    def neighbors(self):
        result = []
        for x in range(self.x - 1, self.x + 2):
            for y in range(self.y - 1, self.y + 2):
                if x == self.x and y == self.y:
                    continue # not a neighbor
                if x in range(MAP_MAX_X) and y in range(MAP_MAX_Y):
                    result.append((x,y))
        return result

    def elevation(self):
        elevation = ord(MAP[self.y][self.x])
        if elevation == ord('S'):
            elevation = ord('a')
        return elevation

def random_walk(start, desired_distance: "desired distance between start and finish"):
    # XXX descripitve name
    my_map = MAP.copy()
    current_position = final_position = start
    while math.dist(current_position, final_position) < desired_distance:
        pass


if __name__ == '__main__':
    # I think this can be solved with "go straight untill you him a wall, then
    # turn right, then try going forward and occasinally try to turn left"
    # solution. But it's not universal path finding...
    for line  in MAP:
        print(line)
