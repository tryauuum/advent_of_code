#!/usr/bin/python3

# run it as
# ./6.py [ --one | --two ] < inputs/6

import sys

buffer = []
bytes_read = 0
if '--one' in sys.argv:
    length = 4
else:
    length = 14

while True:
    char = sys.stdin.read(1)
    bytes_read += 1
    buffer.append(char)
    if len(buffer) == length + 1:
        del buffer[0]
    if len(buffer) == length and len(set(buffer)) == length:
        print(bytes_read)
        print(buffer)
        break
