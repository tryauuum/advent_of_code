#!/usr/bin/python3

# run it as
# ./10.py inputs/10 [--one | --two] [--debug]

import sys
import logging
if '--debug' in sys.argv:
    logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger()

def get_commands():
    with open(sys.argv[1]) as f:
        for line in f:
            line = line.strip().split()
            if len(line) == 1:
                yield [line[0],]
            else:
                yield [line[0], int(line[1])]

class Cpu:
    notable_cycles = (20, 60, 100, 140, 180, 220)

    def __init__(self, commands):
        self.current_cycle = 0
        self.register = 1
        self.input = commands
        self.current_command = None

    def do_cycle(self):
        if not self.current_command:
            self.current_command = next(self.input)
        out = self.increment_cycle_and_check_noteable()
        logger.info('cycle {}, running command {}'.format(
            self.current_cycle, self.current_command))
        if self.current_command[0] == 'noop':
            self.current_command = None
        elif self.current_command[0] == 'addx':
            self.current_command[0] = 'addx_progress'
        elif self.current_command[0] == 'addx_progress':
            self.register += self.current_command[1]
            self.current_command = None
        return out

    def increment_cycle_and_check_noteable(self):
        self.current_cycle += 1
        if self.current_cycle in self.notable_cycles:
            return self.current_cycle * self.register

    # def check_notable(self):
    #     if self.current_cycle in self.notable_cycles:
    #         return self.current_cycle * self.register


if __name__ == '__main__':
    cpu = Cpu(get_commands())
    if '--one' in sys.argv:
        the_sum = []
        while True:
            try: the_sum.append(cpu.do_cycle())
            except StopIteration: break
        print(sum(filter(None, the_sum)))
    elif '--two' in sys.argv:
        display = ''
        while True:
            if cpu.register -1 <= cpu.current_cycle % 40 <= cpu.register + 1:
                display += '#'
            else:
                display += '.'
            try: cpu.do_cycle()
            except StopIteration: break
        for line in range(6):
            print(display[line*40:line*40+40])
