inputs = [
'0,3,6',
'16,11,15,0,1,7',
]

def solve(ns, steps):
    c = {}
    for i, n in enumerate(ns):
        c[n] = i
    last = ns[-1]
    for n in range(len(ns), steps):
        next = n - 1 - c.get(last, n - 1)
        c[last] = n - 1
        last = next
    return last

for inp in inputs:
    ns = [int(n) for n in inp.split(',')]
    for steps in (2020, 30000000):
        print(f'{steps}: {solve(ns, steps)}')
