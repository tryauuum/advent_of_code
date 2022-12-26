#!/usr/bin/python3

# run it as this, redirect is iportant not to fuck up ncurses
# ./12.py inputs/12 [--one | --two] 2>/tmp/knut_i_plet

import sys
import math
import time
import copy
from collections import namedtuple, Counter
import curses
import logging
if '--debug' in sys.argv:
    logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger()

stdscr = None

with open(sys.argv[1]) as f:
    # reversed to have (0, 0) in bottom left corner
    MAP = [line.strip() for line in reversed(f.readlines())]
    MAP_MAX_X = len(MAP)
    MAP_MAX_Y = len(MAP[0])


CoordinateBase = namedtuple('Coordinate', ['x', 'y'])

DIRECTIONS = {"up": (1, 0),
              "right": (0, 1),
              "left": (0, -1),
              "down": (-1, 0)}

class Coordinate(CoordinateBase):

    def __init__(self, x, y):
        assert x in range(MAP_MAX_X)
        assert y in range(MAP_MAX_Y)
        self.elevation = ord(MAP[self.x][self.y])
        if self.elevation == ord('S'):
            self.elevation = ord('a')
        if self.elevation == ord('E'):
            self.elevation = ord('z')

    def neighbors(self):
        result = []
        for neighbor in [(self.x + 1, self.y),
                         (self.x, self.y - 1),
                         (self.x, self.y + 1),
                         (self.x - 1, self.y)]:
            if neighbor[0] in range(MAP_MAX_X) and neighbor[1] in range(MAP_MAX_Y):
                result.append(Coordinate(*neighbor))
        return result


class WalkerWithMemory:

    def __init__(self, start, reverse_rules=False, stop_at_obstacles=False):
        self.current = Coordinate(*start)
        self.visited = list()
        self.knows_what_to_do = True
        self.reverse_rules = reverse_rules
        self.stop_at_obstacles = stop_at_obstacles

    def walk(self, destination, stop_at_steps=6):
        global stdscr
        for _ in range(stop_at_steps):
            if self.current not in self.visited:
                self.visited.append(self.current)
            stdscr.addch(self.current.x, self.current.y + 3, "☭", curses.color_pair(1))
            stdscr.refresh()
            candidates = []
            for neighbor in self.current.neighbors():
                if self.reverse_rules:
                    if ((neighbor.elevation >= self.current.elevation or
                         self.current.elevation - 1 == neighbor.elevation) and
                            neighbor not in self.visited):
                        candidates.append(neighbor)
                else:
                    if ((neighbor.elevation <= self.current.elevation or
                         self.current.elevation + 1 == neighbor.elevation) and
                            neighbor not in self.visited):
                        candidates.append(neighbor)
            if not candidates:
                stdscr.addch(self.current.x, self.current.y + 3, "@",
                    curses.color_pair(2))
                self.knows_what_to_do = False
                continue
            if self.stop_at_obstacles and type(destination) == str:
                destination_t = list(self.current)
                destination_t[0] += DIRECTIONS[destination][0]
                destination_t[1] += DIRECTIONS[destination][1]
                destination_t = tuple(destination_t)
                if destination_t in candidates:
                    self.current = Coordinate(*destination_t)
            else:
                sorted_candidates = sorted(candidates, key=lambda x: math.dist(x, destination))
                logger.debug(sorted_candidates)
                self.current = sorted_candidates[0]
            if self.current not in self.visited:
                self.visited.append(self.current)

START_POINT = Coordinate(20, 0)
FINAL_DESTINATION = Coordinate(20, 43)

class WalkingContest:

    def __init__(self, start, final_destination, reverse_rules):
        self.start = start
        self.final_destination = final_destination
        self.walkers = [WalkerWithMemory(self.start, stop_at_obstacles=True, reverse_rules=reverse_rules)]
        self.steps = 1
        self.iteration = 0
        self.counter = Counter()

    def did_we_win(self):
        for walker in self.walkers:
            if walker.current == self.final_destination:
                for coordinate in walker.visited:
                    stdscr.addch(coordinate.x, coordinate.y + 3, "%",
                        curses.color_pair(3))
                logger.error(f'solution found, length is {len(walker.visited) - 1}')
                stdscr.getkey()

    def did_we_win_part_two(self):
        for walker in self.walkers:
            if walker.current.elevation == ord('a'):
                for coordinate in walker.visited:
                    stdscr.addch(coordinate.x, coordinate.y + 3, "%",
                        curses.color_pair(3))
                logger.error(f'solution found, length is {len(walker.visited) - 1}')
                stdscr.getkey()

    def do_step(self):
        """
        brute force possible paths in 4 directions
        """
        newwalkers = []
        for walker in self.walkers:
            logger.debug(f"walker: {walker.current}")
            for direction in DIRECTIONS.keys():
                newwalker = copy.deepcopy(walker)
                newwalker.walk(direction, stop_at_steps=self.steps)
                newwalkers.append(newwalker)
        logger.error(len(newwalkers))
        self.walkers = []
        # pruning walkers to avoid computational explosion
        for walker in newwalkers:
            self.counter.update({walker.current: 1})
            # if we visited a tile 4 times than it make sense to never visit it again
            if self.counter[walker.current] < 4:
                self.walkers.append(walker)
        logger.error(len(self.walkers))
        logger.error('---')
        for walker in self.walkers:
            stdscr.addch(walker.current.x, walker.current.y + 3, "@",
                curses.color_pair(2))
        self.iteration += 1   


def main(stdscr):
    stdscr.clear()
    curses.start_color()
    curses.use_default_colors()
    curses.init_pair(1, curses.COLOR_RED, -1)
    curses.init_pair(2, curses.COLOR_BLUE, -1)
    curses.init_pair(3, curses.COLOR_YELLOW, -1)
    for number, line in enumerate(MAP):
        stdscr.addstr(number, 0, f"{number:2} {line}")
    stdscr.refresh()
    if '--one' in sys.argv:
        SWAMP = WalkingContest(START_POINT, FINAL_DESTINATION, reverse_rules=False)
        while True:
            SWAMP.do_step()
            SWAMP.did_we_win()
    if '--two' in sys.argv:
        MOUNTAIN = WalkingContest(FINAL_DESTINATION, START_POINT, reverse_rules=True)
        while True:
            MOUNTAIN.do_step()
            MOUNTAIN.did_we_win_part_two()

if __name__ == '__main__':
    stdscr = curses.initscr()
    curses.wrapper(main)
