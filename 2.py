#!/usr/bin/python3

# run it as
# ./2.py [ --one | --two ] < inputs/2

import sys

# fucking ugly
# should have normalized input data

CAN_DESTROY = {'A': 'Z',
               'B': 'X',
               'C': 'Y',
               'X': 'C',
               'Y': 'A',
               'Z': 'B'}
REVERSED_DESTROY = {value: key for key, value in CAN_DESTROY.items()}
VALUE = {'X': 1,
         'Y': 2,
         'Z': 3,
         'A': 1,
         'B': 2,
         'C': 3}

def compare(opponent, me):
    if CAN_DESTROY[me] == opponent:
        return 6
    elif CAN_DESTROY[opponent] == me:
        return 0
    else:
        return 3

def calc_round(opponent, desired_outcome):
    if desired_outcome == 'X':
        # do lose.
        me = [x for x in ('X', 'Y', 'Z') if x != REVERSED_DESTROY[opponent] and
            VALUE[x] != VALUE[opponent]][0]
        return VALUE[me]
    elif desired_outcome == 'Y':
        # a draw
        return VALUE[opponent] + 3
    elif desired_outcome == 'Z':
        # do win
        me = REVERSED_DESTROY[opponent]
        return VALUE[me] + 6

if '--one' in sys.argv:
    print(sum([compare(*line.split()) + VALUE[line.split()[1]] for line in sys.stdin]))
elif '--two' in sys.argv:
    print(sum([calc_round(*line.split()) for line in sys.stdin]))
