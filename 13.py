#!/usr/bin/python3

# run it as
# ./13.py inputs/13 [--one | --two] [--debug]

import sys
import logging
from itertools import zip_longest
from functools import total_ordering
import math

if '--debug' in sys.argv:
    logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger()

EXTRA_PACKETS = [[[2]], [[6]]]

def gimme_pairs():
    with open(sys.argv[1]) as f:
        return zip(*[(eval(line.strip()) for line in f.readlines() if line.strip())]*2)

def gimme_packets():
    with open(sys.argv[1]) as f:
        return (eval(line.strip()) for line in f.readlines() if line.strip())


@total_ordering
class Packet:
    def __init__(self, value):
        self.value = value

    def __eq__(self, other):
        # is this even approved by Vatican?
        return str(self.value) == str(other.value)

    def __lt__(self, other):
        comp = compare(self.value, other.value)
        assert comp is not None
        return comp

    def __repr__(self):
        return repr(self.value)


def compare(left, right):
    """
    there probably is some cool math optimization to avoid all these steps
    """
    logger.info(f'left is {left}, right is {right}')
    if left is None:
        return True
    elif right is None:
        return False
    if type(left) == type(right) == list:
        # zip_longest puts "None" when out of items
        for pair in zip_longest(left, right):
            comp = compare(*pair)
            logger.info(comp)
            if comp is not None:
                return comp
    if type(left) != type(right):
        if type(left) == int:
            left = [left]
        elif type(right) == int:
            right = [right]
        return compare(left, right)
    if type(left) == type(right) == int:
        if left < right:
            return True
        elif left > right:
            return False
        else:
            return None

if __name__ == '__main__':
    if '--one' in sys.argv:
        indexes = []
        for index, pair in enumerate(gimme_pairs(), start=1):
            logger.info(pair)
            if Packet(pair[0]) < Packet(pair[1]):
                indexes.append(index)
        print('part one answer:', sum(indexes))
    if '--two' in sys.argv:
        packets = list(gimme_packets())
        for _ in EXTRA_PACKETS:
            packets.append(_)
        indexes = []
        for index, packet in enumerate(sorted([Packet(x) for x in packets]), start=1):
            logger.error(f'{index}, {packet}')
            if packet.value in EXTRA_PACKETS:
                indexes.append(index)
        print('part two answer:', math.prod(indexes))
