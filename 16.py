inp = open('input16.txt').read().strip()

specs, your, tickets = inp.split('\n\n')
your = your.partition('\n')[2]
tickets = tickets.partition('\n')[2]

tickets = [[int(t) for t in ticket.split(',')] for ticket in tickets.split('\n')]
specs = [(s.partition(': ')[0], s.partition(': ')[2].split(' or ')) for s in specs.split('\n')]
specs = [(n, [(int(r.split('-')[0]), int(r.split('-')[1])) for r in rs]) for n, rs in specs]
your = [int(n) for n in your.split(',')]

all_ranges = []
for n, ranges in specs:
    all_ranges.extend(ranges)

def valid(v, ranges):
    return any(start <= v <= end for start, end in ranges)

# part 1
print(sum(t for ticket in tickets for t in ticket if not valid(t, all_ranges)))

# part 2
tickets = [your] + [ticket for ticket in tickets if all(valid(t, all_ranges) for t in ticket)]
candidates = [set(n for n, _ in specs) for _ in range(len(specs))]

for ticket in tickets:
    for i, t in enumerate(ticket):
        candidates[i] &= set(name for name, ranges in specs if valid(t, ranges))

while any(len(s) > 1 for s in candidates):
    for cs in [set(cs) for cs in candidates]:
        if len(cs) == 1:
            c = next(iter(cs))
            for i in range(len(candidates)):
                if len(candidates[i]) > 1:
                    candidates[i].discard(c)
candidates = [c.pop() for c in candidates]

from functools import reduce
print(reduce(lambda a,b: a*b, (your[i] for i, c in enumerate(candidates) if c.startswith('departure'))))
