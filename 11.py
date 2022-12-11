#!/usr/bin/python3

# run it as
# ./11.py inputs/11 [--one | --two] [--debug]

import sys
import yaml
import pprint
import math

with open(sys.argv[1]) as f:
    monkeys = yaml.safe_load(f.read().replace('    If', '  If')# .replace('old * old', 'old')
        )
    for monkey in monkeys:
        b = monkeys[monkey]['Starting items']
        monkeys[monkey]['items'] = [b] if type(b) is int else list(eval(monkeys[monkey]['Starting items']))
        del monkeys[monkey]['Starting items']

        test = monkeys[monkey]['Test']
        assert 'divisible by ' in test
        monkeys[monkey]['test'] = int(test.split()[-1])
        del monkeys[monkey]['Test']

        monkeys[monkey][True] = 'Monkey ' + monkeys[monkey]['If true'].split()[-1]
        del monkeys[monkey]['If true']
        monkeys[monkey][False] = 'Monkey ' + monkeys[monkey]['If false'].split()[-1]
        del monkeys[monkey]['If false']

        monkeys[monkey]['inspect_count'] = 0
    if '--debug' in sys.argv:
        pprint.pprint(monkeys)



if '--one' in sys.argv:
    ROUNDS = 20
elif '--two' in sys.argv:
    ROUNDS = 10000

R = math.prod([x['test'] for x in monkeys.values()])

for _ in range(ROUNDS):
    for monkey in monkeys:
        while monkeys[monkey]['items']:
            old = monkeys[monkey]['items'].pop(0)
            exec(monkeys[monkey]['Operation'])
            monkeys[monkey]['inspect_count'] += 1
            if '--one' in sys.argv:
                new = new // 3
            if '--two' in sys.argv:
                # IT'S FUCKING AMUSING THAT IT DID WORK
                new = new % R
            dest = monkeys[monkey][new % monkeys[monkey]['test'] == 0]
            monkeys[dest]['items'].append(new)
    if '--debug' in sys.argv:
        print('round', _, [(x, len(monkeys[x]['items']), monkeys[x]['inspect_count']) for x in monkeys])

print(math.prod(sorted([monkey['inspect_count'] for monkey in monkeys.values()])[-2:]))
