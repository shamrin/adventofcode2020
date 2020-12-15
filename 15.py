inputs = [
'0,3,6',
'16,11,15,0,1,7',
]

def solve(ns, steps):
    c = {n: i for i, n in enumerate(ns)}
    last = ns[-1]
    for n in range(len(ns) - 1, steps - 1):
        next = n - c.get(last, n)
        c[last] = n
        last = next
    return last

for inp in inputs:
    ns = [int(n) for n in inp.split(',')]
    for steps in (2020, 30000000):
        print(f'{steps}: {solve(ns, steps)}')
