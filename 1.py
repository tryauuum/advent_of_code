#!/usr/bin/python3

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
