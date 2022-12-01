#!/usr/bin/python3

# run it as
# ./1.py < inputs/1

maximum = 0
current = 0

while True:
    try:
        line = input()
        number = int(line.strip())
        current += number
    except (ValueError, EOFError) as e:
        if maximum < current:
            maximum = current
        if isinstance(e, EOFError):
            print(maximum)
            exit(0)
        current = 0
