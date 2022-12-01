#!/usr/bin/python3

import sys

maximum = 0
current = 0

for line in sys.stdin:
    try:
        number = int(line.strip())
        current += number
    except ValueError:
        if maximum < current:
            maximum = current
        current = 0
# finally, do the last one, we didn't detect it because it lacks ''
if maximum < current:
    maximum = current


print(maximum)
